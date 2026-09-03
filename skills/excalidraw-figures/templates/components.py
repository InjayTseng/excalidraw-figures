"""Component sheet: every box kind, arrow style, frame and label size on one canvas.
Open the generated components-EN.excalidraw in Excalidraw and copy pieces by hand, or read it as
the visual contract for the library. Build: python3 ../scripts/excalidraw_lib.py components.py --out . --png --check
"""
from excalidraw_lib import Diagram, GATE, AGENT, FAIL, FIX, NOTE, GRAY, LIGHT, INK, TRANSPARENT

def components(lang):
    d = Diagram("components", 1000, 620, lang)
    d.title({"en": "excalidraw-figures · component sheet", "zh": "excalidraw-figures · 元件範本"},
            sub={"en": "three fills + white per figure · 4px grid · labels never on lines", "zh": "每張圖最多三色加白 · 4px 網格 · 標籤不壓線"})
    # boxes
    d.text(30, 110, {"en": "BOXES", "zh": "方塊"}, 14, GRAY)
    d.box(30, 140, 150, 60, {"en": "plain step", "zh": "一般步驟"})
    d.box(200, 130, 170, 80, {"en": "gate / decision", "zh": "閘門／判斷"}, GATE, "diamond", fs=14)
    d.box(390, 140, 150, 60, {"en": "agent / model", "zh": "Agent／模型"}, AGENT)
    d.box(560, 140, 150, 60, {"en": "failure / human", "zh": "失敗／人"}, FAIL)
    d.box(730, 140, 150, 60, {"en": "fix / outcome", "zh": "修法／結果"}, FIX)
    d.box(30, 230, 150, 60, {"en": "file / note", "zh": "檔案／註記"}, NOTE)
    d.box(200, 230, 150, 60, {"en": "optional", "zh": "可選"}, TRANSPARENT, dashed=True)
    d.box(370, 230, 170, 60, {"en": "two-line label\nsecond line", "zh": "兩行標籤\n第二行"}, fs=14)
    d.box(560, 230, 100, 60, {"en": "ellipse", "zh": "橢圓"}, TRANSPARENT, "ellipse", fs=14)
    # frame
    d.frame(690, 220, 280, 90, {"en": "dashed frame · caption inside", "zh": "虛線框 · 說明在框內"})
    d.box(710, 254, 110, 44, {"en": "inside", "zh": "框內"}, fs=14)
    d.box(840, 254, 110, 44, {"en": "inside", "zh": "框內"}, fs=14)
    # arrows
    d.text(30, 330, {"en": "ARROWS", "zh": "箭頭"}, 14, GRAY)
    d.arrow(30, 380, 230, 380, {"en": "solid · primary flow", "zh": "實線 · 主流程"})
    d.arrow(270, 380, 470, 380, {"en": "dashed · optional / return", "zh": "虛線 · 可選／回邊"}, dashed=True)
    d.path([(510, 380), (510, 420), (700, 420), (700, 380)], {"en": "path · label on the horizontal run", "zh": "路徑 · 標籤放在水平段"}, mid=(605, 420))
    d.arrow(740, 380, 960, 380, {"en": "grey · secondary", "zh": "灰 · 次要"}, color=GRAY)
    # text sizes
    d.text(30, 460, {"en": "TEXT", "zh": "文字"}, 14, GRAY)
    d.text(30, 486, {"en": "24 title", "zh": "24 標題"}, 24)
    d.text(200, 492, {"en": "18 section", "zh": "18 節標"}, 18, GRAY)
    d.text(360, 496, {"en": "16 box label", "zh": "16 方塊標籤"}, 16)
    d.text(540, 498, {"en": "13 arrow label / caption", "zh": "13 箭頭標籤／說明"}, 13, GRAY)
    d.text(30, 540, {"en": "width budget: 1em per CJK glyph, 0.55em per Latin glyph · CJK floor 13px · wrap, don't shrink",
                     "zh": "寬度預算：CJK 一字 1em、拉丁字 0.55em · CJK 最小 13px · 寧可換行，不要縐字"}, 13, GRAY)
    return d

DIAGRAMS = [components]
