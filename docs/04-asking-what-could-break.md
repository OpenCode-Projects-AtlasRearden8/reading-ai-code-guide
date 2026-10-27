# Chapter 4 — Asking What Could Break

Chapter 3 trained your ear for over-confidence. This chapter gives you the *questions* — a playbook of asks that, used before running anything, will catch most of what can go wrong. It's structured as a conversation you can have with your AI in a few minutes. The questions are also useful, with light adaptation, for a friend or nephew who wrote you a script: the goal is precise communication about risk, not interrogation.

Two framing ideas before the list.

**First: breakage is a *planning* question, not a *code* question.** Asking an AI mid-task "will this break?" tends to produce reassurance ("I've handled that"). Asking *before* it writes ("before you write it — what could this break?") produces genuinely useful analysis, because the answer shapes the plan rather than defending a finished product. Ask early. Ask as design, not audit.

**Second: you are not Looking for no; you're looking for specifics.** An answer like "we should handle missing files" is a *specific* — it names a failure and implies a guard. An answer like "it's robust" is a *vibe* — note it and re-ask. The quality bar for this chapter's questions is: **nameable failure, nameable guard.**

## The opening move: the pre-mortem

Before the AI writes anything, ask the question this chapter is named for:

> "Before you write it — what could this break? Walk me through the ways this could go wrong on my machine, in plain English. Then decide what to do about each."

This is called a **pre-mortem**: imagine the project already failed, then ask why. People love the phrase because it works: it converts vague anxiety into a list. Expect the first answer to be short (AIs front-load one or two risks). Then pull the thread with, one at a time:

- "Which of those risks is the *most* expensive to fix after it happens?"
- "What's a risk you didn't list because you assumed I'd never hit it?"
- "For each, what would I *notice* on my end if it happened — a crash, a weird filename, or silent wrongness?" (Silent wrongness is the expensive category. It's what Chapter 5 is really about.)

You'll usually get a shortlist of 3–5 real risks. **You are not expected to fix them.** You carry them into Chapter 5 as the checklist of "things I'll watch in the test run." That's the whole loop: *ask early, turn risks into things-to-notice.*

## The core question set

These eight questions cover most scripts, most failure modes, and take maybe three minutes of typing. They're ordered not by importance but by conversation flow — like a small interview.

| # | Ask this | What you're really asking |
|---|---|---|
| 1 | "What files and folders will this **read**, and what will it **change**? List them, including any subfolders." | Scope. If the list surprises you, the plan is wrong before code exists. |
| 2 | "Can it run in a **mode that changes nothing** — a dry run or plan-only mode?" | The rehearsal option. If "no," ask for it now (Ch 5's cornerstone). |
| 3 | "If I run it **twice in a row**, does it do something wrong the second time — copy twice, duplicate, corrupt?" | Whether it's repeatable. Accidental double-runs are the most common how-did-this-break story in real life. |
| 4 | "What happens if the **network is down** halfway through?" | Whether the failure is graceful (stop, tell you, leave things as they were) or messy (half-changed everything). |
| 5 | "What happens if an **input file is empty, missing, or misnamed**?" | The perfect-world-assumption check from Chapter 3. |
| 6 | "How do I **undo** this? Exactly what does rollback look like?" | The escape hatch. If the honest answer is "you can't," the design changes before code is written. |
| 7 | "Does it need any **secrets** — keys, tokens, passwords — and if so, where do I put them?" | Chapter 7's territory, asked up front instead of discovered in the code. |
| 8 | "What's the **simplest version** that still does the job — no extra features?" | Scope discipline. Every extra feature is extra read-time, extra test-time, extra risk. |

Question 6 deserves a moment of resonance: *undo as a design requirement, not an afterthought.* A script whose rollback story is "restore from your backup" is fine *if* you have a backup — that's Chapter 6's job. But many scripts can have better undo for free: writing outputs to a new folder instead of in place, a `--dry-run` default, a rename batch written to a log first. Asking "how do I undo it" *first* is the single highest-value question in this list, because it moves undo from hope into design.

## Question drills for specific moments

Beyond the core set, here are pointed asks for situations you'll recognize.

**When the AI proposes something you didn't ask for:**

> "I asked for X. What did you add beyond X, and why? Can I have the version with only X?"

Almost every AI answer includes unsolicited cleverness — retries, parallelism, caching, logging frameworks. Some are genuinely helpful; some are read-time you don't want. Choose consciously.

**When you're about to run something for the first time on real data:**

> "You've never seen my actual folder. What are the three things most likely to be different from what you assumed? What should I check *before* running?"

This question produces gold surprisingly often — the AI knows exactly what it assumed, and listing its assumptions briefly forces those assumptions into the open where you can compare them to reality.

**When something works and you're about to rely on it:**

> "Before I rely on this weekly, stress it: what input, timing, or environment would break it? Is there a small test I can run each time to confirm it's healthy?"

This is how Chapter 5's "health checks" are born — the five-second test you rerun forever after.

**When a fix fails twice:**

> "We've tried twice and it keeps failing. Stop patching. Re-look at the *problem*: what's the likely real cause, and what's the simplest script that avoids it entirely?"

Two failed patches usually mean the *design* is fighting reality, not the code. Ask for a rethink, not fix number three.

**When code does something you can't explain (the Chapter 2 "?"):**

> "Line 14 — explain like I've never programmed, in one paragraph: what does it do, why is it here, what's the worst realistic thing it could do, and is there a safer version?"

## Getting the AI to write the checklist *for* you

A trick worth its own section because it doubles your leverage. After the AI finishes a task, instead of you inventing tests, ask:

> "Write me a short testing checklist for what you just built: what a healthy run looks like, three edge cases to try on purpose, and one 'rollback drill' to prove I can undo it. Keep it to one page, plain English."

You get four things free: the healthy-run definition — protecting against the silent-nothing failure — deliberate edge cases instead of accidental ones, an undo practice, and a *re-readable document* for next time (file it next to your script; Chapter 6's snapshot habit pairs beautifully with it).

Use the same trick on the *risks* side, at the very start:

> "Before writing code: list the top 3 ways this could break, each with the plain-English symptom I'd notice, and one guard you'll build in."

That's the pre-mortem with built-in alarms. Keep both lists; they'll be your Chapter 5 test plan almost word for word.

## When it's not an AI — applying the playbook to people

Half of this playbook transfers, word for word, to asking a human friend or colleague about their code. What changes is *tone*: with a person, soften ("walk me through" → "can you remind me," "what could this break" → "what are you worried about?"). The conversational moves — ask early, ask for specifics, ask about undo, ask for the simplest version — work identically on people; often better. A good rule from years of tutoring humans: **a beginner's sincere question is never a burden. If someone acts like it is, find a different mentor.**

## A worked mini-conversation

From a real session, compressed. You asked for a script that backs up your writing folder to a `backups` subfolder, once a day, keeping the last 7 copies.

- ☐ *Pre-mortem first:* "Before you write it — what could this break, in plain English, and what will you do about each?"
  → The AI lists: wrong folder path; disk filling up; backup *deleting* existing backups incorrectly; silently backing up zero files. Guards: verify source exists, check free space, name backups with today's date, log the count of files backed up.
  → Notice item three: "deleting existing backups." A backup routine that touches *old* backups is exactly the delete-before-create trap from Chapter 3. Your questions found it before a single line was written.
- ☐ "Run-twice check?" → Confirms two same-day runs are safe (same filename, overwrite same-day copy only).
- ☐ "Undo?" → "Delete today's backup file; originals are never touched." Good boundary story.
- ☐ "Secrets?" → None needed. (Checked anyway, Chapter 7 habits.)
- ☐ "Simplest version?" → Drops parallel copying, adds logging; file copied count remains.
- ☐ Testing plan requested → "Back up a scratch folder of 5 fake files; then back up again same day and confirm one file, not two; then disconnect the source folder and confirm it *refuses loudly* rather than backing up nothing."

Ten minutes, and every risk in the room has been named, guarded, and has an alarm you'll actually see. That's the difference between hoping code works and being the person in charge of it.

## The one-sentence version

If you take one reflex away: **before code exists, ask what could break and how you'd notice; after code exists, ask what to rehearse and how to undo.** Everything else in this book is the discipline of doing that on purpose.

---
