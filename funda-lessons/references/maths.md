# Maths and symbols — in the text and in diagrams

The phone, the website and the admin preview render lesson maths with MathJax (SVG output). The
API renders every `$…$` once and ships the SVG with the lesson. Diagram maths is baked into the
SVG at build time with the same font, so a formula looks identical everywhere.

This applies to every subject that writes symbols: Mathematics, Mathematical Literacy, Physical
Sciences (units, formulas, equations), Life Sciences (chemical formulas), Accounting (formulas in
worked calculations), Geography (scale, gradient), Technology/EGD (dimensions).

## In lesson text

- Inline `$…$`, display `$$…$$` (or `eq(tex)`). Works in text, headings, list items, callout and
  card titles, reveal prompts, quickcheck question/options/explanation, flashcards, table cells
  and figure captions.
- **Base TeX package only.** Allowed: `\frac`, `\sqrt`, `^`, `_`, `\times`, `\div`, `\pm`, `\le`,
  `\ge`, `\ne`, `\approx`, `\text{}`, `\left( \right)`, `\begin{array}{rcl}…\end{array}` (with
  `\hline` and `|` rules — they draw), `\quad`, `\;`, `\,`, `^\circ`, Greek letters, `\mathbb{R}`,
  `\cdot`, `\ldots`, `\overline{}`, `\hat{}`, `\triangle`, `\angle`, `\rightarrow`.
  Not allowed: `aligned`, `align`, `cases`, `\color`/`\textcolor`, `\ce` (mhchem), any package.
- **Everything that is maths goes in `$…$`** — never plain letters beside typeset ones:
  - variables, unknowns, point/side/angle/triangle names: `$x$`, `$\theta$`, `angle $P$`,
    `side $AB$`, `$\triangle PQR$`, `$\hat{R}$`, `$x$-axis`, `the $y$-intercept`
  - expressions, equations, inequalities: `$QR = 9$ m` (unit outside, the whole formula inside —
    never `$QR$ = 9 m`)
  - function names used as maths: `$\sin\theta$`, `$f(x)$`; a calculator key named as a key stays a word
  - sets and probability: `$P(A)$`, `$n(S)$`; coordinates `$(2;\,3)$`
  - chemistry: `$\text{H}_2\text{O}$`, `$\text{CO}_2$`, `$\text{C}_6\text{H}_{12}\text{O}_6$`;
    reactions `$\text{2H}_2 + \text{O}_2 \rightarrow \text{2H}_2\text{O}$`
  - physics: `$F = ma$`, `$v = 12\ \text{m·s}^{-1}$`, `$9.8\ \text{m·s}^{-2}$`
  - no Unicode stand-ins in copy: ², ³, ₁, √, π, θ, ≤, ≥, ≠, ×, ÷ in maths → TeX.
- **Stays plain**: numbers in prose ("3 lessons", "Step 1", "Grade 10", years), money and
  percentages in prose (R1 500, 12%) unless inside a formula, units after a number ("15 m"),
  lesson titles (not typeset), words like "sine" and "hypotenuse", option labels a), (A).
- A dollar sign for money is `\$` (rare — rands are R).
- Degrees: `$30^\circ$` in maths; "30°" is fine in a plain-text title.
- Subtraction of one equation from another: write it as its own row (`working()` does it); a rule
  under a column reads as a number from nowhere.
- `node <kit>/check-math.mjs <topic-dirs>` renders every expression exactly as the API does. It must print
  `ok` for every file.

## In diagrams — `<kit>/mathsvg.mjs`

```js
import { math, mathWidth, mathExtent, wordsMath } from '../../../../kit/mathsvg.mjs'; // from src/NN-name/
math('2^3 \\times 2^4 = 2^{7}', x, y, { size: 16, fill: BLUE, anchor: 'middle' });
math('\\textcolor{#e0764f}{3x} + \\textcolor{#5b8fd9}{6}', x, y);   // several colours
wordsMath(x, y, 'asymptote', 'y = 0', { fill: AMBER });               // sans words + maths
```

- `y` is the baseline, like `<text y>`; `size` is the font size in viewBox units.
- Diagrams are baked at build time, so `color` and `ams` ARE available here (not in text).
- `\color{c}{x}` is a switch that colours everything after it — use `\textcolor{c}{x}`.
- It throws on a TeX error or a character MathJax can't draw — fix the TeX, never catch it.
- Every piece of maths in a diagram goes through `math()`: variables, expressions, point and
  vertex labels (A, B, P — italic like `$A$` in the text), axis letters, angles, `30^\circ`,
  coordinates, function labels, chemical formulas. Plain words stay `<text>`. Bare tick numbers may
  stay `<text>`, but be consistent inside one diagram.
- Words next to maths: `wordsMath()`. It anchors the words to END at the formula, because the
  phone's sans font runs wider than any estimate and a start-anchored word runs into the maths
  ("asymptotey = 0" — a real bug).
- Each label is 2–8 KB of paths; keep a diagram under ~80 KB. Never typeset a sentence.

## Traps that already bit (don't rediscover them)

- MathJax without `linebreaks: { inline: false }` splits a long inline formula and returns only
  the first piece. The kit sets it.
- MathJax draws a space as `<path d="">`; the API sanitizer turns it into a bare `d` — invalid XML —
  and the phone drops the whole diagram. The kit strips it; `check-svg.mjs` catches it.
- `<tspan>` for a raised exponent or a coloured word piles up on the phone (react-native-svg lays
  out each tspan on its own). Never use tspans; use `math()`.
- The phone doesn't decode XML entities (`&lt;` shows literally).
