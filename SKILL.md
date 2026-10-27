---
name: learn-easier
description: Turn any course content (handwritten/scanned note PDFs, typed PDFs, slides, Word/text/markdown, images, lecture transcripts) into a print-ready A4 exam-revision study-notes PDF in the user's established design (infographics, flowcharts, Q&A blocks, callouts, mnemonics, Quick Revision pages, cheat-sheet, glossary). Use whenever the user gives course content and asks for a PDF note/study notes/revision book, or invokes /learn-easier.
argument-hint: <path(s) to content> [course name / lecturer / language if not obvious]
---

# learn-easier

Input = the content the user gives (file path(s) or pasted text). Output = one finished PDF + 2x PNGs + a verification list. The user must not need to explain anything: everything below is the standing instruction.

## Standing defaults (do NOT ask about these)
- Compiled by: **Sadat**. Page footer credit = whoever wrote the source notes (e.g. "সংকলন: Anika"); if the source has no named author use "সংকলন: Sadat".
- Format A4 portrait, design = `reference/design_spec.md` exactly (colours, 4 fonts, icons, flowcharts, components).
- Language rule: all sentences/explanations in **Bangla**; technical keywords, formulas, units, test names, grades stay **English** (bold the key English terms; at most one yellow `<mark>` per paragraph, only for what the teacher stressed). If the source is entirely a non-Bangla subject, still write Bangla sentences with English terms, unless the user said otherwise.
- Do not skip, shorten or invent content. Keep source order. Unclear word/number/formula → `{{chk:reason}}`, never guess. Any fact not in the source → `{{tb}}`.
- No outline-approval pause: print a short chapter outline (name, lecture, date, source pages) as text, then continue straight to building. Pause for approval only if the user said "outline first".
- Course code: take it from the source/arguments; if absent, leave the cover value `—` (do not invent).

## Ask the user ONLY when blocked
Ask (AskUserQuestion, one short batch) only for things you cannot find in the content/arguments and that change the result: who the lecturer is *if* the cover needs it and it is not in the source (otherwise use `—`), or a contradiction that makes chapter splitting impossible. Everything else: decide, and list the decision in `notes_to_verify.md`.

## Files in this skill (read on demand)
- `reference/design_spec.md` – the design rules. **Read first.**
- `reference/components.md` – every HTML/SVG pattern + icon names + placeholders. **Read before writing chapters.**
- `reference/book_json.md` – cover/book settings.
- `reference/reference_design.pdf` – finished 49-page example; `reference/inspiration/*.png` – original design images. View a few pages.
- `examples/` – `book.json`, `cover_art_pavement_layers.svg`, `sample_chapter.html` (a full chapter incl. mind map & Quick Revision), `sample_formulas.html`, `sample_glossary.html`.
- `assets/` – `style.css`, `fonts/` (copied into each project automatically).
- `scripts/render_source.py`, `scripts/build.py`, `scripts/make.py`.

## Workflow
Use the task list (one step per phase below). Python 3 with PyMuPDF (`fitz`) and Pillow is required, plus Edge or Chrome for printing (make.py finds them). If a module is missing: `pip install pymupdf pillow`.

1. **Intake.** Identify the source type.
   - PDF: `python <skill>/scripts/render_source.py "<src.pdf>" <work>/src 110`. It reports whether a text layer exists. If yes, extract text with fitz and use it (plus images for diagrams). If scanned/handwritten, read **every single-page image** (`src/pNN.jpg`) with the Read tool, several per message, and transcribe as you go into `<work>/transcript.md` (page-tagged). Contact sheets (`sheetK.jpg`) are only for spotting headings/dates/lecture numbers, never for transcription.
   - Check that every image read actually returned an image. If a read fails or comes back empty, re-read that page before using it. Never write a chapter from memory of a page you did not see.
   - Images / pptx / docx / md / txt: read directly (pptx/docx: use text extraction; keep slide/section order).
   - Blank pages: skip but note them.
2. **Outline.** Split into chapters by lecture/date/heading changes. For each: number, title, lecture no., date, source page range. Note odd things (out-of-order dates, missing lecture numbers, incomplete topics) → they go in `notes_to_verify.md` and the final message. Print the outline.
3. **Project folder.** `<content folder>/<Title>_Build/` containing `book.json` (copy `examples/book.json`, edit), `chapters/ch1.html …`, `chapters/formulas.html`, `chapters/glossary.html`, optional `cover_art.svg`, `notes_to_verify.md`. Output goes to `<content folder>/<Title>_Output/` (make.py default).
4. **Write chapters** with `reference/components.md` patterns. For EVERY chapter: first page opens with its h2 topics; ≥1 infographic (flow/decision tree/comparison table/mind map/gauge/cross-section/graph) wherever the content is a process, comparison, classification or list of tests/properties; Q&A for every teacher question; callouts where justified (Important = teacher stressed/yellow-marked; Remember; Common mistake; Exam tip; Memory trick for every list of 3+); last page = Quick Revision (6 number tiles, mind map, memory trick, 3 self-test checkboxes). Add formulas + numbers cheat-sheet (all formulas and key numbers, grouped by chapter) and glossary (English term | one-line Bangla meaning, 2 pages max per ~40 terms).
   Transcription fidelity: every number, grade, temperature, ratio and formula must equal the source exactly. Do not add "Common mistake"/"Exam tip" content that the source does not support unless it only restates the source; invented facts need `{{tb}}`.
   Page budget: roughly 3–5 infographic-or-text blocks per page; split with `<!--PAGE-->` so no page exceeds ~85% full.
5. **Build + check.** `python <skill>/scripts/make.py <Build folder>` (output dir optional). Read the report: pages marked OVERFULL (>98%) or NEARLY EMPTY (<40%) must be fixed by moving blocks across `<!--PAGE-->` breaks; `FALLBACK FONT` lines mean a glyph outside the design fonts (replace per components.md). Then view the PNGs in `<Build>/prev/pNN.png` (Read tool) for **every page**: look for overlapping SVG labels, clipped text, content touching the footer, broken Bangla, empty space, oversized single cards. Fix and rebuild until clean. Spot-check one page at 250 dpi (`fitz` clip) for Bangla conjuncts.
6. **Deliver.** Final message (short, plain): file paths of the PDF, PNG folder, verification list; page count; counts of `[CHECK]` and `(textbook)` items; the decisions/oddities from `notes_to_verify.md`; anything not verified (e.g. low-confidence handwriting pages). Do not claim pages were viewed if they were not.

## Features added in the second book (slides + LaTeX edition)
- **LaTeX math (KaTeX, offline, `assets/katex`)**: inline `\( … \)`, display `\[ … \]` (white formula box). Used for every formula; English words via `\text{}`, no Bangla inside math, not usable inside `<svg>`. `scripts/build.py` renders it through `scripts/latex.js` (needs `node`); a bad formula shows a red `LATEX ERROR` tag. **Write chapter HTML only with Write/Edit, never bash heredocs or python strings** (backslashes like `\f`, `\r` get corrupted).
- **New callouts**: `call easy` (green "সহজ কথায়" beginner/analogy box) and `call ex` (tan "Worked example"). See `reference/components.md`.
- **Slide pictures**: `<div class="pic"><img src="img/chN_name.png"><div class="cap">…</div></div>`; crop at 220 dpi from the source PDF, name files with a chapter prefix.
- **Contents page** now spans as many pages as needed (8 rows per page); glossary/formula extras may be several pages (≤ ~20 glossary rows, ≤ ~12 table rows per page).
- **Slide decks as source** (pptx-exported PDFs with a text layer): extract text with fitz to `work/<deck>.txt`, render every page to `work/pages/<deck>/pNNN.png`, make 12-page contact sheets; image-only slides (charts, tables, worked examples) must be opened and read. Slides outrank class-note remarks; when numbers differ show the slide value first and list the conflict in `notes_to_verify.md`.
- **Large books: parallel chapter agents.** Use `reference/parallel_brief.md` as the shared brief; give each agent its own `<name>_Build` folder (own `book.json`, `chapters/`, `img/`), then copy chapters + images into the final Build folder, write `formulas.html`/`glossary.html` yourself, rebuild, and review every page with 2x2 contact sheets (`prev/pNN.png`, sort numerically). `make.py` uses a per-project `.browser_profile` so several builds can run at once.
- Headings `h2 .no` numbers must be unique and sequential inside a chapter (renumber after merging agent output).

## Hard rules learned from the first book (avoid repeating)
- Unicode subscripts/∝/①②③ fall back to wrong fonts → use `<sub>`, `1)` etc.
- JetBrains Mono has no Bangla: `style.css`/build.py already chain `Hind` after it. In inline SVG don't use `class="m"` on Bangla text.
- Table `td:first-child` is bold; long Bangla in first column wraps awkwardly: keep first columns short.
- A page filled to 100% overlaps the footer. Always leave slack; never rely on the page cutting content.
- Keep all text ≥13px; SVG viewBox is 618 wide, rendered full width, so SVG 13px text ≈ 13px on the page.
- Windows consoles: the scripts reconfigure stdout to UTF-8; when running ad-hoc Python that prints Bangla use `PYTHONIOENCODING=utf-8`.
- Variable fonts (Schibsted, JetBrains Mono) are embedded as Type3 by Chromium: this is normal and still embedded.
- Image reads can silently fail in long sessions; verify each read returned an image.

## Quick command reference
```
python .claude/skills/learn-easier/scripts/render_source.py "<src.pdf>" "<work>/src" 110
python .claude/skills/learn-easier/scripts/make.py "<Build folder>"            # build + render + checks + deliverables
```
