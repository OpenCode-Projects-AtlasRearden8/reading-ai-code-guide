# Chapter 9 — An Annotated Walkthrough

Time to watch the whole method happen, start to finish, on a real script. The example in this chapter ships with this book as a *runnable* file — `examples/walkthrough/safe_rename.py` — so you can read the annotations here and then run the actual thing yourself, exactly the way the routine teaches. Nothing in it is theoretical.

## The mission

A common real-life ask. You have a folder of camera exports named like `IMG_4021.jpg`, and you want them renamed to `2026-10-27_IMG_4021.jpg` (date-prefixed). You don't trust your memory of which is which, and there are *lots* of them. You asked your AI helper for a small script, and it produced this.

This walkthrough will follow the full loop from Chapter 8: read it (Ch 2 method), interrogate it (Ch 3–4), copy (Ch 6), run it staged (Ch 5), watch the secrets/paths scans (Ch 7), and rehearse rollback. Along the way we'll spot **three deliberate trust-me traps** — the version you got from the AI, like the first drafts of all AI code, was *slightly* too optimistic, and we pushed back before touching anything real. All edges, honestly shown.

## Pass 1: reading the script (structure)

Here is the script, verbatim, with the code in the left column and the reader's commentary alongside. **Blocks** are the named chunks of the file. Compare each row to what a *less careful* version would look like — that contrast is where the teaching lives.

```python
#!/usr/bin/env python3
"""Rename photo files by prefixing the current date, e.g.:
    IMG_4021.jpg  ->  2026-10-27_IMG_4021.jpg

By default this makes NO changes: it prints a plan only.
Add --apply to actually rename. It never overwrites and
never touches paths outside the folder you give it.
"""
```

*Block A — the header docstring.* Claims, in writing: renames; by default changes nothing; never overwrites; never roams outside the folder you name. Four explicit claims is *good* sign (most scripts make zero). But claims are claims — Chapter 3 says we verify. Keep score as you read: by the end we'll confirm each of the four.

```python
import argparse
import datetime
import pathlib
import sys
```

*Block B — imports.* Notice what is *not* here: no `os`-level delete helpers imported directly, no `subprocess` (can't run other programs), `no requests` (can't phone home), no `shutil` at top level (which would hint at move/delete powers). The script borrows only argument-parsing, dates, path objects, and system-exit. **Power inventory, via imports, in ten seconds: file renames only.** That's a script with a small blast radius.

```python
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", help="folder containing files to rename")
    parser.add_argument("--apply", action="store_true",
                        help="actually rename (default: plan only)")
    args = parser.parse_args()

    root = pathlib.Path(args.folder).expanduser().resolve()
```

*Block C — the command line.* Two arguments and both speak English when you ask for `--help`. `--apply` defaults to *false* — meaning **the safe mode is the default mode**, exactly the Chapter 5 habit we want. Then `resolve()` — this turns the folder argument into an absolute path *now*, and prints stability: whatever wayward tricks the script does later, every path it computes is anchored to the folder `you` named, not to "wherever I happened to be run from." (The Chapter 7 relative-path trap, defused at the door.)

```python
    if not root.is_dir():
        print(f"ERROR: '{args.folder}' is not a folder.", file=sys.stderr)
        return 2
    if not any(root.iterdir()):
        print(f"ERROR: '{root}' is empty — is the path right?", file=sys.stderr)
        return 2
```

*Block D — the boundary checks.* This is the block a trust-me draft omits entirely, and where our walkthrough's first trap is going to live. Two `if` statements, each pairing a *check* with a *polite refusal and exit code*: wrong folder → say so and stop; empty folder → probably a typo — *ask the human*, rather than proceed. Notice how the error messages help: they name what was wrong and suggest what might be right. Boundary, alarm, story. Three of the Chapter 2 audit's three yeses.

```python
    today = datetime.date.today().isoformat()
    renames = []
    for entry in sorted(root.iterdir()):
        if not entry.is_file():
            continue
        if not entry.name.startswith("IMG_"):
            continue
        new_name = f"{today}_{entry.name}"
        renames.append((entry, entry.with_name(new_name)))
```

*Block E — the planner.* **Nothing here renames anything.** The loop only *lists*: walks the folder, filters to `IMG_*` files, builds the *proposed* new names, appends them to a list called `renames`. Two filters, both suggesting good boundaries: `is_file()` skips folders (no folder-rename weirdness); `startswith("IMG_")` targets only the files you meant. And `sorted(...)` — an organized pass, not a chaotic one — is a small but real clue that the author thought about reproducibility: two runs produce the same plan in the same order.

```python
    if not renames:
        print("Nothing to do: no 'IMG_*' files found.")
        return 0
    print(f"Plan: rename {len(renames)} file(s) in {root}\n")
```

*Block F — the count.* The silent-nothing failure from Chapter 5, pre-empted. If the filter matched zero files — as it *will* if your files are actually called `DSC_3021.jpg` instead of `IMG_` — the script says so out loud, with the reason, and exits *successfully* rather than pretending to have done work. And every run states its count up front: "rename 42 file(s)." Compare that to Chapter 5's "42 expected" — now it's a number you can *check against reality*.

```python
    for entry, target in renames:
        if target.exists():
            print(f"SKIP (already renamed, stopping): {entry.name}")
            return 0
        print(f"  {entry.name}  ->  {target.name}")
```

*Block G — plan printing with a collision guard.* Before it names each proposed change, it checks: does the target already exist? If *anything* would be overwritten — including "it's already been renamed" — the whole plan **stops right there** rather than barreling through with collisions. That's the Chapter 3 no-gap principle, again in miniature. Then each line of the plan, old name → new name, printed plainly. This is the exact output Chapter 5 taught you to read: *name by name*, nodding or frowning at each.

```python
    if not args.apply:
        print(f"\nPlan only ({len(renames)} file(s)). "
              "Re-run with --apply to make the changes.")
        return 0
```

*Block H — the dry-run gate.* The gate that keeps promises: without `--apply`, the script *stops here*, having changed nothing, and says how to proceed when you want the real thing. Four claims from Block A checkable so far: default mode changes nothing — **confirmed**; never overwrites — **confirmed** (Block G); state-covered count and plan — **confirmed** (E, G, H).

```python
    moved = 0
    for entry, target in renames:
        try:
            entry.rename(target)
            moved += 1
        except OSError as exc:
            print(f"ERROR: could not rename {entry.name}: {exc}",
                  file=sys.stderr)
            return 3
    print(f"Done: {moved} file(s) renamed in {root}")
    return 0
```

*Block I — the safe apply.* Now — and only now — does anything change. And look *how*: one file per loop trip, each rename individually guarded, and any failure stops everything with a specific message about *which* file and *why*. (Not "some error occurred"; the exact one.) The final line echoes the Chapter 5 ask: **"Done: N things changed."** with N you can compare to the plan. If reality and plan ever disagree, this is the line that will tell you. (A two-line tail not shown here — `if __name__ == "__main__":` calling `main()` — merely hands control to the code above; nothing to audit there.)

## What our three traps looked like

The chapter promised three deliberate trust-me traps found during the walkthrough. Here they are, from the *first draft* the AI gave us, each one caught with a question *before* any code ran:

| Trap | First draft had | The question that caught it | What it became |
|---|---|---|---|
| 1. Optimistic world | `folder = "photos"` — silently relative to wherever the script happened to run | "Which photos, exactly — what if I run this from a different folder?" | Absolute `resolve()` anchored to a folder you *name* (Block C) |
| 2. Silent blast radius | No count, no plan, no filters. *Renamed every file in the folder* to date-prefixed, including the script copies and your notes file | "What files will this touch — list them before changing anything?" | `is_file()` + `IMG_` filter, plan printing, and a count (E–G) |
| 3. Deleting before creating | Collisions solved with `os.remove(target)` before renaming | "What happens to a name that already exists? Delete it?!" | Refuse loudly on any collision (Block G) — no deletion anywhere |

Notice each one is Chapter 3/4's decoder, aimed at a *specific* claim. You don't need to *read code better* to catch these; you need to ask about the boundary of the cook's behavior. And that's the chapter's quiet lesson: **three questions caught three traps. Not code knowledge — asking.**

## Now the routine, timed

The Chapter 8 loop, applied for real. Times here are true ones from the actual run of this book's build tests.

**COPY (2 min).** Snapshot the test folder (`cp -r mini-real mini-real-BEFORE-rename`) — wait, no: the *playground* folder's snapshot, since the audition is in the playground. In the walkthrough's case that's: a mini-real folder inside the playground with three fake "photos" (`IMG_0001.jpg`, `IMG_0002.jpg`, `IMG_0004.jpg`), plus one decoy (`notes.txt`) plus one subfolder. Then the sweeps: no secrets in the script (none — Block B showed no imports with any need, and a text search confirmed no `token|key|password` words), paths clean (no bare roots; no `..` anywhere; no wildcards). Green.

**RUN (5 min).** Dry run:

```
$ python3 examples/walkthrough/safe_rename.py 00-playground/mini-real
Plan: rename 3 file(s) in .../00-playground/mini-real

  IMG_0001.jpg  ->  2026-10-27_IMG_0001.jpg
  IMG_0002.jpg  ->  2026-10-27_IMG_0002.jpg
  IMG_0004.jpg  ->  2026-10-27_IMG_0004.jpg

Plan only (3 file(s)). Re-run with --apply to make the changes.
```

Read that output with Chapter 5's eyes: **count right?** (3 — the decoy `notes.txt` and the subfolder were skipped, which is *exactly* what I want. Green light.) **First few changes sane?** Every line is date + original name, no truncation, no weirdness. **Untouched things untouched?** Dry run proves it structurally (no `--apply`).

Then `--apply` on the mini-real slice: three renames actually happen, "Done: 3 file(s) renamed." Then the **run-twice check**: re-run, and the script answers:

```
Nothing to do: no 'IMG_*' files found.
```

…which is *healthy* for this script: renamed files now start with a date, not `IMG_`, so the filter matches nothing — the idempotence we wanted, arrived at in the natural way rather than by a special-case hack. (A subtler script might want a "re-scan prefix" option; that's a nice-to-have, noted for Chapter 4's "what would you add later" list.)

**ROLLBACK (2 min).** The drill, exactly as rehearsed in Chapter 6: rename the files halfway back with your own two hands — or, the *honest* drill, since the snapshot was taken: wipe the folder, restore from `mini-real-BEFORE-rename`, verify all 4 files identical to pre-run state. Two minutes, half-asleep-able, and now I *know* I'm safe with this script rather than hoping.

Total: under ten minutes, exactly as promised, and every claim the script's header made (four of them) is now *individually verified by watched evidence*, not tone.

## A closing reflection from the walkthrough

Something worth saying plainly, because it's the emotional turn of this whole book: after a walkthrough like this, the script stops being "that thing the AI wrote that I don't understand" and becomes "my renamer, with known edges." That's *agency*, and it's buildable in minutes per script, and it's why this book keeps insisting that a non-coder can, in the practical run-of-life sense, **read code safely** — not by becoming a magician, but by becoming an auditor: the kind of person who checks counts, watches for surprises, rehearses undo, and holds every confident claim until evidence arrives.

The last chapter wraps the essentials into one printable page: the safety checklist and the glossary.

---
