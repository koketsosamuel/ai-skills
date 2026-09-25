# Graphics — diagrams you draw, and when to ask for a photo instead

Diagrams are `svg` blocks: hand-built SVG strings, drawn on the phone by react-native-svg, on the
website as inline SVG, and served through the API's sanitizer. Build them in code with
`<kit>/svg.mjs` + `<kit>/mathsvg.mjs` (`<kit>` = `<Funda>/scripts/lessons/kit`), never by hand-typing coordinates.

## Draw it, or photograph it?

| Draw an SVG diagram when… | Ask for a photo (photos.md) when… |
| --- | --- |
| the idea is a structure, process, relationship or quantity | the point is what the real thing looks like |
| labels, arrows and colour carry the teaching | texture, colour, scale or "this exists" carry it |
| accuracy is geometric (graphs, shapes, circuits, maps to scale) | a drawing would be a guess (a specific rock, organism, artwork, building, historical scene) |
| e.g. graphs, triangles, number lines, Venn diagrams, circuits, force diagrams, food webs, the water cycle, a cell schematic, a timeline, a flow of money, a ledger layout | e.g. a microscope slide, a rock sample, a landform, a historical photograph, a painting, a crop disease, lab apparatus as it really looks, a person doing a skill |

When in doubt, draw a clear schematic now AND request the photo — a labelled diagram teaches the
parts, the photo proves it is real. Never draw a realistic picture of a real person, artwork or
historical event, and never fake a photograph.

## SVG rules (the phone is strict)

- `viewBox="0 0 W H"` with non-negative whole numbers. Width ~320–420: the phone shows the
  diagram ~340 pt wide, so a 700-wide viewBox halves every label.
- Presentation attributes only. No `<style>`, `class`, `style=""`, CSS, scripts, `<image>`,
  `<foreignObject>`, `<use>`/`href`, `<tspan>`, XML entities.
- The API sanitizer (`apps/api/src/modules/lessons/lesson-content-sanitizer.ts`, `SVG_OPTIONS`)
  serves only allowlisted tags and attributes and drops the rest silently. `<kit>/check-svg.mjs`
  mirrors that list — if a diagram needs a new attribute, add it to the sanitizer (with a spec)
  first. `stroke-dasharray` was missing until 2026-09-25 and every dashed asymptote drew solid.
- Colours from the kit palette only (GREY, BLUE, TEAL, AMBER, CORAL, PURPLE): mid-tones readable
  on the white card AND the dark theme. Never black or white for anything that carries meaning.
  Colour carries meaning (one colour per idea, matched in the caption and text), not decoration.
- Text 12–16 in viewBox units, short labels, ~10 units of margin so nothing clips. One `<text>`
  per label. `<kit>/fit-viewbox.mjs` (run by `<kit>/build.mjs`) widens the viewBox when a label would clip.
- Keep each diagram under ~80 KB (maths labels are the heavy part).
- The caption says what to notice, and may use `$…$`.

## Accuracy

- Compute coordinates: map data to pixels with a function (`X(x)`, `Y(y)`) so graphs are to
  scale and points land exactly on curves. Intercepts, turning points and asymptotes where the
  numbers say; asymptotes and construction lines dashed.
- Geometry: equal-side ticks, angle arcs, right-angle squares, parallel arrows — and angles that
  are actually the size labelled.
- Science: arrows point the right way (energy, current, water, force), parts in the right place,
  scale bars when size matters.
- Data (histograms, bar and pie charts, box plots): bars from the data, axes labelled with units,
  a zero baseline.

## Subject catalogue — what to draw

- **Mathematics / Maths Lit**: function graphs, number lines and inequalities, geometry figures,
  right triangles with opposite/adjacent/hypotenuse, trig graphs, the Cartesian plane, Venn and
  tree diagrams, histograms, box-and-whisker, frequency polygons, 3-D solids and nets, interest
  growth bars, floor plans with scale, maps with a scale bar.
- **Physical Sciences**: circuit diagrams (standard symbols), force/free-body diagrams, wave
  diagrams with λ and amplitude, particle models of states of matter, atomic models and electron
  shells, ray diagrams, velocity–time and position–time graphs, the periodic table section.
- **Life Sciences / Natural Sciences**: cell schematics, organ systems, food chains and webs, the
  carbon/water/nitrogen cycles, Punnett squares (as a `table`), DNA ladder, population graphs,
  labelled flower/leaf/heart schematics. Microscope images and specimens → photo.
- **Geography**: cross-sections, the water cycle, weather-map symbols, contour lines and a
  worked cross-section, climate graphs, landform schematics, a map grid with scale. Real
  landforms and satellite images → photo.
- **History**: timelines, cause-and-effect chains, simple locator maps. Sources, portraits and
  historical scenes → photo (a real, credited source), never a drawing.
- **Accounting / Business / Economics / EMS**: T-accounts, ledger and journal layouts (`table`),
  flow of money diagrams, supply–demand curves, the business cycle, organograms.
- **Languages**: mostly none — use `table` for vocabulary and verb forms, `flashcards` for
  recall. A diagram only for structure (a paragraph plan, a story arc).
- **Technology / EGD / Civil / Electrical / Mechanical**: orthographic and isometric views,
  dimensioned drawings, mechanisms (levers, gears, pulleys), circuit and logic diagrams.
- **Life Orientation / Creative Arts / others**: process diagrams and simple icons; artworks,
  performances and real equipment → photo.

## Look at every diagram — not optional

```
node <kit>/build.mjs <set>                    # builds, then fits viewBoxes
node <kit>/check-svg.mjs <topic-dirs>
node <kit>/render-svgs.mjs <png-dir> <topic-dirs>   # then Read every PNG
```

Check each one: nothing overlaps (labels vs lines vs other labels), nothing clipped, labels sit
next to what they label, the maths matches the lesson text, colours match their meaning, arrows
point the right way, graphs are accurate, and the diagram actually helps. Quick Look draws text in
a serif font, so the final say on spacing is the phone.
