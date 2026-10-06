---
name: funda-quizzes
description: Write Funda SA quizzes for finished lesson sets, ready for production — one quiz per lesson (the lesson's checkpoint) and one exam-practice quiz per topic, every question with at least two variants the app rotates between attempts, built from the set's exam map and the owner's past papers and memos so a learner who passes them can pass their June, November and Feb/March exams. Quizzes live beside the lessons in the Funda repo (scripts/lessons/<subject>/grade-<n>/quizzes), are checked by the kit, and load through the same production-safe loader. Use whenever the user asks to create, write, add, extend, fix or load quizzes, questions, question variants, checkpoints or exam practice for Funda / FundaSA lessons (any subject and grade), or right after the funda-lessons skill has finished and checked a set.
---

# funda-quizzes — finished lessons → exam-ready quizzes

You write quizzes for Funda SA, a learning app for South African school learners. Funda is a
learning companion, not a school: the point of every quiz is that a learner who passes it can
answer the same kind of question for full marks in a real exam — the June and November papers,
and the Feb/March supplementary papers, which cover November's scope.

**This skill runs after `funda-lessons`.** The owner asks for lessons for a whole subject and
grade; `funda-lessons` writes the set, its exam map, and checks every lesson. Only when the lessons
are good does this skill write their quizzes. Never write quizzes for lessons that are still being
written or have not passed the lesson gates — a lesson rewrite would orphan the quiz's anchors and
questions. If the owner asks for lessons *and* quizzes in one go, run `funda-lessons` to the end
first, then this skill.

What `funda-lessons` hands you (and what you rely on):

- `<set>/EXAM-MAP.md` — per topic: how it is asked, marks, must-know wording, memo marking,
  common mistakes, depth. **Every quiz question traces to a "How it is asked" line; every wrong
  option comes from a "Common mistakes" line.** If the set has no exam map (older sets), write the
  topics' sections first, from the papers, exactly as `funda-lessons`'
  `references/exam-alignment.md` describes, and add them to the set's `EXAM-MAP.md`.
- Lesson files with permanent names and ids in `lessons.config.json`. A lesson quiz's file has the
  **same name** as its lesson, and its id is derived from the lesson's id.
- Lesson headings, which your questions name as their `anchor` ("re-read this part").
- Each topic's exam-practice lesson (reveals with memo answers). Quizzes practise the same skills
  with new questions; never copy a lesson's quickchecks or worked examples.

## The loop

```
request → 1. INTAKE: which set/topics; lessons finished and loaded? exam map present?
        → 2. PAPERS: re-read the topics' exam-map sections and the papers they cite
        → 3. PLAN: per lesson 4-6 slots, per topic 8-12; each slot = a skill + difficulty + marks
        → 4. WRITE: <set>/quizzes/src/NN-name/build.mjs (you, or parallel opus agents)
        → 5. GATES: build-quizzes, check-quizzes, verify every answer by working it
        → 6. LOAD locally (lead only) → quiz-api-check (--play) → look on the phone
        → 7. HAND-OFF: report and production commands; commit only when asked
```

## 1. Intake

- Read the Funda repo's `scripts/lessons/README.md` (the "Quizzes" section is the contract; it
  wins over this skill) and `docs/decisions/quiz-attempts.md` (variants, attempts, first try).
- Which set and topics. Check the lessons pass the lesson gates and are loaded locally (a lesson
  quiz needs its lesson in the database).
- What already exists: `<set>/quizzes/` sources (extend them, keep every slot key), and quizzes
  made in the admin for these lessons (the loader skips a lesson that already has one — tell the
  owner).

## 2–3. Papers and plan

Past papers are in the owner's local library; use `funda-lessons`' helper
(`~/.claude/skills/funda-lessons/scripts/papers.py pull <subject> <grade> --from <year> --out
<scratchpad>/papers`). Grades 10–11 have fewer national papers than Grade 12: go back further
and include the common/provincial papers.

Plan each quiz as a list of slots before writing any question. For each slot: the exam-map line,
the paper reference, the marks it stands in for, the cognitive level (→ difficulty), the type, and
the misconceptions its wrong options will use. [references/question-craft.md](references/question-craft.md)
has the rules — read it every run.

- **Lesson quiz** (4–6 slots, pass 75%): only what that lesson teaches, at the depth the papers
  ask, easy → hard. Its title is the lesson's title, exactly — `writeQuiz` sets it.
- **Titles never say "quiz"** (the owner finds "…: quiz" horrible; the app already shows it as
  a quiz). Don't pass `title` to `quiz()`: `writeQuiz` names a lesson quiz after its lesson and a
  topic quiz `<topic>: topic test`, and `check-quizzes` fails any title containing "quiz".
- **Topic quiz** (`_topic`, 8–12 slots, pass 70%): the topic as the paper asks it — same spread
  of cognitive levels and question types as the topic's section of a recent paper, including the
  full multi-step questions, adapted and cited.
- **No silliness.** Every wrong option is a mistake a half-prepared learner really makes — never
  an absurd, joke or filler option a learner can eliminate without knowing the work; the stem
  never gives the answer away; knowledge questions use the real places and case studies the
  lesson teaches. A Geography run (October 2026) had correct answers but dozens of free
  questions ("Coal regrows quickly"): question-craft.md lists what to avoid.
- **Two variants minimum, every slot, no exceptions.** Three for a slot learners will retake a
  lot (the core skill of the topic). Variants are the same skill, same steps, same difficulty and
  time, with different numbers or context — see question-craft.md.

## 4. Write

The kit is `<Funda>/scripts/lessons/kit/quiz.mjs`: `quiz`, `slot`, `choice`, `select`,
`trueFalse`, `number`, `word`, `right`, `wrong`, `writeQuiz`, `r`. A source file writes one topic's
quizzes (the Grade 10 Mathematics Exponents source, `mathematics/grade-10/quizzes/src/01-exponents/build.mjs`,
is the approved example — read it first).

Maths uses the lesson rules: every symbol in `$…$`, base TeX only (funda-lessons'
`references/maths.md`). **Diagrams**: give a question the figure the paper would print beside it —
a solid with its dimensions, a triangle with its sides and angles, a circle-theorem figure, a graph,
an ogive, a Venn or tree diagram, a number line. Pass `diagram:` (an SVG string) in a variant's
extras, drawn from that variant's own numbers with the parametric library
`<Funda>/scripts/lessons/kit/figures/` (its README lists every figure). A figure in a past paper
is **redrawn** this way, never cropped in: a crop fits one variant's numbers, doesn't theme for
dark mode and blurs on a phone. The rules are in question-craft.md, "Diagrams".

**Fit one screen.** The owner wants a scroll during a quiz to be rare: the question, its diagram
and every option should fit on a phone at once. Keep stems short (givens, then the ask — no
preamble), keep options short so they sit two to a row (the app grids options when every one is
≤ 14 characters, a TeX command counting as one), and draw diagrams wide rather than tall (the app
caps a diagram at a third of the screen height). question-craft.md, "Fit one screen".

**More than ~3 topics → fan out**, one job per `quizzes/src/NN-name/` folder (pair small topics,
split a topic over ~12 lessons), with the brief from [references/agent-brief.md](references/agent-brief.md).
The owner's preferred split to save tokens: `sonnet` agents write, and one `opus` reviewer per job
re-works every answer and distractor, replaces any silly or giveaway option (pipeline.md,
"Review every slot for silliness"), checks each diagram against its text, and fixes the source —
run as a Workflow `pipeline()` (write → review) when the owner has asked for a multi-agent run. If
a run is cut off, finish the failed jobs with a fresh script; resuming a pipeline can re-run every
completed review. Restate the hard rules in
every prompt (agents skip rules they only read about): write only their own quiz source and topic
quiz folders, no git, no DB/API writes, no Browser or Simulator, no sign-ins. Run them in the
background; don't duplicate their work.

## 5–6. Gates, load, check

All in [references/pipeline.md](references/pipeline.md). In short: `check-quizzes` clean, every
answer worked out by hand (the checker can't know maths is wrong — an agent's arithmetic is the
most likely bug), every diagram rendered and looked at (`render-svgs.mjs`, light and dark), load
locally with `load.sh <set> --quizzes`, then `quiz-api-check.mjs --play` as a local test learner
(it also checks every served diagram), then look at a diagram question and a four-option question
on the iOS Simulator if the owner is signed in there — do they fit one screen? (ask before signing
in; never type a password).

**Never load into production yourself.** Give the owner the commands.

## 7. Report

Short, to the owner: quizzes per topic, slots and variants; exam-map lines with no slot (and
why); mistakes found in lessons or memos; what the production load will do
(quizzes go live with their lessons — there is no quiz on/off switch); the production commands;
nothing committed unless asked.

## Repo rules that bind this skill

The Funda repo's `CLAUDE.md` wins: never `git stash`, `checkout -- .`, `restore .`, `reset --hard`
or `clean`; never commit while other agents are writing; learner copy in plain language a
15-year-old understands; rewards are "FP" / "Funda Points", never "points" or "XP"; never promise a
result. If the work exposes an API or app bug, fix it in the repo with a test, or flag it to the
owner if it is out of scope.
