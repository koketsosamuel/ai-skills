# Exam alignment — teach what the papers ask, at the depth they ask it

Funda is a **learning companion**, not a school. Learners already have a teacher, a textbook and a
classroom. Our job is to help them pass their tests and exams: explain the examinable core
clearly, show exactly how it is asked and marked, and give them practice. Anything a paper never
asks is out of scope, however interesting.

## Sources, in order of authority

| Source | Tells you | Where |
| --- | --- | --- |
| **CAPS** | what content exists for the grade | `FundaSA/curriculum-sources/` (`*-caps*.txt`) |
| **ATP** (Annual Teaching Plan) | term/week order, formal assessment tasks per term | `FundaSA/curriculum-sources/senior-phase/atp-*` |
| **Examination Guidelines** (Gr 10–12) | what is examinable and what is not, papers and marks per topic, cognitive-level weights, the exact wording of definitions and laws learners must know, the data/formula sheet | the local library (below, `papers.py guide`), or `FundaSA/curriculum-sources/*-exam-guidelines-*` |
| **Past papers + memos** | how questions are worded, how marks are split, which topics come up every year | the local library (below) |
| **NSC Diagnostic Reports** (Gr 12) | the mistakes learners actually make, per question | DBE website |

Where the guideline and CAPS disagree about what is examined, **the guideline wins** — it is
what the paper setters follow. Use the newest guideline (2021 at the time of writing). If a
document isn't in the library or `curriculum-sources/`, ask the owner before downloading it
(name the file and the DBE URL).

## The local past-paper library

The owner keeps every DBE and Eastern Cape paper, memo and exam guideline they have at
`~/Documents/past papers` (about 9 600 papers, Grades 9–12, 2008–2026: NSC November and May/June,
September preparatory, Grade 10/11 common exams, Grade 9 common tests). `papers-tracker.json`
indexes it; some files sit inside zips. Don't write into that folder. Use the skill's helper:

```bash
S=<skill>/scripts/papers.py
python3 $S list  "Life Sciences" 12 --from 2022            # papers + memos, newest first
python3 $S guide "Life Sciences"                           # exam guideline PDFs
python3 $S pull  "Life Sciences" 12 --from 2023 --source DBE --out <scratchpad>/papers
```

`pull` copies each paper, memo and addendum into the scratchpad and writes a `pdftotext -layout`
`.txt` beside it. Maths and chemistry come out garbled in text; open the PDF page (Read with
`pages`, or `pdftoppm` a page to PNG) when an equation or diagram matters. `--source DBE` keeps the
national papers; add provincial ones for Grades 9–11, which have few national papers.

Grades 8–9 have no national exam: schools set their own tests from the ATP's formal assessment
tasks. Use the ATP (which task, which term, which topics), CAPS's assessment section and the
Grade 9 common tests in the library. Grades 10–11 write school or provincial papers built on the
same Examination Guidelines as Grade 12 — align them the same way, using their common exams.

Read at least the **last three years** of papers and memos for the grade before planning — or
have a research agent do it and write the exam map (below).

Images in these papers can be redrawn or cropped for lessons — see graphics.md and photos.md.

## The exam map (write it before any lesson)

Write `<set>/EXAM-MAP.md` once per set; the plan and every agent brief are built from it. One
section per topic:

- **Paper and weight**: which paper, and its marks (guideline) or its share of recent papers.
- **How it is asked**: the recurring question types, with the paper reference —
  e.g. "State Newton's second law in words (2) — every Nov P1 2022–2025, Q3.1".
- **Must know word for word**: definitions, laws and principles as the guideline words them.
- **Memo marking**: where the marks go (formula ✓, substitution ✓, answer with unit ✓), what
  loses them (no unit, wrong sign convention, no direction for a vector).
- **Common mistakes**: from memos and diagnostic reports.
- **Not examined**: CAPS content the guideline excludes or papers never ask. Don't teach it, or
  give it one sentence if a later topic needs it.
- **Depth**: the highest cognitive level the papers reach here, so lessons don't go past it.

Lesson plans cite it: every lesson must trace to at least one "How it is asked" line. A lesson
that traces to none is cut or merged.

## Depth — the companion rule

- Teach the idea once, clearly, at the depth the papers reach. No derivations, history, proofs,
  enrichment or "did you know" unless a paper asks for them.
- Fewer, tighter lessons beat a complete textbook. If CAPS lists it but the papers treat it as a
  one-mark recall item, it gets a definition and a quickcheck, not a lesson.
- Say what the teacher will usually cover (practicals, investigations, projects) only as far as
  the paper examines them — e.g. the variables, the conclusion and the graph of a prescribed
  experiment, not how to run the lab.
- Spend the words saved on worked examples and practice in the exam's format.

## Exam style inside lessons

- **Command words** mean what the guideline says (state, define, explain, describe, calculate,
  compare, name, identify). A lesson teaching a definition shows the full-marks answer to
  "Define …", word for word from the guideline.
- **Marks shown**: every exam-style prompt ends with its marks, e.g. `(3)`. The answer inside the
  reveal shows where each mark goes, one mark per line or `✓` after each marked step, as the memo
  does.
- **Every lesson has an "Exam-style question"** `reveal` in the exact style, structure and mark
  allocation of a recent paper question on that idea, with a memo-style answer. Adapt a real
  question (new numbers, same shape) and cite it in the prompt ("From NSC Nov 2024 P1 Q4.2"); check
  your answer against that memo — memos have errors too, so verify, don't copy.
- **Multiple choice**: where the paper opens with a multiple-choice section, quickchecks match
  its form (four options, one correct, distractors built from the common mistakes in the exam map).
- **Formula and data sheets**: use the sheet's symbols and form exactly, and tell the learner
  which formulas are on the sheet and which they must know.
- **Warnings** (`callout` `warning`) come from the exam map's common mistakes, phrased as what
  loses marks: "Leave out the unit and you lose the final mark."
- **Topic's last lesson**: a short exam-practice lesson — 2–4 full exam-style questions covering
  the topic across cognitive levels, each in a reveal with the memo answer, plus a line pointing
  to the topic's past papers in Funda. The flashcard recap sits here too.
- Never promise a result ("this will be in your exam", "guaranteed marks"). Say what papers have
  asked: "This comes up in most Paper 1s."
