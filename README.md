# ai-skills

A collection of [Claude Code](https://claude.com/claude-code) skills.

Each skill lives in its own directory with a `SKILL.md` (name + description frontmatter,
followed by the instructions Claude loads when the skill is invoked).

## Skills

### [`orcaz/`](orcaz/SKILL.md)

Orchestrate a large / multi-phase feature build as the **conductor of subagents**:

- **Decompose** the spec into right-sized, individually testable phases (not one giant chunk, not trivial micro-tasks), and write a **brief** once — commands, conventions, repo rules, report schema — that every subagent reads instead of having it re-pasted into its prompt.
- **Implement** each phase with a BUILDER (`sonnet`) subagent that ships code *and* unit tests together — small models (haiku / GPT-mini class) never do implementation, fixes, review, or verification.
- **Verify** each batch with a VERIFIER (`sonnet`) agent that re-runs **typecheck → affected tests → build** and commits — cheap because the work is mechanical, **escalated to `opus`** the moment it isn't (verdict contradicts the implementer, ambiguous failure, coverage that looks gamed, anything touching auth/money/tenancy). The orchestrator never verifies by hand, and the repo's own rules (commit-gate policy, branch flow) always outrank the skill.
- **Review** the full diff in **one round** once every phase has landed — parallel REVIEWER (`opus`) agents, lenses derived from what the change touches (e.g. security/tenancy, correctness/lifecycle, frontend/integration). Judgment work never gets downgraded.
- **Fix** findings with BUILDER agents split so no two touch the same files.
- **Manual-test on a real stack** — warmed in the background from minute one, brought up on **random ports** (parallel-safe); smoke-test the real API with `curl`, drive the real UI with `playwright-cli`.
- **Log what's out of scope** rather than silently fixing or dropping it: unrelated bugs go to a findings doc, and the end-of-run report *lists* them (severity + `file:line`), then asks once whether to file them, plan them, or leave them.
- **Ship** by integrating into the repo's default branch and pushing — that push *is* the definition of "done"; invoking the skill is standing authorization to make it. One full build + full suite runs here, once, as the net under every scoped gate.
- **Tear down** every server / DB / Docker container the run started, and close out the tracking tasks.
- **Terse up, verbose down**: one line per landed milestone to the user, exhaustive context to subagents.
- **Context and resource economy** throughout: the orchestrator reads structured summaries and evidence pointers, never raw logs, full diffs, or coverage dumps — and *no* agent `cat`s a log. Parallel edits, serialized builds and suites, capped test workers, batched gates.

A short sound plays when a batch lands and again when the work ships.

### [`orcaz-plan/`](orcaz-plan/SKILL.md)

Turn a fuzzy feature request into the **implementation-ready phase docs** that `orcaz` builds from:

- **Recon** the codebase first — real conventions, exemplar files to mirror, migration numbering, test gates. Phases cite real paths, never assumptions.
- **Research** the problem space (web + in-repo, fan-out): common misconceptions, expert advice from primary sources, version-specific footguns — adversarially verifying load-bearing claims. The gotchas shape the phase boundaries.
- **Decompose** into right-sized, dependency-ordered, individually-shippable slices (paired API-before-web where the repo does that).
- **Design for simplicity**, since the plan is where it's decided: fewest moving parts that make the Objective true, extend the exemplar before inventing a pattern, today's requirement only, every new abstraction / table / dependency justified in a line or cut. Simple is the solution's *shape*, never dropped edge cases.
- **Write** one markdown doc per phase using a canonical anatomy: Objective, Context, Scope (+ out-of-scope), Misconceptions & gotchas, Design decisions, checkbox Tasks and Acceptance checks, Phase gate, Open decisions.
- **Surface** the architecture-deciding open questions to the user (with recommended defaults) before committing, then **commit + push the docs** — that's the deliverable; it never writes feature code or invokes `orcaz` itself.

### [`frontend-design/`](frontend-design/SKILL.md)

Distinctive, intentional visual design for new UI — adapted from [Anthropic's official skill](https://github.com/anthropics/skills/tree/main/skills/frontend-design) (Apache 2.0, modified) with these additions:

- **Greenfield vs existing product** — in a codebase with a design system, the system wins; distinctiveness is spent within its tokens, never against them.
- **Environment check for fonts/assets** — CSP-sandboxed artifacts and offline products can't reach CDNs; verify the display face actually loads.
- **Concrete craft floor** — WCAG AA contrast numbers, 45–75ch measure, one spacing scale, semantic HTML, keyboard + reduced-motion.
- **Verify by rendering** — screenshot mobile + desktop, check the console, stress with real/long content; then remove one accessory.
- **Extended AI-default tells** — beyond the three classic looks: purple-gradient SaaS, Inter-for-everything, uniform rounded-card grids, bento-by-default, gradient hero text, emoji as icons.
- A deliberate **light/dark stance** as part of the plan.

### [`landing-trio/`](landing-trio/SKILL.md)

Design a stunning, mobile-first **landing page by options, not by fiat** — built on `frontend-design`:

- **Intake** the subject, audience, and the page's ONE conversion job.
- **Pick three genuinely divergent style directions** that fit the subject (editorial, brutalist, luxury, playful, technical, retro, …) — different palette, type, layout, motion, and signature per direction; never three tints of one design, never an AI-default look.
- **Build three complete, self-contained variant pages** in parallel with `opus` subagents — design work always runs on opus (mobile-first gate: every variant must sell at 375px).
- **Show them side by side** — a `compare.html` strip plus mobile + desktop screenshots of each, verified rendered before presenting.
- **The user picks** (or mixes: "A's layout with C's palette"), then the winner is **fully implemented** in the real target — framework/design-system conventions, real CTA, SEO/OG meta — and verified by rendering.

### [`seo-max/`](seo-max/SKILL.md)

Act as an **SEO expert** who audits and maximizes a site's search visibility end-to-end — with per-stack playbooks, all research-verified against primary sources (Google Search Central, framework docs, npm, log-data studies) as of July 2026:

- **Detect the stack, load its playbook**: [Astro](seo-max/references/astro.md) (v6/v7-aware), [Next.js](seo-max/references/nextjs.md) (App Router, Next 16), [pure HTML/CSS](seo-max/references/html-css.md) (no build step), plus a [universal technical-SEO backbone](seo-max/references/technical-seo.md) for any other stack.
- **Audit the real site** (built output / live HTML, not source assumptions), findings **ranked by impact**: indexability blockers → duplicate-content structure → crawl surface → on-page → structured data → social meta → Core Web Vitals.
- **Fix with one source of truth per signal** — canonical, sitemap, internal links, and og:url must agree; metadata wired to content, never hand-copied.
- **AI visibility with honest framing**: [llms.txt](seo-max/references/llms-txt.md) generated from the same source as the sitemap, robots.txt stance for AI retrieval vs training bots, answer-shaped content — sold as cheap insurance, never as rankings.
- **Myth-refusal as a feature**: declines dead tactics (meta keywords, FAQ/HowTo rich results, keyword density, sitemap priority) with the one-line why.
- **Verify by fetching**: raw-HTML check (`curl` — what AI crawlers and Bing actually see), robots/sitemap/llms.txt resolution, structured-data validation.

### [`funda-lessons/`](funda-lessons/SKILL.md)

Write **Funda SA lessons for any subject and grade, ready for production**, with graphics, checked on the phone:

- **Production-first**: every lesson lives in the Funda repo as a *lesson set* (`scripts/lessons/<subject>/grade-<n>/` — source build scripts, built JSON, fixed ids) and reaches production through the repo's loader, which keeps ids stable across environments, never deletes (learner progress cascades), never overwrites an admin's edit, and hides lessons still waiting for photos. Claude loads locally and hands the owner the production commands.
- **Intake → plan → write**: CAPS topic order checked against what production's curriculum already has, one idea per lesson, plain language for a 15-year-old, every worked step shown, reveals and quickchecks in every lesson. Large jobs fan out to `opus` agents sharing one [brief](funda-lessons/references/agent-brief.md).
- **Maths everywhere it belongs** ([rules](funda-lessons/references/maths.md)): every symbol in `$…$`, including chemistry and physics units; diagram labels drawn as MathJax glyph paths so they match the text exactly.
- **Graphics drawn in code** ([rules](funda-lessons/references/graphics.md)): to-scale graphs, geometry, circuits, cycles, timelines, ledgers, with a per-subject catalogue of what's worth drawing and what the phone's SVG renderer and the API sanitizer will and won't draw.
- **Photo placeholders, never fetched or invented photos** ([rules](funda-lessons/references/photos.md)): a "Photo coming soon" frame where only a real photo will do, an `IMAGES-NEEDED.md` shopping list (what to shoot or find, legal sources, alt text, caption), and the path for a photo uploaded in production to come back into the source.
- **Gates** ([pipeline](funda-lessons/references/pipeline.md)) using the repo's kit: maths render check, SVG/sanitizer check, the admin editor's own validator, render-to-PNG for looking, local load + API check, then the phone.

## Installing a skill

Copy a skill directory into your Claude Code skills folder:

```bash
# user-level (all projects)
cp -r orcaz ~/.claude/skills/

# or project-level
cp -r orcaz /path/to/project/.claude/skills/
```

Then invoke it (e.g. `/orcaz`) or let Claude trigger it from the description.
