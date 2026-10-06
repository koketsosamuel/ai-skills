# Question craft — exam-aligned questions and their variants

A quiz question earns its place only if it practises something a paper asks, in a form close to
how the paper asks it, and teaches the learner something when they get it wrong.

## What the app does with a question

- **Slot** = one question position in a quiz. It holds 2+ **variants** (one variant group). The
  first variant is linked; the API serves each learner unseen variants first, so a retake gets a
  new variant of every slot. Variants must share the question type and topic (the API drops any
  that don't).
- **Difficulty** sets the FP a correct answer pays: easy 1, medium 2, hard 3, legendary 5. The
  quiz's difficulty is the most common one among its slots; its clock is the sum of slot times.
- Options are **shuffled** (except True/False). Never write "all of the above", "A and B", "option
  C".
- On review the learner sees: whether they were right, the `feedback` of the option they picked,
  the `explanation`, the `solution` (worked, memo-style), and — for a lesson quiz — a link back to
  the lesson labelled with the slot's `anchor`. `objective` is admin-only: put the exam-map line
  and paper reference there.

## Difficulty = cognitive level

Use the level the exam guideline would give the same question, not how hard it feels:

| Difficulty | Cognitive level (Maths / Sciences wording) | Typical form | Seconds |
| --- | --- | --- | --- |
| easy | Knowledge / recall; 1-mark steps | define, identify, one law | 30–45 |
| medium | Routine procedures; 2–3 marks | a standard method, one or two steps | 45–120 |
| hard | Complex procedures; 3–4 marks | several laws or steps chained | 90–180 |
| legendary | Problem solving; non-routine | unfamiliar context, reasoning | 180–300 |

Time a slot at about the exam's own rate for the marks it stands in for (Mathematics papers run at
roughly 1.2 minutes per mark), plus reading time. Don't reward speed: nothing in scoring does.

A lesson quiz runs easy → hard. A topic quiz matches the topic's spread in recent papers (for
Mathematics roughly 20% knowledge, 35% routine, 30% complex, 15% problem solving), and uses
legendary only where the papers really set non-routine questions on that topic.

## Types — pick the one the exam skill needs

- **choice** (4 options, one right): the default, and the form of Section A multiple choice in the
  papers. Use it for any answer that is an expression, a fraction, a root, a sentence or a unit.
- **select** (4–6 options, 2+ right, "Pick all that apply."): classification and "which of these
  are…" questions. Graded all-or-nothing, so keep it to 2–3 correct.
- **trueFalse**: a statement that tests one misconception. Variants may flip the truth value —
  a slot whose variants are all "False" teaches learners to guess.
- **number / word** (typed): **only** a single word, or a plain number — whole, or at most two
  decimal places (`number(text, value, { decimals, rounded })`, `word(text, words)`). Never a
  fraction, root, expression, unit or "x = …": those are choice questions. The helpers end the
  question with the exact instruction ("Type an integer.", "Round to two decimal places and
  type the number.", "Answer in one word.") and list every accepted form (−/-, comma/point,
  1 024/1024). Put units in the question ("How many metres…?"). For `word`, list every accepted
  spelling (British and common variants).

## Exam alignment

- Each slot's `objective` names the exam-map line and, where the slot adapts a real question, the
  paper: "Equate exponents and solve — Nov 2018 P1 Q2.1.3 (3 marks)". Adapt: new numbers, same
  shape. Check your answer against the memo's method, and check the memo too (memos have errors).
- Command words mean what the guideline says. "Define" questions quote the guideline wording in
  the right option; distractors are the near-misses learners write (missing a condition, wrong
  quantity).
- Multi-step paper questions become either a **typed** final answer (when it is a plain number) or
  a **choice** between the right result and the results of the common wrong steps. The
  `solution` shows the memo's marks, one ✓ per marked step: `$27 = 3^3$ ✓ · $2x + 1 = 3$ ✓ · $x = 1$ ✓`.
- Formula-sheet subjects: use the sheet's symbols and form. Tell the learner in the question when
  a value must be read or derived that the sheet gives.
- Cover the exam map, not the lesson's paragraphs. A lesson quiz that only asks recall is wasted:
  at least half its slots should be medium or harder when the papers ask the idea at that level.

## Typed numbers: say exactly how to get the keyed value

A typed answer is compared exactly, so the question must remove every legitimate alternative:

- Rounding: say how many decimals (the helper does), and add "Round only at the end." wherever
  rounding a step first changes the answer.
- π: "Use the π key on your calculator." whenever π is involved; 3.14 gives a different answer.
- Method: where Grade 10 methods differ (quartiles with or without the median, percentile
  positions $\frac{k}{100}(n + 1)$ versus $\frac{k}{100}n$), say which one the question uses.
- Given facts: say "a fair coin", "a standard deck of 52 cards", which faces of a solid are open.

## Maths that fits a phone

The app shrinks a formula wider than the screen until it fits, so a long one becomes unreadable.
`writeQuiz` splits a chain `$a = b = c$` into `$a = b$ $= c$` automatically; anything else wider
than about 48ex fails `check-quizzes`. Write one step per formula, and plain numbers (a long sum
of data values) as plain text, not maths.

## Diagrams

Papers print a figure beside most geometry, trigonometry, measurement, functions, analytical
geometry, statistics and probability questions, because learners reason from what they see. Do the
same: a quiz question gets a diagram wherever the paper's version of it has one, or where a learner
would sketch one to start (a cone's radius, height and slant height; the triangle a sine-rule
question describes).

- Draw it from the variant's own numbers with `kit/figures/` (never a fixed lesson figure with
  other numbers in the text). Each variant has its own diagram; the diagram and the text must agree
  exactly — same letters, values, units.
- Show what the paper shows: the givens, the letter or "?" for the unknown, right-angle marks,
  equal-side ticks, parallel arrows. Never label the answer, and never draw something that gives it
  away (a length drawn to scale when the question asks "estimate from the drawing" is fine; a
  labelled answer is not).
- Keep the words sufficient on their own for a screen reader: the question still states every
  given the learner needs, and says "in the diagram" where it refers to the figure.
- A past paper's figure is redrawn with `kit/figures/` from the variant's numbers — never a crop of
  the paper (it fits one set of numbers, stays light in dark mode and blurs on a phone). A skill
  whose figure can't be drawn (a photograph, a map) is left out and listed in the report.
- Graph-reading and figure-based skills that were left out for want of a picture are now in scope:
  read intercepts, turning points, asymptotes and values off a drawn graph; name the circle theorem
  that gives an angle; read a quartile off an ogive; fill a Venn region.
- "Which graph…?" questions: draw the candidates in one diagram labelled A–D, and make the options
  "Graph A" … "Graph D" (options are shuffled, labels in the figure are not).
- `check-quizzes` runs the lesson diagram checks on every quiz diagram (what the phone parses and
  the API keeps; labels readable in light and dark). LOOK at your diagrams:
  `node <kit>/render-svgs.mjs [--dark] <png-dir> <set>/quizzes/<topic>` and Read the PNGs.

## Fit one screen

A learner should see the question, its diagram and every option without scrolling — the owner
wants a scroll during a quiz to be rare.

- **Stem**: the givens, then the ask, in as few sentences as the maths allows. No story preamble
  and no restating what the diagram already shows beyond the givens a screen reader needs.
- **Options**: short. When every option is ≤ 14 characters (a TeX command counts as one; spaces,
  braces, `^`, `_` and `$` count nothing) the app sets them two to a row. Put shared units or words
  in the stem ("in cm²") rather than in every option, and prefer the bare result (`$32\pi$`) to a
  sentence. Long options are fine when the skill needs a sentence (a reason, a theorem) — then
  keep all four similar in length.
- **Diagrams**: wide rather than tall (the app caps a diagram at about a third of the screen height
  and shrinks a tall one until labels get small); nothing in the figure the question doesn't use;
  tight margins.
- Check a diagram question and a four-option question on the phone before calling a topic done.

## Wrong options are diagnoses — never jokes

Every wrong option is the answer a learner gets from a real mistake — from the exam map's
"Common mistakes", the answers the memo rejects, or diagnostic reports — not a random number and
not a filler sentence.

- **The plausibility test**: could a learner who studied a bit, but not enough, pick it?
  If only someone who never opened the lesson would, cut it. Silly options make a question free:
  the learner eliminates three and is "right" without the knowledge. Banned, all seen in a real
  run (Geography, October 2026):
  - absurd causes or effects: "Coal regrows quickly", "Workers become a renewable fuel",
    "Loan repayments block sunlight", "Power cuts make the Earth rotate faster",
    "Illness is impossible after rain", "The clear eye keeps all land dry";
  - options that contradict what every learner already knows (the sun rises in the west, rivers
    flow uphill), or that no textbook or memo would ever say;
  - "no reason", "nothing happens", "it is random", "none of these" fillers;
  - the opposite-direction twin of the answer used as the only alternative ("Coriolis
    strengthens" beside "Coriolis weakens") when the other two options are filler.
- **Good distractors in content subjects** (Geography, Life Sciences, History, Business…) are:
  a true fact that answers a different question (a cause offered for an effect, a feature of the
  neighbouring landform, the other hemisphere's rule); a half-right answer the memo gives no
  mark for (missing the condition, too vague); a confused term (relative vs absolute humidity,
  epicentre vs focus); the right idea for the wrong place, season or scale.
- **All options look alike**: same kind of answer (four causes, four places, four numbers), same
  grammar, similar length and tone, equally specific. The right one must not be the only long,
  careful or hedged option, nor the only one using the lesson's key term.
- `feedback` (required on every wrong option): name the mistake and the fix in one or two
  sentences a 15-year-old understands. "You multiplied the exponents. When you multiply powers
  with the same base, add them." If the only honest feedback is "this is not true", the option
  is not a mistake anyone makes — replace it.
- `tag`: a short kebab-case name for the mistake (`added-coefficients`,
  `negative-exponent-negative-answer`). Reuse the same tag for the same mistake across slots and
  variants: the admin's analytics group wrong answers by it.
- No option may be right by another reading of the question.

## The stem never gives the answer

- Don't state a value the question then asks for ("Utility A's reliability is 88%. Which utility
  is 88% reliable?"), name the answer's term in the stem, or describe it so closely that matching
  words picks it ("the height above sea level marked by a trig beacon… What does a trig beacon
  show?").
- Don't let grammar give it away ("an …" with only one option starting with a vowel; a plural
  stem with one plural option).
- **Elimination test**: cover the lesson and try to answer from the stem and options alone, with
  only general knowledge and reading skill. If you can, rewrite the slot.

## Real content, not invented scenarios

Exam papers in content subjects ask about real places, case studies and data. So do quizzes:

- Knowledge and explanation questions use the real South African (and guideline-named world)
  examples the lesson teaches: named rivers, cities, industries, dates, case studies. Use only
  facts the lesson states or the exam map cites — a quiz never introduces an unverified fact.
- "Town A / Site 2B / Utility X" framing is for skills that really work on any data: a
  calculation, reading a map, graph or synoptic chart, interpreting a given table. Even then, a
  real SA setting reads better.
- A case-study lesson's quiz tests that case study's facts (a quiz on Cyclone Idai names Idai,
  Beira, Mozambique, the dates and effects the lesson teaches).

## Every quiz is new questions

- A topic quiz and an exam-practice lesson's quiz are not copies of the lesson quizzes' slots.
  Reuse a skill, never a stem: new numbers, a new place, a new extract. Aim for no verbatim stem
  shared between two quizzes; the review step checks (pipeline.md).
- Never copy a lesson's quickcheck or worked example.

## Variants

Two variants are two sittings of the same exam question:

- Same skill, same number of steps, same difficulty and time, same traps. Change the numbers,
  the base, the variable letters, the context (a different taxpayer, a different circuit). If V1
  asks for a definition, V2 asks for the same definition's application or a sibling definition at
  the same level — not a different idea ("shedding" in V1, "routine repair" in V2 is two skills).
- Different answer. A learner who remembers variant A's answer must still have to work B.
- The same misconception family in the wrong options, with the same tags.
- Not a harder or easier question in disguise: if one variant needs an extra step, rebalance.
- Written independently: check each variant's answer by working it from scratch.
- **A different outcome, not just different numbers.** If every variant's answer is "Yes",
  "isosceles" or "parallelogram", a retake is a guess. Make one collinear and one not, one
  isosceles and one right-angled; `check-quizzes` notes a slot whose variants share an answer.
  Only a theorem-fixed answer ($P(A \text{ and } B) = 0$ for mutually exclusive events) may repeat.

## Copy

Plain language, short sentences, sentence case. "Simplify…", "Solve for $x$:…", "Which…?".
Read every stem aloud once: subject–verb agreement ("Which latitude do the first two digits
show?"), singular/plural with numbers ("1 landfall"). Use the papers' formats: scales as
"1 : 50 000", and only the scales the papers use (SA topographic maps 1 : 50 000, orthophotos
1 : 10 000).
Tell the learner what form the answer takes ("Give your answer with positive exponents.").
South African context and spelling (rand as R, decimal comma accepted, metres, colour). Rewards:
"FP" beside a number, "Funda Points" in words — never "points" or "XP". Never promise a result
("this will be in your exam"); "Paper 1 asks this every year" is fine.
