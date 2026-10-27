#!/usr/bin/env python3
"""Rename photo files by prefixing the current date, e.g.:
    IMG_4021.jpg  ->  2026-10-27_IMG_4021.jpg

By default this makes NO changes: it prints a plan only.
Add --apply to actually rename. It never overwrites and
never touches paths outside the folder you give it.
"""
import argparse
import datetime
import pathlib
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", help="folder containing files to rename")
    parser.add_argument("--apply", action="store_true",
                        help="actually rename (default: plan only)")
    args = parser.parse_args()

    root = pathlib.Path(args.folder).expanduser().resolve()

    if not root.is_dir():
        print(f"ERROR: '{args.folder}' is not a folder.", file=sys.stderr)
        return 2
    if not any(root.iterdir()):
        print(f"ERROR: '{root}' is empty — is the path right?", file=sys.stderr)
        return 2

    today = datetime.date.today().isoformat()
    renames = []
    for entry in sorted(root.iterdir()):
        if not entry.is_file():
            continue
        if not entry.name.startswith("IMG_"):
            continue
        new_name = f"{today}_{entry.name}"
        renames.append((entry, entry.with_name(new_name)))

    if not renames:
        print("Nothing to do: no 'IMG_*' files found.")
        return 0
    print(f"Plan: rename {len(renames)} file(s) in {root}\n")

    for entry, target in renames:
        if target.exists():
            print(f"SKIP (already renamed, stopping): {entry.name}")
            return 0
        print(f"  {entry.name}  ->  {target.name}")

    if not args.apply:
        print(f"\nPlan only ({len(renames)} file(s)). "
              "Re-run with --apply to make the changes.")
        return 0

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


if __name__ == "__main__":
    raise SystemExit(main())
