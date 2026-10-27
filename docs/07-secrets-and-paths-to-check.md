# Chapter 7 — Secrets and Paths to Check

Two things cause the *real* damage when AI-written code goes wrong: **secrets** (credentials that shouldn't be seen, shared, or uploaded) and **paths** (places in your file system the script shouldn't go). Neither one is exotic. Both show up in tiny beginner scripts. Both are checkable in a couple of minutes once you know what to look for. This chapter gives you the two scans that, between them, cover the worst practical outcomes of running code you didn't write.

## Part one: secrets

### What counts as a secret

Broader than most people think. A secret is *anything another party could use to be you or to unlock something of yours*:

| Category | Examples |
|---|---|
| API keys & tokens | `sk-…` (OpenAI-style), `ghp_…` (GitHub personal access token), AWS access keys, Stripe keys, Notion/Airtable/Zapier tokens |
| Login credentials | Passwords, sign-in cookies, saved-session files |
| Identity documents you'd never share | Tax forms, account statements, patient records (and nurses: anything PHI), contracts |
| Access to your money or your store | PayPal API strings, eBay/Etsy tokens, bank feeds |
| Private personal data | Contacts, addresses, birthdates — yours, family's, clients' |

An AI cannot be *given* a secret safely either. Any key, password, or sensitive personal file you paste into a chat is now outside your control — even with a trustworthy vendor, it lands in logs you don't read. Rule for this book: **never paste a secret into an AI conversation. Not even to ask "is this key safe?"** Describe it instead: "the AI asked for an API key; what should I do?"

### Where AI code leaks secrets — the four classic doors

**Door 1: The code hard-codes it.** You asked for "use my OpenAI key" and the AI, knowing no better (you didn't provide one), wrote a placeholder like `API_KEY = "sk-REPLACE-ME"` — and *then you* filled in the real key, and now it lives in a file that Git or an upload might someday carry away. This is the most common real-world secret mishap in beginner projects. The fix is structural and easy to ask for: **"Load the key from an environment variable or a `.env` file that's listed in `.gitignore`; never write it inside the code."** (Your AI knows exactly what that means — it's the industry-standard shape — and the *Free AI Coding with OpenCode* handbook covers the `.gitignore` side in detail.)

**Door 2: The code reads the wrong file.** A script meant to process your photos also walks the folder and reads `passwords.txt` — not maliciously, just indiscriminately. Prevention: keep secrets *outside* folders scripts operate on. Physical separation is the only 100% defense; a script scanning `/home/you` can find things, while one restricted to `/home/you/photos-editing` mostly can't.

**Door 3: The code *sends* your files somewhere.** Networking plus careless file-reading: an upload accompanying a "helpful" debug log. Ask Chapter 4's question 7 up front; read network-sending code per the Chapter 2 method. If a script uploads *anything*, you should be able to name the destination and why.

**Door 4: The AI repeats it back.** If a key is already in your chat history from an earlier paste, later messages can quote it, log it, or embed it in "just a debugging print" — and screenshots of those chats end up in tutorials. If a secret ever entered a chat, treat it as **leaked: rotate it now.** Revoking and re-issuing an API key takes two minutes in the vendor's dashboard and is nearly always free. It's the cheapest insurance in computing and beginners skip it constantly.

### The 2-minute secret sweep

Before relying on any AI-written script, run this sweep on it. If your text editor has find, you can do it in 60 seconds:

- ☐ Search the code for the shape of keys you actually use (see table above). Expect *none* in code.
- ☐ Search for the words `key`, `token`, `password`, `secret`, `Authorization`, where they're *used*.
- ☐ Check what it reads/writes: is any file on that list instead of your data?
- ☐ Find *where* secrets, if any, are expected to live — env var, `.env`, config file — and confirm that file is *not* somewhere Git would grab it.
- ☐ If the script talks to the internet: confirm nothing sensitive travels. When in doubt, Chapter 5's airplane-mode-ish testing works here too (run offline and watch what it complains about).

If anything on this list surprises you: stop, ask your AI about it in the plain-words way (no pasting), and rotate anything already exposed. That's the whole sweep — a couple of searches, half a minute each, and the class of "oops, my key" is effectively covered.

## Part two: paths

### The one idea to internalize

A **path** is where something lives on your computer, written down. `C:\Users\Dylan\Documents\book\chapter-3.docx` is one; `book/chapter-3.docx` is another. The difference between those two is *the entire concept* of this half of the chapter:

| Kind | Written like | What it says | Risk level |
|---|---|---|---|
| **Absolute** | `C:\Users\…`, `/Users/you/…`, `/home/you/…` | A place *in absolute terms* — which computer, which account, everything pinned | Safe but rigid: breaks on other machines unless adjusted |
| **Relative** | `photos`, `./output`, `../data` | A place *relative to where you happen to run it* | Flexible but surprising: run it from the wrong folder and "photos" means a *different* photos |

Relative is why the Chapter 1 example script had a loose end: `folder = "photos"` doesn't say *which* photos — it means "a folder named photos near wherever I happen to be run." Run it from your home directory and *you* probably have no such folder — or worse, you do. This is the #1 lurking surprise for beginners running scripts prepared by someone else: **the script's "photos" and your photos are different folders unless proven otherwise.**

### The dangerous-paths scan

AI misadventures in file paths follow patterns. Scan for these:

- ☐ **Root paths.** Any path that is just `/`, `C:\`, `C:\Windows`, `~` (your whole home!), or a drive letter with nothing after it. A script told to delete everything in such a path will happily do so. If a *bare* root shows up as a default, stop and ask.
- ☐ **Walking up.** `..` (or `../..`) means "one level up." A cleanup script that computes "everything one level up from here…" is sweeping beyond its lane. Ask: how far up do you go, and why?
- ☐ **Home-wide or disk-wide operations.** Anything that *searches from* your home folder, mentions "all drives", `/mnt`, backup locations ("backup!") or system directories is beyond reasonable for a fresh script. The right place is a subfolder of your project.
- ☐ **Hard-coded personal paths from the AI's imagination.** `C:\Users\YourName\...`, `/Users/username/...` — never real. Replace with your actual path; verify by *printing* it before acting on it.
- ☐ **Wildcards in commands.** `rm -rf *`, `del *.*`, `find … -delete` — delete-everything-matching commands. If you see one and you did not explicitly discuss it, do not run it. Ask what it would actually match — the truth may be "everything in this folder, including what you meant to keep."
- ☐ **The silent overwrite target.** Where does output *go*? Same folder (overwrites) or a new folder (almost always what you want for iterables)? This is Chapter 3's no-gap principle again, expressed as a path question.

### Rehearsing paths safely

Paths are easy to test *before* landing on real files, and the tests are pleasant to watch:

- ☐ Run the script's first stage (or dry run) and note the paths it *claims*. In our Chapter 9 example, the dry run prints each path before touching anything.
- ☐ Use `pwd` (Linux/macOS) or `cd` (bare, Windows) — prints the folder you're standing in relative to the script.
- ☐ Rename one file's path deliberately (a playground file): does the script skip it loudly?
- ☐ Feed it a path that doesn't exist: does it refuse or guess? (Guessing paths = asking for weird outcomes.)

None of these take more than a minute each. They teach you what beforehand: **what the script thinks "here" is, whether it checks those beliefs, and how it fails when wrong.** That's path-safety, whole.

## The combined pre-launch check: one paragraph you'll memorize

Long after this book's details fade, keep the paragraph. Here it is, one breath long:

> *What does it read, what does it change, where does it go outside its folder, and what does it ask for secrets-wise — and where do those live?*

Read (Chapter 2) and distrust (Chapter 3), and you'll have narrowed in on those four questions already. This chapter just gives them teeth: two minutes scanning for secrets, three minutes for paths, and the scary categories are covered.

Next up, these combine into the one routine to carry everywhere: **copy-run-rollback.**

---
