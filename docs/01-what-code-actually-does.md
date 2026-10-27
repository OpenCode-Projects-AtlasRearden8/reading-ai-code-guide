# Chapter 1 — What Code Actually Does

Before you can read code safely, you need a working mental model of what code *is*. Not a computer science model — a kitchen model. Once you have this one analogy, 90% of what confuses beginners about "code" stops being mysterious, and the safety chapters in this book start to feel obvious rather than exotic.

## The recipe analogy (and where it runs out)

Code is a **recipe written for a very fast, very literal, very dumb cook**.

- A *program* is the whole recipe: "Make lasagna. First boil the pasta, then brown the meat…"
- A *script* is a one-page recipe — renamethese-files.txt, redo-my-spreadsheet.txt. Most AI-written code you'll get is a script.
- The *computer* is the cook: it follows the recipe word for word, at absurd speed.
- The cook is **dangerously literal**. If the recipe says "cut the onions," the cook cuts whatever is nearest, no questions asked — while you meant "the two onions in the fridge." The recipe had no idea what you "meant."
- The cook **never tastes anything**. It doesn't notice the dish is wrong; it only notices when the *instructions* are impossible ("take the pan out of a cupboard with no pan"). "The lasagna tastes like salt-salt salt" is a real dish the cook will proudly serve you, because nobody told it onions aren't salt.

That last point is the core insight of this entire book: **a computer running code never evaluates the outcome**. If the instructions are wrong *in a possible way* — "delete every file in C:\Users\Dylan" when you only wanted a temp folder cleaned — the cook will do exactly that, immediately, without hesitating, without asking.

And here's where the analogy runs out in an important, uncomfortable direction: recipes only touch food. **Code touches files, internet connections, and other programs.** The cook can open your mail, wire money, and burn down the kitchen if the recipe says so. That's why we have safety routines you'd never need for making soup.

## What a program actually consists of

Any script, in any language, is made of a few kinds of parts. You can ignore the fancy names below on a first read; they're here for the glossary to point back at.

| Part | What it really is | Kitchen phrase |
|---|---|---|
| Statement | One instruction. Often one line. | "Preheat the oven." |
| Variable | A labeled box holding one piece of information. | The note "2 cups" taped to the counter. |
| Function | A named mini-recipe you can call by name, over and over. | "The dressing recipe" — invokes it whenever. |
| Condition (`if`) | "If this, do that; otherwise something else." | "If the dough is wet, add flour." |
| Loop (`for`, `while`) | "Do the following over and over — usually once per item." | "Roll one ball; repeat for the whole batch." |
| Comment | A note written *for humans* the computer skips entirely. | A margin note in the recipe. |
| Import | A line that borrows somebody else's pre-written mini-recipes. | "Use the store's pizza dough." |

**Imports matter more than beginners expect.** When your script says `import requests`, it is borrowing someone else's internet-handling code. `import os` grants access to your files and folders — the cook's hands. In Chapter 2 we'll build a habit of checking imports first, because they tell you which *domains* of power a script holds.

Also worth knowing: most scripts you get from an AI are a **main flow plus a few helper functions**. The main flow is what happens when you run it; the helpers are sub-recipes it uses. When you read code in Chapter 9's walkthrough, you'll see exactly this shape.

## A real tiny script, dissected

Here is a genuinely small, genuinely useful script of the kind an AI would hand you. You are not asked to write one ever — only to recognize its parts. Language is Python, chosen for readability + ubiquity.

```python
import os
import datetime

def today_prefix():
    return datetime.date.today().isoformat()

folder = "photos"
for filename in os.listdir(folder):
    if filename.startswith("IMG_"):
        new_name = today_prefix() + "_" + filename
        print("Would rename", filename, "to", new_name)
```

Line by line, in non-coder language:

| Code | What it does | Sanity check a reader does |
|---|---|---|
| `import os` | Grants the script file-and-folder access. | "This one touches my files." |
| `import datetime` | Grants access to a catalog of date helpers. | "It needs to know today's date. Fine." |
| `def today_prefix():` | Defines a helper mini-recipe producing today's date as text. | "Skimmed. A date, fine." |
| `folder = "photos"` | Sets the working folder to *photos, relative to wherever this is run*. | "Which photos? Note for Chapter 7." |
| `for filename in os.listdir(folder):` | Loop: once for every file in the folder. | "It will act on EVERY file there. All of them?" |
| `if filename.startswith("IMG_"):` | Condition: only files starting with `IMG_` get processed. | "Good — the ones I care about." |
| `new_name = today_prefix() + …` | Builds the new name: date prefix + the old name. | "Old name survives. Nothing destructive." |
| `print("Would rename", …)` | Prints a plan. **Does not rename.** | "This version changes nothing. This is a DRY RUN." (Chapter 5) |

Notice what you just did without being able to write a line of code: you identified what it touches (files), what it would *not* do (rename), and one loose end (relative folder) that Chapter 7 turns into a habit. That is reading code, reader-style: not comprehending every character, but understanding **every *kind* of thing it could do to your world**.

## What happens when you run it

A useful thing to internalize: between "code exists" and "code does anything," there is a gap. Code written by an AI has *proven* nothing by existing. Three moments matter:

1. **It must be written** (AI's moment — seconds, effortless).
2. **It must be run** (your moment — here the real world enters: your folders, your network, your bad luck).
3. **It must be relied on** (a later moment — when it *matters*, e.g., it runs overnight, unwatched, on data you didn't back up).

The AI can never perform steps 2–3. This is why the phrase "it works on my end" is literally meaningless in an AI's mouth — a chapter 3 topic — and why Chapter 5's philosophy is: **the moment code meets actual reality is the only moment that counts.**

## The four reader questions

Every script can be interrogated with four questions. You can't answer them perfectly on first glance, but even a half-answer flags 80% of the trouble a script can cause:

| Question | What it uncovers | Where in the code to look |
|---|---|---|
| **1. What does it take in?** | Inputs: files it reads, things you type with flags/arguments, network calls it makes | The start; `open(`, `input(`, `sys.argv`, `requests.` |
| **2. What does it change?** | What it creates or alters: renames, writes, database edits | The middle; `open(…, "w")`, `$file > `, `.write(`, `rename`, `commit` |
| **3. What does it touch outside itself?** | The boundaries where dangerous stuff lives — deletes, sends, emails, uploads, shell-outs | DANGER WORDS. Chapter 2 gives you the exact list |
| **4. When does it stop?** | Whether it knows how to stop gracefully — and whether loops have safety valves | "while" loops, missing `if` conditions, missing maximums |

Chapter 2 turns these into an actual 10-minute reading method. But keep the questions around; they're the reason a non-coder *can* read code: you're not reading for grammar, you're reading for **power and boundaries**. Power = what it can do. Boundaries = what limits that power. Dangerous code is, almost always, code with lots of power and few obvious boundaries.

## You don't need to read it all

The most liberating sentence in this chapter might be this: **nobody fully reads code either.** Professional programmers skim constantly, selectively, and strategically — reading just enough of the right parts to answer *the four questions above and the specific new risk on the table.* The AI-generated 200-line script someone hands you? You will read roughly 10% of it carefully: the countryside around imports, file names, loops, and any danger words. The rest — the beautiful formatting of the HTML it generates, the long lists of test data — gets skimmed.

| Reading pass | Time | What you do |
|---|---|---|
| **Structure pass** | 2 minutes | Names of the file(s), function names, comments. What is this *for*? Does the shape match the promise? |
| **Power pass** | 3 minutes | Imports, `for` loops, and any DANGER WORDS from the table in Chapter 2 |
| **Boundary pass** | 5 minutes | For each contact point with your world: does it ask first? check first? have limits? refuse the dangerous version? |

Ten minutes, twice. That's a full non-coder review. Chapter 9 walks one script through it step by step.

## When "I can't read code" stops being true

A friendly note, since this book is written for people who self-describe that way: after years of teaching beginners, the honest observation is that practically no one *can't* read code. Plenty of people *believe* they can't because they've been shown code through the wrong lens — the lens of "understand every line" (which fails, and always would) instead of "understand what it does to me and my files" (which anyone can achieve in ten minutes per script).

Reading code is closer to reading a rental agreement than reading a novel. You're not there to admire the prose. You're there to scan clause by clause, find the ones that can legally hurt you, and refuse anything that doesn't come with a way out. That skill is learnable, teachable, and — given one morning and this book — fully inside your capability.

Let's get you the exact method.

---
