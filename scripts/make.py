"""Build -> render PDF -> per-page PNG previews -> fill report -> font check -> CHECK list.

Usage: python make.py <project_dir> [output_dir]
Default output_dir = <project_dir>/../<project name>_Output
Writes: <output>/<book>.pdf, <output>/PNG_2x/page_NN.png, <output>/CHECK_and_textbook_list.md
Previews (96 dpi) go to <project_dir>/prev/pNN.png for visual review.
"""
import subprocess, os, sys, re, html, json, shutil
import fitz
sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
proj = os.path.abspath(sys.argv[1])
out = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(os.path.dirname(proj), os.path.basename(proj).replace("_Build", "") + "_Output")
cfg = json.load(open(os.path.join(proj, "book.json"), encoding="utf-8"))
subprocess.run([sys.executable, os.path.join(HERE, "build.py"), proj], check=True)

CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]
browser = next((c for c in CANDIDATES if os.path.exists(c)), None) or shutil.which("msedge") or shutil.which("chrome") or shutil.which("chromium")
if not browser:
    raise SystemExit("No Edge/Chrome found for PDF printing.")

pdf = os.path.join(proj, "out.pdf")
if os.path.exists(pdf):
    os.remove(pdf)
url = "file:///" + os.path.join(proj, "index.html").replace("\\", "/").replace(" ", "%20")
profile = os.path.join(proj, ".browser_profile")
subprocess.run([browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--user-data-dir=" + profile, "--print-to-pdf=" + pdf, url], capture_output=True, timeout=600)
if not os.path.exists(pdf):
    raise SystemExit("PDF was not produced.")

d = fitz.open(pdf)
print("pages", len(d))
prev = os.path.join(proj, "prev")
os.makedirs(prev, exist_ok=True)
warn = []
for i, p in enumerate(d):
    n = i + 1
    path = os.path.join(prev, "p%02d.png" % n)
    p.get_pixmap(dpi=96).save(path)
    if n == 1:
        continue
    im = Image.open(path).convert("RGB")
    px = im.load()
    last = 0
    for y in range(70, 1060):
        for x in range(60, 740, 3):
            r, g, b = px[x, y]
            if abs(r - 252) + abs(g - 251) + abs(b - 247) > 12:
                last = y
                break
    fill = (last - 76) / (1055 - 76) * 100
    flag = ""
    if fill > 98:
        flag = "  <-- OVERFULL: may touch footer, move content to next page"
    elif fill < 40:
        flag = "  <-- NEARLY EMPTY: merge with neighbour page"
    if flag:
        warn.append(n)
    print("p%02d content-fill %.0f%%%s" % (n, fill, flag))

# font check: anything other than the four requested families is a fallback
# (Type3 = variable fonts Schibsted/JetBrains, embedded by Chromium as Type3: fine)
allowed = ("Atkinson", "HindSiliguri", "Schibsted", "JetBrains", "KaTeX")
bad = {}
for i, p in enumerate(d):
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                f = s["font"].split("+")[-1]
                if not f.startswith("Type3") and not any(a in f for a in allowed) and s["text"].strip():
                    bad.setdefault(f, set()).add((i + 1, s["text"].strip()[:10]))
for f, v in bad.items():
    print("FALLBACK FONT", f, sorted(v)[:8])
if not bad:
    print("fonts OK (only the 4 design fonts used)")

# deliverables
os.makedirs(os.path.join(out, "PNG_2x"), exist_ok=True)
name = re.sub(r"[^A-Za-z0-9]+", "_", html.unescape(" ".join(cfg["title_lines"]))).strip("_") + "_Notes.pdf"
shutil.copy(pdf, os.path.join(out, name))
for i, p in enumerate(d):
    p.get_pixmap(dpi=192).save(os.path.join(out, "PNG_2x", "page_%02d.png" % (i + 1)))

h = open(os.path.join(proj, "index.html"), encoding="utf-8").read()
pages = re.split(r'<section class="page', h)[1:]


def clean(s):
    s = re.sub(r"<svg.*?</svg>", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


chk, tb = [], []
for n, pg in enumerate(pages, start=1):
    for m in re.finditer(r'<span class="(chk|tb)">(.*?)</span>', pg):
        ctx = clean(pg[max(0, m.start() - 700):m.start()])[-110:]
        (chk if m.group(1) == "chk" else tb).append((n, clean(m.group(2)), ctx))
L = ["# CHECK items and (textbook) additions\n", "Page numbers = printed page numbers in the PDF.\n",
     "## A. [CHECK: unclear in original] (%d)\n" % len(chk), "| Page | Note | Text just before |\n|---|---|---|"]
for n, t, c in chk:
    L.append("| %d | %s | …%s |" % (n, t.replace("CHECK:", "").strip(), c.replace("|", "/")))
L += ["\n## B. (textbook) additions (%d)\n" % len(tb), "| Page | Text just before |\n|---|---|"]
for n, t, c in tb:
    L.append("| %d | …%s |" % (n, c.replace("|", "/")))
extra = os.path.join(proj, "notes_to_verify.md")
if os.path.exists(extra):
    L += ["\n## C. Other things to verify\n", open(extra, encoding="utf-8").read()]
open(os.path.join(out, "CHECK_and_textbook_list.md"), "w", encoding="utf-8").write("\n".join(L))
print("OUTPUT:", out)
print("CHECK items:", len(chk), "textbook items:", len(tb), "pages needing layout fix:", warn)
