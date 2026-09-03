# Style reference — excalidraw-figures

The look is Excalidraw's own: black ink, rough strokes, its default pastel fills, hand-drawn font. The discipline is in how few things you draw and where the words go.

## Palette roles

| Role | Fill | Use for | Do not use for |
|---|---|---|---|
| `GATE` | `#ffec99` yellow | decisions, gates, checks, the thing that says yes/no | headings, emphasis |
| `AGENT` | `#a5d8ff` blue | a model, an agent, a fresh context, "the thing that reasons" | files |
| `FAIL` | `#ffc9c9` red | an incident, a failure class, a human-only step | every "important" box |
| `FIX` | `#b2f2bb` green | the fix, the outcome, what to do instead | decoration |
| `NOTE` | `#ffffff` white | files, evidence, notes, callouts | — |
| `TRANSPARENT` | none | plain steps | — |

Three fills plus white per figure, maximum. If you need a fourth colour you have two figures.

Strokes: `INK #1e1e1e` for boxes and arrows, `GRAY #495057` for captions and arrow labels, `LIGHT #868e96` for dashed grouping frames. Dashed = optional, return, back-edge, or "frame around a group"; solid = primary flow.

## Type sizes

| Element | px | Notes |
|---|---|---|
| Figure title | 24 | top-left at (30, 20). One line |
| Section label inside a frame | 15–18 | grey |
| Box label | 14–16 | 13 is the floor, and only for dense figures |
| Arrow label / caption | 12–13 | grey; short, uppercase protocol tokens stay uppercase |
| Footnote | 12–14 | grey, bottom |

CJK floor is 13px. Prefer wrapping over shrinking.

## Width budget

`width ≈ Σ (1em per CJK glyph, 0.55em per Latin glyph) × font size`. Leave ≥ 8px on each side inside a box. In practice: a 16px label fits ~14 CJK characters or ~26 Latin characters in a 240px box. Wrap with `\n`; the box label helper centres multi-line text.

## Layout rules

- 4px grid for box positions and sizes (the library snaps boxes; keep your own numbers on the grid too).
- ≥ 24px gap between boxes; ≥ 40px between a box and the canvas edge.
- Arrows leave and enter box edges, not corners. Straight when the endpoints share an axis; otherwise an orthogonal `path()` with 90° bends.
- A label never sits on its line: 18–20px above a horizontal segment, or beside a vertical one. Pass `mid` explicitly for `path()`.
- No arrow passes through a heading or a box it does not connect.
- Loops close visibly: draw the return edge as a `path()` below or above the row, label it ("next round", "下一輪").
- Callout / evidence boxes in `NOTE` white go in a margin, not in the flow.
- Title states the claim, not the topic: "Loop 只會最大化它量得到的東西", not "迴圈架構圖".

## Bilingual discipline

- One spec, two outputs. Write every visible string as `{"en": ..., "zh": ...}`.
- Keep code tokens, file names, commands and protocol words identical across languages (`LOOP_RESULT`, `main`, `claude -p`, `ACCEPT`).
- Translate concepts, not tokens: `Value gate` ↔ `價值閘`, `fresh context` ↔ `Fresh Context` (kept as a term) is a judgment call; be consistent inside one article.
- Chinese labels take about 1.6× the width of the English at the same character count. Check both PNGs; the ZH one breaks first.

## Anti-patterns seen in practice

| Anti-pattern | What happened | Fix |
|---|---|---|
| Label on a vertical segment | `path()` default label position landed on the line | `mid=(x, y)` on the horizontal run |
| Line too long for the box | 26-char CJK string in a 340px box at 17px | wrap to two lines, box +24px |
| Arrow through a heading | a back-edge routed up past the section label | move the label below the gate, or route the arrow lower |
| Footer sentence across the whole canvas | three pull-quotes in one line | one quote per line |
| Every box a different colour | "importance" signalled by fill | three fills max; importance by position and title |
| Diagram restates the text | five boxes that say what the paragraph says | delete the figure |
