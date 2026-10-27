"""Tests for the runnable walkthrough example: examples/walkthrough/safe_rename.py.

Run with:
    python3 -m unittest discover -s tests -v

Runs the real script (via subprocess) against throwaway fixtures in a temp
directory and verifies the safety behaviors the book teaches:
- plan-only default mode changes nothing
- --apply renames only IMG_* files, leaves decoys and subfolders
- run-twice idempotence ("Nothing to do")
- loud, coded refusals for missing/empty folders (exit 2)
- collision guard stops the plan instead of overwriting
- --help presents the English summary
"""

import datetime
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "walkthrough" / "safe_rename.py"

TODAY = datetime.date.today().isoformat()


def run(*argv, cwd=None):
    return subprocess.run(
        [sys.executable, str(EXAMPLE), *argv],
        capture_output=True,
        text=True,
        cwd=cwd,
    )


class SafeRenameExampleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp(prefix="example-test-"))
        self.folder = self.tmp / "mini-real"
        self.folder.mkdir()
        for name in ("IMG_0001.jpg", "IMG_0002.jpg", "IMG_0004.jpg",
                     "notes.txt", "odd name (final)v2.jpg"):
            (self.folder / name).write_text("fixture")
        (self.folder / "2016-old").mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def captures(self):
        return sorted(p.name for p in self.folder.iterdir())

    def test_plan_only_changes_nothing(self):
        proc = run(str(self.folder))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Plan: rename 3 file(s)", proc.stdout)
        self.assertIn("Plan only (3 file(s))", proc.stdout)
        self.assertIn(f"IMG_0001.jpg  ->  {TODAY}_IMG_0001.jpg", proc.stdout)
        self.assertNotIn("notes.txt", proc.stdout)  # decoy never in the plan
        self.assertNotIn("odd name", proc.stdout)
        self.assertEqual(
            self.captures(),
            ["2016-old", "IMG_0001.jpg", "IMG_0002.jpg", "IMG_0004.jpg",
             "notes.txt", "odd name (final)v2.jpg"],
            "plan-only run must not touch anything",
        )

    def test_apply_renames_only_img_files(self):
        proc = run(str(self.folder), "--apply")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Done: 3 file(s) renamed", proc.stdout)
        self.assertEqual(
            self.captures(),
            ["2016-old", f"{TODAY}_IMG_0001.jpg", f"{TODAY}_IMG_0002.jpg",
             f"{TODAY}_IMG_0004.jpg", "notes.txt", "odd name (final)v2.jpg"],
        )
        # decoys survive byte-for-byte
        self.assertEqual((self.folder / "notes.txt").read_text(), "fixture")
        self.assertTrue((self.folder / "2016-old").is_dir())

    def test_run_twice_is_idempotent(self):
        self.assertEqual(run(str(self.folder), "--apply").returncode, 0)
        second = run(str(self.folder), "--apply")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("Nothing to do", second.stdout)
        self.assertNotIn("Plan: rename", second.stdout)

    def test_missing_folder_is_loud(self):
        proc = run(self.tmp / "does-not-exist")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("is not a folder", proc.stderr)

    def test_empty_folder_is_loud(self):
        (self.tmp / "empty").mkdir()
        proc = run(self.tmp / "empty")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("empty", proc.stderr)

    def test_collision_stops_plan_without_changes(self):
        (self.folder / f"{TODAY}_IMG_0001.jpg").write_text("already here")
        proc = run(str(self.folder))
        self.assertEqual(proc.returncode, 0)
        self.assertIn("SKIP (already renamed, stopping)", proc.stdout)
        self.assertNotIn("--apply", proc.stdout)  # no push to proceed with collisions
        self.assertTrue((self.folder / f"{TODAY}_IMG_0001.jpg").exists())
        self.assertTrue((self.folder / "IMG_0002.jpg").exists(), "plan stopped early")

    def test_help_works(self):
        proc = run("--help")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("--apply", proc.stdout)
        self.assertIn("NO changes", proc.stdout)

    def test_nothing_outside_the_folder_is_touched(self):
        sibling = self.tmp / "outside"
        sibling.mkdir()
        (sibling / "IMG_9999.jpg").write_text("outside")
        run(str(self.folder), "--apply")
        self.assertTrue((sibling / "IMG_9999.jpg").exists(), "script touched outside folder")


if __name__ == "__main__":
    unittest.main()
