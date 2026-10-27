"""Build index.html from a project folder.

Usage: python build.py <project_dir>

<project_dir> contains:
  book.json                 book settings (see reference/book_json.md)
  chapters/ch1.html ...     one file per chapter (see reference/components.md)
  chapters/<extra>.html     optional extra sections listed in book.json "extras"
  cover_art.svg             optional illustration for the cover (inside a 650x250 box)
The skill's assets (style.css, fonts/) are copied next to index.html.
"""
import re, json, glob, os, sys, shutil, subprocess, html as _html

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
TINTS = ["blue", "yellow", "green", "red", "purple", "tan", "teal", "lime"]
CARD_TINTS = [("yellow", "a-yellow"), ("blue", "blue"), ("green", "a-green"), ("purple", "a-purple")]

ICONS = {
 "droplet": '<path d="M12 3c3 4.2 6 7.2 6 10.5a6 6 0 0 1-12 0C6 10.2 9 7.2 12 3z"/>',
 "flask": '<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4A2 2 0 0 0 19 18l-5-9V3M7.5 14h9"/>',
 "flame": '<path d="M12 3c1 3 5 5 5 10a5 5 0 0 1-10 0c0-2 1-3 2-4 0 2 1 3 2 3 0-3-1-5 1-9z"/>',
 "gauge": '<path d="M4 17a8 8 0 1 1 16 0M12 17l4-5M7 21h10"/>',
 "truck": '<path d="M3 6h11v10H3zM14 9h4l3 3v4h-7"/><circle cx="7.5" cy="18" r="1.6"/><circle cx="17.5" cy="18" r="1.6"/>',
 "thermo": '<path d="M10 14V5a2 2 0 0 1 4 0v9a4 4 0 1 1-4 0zM12 9v7"/>',
 "ruler": '<path d="M3 15L15 3l6 6L9 21zM7 11l2 2M10 8l2 2M13 5l2 2"/>',
 "shield": '<path d="M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6z"/>',
 "umbrella": '<path d="M3 12a9 9 0 0 1 18 0zM12 12v6a2 2 0 0 0 4 0"/>',
 "layers": '<path d="M12 3l9 5-9 5-9-5zM3 13l9 5 9-5"/>',
 "mountain": '<path d="M3 19l6-11 4 7 3-4 5 8z"/>',
 "road": '<path d="M7 3L4 21M17 3l3 18M12 4v3M12 10v4M12 17v3"/>',
 "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
 "xc": '<circle cx="12" cy="12" r="9"/><path d="M9 9l6 6M15 9l-6 6"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "scale": '<path d="M12 4v16M6 20h12M5 8h14M5 8l-3 7a3 3 0 0 0 6 0zM19 8l-3 7a3 3 0 0 0 6 0z"/>',
 "sieve": '<path d="M4 9h16l-2 10H6zM4 9a8 3 0 0 1 16 0"/><path d="M9 13h.01M12 15h.01M15 13h.01M10 17h.01M14 17h.01"/>',
 "cube": '<path d="M12 3l8 4v10l-8 4-8-4V7zM12 12l8-5M12 12v9M12 12L4 7"/>',
 "wave": '<path d="M3 12c3-6 5 6 9 0s6 6 9 0"/>',
 "bulb": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10c1 1 1 2 1 3h6c0-1 0-2 1-3a6 6 0 0 0-4-10z"/>',
 "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
 "alert": '<path d="M12 4l9 16H3zM12 10v4M12 17v.5"/>',
 "bookmark": '<path d="M6 3h12v18l-6-4-6 4z"/>',
 "rain": '<path d="M7 15a4 4 0 1 1 1-7.9A5 5 0 0 1 17.5 8.5 3.5 3.5 0 0 1 17 15zM9 18l-1 3M13 18l-1 3M17 18l-1 3"/>',
 "hammer": '<path d="M14 4l6 6-3 3-6-6zM12 8L4 16l4 4 8-8"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
 "chart": '<path d="M4 20V4M4 20h16M7 15l4-5 3 3 5-7"/>',
 "pit": '<path d="M3 8h18M5 8v10h14V8M8 12h2M13 14h3"/>',
 "factory": '<path d="M3 20V10l6 4v-4l6 4V6h3v14zM8 20v-3M12 20v-3M16 20v-3"/>',
 "tire": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><path d="M12 3v6M12 15v6M3 12h6M15 12h6"/>',
 "magnet": '<path d="M6 3v9a6 6 0 0 0 12 0V3h-4v9a2 2 0 0 1-4 0V3zM6 7h4M14 7h4"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
 "link": '<path d="M10 14a4 4 0 0 0 5.6 0l3-3a4 4 0 0 0-5.6-5.6l-1 1M14 10a4 4 0 0 0-5.6 0l-3 3a4 4 0 0 0 5.6 5.6l1-1"/>',
 "list": '<path d="M8 6h12M8 12h12M8 18h12M4 6h.01M4 12h.01M4 18h.01"/>',
 "weight": '<path d="M6 8h12l2 12H4zM9 8a3 3 0 0 1 6 0"/>',
}
# extra icons added for non-civil subjects (same 24x24 line style: stroke 1.6, round caps)
ICONS.update({
 "book": '<path d="M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4zM20 4h-6a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h7z"/>',
 "pencil": '<path d="M4 20l1-4L16 5l3 3L8 19zM14 7l3 3"/>',
 "calc": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h.01M12 12h.01M16 12h.01M8 16h.01M12 16h.01M16 16h.01"/>',
 "bolt": '<path d="M13 3L5 14h6l-1 7 8-11h-6z"/>',
 "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/>',
 "chip": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
 "dna": '<path d="M7 3c0 6 10 6 10 12s-10 6-10 6M17 3c0 6-10 6-10 12M8 7h8M8 17h8"/>',
 "atom": '<circle cx="12" cy="12" r="1.5"/><ellipse cx="12" cy="12" rx="9" ry="3.5"/><ellipse cx="12" cy="12" rx="9" ry="3.5" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="9" ry="3.5" transform="rotate(120 12 12)"/>',
 "coin": '<circle cx="12" cy="12" r="9"/><path d="M14.5 9c-.5-1-1.5-1.5-2.5-1.5-1.5 0-2.5.8-2.5 2s1 1.7 2.5 2 2.5.8 2.5 2-1 2-2.5 2c-1 0-2-.5-2.5-1.5M12 6v1.5M12 16.5V18"/>',
 "people": '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M16 5.5a3 3 0 0 1 0 5M18 14c2 .6 3 2.4 3 6"/>',
 "scales": '<path d="M12 4v16M6 20h12M5 7h14M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
 "code": '<path d="M8 8l-5 4 5 4M16 8l5 4-5 4M14 5l-4 14"/>',
 "map": '<path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2zM9 4v14M15 6v14"/>',
 "heart": '<path d="M12 20s-8-5-8-11a4.5 4.5 0 0 1 8-2.5A4.5 4.5 0 0 1 20 9c0 6-8 11-8 11z"/>',
 "leaf": '<path d="M5 19c0-9 5-14 15-14 0 10-5 15-14 15zM5 19c2-5 5-8 9-10"/>',
 "wrench": '<path d="M14 6a4 4 0 0 0 5 5l-9 9a2.5 2.5 0 0 1-3.5-3.5l9-9z"/>',
 "pipe": '<path d="M3 9h8V5h4v4h6M3 15h4v4h4v-4h10"/>',
 "building": '<path d="M5 21V4h9v17M14 9h5v12M8 8h3M8 12h3M8 16h3M3 21h18"/>',
 "wheel": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2"/><path d="M12 3v7M12 14v7M3 12h7M14 12h7"/>',
})
ARROW = '<svg viewBox="0 0 22 14"><path d="M1 7h19M14 2l6 5-6 5"/></svg>'


def icon(m):
    n = m.group(1)
    if n not in ICONS:
        raise SystemExit("Unknown icon {{ic:%s}}. Available: %s" % (n, ", ".join(sorted(ICONS))))
    return '<svg class="ic" viewBox="0 0 24 24">%s</svg>' % ICONS[n]


def expand(s):
    s = re.sub(r"\{\{ic:(\w+)\}\}", icon, s)
    s = s.replace("{{arr}}", '<div class="arr">%s</div>' % ARROW)
    s = s.replace("{{CHK}}", '<span class="chk">CHECK: unclear in original</span>')
    s = re.sub(r"\{\{chk:([^}]*)\}\}", lambda m: '<span class="chk">CHECK: %s</span>' % m.group(1), s)
    s = s.replace("{{tb}}", '<span class="tb">textbook</span>')
    return s


LATEX_RE = re.compile(r"\\\[(.+?)\\\]|\\\((.+?)\\\)", re.S)


def latex(s):
    """Render LaTeX (inline: backslash-paren, display: backslash-bracket) with KaTeX via node. Skips <svg> blocks."""
    items, spans = [], []
    for m in LATEX_RE.finditer(s):
        if "<svg" in s[max(0, m.start() - 4000):m.start()] and s[max(0, m.start() - 4000):m.start()].rfind("<svg") > s[max(0, m.start() - 4000):m.start()].rfind("</svg>"):
            continue
        disp = m.group(1) is not None
        tex = _html.unescape(m.group(1) if disp else m.group(2)).strip()
        items.append({"tex": tex, "display": disp})
        spans.append((m.start(), m.end(), disp))
    if not items:
        return s
    r = subprocess.run(["node", os.path.join(HERE, "latex.js")], input=json.dumps(items), capture_output=True, text=True, encoding="utf-8", check=True)
    outs = json.loads(r.stdout)
    res, last = [], 0
    for (a, b, disp), h in zip(spans, outs):
        res.append(s[last:a])
        res.append('<div class="fm">%s</div>' % h if disp else h)
        last = b
    res.append(s[last:])
    return "".join(res)


def split_pages(body):
    parts = re.split(r"<!--PAGE([^>]*)-->", body)
    return [(parts[i].strip(), parts[i + 1].strip()) for i in range(1, len(parts), 2)]


def load_chapters(proj):
    chs = []
    for f in sorted(glob.glob(os.path.join(proj, "chapters", "ch*.html")), key=lambda p: int(re.findall(r"ch(\d+)", os.path.basename(p))[0])):
        t = open(f, encoding="utf-8").read()
        meta = json.loads(re.search(r"<!--META(.*?)-->", t, re.S).group(1))
        body = t[t.index("-->", t.index("<!--META")) + 3:]
        meta.setdefault("tint", TINTS[(meta["n"] - 1) % len(TINTS)])
        meta.setdefault("icon", "layers")
        meta["pages"] = split_pages(body)
        chs.append(meta)
    return chs


def page(cfg, ch, tint, num, inner, header_title, cls="", show_tab=True):
    tab = ""
    if show_tab and ch:
        tab = '<div class="tab" style="top:%dpx">%s</div>' % (150 + ((ch - 1) % 11) * 74, ch)
    return (
        '<section class="page %s" data-ch="%d" data-tint="%s">'
        '<div class="hdr"><div class="l"><span class="dot"></span>%s</div><div>%s</div></div>'
        '%s<div class="content">%s</div>'
        '<div class="ftr"><div>%s</div><div class="pn">%d</div></div></section>'
    ) % (cls, ch, tint, header_title, cfg["header_right"], tab, inner, cfg["footer_credit"], num)


def strip(cfg, m):
    return (
        '<div class="strip"><div class="num">%d</div><div><div class="meta">%s %d &middot; %s &middot; %s</div>'
        '<h1>%s</h1></div>{{ic:%s}}</div>'
    ) % (m["n"], cfg.get("chapter_word", "অধ্যায়"), m["n"], m["lec"], m["date"], m["bn"], m["icon"])


def cover(cfg, proj):
    art = os.path.join(proj, "cover_art.svg")
    lines = "<br>".join(cfg["title_lines"])
    items = "".join('<text x="0" y="%d" font-size="16" fill="#1A1F36">%s</text>' % (46 + 28 * i, t) for i, t in enumerate(cfg["cover_contents"][:6]))
    if os.path.exists(art):
        art_svg = open(art, encoding="utf-8").read()
        box = (
            '<svg style="position:absolute;left:72px;top:560px" width="650" height="250" viewBox="0 0 650 250">'
            '<rect x="0" y="0" width="650" height="250" rx="22" fill="#fff" stroke="#E4E1D6"/>'
            '<g transform="translate(40,34)">%s</g>'
            '<g transform="translate(410,40)"><text x="0" y="14" class="m" font-size="13" fill="#2747A8" font-weight="700">IN THIS BOOK</text>%s</g></svg>'
        ) % (art_svg, items)
    else:
        box = (
            '<svg style="position:absolute;left:72px;top:560px" width="650" height="250" viewBox="0 0 650 250">'
            '<rect x="0" y="0" width="650" height="250" rx="22" fill="#fff" stroke="#E4E1D6"/>'
            '<g transform="translate(40,40)"><text x="0" y="14" class="m" font-size="13" fill="#2747A8" font-weight="700">IN THIS BOOK</text>%s</g></svg>'
        ) % items
    cards = ""
    for i, c in enumerate(cfg["credits"][:4]):
        tint, acc = CARD_TINTS[i]
        cards += (
            '<div style="background:var(--c-%s);border-radius:16px;padding:14px 18px"><div style="font-family:\'JetBrains Mono\',\'Hind\';font-size:13px;'
            'color:var(--%s);font-weight:700;letter-spacing:.05em">%s</div><div style="font-family:\'Schibsted Grotesk\',\'Hind\';font-size:22px;font-weight:800">%s</div></div>'
        ) % (tint, acc, c["label"], c["value"])
    return (
        '<section class="page cover" data-ch="0" data-tint="blue"><div class="content">'
        '<div style="position:absolute;left:72px;right:72px;top:72px;display:flex;justify-content:space-between;font-family:\'JetBrains Mono\',\'Hind\';font-size:13px;color:var(--soft)">'
        '<div style="display:flex;align-items:center;gap:8px"><span style="width:12px;height:12px;border-radius:4px;background:var(--blue);display:inline-block"></span>%s</div><div>STUDY NOTES</div></div>'
        '<div style="position:absolute;left:72px;right:72px;top:150px">'
        '<div style="font-family:\'JetBrains Mono\',\'Hind\';font-size:14px;color:var(--blue);letter-spacing:.08em;font-weight:500">%s</div>'
        '<h1 style="font-family:\'Schibsted Grotesk\',\'Hind\';font-weight:800;font-size:%dpx;line-height:1.05;margin:12px 0 14px;letter-spacing:-.01em">%s</h1>'
        '<p style="font-size:21px;color:var(--soft);line-height:1.55;max-width:560px">%s</p></div>'
        '%s'
        '<div style="position:absolute;left:72px;right:72px;bottom:96px;display:grid;grid-template-columns:1fr 1fr;gap:12px">%s</div>'
        '</div></section>'
    ) % (cfg["cover_top"], cfg["kicker"], cfg.get("title_size", 58), lines, cfg["tagline"], box, cards)


def main():
    proj = os.path.abspath(sys.argv[1])
    cfg = json.load(open(os.path.join(proj, "book.json"), encoding="utf-8"))
    for k in ("title_lines", "kicker", "tagline", "cover_top", "header_right", "footer_credit", "cover_contents", "credits"):
        if k not in cfg:
            raise SystemExit("book.json missing key: " + k)
    for d in ("fonts",):
        dst = os.path.join(proj, d)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(ASSETS, d), dst)
    shutil.copy(os.path.join(ASSETS, "style.css"), os.path.join(proj, "style.css"))
    shutil.copy(os.path.join(ASSETS, "katex", "katex.min.css"), os.path.join(proj, "katex.css"))

    chs = load_chapters(proj)
    extras = []
    for e in cfg.get("extras", []):
        f = os.path.join(proj, "chapters", e["file"] + ".html")
        if os.path.exists(f):
            extras.append((e, [p for _, p in split_pages(open(f, encoding="utf-8").read())]))
    TOC_PER_PAGE = 8
    n_toc = max(1, -(-(len(chs) + len(extras)) // TOC_PER_PAGE))
    cur = 2 + n_toc
    starts, ex_start = {}, {}
    for m in chs:
        starts[m["n"]] = cur
        cur += len(m["pages"])
    for e, pgs in extras:
        ex_start[e["file"]] = cur
        cur += len(pgs)

    out = [cover(cfg, proj)]
    rowlist = []
    for m in chs:
        rowlist.append(
            '<div class="toc-row"><div class="tn" style="background:var(--c-%s);color:var(--a-%s)">%d</div>'
            '<div class="tt"><b>%s</b><span>%s &middot; %s &middot; %s</span></div><div class="pg">%d</div></div>'
            % (m["tint"], m["tint"], m["n"], m["bn"], m["lec"], m["date"], m["topics"], starts[m["n"]]))
    for e, pgs in extras:
        rowlist.append(
            '<div class="toc-row"><div class="tn" style="background:#EFEDE4;color:var(--ink)">%s</div>'
            '<div class="tt"><b>%s</b><span>%s</span></div><div class="pg">%d</div></div>'
            % (e.get("mark", "+"), e["title"], e.get("sub", ""), ex_start[e["file"]]))
    for k in range(n_toc):
        rows = "".join(rowlist[k * TOC_PER_PAGE:(k + 1) * TOC_PER_PAGE])
        toc = (
            '<div style="font-family:&quot;JetBrains Mono&quot;,&quot;Hind&quot;;font-size:13px;color:var(--blue);letter-spacing:.06em;font-weight:500">CONTENTS%s</div>'
            '<h1 style="font-family:&quot;Schibsted Grotesk&quot;,&quot;Hind&quot;;font-weight:800;font-size:30px;margin:-4px 0 8px">%s</h1>%s'
        ) % (" %d/%d" % (k + 1, n_toc) if n_toc > 1 else "", cfg.get("toc_title", "সূচিপত্র"), rows)
        out.append(page(cfg, 0, "blue", 2 + k, toc, cfg.get("toc_title", "সূচিপত্র"), show_tab=False))

    n = 2 + n_toc
    for m in chs:
        for i, (flag, inner) in enumerate(m["pages"]):
            if i == 0:
                inner = strip(cfg, m) + inner
            out.append(page(cfg, m["n"], m["tint"], n, inner, "%s %d &middot; %s" % (cfg.get("chapter_word", "অধ্যায়"), m["n"], m["en"]), "qr" if "qr" in flag else ""))
            n += 1
    for e, pgs in extras:
        for inner in pgs:
            out.append(page(cfg, 0, "blue", n, inner, e["title"], show_tab=False))
            n += 1

    html = (
        '<!doctype html><html lang="bn"><head><meta charset="utf-8"><title>%s</title>'
        '<link rel="stylesheet" href="katex.css"><link rel="stylesheet" href="style.css"></head><body>%s</body></html>'
    ) % (re.sub(r"<[^>]+>", " ", " ".join(cfg["title_lines"])).replace("&amp;", "&"), "\n".join(out))
    open(os.path.join(proj, "index.html"), "w", encoding="utf-8").write(latex(expand(html)))
    print("pages:", n - 1, "starts:", starts, ex_start)


if __name__ == "__main__":
    main()
