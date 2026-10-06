# Pipeline — quizzes from source to production

`<kit>` is `<Funda>/scripts/lessons/kit`. The repo's `scripts/lessons/README.md` ("Quizzes") is the
contract and wins over this file.

## Layout

```
<set>/quizzes/
  src/NN-<name>/build.mjs              writes quiz JSON with writeQuiz(); import the kit as
                                       '../../../../../kit/quiz.mjs'
  <topic-folder>/<lesson-file>.json    one per lesson, named exactly like the lesson file
  <topic-folder>/_topic.json           the topic's exam-practice quiz
```

Build scripts are the source of truth; never hand-edit the JSON. Number `src/` folders like the
lesson set's (`01-exponents` for the lessons' topic order) and resolve the output folder with
`new URL('../../<topic-folder>/', import.meta.url)`.

## Ids — nothing to assign

Quiz ids derive from the lesson id (or topic id), questions from the quiz id + slot `key` + variant
position, options from the question id + option position (`kit/quiz-rows.mjs`). Consequences:

- A slot `key` is permanent once loaded. Rename it and the loader makes new questions; the old
  ones stay (reported).
- Variant order is permanent: append new variants at the end, never insert or reorder.
- Option order within a loaded variant should stay; the app shuffles anyway.
- A renamed lesson file keeps its id (funda-lessons moves the id), so rename its quiz file too.

## Gates — all clean before loading

```
node <kit>/build-quizzes.mjs <set>
node <kit>/check-quizzes.mjs <set> [topic-folder…]
```

`check-quizzes` enforces: a quiz for every lesson of each checked topic plus `_topic.json`; 2+
variants per slot, one type per slot; option counts and exactly-one-right; feedback on every wrong
option; typed answers are one word or a plain number with the matching instruction; anchors are
headings (or the title) of the lesson; lengths the API accepts; copy rules; every `$…$` renders
with the API's MathJax.

It also runs the lesson diagram checks (`check-svg`, `check-contrast`) on every question
diagram. It cannot check that a diagram looks right: render them —
`node <kit>/render-svgs.mjs [--dark] <png-dir> <set>/quizzes/<topic>` — and Read the PNGs.

It cannot check that an answer is right. **Work every variant's answer yourself**, from scratch,
and every distractor's claimed mistake (does that mistake really give that option?). For
Mathematics, evaluate numerically where you can (substitute a value into both the question and the
answer).

It cannot judge distractors either. **Review every slot for silliness** (the checklist is
question-craft.md, "Wrong options are diagnoses", "The stem never gives the answer"):

- Each wrong option: would a half-prepared learner pick it? Is its feedback a real mistake, not
  "this is false"? Same kind and length as the right option?
- Elimination test: answerable without the lesson? Rewrite.
- Content subjects: count variants naming a real place, case study or dated event; a topic
  where few do is too hypothetical.
- Reuse: no stem shared verbatim between two quizzes —
  `node <kit>/audit-quiz-repetition.mjs <set>` fails on one.

When an agent wrote the quizzes, the lead samples at least one topic per grade with this list
before loading; a pattern found there means a fix pass over every topic, not just the sample.

## Load locally (lead only)

```
./scripts/lessons/load.sh <set> --quizzes --dry-run     # outcome, rolled back
./scripts/lessons/load.sh <set> --quizzes               # local DB + cache bump
node <kit>/quiz-api-check.mjs <set>                     # what the API serves: count, clock, difficulty
```

The lessons must be loaded first. The loader, per quiz and per question, inserts new rows, updates
rows that are still a version the repo produced (git history of the quiz file + working copy), and
skips and lists anything edited in the admin. **During local iteration** an uncommitted change to
something already loaded reads as "edited": reload with `--overwrite-edited=<quiz id>` (local only),
or commit first.

Then play every quiz as a local test learner:

```
QUIZ_CHECK_TOKEN=<local learner access token> node <kit>/quiz-api-check.mjs <set> --play
```

It starts and submits every quiz twice: the source's answers must score 100%, "4" must fail for
"-4", and the second sitting must serve other variants. Mint the token for a seeded local learner
(HS256 over `JWT_ACCESS_SECRET` from the repo's `.env`, payload `{sub, email, isAdmin: false, iat,
exp}`, sent as the `access_token` cookie). Local only: it spends that learner's first attempts.

Look at one lesson quiz and the topic quiz on the iOS Simulator if the owner is signed in there:
maths on the baseline, options readable in dark mode, the review screen's feedback and "re-read"
link. Ask before signing in; never type a password.

## Hand-off

1. Commit sources and JSON together — only when the owner asks, never while agents are writing.
2. Production commands for the owner (lessons first if they are new too):

   ```bash
   DATABASE_URL=<prod> ./scripts/lessons/load.sh <subject>/grade-<n> --quizzes --dry-run
   DATABASE_URL=<prod> VALKEY_URL=<prod valkey> ./scripts/lessons/load.sh <subject>/grade-<n> --quizzes
   node scripts/lessons/kit/quiz-api-check.mjs scripts/lessons/<subject>/grade-<n> https://<prod api>
   ```

3. Quizzes have no on/off switch: they go live with their lesson (or topic). A lesson hidden while
   it waits for a photo keeps its quiz hidden too.
