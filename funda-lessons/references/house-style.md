# House style — how a Funda lesson reads

Learned from the product owner's feedback on the Grade 10 Mathematics rewrite (133 lessons,
September 2026). Follow it exactly; it is what "good" means here.

## Voice

- Plain language a 15-year-old understands. Short sentences, direct verbs, sentence case.
- Explain every term the first time it appears. Use the CAPS term (factorise, photosynthesis,
  hydrological cycle, ledger, figure of speech) and say what it means.
- Tell the learner what happened and what to do next. No idioms, no filler ("Let's dive in",
  "In this exciting lesson"), no hype, no claims the app cannot guarantee.
- South African context and spelling: rands (R250, R1 250.50), the decimal point (0.75, never a
  comma), metric units, SA places, names and examples. Coordinates use the semicolon: (2; 3).
- Accurate. You are the checker: if the source notes contain a mistake, fix it and report it.

## Shape of a lesson

- One lesson = one idea a learner finishes in 5–8 minutes. Split a long source into 2–4
  lessons; keep a short one whole. Aim for ≤ 20 top-level blocks (the editor suggests splitting
  past 20).
- Title: short, sentence case, plain ("Solving exponential equations", "How osmosis works").
  No "Lesson 3:" prefixes. Don't open with a heading that repeats the title — the app drops it.
  Open with a paragraph that says why this matters.
- `h2` for main sections, `h3` inside them.
- A topic's first lesson (the introduction) hooks with a real-life example, lists what the
  learner will be able to do (outcomes, not lesson titles), and has 2–3 quickchecks on the
  prior-grade knowledge they need.

## Teaching blocks

- **Worked examples**: under an `h3` "Worked example 1". One step per paragraph ("Step 1: …").
  Show EVERY operation — what you multiply by, what you subtract, which rule you used, which
  source line a fact comes from. A learner must never wonder where a number came from.
- **Definitions**: a bullet list with a bold term — `'**Osmosis**: water moving …'`. No `card`
  blocks. Bold and `$maths$` cannot share a block (the maths wins, the bold is lost): keep the
  bold item in words and put the maths in a child item.
- **Every lesson** has at least one `reveal` ("Try it yourself: …", the full answer inside)
  and 1–3 `quickcheck`s with exactly one correct option and an explanation that teaches (why
  the right answer is right, what the tempting wrong one gets wrong).
- **Multi-part prompts** put each part on its own line with real newlines:
  `'Try it yourself: solve these.\na) $9^x = 27$\nb) $4^{x-1} = 8^x$'`.
- **Callouts** sparingly (≤ 2–3 per lesson): `warning` for a common mistake, `tip` for a
  shortcut, `info` for context. Never decoration.
- **Tables** of values, comparisons, vocabulary or data use the `table` block (grid of cells,
  `$…$` allowed, 1–20 rows, 1–10 columns). Never a TeX `array` pretending to be a table.
- **Flashcards**: at most one set per topic, as an end-of-topic recap in its last lesson.
- **Diagrams** wherever a picture teaches faster than words — see graphics.md. **Photos**
  where only reality will do — see photos.md.

## Copy rules the whole product enforces

- Funda Points: `FP` beside a number, "Funda Points" in labels — never points/pts/XP. Funda
  Bucks likewise `FB`. Lessons rarely need either.
- Reward, privacy and eligibility wording stays faithful to the feature rules; lessons don't
  promise rewards.
