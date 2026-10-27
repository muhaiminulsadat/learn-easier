"""Turn a source PDF into page images (for reading handwritten/scanned content) and optional contact sheets.

Usage: python render_source.py <source.pdf> <out_dir> [dpi=110]
Writes out_dir/pNN.jpg and out_dir/sheetK.jpg (13 pages per sheet, labelled P<nn>).
Also prints how many pages have an extractable text layer (if > 0, read text directly: more accurate).
"""
import sys, os, glob
import fitz
from PIL import Image, ImageDraw

src, out = sys.argv[1], sys.argv[2]
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 110
os.makedirs(out, exist_ok=True)
d = fitz.open(src)
texty = 0
for i, p in enumerate(d):
    if len(p.get_text().strip()) > 40:
        texty += 1
    p.get_pixmap(dpi=dpi).save(os.path.join(out, "p%02d.jpg" % (i + 1)))
print("pages:", len(d), "| pages with text layer:", texty)
fs = sorted(glob.glob(os.path.join(out, "p*.jpg")))
W, H = 400, 566
for k in range(0, len(fs), 13):
    sheet = Image.new("RGB", (W * 5, H * 3), "white")
    for i, f in enumerate(fs[k:k + 13]):
        im = Image.open(f).resize((W, H))
        dr = ImageDraw.Draw(im)
        dr.rectangle([0, 0, 70, 34], fill="red")
        dr.text((8, 8), "P" + os.path.basename(f)[1:3], fill="white")
        sheet.paste(im, ((i % 5) * W, (i // 5) * H))
    sheet.save(os.path.join(out, "sheet%d.jpg" % (k // 13)))
print("sheets written (use for outline only; transcribe from the single-page images)")
