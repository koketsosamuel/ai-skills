---
name: funda-lessons
description: Write Funda SA lessons for any subject and grade, ready for production — plain-language, CAPS-aligned and exam-focused lesson sets (built from DBE exam guidelines and the owner's local past papers and memos, at the depth the papers ask) in the Funda repo (scripts/lessons) with typeset maths, accurate SVG diagrams drawn in code, grid tables, reveals and quickchecks, a "photo coming soon" placeholder wherever a real photograph is needed plus a list of photos for the owner to get, and a loader that is safe to run against production. Use whenever the user asks to create, write, rewrite, convert or improve lessons or lesson content for Funda / FundaSA (any subject — Mathematics, Physical or Life Sciences, Geography, History, Accounting, languages, technology subjects…), turn curriculum notes or CAPS material into lessons, add diagrams, graphics or photos to lessons, load lessons into a database or production, or fix how lesson maths or diagrams look on the phone.
---

# funda-lessons — notes → production-ready lesson sets

You write lessons for Funda SA, a learning app for South African school learners. A lesson is a
JSON array of content blocks (text, headings, lists, callouts, reveals, quickchecks, flashcards,
tables, svg diagrams, images) that the phone app, the website and the admin preview all render.

**Funda is a learning companion, not a school.** Learners have teachers and textbooks; we help
them pass tests and exams. Every lesson teaches what DBE papers actually ask, at the depth they
ask it, in the words the memo rewards — and no more. [references/exam-alignment.md](references/exam-alignment.md)
is how: the sources, the owner's local past-paper library, the exam map, and exam style in
lessons.

**Every lesson you write will be pushed to production later.** It lives in the Funda repo as a
*lesson set* (`scripts/lessons/<subject>/grade-<n>/`: source build scripts, built JSON, fixed ids)
and reaches production through `scripts/lessons/load.sh`, which never deletes and never
overwrites an admin's edit. Read the repo's `scripts/lessons/README.md` at the start of every
run — it is the contract, and it wins over this skill. The kit (`scripts/lessons/kit/`) and the
rules in `references/` were proven on the Grade 10 Mathematics set (133 lessons, 219 diagrams,
September 2026): everything in them fixes a bug someone actually saw on a phone.

## The loop

```
request → 1. INTAKE: subject, grade, topics, source, what production already has
        → 1b. EXAM MAP: guideline + 3 years of papers and memos → <set>/EXAM-MAP.md
        → 2. PLAN: the set's topics (fixed ids), lesson split from the exam map, who writes what
        → 3. WRITE: src/NN-name/build.mjs per group (you, or parallel opus agents)
        → 4. GRAPHICS: diagrams drawn in code; photo placeholders where reality is needed
        → 5. GATES: build, check-math, check-svg, check-contrast, validate, render light + dark + LOOK, photos, ids
        → 6. LOAD locally (lead only) → api-check → look on the phone
        → 7. HAND-OFF: report, photo list, production commands; commit only when asked
        → 8. QUIZZES: once the whole set is good, run the funda-quizzes skill on it
```

## Quizzes come next — write lessons with them in mind

Every lesson gets a quiz and every topic an exam-practice quiz, written by the `funda-quizzes`
skill **after** this skill has finished and checked the whole set (never while lessons are still
changing). When the owner asks for a subject and grade, finish the lessons first, then run
`funda-quizzes` on the set unless they say otherwise. What that skill relies on from you:

- `EXAM-MAP.md` complete for every topic: its quiz questions trace to "How it is asked", and its
  wrong answers come from "Common mistakes" — write those lines concretely (the wrong result a
  learner gets, not just "sign errors").
- Permanent lesson file names and ids: a lesson quiz has the lesson's file name and an id derived
  from the lesson's id. A renamed lesson file keeps its id; its quiz file is renamed with it.
- Descriptive, stable headings (`Worked example 2`, `The two new rules`): quiz questions name them
  as the part of the lesson to re-read. Renaming a heading breaks those anchors (the quiz check
  catches it).
- Quickchecks and worked examples stay in the lesson; quizzes practise the same skills with new
  questions, so keep lesson practice short and let the quiz carry the drill.

## 1. Intake

Find out, asking only what the repo and sources can't tell you:

- **Subject, grade, topics.** Topic list and teaching order come from CAPS. The FundaSA repo
  (`~/Documents/GitHub/FundaSA`: `senior-phase-subjects/<subject>/grade-NN/`,
  `curriculum-sources/`) holds per-topic notes and CAPS documents — check
  `curriculum-audit-tracker.md` there before trusting a note; the audit has found errors.
- **What production will have.** Production's grades, subjects, paper categories and broad topics
  come from the curriculum loader (`scripts/insert-*.sql`). Use their exact names. If your topics
  split or rename the broad ones, they go in `replacesTopics` — and that changes what learners
  see, so confirm with the owner.
- **Existing sets and lessons.** Extending a set keeps every existing file name and id. Replacing
  lessons learners may already have progress on is the owner's call.
- **Source**: FundaSA notes, the owner's material, or CAPS alone. You are the checker — fix
  mistakes in the source and list them in the report. FundaSA notes are often deeper than the
  papers need: cut to the exam map, don't transcribe.
- **Exam sources**: the newest Examination Guideline and the last three years of papers and memos
  for the grade, from the owner's library via `scripts/papers.py` (exam-alignment.md). For a big
  set, one `opus` research agent per paper reads them and drafts its topics' exam-map sections.

## 1b. Exam map

Write `<set>/EXAM-MAP.md` before planning lessons (exam-alignment.md has the shape): per topic, the
paper and marks, how it is asked (with paper references), what must be known word for word, how
the memo awards marks, common mistakes, what is not examined, and the depth ceiling. It is the
brief for every lesson and stays in the set for the next run.

## 2. Plan

- The set's `lessons.config.json`: grade, subject, `publish`, `replacesTopics`, and topics in
  CAPS order, each with a fixed UUID, folder, name, description, icon, paper (`category`) and
  term/week `pacing` where CAPS gives one. Lesson ids are added by `--assign-ids`.
- One lesson = one idea (5–8 minutes, ≤ 20 top-level blocks). A topic opens with a short
  introduction lesson and closes with an exam-practice lesson. Every lesson traces to a "How it
  is asked" line in the exam map; cut what doesn't. Lean: fewer, tighter lessons beat covering
  every CAPS bullet. File names (`SS-LL-slug`) are permanent once loaded — choose them well.
- Decide graphics per lesson up front: which ideas get a diagram, which need a real photo.
- **More than ~6 lessons → fan out** to `opus` agents (lesson writing and diagram judgement are
  never downgraded), one per `src/NN-name/` folder and its topic folder(s). Write the brief once
  from `references/agent-brief.md`; restate the hard rules in every prompt, because agents skip
  rules they only read about: write only their own `src/` and topic folders, no git, no DB/API
  writes, no Browser or Simulator, no sign-ins, no downloaded or invented photos. Make each prompt
  `cd` to and verify its folder. Run agents in the background; don't duplicate their work.

## 3–4. Write and draw

Follow, exactly:

- [references/exam-alignment.md](references/exam-alignment.md) — depth, command words, marks,
  exam-style questions, past-paper sources.
- [references/house-style.md](references/house-style.md) — voice, lesson shape, worked
  examples, definitions, reveals, quickchecks, callouts, tables.
- [references/maths.md](references/maths.md) — every symbol in `$…$` (maths, chemistry,
  physics units), base TeX only in text; `math()` / `wordsMath()` for diagram labels.
- [references/graphics.md](references/graphics.md) — draw vs photograph, SVG rules the phone
  enforces, accuracy, a per-subject catalogue of diagrams worth drawing.
- [references/photos.md](references/photos.md) — `photo()` placeholders, cropping real images
  from past papers, never fetching or generating one, and how an uploaded photo comes back.

Build scripts are the source of truth and must be deterministic (same source, same bytes); never
hand-edit built JSON.

## 5–6. Gates, load, look

All in [references/pipeline.md](references/pipeline.md), including the production rules that
shape the writing (ids are forever, nothing is deleted, no moving lessons between topics, admin
edits win). Every gate clean, every diagram rendered and **looked at**, then load into the LOCAL
database with `load.sh`, run `api-check.mjs`, and check on the iOS Simulator. If the app wants a
sign-in, ask the owner — never enter credentials.

**Never load into production yourself.** That is the owner's step with their credentials; give
them the exact commands.

## 7. Report

Short, to the owner:

- The set path, lessons per topic, diagrams, tables.
- Exam coverage: the papers read, and any exam-map line no lesson covers (or why it was left out).
- Mistakes found in the source notes and how you fixed them; anything unsure or unverified.
- **Photos needed**: count (and how many are already cropped into `photos/`), which lessons, the path to `IMAGES-NEEDED.md`, that those lessons stay
  hidden until the photos are in, and that you'll wire the photo URLs into the source once they're
  uploaded in production.
- **Production**: what the load will do there (topics added or hidden, lessons inserted live or
  hidden) and the commands — `--dry-run` first, then the load with `VALKEY_URL`, then
  `api-check.mjs` against the production API.
- Nothing committed unless the owner asked.
- Next: the set's quizzes with `funda-quizzes` (or why not yet).

## Repo rules that bind this skill

The Funda repo's `CLAUDE.md` wins over this skill. In particular: never `git stash`, `checkout
-- .`, `restore .`, `reset --hard` or `clean`; never commit while other agents are writing; no
lint/type suppressions; comments explain why, never what. If the work exposes a renderer or
sanitizer bug (it has, three times), fix it in the repo with a test and record the trap in the
matching `docs/decisions/` file or `packages/database/src/seeds/content/AUTHORING.md`.
