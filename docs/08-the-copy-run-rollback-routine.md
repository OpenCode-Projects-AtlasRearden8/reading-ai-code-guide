# Chapter 8 — The Copy-Run-Rollback Routine

Everything so far — reading, distrusting, questioning, testing, snapshots, secret-and-path scans — now folds into one repeatable loop you'll run on every piece of AI code you take seriously. It's called **copy-run-rollback**, and once it's a habit it will take you about ten minutes, start to finish (fifteen the first few times — that's honest and normal). It's the routine this whole book exists to teach, and by far the most important muscle here.

## The name

Three moves:

- **COPY** — make the situation copy-safe before anything runs.
- **RUN** — execute, starting from the least destructive mode, escalating only as evidence accumulates.
- **ROLLBACK** — proven, one-step undo, rehearsed *before* you need it.

That's the loop. When something new and untrusted enters your world (an AI script, a new version of a trusted script, first run against a new set of files), you run the loop. When you've nothing new, the loop is short — a quick dry run in the playground a second time, then carry on. The loop is what lets you use AI code as *material* rather than *mystery*, which is the actual goal of this book.

## Phase 1: COPY (2 minutes)

Do these in order. They're cheap, and each one removes a whole class of bad outcomes:

- ☐ **Snapshot the folder(s) the script might touch** — *outside* the tree, date-first names (Chapter 6). Two minutes; this is the whole safety net.
- ☐ **Check the secrets sweep** (Chapter 7's checklist) — no keys in code, no secrets in the blast radius.
- ☐ **Check the paths sweep** — no bare roots, no `..` inheritance, no delete-wildcards you didn't discuss.
- ☐ **Read the script's structure** lightly (Chapter 2's three passes — you'll be fast at this now).
- ☐ **Skim the risk list** from Chapter 4's pre-mortem, and refresh memory: *what am I watching for?*

One crucial nuance for Phase 1: the source of truth here is the *latest* code. If the AI wrote version 3 while you were sleeping — this happens more than beginners expect, silently editing files — glance at what changed (`git diff`, or a fresh eyeball pass) before skipping anything. **The trust-me moment restarts with each new version.** There's no "it worked last time" for code you didn't write.

## Phase 2: RUN (5 minutes, staged)

Step 1: **Dry run first.** playground folder (real copies), `--dry-run` or plan mode on, and watch the output (Chapter 5's four things to watch: counts, first few changes, untouched things, skips).

Step 2: **Rehearsal run on a small slice of real data.** --limit-3, or a `mini-real` playground folder. This is the step that catches "wrong assumptions about *my* files," and it's worth five minutes.

Step 3: **Run-twice check on the rehearsal set.** Idempotence — Chapter 5's rule — means the second run says "nothing to do." The second run's honesty is one of the best single signals you'll ever get about a script's character.

Step 4: **The real run.** Against actual files — this should *feel anticlimactic*: dry run, rehearsal, and run-twice already happened. That's success; not the drama of a first attempt, but the boredom of a prepared one.

Each step escalates only if the previous one was boring. A surprise anywhere — a count off by one, a file in the plan you didn't expect — *stops the routine* and sends you back to Chapters 3–4: name the surprise in plain words, ask the AI about it, re-rehearse. Surprises are cheap when caught at a dry run; and exactly as expensive as the stage where you didn't listen.

## Phase 3: ROLLBACK (2 minutes — or nothing, if you already did it)

The rollback isn't an emergency measure; it's a *first-class phase* of the routine with two requirements:

1. **It exists.** You can name the exact way you'd undo: restore snapshot; `git restore .`; delete the outputs folder and re-copy originals; re-run a reverse script if one exists (a "no-gap" design, Chapter 3).
2. **You've *used* it once, on purpose.** During Phase 2's rehearsal, sometimes do the undo drill: after rehearsing real-but-throwaway changes, roll back, verify everything's identical, and then re-run. Every 10th run, drill again; and once a month at minimum. It costs two minutes and guarantees your undo knowledge doesn't rust.

Rollback drills also build a different, quieter thing: **calm.** Non-coders' panic around code comes almost entirely from feeling trapped — "I broke something and I don't know how to unbreak it." The drill teaches your body the way a fire drill does: this is not a cliff, this is a stairway; you have walked it.

## The checklist, printable

Here's the whole routine as a one-page checklist. Print it, tape it, use it forever — or fold it in half and keep it next to your keyboard.

> **COPY (2 min)**
>
> - ☐ Snapshot the folders the script will touch — *outside* the tree, `YYYY-MM-DD-BEFORE-thing`
> - ☐ Secrets sweep clean (no keys in code; nothing sensitive in its blast radius)
> - ☐ Paths sweep clean (no bare `/` or `C:\`; no unexpected `..`; no delete-wildcards)
> - ☐ Three light reading passes done; risk list refreshed
>
> **RUN (5 min, staged)**
>
> - ☐ Dry run on playground copies — watch counts, first few changes, untouched things, skips
> - ☐ Mini-real rehearsal (3–5 real files) — does the output *look* right, name by name?
> - ☐ Run twice — second run is either "nothing to do" or demonstrably safe
> - ☐ Now, and only now: real run. Watch the same four things. Expect a *quiet* run.
>
> **ROLLBACK (2 min)**
>
> - ☐ Can I name the undo path right now, from memory? (If no: make one before continuing.)
> - ☐ Drill it on the rehearsal set, roughly every 10th run: roll back, verify identical, re-run.
> - ☐ If surprised at any stage: stop, describe the surprise in plain words to the AI, re-run from Phase 1.

Laminate it if you must (figuratively); it's the whole book in fifteen lines.

## Ten-minute budget, realistically

Let's time it honestly — the routine has to fit in an evening to survive:

| Stage | Time |
|---|---|
| Reading passes (Ch 2) | 5—8 min (fast after a few scripts; beginners take 15) |
| Pre-mortem questions (Ch 4) | 3–5 min |
| COPY phase | 2–3 min |
| RUN phases (dry, mini-real, run-twice, real) | 5–8 min |
| ROLLBACK noted/drilled | 0–2 min |
| **Total** | **~15 minutes first times; ~10 once it's a habit** |

Fifteen minutes is the honest first-time number; don't let anyone tell you less. The habit is real once it's under ten and doesn't feel like effort. It does get there — the walkthrough in Chapter 9 comes in at roughly nine.

## When the routine encounters the AI's own workflow

If you're using an agent like OpenCode directly in your project (the *Free AI Coding with OpenCode* route), the routine adapts cleanly:

- Phase 1's snapshot becomes `git commit` before the task (plus the branch habit that book teaches).
- Phase 2's dry run is often OpenCode's **plan mode** — a plan you read *before* it writes anything, which is a dry run for *plans*.
- Phase 3's rollback is `git restore` and/or `/undo`.

The *sequence* stays identical, though: see it before it happens, rehearse before it's real, undo is a proven step and not a wish. That's the deeply transferable idea: **the routine is tool-agnostic — it's a philosophy of staged evidence, and it works in every environment you'll ever meet, including ones that don't exist yet.**

## What "trusted" means at the end

The routine exits when a script has passed enough auditions that you use it without the ceremony. What enough means is your call, and here are honest criteria:

- ☐ Three real runs, no surprises, counts verified each time
- ☐ The run-twice check is trusted (second run always says "nothing to do")
- ☐ The rollback has been drilled recently enough that you could do it half-asleep
- ☐ Its failure modes are known to you — you've *seen* it fail (on purpose: fed it an empty file, a missing folder) and it failed gracefully

Green on all four = everyday tool; checklists optional but recommended weekly. Two greens = audition tool; full routine every time. Anything less — including code you can't read at all (Chapter 2's "?" list unresolved) — stays a full-routine tool, permanent. There's no shame in a script living at full routine forever: plenty of real code works this way, in every serious shop, all the time.

Boring, repeatable, calm. That's the whole routine. Now let's *watch* it happen, block by block, on a real script.

---
