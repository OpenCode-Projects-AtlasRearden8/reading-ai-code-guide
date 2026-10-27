# Chapter 6 — Keeping Originals Safe

Everything in Chapters 1–5 only works if one thing is guaranteed underneath: **when a run goes wrong, the originals survive.** This chapter is about making that guarantee boring, cheap, and repeatable. It's written for people whose data includes irreplaceables — years of photos, a manuscript only they wrote, their business's records — and who have deleted something once in their life and never want to feel that again.

## The golden rule

> **The originals always have a copy that no run, no script, no AI, and no cleaning rampage can touch — at least until the thing you're doing has been trusted.**

Notice what this rule does *not* say. It does not say "back up everything constantly in six places" (burnout) or "never touch your files again" (not possible). It says: for the specific, narrow window in which you are giving an AI-written script its audition, your originals belong to a *different universe of files* — one the script could not reach if it took a wrong turn. The window closes when the script is trusted (Chapters 5's criteria) and you resume normal life.

## The two-snapshot move

For any project that involves running unfamiliar code near things you care about, spend five minutes on two snapshots:

1. **The folder snapshot.** A copy of *the folder(s) the script might touch*, zipped or plain-copied, with the date in the name:
   ```bash
   cp -r myproject myproject-BEFORE-autorename-2026-10-27
   ```
   Vanilla-copy first; fancy tools optional. And do it *before* running anything, always.
2. **The everything-might-really-matter snapshot.** For anything you'd be devastated to lose — books, photos, business records — one copy on a *different device or drive* (a second disk, a USB stick, a family computer). Two devices, not two folders. That's the "3-2-1-lite": 1 = working copy, 2 = a copy somewhere else, and ideally, 3 = history (more versions than just latest).

And for anything you'd be *professionally* devastated to lose, go further. But no amount of online-only redundancy makes up for skipping the local rehearsal run — Chapter 5's playground — because backup protects against loss, and a rehearsed dry run protects against *breakage*, which is what an AI-written script most likely does.

Three rules for naming snapshots, because respect for future-you is the actual mechanism:

| Rule | Reason |
|---|---|
| Date-first, purpose-second (`2026-10-27-BEFORE-autorename`) | Sorts historically, tells you what it's *protecting against*. |
| Say `BEFORE-` not `backup-` | "Backup" is vague; `BEFORE` literally states what it lets you *return to*. |
| Never snapshot into the same folder being processed | A `cp` inside the same tree gets swept up by the very deleting/cleaning script you fear. Snapshot to *outside* the tree. |

That third rule avoids a real scenario worth naming: **the snapshot that eats itself.** Copy `/photos` to `/photos/BACKUP-FROM-2026-10-27` and then run a folder-wide rename, and the rename will *also rename the snapshot's files*, or worse, the cleaner will treat the extras as clutter. Outside-the-tree copies only.

## Versioning as superpower (a friendly intro)

Snapshots are the beginner's superpower; **version control** is the superpower's superpower — one tool, `git`, that snapshots *everything, constantly, automatically, with an undo.* If this sounds like it's for programmers: yes, but it's also for you, and it pairs with this book's mission better than almost anything else in computing. Two options worth knowing about:

- **Word-level history** (Word, Google Docs, Notion, etc. all keep edit history). If your project lives in *documents*, you already have a partial safety net. Use it — it's free.
- **Git** (the real thing). If you'll keep working with AI on projects of files, spend one evening learning `git init`, `git add -A`, `git commit -m "before trying the AI script"`, `git restore .` from the *Free AI Coding with OpenCode* handbook, Chapter 6. That sequence is "save a restoration point; return to it," and it works at *every* level: project code, prompts, drafts.

To net it out at beginner scale: **a fresh snapshot before every first run; a git restore-point if the project is code-heavy.** You don't need to be a Version Control Person to be safe; you need to be a Person Who Takes Two Snapshots. And since the philosophy of this book is cheap habits over perfect systems, one habit — **"snapshot before first run"** — is honestly enough to cover 90% of the ways an AI script can go wrong.

## What "keeping originals" means for *inputs* vs. *code*

Keep these two kinds of precious separate — they don't survive the same way:

| Kind | Examples | What to protect | Why different |
|---|---|---|---|
| **Your data (inputs)** | photos, manuscripts, spreadsheets, photos again, *photos* | Snapshots + out-of-tree copy; playground rehearsals; dry runs | Irreplaceable; and the *first* thing scripts run over |
| **The script (code)** | `safe_rename.py`, the AI's many versions | Version history + the chat log itself | Re-generatable. Worst case you re-ask the AI. |

A consequence worth making explicit: **when a run looks wrong, the script is the expendable thing.** Delete it without ceremony — you can re-ask. The data is the thing you saved snapshots for. Beginners sometimes protect code feelings — "I spent 20 prompts getting this perfect" — and forget the data. Scripts are disposable; data is forever. (The flip side is a warm note: keeping the *prompt that worked* is far more valuable than keeping the script — the prompt is short, readable by humans, and can re-create the script on any AI. Worth telling yourself that when you archive code you might discard.)

## The verified-restore habit

A snapshot is only a safety net if you know how to fall into it. Once — once is enough, ever — do a **restore rehearsal**:

- ☐ Snapshot a folder.
- ☐ Delete (or modify) some files in the *working copy* on purpose.
- ☐ Restore the contents from the snapshot — `cp -r snapshot-things/. working-folder/` — or open the zip and copy back.
- ☐ Confirm everything came back, then close the laptop, satisfied.

Ten minutes. The day you actually need it, it goes well, because you've done it when nothing was at stake. This is the same trick fire drills use, adapted for files. (If your backups live on another device or drive, restore from *that* during the drill, so you've proven the *whole* path, not just the copy-getting step.)

## Anti-patterns: how beginners accidentally skip protection

| Anti-pattern | What happens | Fix |
|---|---|---|
| Working directly on originals "because it's just a rename" | Renames can collide, truncate, or mis-target; rename is still *changing* them | Playground first; originals only after auditions pass |
| Snapshot inside the folder being processed | Snapshot gets mutated by the script | Snapshot *outside* the tree |
| "It'll be fine, it's a dry run" | …for the run you did. But the third argument you passed changed the run's *mode* | Snapshot before *every* first run of a new version |
| Snapshot stack-of-doom (14 `BEFORE-` copies, all outdated) | None current; restoration becomes archaeology | Keep the two most relevant; archive the rest into one dated zip |
| Only backup = same drive, different folder | Drive dies, both die | Second device or drive for anything devastating-to-lose |
| The AI offers to "clean up" your working folder as part of a bigger task | Unrelated files get deleted — the silent wrongness pattern | The phrase that always works: "Do not delete **anything**. Leave every file you didn't create. I will clean up." |

That last one deserves underlining. It is possibly the single most useful sentence in this book to say to an AI when you mean it:

> **"Do not delete anything. Do not move anything you didn't create. Tell me what you would delete, and I'll decide."**

## Where this leaves the overall picture

By the end of Chapter 6, the safety stack looks like this: read a little (Ch 2), distrust the confident (Ch 3), ask what breaks (Ch 4) — then *snapshot*, *rehearse in the playground*, *watch the counts*, *run twice*. Two chapters remain on the safety core: where scripts usually go wrong specifically (Ch 7: secrets and paths), and the routine that ties it all together in ten minutes (Ch 8: copy-run-rollback). The finish line is close, and you're doing fine.

---
