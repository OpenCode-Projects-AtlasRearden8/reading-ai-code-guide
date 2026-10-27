#!/usr/bin/env python3
"""Build the "Reading AI-Written Code" static website.

Reads the book chapters from docs/*.md and generates a static HTML site in
site/: one page per chapter, a landing page, and a single-file full-book page.
No network access is used at build or view time.

Usage:
    python3 build.py            # build the site (creates/overwrites site/)

Requires the "markdown" package:  pip install -r requirements.txt
"""

import html
import pathlib
import re
import sys

try:
    import markdown
except ImportError:
    sys.stderr.write(
        "Error: the 'markdown' package is required.\n"
        "Install it with:  pip install -r requirements.txt\n"
    )
    sys.exit(1)

ROOT = pathlib.Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

BOOK_TITLE = "Reading AI-Written Code"
BOOK_SUBTITLE = "A non-coder's guide to using AI-written code safely"
CREDIT = "By Asdale Dynamics, LLC"

MD_EXTENSIONS = [
    "extra",
    "sane_lists",
    "toc",
]

MARKDOWN_INSTANCE = markdown.Markdown(extensions=MD_EXTENSIONS)

STYLE_CSS = """\
:root {
  --bg: #f8f7f2;
  --fg: #20241f;
  --muted: #68705f;
  --accent: #2e6e4e;
  --accent-soft: #e6f0e8;
  --border: #dde2d4;
  --code-bg: #eef0e6;
  --pre-bg: #24291f;
  --pre-fg: #eff0e6;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1b1e19;
    --fg: #e8ebe2;
    --muted: #9aa38f;
    --accent: #93d3af;
    --accent-soft: #24322a;
    --border: #343a30;
    --code-bg: #2a3027;
    --pre-bg: #12150f;
    --pre-fg: #e4e8d9;
  }
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  padding: 0 1rem;
  background: var(--bg);
  color: var(--fg);
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  font-size: 1.05rem;
  line-height: 1.65;
}
main {
  max-width: 46rem;
  margin: 0 auto;
  padding: 2rem 0 4rem;
}
h1, h2, h3, h4 { line-height: 1.25; color: var(--fg); }
h1 { font-size: 2rem; margin: 0 0 1rem; }
h2 { font-size: 1.4rem; margin: 2.2rem 0 0.7rem; padding-bottom: 0.25rem; border-bottom: 1px solid var(--border); }
h3 { font-size: 1.15rem; margin: 1.8rem 0 0.5rem; }
p, li { max-width: 46rem; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
code {
  font-family: ui-monospace, "Cascadia Code", Menlo, Consolas, monospace;
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0.1em 0.35em;
  font-size: 0.88em;
}
pre {
  background: var(--pre-bg);
  color: var(--pre-fg);
  border-radius: 8px;
  padding: 0.9rem 1.1rem;
  overflow-x: auto;
  line-height: 1.5;
}
pre code {
  background: none;
  border: none;
  padding: 0;
  color: inherit;
  font-size: 0.88em;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1.2rem 0;
  font-size: 0.95rem;
}
th, td {
  border: 1px solid var(--border);
  padding: 0.5rem 0.7rem;
  text-align: left;
  vertical-align: top;
}
th { background: var(--accent-soft); }
blockquote {
  margin: 1.2rem 0;
  padding: 0.6rem 1.1rem;
  border-left: 4px solid var(--accent);
  background: var(--accent-soft);
  border-radius: 0 6px 6px 0;
  color: var(--fg);
}
blockquote p { color: var(--fg); }
blockquote blockquote { border-left-color: var(--muted); background: transparent; }
hr { border: none; border-top: 1px solid var(--border); margin: 2.5rem 0; }
li.todo, li.done { list-style: none; margin-left: -1.4em; }
li.todo .box, li.done .box { color: var(--accent); font-weight: 700; margin-right: 0.35em; }
li.done .box { color: #4c8a4c; }
li.done { color: var(--muted); }
li.done s { text-decoration-color: var(--muted); }
.site-header { max-width: 46rem; margin: 0 auto; padding-top: 1.5rem; }
.bookmark { font-size: 0.8rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; }
.bookmark a { color: inherit; }
.chapter-meta { color: var(--muted); font-size: 0.9rem; margin-top: -0.4rem; }
.nav {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  border-top: 1px solid var(--border);
  margin-top: 3rem;
  padding-top: 1rem;
  max-width: 46rem;
  margin-left: auto;
  margin-right: auto;
}
.nav a { font-size: 0.95rem; }
.footer {
  text-align: center;
  color: var(--muted);
  font-size: 0.85rem;
  margin-top: 2rem;
}
.btn-nav { display: flex; justify-content: center; gap: 0.4rem; margin: 1rem auto; flex-wrap: wrap; }
.btn-nav a {
  font-size: 0.85rem;
  border: 1px solid var(--border);
  border-radius: 999px;
  padding: 0.15rem 0.8rem;
  background: var(--accent-soft);
}
.btn-nav a:hover { text-decoration: none; border-color: var(--accent); }
.chapters { list-style: none; padding: 0; }
.chapters li { margin: 1.1rem 0; }
.chapters .ch-title { font-size: 1.15rem; font-weight: 600; }
.chapters .ch-blurb { color: var(--muted); font-size: 0.95rem; margin: 0.15rem 0 0; }
.toc-list { background: var(--accent-soft); border: 1px solid var(--border); border-radius: 8px; padding: 1rem 1.5rem; }
@media print {
  .nav, .btn-nav { display: none; }
  body { background: #fff; }
}
"""


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def scan_convert_task_lists(markdown_text: str) -> str:
    """Convert checkbox markers to HTML-friendly forms.

    Tracks fenced code blocks so literal markers inside code are untouched.
    Handles both '- [ ] ' and the typographic '- ☐ ' used in this book.
    """
    out_lines = []
    in_fence = False
    fence_re = re.compile(r"^\s*(```|~~~)")
    open_re = re.compile(r"^(\s*(?:-\s|\*\s)?\s*)\[ \]\s")
    done_re = re.compile(r"^(\s*(?:-\s|\*\s)?\s*)\[x\]\s", re.IGNORECASE)
    for line in markdown_text.splitlines():
        if fence_re.match(line) and (line.strip().startswith("```") or line.strip().startswith("~~~")):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if not in_fence:
            if open_re.match(line):
                line = open_re.sub(r"\1☐ ", line, count=1)
            elif done_re.match(line):
                line = done_re.sub(r"\1☑ ", line, count=1)
        out_lines.append(line)
    return "\n".join(out_lines) + ("\n" if markdown_text.endswith("\n") else "")


def style_task_lists(html_text: str) -> str:
    """Turn plain ☐/☑ list items into styled checkbox <li> elements."""
    html_text = re.sub(r"<li>☐\s*", '<li class="todo"><span class="box" aria-hidden="true">☐</span> ', html_text)
    html_text = re.sub(r"<li>☑\s*", '<li class="done"><span class="box" aria-hidden="true">☑</span> ', html_text)
    return html_text


def md_links_to_html(html_text: str) -> str:
    """Rewrite links pointing at docs/*.md to the generated .html pages."""
    return re.sub(r'(<a[^>]*href=")([^"]+)\.md(")', r"\1\2.html\3", html_text)


def external_links_rel(html_text: str) -> str:
    """Add rel/target to links that leave the site."""
    def fix(m: re.Match) -> str:
        tag, url = m.group(1), m.group(2)
        if re.match(r"https?://", url):
            return tag + url + m.group(3) + ' rel="noopener"'
        return m.group(0)
    return re.sub(r'(<a[^>]*href=")([^"]+)("\s[^>]*>|">)', fix, html_text)


def md_to_html(md_text: str) -> str:
    MARKDOWN_INSTANCE.reset()
    prepared = scan_convert_task_lists(md_text)
    body = MARKDOWN_INSTANCE.convert(prepared)
    body = style_task_lists(body)
    body = md_links_to_html(body)
    body = external_links_rel(body)
    return body


def chapter_slugs() -> list[str]:
    slugs = sorted(p.stem for p in DOCS.glob("*.md"))
    if "index" in slugs:
        slugs.remove("index")
        slugs.insert(0, "index")
    return slugs


def chapter_label(slug: str) -> str:
    if slug == "index":
        return "Welcome"
    m = re.match(r"^(\d+)-", slug)
    if m:
        return f"Chapter {int(m.group(1))}"
    return slug.replace("-", " ").title()


def chapter_title(md_text: str, fallback: str) -> tuple[str, str]:
    """Return (title, blurb): first # H1, then the first non-heading line after it."""
    title = fallback.title()
    blurb = ""
    lines = md_text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            for j in range(i + 1, min(i + 40, len(lines))):
                candidate = lines[j].strip()
                if not candidate or candidate.startswith("#"):
                    continue
                blurb = re.sub(r"[*_`#>|]", "", candidate)
                break
            break
    return title, blurb


def strip_h1(md_text: str) -> str:
    return re.sub(r"^# .*\n", "", md_text, count=1)


def page_shell(title: str, body_html: str, extra_head: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{BOOK_TITLE} — {BOOK_SUBTITLE}, by Asdale Dynamics, LLC">
<title>{html.escape(title)} · {BOOK_TITLE}</title>
<link rel="stylesheet" href="style.css">
{extra_head}
</head>
<body>
{body_html}
</body>
</html>
"""


def unit_footer(chapter_label: str = "") -> str:
    here = f' · {html.escape(chapter_label)}' if chapter_label else ""
    return (
        '<div class="footer">'
        f"{html.escape(BOOK_TITLE)}{here} · {html.escape(CREDIT)} · "
        'MIT License · <a href="index.html">contents</a>'
        "</div>"
    )


def build() -> None:
    if not DOCS.is_dir():
        sys.stderr.write("Error: docs/ directory not found.\n")
        sys.exit(1)
    SITE.mkdir(parents=True, exist_ok=True)

    slugs = chapter_slugs()
    if not slugs:
        sys.stderr.write("Error: no markdown chapters in docs/.\n")
        sys.exit(1)

    chapters = []  # (slug, title, md_text, words)
    for slug in slugs:
        path = DOCS / f"{slug}.md"
        text = read_text(path)
        fallback = slug.replace("-", " ")
        title, _ = chapter_title(text, fallback)
        chapters.append((slug, title, text, len(text.split())))

    total_words = sum(c[3] for c in chapters)

    # One page per chapter
    for i, (slug, title, text, words) in enumerate(chapters):
        prev_slug, prev_title = chapters[i - 1][:2] if i > 0 else (None, None)
        next_slug, next_title = chapters[i + 1][:2] if i < len(chapters) - 1 else (None, None)
        label = chapter_label(slug) if slug != "index" else "Welcome"

        body_parts = [
            '<div class="site-header"><div class="bookmark">'
            f'<a href="index.html">{html.escape(BOOK_TITLE)}</a></div></div>',
            "<main>",
            f"<h1>{html.escape(title)}</h1>",
            f'<div class="chapter-meta">{label} · '
            f"~{words:,} words · ~{max(1, round(words / 220))} min read</div>",
            md_to_html(strip_h1(text)),
            "</main>",
            '<div class="nav">',
            f'<a href="{prev_slug}.html">← {html.escape(prev_title)}</a>' if prev_slug else "<span></span>",
            f'<a href="{next_slug}.html">{html.escape(next_title)} →</a>' if next_slug else "<span></span>",
            "</div>",
            unit_footer(label),
        ]
        (SITE / f"{slug}.html").write_text(page_shell(title, "\n".join(body_parts)), encoding="utf-8")

    # Landing page
    items = []
    for i, (slug, title, text, words) in enumerate(chapters):
        _, blurb = chapter_title(text, slug)
        minutes = max(1, round(words / 220))
        items.append(
            f'<li><div class="ch-title"><a href="{slug}.html">{html.escape(title)}</a></div>'
            f'<p class="ch-blurb">{html.escape(blurb)}</p>'
            f'<p class="ch-blurb">{chapter_label(slug)} · ~{minutes} min read</p></li>'
        )
    landing_body = f"""\
<div class="site-header"><div class="bookmark">{html.escape(CREDIT)}</div></div>
<main>
<h1>{html.escape(BOOK_TITLE)}</h1>
<p class="chapter-meta">{html.escape(BOOK_SUBTITLE)}</p>
<p>A plain-English manual for people who get code written <em>for</em> them by AI
helpers: what code even does, how to read it without being a programmer,
spotting the <strong>"trust me"</strong> moments, asking what could break,
testing in a playground before you rely on anything, keeping originals safe,
and the copy-run-rollback routine that ends with a tool you actually own.
 Includes an annotated walkthrough of a real, runnable example script —
plus a printable safety checklist and a pocket glossary.</p>
<div class="toc-list">
<h2 style="margin-top:0.4rem">Contents</h2>
<ul class="chapters" style="margin:0.5rem 0 0">
{''.join(items)}
</ul>
</div>
<h2>One-page edition</h2>
<p>Prefer the whole book on one page for reading or printing?
<a href="full-book.html">Read the full single-file edition</a>.</p>
<h2>Details</h2>
<table>
<tr><td>Format</td><td>Welcome page + 10 chapters, built into this static site</td></tr>
<tr><td>Length</td><td>~{total_words:,} words</td></tr>
<tr><td>Runnable example</td><td><code>examples/walkthrough/safe_rename.py</code> (dry-run by default)</td></tr>
<tr><td>License</td><td>MIT (see LICENSE in the repository)</td></tr>
<tr><td>Companions</td><td><em>Free AI Coding with OpenCode</em> and <em>Terminal Comfort Guide</em></td></tr>
</table>
</main>
{unit_footer()}
"""
    (SITE / "index.html").write_text(page_shell(BOOK_TITLE, landing_body), encoding="utf-8")

    # Full-book single page
    sections = []
    toc_items = []
    for i, (slug, title, text, _words) in enumerate(chapters):
        anchor = f"ch-{i}-{slug}"
        toc_items.append(f'<li><a href="#{anchor}">{html.escape(title)}</a></li>')
        sections.append(
            f'<section id="{anchor}">'
            f"<h1>{html.escape(title)}</h1>" + md_to_html(strip_h1(text)) + "</section><hr>"
        )
    full_body = f"""\
<div class="site-header"><div class="bookmark">
<a href="index.html">{html.escape(BOOK_TITLE)}</a> · full-book edition</div></div>
<main>
<h1>{html.escape(BOOK_TITLE)}</h1>
<div class="toc-list"><h2 style="margin-top:0.3rem">Contents (jump to chapter)</h2>
<ol style="margin:0.5rem 0 0">{''.join(toc_items)}</ol></div>
{''.join(sections)}
</main>
{unit_footer()}
"""
    (SITE / "full-book.html").write_text(page_shell(f"{BOOK_TITLE} — full book", full_body), encoding="utf-8")

    (SITE / "style.css").write_text(STYLE_CSS, encoding="utf-8")

    print(f"Built {len(chapters)} chapter pages + index + full-book edition into site/")
    print(f"Total book length: ~{total_words:,} words")


if __name__ == "__main__":
    build()
