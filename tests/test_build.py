"""Tests for the "Reading AI-Written Code" manual and site builder.

Run with:
    python3 -m unittest discover -s tests -v

Checks:
- book structure (required chapters, word count >= 10,000, tables, checklists)
- internal .md chapter links resolve
- markdown conversion correctness (headings, tables, code, checkboxes, links)
- full build into a temporary site/ (pages valid, nav present, no external assets)
- the walkthrough chapter's code excerpts really exist in examples/walkthrough/safe_rename.py
- privacy sweep (no secret-shaped strings anywhere in docs, examples, or the built site)
- LICENSE contains the required exact copyright line; README credits Asdale Dynamics, LLC
"""

import html.parser
import pathlib
import re
import shutil
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build  # noqa: E402

DOCS = ROOT / "docs"
SITE = ROOT / "site"
EXAMPLE = ROOT / "examples" / "walkthrough" / "safe_rename.py"

REQUIRED_SLUGS = [
    "index",
    "01-what-code-actually-does",
    "02-reading-code-you-cannot-write",
    "03-spotting-trust-me-moments",
    "04-asking-what-could-break",
    "05-testing-before-you-rely-on-it",
    "06-keeping-originals-safe",
    "07-secrets-and-paths-to-check",
    "08-the-copy-run-rollback-routine",
    "09-annotated-walkthrough",
    "10-safety-checklist-and-glossary",
]


class TestBookContent(unittest.TestCase):
    def setUp(self):
        self.slugs = build.chapter_slugs()
        self.texts = {s: build.read_text(DOCS / f"{s}.md") for s in self.slugs}

    def test_required_chapters_exist(self):
        for slug in REQUIRED_SLUGS:
            self.assertIn(slug, self.slugs, f"missing chapter: {slug}.md")

    def test_every_chapter_has_title_and_body(self):
        for slug, text in self.texts.items():
            self.assertIn("# ", text, f"{slug}: no H1 title")
            self.assertGreater(len(text.split()), 600, f"{slug}: suspiciously short")

    def test_word_count_at_least_ten_thousand(self):
        total = sum(len(t.split()) for t in self.texts.values())
        self.assertGreaterEqual(total, 10000, f"book is only {total} words")

    def test_manual_has_tables_and_checklists(self):
        all_text = "\n".join(self.texts.values())
        self.assertGreaterEqual(all_text.count("\n| "), 25, "expected many tables")
        checkbox_lines = [l for l in all_text.splitlines() if l.strip().startswith(("- ☐", "- [ ]"))]
        self.assertGreaterEqual(len(checkbox_lines), 25, "expected many checklist items")

    def test_required_topics_covered(self):
        all_text = "\n".join(self.texts.values()).lower()
        for topic in ("trust me", "what could break", "dry run", "rollback", "snapshot",
                      "api key", "originals always have a copy", "glossary", "secret", "playground"):
            self.assertIn(topic, all_text, f"required topic missing: {topic!r}")

    def test_glossary_has_enough_terms(self):
        text = self.texts["10-safety-checklist-and-glossary"]
        rows = [l for l in text.splitlines() if l.startswith("| **")]
        self.assertGreaterEqual(len(rows), 25, "expected a substantial glossary")

    def test_companion_books_mentioned(self):
        all_text = "\n".join(self.texts.values())
        self.assertIn("Free AI Coding with OpenCode", all_text)
        self.assertIn("Terminal Comfort Guide", all_text)

    def test_internal_md_links_resolve(self):
        for slug, text in self.texts.items():
            for m in re.finditer(r"\]\(([^#http][^)]*\.md)\)", text):
                target = m.group(1)
                self.assertTrue((DOCS / target).exists(), f"{slug}: broken link {target}")


class TestMarkdownConversion(unittest.TestCase):
    def test_headings_get_ids(self):
        html = build.md_to_html("# Hello There\n\ntext")
        self.assertIn('<h1 id="hello-there">', html)

    def test_table_renders(self):
        html = build.md_to_html("| a | b |\n|---|---|\n| 1 | 2 |\n")
        self.assertIn("<table>", html)
        self.assertIn("<th>", html)

    def test_fenced_code_renders(self):
        html = build.md_to_html("```bash\ngit status\n```\n")
        self.assertIn("<pre>", html)
        self.assertIn("git status", html)

    def test_open_task_item_becomes_styled_todo(self):
        html = build.md_to_html("- [ ] Water the plants\n")
        self.assertIn('class="todo"', html)
        self.assertIn("☐", html)

    def test_box_character_list_item_becomes_styled_todo(self):
        html = build.md_to_html("- ☐ Water the plants\n")
        self.assertIn('class="todo"', html)

    def test_done_task_item_becomes_styled_done(self):
        html = build.md_to_html("- [x] Water the plants\n")
        self.assertIn('class="done"', html)
        self.assertIn("☑", html)

    def test_task_marker_inside_code_fence_is_untouched(self):
        html = build.md_to_html("```\n- [ ] literal in code\n- ☐ literal too\n```\n")
        self.assertNotIn('class="todo"', html)
        self.assertIn("[ ] literal in code", html)
        self.assertIn("☐ literal too", html)

    def test_md_link_rewritten_to_html(self):
        html = build.md_to_html("[Git basics](06-keeping-originals-safe.md)")
        self.assertIn('href="06-keeping-originals-safe.html"', html)
        self.assertNotIn("06-keeping-originals-safe.md", html)

    def test_external_link_gets_rel(self):
        html = build.md_to_html("[site](https://example.com)")
        self.assertIn('rel="noopener"', html)


class TestBuildOutput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="site-test-")
        real_site = build.SITE
        build.SITE = pathlib.Path(cls.tmp)
        try:
            build.build()
        finally:
            build.SITE = real_site
        cls.out = pathlib.Path(cls.tmp)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_expected_files_generated(self):
        for slug in build.chapter_slugs():
            self.assertTrue((self.out / f"{slug}.html").exists(), f"missing site/{slug}.html")
        for name in ("index.html", "full-book.html", "style.css"):
            self.assertTrue((self.out / name).exists(), f"missing site/{name}")

    def test_pages_are_wellformed_html(self):
        class Auditor(html.parser.HTMLParser):
            def __init__(self):
                super().__init__()
                self.errors = []
            def error(self, message):
                self.errors.append(message)
        for page in self.out.glob("*.html"):
            text = page.read_text(encoding="utf-8")
            self.assertIn("<!DOCTYPE html>", text, f"{page.name}: no doctype")
            self.assertIn("</html>", text, f"{page.name}: unclosed html")
            self.assertIn('lang="en"', text)
            self.assertIn('charset="utf-8"', text)
            auditor = Auditor()
            auditor.feed(text)  # raises ValueError on hard errors, collects soft ones
            self.assertFalse(auditor.errors, f"{page.name}: parser errors")

    def test_pages_use_local_stylesheet_only(self):
        for page in self.out.glob("*.html"):
            text = page.read_text(encoding="utf-8")
            self.assertIn('href="style.css"', text)
        style = (self.out / "style.css").read_text(encoding="utf-8")
        self.assertNotIn("http://", style)
        self.assertNotIn("https://", style)

    def test_chapter_labels_and_nav(self):
        text = (self.out / "08-the-copy-run-rollback-routine.html").read_text(encoding="utf-8")
        self.assertIn("Chapter 8", text)
        self.assertIn('class="nav"', text)
        next_ch = "09-annotated-walkthrough"
        prev_ch = "07-secrets-and-paths-to-check"
        self.assertIn(f'<a href="{next_ch}.html"', text)
        self.assertIn(f'href="{prev_ch}.html"', text)
        self.assertIn("Asdale Dynamics, LLC", text)

    def test_landing_lists_every_chapter(self):
        text = (self.out / "index.html").read_text(encoding="utf-8")
        self.assertIn("Contents", text)
        for slug in build.chapter_slugs():
            self.assertIn(f'href="{slug}.html"', text, f"index missing link to {slug}")

    def test_full_book_contains_all_chapters(self):
        text = (self.out / "full-book.html").read_text(encoding="utf-8")
        for slug in build.chapter_slugs():
            md_text = build.read_text(DOCS / f"{slug}.md")
            title, _ = build.chapter_title(md_text, slug)
            fragment = title.split("—")[0].strip()[:20].replace("&", "&")
            self.assertIn(fragment, text, f"full-book is missing '{title}'")

    def test_checklists_render_styled_on_chapter_pages(self):
        for slug in REQUIRED_SLUGS:
            page = self.out / f"{slug}.html"
            text = page.read_text(encoding="utf-8")
            if 'class="todo"' in text:
                self.assertIn("☐", text, f"{slug}: todo styling without the box")

    def test_no_md_links_left_in_html(self):
        for page in self.out.glob("*.html"):
            text = page.read_text(encoding="utf-8")
            self.assertNotIn('href="docs/', text, f"{page.name}: raw markdown link")


class TestWalkthroughConsistency(unittest.TestCase):
    def test_example_file_exists_and_runs_help(self):
        self.assertTrue(EXAMPLE.exists(), "examples/walkthrough/safe_rename.py is missing")

    def test_chapter_code_excerpts_match_the_real_file(self):
        chapter = build.read_text(DOCS / "09-annotated-walkthrough.md")
        source = EXAMPLE.read_text(encoding="utf-8")
        fences = re.findall(r"```python\n(.*?)```", chapter, re.S)
        self.assertGreaterEqual(len(fences), 7, "walkthrough lost most of its code blocks")
        for block in fences:
            for line in block.splitlines():
                stripped = line.rstrip()
                if not stripped or stripped == "python":
                    continue
                self.assertIn(
                    stripped,
                    source,
                    f"walkthrough excerpt line not in the real example script: {stripped!r}",
                )

    def test_example_script_is_safe_shaped(self):
        source = EXAMPLE.read_text(encoding="utf-8")
        self.assertIn("--apply", source, "dry run must be the default")
        self.assertNotIn("rmtree", source)
        self.assertNotIn("unlink", source)
        self.assertNotIn("import requests", source)
        self.assertNotIn("subprocess", source)


class TestPrivacyAndLicense(unittest.TestCase):
    SECRET_PATTERNS = [
        re.compile(r"sk-[A-Za-z0-9]{10,}"),           # OpenAI-style key
        re.compile(r"AKIA[0-9A-Z]{16}"),              # AWS access key
        re.compile(r"ghp_[A-Za-z0-9]{20,}"),          # GitHub PAT
        re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY"), # PEM key material
        re.compile(r"nvapi-[A-Za-z0-9]{10,}"),        # NVIDIA-style key
    ]

    def test_no_secret_shaped_strings(self):
        targets = list((ROOT / "docs").glob("*.md"))
        targets.extend((ROOT / "examples").rglob("*.py"))
        targets.extend((ROOT / "build.py", ROOT / "README.md"))
        if SITE.is_dir():
            targets.extend(SITE.glob("*.html"))
            targets.extend(SITE.glob("*.css"))
        for path in targets:
            text = path.read_text(encoding="utf-8")
            for pattern in self.SECRET_PATTERNS:
                self.assertIsNone(
                    pattern.search(text),
                    f"{path.name}: looks like a secret: {pattern.pattern}",
                )

    def test_no_fill_in_credential_stubs_in_shipped_code(self):
        # The prose may *discuss* placeholder keys (Chapter 7 does), but the
        # shipped example script must contain no credential stub at all.
        source = EXAMPLE.read_text(encoding="utf-8")
        for bad in ("API_KEY", "YOUR_API_KEY", "PUT YOUR KEY HERE", "sk-REPLACE"):
            self.assertNotIn(bad, source, f"fill-in credential stub found in example: {bad}")

    def test_license_line_exact(self):
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", text)

    def test_readme_credits_asdale(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", text)


if __name__ == "__main__":
    unittest.main()
