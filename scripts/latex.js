// Reads JSON [{tex, display}] from stdin, prints JSON [html] (KaTeX, html-only output).
const katex = require("../assets/katex/katex.min.js");
let s = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (c) => (s += c));
process.stdin.on("end", () => {
  const items = JSON.parse(s);
  const out = items.map((it) => {
    try {
      return katex.renderToString(it.tex, { displayMode: !!it.display, output: "html", throwOnError: true, strict: "ignore", trust: false });
    } catch (e) {
      return '<span class="chk">LATEX ERROR: ' + String(e.message).replace(/[<>&]/g, "").slice(0, 80) + "</span>";
    }
  });
  process.stdout.write(JSON.stringify(out));
});
