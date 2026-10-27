# STATUS.md — Reading AI-Written Code

Last updated: 2026-10-27

## What was built

A complete beginner manual, **"Reading AI-Written Code"**, in two forms:

1. **`docs/`** — the source of truth: a welcome page plus 10 numbered chapters, ~17,300 words
   total. Written for non-coders who get AI-written code and need to use it safely: plain English
   throughout, tables and checklists everywhere, every jargon term explained on first use.
2. **`site/`** — a built static HTML site (committed, works offline): one page per chapter with
   prev/next navigation, a landing contents page, a single-file print-friendly `full-book.html`
   edition, and `style.css`. Zero external assets: no web fonts, no scripts, no trackers, nothing
   fetched from the network to view it.

Required topics, all covered as first-class chapters or sections:

| Topic | Where |
|---|---|
| What code even does | Ch 1 (recipe analogy, dissected real script, the four reader questions) |
| Reading AI-written code as a non-coder | Ch 2 (three passes: structure, power, boundaries + danger-word table) |
| Spotting the "trust me" moments | Ch 3 (phrase decoder table + trust-me *code* pattern table) |
| Asking what could break | Ch 4 (pre-mortem + core question set + question drills) |
| Testing before you rely on it | Ch 5 (playground fakes, dry runs, mini-real, run-twice, health checks) |
| Keeping originals saved | Ch 6 (two-snapshot move, naming rules, restore drill, anti-patterns) |
| Secrets and paths to check | Ch 7 (four leak doors, 2-minute secret sweep, dangerous-paths scan) |
| The copy-run-rollback routine | Ch 8 (the three-phase loop, printable checklist, ~10-minute budget) |
| Annotated example walkthrough | Ch 9 (real shipped script, block by block, incl. 3 caught trust-me traps) |
| Safety checklist | Ch 10 (one-page printable checklist) |
| Glossary | Ch 10 (pocket glossary, 28 plain-English terms) |

Supporting files:

- `examples/walkthrough/safe_rename.py` — the runnable annotated example from Chapter 9.
  Dry-run by default; `--apply` to act; refuses collisions; refuses to act outside the folder
  you name; prints a plan + count on every run. (Deliberately safe: no delete, no network,
  no subprocess.)
- `README.md` — overview, chapter map, build/test/run instructions, credit to Asdale Dynamics, LLC.
- `LICENSE` — MIT with the exact line `Copyright (c) 2026 Asdale Dynamics, LLC`.
- `build.py` — site generator (docs/*.md → site/*.html + index + full-book).
- `tests/test_build.py` — book-structure, conversion, build-output, walkthrough-consistency,
  privacy, and license tests (32 tests).
- `tests/test_examples.py` — runs the real example script as a subprocess and verifies its
  safety behaviors (8 tests).
- `requirements.txt` (build dependency: `markdown`), `.gitignore`.

Companion positioning: explicitly complements **Free AI Coding with OpenCode** (prompting/
permissions/Git/review workflow) and **Terminal Comfort Guide** (first-keystroke basics); both are
cross-referenced in the welcome page, Chapter 6, Chapter 8, Chapter 9, Chapter 10, and README.

## How to run / read / test it

**Read the book:** open `site/index.html` in any browser (or start at `docs/index.md`).
Fully offline once cloned; no network requests.

**Try the worked example yourself** (it makes no changes unless you say so):

```bash
python3 examples/walkthrough/safe_rename.py <some-folder>           # plan only
python3 examples/walkthrough/safe_rename.py <some-folder> --apply   # actually rename
```

**Rebuild the site** after editing chapters:

```bash
pip install -r requirements.txt
python3 build.py
```

**Run the tests:**

```bash
python3 -m unittest discover -s tests -v
```

## Verification results (all green, run 2026-10-27)

- ✅ `python3 build.py` builds cleanly: 11 chapter pages + landing + full-book edition + style.css
  (~17,297 words total).
- ✅ Test suite: **40/40 tests pass** (`Ran 40 tests ... OK`) — book structure (required chapters,
  ≥ 600 words/chapter, ≥ 10,000 total — actual ~17,300), tables/checklists presence, required
  topics, internal link resolution, markdown conversion (headings, tables, fenced code,
  checkbox styling for both `- [ ]` and `☐` styles, link rewriting, rel="noopener"), generated
  site validity (well-formed HTML, local stylesheet only, nav, labels, landing completeness,
  full-book completeness, no raw `.md` links), walkthrough↔example line-by-line consistency,
  example-script safety shape, secret-pattern sweep on docs/examples/build/README/site, exact
  LICENSE line, README credit.
- ✅ Example script behaviors verified by executable tests: plan-only leaves every file
  byte-identical; `--apply` renames exactly the 3 `IMG_*` files (decoy `.txt`, odd-named file,
  and subfolder untouched); second run says `Nothing to do...` (idempotent); missing folder and
  empty folder refuse loudly with exit code 2; a pre-existing target name stops the plan with
  `SKIP (already renamed, stopping)` and zero changes; `--help` works; files outside the
  given folder are never touched.
- ✅ Manual dry-run of the walkthrough example matches the transcript printed in Chapter 9
  verbatim (Plan: rename 3 file(s) … with the three IMG_ files; decoys skipped).
- ✅ HTTP smoke test: served `site/` locally; `index.html` (7,714 bytes), `full-book.html`
  (128,454 bytes), `01-what-code-actually-does.html` (12,925 bytes), and `style.css`
  (3,939 bytes) all returned HTTP 200.
- ✅ Rendered-page spot checks: styled checkbox lists on the checklist pages (19 items on the
  Ch 10 one-pager, 20 on Ch 8), 11 code blocks on the walkthrough page, zero raw markdown
  links in any HTML, landing lists all 11 chapters with blurbs and labels.
- ✅ No secrets/API keys/personal data: secret-pattern sweep passes; the only credential-ish
  string in the book is the *illustrative* placeholder shown in Chapter 7 to explain what to
  look out for (`"sk-REPLACE-ME"` as an example of one to delete) — the shipped example
  script contains none (test-enforced).

## Design decisions of note

- **Local-first and static:** the builder only reads/writes local files; the site has no
  JavaScript, web fonts, or trackers; no emoji in the book text; ASCII-plus-typographic-punctuation.
- **The example doubles as the teaching artifact:** `safe_rename.py` is a real, tested script
  whose every block is annotated in Chapter 9, and the chapter's example-session transcript was
  generated by actually running it (then verified again by the test suite on the day of writing —
  note the test fixtures are generated with *today's* date, so transcript dates may differ from
  a reader's).
- **Toast to the "trust me" theme:** Chapter 3's decoder table and Chapter 9's traps table give
  the same idea twice — by phrase and by code shape — because beginners meet both.
- **Checkbox rendering** handles both GitHub-style `- [ ]`/`- [x]` and the book's typographic
  `- ☐`/`- ☑` items, code-fence-aware, so lists render as real styled checkboxes and stay
  literal inside code blocks.
- **Companion positioning** is explicit: this book is deliberately the middle layer between the
  Terminal Comfort Guide (basics) and the OpenCode handbook (full agent workflow), and it points
  readers onward rather than repeating what those books cover.

## Known gaps / honest notes

- **No screenshots or illustrations yet** — everything is text and tables; diagrams of the
  copy-run-rollback loop would be a nice addition later.
- **Transcript dates** in Chapter 9's example output (e.g. `2026-10-27_IMG_…`) will not match
  the day a reader runs it; that's inherent to a date-prefixing example and now called out in
  STATUS (a reader-facing note may be added later).
- **Windows-specific subtleties** (drive letters, backslash paths, PowerShell quoting) are
  covered conceptually (Ch 7's `C:\` examples) but commands lean Unix/macOS; Windows-y exact
  commands for the same steps could be added as an appendix.
- **No search on the site** — deliberate (offline/reliability goals, no JS), same trade-off as
  the sibling manuals.
- **Glossary scope** — 28 terms sized for this book specifically; the wider AI-glossary
  pocketbook project covers AI terms more broadly.
- **Single test engine** (`unittest`, standard library only) — fine for scope; no external
  test framework.

## Git

Repository initialized locally and committed with a plain commit message (no co-author trailers).
No remote configured, nothing pushed, nothing published — per instructions.
