#!/usr/bin/env python3
"""excalidraw_lib — build hand-drawn-style article figures as editable Excalidraw files from one
bilingual Python spec, with an SVG preview, a real-browser PNG, and a layout self-check.

    python3 excalidraw_lib.py my_spec.py --out figures/ --png --check

A spec is a Python file that defines `DIAGRAMS = [fn, ...]`, where each fn(lang) returns a Diagram.
Every label may be a plain string or a dict {"en": ..., "zh": ...}; the CLI builds one file set per
language (default: en, zh). Outputs per diagram: <name>-<LANG>.excalidraw (open in Excalidraw or the
Obsidian plugin), <name>-<LANG>.svg (approximate preview), <name>-<LANG>.png (headless Chrome render).

Schema mirrors what Excalidraw 0.17+ writes (type "excalidraw", version 2): fontFamily 1 (Virgil /
Excalifont, CJK falls back to Xiaolai inside Excalidraw), roughness 1, the default Excalidraw palette.
"""
from __future__ import annotations
import argparse, html, importlib.util, json, math, os, pathlib, random, shutil, subprocess, sys

# ---- palette (Excalidraw defaults) and semantic aliases ------------------------------------------
INK, GRAY, LIGHT = "#1e1e1e", "#495057", "#868e96"
BLUE, RED, YELLOW, GREEN, WHITE, PURPLE = "#a5d8ff", "#ffc9c9", "#ffec99", "#b2f2bb", "#ffffff", "#d0bfff"
TRANSPARENT = "transparent"
GATE, AGENT, FAIL, FIX, NOTE, HUMAN = YELLOW, BLUE, RED, GREEN, WHITE, RED   # semantic roles → fills

CHROME_CANDIDATES = [os.environ.get("CHROME_BIN", ""),
                     "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                     "/Applications/Chromium.app/Contents/MacOS/Chromium",
                     shutil.which("google-chrome") or "", shutil.which("chromium") or ""]

def _rid(rng): return "".join(rng.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(16))
def is_cjk(c: str) -> bool: return ord(c) > 0x2E7F
def text_width(s: str, fs: float) -> float:
    """Width budget: 1em per CJK/full-width glyph, 0.55em per Latin glyph (Virgil is narrow)."""
    return sum(fs if is_cjk(c) else fs * 0.55 for c in s)
def snap(v: float, grid: int = 4) -> int: return int(round(v / grid) * grid)


class Diagram:
    """One figure. Coordinates are Excalidraw scene units (px). Origin top-left."""
    def __init__(self, name: str, w: int, h: int, lang: str = "en", grid: int = 4, seed: int = 20260903):
        self.name, self.w, self.h, self.lang, self.grid = name, w, h, lang, grid
        self.els: list[dict] = []
        self._rng = random.Random(f"{name}-{lang}-{seed}")
        self._texts: list[tuple] = []   # (x, y, w, h, s, container_box or None) for check()
        self._boxes: list[tuple] = []   # (x, y, w, h)

    # ---- helpers
    def L(self, label):
        """Resolve a bilingual label for this diagram's language."""
        if isinstance(label, dict):
            return label.get(self.lang) or label.get("en") or next(iter(label.values()))
        return label

    def _base(self, t, x, y, w, h, **kw):
        e = dict(id=_rid(self._rng), type=t, x=x, y=y, width=w, height=h, angle=0, strokeColor=INK,
                 backgroundColor=TRANSPARENT, fillStyle="solid", strokeWidth=2, strokeStyle="solid",
                 roughness=1, opacity=100, groupIds=[], frameId=None, roundness=None,
                 seed=self._rng.randint(1, 2**31), version=1, versionNonce=self._rng.randint(1, 2**31),
                 isDeleted=False, boundElements=None, updated=1756900000000, link=None, locked=False)
        e.update(kw); return e

    # ---- primitives
    def text(self, x, y, label, fs=16, color=INK, align="left", w=None, container=None):
        """Free text. align="center" treats x as the centre. Returns (x, y, w, h)."""
        s = self.L(label); lines = s.split("\n")
        width = w or max(text_width(l, fs) for l in lines); height = fs * 1.25 * len(lines)
        if align == "center": x = x - width / 2
        self.els.append(self._base("text", x, y, width, height, strokeColor=color, text=s, fontSize=fs, fontFamily=1,
                                   textAlign=align, verticalAlign="top", containerId=None, originalText=s, lineHeight=1.25, baseline=fs))
        self._texts.append((x, y, width, height, s, container))
        return x, y, width, height

    def box(self, x, y, w, h, label=None, bg=TRANSPARENT, shape="rectangle", stroke=INK, dashed=False, fs=16, tcolor=INK):
        """Rectangle / diamond / ellipse with a centred multi-line label. Snapped to the grid."""
        x, y, w, h = snap(x, self.grid), snap(y, self.grid), snap(w, self.grid), snap(h, self.grid)
        self.els.append(self._base(shape, x, y, w, h, strokeColor=stroke, backgroundColor=bg,
                                   strokeStyle="dashed" if dashed else "solid",
                                   roundness={"type": 3} if shape == "rectangle" else None))
        self._boxes.append((x, y, w, h))
        if label:
            s = self.L(label); n = s.count("\n") + 1; th = fs * 1.25 * n
            self.text(x + w / 2, y + (h - th) / 2, s, fs, tcolor, "center", container=(x, y, w, h))
        return x, y, w, h

    def arrow(self, x1, y1, x2, y2, label=None, dashed=False, color=INK, fs=13, mid=None):
        """Straight arrow. Optional label 24px above the midpoint (or at `mid`)."""
        self.els.append(self._base("arrow", x1, y1, abs(x2 - x1), abs(y2 - y1), strokeColor=color,
                                   strokeStyle="dashed" if dashed else "solid", points=[[0, 0], [x2 - x1, y2 - y1]],
                                   lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None,
                                   endArrowhead="arrow", roundness={"type": 2}))
        if label:
            mx, my = mid or ((x1 + x2) / 2, (y1 + y2) / 2 - 24); self.text(mx, my, label, fs, GRAY, "center")

    def path(self, pts, label=None, dashed=False, color=INK, fs=13, mid=None):
        """Polyline arrow through pts. Put the label with `mid`, never on a vertical segment."""
        x0, y0 = pts[0]; xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        self.els.append(self._base("arrow", x0, y0, max(xs) - min(xs), max(ys) - min(ys), strokeColor=color,
                                   strokeStyle="dashed" if dashed else "solid", points=[[x - x0, y - y0] for x, y in pts],
                                   lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None,
                                   endArrowhead="arrow", roundness=None))
        if label:
            mx, my = mid or pts[len(pts) // 2]; self.text(mx, my - 24, label, fs, GRAY, "center")

    def title(self, label, fs=24, sub=None, sub_fs=18):
        """Standard header: title at (30, 20), optional grey subtitle under it."""
        self.text(30, 20, label, fs)
        if sub: self.text(30, 20 + fs * 1.25 + 14, sub, sub_fs, GRAY)

    def frame(self, x, y, w, h, label=None, fs=15):
        """Dashed grey grouping frame with an optional caption inside the top-left corner."""
        self.box(x, y, w, h, None, TRANSPARENT, stroke=LIGHT, dashed=True)
        if label: self.text(x + 20, y + 12, label, fs, GRAY)

    # ---- self-check
    def check(self) -> list[str]:
        """Estimated-bbox layout check: text outside canvas, text overflowing its box, text/text overlap."""
        issues = []
        def inter(a, b):
            ax, ay, aw, ah = a; bx, by, bw, bh = b
            return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah
        for (x, y, w, h, s, c) in self._texts:
            if x < 0 or y < 0 or x + w > self.w or y + h > self.h:
                issues.append(f'text outside canvas: "{s[:40]}" at ({x:.0f},{y:.0f}) size {w:.0f}x{h:.0f}')
            if c and (x < c[0] + 4 or x + w > c[0] + c[2] - 4):
                issues.append(f'text wider than its box: "{s[:40]}" ({w:.0f}px in a {c[2]}px box) — wrap it or widen the box')
        for i, a in enumerate(self._texts):
            for b in self._texts[i + 1:]:
                if inter(a[:4], b[:4]):
                    issues.append(f'text overlaps text: "{a[4][:30]}" ↔ "{b[4][:30]}"')
        for (x, y, w, h, s, c) in self._texts:
            if c: continue
            for bx in self._boxes:
                if inter((x, y, w, h), bx) and not (x >= bx[0] and x + w <= bx[0] + bx[2] and y >= bx[1] and y + h <= bx[1] + bx[3]):
                    issues.append(f'free text straddles a box edge: "{s[:30]}" vs box at ({bx[0]},{bx[1]})')
        return issues

    # ---- outputs
    def excalidraw(self) -> dict:
        return {"type": "excalidraw", "version": 2, "source": "excalidraw-figures", "elements": self.els,
                "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"}, "files": {}}

    def svg(self) -> str:
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
             "font-family=\"'Comic Sans MS', 'Segoe Print', 'PingFang TC', 'Noto Sans TC', sans-serif\">"
             '<rect width="100%" height="100%" fill="#fff"/>',
             '<defs><marker id="ah" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>']
        for e in self.els:
            t = e["type"]; dash = ' stroke-dasharray="8 6"' if e["strokeStyle"] == "dashed" else ""
            if t == "rectangle":
                o.append(f'<rect x="{e["x"]}" y="{e["y"]}" width="{e["width"]}" height="{e["height"]}" rx="10" fill="{e["backgroundColor"]}" stroke="{e["strokeColor"]}" stroke-width="2"{dash}/>')
            elif t == "ellipse":
                o.append(f'<ellipse cx="{e["x"]+e["width"]/2}" cy="{e["y"]+e["height"]/2}" rx="{e["width"]/2}" ry="{e["height"]/2}" fill="{e["backgroundColor"]}" stroke="{e["strokeColor"]}" stroke-width="2"{dash}/>')
            elif t == "diamond":
                x, y, w, h = e["x"], e["y"], e["width"], e["height"]
                o.append(f'<polygon points="{x+w/2},{y} {x+w},{y+h/2} {x+w/2},{y+h} {x},{y+h/2}" fill="{e["backgroundColor"]}" stroke="{e["strokeColor"]}" stroke-width="2"{dash}/>')
            elif t == "arrow":
                pts = " ".join(f'{e["x"]+px},{e["y"]+py}' for px, py in e["points"])
                o.append(f'<polyline points="{pts}" fill="none" stroke="{e["strokeColor"]}" stroke-width="2" marker-end="url(#ah)"{dash}/>')
            elif t == "text":
                fs = e["fontSize"]; anchor = "middle" if e["textAlign"] == "center" else "start"
                tx = e["x"] + (e["width"] / 2 if anchor == "middle" else 0)
                for i, l in enumerate(e["text"].split("\n")):
                    o.append(f'<text x="{tx}" y="{e["y"] + fs + i * fs * 1.25}" font-size="{fs}" fill="{e["strokeColor"]}" text-anchor="{anchor}">{html.escape(l)}</text>')
        o.append("</svg>"); return "\n".join(o)

    def write(self, out: pathlib.Path, png: bool = False) -> pathlib.Path:
        out.mkdir(parents=True, exist_ok=True)
        stem = out / f"{self.name}-{self.lang.upper()}"
        stem.with_suffix(".excalidraw").write_text(json.dumps(self.excalidraw(), ensure_ascii=False, indent=1), encoding="utf-8")
        stem.with_suffix(".svg").write_text(self.svg(), encoding="utf-8")
        if png:
            chrome = next((c for c in CHROME_CANDIDATES if c and pathlib.Path(c).exists()), None)
            if not chrome:
                print(f"  ! no Chrome found for PNG render of {stem.name}; set CHROME_BIN", file=sys.stderr)
            else:
                subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={self.w},{self.h}",
                                f"--screenshot={stem.with_suffix('.png')}", f"file://{stem.with_suffix('.svg').resolve()}"], capture_output=True)
        return stem


def load_spec(path: str):
    spec_path = pathlib.Path(path).resolve()
    sys.path.insert(0, str(spec_path.parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    s = importlib.util.spec_from_file_location(spec_path.stem, spec_path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    if not hasattr(m, "DIAGRAMS"): sys.exit("spec must define DIAGRAMS = [fn(lang) -> Diagram, ...]")
    return m


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build Excalidraw figures from a bilingual spec.")
    ap.add_argument("spec"); ap.add_argument("--out", default="figures"); ap.add_argument("--png", action="store_true")
    ap.add_argument("--check", action="store_true", help="run the layout self-check and exit 1 on issues")
    ap.add_argument("--lang", default="en,zh", help="comma-separated languages to build (default en,zh)")
    a = ap.parse_args(argv); m = load_spec(a.spec); out = pathlib.Path(a.out); langs = [l.strip() for l in a.lang.split(",") if l.strip()]
    langs = getattr(m, "LANGS", langs); bad = 0
    for fn in m.DIAGRAMS:
        for lang in langs:
            d = fn(lang); stem = d.write(out, png=a.png)
            issues = d.check() if a.check else []
            bad += len(issues)
            print(f"{stem.name}: {len(d.els)} elements" + (f" · {len(issues)} issue(s)" if a.check else ""))
            for i in issues: print("   -", i)
    if a.check and bad: sys.exit(1)

if __name__ == "__main__":
    main()
