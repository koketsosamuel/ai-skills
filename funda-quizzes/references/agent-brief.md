# Agent brief — template

Write this once per run as `QUIZ-BRIEF.md` in the session scratchpad (not the repo), fill the `{…}`
parts, and have every quiz agent read it. Prompts then stay short: identity, the brief path, their
topic(s), their output folder.

---

# Brief: {Grade} {Subject} quizzes for Funda SA

You write the quizzes for finished Funda SA lessons: one quiz per lesson and one exam-practice
quiz per topic. Readers are South African {Grade} learners (about {age}) preparing for their June
and November papers.

## Hard rules (non-negotiable)

- Write ONLY `{set}/quizzes/src/{NN-name}/` and `{set}/quizzes/{topic-folder}/`. Every other
  file — the lessons, `lessons.config.json`, the kit — is read-only to you.
- No git commands at all. No database, Valkey or API writes. No browser, Browser pane or iOS
  Simulator. Never sign in anywhere or type a password.
- Other agents work in sibling folders at the same time. Don't touch their folders.
- Every slot has at least 2 variants: same skill, steps, difficulty and time; different numbers
  and a different answer.
- Typed answers are one word or a plain number (≤ 2 decimals) — build them with `number()` or
  `word()`. Anything else is `choice`.
- Every wrong option is a real mistake from the exam map, with `feedback` and a `tag` — one a
  learner who half-studied would pick. No silly, absurd or joke options ("coal regrows",
  "workers become fuel", "illness is impossible"), no "no reason" fillers. All options the same
  kind, length and tone. question-craft.md, "Wrong options are diagnoses".
- The stem never contains or points to the answer; if you can answer from the stem and options
  without the lesson, rewrite it.
- Knowledge questions use the real places, case studies and facts the lesson teaches, not
  "Town A / Utility B" (keep those for calculations and data reading). A case-study quiz names
  its case study.
- Never pass a `title` to `quiz()` and never write "quiz" in a title: `writeQuiz` names each quiz.
- The topic quiz uses new stems, never copies of lesson-quiz slots or lesson quickchecks.
- Every slot's `objective` names its exam-map line and the paper it adapts.
- Work every answer yourself, from scratch. Wrong answers in a quiz teach wrong maths.
- Give a question the diagram the paper would print beside it, drawn with `{Funda}/scripts/lessons/kit/figures/`
  from that variant's own numbers (`diagram:` in the variant's extras); redraw a paper's figure,
  never crop it. Text and figure must agree exactly, and the figure never gives the answer away.
- Fit one screen: short stems, options short enough to sit two to a row (≤ 14 characters, units in
  the stem), diagrams wide rather than tall — question-craft.md, "Fit one screen".

## Read first

- `{set}/EXAM-MAP.md` — your topics' sections
- `{skill}/references/question-craft.md` — how a question, its options and its variants are built
- the lessons in `{set}/{topic-folder}/` — what each teaches and its headings (your anchors)
- `{Funda}/scripts/lessons/kit/figures/README.md` — the figure library, one example per figure
- `{Funda}/scripts/lessons/mathematics/grade-10/quizzes/src/01-exponents/build.mjs` — the
  approved example
- `~/.claude/skills/funda-lessons/references/maths.md` — maths in `$…$`, base TeX only
- past papers: `~/.claude/skills/funda-lessons/scripts/papers.py pull … --out
  {scratchpad}/papers-{your-folder}` (read-only library)

## Output

`{set}/quizzes/src/{NN-name}/build.mjs`, importing `../../../../../kit/quiz.mjs`, writing with
`writeQuiz(new URL('../../{topic-folder}/', import.meta.url), '<lesson file>' | '_topic', quiz({…}))`.
Deterministic: the same source builds the same bytes. Slot keys are permanent once loaded — name
them for the skill (`equate-exponents`), not the position.

## Before you finish

1. `node build.mjs` in your folder, then `node {Funda}/scripts/lessons/kit/check-quizzes.mjs {set}
   {topic-folder}` — clean (it runs the diagram checks too).
   Render your diagrams — `node {Funda}/scripts/lessons/kit/render-svgs.mjs {scratchpad}/png {set}/quizzes/{topic-folder}`
   (and `--dark`) — and Read the PNG of at least the first variant of every slot with one.
2. Re-work every answer and every distractor's claimed mistake. Then read every slot as a learner
   who skipped the lesson: if elimination of silly options or a clue in the stem gets the answer,
   rewrite it.
3. Report (short): quizzes written (file, slots, variants), exam-map lines with no slot and why,
   mistakes you found in lessons or memos, anything unsure.
