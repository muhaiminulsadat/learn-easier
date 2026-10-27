# Component library (copy these exact patterns)

Every chapter file is `chapters/chN.html`: a META comment, then pages separated by `<!--PAGE-->`.
Use `<!--PAGE qr-->` for the Quick Revision page. Never write `<html>`/`<head>`: build.py wraps the pages.
The chapter strip (number, lecture, date, title, icon) is added automatically above the first page's content.

```html
<!--META {"n":2,"bn":"অধ্যায়ের বাংলা/মিশ্র শিরোনাম","en":"Short English header","lec":"L-2","date":"22-04-25","tint":"yellow","icon":"droplet","topics":"topic · topic · topic"} -->
<!--PAGE-->
...content...
<!--PAGE-->
...
<!--PAGE qr-->
...quick revision...
```
`tint` optional (auto-cycles blue, yellow, green, red, purple, tan, teal, lime). `lec`/`date`: use `—` if unknown (never invent).

Entities: write `&middot; &rarr; &ge; &le; &plusmn; &times; &ndash; &mdash; &prime;`. Use `<sub>`/`<sup>`, never Unicode subscripts (they fall back to a wrong font).
Avoid the glyphs ∝ ① ② ③ ₂ ₄ (not in the design fonts). Write "varies as" or `1)` `2)` instead.

## Placeholders (expanded by build.py)
- `{{ic:NAME}}` thin line icon (24px, 1.6 stroke). Names: droplet flask flame gauge truck thermo ruler shield umbrella layers mountain road check xc clock scale sieve cube wave bulb star alert bookmark rain hammer globe chart pit factory tire magnet target link list weight book pencil calc bolt gear chip dna atom coin people scales code map heart leaf wrench pipe building wheel. Pick the closest; if none fits, add a new path to `ICONS` in `scripts/build.py` (24x24, stroke only, round caps) and list it here.
- `{{arr}}` arrow between flow nodes.
- `{{chk:short reason}}` red dashed [CHECK] tag (unclear in source). `{{CHK}}` = generic.
- `{{tb}}` grey "textbook" tag (fact not in the source).

## Text
```html
<h2><span class="no">1.1</span>Topic heading</h2>
<h3>Sub-topic</h3>
<ul class="n">
 <li>Bangla sentence with <b class="en">English Keyword</b>.
   <ul><li>nested bullet</li></ul></li>
</ul>
<mark>highlight</mark>   <!-- max ONE per paragraph, only for what the teacher stressed -->
<span class="f inline">formula</span>      <div class="f">block formula with W<sub>d</sub></div>
<p class="sm">small soft note</p>
```
Bold every key English term with `<b class="en">…</b>` (or plain `<b>` for numbers).

## Q & A (blue Q chip, tinted answer box) — one per question the teacher raised
```html
<div class="qa">
<div class="q"><span class="chip">Q</span><span>Question in Bangla/English?</span></div>
<div class="a"><span class="al">A</span>Answer text.</div>
</div>
```

## Callouts (only where the notes justify them)
```html
<div class="call imp"><div class="lab">{{ic:alert}}Important</div> text, stressed/yellow-marked in source </div>
<div class="call rem"><div class="lab">{{ic:bookmark}}Remember</div> … </div>
<div class="call mis"><div class="lab">{{ic:xc}}Common mistake</div> … </div>
<div class="call exam"><div class="lab">{{ic:star}}Exam tip</div> … </div>
<div class="call mem"><div class="lab">{{ic:bulb}}Memory trick &middot; ABC</div> <b>A</b>… <b>B</b>… <b>C</b>… </div>
```

## Infographic card wrapper (every infographic sits in one)
```html
<div class="ig"><div class="il">INFOGRAPHIC 2.1 &middot; তুলনা</div><div class="it">Title of the figure</div> …figure… </div>
```
Label words: তুলনা (comparison), প্রক্রিয়ার ধাপ (process), শ্রেণিবিভাগ (classification), তালিকা (list), সূত্র (formula), Graph, Decision tree, Cross-section, Gauge, Test সেটআপ, MIND MAP.

### A. Process flow (3–5 boxes; last box dark = result)
```html
<div class="flow">
<div class="node">{{ic:droplet}}<b class="en">Step</b><span class="s">sub-label</span></div>{{arr}}
<div class="node">…</div>{{arr}}
<div class="node k">{{ic:layers}}<b class="en">Result</b><span class="s">sub-label</span></div>
</div>
```
Classes: `node` tinted, `node w` white, `node k` dark. Max 5 nodes per row; keep each label under ~28 characters. Two rows: add `style="margin-top:8px;gap:8px"` to the second `.flow`.

### B. Comparison table
```html
<table class="tbl"><tr><th></th><th>A</th><th>B</th></tr>
<tr><td>row label</td><td>…</td><td>…</td></tr></table>
```
First column is bold automatically; add `style="font-weight:400"` to a cell to un-bold.

### C. Cards (2–3 across)
```html
<div class="row"><div class="card"><div class="ct">{{ic:ruler}}Title</div>text</div><div class="card">…</div></div>
```

### D. Decision tree (inline SVG, diamonds for decisions, straight arrows, labels never overlap)
Pattern from the reference (viewBox 618 wide; boxes rx=12; colours = chapter tint fill + accent stroke):
```html
<svg viewBox="0 0 618 214" width="100%" height="214">
<g stroke="ACCENT" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round">
 <path d="M309 38V58"/><path d="M309 38l-5-7M309 38l5-7"/> …arrows… </g>
<rect x="219" y="0" width="180" height="30" rx="10" fill="#1A1F36"/><text x="309" y="20" text-anchor="middle" fill="#fff" font-size="14" font-weight="700">Start</text>
<path d="M309 60L403 98L309 136L215 98Z" fill="#FFEFAD" stroke="#8F6B00" stroke-width="1.5"/>  <!-- decision diamond -->
<text x="309" y="94" text-anchor="middle" font-size="13" font-weight="700">Question?</text>
<text x="190" y="90" text-anchor="middle" class="m" font-size="13" font-weight="700" fill="#1F7A4D">হ্যাঁ</text>
<rect x="60" y="130" width="180" height="62" rx="12" fill="#DAEEE2" stroke="#1F7A4D" stroke-width="1.5"/> … outcome boxes …
</svg>
```
Rules: use the SVG `class="m"` only for Latin/digits (monospace); Bangla text without it. Leave ≥8px between any text and a line or edge. Arrowheads are short strokes, not markers.

### E. Number tiles (Quick Revision) and gauge/bar
```html
<div class="qr"><div class="nums"><div class="nm"><div class="v">140&deg;C</div><div class="t">what it is</div></div> … 6 tiles …</div></div>
```
Gauge/bar = SVG: rounded `rect rx=11` track in the tint colour, filled part in ink `#1A1F36` or accent, 13px labels beneath.

### F. Mind map (SVG, centre dark node + 4 tinted satellites + 1 dashed bottom node)
Copy the mind-map block from `examples/sample_chapter.html` (last page) and change the texts and the three colours (stroke accent, fill tint). Each node: 140×44 (satellites) / 166×46 (centre); two text lines max (14px bold + 13px soft).

### G. Graph (SVG axes + curve)
Axes `stroke="#1A1F36" stroke-width="1.6"`, curve `stroke="#2747A8" stroke-width="2.4"`, optimum point = small circle `r=6 fill=none stroke="#B3382C"` with dashed guide lines `stroke="#4A5068" stroke-dasharray="4 4"`. Put a caption "চিত্র ধারণাগত" when curves are schematic, never fake data.

### H. Cross-section / diagram
Stack of rects (rx only at ends), labels centred in white/ink 14px bold, callout boxes at left/right joined by 1.5px lines.

## Quick Revision page (last page of every chapter, `<!--PAGE qr-->`)
Order: eyebrow `QUICK REVISION · অধ্যায় N` → `<h2 style="font-size:26px;margin-top:-6px">এক পাতায় সারকথা</h2>` → number tiles (6) → formula strip (if any) → mind map → memory-trick callout → `<h3>Self-test</h3>` with 3 checkbox questions:
```html
<ul class="selftest"><li><span class="box"></span><span>Question?</span></li> …3… </ul>
```
Eyebrow markup: `<div style="font-family:'JetBrains Mono','Hind';font-size:13px;color:var(--acc);font-weight:700;letter-spacing:.06em">QUICK REVISION &middot; অধ্যায় 1</div>`

## Extra sections (listed in book.json "extras")
`chapters/formulas.html`: cards, one per chapter, with `<span class="pill" style="background:var(--c-blue);color:var(--a-blue)">Ch 1</span>` + formulas, then a numbers table. `chapters/glossary.html`: `.tbl` rows of English term | one-line Bangla meaning, A–L / M–W style split over 2 pages. See `examples/sample_formulas.html` and `examples/sample_glossary.html`.

## Added in the second book
### LaTeX (KaTeX)
Inline `\( G_{sb}=\dfrac{W_{dry}}{W_{SSD}-W_{sub}} \)`, display `\[ \text{VFA}=\dfrac{V_{be}}{V_{ma}}\times 100 \]` (renders in a white `.fm` box; also fine inside callouts, tables, Q&A, cards). After every formula add a one-line "where" explanation of the symbols and, when the source has one, a worked numeric example. Not available inside `<svg>`.

### Beginner callouts
```html
<div class="call easy"><div class="lab">{{ic:bulb}}সহজ কথায়</div>plain-language analogy…</div>
<div class="call ex"><div class="lab">{{ic:calc}}Worked example</div>step 1… step 2…</div>
```

### Picture with caption
```html
<div class="pic"><img src="img/ch7_la.png" alt="…"><div class="cap">চিত্র 7.1 — caption (slide N)</div></div>
```
Keep ≤ ~330 px tall; `img/` lives in the project folder next to `chapters/`.

### Multi-page extras
Glossary: split into pages of ≤ 20 rows (`<table class="tbl">`, first cell `style="width:34%"`, header `GLOSSARY k/N` and range `A – C`). Formula sheet: one `.card` per chapter with `.pill` + display LaTeX; numbers table ≤ 12 rows per page.
