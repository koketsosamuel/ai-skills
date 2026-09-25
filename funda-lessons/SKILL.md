---
name: funda-lessons
description: Write Funda SA lessons for any subject and grade, ready for production — plain-language, CAPS-aligned lesson sets in the Funda repo (scripts/lessons) with typeset maths, accurate SVG diagrams drawn in code, grid tables, reveals and quickchecks, a "photo coming soon" placeholder wherever a real photograph is needed plus a list of photos for the owner to get, and a loader that is safe to run against production. Use whenever the user asks to create, write, rewrite, convert or improve lessons or lesson content for Funda / FundaSA (any subject — Mathematics, Physical or Life Sciences, Geography, History, Accounting, languages, technology subjects…), turn curriculum notes or CAPS material into lessons, add diagrams, graphics or photos to lessons, load lessons into a database or production, or fix how lesson maths or diagrams look on the phone.
---

# funda-lessons — notes → production-ready lesson sets

You write lessons for Funda SA, a learning app for South African school learners. A lesson is a
JSON array of content blocks (text, headings, lists, callouts, reveals, quickchecks, flashcards,
tables, svg diagrams, images) that the phone app, the website and the admin preview all render.

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
        → 2. PLAN: the set's topics (fixed ids), lesson split, who writes what
        → 3. WRITE: src/NN-name/build.mjs per group (you, or parallel opus agents)
        → 4. GRAPHICS: diagrams drawn in code; photo placeholders where reality is needed
        → 5. GATES: build, check-math, check-svg, validate, render + LOOK, photos, ids
        → 6. LOAD locally (lead only) → api-check → look on the phone
        → 7. HAND-OFF: report, photo list, production commands; commit only when asked
```

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
  mistakes in the source and list them in the report.

## 2. Plan

- The set's `lessons.config.json`: grade, subject, `publish`, `replacesTopics`, and topics in
  CAPS order, each with a fixed UUID, folder, name, description, icon, paper (`category`) and
  term/week `pacing` where CAPS gives one. Lesson ids are added by `--assign-ids`.
- One lesson = one idea (5–8 minutes, ≤ 20 top-level blocks). A topic opens with a short
  introduction lesson. File names (`SS-LL-slug`) are permanent once loaded — choose them well.
- Decide graphics per lesson up front: which ideas get a diagram, which need a real photo.
- **More than ~6 lessons → fan out** to `opus` agents (lesson writing and diagram judgement are
  never downgraded), one per `src/NN-name/` folder and its topic folder(s). Write the brief once
  from `references/agent-brief.md`; restate the hard rules in every prompt, because agents skip
  rules they only read about: write only their own `src/` and topic folders, no git, no DB/API
  writes, no Browser or Simulator, no sign-ins, no downloaded or invented photos. Make each prompt
  `cd` to and verify its folder. Run agents in the background; don't duplicate their work.

## 3–4. Write and draw

Follow, exactly:

- [references/house-style.md](references/house-style.md) — voice, lesson shape, worked
  examples, definitions, reveals, quickchecks, callouts, tables.
- [references/maths.md](references/maths.md) — every symbol in `$…$` (maths, chemistry,
  physics units), base TeX only in text; `math()` / `wordsMath()` for diagram labels.
- [references/graphics.md](references/graphics.md) — draw vs photograph, SVG rules the phone
  enforces, accuracy, a per-subject catalogue of diagrams worth drawing.
- [references/photos.md](references/photos.md) — `photo()` placeholders, why Claude never
  fetches or generates a photo, and how an uploaded photo comes back into the source.

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
- Mistakes found in the source notes and how you fixed them; anything unsure or unverified.
- **Photos needed**: count, which lessons, the path to `IMAGES-NEEDED.md`, that those lessons stay
  hidden until the photos are in, and that you'll wire the photo URLs into the source once they're
  uploaded in production.
- **Production**: what the load will do there (topics added or hidden, lessons inserted live or
  hidden) and the commands — `--dry-run` first, then the load with `VALKEY_URL`, then
  `api-check.mjs` against the production API.
- Nothing committed unless the owner asked.

## Repo rules that bind this skill

The Funda repo's `CLAUDE.md` wins over this skill. In particular: never `git stash`, `checkout
-- .`, `restore .`, `reset --hard` or `clean`; never commit while other agents are writing; no
lint/type suppressions; comments explain why, never what. If the work exposes a renderer or
sanitizer bug (it has, three times), fix it in the repo with a test and record the trap in the
matching `docs/decisions/` file or `packages/database/src/seeds/content/AUTHORING.md`.
