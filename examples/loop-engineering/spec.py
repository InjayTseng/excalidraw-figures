"""Five figures for the article "Agents Only Build What You Measure" (loop-engineering-on-product),
EN and ZH from one spec. Build: python3 ../../skills/excalidraw-figures/scripts/excalidraw_lib.py spec.py --out out --png --check
"""
from excalidraw_lib import Diagram, INK, GRAY, LIGHT, BLUE, RED, YELLOW, GREEN, WHITE

# ----------------------------------------------------------------------------------------------------- D1
def d1(lang):
    d = Diagram("D1-gates-are-the-objective", 1000, 560, lang)
    d.text(30, 20, {"en": "A loop maximizes whatever its gates measure", "zh": "Loop 只會最大化它量得到的東西"}, 24)
    # left: v1
    d.text(30, 70, {"en": "V1 · one gate", "zh": "V1 · 一道閘門"}, 18, GRAY)
    d.box(30, 110, 130, 60, {"en": "spec\n(PRP)", "zh": "規格\n(PRP)"})
    d.arrow(160, 140, 200, 140)
    d.box(200, 110, 130, 60, {"en": "build", "zh": "開發"})
    d.arrow(330, 140, 370, 140)
    d.box(370, 100, 150, 80, {"en": "tests\npass?", "zh": "測試\n過了嗎？"}, YELLOW, "diamond", fs=15)
    d.arrow(520, 140, 560, 140)
    d.box(560, 110, 130, 60, {"en": "ship", "zh": "出貨"})
    d.path([(625, 170), (625, 215), (95, 215), (95, 170)])
    d.text(360, 222, {"en": "Builder runs the tests, declares them passed, marks COMPLETED, pushes main",
                      "zh": "Builder 自己跑測試、自己判通過、自己標 COMPLETED、直接推 main"}, 13, GRAY, "center")
    d.box(720, 95, 250, 100, {"en": "iOS health app, overnight:\n31 of 35 rounds added\nthe same HealthKit metric",
                              "zh": "iOS 健康 App 過夜：\n35 輪有 31 輪\n在加同一種 HealthKit 指標"}, RED, fs=14)
    # right: v2+
    d.text(30, 280, {"en": "V2+ · value before build, validation after", "zh": "V2+ · 動工前擋價值，完工後擋驗證"}, 18, GRAY)
    d.box(30, 330, 110, 60, {"en": "research", "zh": "研究"})
    d.arrow(140, 360, 175, 360)
    d.box(175, 320, 130, 80, {"en": "value\ngate", "zh": "價值閘"}, YELLOW, "diamond", fs=15)
    d.arrow(305, 360, 340, 360)
    d.box(340, 330, 110, 60, {"en": "PRD\n(+CLAIM, V3)", "zh": "PRD\n（V3 加 CLAIM）"}, fs=13)
    d.arrow(450, 360, 485, 360)
    d.box(485, 330, 100, 60, {"en": "build", "zh": "開發"})
    d.arrow(585, 360, 615, 360)
    d.box(615, 320, 130, 80, {"en": "validator\nvs PRD", "zh": "驗證閘\n對 PRD"}, YELLOW, "diamond", fs=14)
    d.arrow(745, 360, 780, 360)
    d.box(780, 330, 100, 60, {"en": "ship", "zh": "出貨"})
    d.path([(830, 390), (830, 440), (85, 440), (85, 390)])
    d.text(240, 404, {"en": "REJECT → redirect (≤2)", "zh": "REJECT → 換角度（≤2）"}, 12, GRAY, "center")
    d.text(680, 404, {"en": "FAIL → fix (≤3) or back to PRD", "zh": "FAIL → 修（≤3）或回 PRD"}, 12, GRAY, "center")
    d.box(60, 470, 400, 62, {"en": "independent agents, fresh context, no authorship",
                             "zh": "獨立 Agent、獨立 Context、不是作者"}, BLUE, fs=14)
    d.box(520, 470, 420, 62, {"en": "measure only correctness → correct, worthless features\nmeasure value first → 17 ideas rejected before any code",
                              "zh": "只量正確性 → 正確但沒價值的功能\n先量價值 → 17 個想法在寫 Code 前就被拒"}, WHITE, fs=13)
    return d

# ----------------------------------------------------------------------------------------------------- D2
def d2(lang):
    d = Diagram("D2-judgment-vs-control-flow", 1000, 560, lang)
    d.text(30, 20, {"en": "Judgment goes to agents. Control flow goes to a script.", "zh": "判斷交給 Agent，控制流交給腳本"}, 24)
    d.box(30, 70, 560, 400, None, "transparent", stroke=LIGHT, dashed=True)
    d.text(50, 82, {"en": "driver · run-loop.sh · deterministic · never reasons", "zh": "Driver · run-loop.sh · Deterministic · 從不推理"}, 15, GRAY)
    d.box(60, 120, 200, 50, {"en": "for round in 1..N", "zh": "for round in 1..N"}, fs=15)
    d.arrow(160, 170, 160, 205)
    d.box(60, 205, 480, 110, {"en": "fresh claude -p round\nresearch → value gate → PRD → build → validate → ship\n(in-round VALUE / BUILD / VERDICT routed by the agent itself)",
                              "zh": "全新的 claude -p 一輪\n研究 → 價值閘 → PRD → 開發 → 驗證 → 出貨\n（輪內的 VALUE／BUILD／VERDICT 由當輪 Agent 自己路由）"}, BLUE, fs=14)
    d.arrow(300, 315, 300, 350)
    d.box(60, 350, 480, 44, {"en": "LOOP_RESULT: SHIPPED | category=… | rejects=N", "zh": "LOOP_RESULT: SHIPPED | category=… | rejects=N"}, YELLOW, fs=14)
    d.text(300, 400, {"en": "the only line the driver reads (plus TRAJ / AUDIT / POSITION)", "zh": "Driver 唯一讀的一行（加 TRAJ／AUDIT／POSITION）"}, 12, GRAY, "center")
    d.path([(540, 372), (570, 372), (570, 145), (260, 145)], {"en": "parse → flags · stop? · hand to whom?", "zh": "Parse → 旗標、停不停、交給誰"}, fs=12, mid=(415, 140))
    # right: state in files
    d.box(630, 70, 340, 230, None, "transparent", stroke=LIGHT, dashed=True)
    d.text(650, 82, {"en": "all state in files (mostly git)", "zh": "狀態全在檔案裡（多數進 Git）"}, 15, GRAY)
    for i, lab in enumerate(["product/positioning.md", "product/state.md", "_idea_ledger.md · _product_backlog.md", "PRPs/*.md · research/briefs/*.md", ".loop/loop.log"]):
        d.box(650, 112 + i * 36, 300, 30, lab, WHITE, fs=13)
    d.arrow(590, 260, 630, 260, None, True); d.arrow(630, 240, 590, 240, None, True)
    # bottom right: why
    d.box(630, 330, 340, 140, {"en": "fresh context per round → nothing accumulates\nstate in files → resume after a crash\none result line per gate → a human can audit\ndeterministic driver → test it with a stub",
                               "zh": "每輪 Fresh Context → 什麼都不累積\n狀態在檔案 → 半夜當掉可續跑\n每個閘吐一行 → 人看得懂、可審計\nDriver 是 Deterministic → 可以用 Stub 測"}, GREEN, fs=13)
    d.text(500, 500, {"en": "the model decides what; the script decides whether and when", "zh": "模型決定「做什麼」，腳本決定「要不要、什麼時候」"}, 15, GRAY, "center")
    return d

# ----------------------------------------------------------------------------------------------------- D3
def d3(lang):
    d = Diagram("D3-layered-defenses", 1000, 600, lang)
    d.text(30, 20, {"en": "Nobody grades their own homework: five layers, each catches one failure class", "zh": "驗收不能是自己人：五層防禦，各抓一種失敗"}, 22)
    rows = [
        ({"en": "value gate\n(before build)", "zh": "價值閘\n（動工前）"}, {"en": "an idea that moves nothing on the funnel", "zh": "推不動漏斗任何一段的想法"},
         {"en": "a second draw button at the end of a section:\nsame mechanism already exists → rejected", "zh": "流年段末尾再放一顆求籤按鈕：\n同機制已存在，拒"}),
        ({"en": "category\ndiversity", "zh": "類別\n多樣性"}, {"en": "surface repetition inside one category", "zh": "同一類別裡的表面重複"},
         {"en": "prompt carries the last 4 categories;\nthe loop must change direction", "zh": "Prompt 帶最近 4 輪類別，\n逼它換方向"}),
        ({"en": "trajectory\nmonitor", "zh": "軌跡\n監測"}, {"en": "same trick across different categories", "zh": "不同類別、同一招的 meta 同質"},
         {"en": "every 5 rounds, on recent commits:\nCONTINUE / REDIRECT / STOP", "zh": "每 5 輪看最近 Commit：\nCONTINUE／REDIRECT／STOP"}),
        ({"en": "trust gate\n(overrides impact)", "zh": "信任閘\n（蓋過 Impact）"}, {"en": "a fabricated signal that would work", "zh": "「有效」的捏造訊號"},
         {"en": "\"N people cast a reading today\", N from a hash:\nshipped once, now rejected", "zh": "「今日已有 N 人起盤」，N 是 Hash 算的：\n曾出貨，現在拒"}),
        ({"en": "label-promise\n(validator axis 4)", "zh": "Label-promise\n（驗證第 4 軸）"}, {"en": "correct code that breaks the label's promise", "zh": "Code 正確但沒兌現 Label 承諾"},
         {"en": "\"draw a stick?\" button only preselected & scrolled:\nbuild green, validator PASS, user: nothing", "zh": "「問一籤？」按鈕只預選類別並捲動：\nBuild 綠、Validator PASS、用戶：沒反應"}),
    ]
    d.text(120, 70, {"en": "layer", "zh": "層"}, 14, GRAY, "center"); d.text(420, 70, {"en": "what it catches", "zh": "抓什麼"}, 14, GRAY, "center"); d.text(770, 70, {"en": "the case it came from", "zh": "它從哪個案子來"}, 14, GRAY, "center")
    for i, (layer, catches, case) in enumerate(rows):
        y = 95 + i * 88
        d.box(30, y, 180, 70, layer, YELLOW, fs=14)
        d.arrow(210, y + 35, 250, y + 35)
        d.box(250, y, 350, 70, catches, RED, fs=14)
        d.arrow(600, y + 35, 640, y + 35, None, True)
        d.box(640, y, 350, 70, case, WHITE, fs=12)
    d.text(500, 545, {"en": "three layers are independent agents, two are rules those agents apply. Remove one and you are back to V1.",
                      "zh": "三層是獨立 Agent，兩層是 Agent 要套的規則。少一層就回到 V1。"}, 15, GRAY, "center")
    return d

# ----------------------------------------------------------------------------------------------------- D4
def d4(lang):
    d = Diagram("D4-untested-stop-condition", 1000, 560, lang)
    d.text(30, 20, {"en": "A stop condition you have not tested with a stub does not exist", "zh": "沒用 Stub 測過的停機條件，不存在"}, 24)
    d.text(30, 70, {"en": "intended: rolling window of the last 5 rounds fills up, then rejection rate is checked", "zh": "設計：滾動視窗裝最近 5 輪，裝滿後算拒絕率"}, 15, GRAY)
    for i in range(5):
        d.box(30 + i * 90, 100, 80, 50, {"en": f"r{i+1}", "zh": f"第 {i+1} 輪"}, GREEN, fs=14)
    d.arrow(480, 125, 530, 125); d.box(530, 100, 200, 50, {"en": "rate ≥ 1.5 → STOP → P", "zh": "拒絕率 ≥ 1.5 → 停 → 交回 P"}, YELLOW, fs=13)
    d.text(30, 190, {"en": "actual (macOS bash 3.2): ${arr[@]: -5} on an array shorter than 5 returns an EMPTY array", "zh": "實際（macOS bash 3.2）：陣列比 5 短時，${arr[@]: -5} 回傳空陣列"}, 15, GRAY)
    for i in range(5):
        d.box(30 + i * 90, 220, 80, 50, {"en": "[ ]", "zh": "[ ]"}, RED, fs=16)
        d.text(70 + i * 90, 275, {"en": f"round {i+1}: wiped", "zh": f"第 {i+1} 輪：清空"}, 11, GRAY, "center")
    d.arrow(480, 245, 530, 245); d.box(530, 220, 200, 50, {"en": "never fills → never fires", "zh": "永遠湊不滿 → 永遠不觸發"}, RED, fs=13)
    d.box(770, 95, 200, 175, {"en": "2 months in the docs:\n\"plateau, to be\nconfirmed that it fires\"\n\n= never will", "zh": "文件裡放了兩個多月：\n「Plateau 待確認\n會觸發」\n\n＝ 永遠不會"}, WHITE, fs=14)
    # bottom: how it was found + honesty
    d.box(30, 330, 290, 110, {"en": "stub claude: prints one scripted\nresult line per call\n→ a handful of scenarios, in seconds", "zh": "假的 claude：每次呼叫\n印一行預設結果\n→ 幾個 Driver 劇本，幾秒跑完"}, BLUE, fs=14)
    d.arrow(320, 385, 360, 385)
    d.box(360, 330, 290, 110, {"en": "plateau scenario fails\n→ fix: drop the oldest entry only\nonce the window is over-full", "zh": "Plateau 劇本壞掉\n→ 修法：視窗超過長度\n才丟掉最舊的一筆"}, GREEN, fs=14)
    d.arrow(650, 385, 690, 385)
    d.box(690, 330, 280, 110, {"en": "honest footnote: even fixed, the\n20-round data never reaches 1.5\n(max 5 rejects vs 5 ships = 1.0)", "zh": "誠實補一句：即使修好，\n那 20 輪的資料也到不了 1.5\n（最多 5 拒對 5 出貨 = 1.0）"}, WHITE, fs=13)
    d.text(500, 490, {"en": "the driver is deterministic, so it can and must be tested deterministically. Don't wait for an overnight run.",
                      "zh": "Driver 是 Deterministic 的，所以可以、也必須 Deterministic 地測。不要等一整晚的實跑。"}, 14, GRAY, "center")
    return d

# ----------------------------------------------------------------------------------------------------- D5
def d5(lang):
    d = Diagram("D5-perpetual-graph", 1000, 620, lang)
    d.text(30, 20, {"en": "Stopping means handing control back to the slow node, not ending", "zh": "停機是把控制權交回慢節點，不是結束"}, 24)
    # round loop (fast)
    d.box(30, 80, 700, 230, None, "transparent", stroke=LIGHT, dashed=True)
    d.text(50, 90, {"en": "one round · fresh agent · 10–20 min", "zh": "一輪 · Fresh Agent · 10–20 分"}, 14, GRAY)
    nodes = [("C", {"en": "C\nstate", "zh": "C\n現況"}, "transparent"), ("R", {"en": "R\nresearch", "zh": "R\n研究"}, "transparent"),
             ("F", {"en": "F\nvalue", "zh": "F\n價值閘"}, YELLOW), ("S", {"en": "S\nPRD", "zh": "S\nPRD"}, "transparent"),
             ("D", {"en": "D\nbuild", "zh": "D\n開發"}, "transparent"), ("B", {"en": "B\nbuild ok", "zh": "B\nBuild 過"}, YELLOW),
             ("V", {"en": "V\nvalidate", "zh": "V\n驗證閘"}, YELLOW), ("Y", {"en": "Y\nship", "zh": "Y\n出貨"}, "transparent")]
    xs = []
    for i, (k, lab, bg) in enumerate(nodes):
        x = 50 + i * 84; xs.append(x)
        d.box(x, 130, 66, 60, lab, bg, "diamond" if bg == YELLOW else "rectangle", fs=12)
        if i: d.arrow(x - 18, 160, x, 160)
    d.path([(xs[-1] + 33, 190), (xs[-1] + 33, 240), (xs[0] + 33, 240), (xs[0] + 33, 190)], {"en": "next round", "zh": "下一輪"}, fs=12, mid=((xs[-1] + xs[0]) / 2 + 33, 240))
    d.text(330, 262, {"en": "back-edges (not drawn) are capped ≤1 / ≤2 / ≤3; past the cap → revert, NOOP", "zh": "回邊（圖中省略）有上限 ≤1／≤2／≤3，超過就還原 → NOOP"}, 12, GRAY, "center")
    # T
    d.box(770, 110, 200, 70, {"en": "T · trajectory\nevery 5 rounds", "zh": "T · 軌跡\n每 5 輪"}, YELLOW, "diamond", fs=13)
    d.arrow(730, 160, 770, 145, None, True)
    d.text(870, 190, {"en": "CONTINUE / REDIRECT / STOP", "zh": "CONTINUE／REDIRECT／STOP"}, 11, GRAY, "center")
    # stop conditions → P
    d.box(30, 335, 320, 120, {"en": "hand back to P when:\nrejection-rate plateau (script)\nrejected even after RESET (script)\ntrajectory STOP (independent agent)",
                              "zh": "交回 P 的訊號：\n拒絕率 Plateau（腳本算）\nRESET 後仍被拒（腳本算）\n軌跡 STOP（獨立 Agent 判）"}, WHITE, fs=12)
    d.text(190, 462, {"en": "3× failure · 3 maintenance rounds · budget → exit, fix tools", "zh": "連 3 輪失敗 · 連 3 維護輪 · 預算 → 退出，修工具"}, 11, GRAY, "center")
    d.arrow(350, 395, 380, 395)
    d.box(380, 330, 250, 130, {"en": "P · positioning\nthe only slow node\nthe only place the objective\nfunction can change", "zh": "P · 定位\n唯一的慢節點\n唯一能改目標函數的地方"}, BLUE, fs=14)
    d.path([(505, 330), (505, 298), (42, 298), (42, 160), (50, 160)], {"en": "P → C", "zh": "P → C"}, True, fs=12, mid=(540, 330))
    d.box(650, 330, 320, 60, {"en": "human present: /position,\nmulti-round questions, all fields", "zh": "人在：/position 多輪提問收斂，\n全部欄位"}, RED, fs=12)
    d.box(650, 400, 320, 60, {"en": "nobody present: strategist proposes,\ncritic attacks; agree → soft fields only,\nelse wait", "zh": "人不在：Strategist 提案、Critic 找反證；\n都同意才改軟欄位，否則等人"}, GREEN, fs=12)
    d.arrow(630, 375, 650, 360); d.arrow(630, 415, 650, 430)
    d.text(500, 500, {"en": "hard fields (audience · problem · trust rules) are human-only. If the two agents disagree, nothing changes.",
                      "zh": "硬欄位（對象、問題、信任規則）人專屬。兩個 Agent 不同意，就什麼都不改。"}, 14, GRAY, "center")
    d.text(500, 540, {"en": "five time scales on one graph: fix loop (minutes) · round (10–20 min) · trajectory (5 rounds) · positioning (on STOP) · human (hours–weeks)",
                      "zh": "同一張圖五個時間尺度：修正迴圈（分）· 一輪（10–20 分）· 軌跡（每 5 輪）· 定位（STOP 時）· 人（小時到週）"}, 12, GRAY, "center")
    return d


DIAGRAMS = [d1, d2, d3, d4, d5]
