# Chapter 2 — Reading Code You Cannot Write

Chapter 1 gave you the mental model: code is a recipe for a literal-minded cook, and reading means scanning for **power and boundaries**. This chapter gives you the actual method — a ten-minute, three-pass way to read any AI-written script without being able to write one.

Before the method, one mindset reset. People who "can't program" tend to open a code file and feel the same dread as opening a book in a language they don't speak. But code has a superpower natural language doesn't: **it's readable backwards, in any order, one part at a time.** You can start in the middle, find one clause you understand, and grow out from there. There's no plot to lose. Enter anywhere, exit anytime.

## Pass 1: The structure pass (2 minutes)

You're not reading yet — you're *mapping*. Scan top to bottom and collect, on a sticky note or in a comment at the top of your notes:

**Files, and what they claim to be.** The file name itself is data. `rename_photos.py` promises one thing; `backup_and_email_and_delete.py` promises four things. Multi-promise scripts get extra suspicion; single-promise scripts get slightly less.

**The comments at the top.** AI-written scripts usually open with a header comment block explaining usage. Read it — but read it as a *claim*, not a description. The comment was written by the same confident author whose claims we'll audit in Chapter 3. Header comments often genuinely lie by omission: they say what a script does, not what *changes* it makes.

**The function names.** Functions are the script's table of contents. Just reading them in order usually tells you the story:

| Function sequence | The story it tells you before reading a single body |
|---|---|
| `find_files`, `parse_dates`, `build_new_name`, `rename_safely`, `main` | Takes files, works out new names aligned to dates, renames with a safety emphasis. Coherent. |
| `load_config`, `connect`, `fetch_all`, `transform`, `push_to_remote`, `cleanup` | Reads settings, goes to the network, fetches data, changes it, sends it somewhere else, then "cleans up" — and cleanup is exactly the kind of vague word that hides deletes. Be more suspicious. |
| `obfuscate`, `encode_payload`, `do_request`, `decode_response` | A network thing that hides what it's sending. Anytime "encode/obfuscate" appears without an obvious honest purpose, stop and question. |

Naming honesty is a real signal. An AI-generated script with a function called `rename_safely` might still not rename safely — functions can be ignorantly or aspirationally named — but it's *more* likely than one named `do_it`. More importantly, a name like `push_to_remote` is a **boundary marker**: it names a part of your world (somewhere remote) the script will touch.

## Pass 2: The power pass (3 minutes)

Now read for four specific kinds of lines. You're allowed to skip everything else.

**1. Imports — who is it borrowing power from?**

| Import you'll see | What power it grants | Read it as |
|---|---|---|
| `os`, `shutil`, `pathlib`, `Path` | Files and folders — the cook's hands | "This touches my files." |
| `requests`, `urllib`, `httpx`, `fetch`/`axios` (JS) | The internet — sends and downloads | "This talks to the outside world." |
| `subprocess`, `child_process`, `exec`, `spawn` | Runs *other programs* | "This can do literally anything the Other Program can do." |
| `smtplib`, `email`, `nodemailer` | Sends email | "This sends mail as me." |
| `json`, `csv`, `sqlite3`, `database` | Reads/writes structured data, maybe databases | "This changes data records, not just files." |
| `schedule`, `time.sleep` in loops, `threading` | Runs over time / in parallel | "This doesn't necessarily end when I expect." |
| `crypt`/`bcrypt`/`hashlib` with no clear reason | Password or credential handling | Red flag. Why does a photo-renamer need this? |

**2. Loops — what is it doing once for *every* thing?**

`for` loops are where scripts scale up their effect. "Rename 3 files" and "rename 30,000 files" can be the *same line of code*. Find each loop and ask: over what collection, and is the range what I'd expect? A silent classic: a loop over `os.listdir(".")` — which includes files you forgot exist, plus system clutter the script will now chew on.

**3. Conditions — what are its safety valves?**

`if` statements are the script's boundaries. For each loop or destructive action, look uphill: is there a check that says "this thing exists," "this thing isn't empty," "this thing matches what I expect"? A script whose dangerous line has an `if` guarding it is infinitely tamer than the same dangerous line with nothing above it. Beginners should learn to *spot the void*: a destructive line standing naked in the code, nothing between it and execution.

**4. Danger words — the specific classics.**

| Danger word | Typical meaning | Why non-programmers should know it |
|---|---|---|
| `remove`, `unlink`, `os.remove`, `del` | Deletes a file — gone, no undo, no trash | The cook doesn't use a trash can. |
| `rmtree`, `shutil.rmtree`, `rm -rf` | Deletes a folder **and everything inside it** | Nuclear. Chapter 7. |
| `"w"` mode, `open(f, "w")`, `WriteAllText` | **Overwrites** a file with new content | Old contents replaced forever. |
| `write()` on an existing file (JS/Go-style), `>` in shell | Same as above, different costume | |
| `subprocess`, `os.system`, backticks in shell code | Runs another program with these words as arguments | Bugs here can become arbitrary commands run as you. |
| `requests.post`, `fetch(url, {method: "POST"})` | Sends data somewhere over the network | Where to? That's a question for Chapter 3/4. |
| `curl` piped into `bash` or `sh` (download-and-run in one line) | Downloads a script and runs it *immediately* | The single most "trust me" pattern in existence. |
| `chmod`, `sudo`, `Authorization: Bearer` | Changes permissions / does privileged things / sends a credential | Chapter 7 twice. |
| `.env`, `config`, `password`, `token`, `api_key` | Credential-adjacent words anywhere | Instant Chapter 7 reading pass. |
| `git push --force`, `rm -rf .git` | Rewrites or destroys your version history | Refuse automatically. |

You do not need to memorize this table to use this book; you need to *skim with it in mind*, and let Chapter 10's checklist remind you. Pro readers google unknown words rather than skip them — and if an AI is beside you (OpenCode, ChatGPT, etc.), the fastest move is: **"What does this exact line do? What's the worst realistic thing it could do?"** — no shame in that, ever. The AI can't read your mind, but it *can* annotate its own work; using it for that is Chapter 4's job.

## Pass 3: The boundary pass (5 minutes)

Now you read, slowly, only the **contact points** — the places where the script touches Anything That Exists:

1. **Every file it might open, write, rename, or delete.** Trace each one: is the name hard-coded (`"photos"`) — which is brittle but predictable — or assembled from something flexible? Where does the flexible part come from: your typing, a config file, an AI guess?
2. **Every network send.** What data goes where, and is the destination a name you recognize and approve?
3. **Every external program it runs.** A script that shells out to `rclone`, `git`, `ffmpeg`, or `node` inherits *all* of those programs' powers. You should know which ones and why.
4. **Endings.** Does the script end when you'd expect? Or does it loop forever / run on a schedule / wait for more work? Anything that "doesn't necessarily stop" needs an extra look at Chapter 5 (the run-twice rule).

For each contact point, run a small three-question audit:

- ☐ Does it **check first**? (Does the code verify the thing exists, is non-empty, matches expectations, *before* acting?)
- ☐ Does it **ask me first**? (For anything irreversible: does the script prompt — or at minimum support a dry-run — or just act?)
- ☐ Does it **limit itself**? (Loops bounded? Files restricted to one folder? Sizes capped? Retries limited?)

Three yeses = a well-bounded script. Two or fewer = you found exactly where to point your Chapter 4 questions. This is the whole reader's game: **notice where the power is, then check whether anyone built fences around it.**

## What to do when you hit something you truly don't understand

You will, often. Three moves, in order:

1. **Note it and keep scanning.** Non-programmers' biggest reading mistake is *bailing out at the first hard line*, as if reading requires total comprehension. It doesn't. Exit and reenter; mark it `?` and move on. Many "?"s resolve themselves from context two paragraphs later.
2. **Ask your AI to explain *that exact line*, like this:** "Explain line 14 like I've never programmed. What does it do? Worst realistic thing it could do? Is there a safer version?" Asking *per line* works much better than asking "explain this whole file" (the answer will be confident, generic, and too long). Line-by-line keeps the AI honest.
3. **If it still doesn't resolve: it goes on the risk list.** Anything you don't understand *as a reader* is, by definition, a boundary whose power you haven't assessed — treat it as a candidate risk, and let Chapter 4 turn your list into pointed questions before you ever run anything.

## One warning about reading AI code that reads "fine"

AI-written code is usually *beautiful*. Consistent spacing, nice function names, friendly comments, tidy structure. It doesn't look like a beginner's chaos; it looks like a senior engineer's prose. This is a trap worth naming in plain terms: **looks-professional and works-safely are different axes.** Beautiful code with no error handling will crash the same way ugly code would; a confidently commented script can still hard-code a wrong path. In Chapter 3 we'll target the *claims* made about beautiful code; here, just stamp this on your brain: **style is not safety.** You're reading for power and fences, not for elegance.

---
