# Chapter 5 — Testing Before You Rely on It

You've read the code (Chapter 2), heard the trust-me claims (Chapter 3), and gotten the risk list (Chapter 4). Now comes the step that actually earns your confidence: **running the thing — carefully.** This chapter is the linker between "code that exists" and "code I can rely on," and it's built around one sentence: **test in a classroom, not the kitchen.** You never want a first-ever run aimed at files you care about. Practice on the copies and the fakes; build confidence cheaply; *then* aim it at the real thing.

## The playground habit

Create a **playground folder** — a scratch copies-area for rehearsal runs — outside your real data. Name it something unmistakable, like `00-playground`. Inside it, build small fakes that imitate your real situation badly *on purpose*:

| Fake to include | Why |
|---|---|
| A copy of 3—5 real files (copies — copies, as Chapter 6 will hammer) | The closest thing to the real test, run on real data without risk. |
| One **empty file** | Catches the perfect-world assumption (Ch 3). |
| One file with a **long or odd name** (`IMG_2026-??-01 (final) (final)v2.jpg` — spaces, parentheses, symbols) | Filenames break more scripts than any other cause. |
| One file whose type the script **surely didn't expect** (a `.txt` in your photo folder) | Finds out whether it skips gracefully or crashes. |
| One **duplicate** (same content, two names, or the same name twice in different subfolders) | Catches overwrite and dedupe bugs. |

Five minutes of setup, used forever. Every script you ever get from an AI gets its first run here, before it ever meets `/photos`. Bonus: a playground is exactly where the walkthrough in Chapter 9 does its first run.

## The dry run

A **dry run** is a run that performs no changes: it shows what *would* happen. Every script in this book's universe should have one. Use the pre-mortem question from Chapter 4 ("can it run in a mode that changes nothing?") and be persistent: dry runs are easy for the AI to add and hideously valuable to have.

To retrieve facts from an unknown script: check for `--help` (Unix-y scripts often expose a help screen), or just skim the code for words like `dry`, `plan`, `--apply`, or a comment that says "default is dry-run." If a script has *no* dry run and you want one, the *make it default* trick works wonders: ask for "the safest mode to be the default, with a flag like `--apply` to allow real changes." Never add the reverse. Defaults are habits, and habits should be safe.

What a good dry run shows:

- The **list** of changes it would make (before → after)
- A **count** ("42 files") — so you can compare with your expectation ("should be 43 — why one less?")
- Any **skips** ("2 files left untouched because…")

Reading a dry run is a skill of its own, and it's Chapter 2's four questions again, but with reality supplying the answers this time: what will it take in, what will it change (now visible!), what does it touch, when does it stop. You should be able to answer "does this dry run look like what I asked for?" in one yes/no sentence. If the answer is close-but-not-quite, stop running things — that discrepancy you noticed is *exactly* what Chapter 4's risk list was asking you to find.

## Sample runs, small to large

When something has a dry run, add rehearsal sizes: deliberately run it on a tiny subset of *real* data before letting it loose on the whole. Ways to do it, cheapest first:

- ☐ Make a **mini real folder**: copy 3 real files into `00-playground/mini-real/`, run there.
- ☐ Use a **limit flag** if the script has one (`--limit 3`, `--max 5`) — a good AI adds these if asked.
- ☐ Run on the playground's deliberately weird fakes first: empty file, longer names, duplicates.

Reading order matters: fakes catch *crashes and logical errors*; mini-real catches *assumption errors* (filenames you didn't think about, content quirks). Run both. It's the difference between "the recipe has no impossible steps" and "the recipe is wrong for *my* kitchen's ingredients."

## What to actually watch

Non-programmers watching their first run tend to look at the end ("did it finish?") instead of the middle. Train yourself on these four:

| Watch | Healthy looks like | Unhealthy looks like |
|---|---|---|
| **Number processed** | Matches the count you had | 97 of 100, unexplained; or 1,037 when you have 42 |
| **First few changes** | You can *name* each one as right | "Wait, why is that file in the list?" |
| **End state** | Files you didn't expect to touch are… untouched | Mtime of your original files changed; things *lower* in the folder tree moved |
| **Skips and warnings** | Skips have reasons printed | Empty, or "Warning (suppressed) x214" |

The silent-nothing failure is the sneakiest: the script finishes instantly, prints nothing, and claims success. It did nothing wrong (nothing at all) — wrong folder, wrong extension match, permissions blocked. The ask that catches it early: **"End with 'Done: N things changed.'"** A healthy run ends with a number. Then check that number against your own count. (Also note the mirror-image failure: the loud crash that *feels worse* than the silent nothing but is *better* for you. A script that stops immediately with an error, having changed nothing yet, is behaving exactly right — that's what Chapter 4's "does it fail gracefully?" answer looks like in the wild.)

## The run-twice rule

If a script is one-run-and-done, add a second run to the audition before you adopt it. Then check whether it:

- Says "nothing to do" (idempotent and correct — the best case)
- Does the same thing again safely overwriting its own earlier output (fine for some tasks)
- Duplicates, corrupts, deletes, or mixes up files (broken — report back to the AI with the run-twice observation)

Why? Because in real life you *will* run things twice: out of habit, after an interruption, because "did I even click run?" haunted you. The run-twice check catches the whole accident class for the cost of one extra click on safe data. For the walkthrough in Chapter 9, it's built in; the example script is dry-run-first and refuses to overwrite existing (so it says "already done — nothing to do", which you would read as healthy).

## Health checks after adoption

Once a script becomes part of your routine — the "this runs every week" script — give it a health check: a tiny, repeatable test that takes 60 seconds and tells you it's still itself:

- ☐ Same count? (42 files in; 42 files counted.)
- ☐ Makes the expected *kind* of change on the playground copy first?
- ☐ Same rollback path proven? (Extra-good check when the script version *changed* since last run.)

Recording it in one line each time (`2026-10-27 — run on mini-real: 5 files, correct; dry again: "nothing to do" — healthy`) builds a personal log that's both evidence and history; you'll appreciate it the day an update turns the script wrong. Set it up with Chapter 4's closing-habits ask ("write me a short testing checklist").

## When to escalate the testing level

Some scripts deserve more than playground+fakes. Escalate when any of these are true:

| Trigger | Escalate to |
|---|---|
| It touches files outside its own folder (anything in `Documents`, `System`, your `backups`) | Snapshot your originals first — Chapter 6 — *before* even the dry run |
| It talks to the network at all | Check where exactly (Ch 4 Q5, Ch 7); consider airplane-mode testing for network-optional paths |
| It deletes anything, anywhere | `no-gap` version + rehearsal on 3 files only; count checks after |
| Other people depend on the output (family calendar, business books) | Add a buddy check: someone else skims the output before you rely on it |
| It runs unattended (on a schedule, a watcher, a server) | Run it scheduled-but-in-the-playground first — never first-run unattended on real data |

## The one-piece-at-a-time principle

If a script does several things at once and one of them is the risky part — say it "renames files and emails you a summary" — it's fine to ask the AI to split it: **"Give me version one: renames only. Version two: adds the email step."** Each piece gets its own audition; the risky piece never hides inside a bigger working thing. Programmers call this modularization; you can call it "one thing at a time, please" and you get the same benefit.

## Where this chapter ends and Chapter 6 begins

Everything here assumed you're playing with *copies* and *fakes*. The moment a script is aimed at files your heart cares about — your photos, your writing, your books — you need to know that even a bad run leaves the originals alive. That's Chapter 6: keeping originals safe. It's the chapter that makes everything in 1–5 *stress-free*, because once originals are guaranteed, mistakes become lessons and nothing is precious. On we go.

---
