"""Template spec for excalidraw-figures. Copy, rename, edit the labels, run:

    python3 <skill>/scripts/excalidraw_lib.py my-figures.py --out figures/ --png --check

Each function takes a language code and returns a Diagram. List them in DIAGRAMS.
Every visible string is bilingual: {"en": ..., "zh": ...}. Code tokens stay identical.
"""
from excalidraw_lib import Diagram, GATE, AGENT, FAIL, FIX, NOTE, GRAY, INK

def before_after(lang):
    d = Diagram("F1-before-after", 1000, 520, lang)
    d.title({"en": "State the claim here, not the topic", "zh": "標題寫論點，不寫主題"})
    # row 1 — the way it was
    d.text(30, 80, {"en": "BEFORE · one gate", "zh": "之前 · 一道閘門"}, 16, GRAY)
    d.box(30, 110, 150, 60, {"en": "step A", "zh": "步驟 A"})
    d.arrow(180, 140, 230, 140)
    d.box(230, 100, 170, 80, {"en": "the only\ncheck", "zh": "唯一的\n檢查"}, GATE, "diamond", fs=15)
    d.arrow(400, 140, 450, 140)
    d.box(450, 110, 150, 60, {"en": "ship", "zh": "出貨"})
    d.path([(525, 170), (525, 215), (105, 215), (105, 170)], {"en": "next round", "zh": "下一輪"}, mid=(315, 215))
    d.box(660, 100, 310, 80, {"en": "what went wrong, in one line,\nwith the number that proves it", "zh": "出了什麼事，一行寫完，\n附上證明它的數字"}, FAIL, fs=14)
    # row 2 — the way it is now
    d.text(30, 280, {"en": "AFTER · judge before you build", "zh": "之後 · 動工前先判斷"}, 16, GRAY)
    d.box(30, 320, 130, 60, {"en": "idea", "zh": "想法"})
    d.arrow(160, 350, 200, 350)
    d.box(200, 310, 150, 80, {"en": "worth it?", "zh": "值得嗎？"}, GATE, "diamond", fs=15)
    d.arrow(350, 350, 390, 350, {"en": "yes", "zh": "是"})
    d.box(390, 320, 130, 60, {"en": "build", "zh": "開發"})
    d.arrow(520, 350, 560, 350)
    d.box(560, 310, 150, 80, {"en": "does what\nit says?", "zh": "做的事等於\n承諾嗎？"}, GATE, "diamond", fs=14)
    d.arrow(710, 350, 750, 350, {"en": "yes", "zh": "是"})
    d.box(750, 320, 130, 60, {"en": "ship", "zh": "出貨"})
    d.text(275, 400, {"en": "no → try another (≤2)", "zh": "否 → 換一個（≤2）"}, 12, GRAY, "center")
    d.text(635, 400, {"en": "no → fix (≤3)", "zh": "否 → 修（≤3）"}, 12, GRAY, "center")
    d.box(60, 440, 400, 56, {"en": "independent judges, fresh context, not the author", "zh": "獨立的判斷者、獨立的 Context、不是作者"}, AGENT, fs=14)
    d.box(520, 440, 420, 56, {"en": "measure only correctness → correct, worthless work\nmeasure value first → rejected before any code", "zh": "只量正確性 → 正確但沒價值\n先量價值 → 寫 Code 前就被拒"}, NOTE, fs=13)
    return d

DIAGRAMS = [before_after]
