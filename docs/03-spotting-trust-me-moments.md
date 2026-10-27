# Chapter 3 — Spotting the "Trust Me" Moments

Somewhere in every AI-assisted project there comes a moment when the confident voice says something like:

> "This will work — I've handled the edge cases. Just run it."

That sentence is the **"trust me" moment.** Not because the AI is lying — it isn't, it's usually *sincere* — but because it can't know. It cannot see your folders. It cannot run anything, ever, anywhere. It has no memory of last week's broken attempt. Every claim it makes about code "working" is a prediction about a world it has never touched, delivered in the confident tone of someone who has.

This chapter teaches you to hear that tone. Not to distrust AI generally — it's a phenomenal, mostly-reliable assistant — but to react to confidence the way experienced computer people do: **confidence is interesting information; it is not evidence.**

## Why the AI sounds so sure

Generative models are trained to produce *likely-sounding text*. When you ask "will this work?", the statistically likely answer is an assured one, the same way autocomplete completes "Thanks so mu—" with "ch!" Look at what the AI is without anthropomorphizing it: a master of *the shape confidence takes in text*. It will produce shape-confidence even about things that fail immediately when run.

Three deep reasons AI claims are weaker than they sound:

| Reason | The plain-English version |
|---|---|
| It has never executed anything | It can't get a runtime error, watch a crash, or discover a typo. It uses languages it has only ever *read*. |
| It doesn't know your machine | Your folders, your filenames, your half-converted backups, your Windows quirks — absent from its world unless a previous message said so. |
| It predicts *plausible*, not *true* | "It works!" is plausible-sounding and gets generated even if the code contains an obvious bug. Plausibility is the currency; truth must be supplied by you. |

## Phrase-by-phrase decoder

Treat these as five-second reactions: notice the phrase, file the message under "needs a specific check." Phrases are ordered roughly by frequency.

| The AI says | What it can actually mean | What you respond |
|---|---|---|
| "Just run this." | "I wrote something." | "Not yet — walk me through what it touches, then I'll dry-run it." |
| "I've tested it / it works" | "I believe it works." (It cannot have any test evidence.) | "Show me exactly how to test it, step by step, and what output to expect." |
| "This is safe." | "This is safe *for a file layout I imagined*." | "What's the worst thing it does if a file is missing / named weird / already up to date?" |
| "I've handled the edge cases" | "I can list plausible edge cases." | "List the edge cases you handled, then the three you *didn't*." |
| "It's fine on my end" | Nothing. There is no end. | (Silently note it; move to Chapter 5.) |
| "Don't worry about that warning." | "The warning is one I see often." | "Explain the warning in plain words. I'll paste it if it shows for me." |
| "Should work now." (after a fix) | "I changed something." | "Great — what changed, and how do I re-test the same way?" |
| "You don't need to back anything up for this." | A guess about your pain tolerance | "I'm backing up regardless. Where should the snapshot live?" |
| "This minimal version is temporary, we'll harden it later" | Next week never comes | "Fine — but what does the temporary version refuse to touch?" |
| "Error X is harmless." | "Error X is common." | "Common *when*, on what setup? What should I do if mine persists?" |

Notice the pattern in the responses: **they all convert a feeling into a test.** The decoder's whole philosophy: never accept a claim about the future when you can turn it into a check about the present.

## Trust-me code patterns (the ones without words)

Some trust-me moments hide inside the *code itself*, no confident sentence needed. Memorizing these shapes is high-yield — they're the classic "worked perfectly in the demo, destroyed my Tuesday in practice" patterns.

| Code/command shape | Trust-me-ness | Why it deserves a second look |
|---|---|---|
| Deletes before creating (`rm`, `del`, `rmtree`, then regenerate) | High | If the regenerate fails halfway, you're left with *fewer* files than before. Correct version: build the new thing fully first, then swap. |
| Downloads-and-runs in one line (`curl` piped into `bash`/`sh`, or `.sh`/`.ps1` scripts fetched and executed) | The max | You skipped every safety layer this book has. Refuse, or download first, read briefly, run in a sandbox copy. |
| Overwrites existing files (`open(x, "w")`, `>` redirection, `WriteAllText`) without a "does it exist?" check | High | The old version of your file is being silently replaced forever. |
| `git push --force` / force flags anywhere | Very high | "Trust me" aimed not at files but at your *history*. Refuse unless you personally understand exactly why. |
| Long, clever "one-liners" accomplishing many things | Medium-high | Compact = hard to read = your reader's method can't see boundaries. Ask for the boring twelve-line version. |
| Code that pipes your **project contents** into the network (uploading before asking) | Very high | Chapter 7's domain; a trust-me moment with your secrets attached. |
| Anything with a comment saying `# TODO: add error handling` | Explicit | The boundary it will need (Chapter 2) is openly missing. |
| Scheduled/background execution (`cron`, `while True:`, "watcher", `--daemon`) | High | Runs when you're not watching. The inverse of the copy-run-rollback philosophy. |
| Changes many files in one pass ("batch," "bulk," "all files in") | High | Destructive scale. The right version has a `--limit 3` for a rehearsal (Ch 5). |

Two classics deserve their own paragraphs because they're so common.

**The delete-then-recreate pattern.** An AI writes `git` workflows, build scripts, and cache-cleanup scripts this way constantly: remove the old thing, then re-make it. In the AI's imagined world the second half always succeeds. On your Tuesday the second half fails — network hiccup, typo'd path, a file already open in another program — and now you have deleted your originals *and* have no replacements. The ask that fixes it: **"Rewrite so nothing is deleted until its replacement fully exists and is verified. Then delete the old one."** That request is so useful it has a folk name in our house: "no-gap version."

**The perfect-world input assumption.** The script reads *one* file. Not zero. Not two. Format exactly as imagined: field names spelled right, dates consistent, headers present. Then it meets your actual CSV where someone typed the date three different ways and one row is empty. The failure mode isn't just a crash — it's a *silent* drift: the script skips rows, or honestly processes 97 of 100 without telling you which. The ask that fixes it: **"Before doing real work, verify the input: right file, right columns, non-empty, and report how many rows you'll process — then compare with how many you did."**

## The AI repeated-my-own-mistake moment

A special trust-me worth naming. When you paste your own broken attempt (or the previous AI's answer) into a chat and the new answer confidently copies its assumptions — the wrong path, the wrong column name, the invented library — the new answer inherits those bugs with total confidence. Signs: the answer starts "Great code!" or "Your approach is basically right" — then keeps your bug intact. Fixes: include the *original goal*, not just the broken code ("I wanted X; this claims X; here's the full error"); and when correcting a previous failure, explicitly restate what reality was ("the folder is named `photos` not `Photos`").

## What a real "trust me" escape looks like

Watch the move happen — the moment where a beginner's instinct beats a confident tone. Scenario: you ask for a script that resizes images. The AI answers with beautiful code and says "This handles everything — just replace the folder path and run it."

Your instinct: *"everything" — the word "everything" is doing a lot of work there.*

The escape, in 45 seconds of typing:

- ☐ "What does 'everything' include, specifically? What are three things it does *not* handle?"
- ☐ "What folder does it write the new images to — same folder, new subfolder, or does it delete the originals?"
- ☐ "Is there a mode that processes exactly three images as a rehearsal so I can eyeball them before running the rest?"
- ☐ "If a file in the folder is corrupt or uninstall-sized, does it crash, skip, or stop the whole batch?"

That's not professional paranoia; that's four cheap questions that take less time than the confident answer took to generate. Chapter 4 turns this instinct into a full playbook. For now, keep the sentence: **listen for the confident verbs; answer them with specific, small, ever-so-slightly skeptical questions.**

## The honest baseline: most AI code is fine

It's easy to read this chapter as paranoia. It isn't. The majority of small scripts an AI writes for simple file tasks are *fine* — and the trust-me habits in this book are what let you say that with your own eyes instead of a leap of faith. You're not becoming a skeptic; you're becoming a **calm verifier** — somebody whose confidence comes from tests run, not vibes received. That disposition will serve you far beyond this book's subject.

Next up: turning that disposition into the exact questions to ask.

---
