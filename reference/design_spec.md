# Design spec (the "exact design idea")

Source of truth, in order: `assets/style.css` (implements everything below) → `reference/reference_design.pdf` (49-page finished book: look at its pages) → `reference/inspiration/*.png` (the six original infographic reference images).
Before building any new book, open 3–4 pages of `reference_design.pdf` (cover, a chapter's first page, an infographic page, a Quick Revision page) so the output matches visually.

## Look
Clean, modern, student-friendly: premium-Notion-page meets well-made textbook. Hand-designed feel. NO emoji, NO gradient washes, NO left-border-stripe cards. Rounded cards, subtle shadows, generous whitespace, 72px margins, A4 portrait (794×1123 CSS px per page).

## Colours
paper #FCFBF7 · ink #1A1F36 · soft ink #4A5068 · pen blue #2747A8 · highlighter #FFE36E
Chapter tints (fill / accent): blue #DCE4FA/#2747A8 · yellow #FFEFAD/#8F6B00 · green #DAEEE2/#1F7A4D · red #FBE0DC/#B3382C · purple #E8E0F7/#5B3FA6 · tan #F2E5CF/#7F5F26 · teal #D5ECEE/#1B7C85 · lime #E6EBD3/#55701A (8th tint, added for 8+ chapters). Cycle in this order for chapter 1, 2, 3 …

## Fonts (all bundled in assets/fonts, embedded in the PDF)
Schibsted Grotesk = headings · Hind Siliguri = Bangla body · Atkinson Hyperlegible = English keywords · JetBrains Mono = formulas, labels, page numbers.
Sizes: body 16–17px, callouts 15–16px, labels ≥13px, headings 22–30px (chapter title 27px, h2 22px, h3 17px).

## Page furniture (automatic)
Running header (chapter name left, `header_right` right), footer (`footer_credit` left, dark pill page number right), coloured edge tab per chapter on the right edge, chapter strip at the top of each chapter's first page (number circle, lecture/date, title, line icon).

## Book structure
Cover → contents (colour-coded chapters, correct page numbers) → chapters in source order → formulas & key numbers cheat-sheet → key-terms glossary. Each chapter ends with a Quick Revision page.

## Readability / memory rules (these make it an exam tool)
- Every process, comparison, classification, list of tests/properties → an infographic, never a plain paragraph. At least one per chapter, normally 2–4.
- Every teacher question → Q&A block. Stressed/highlighted things → Important callout + one `<mark>`.
- Make a mnemonic for every list of 3+ items (first-letter words, e.g. "CAR-W").
- Numbers, grades, temperatures, ratios and formulas copied exactly. Added textbook facts carry `{{tb}}`.
- Pages ≤ ~85% full (build report warns above 98% or below 40%), balanced, no near-empty pages except the last page of a chapter's Quick Revision.
- Diagrams: separate clean elements (boxes, diamonds for decisions, straight arrows). No overlapping labels.
- Icons: thin line only. Use the built-in set (see components.md).
