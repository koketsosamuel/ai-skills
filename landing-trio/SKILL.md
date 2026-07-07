---
name: landing-trio
description: Landing-trio — design a stunning, mobile-first landing page by building THREE genuinely different style variants, showing them side by side (live files + screenshots), letting the user pick a direction (or a mix), then fully implementing the winner in the real target. Use when the user says "landing-trio", asks for a landing page / marketing site / homepage with style options, or wants design variants to choose from before committing.
---

# landing-trio — 3 directions → side-by-side → pick → implement

You design by **options, not by fiat**: three genuinely divergent, complete landing-page variants the user compares side by side, then a full build of the winner. Apply the [`frontend-design`](../frontend-design/SKILL.md) skill's principles throughout (subject-grounded choices, no AI-default looks, signature element, craft floor, copy rules) — this skill adds the compare-and-pick workflow and the landing-page/mobile specifics.

## The loop

```
brief → 1. INTAKE (subject, audience, ONE conversion job, content, environment)
      → 2. DIRECTIONS: pick 3 divergent styles that fit the subject; token plan each
      → 3. BUILD 3 self-contained variant pages (parallel subagents, disjoint files)
      → 4. SHOW side by side: compare page + mobile & desktop screenshots per variant
      → 5. USER PICKS (a variant, or a mix — "A's layout, B's palette")
      → 6. IMPLEMENT the winner properly in the real target → verify → done
```

## 1. Intake

Pin down before designing: the **subject** and audience; the page's **one conversion job** (sign up? book? buy? call?) — a landing page has exactly one primary CTA; the **real content** available (copy, logo, images, testimonials — what must be invented, invent per frontend-design's writing rules); the **target environment** (standalone HTML? the project's framework? where fonts/assets can load from — CSP/offline check); and any brand constraints (existing colors/logo lock some axes — say which remain free).

## 2. Directions — three that could not be mistaken for each other

Choose 3 styles **that fit the subject** from across the spectrum — e.g. editorial/magazine, brutalist, luxury/refined, playful/toy-like, technical/precise, organic/natural, retro (specify era), ultra-minimal, maximalist, art-deco, terminal/mono — or invent one from the subject's own world. Rules:

- **Divergent on every axis**: palette, type pairing, layout concept, motion stance, and signature element all differ. Three tints of the same design is a failed trio.
- **None of them an AI-default look** (frontend-design's calibration list). Each direction gets its own compact token plan: 4–6 named hex values, display+body faces, one-line layout concept, the signature.
- **All three mobile-first**: design at ~375px, then enhance up. Every direction must be able to sell at phone width — a hero that only works on desktop is disqualified.
- One line per direction to the user later: name + the feeling it optimizes for + the risk it takes.

## 3. Build the variants

- Each variant is a **complete, self-contained landing page** — full page (hero → proof → features/story → CTA → footer as the subject demands), real copy per the writing rules, inline CSS/assets so it opens anywhere. Not a mood board, not a hero-only teaser: the user must be able to judge the whole page.
- Files: `<dir>/variant-a-<style>.html`, `variant-b…`, `variant-c…` in the project (or scratch dir for throwaway comparisons).
- **Fan out three BUILDER subagents in parallel** (disjoint files; each gets the shared brief + its own token plan) or build serially if the environment lacks agents. Each variant honors the full craft floor: AA contrast, 45–75ch, one spacing scale, semantic HTML, keyboard + focus, `prefers-reduced-motion`, **no horizontal scroll at 360px, tap targets ≥ 44px, fluid type via `clamp()`**, lightweight (no heavy frameworks for a static page; lazy-load below-the-fold images).

## 4. Show them side by side

- Write `compare.html`: a strip/grid that iframes all three variants with the direction name + one-line pitch above each, and a mobile/desktop width toggle per frame if cheap. Send it (and the three variant files) to the user rendered.
- **Screenshot each variant at ~375px and ~1280px** (playwright-cli or the preview tools) and share the shots — screenshots survive where an iframe might not, and they force you to actually look at your own work before the user does.
- Verify before presenting: no console errors, fonts actually loaded (not fallback), nothing clipped at mobile width. A broken variant poisons the comparison.

## 5. The pick

Ask with `AskUserQuestion` — one option per variant (name + one-line pitch + tradeoff), and note that **mixing is welcome** ("A's layout with C's palette"). If the user picks a mix, restate the merged token plan in one short block and confirm it's what they meant before building. No pick / "you decide" → recommend one with your reasoning and proceed.

## 6. Implement the winner

- Build it **properly in the real target**: the project's framework/components/i18n/design-token conventions if it lives in a codebase (repo rules win — see frontend-design's existing-product rule), or a polished standalone page if static. Componentize, wire the real CTA target, real assets, SEO/meta + OG tags, favicon.
- The two losing variants are kept as files (cheap reference for future "actually, can we try B's vibe?") unless the user wants them deleted; `compare.html` and scratch shots are disposable.
- **Verify the final page by rendering**: mobile + desktop screenshots, console clean, Lighthouse-level sanity (images sized, no layout shift from late fonts — `font-display: swap` + preload the display face), stress with long content. Then remove one accessory.
- Stop after the implemented page is verified. Shipping/committing follows the project's workflow (or hand to orcaz) — not this skill's job unless asked.

## Principles

- **Options are only useful if they're really different** — divergence per axis is the whole value; enforce it at the token-plan stage, before code is written.
- **Whole pages, judged rendered** — users pick between finished impressions, not descriptions; you screenshot your own work before showing it.
- **Mobile-first is a gate, not a feature** — every variant must sell at 375px or it doesn't get shown.
- **The user's pick is the spec** — implement the chosen direction faithfully; don't sneak back your own favorite.
- **frontend-design's rules ride along** — subject-grounded, no default looks, one signature, craft floor, copy as design material.
- **Context economy** — subagents return file paths + screenshot paths + a one-line self-critique, not HTML dumps.

## Anti-patterns

Three tints of one design · variants that are AI-default looks · hero-only teasers instead of complete pages · presenting variants you never rendered/screenshotted · desktop-first variants that collapse at 375px · ignoring the pick and blending in your own preference uninvited · re-asking the user to choose again after a clear pick · heavyweight JS frameworks for a static landing page · implementing off-system styling inside a codebase that has a design system.
