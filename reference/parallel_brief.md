> TEMPLATE from the CE 451 bitumen book. Copy it to the work folder of a new book and change the paths, source table, goal paragraph and chapter list before giving it to chapter agents.

# BRIEF — rebuilding the "Bituminous Materials & Mix Design" study book (CE 451)

You are writing **some chapters** of one big A4 study-notes PDF. Other agents write the other chapters in parallel; I (the lead) merge everything. Follow this brief exactly so the chapters look and read like one book.

## 0. The goal in one paragraph
The reader is a **complete beginner** (Civil Eng. student) who knows nothing about bitumen, aggregates or mix design and wants to *understand everything from the very first line*, then revise for exams. The old book (`E:\Academics\4-1\Theory\CE 451\Notes\Pavement_Notes_Output\Bituminous_Materials_Mix_Design_Notes.pdf`, text dump in `work/existing.txt`) was made only from a senior's (Anika's) handwritten class notes and is thin / full of "CHECK" gaps. We now rebuild it **from the teacher's (Dr. Hadiuzzaman, "Hadi Sir") lecture slides**, using the senior's notes only for the things the teacher *said in class* that are not on the slides.

## 1. Sources (all on disk, read them yourself)
Root: `E:\Academics\4-1\Theory\CE 451\`
| What | Where |
|---|---|
| Slide text (page-tagged) | `work/bitumen.txt` (56 slides), `work/aggregate.txt` (125), `work/marshall.txt` (48), `work/hveem.txt` (52) |
| Slide pages as PNG (110 dpi, 720x540 pt pages) | `work/pages/<deck>/pNNN.png` with deck = `bitumen` `aggregate` `marshall` `hveem` |
| Contact sheets (12 pages each, red page number) | `work/sheets/<deck>_NN.jpg` |
| Original slide PDFs | `Slides/Hadi Sir/*.pdf` (bitumen = `Bitumen_for_Student.pdf`, aggregate = `CE 451_Aggregate for Asphalt Mixtures_Student.pdf`, marshall = `Asphalt_hot mix design_Marshall.pdf`, hveem = `Asphalt_hot mix design_Marshall_HVEEM.pdf`) |
| Senior's class notes (old book text, page-tagged; contains class remarks + CHECK gaps) | `work/existing.txt` |
| Old book's page images (for layout of senior-notes material) | `Notes/Pavement_Notes_Output/PNG_2x/page_NN.png` |

**Many slides are pure images** (charts, tables, worked examples, equipment photos: the text file shows nothing for them). You MUST open (Read tool, it shows images) every slide page of your chapters that has little/no text, and the contact sheets, so that you do not miss a graph, table or example. Slide text extraction of equations is sometimes garbled (e.g. `Gsb` formulas in aggregate.txt p80/p81) — look at the PNG and re-derive the correct formula.

**Source priority:** (1) the slides = the official content; (2) the senior's class remarks = what Hadi Sir *said* (keep them, labelled as "ক্লাসে স্যার বলেছিলেন" / class remark, they are often the exam hints); (3) general textbook knowledge only to *explain* (analogies, definitions of basic words) — never to add new numbers. If a number/fact is not in (1) or (2) but you add it, tag it `{{tb}}`. If slides and senior's notes disagree on a number (e.g. emulsion bitumen %, sand-equivalent minimum, LAA limit), show the **slide value** as the main one, mention the class-note value as "ক্লাস নোটে ... লেখা", and add a line to `notes_to_verify.md`.
Do not invent. Unclear/illegible → `{{chk:reason}}`. The old book's CHECK items (list in `Notes/Pavement_Notes_Output/CHECK_and_textbook_list.md`) should now be **resolved from the slides wherever possible**.

## 2. The design system (do not deviate)
Read these first: `.claude/skills/learn-easier/SKILL.md`, `reference/design_spec.md`, `reference/components.md`, `reference/book_json.md`, `examples/sample_chapter.html`, and look at a few pages of `reference/reference_design.pdf` (render with fitz) — all under `E:\Academics\4-1\Theory\CE 451\.claude\skills\learn-easier\`. **Do not edit the skill folder** (the lead already added LaTeX + the two new callout types below).

Key points (details in components.md): A4 portrait; pages separated by `<!--PAGE-->` inside `chN.html`; last page of each chapter is `<!--PAGE qr-->` (Quick Revision: 6 number tiles, mind map, memory trick, 3 self-test checkboxes). Every chapter: first page opens with its `<h2>` topics (the chapter strip is added automatically); ≥2–4 infographics (flows, comparison tables, decision trees, cross-sections, gauges, graphs, mind map); Q&A block for every teacher question / likely exam question; callouts (`imp`, `rem`, `mis`, `exam`, `mem`); a mnemonic for every list of 3+ items. NO emoji. Min text 13px. Pages ≤ ~85% full. Use the 8 tints in order (blue, yellow, green, red, purple, tan, teal, lime) — `tint` auto-cycles from the chapter number `n`, so keep `n` correct.

### New things the lead added
1. **LaTeX math (KaTeX).** For EVERY formula/equation/symbol expression use LaTeX: inline `\( ... \)`, display `\[ ... \]` (display gets a white formula box automatically). Do not use the old `.f` mono box for formulas any more. Rules:
   - Put English words inside math with `\text{...}` and subscripts as `_{...}` (e.g. `G_{sb}=\dfrac{W_{dry}}{W_{SSD}-W_{sub}}`, `\text{VFA}=\dfrac{V_{be}}{V_{ma}}\times 100`).
   - **No Bangla inside math.** Put Bangla in the surrounding sentence.
   - Use `\dfrac`, `\left( \right)`, `\times`, `\%`, `\approx`, `\ge`, `\le`, `^\circ\text{C}`. KaTeX works inside callouts, tables, Q&A. It does NOT work inside `<svg>` — in SVG diagrams write simple text (use `<tspan baseline-shift="sub">` or plain `Gsb`).
   - **Write the HTML files only with the Write/Edit tools. Never create them through a bash heredoc or a python string** — backslashes (`\f`, `\r`, `\t`, `\b`) get corrupted. After every build, if you see a red `LATEX ERROR` tag on a page, fix it.
   - Every formula must be followed by a one-line "where" explanation of each symbol (in Bangla + English terms) and, where the slides give one, a **worked numeric example** (copy the slide's numbers exactly; show every step).
2. **New callouts**: `<div class="call easy"><div class="lab">{{ic:bulb}}সহজ কথায়</div>…</div>` (green; the beginner's plain-language/analogy box — use it freely, e.g. "bitumen = রাস্তার আঠা, aggregate = রাস্তার হাড়") and `<div class="call ex"><div class="lab">{{ic:calc}}Worked example</div>…</div>` (tan; step-by-step numeric example).
3. **Pictures from the slides** (`<div class="pic"><img src="img/chN_name.png" alt="…"><div class="cap">চিত্র N.x — caption</div></div>`; also allowed inside an `.ig` card). How to make them:
   - Crop the figure from the slide at higher resolution than the 110-dpi PNGs: with PyMuPDF `page.get_pixmap(dpi=220, clip=fitz.Rect(...))` from the original PDF (page rect is 720x540), or crop `work/pages/...png`. Extract embedded photos with `page.get_images()`/`fitz.Pixmap`. Improve them (PIL: crop whitespace, `ImageOps.autocontrast`, sharpen, convert to RGB, max width ~1300 px) and save to `<your project>/img/<chN>_<short-name>.png` or `.jpg` (prefix with the chapter number, e.g. `ch7_los_angeles.jpg`, so files from different agents never collide).
   - Some slide figures are poor (blurry charts, numbers needed for the exam): **redraw them as clean inline SVG** in the book's style instead. Process/flow/comparison/decision diagrams should always be redrawn as SVG infographics; equipment photos, real charts (Hveem charts 1–5, Marshall plots), worked-example tables may be used as cropped images (and/or re-typed as an HTML table + LaTeX so the numbers are readable).
   - Add 1–3 pictures per chapter wherever the slide has a useful diagram/photo. Always give a caption. Keep each image ≤ ~330 px tall on the page so pages stay balanced.

## 3. Language rule (very important)
All sentences/explanations in **Bangla**; technical keywords, test names, units, grades, symbols stay **English** (wrap key English terms in `<b class="en">…</b>`; at most one `<mark>` per paragraph — only for what the teacher stressed or the slide highlights). Do not translate technical terms (e.g. write "Marshall stability", "air void", "stripping", not Bangla transliterations). Write natural, simple, friendly Bangla for a beginner — short sentences, step by step, define each term the first time it appears (in a `call easy` box or in the sentence). Chapter-opening page: start with a short "এই অধ্যায়ে কী শিখবে / কেন দরকার" bullet list (2–4 bullets) before the first h2 content, and say what the previous chapter taught if useful.
Avoid the glyphs `∝ ① ② ③` and Unicode sub/superscripts (use LaTeX or `<sub>`). Use `&middot; &rarr; &ge; &le; &plusmn; &times; &deg;` entities in non-math HTML.

## 4. Depth / completeness rules
- Cover **every** slide of your range (even text-only ones, even image-only ones) and **every class remark** in the old book's pages for your chapters. Nothing from the slides may be skipped or shortened away; condense wording but keep every fact, number, grade, limit, test name and standard code (AASHTO/ASTM numbers are exam-relevant: keep them, e.g. AASHTO T96 / ASTM C131).
- Keep source order inside the chapter (slides order), unless a beginner prerequisite must come first.
- Beginner depth: assume the reader never saw the object. Explain what it is, what it looks like, why engineers care, how it is measured, what the result means, typical numbers. Use analogies (kitchen, cricket, sand-castle, glue…) sparingly but clearly. Add `call mis` "Common mistake" only when supported by the source or just restating it.
- Chapter length target: 7–12 pages including the Quick Revision page (more pages are fine if the slides need it; never squeeze; pages ≤ 85% full, none < 40% except the QR page may be a bit emptier).
- Exact numbers: copy from the slide/PNG. Re-check every number you typed against the source.

## 5. Your project folder & workflow
Make **one folder per agent** (name given in your task), e.g. `E:\Academics\4-1\Theory\CE 451\work\agents\<name>_Build\` containing:
- `book.json` (copy `examples/book.json` from the skill; keep as is, `extras` may stay — missing extra files are ignored; set `footer_credit` to `"সংকলন: Sadat · Hadi Sir-এর slide + Anika-র নোট"`),
- `chapters/chN.html` for each chapter you own (N = global chapter number from your task; the META `n` must equal N; `lec`/`date`: use the lecture/date from the old book's chapter list for chapters that came from class notes (e.g. L-4 · 13-05-25) — for slide-only chapters use the deck name in `lec` (e.g. "Slide: Bitumen") and `—` for date),
- `img/` (your cropped images),
- `notes_to_verify.md` (conflicts between slides and class notes, unreadable bits, decisions, anything not verified).
Build + check: `python "E:\Academics\4-1\Theory\CE 451\.claude\skills\learn-easier\scripts\make.py" "<your Build folder>"` (use `python`, Windows; the report lists OVERFULL / NEARLY EMPTY pages, FALLBACK FONT lines). Then **look at every generated page** `<Build>/prev/pNN.png` with the Read tool (page numbers there are within your sub-book: page 1 = cover, 2 = contents, your chapters start at page 3). Fix overlapping SVG labels, clipped text, content touching the footer, LATEX ERROR tags, tiny/blurry images, empty gaps, until clean. Rebuild until the report has no OVERFULL (>98%) page; avoid <40% pages. Only the Write/Edit tools for HTML. Do not run more than one make.py at a time for your own folder.
Do not touch other agents' folders, the old output, or the skill folder.

## 6. What to report back (short)
Your final message must list: chapter files + image files created, page count, the number of `{{chk}}` and `{{tb}}` tags, conflicts/oddities (also written to your `notes_to_verify.md`), and honestly anything you did not verify. Keep it under 250 words.
