# learn-easier 📚

> **Agent Skill**: Turn course materials (lecture slides, handwritten/scanned notes, textbooks, transcripts, Word documents) into beautifully formatted, print-ready A4 exam-revision study notes, cheat sheets, infographics, and glossaries.

Compatible with **Claude Code**, **Google Antigravity**, **Cursor**, **GitHub Copilot**, **Codex**, and any agent supporting the open Agent Skills standard.

---

## ⚡ Instant Install (Recommended)

Install directly using the official skills package manager:

### Project Install:
```bash
npx skills add muhaiminulsadat/learn-easier
```

### Global Install (Available across all projects & agents):
```bash
npx skills add muhaiminulsadat/learn-easier -g
```

---

## 🚀 Manual Install (Git Clone)

If you prefer installing via git:

### 1. Claude Code
```bash
# macOS / Linux
git clone https://github.com/muhaiminulsadat/learn-easier.git ~/.claude/skills/learn-easier

# Windows (PowerShell)
git clone https://github.com/muhaiminulsadat/learn-easier.git "$HOME\.claude\skills\learn-easier"
```

### 2. Antigravity / Gemini
```bash
# macOS / Linux
git clone https://github.com/muhaiminulsadat/learn-easier.git ~/.gemini/config/skills/learn-easier

# Windows (PowerShell)
git clone https://github.com/muhaiminulsadat/learn-easier.git "$HOME\.gemini\config\skills\learn-easier"
```

### 3. Project Workspace (Cursor / Windsurf / Codex)
```bash
git clone https://github.com/muhaiminulsadat/learn-easier.git .agents/skills/learn-easier
```

---

## ⚙️ Prerequisites

The skill scripts run locally to parse and compile your notes to PDF:

- **Python 3.8+**
  ```bash
  pip install pymupdf pillow
  ```
- **Node.js** (for offline KaTeX math formula rendering)
- **Google Chrome** or **Microsoft Edge** (used headless by `make.py` to print HTML chapters to vector PDF)

---

## 📖 How to Use

Once installed, simply ask your agent or invoke `/learn-easier`:

```text
/learn-easier "path/to/lecture_notes.pdf"
```
or
```text
Please convert my scanned lecture notes in "CE451/Lecture1-5.pdf" into study notes using the learn-easier skill.
```

### Output Features
- **Print-ready A4 Portrait Vector PDF**
- **Structured Explanations**: Bangla narrative sentences with standard English technical keywords, formulas, and units.
- **Rich Infographics**: Flowcharts, mind maps, comparison tables, and decision trees.
- **Active Recall**: Quick Revision tiles, Q&A blocks, memory tricks, common exam mistakes, and end-of-chapter cheat sheets.
- **Offline KaTeX Math**: Crystal clear math expressions rendered directly in HTML/PDF.
- **Quality Verification**: Automatic page overflow checks (>98%) and layout validation.

---

## 📂 Repository Structure

- `SKILL.md` – Main skill definition and procedure for the AI agent
- `assets/` – Styling and embedded fonts (Atkinson Hyperlegible, Hind Siliguri, JetBrains Mono, KaTeX)
- `examples/` – Sample chapter HTML, formula sheet, glossary, and `book.json` template
- `reference/` – Design specification, layout rules, components catalog, and sample PDF
- `scripts/` – Python and Node build scripts (`make.py`, `build.py`, `render_source.py`, `latex.js`)

---

## 👤 Author & Credits

- Designed and compiled by **Sadat** ([@muhaiminulsadat](https://github.com/muhaiminulsadat))
- Source credit is automatically preserved in page footers for original lecture notes.
