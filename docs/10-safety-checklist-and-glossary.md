# Chapter 10 — Safety Checklist & Glossary

The wrap-up: one printable page of routine, one pocket dictionary. This chapter is designed to be used *forever* — bookmark it, print it, tape it near the monitor.

## The one-page safety checklist

This is Chapters 1–8 compressed to what you actually need at the keyboard. Photocopy-friendly on purpose.

> ### Before you run AI-written code (the whole book, one page)
>
> **Reading (about 5 minutes — Chapters 1–2)**
>
> - ☐ Does the purpose match the promise? (File name, top comments, function names)
> - ☐ Imports tell you its powers: files? network? other programs? (Danger words: `rmtree`, `rm -rf`, `"w"` overwrite, `subprocess`, `curl` piped into `sh`, `push --force`)
> - ☐ Loops over *everything*? Conditions guarding destructive lines? Can I name each `?` and unresolved line? (Those go on the ask list)
>
> **Questioning (3 minutes — Chapters 3–4)**
>
> - ☐ Any "trust me" phrases in the conversation? ("just run it", "I tested it", "it's safe") Decoded & converted into specific checks?
> - ☐ Pre-mortem asked: *what could this break, and what would I notice?*
> - ☐ Counts, undo path, network talks, and secrets covered. Simplest version?
>
> **COPY (2 minutes — Chapters 6–7)**
>
> - ☐ Snapshot the folders it might touch — *outside* the tree, named `YYYY-MM-DD-BEFORE-something`
> - ☐ Secret sweep: no key-shaped strings in code; nothing sensitive in its blast radius; secrets live in env/`.env`, never in code, never in chat
> - ☐ Path sweep: no bare `/`, `C:\`, or `~`; no sneaky `..`; no delete-wildcards; output goes somewhere *new*, not over
>
> **RUN (5 minutes, staged — Chapter 5)**
>
> - ☐ Dry run in a playground of copies — count, first few changes, untouched things, skips, all sane
> - ☐ Mini-real rehearsal (3–5 real files) — output *looks* right, name by name
> - ☐ Run twice: second run = "nothing to do" or demonstrably safe
> - ☐ Real run: expect it quiet. Counts match plan. Nothing touched that shouldn't have been.
>
> **ROLLBACK (2 minutes, drilled — Chapter 8)**
>
> - ☐ Undo path nameable from memory right now
> - ☐ Drill once a month (and after any script update): roll back a rehearsal run, verify identical, re-run
>
> **When surprised:** stop → describe the surprise in plain words to the AI → re-rehearse → re-run. Never "keep going regardless"; surprises are cheap caught at a dry run and expensive ignored.

### The 30-second version (memorize this)

> **Read for power, ask for specifics, copy first, run small, watch counts, know your way back.**

## The pocket glossary

Plain-English definitions, alphabetized. Cross-references point at the chapter that teaches it in context.

| Term | Meaning |
|---|---|
| **Absolute path** | A file's location written in full from the top (`C:\Users\you\…`, `/home/you/…`). Predictable, but breaks if moved to another machine. (Ch 7) |
| **API key / token** | A password-like string identifying you to a service. Treat like cash: never in code, chat, or screenshots. (Ch 7) |
| **Argument / flag** | Extra words after a command that change its behavior, like `--apply` or `--dry-run`. |
| **Blast radius** | Everything a script *could* touch if it misbehaved. Reading code = sizing the blast radius before running it. (Ch 2) |
| **Branch** | In Git, a parallel line of work you can try and throw away without affecting the main one. |
| **Code / program / script** | Text that is instructions for a computer. A *script* is a one-file, one-job program. (Ch 1) |
| **Command line / terminal** | The text window where you type commands directly to your computer. |
| **Condition (`if`)** | Code that acts only when something is true. The fence around dangerous actions. (Ch 2) |
| **Dry run / plan mode** | A run that shows what *would* happen without doing it. Chapter 5's cornerstone; also Chapter 8's RUN step 1. |
| **Env var (.env)** | A place to store secrets *outside* your code — the safe house for API keys. (Ch 7) |
| **Function** | A named mini-recipe inside a script, callable by name. Reading function names = skimming the table of contents. (Ch 1) |
| **Git** | Industry-standard version control: perfect memory + undo for a folder of files. (Ch 6; full walkthrough in *Free AI Coding with OpenCode*, Ch 6) |
| **Idempotent** | Safe to run twice — the second run does nothing new. Chapter 5's run-twice test checks for it. |
| **Import** | A line borrowing someone else's code. Reading imports = a script's power inventory. (Ch 2) |
| **Loop (`for`/`while`)** | Code that repeats — once per item or until told to stop. Where effects multiply. (Ch 2) |
| **No-gap version** | A design where nothing is deleted until its replacement fully exists. (Ch 3) |
| **Path** | Where something lives on disk, written down. Absolute (pinned) vs relative (relative to where you run it). (Ch 7) |
| **PHI** | Protected Health Information — patient data. Nurses and other health workers: PHI is never a chat input, ever. (Ch 7) |
| **Playground** | A scratch folder of copies and fakes where first runs happen. (Ch 5) |
| **Pre-mortem** | Asking "what could this break?" *before* writing/running — imagining the failure first. (Ch 4) |
| **Relative path** | A location written relative to *where you are now* (`photos`, `../data`). Flexible, but means different things from different places. (Ch 7) |
| **Resolve (a path)** | Turn a possibly-relative path into a definite one. Common first defense in careful scripts. (Ch 9) |
| **Rollback** | Going back to the pre-run state via snapshot, Git, or a reverse step. Rehearsed, not hoped for. (Ch 6, 8) |
| **Secret** | Anything that lets someone be/unlock you: keys, tokens, passwords, cookies, PHI, money-access strings. (Ch 7) |
| **Silent wrongness** | A failure with no crash — the worst kind. Count checks and plan-output defeat it. (Ch 5) |
| **Snapshot** | A full copy of a folder (or Git commit) taken before doing something risky, named so future-you understands it. (Ch 6) |
| **Terminal** | See command line. |
| **Trust-me moment** | When confidence is offered instead of evidence — in AI words ("just run it") or AI code (delete-then-create with no guard). (Ch 3, 4) |
| **Variable** | A labeled box holding one piece of information inside a program. (Ch 1) |

## Thirty days of practice (a tiny curriculum)

If you want to *own* this skill, here's an honest, low-effort month of practice — one small script per week, real ones you might actually want:

- ☐ **Week 1:** a single-file task (like the renamer, or a "list my files by size" script). Walk the full routine twice. The goal: the sequence feels mechanical, not scary.
- ☐ **Week 2:** a script that *creates* files (organizer, report generator). Add output-to-a-new-folder to your default asks. Rollback drill included.
- ☐ **Week 3:** a script that *reads* something with columns (CSV of your books, your mileage). Meet silent wrongness deliberately: give it a bad column name on purpose, watch it either catch or miss, then fix it with a Chapter 4 question.
- ☐ **Week 4:** a script that touches the network (a "check my public IP" or "fetch page title" tool, on data that's yours). Secrets and paths get full checks; offline testing included.

By week's end, the loop is yours. You'll have handled every category this book covers — renames, creation, structured data, network — and the routine will have shown you both its boring successes and its genuinely useful saves.

## The last word

Non-coders in the AI age have a real, unfair problem: everyone can *get* code now, and almost nobody was taught to *use* it safely. This book's answer fits in one breath — **read for power, ask for specifics, copy first, run small, watch counts, know your way back** — and stretches over the rest of your life as a habit. AI will keep handing you code. You'll keep being the one at the keyboard. Take the ten minutes; be the one in charge.

If you want to go deeper anywhere, the two companion manuals wait: *Free AI Coding with OpenCode* for the full prompting-and-reviewing workflow (and Git), and *Terminal Comfort Guide* for the black-window basics. Happy reading — and even happier rolling back.

---
