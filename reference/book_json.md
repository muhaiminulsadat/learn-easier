# book.json

Create in the project (build) folder. Working example: `examples/book.json`.

| key | meaning |
|---|---|
| title_lines | cover title split into 2–3 lines, e.g. ["Bituminous","Materials","&amp; Mix Design"] (HTML entities) |
| title_size | optional cover title px (default 58; use 46 for long titles) |
| kicker | small caps line above the title |
| tagline | one Bangla/English sentence under the title |
| cover_top | small top-left cover label, e.g. "CE 451 · PAVEMENT MATERIALS" |
| header_right | running header, right side, e.g. "Hadi Sir · CE 451" |
| footer_credit | footer left, e.g. "সংকলন: Anika" (credit the original note taker/source) |
| chapter_word | "অধ্যায়" (default) |
| toc_title | "সূচিপত্র" (default) |
| cover_contents | up to 6 short strings listed in the "IN THIS BOOK" box |
| credits | 4 items {label,value}: lecturer, notes by, COMPILED BY (the user), COURSE CODE |
| extras | [{"file":"formulas","title":"…","sub":"…","mark":"∑"},{"file":"glossary",…,"mark":"Aa"}] → files `chapters/<file>.html` |

Optional `cover_art.svg` in the project folder: an SVG fragment drawn inside a 340×200 area (it is placed at left of the cover box). Example: `examples/cover_art_pavement_layers.svg`. Without it the contents list is shown alone. Draw a subject-appropriate simple diagram (rects/lines, the tint colours) when it helps.

Optional `notes_to_verify.md` in the project folder is appended to the verification list.

Notes (second book): `footer_credit` may name both sources, e.g. "সংকলন: Sadat · Hadi Sir-এর slide + Anika-র নোট". The contents page auto-splits over several pages when there are more than 8 chapters/extras; `cover_contents` still takes up to 6 strings.
