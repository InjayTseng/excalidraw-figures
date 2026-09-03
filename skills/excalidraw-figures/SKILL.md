---
name: excalidraw-figures
description: Make inline figures for articles, READMEs and talks as editable Excalidraw files (hand-drawn look) from one bilingual Python spec, with an SVG preview, a headless-Chrome PNG, and a layout self-check. Triggers — "excalidraw figure", "畫圖用 excalidraw", "文章內圖", "inline figure", "diagram for the article", "把這段畫成圖", "中英各一張圖", "excalidraw template", "出圖".
license: MIT
metadata:
  version: "0.1"
---

# Excalidraw figures

One Python spec in → for every language: `<name>-<LANG>.excalidraw` (open and edit in Excalidraw or the Obsidian Excalidraw plugin), `<name>-<LANG>.svg` (approximate preview), `<name>-<LANG>.png` (what a reader actually sees, rendered by headless Chrome). Labels are written once as `{"en": ..., "zh": ...}` so the two language versions never drift.

Use this when a reader will learn more from a picture than from the paragraph, and the piece's voice is personal or editorial rather than corporate. For a clinical, print-style figure system, `cathrynlavery/diagram-design` is the alternative; this skill exists because hand-drawn Excalidraw reads warmer inline and stays editable by the author afterwards.

## Workflow

1. **Decide the one idea per figure.** Write the sentence the figure must make obvious. If the sentence is already obvious, do not draw. One figure = one contrast, one flow, or one structure. Budget: ≤ 10 boxes, ≤ 12 arrows, ≤ 3 fill colours plus white.
2. **Copy the template spec.** `cp templates/spec-template.py my-figures.py`. Each figure is a function `fn(lang) -> Diagram`; list them in `DIAGRAMS`. Read `references/style.md` for the palette roles and sizing rules before writing labels.
3. **Write labels bilingually.** Every user-visible string is `{"en": "...", "zh": "..."}`. Keep protocol tokens, code identifiers and file names identical in both (`LOOP_RESULT`, `main`, `claude -p`). Break any line longer than ~26 CJK characters or ~45 Latin characters; the width budget is 1em per CJK glyph and 0.55em per Latin glyph.
4. **Build with the check on.**
   ```bash
   python3 scripts/excalidraw_lib.py my-figures.py --out figures/ --png --check
   ```
   The check reports text outside the canvas, text wider than its box, text overlapping text, and free text straddling a box edge. Fix every issue; do not ship with warnings.
5. **Look at the PNGs.** The check is an estimate; fonts differ. Open each `.png` (or read it with an image-capable tool) and look for: labels sitting on arrow lines, arrows crossing headings, boxes touching. Move labels with `mid=(x, y)`; route arrows with `path([...])` around text.
6. **Reference the PNG in the article** (`![](figures/<name>-EN.png)`), keep the `.excalidraw` next to it for later hand edits, and commit the spec so the figure can be regenerated when the text changes.

## Spec API (scripts/excalidraw_lib.py)

| Call | Purpose |
|---|---|
| `Diagram(name, w, h, lang)` | One figure. Typical inline size 1000×560; taller for stacks (1000×600–640) |
| `d.title(label, fs=24, sub=None)` | Header at top-left; subtitle in grey |
| `d.box(x, y, w, h, label, bg, shape, stroke, dashed, fs)` | Rectangle (default), `"diamond"` for decisions, `"ellipse"`. Label centred, multi-line with `\n`. Snapped to a 4px grid |
| `d.frame(x, y, w, h, label)` | Dashed grey grouping frame with a caption |
| `d.arrow(x1, y1, x2, y2, label, dashed, color, mid)` | Straight arrow; label 18px above the midpoint unless `mid` is given |
| `d.path([(x,y), ...], label, dashed, mid)` | Orthogonal polyline arrow for back-edges and detours; always pass `mid` for the label |
| `d.text(x, y, label, fs, color, align)` | Free text; `align="center"` treats `x` as the centre |
| `d.L(label)` | Resolve a bilingual label inside your own code |
| `d.check()` | Returns a list of layout issues (also run by `--check`) |

Colours: `GATE` (yellow) for decisions and gates, `AGENT` (blue) for models, agents and fresh context, `FAIL` (red) for incidents, failures and human-only steps, `FIX` (green) for fixes and outcomes, `NOTE` (white) for files, evidence and callouts. Grey `GRAY` for captions, `LIGHT` for frames. Never use more than three fills in one figure.

## Rules and edge cases

- **Label placement is the most common defect.** A `path()` label defaults to the middle waypoint, which is usually a vertical segment; pass `mid` on a horizontal segment. Never let a label sit on a line.
- **Chinese runs wider than the estimate on some fonts.** If a ZH label is within 10% of the box width, wrap it. Prefer wrapping to shrinking font size; 13px is the floor for CJK.
- **Arrows must not cross headings or other boxes.** Route with `path()` around them, or move the heading. A dashed arrow through a section title reads as a mistake.
- **Excalidraw font for CJK.** `fontFamily: 1` (Virgil/Excalifont) has no CJK glyphs; Excalidraw substitutes its bundled Xiaolai handwriting font, so the file looks right inside Excalidraw. The SVG preview uses system fonts and is only an approximation; trust the PNG and Excalidraw itself, not the SVG.
- **No Chrome.** PNG export needs Google Chrome or Chromium; set `CHROME_BIN` if it is not in `/Applications`. Without it the script still writes `.excalidraw` and `.svg`. Do not use `qlmanage` thumbnails as a proxy; they rescale and crop.
- **Existing files are overwritten** by name and language. Version by changing `name` if you need to keep an old render.
- **One idea per figure.** If the check passes but the figure needs a paragraph to explain, split it.
- **Do not hand-edit generated `.excalidraw` files that you still intend to regenerate.** Either the spec or the file is the source of truth; pick one per figure and say which in the article's source comment.

## Verification

- `python3 scripts/excalidraw_lib.py my-figures.py --out /tmp/fig --png --check` exits 0.
- Every `.excalidraw` parses as JSON with `type: excalidraw`, `version: 2`, unique element ids.
- You looked at every PNG.

## Example

`examples/loop-engineering/spec.py` holds the five figures of the article "Agents Only Build What You Measure" (flow with two gates, driver vs agent, five defence layers, a stop rule that never fired, a nine-node perpetual loop), EN and ZH from one spec. `templates/components.py` renders a component sheet showing every box kind, arrow style and label size at once; open `templates/components-EN.excalidraw` in Excalidraw to copy pieces by hand.
