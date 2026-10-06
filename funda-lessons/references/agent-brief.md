# Agent brief — template

Write this once per run as `BRIEF.md` in the session scratchpad (not the repo), fill the `{…}` parts, and have every lesson
agent read it plus the four references it names. Agent prompts then stay short: identity, the
brief path, their topic(s), their source files, their output folder.

---

# Brief: {Grade} {Subject} lessons for Funda SA

You turn {source description — e.g. CAPS lesson notes in /…/FundaSA/senior-phase-subjects/…}
into lesson JSON that the Funda SA learner app renders, with diagrams. Readers are South African
{Grade} learners (about {age}).

## Hard rules (non-negotiable)

- Write ONLY your own source folder `{set}/src/{NN-name}/` and your topic folder(s)
  `{set}/{topic-folder}/`. Every other file in the Funda repo — including `lessons.config.json`,
  which the lead owns — is read-only to you. You may READ anything in the Funda and FundaSA repos.
- No git commands at all — no stash, checkout, restore, reset, clean, commit.
- Never write to the database, Valkey or any API (no psql writes, no curl POST/PATCH/PUT/DELETE).
- Never use a browser, the Browser pane or the iOS Simulator. Never sign in anywhere or type a
  password.
- Never download, generate or invent a photograph. Where a real photo is needed, use `photo()`
  (photos.md).
- Other agents work in sibling folders at the same time. Don't touch their folders.
- Teach only what the exam map says is examined, at its depth. Every lesson has an exam-style
  question with marks and a memo-style answer, cited to the paper it adapts.
- Past papers: read-only from `~/Documents/past papers` via `{skill}/scripts/papers.py pull … --out
  {scratchpad}/papers-{your-folder}`; crops go only to `{set}/photos/<id>.png` (photos.md).
- Diagram colours: kit inks and PAPER from `svg.mjs` only; a tint behind a label no stronger than
  `LABEL_TINT`; a strongly coloured labelled box is solid ink with a PAPER label (graphics.md).

## Read first

- `{set}/EXAM-MAP.md` — your topics' sections: what is asked, marks, must-know wording, mistakes, depth
- `{skill}/references/exam-alignment.md` — how lessons follow the exam
- `{skill}/references/house-style.md` — how a lesson reads (follow exactly)
- `{skill}/references/maths.md` — symbols in text and diagrams
- `{skill}/references/graphics.md` — what to draw, SVG rules, look at every diagram
- `{skill}/references/photos.md` — placeholders
- The block contract: `{Funda}/apps/admin-app/src/features/lessons/blocks/block-types.ts`
- {an approved example of the house style, if one exists — e.g. a previously accepted topic}

## Kit

`{Funda}/scripts/lessons/kit/` (import it from your build script as `../../../../kit/…`):
`blocks.mjs` (p, eq, h2, h3, ul, ol, section, callout, reveal, check, cards, figure, table,
working, photo, writePhotoRequests, image, r = String.raw — `**bold**` makes a bold run),
`svg.mjs` (palette GREY BLUE TEAL AMBER CORAL PURPLE PAPER, LABEL_TINT, + svg, text, line, dot,
polyline, polygon, path, rect, circle, arrowLine),
`mathsvg.mjs` (math, mathWidth, mathExtent, wordsMath), and the checks in pipeline.md.

## Output

- `{set}/src/{NN-name}/build.mjs` writes one JSON per lesson into `{set}/<topic-folder>/` (resolve
  it with `new URL('../../<topic-folder>/', import.meta.url)`) named `SS-LL-slug.json` (SS = source
  file number, LL = lesson within it), each `{ "title": "...", "blocks": [ ... ] }`, and calls
  `writePhotoRequests(<topic-folder path>)`. Deterministic: the same source builds the same bytes.
- `{set}/src/{NN-name}/manifest.json`: `[{ "topic", "file", "title", "sourceFile" }]`.
- These lessons go to production. File names are permanent once loaded (a lesson's id is keyed by
  its file name) — pick them carefully and don't rename them.

## How to split

One lesson = one idea, 5–8 minutes, ≤ 20 top-level blocks. {Topic-specific notes: e.g. which
source files to merge or split, which topic owns the introduction.}

## Before you finish

1. `node {Funda}/scripts/lessons/kit/build.mjs {set}` is the lead's; you run your own
   `node build.mjs`, then fit-viewbox, check-math, check-svg, check-contrast, validate on your
   folders — all clean.
2. render-svgs, then render-svgs --dark, and Read every PNG; fix what's weak.
3. photos.mjs for your folders.
4. Re-read every lesson as a {Grade} learner the week before the exam: could they answer each
   "How it is asked" line in your topics for full marks? Is anything there that no paper asks?
5. Report (short): lessons written (topic, file, title, block count, diagram count, photo
   requests and how many are cropped), exam-map lines you didn't cover and why, mistakes you
   found in the source or a memo and how you fixed them, anything you were unsure about.
