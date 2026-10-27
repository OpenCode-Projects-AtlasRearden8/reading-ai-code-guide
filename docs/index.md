# Welcome — Read Me First

## Who this book is for

This book is for anyone who is getting code written *for* them — by ChatGPT, Claude, Gemini, OpenCode, a friend, or your nephew — but who cannot (and does not want to) become a programmer just to use it safely.

Maybe you asked an AI for a little script that renames your photos, tidies your bookkeeping CSV, or scrapes your own sales page. It gave you a block of code, said "just run this," and you felt that familiar flutter: *I am about to run something I genuinely do not understand, written by someone/something that has never seen my computer.* That flutter is correct. It is also completely normal. This book exists because that moment — running code you can read but not write — deserves a real, honest method, not a shrug.

You do not need any programming background. You do not need to memorize anything. The whole book fits around one habit we will build together: **read a little, test a little, keep a way back.** Everything else is detail supporting that habit, including the lessons where we fail — because running unfamiliar code *will* occasionally do something surprising, and a calm recovery is a much better skill than pretending it never happens.

## What you will learn

By the end of this book you will be able to:

1. **Understand what code even does** — plainly: programs are recipes that fetch, change, and create files, talk to the internet, and run other programs. It's all recipes.
2. **Read AI-written code the reader's way** — not like a programmer, but like an informed editor: names, comments, imports, and the handful of danger words that tell you where the risky parts live.
3. **Spot the "trust me" moments** — the confident phrases and confident-looking code that deserve extra checking, because the AI never actually ran anything.
4. **Ask what could break** — the question playbook that turns "it works" into "here's specifically what can go wrong, and here's how you'd notice."
5. **Test before you rely on it** — playground folders, dry runs, sample data, and the run-it-twice check: cheap tests that catch the mistakes that matter most.
6. **Keep originals safe** — snapshots, copies-with-names, and the golden rule that your original data should always survive even a catastrophically bad code run.
7. **Check secrets and paths** — the two places AI code most often does real damage: touching files it shouldn't touch anywhere, and handling credentials it should never see.
8. **Use the copy-run-rollback routine** — the core loop of this entire book, so that *undo* is always one step away, not a hope and a prayer.
9. **Follow a real annotated walkthrough** — a complete, working, deliberately-self-defending example script, explained block by block in non-coder language.
10. **Use the safety checklist and glossary** — a one-page routine and a plain-English word list you can come back to forever.

## How to read this book

Two good ways:

- **Start to finish.** If code still feels like a foreign language where you can't even tell a question from a statement, go in order. The chapters build: what code is, then how to read it, then how to distrust it healthily, then how to test it, then the routine.
- **As a reference.** If you are mid-project with an AI-written script staring at you right now: go to Chapter 8 (the copy-run-rollback routine), then the walkthrough in Chapter 9, then the checklist in Chapter 10. The middle chapters will still be waiting for you.

## Companion books

This manual sits in a small family of beginner guides by [Asdale Dynamics, LLC](https://dylanasdale.github.io):

- **Free AI Coding with OpenCode** — if you haven't yet *got* AI-written code, or want the full workflow of prompting and reviewing AI changes, plus Git as your undo button. This book's Chapter 6 assumes you may want that deeper Git runway.
- **Terminal Comfort Guide** — if the black text window still feels like a power tool with no guard. That book is the handholding intro; this book assumes you can open one and paste a command.

You don't need either book to use this one. But this book is deliberately the *middle* layer: past "how do I even run something," short of "I can program now."

## Conventions used in this book

| What you see | What it means |
|---|---|
| `command --like-this` | Something you type in a terminal. Type everything *after* the `$` in examples; never type the `$` itself. |
| **Bold** | Something to pay attention to, click, or press. |
| *Italic* | A term being introduced, or gentle emphasis. |
| ☐ A checklist | Something to actually do, not just admire. |
| Block | A section of code we're examining — a "block" is one named chunk: a few lines that belong together, like a paragraph. |

Words you'll need early, kept deliberately simple — the full glossary waits in Chapter 10:

- **Code / a program / a script**: text that is also instructions. A *script* is a small code file, usually one file, doing one job. This book is mostly about scripts.
- **Run / execute**: the computer has read the instructions and *does* them. Only at run time does anything actually happen to your files.
- **Terminal**: the text window where you type commands directly to your computer.
- **Snippet**: a few lines of code out of context — often what an AI hands you in chat.

## Map of the book

| Chapter | Title | What it covers |
|---|---|---|
| 1 | What Code Actually Does | The recipe analogy; a real tiny script, dissected; the four questions |
| 2 | Reading Code You Cannot Write | The reader's method: names, comments, imports, danger words |
| 3 | Spotting the "Trust Me" Moments | Confident phrases and confident code that deserve checking |
| 4 | Asking What Could Break | The pre-mortem question playbook for talking to your AI |
| 5 | Testing Before You Rely on It | Playgrounds, dry runs, sample data, the run-twice test |
| 6 | Keeping Originals Safe | Snapshots, copies with names, and the data-survival golden rule |
| 7 | Secrets and Paths to Check | Where AI code leaks credentials and goes where it shouldn't |
| 8 | The Copy-Run-Rollback Routine | The core loop, in full, for every script you'll ever get from an AI |
| 9 | An Annotated Walkthrough | A real safe-renamer script, block by block, with the routine applied |
| 10 | Safety Checklist & Glossary | The printed-one-pager and the word list |

## The one rule of this book

If you remember nothing else, remember this:

> **Never let the first time you run something be the time you actually need it.**

An AI can write a script in seconds, but it has *never run anything in its life*. It has no computer, no files, no bad luck. So it writes code optimistically — code that works in the world it imagines. You live in the world you actually have: folders with odd names, files that are half-empty, a network that drops, and Tuesday evening when you're out of patience. The routine in this book — copy, run dry, run small, run for real — exists to translate *imagined* success into *verified* success safely, every single time, in about ten minutes.

That's it. That's the whole philosophy. The rest is how.

## About the fine print

Tool menus, model behavior, and exact phrases change constantly. This book describes things as of late 2026. The *techniques* — reading for danger words, dry runs, snapshots, rollback drills — are as durable as recipes, and they work on every AI you might be using, free or paid, cloud or local. Where I name a concrete tool or menu, treat it as "an example, check yours."

Ready? Turn the page.

---
