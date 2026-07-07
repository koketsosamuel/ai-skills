---
name: frontend-design
description: Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one — aesthetic direction, typography, layout, copy, and a concrete craft floor, so the result doesn't read as templated AI defaults. Use when designing pages, artifacts, landing pages, dashboards, or restyling components.
license: Complete terms in LICENSE.txt (Apache 2.0). Adapted from anthropics/skills frontend-design; modified.
---

# Frontend Design

Approach this as the design lead at a small studio known for giving every client a visual identity that could not be mistaken for anyone else's. The client has already rejected templated proposals and is paying for a point of view: make deliberate, opinionated choices about palette, typography, and layout specific to this brief, and take one real aesthetic risk you can justify.

## First: greenfield or existing product?

**If the code lives in an existing product with a design system** (tokens, CLAUDE.md conventions, a component library), **the system wins**. Distinctiveness is spent *within* its constraints — composition, hierarchy, spacing rhythm, one signature moment built from existing tokens — never by introducing off-system colors, fonts, or one-off components. Extend the system through its own extension points if it genuinely lacks something. Everything below applies fully only to greenfield work (artifacts, new sites, standalone pages).

**Check the delivery environment before choosing fonts/assets.** CSP-sandboxed artifacts and offline/self-hosted products cannot reach Google Fonts or CDNs — use self-hosted files, data-URIs, or a deliberate system-font stack. A design whose display face silently falls back to Arial is a broken design; verify the font actually loads where the page will run.

## Ground it in the subject

If the brief doesn't pin down the subject, pin it yourself before designing: name one concrete subject, its audience, and the page's single job, and state your choice. Use anything you know about the person's preferences and past work as hints. The subject's own world — its materials, instruments, artifacts, vernacular — is where distinctive choices come from. Build with the brief's real content throughout.

## Design principles

**The hero is a thesis.** Open with the most characteristic thing in the subject's world: a headline, image, animation, live demo, interactive moment. A big number with a small label, supporting stats, and a gradient accent is the template answer — use it only if it's truly best.

**Typography carries the personality.** Pair display and body faces deliberately — not the ones you'd reach for on any project — and set a real scale with intentional weights, widths, and spacing. Make the type treatment memorable, not a neutral delivery vehicle.

**Structure is information.** Numbering, eyebrows, dividers, and labels must encode something true about the content, not decorate it. Numbered markers (01/02/03) are only right when the content actually is a sequence.

**Motion is deliberate.** One orchestrated moment (a page-load sequence, one scroll reveal) lands harder than scattered effects — and extra animation is itself an AI-generated tell. Sometimes less is more.

**Decide the color-scheme stance.** Light, dark, or both is a design decision, not an afterthought. If both, build on tokens from the start; check every accent against both grounds.

**Match complexity to the vision.** Maximalist directions need elaborate execution; minimal ones need precision in spacing, type, and detail. Elegance is executing the chosen vision well.

## Process: brainstorm → plan → critique → build → verify

**Calibration — the current AI-default looks.** Generated design clusters around recognizable defaults: (1) warm cream (~#F4F1EA) + high-contrast serif display + terracotta accent; (2) near-black + one acid-green or vermilion accent; (3) broadsheet layout — hairline rules, zero radius, dense columns; plus the broader tells: purple-to-blue gradient SaaS, Inter/Space Grotesk for everything, uniform rounded cards with soft shadows on every element, bento grids regardless of content, gradient text on the hero, emoji as icons. All are legitimate for some briefs — but they're defaults, not choices, and they appear regardless of subject. Where the brief pins a direction, follow it exactly (its words always win, even asking for one of these looks). Where an axis is free, don't spend that freedom on a default.

**Pass 1 — plan.** A compact token system: **Color** — 4–6 named hex values. **Type** — faces for 2+ roles (characterful display used with restraint, complementary body, utility for captions/data if needed). **Layout** — a concept in one-sentence prose + ASCII wireframes to compare options. **Signature** — the single element this page will be remembered by.

**Pass 2 — critique before building.** Ask of each part: would I have produced this for any similar brief? (Mentally run a similar prompt; if you land in the same place, it's a default.) Revise those parts, note what changed and why. Only then write code, following the revised plan exactly and deriving every color/type decision from it.

When coding, watch CSS selector specificity — type-based (`.section`) and element-based selectors easily cancel each other, especially section paddings/margins. Do the planning iteration in your thinking; show the user ideas once you're confident they'll delight.

**Verify by rendering, not by rereading the code.** Screenshot at mobile (~375px) and desktop widths; check the browser console for errors; stress with real content (long names, empty states, 2× text). Critique the render against the plan — then remove one accessory (Chanel: look in the mirror before leaving the house). If you can jot notes on what you tried, it helps future passes.

## Craft floor (build to it without announcing it)

- Body text contrast ≥ 4.5:1 (WCAG AA); large text/UI ≥ 3:1 — check accents on their actual grounds.
- Measure 45–75 characters; a modular type scale, fluid via `clamp()` where it earns it.
- One spacing scale used everywhere — rhythm breaks read as bugs.
- Semantic HTML with landmarks/headings in order; images get alt text; interactive elements are real buttons/links.
- Fully keyboard-operable, visible focus states, `prefers-reduced-motion` respected.
- Responsive to small screens with no horizontal body scroll.

## Restraint and self-critique

Spend your boldness in one place. Let the signature element be the one memorable thing; keep everything around it quiet and disciplined; cut decoration that doesn't serve the brief. Not taking a risk is itself a risk.

## Writing in design

Words exist to make the design easier to understand and use — design material, not decoration. Bring spacing-and-color intentionality to copy; when the brief has no real content, the copy you invent can make a design feel as templated as the layout.

- **Write from the user's side of the screen.** Name what people control and recognize, never how the system is built (manage *notifications*, not *webhook config*). Specific beats clever.
- **Active voice; controls say what happens** ("Save changes", not "Submit"), and an action keeps its name through the flow — "Publish" → toast "Published". Consistent vocabulary is how people learn their way around.
- **Failure and emptiness are moments for direction, not mood.** Errors say what went wrong and how to fix it — never apologetic, never vague. An empty screen is an invitation to act.
- **Register: conversational and tuned** — plain verbs, sentence case, no filler, tone matched to brand and audience. Each element does exactly one job: a label labels, an example demonstrates, nothing quietly doubles up.
