---
name: orcaz-plan
description: Orcaz-plan — turn a fuzzy feature request into implementation-ready, dependency-ordered phase docs (the written spec orcaz builds from). Recon the codebase for real conventions, research the problem space for misconceptions and gotchas (web + code), decompose into right-sized individually-shippable slices, write one markdown phase doc per slice using the canonical anatomy. Use when the user says "orcaz-plan", asks to "plan / spec / break into phases / write a phase plan", or before an orcaz build when no spec exists yet.
---

# orcaz-plan — recon → research → decompose → write phase docs

You are the **planner**. Output = phase docs good enough that an implementing subagent, pointed at ONE doc and nothing else, builds the right thing without guessing — planning is where correctness is won or lost. This is the flow [`orcaz`](../orcaz/SKILL.md) requires a spec from. It writes **docs only** — no feature code, no orcaz invocation. **"Done" = phase docs committed and pushed** (§6).

**Subagents:** use `Explore`/general-purpose agents (BUILDER tier, `sonnet`; small models only for trivial listing/grep sweeps) for recon/research breadth — demand **conclusions and pointers** (conventions, exemplar paths, gate numbers, cited claims), never file dumps or raw page text into your context. You write the docs yourself.

## The loop

```
request → 1. RECON codebase (real conventions, exemplars, numbering, gates)
        → 2. RESEARCH problem space (misconceptions, expert advice, gotchas — web + code fan-out)
        → 3. DECOMPOSE into right-sized, dependency-ordered, shippable phases
        → 4. WRITE one phase doc per slice (canonical anatomy, research woven in)
        → 5. INDEX + sequence (order list, API↔web pairing, dependency notes)
        → 6. SURFACE open decisions to the user → COMMIT + PUSH the docs (done)
```

Track with TaskCreate/TaskUpdate.

## 1. Recon — anchor in the *real* codebase

A phase citing real files is buildable; one written from assumptions sends agents off a cliff. Record:

- **Where plans live + naming.** Find the existing phase dir (`*/phases/`, `docs/plan/`) and order index; **match its convention exactly** (naming, numbering). None → propose `<plan-dir>/phases/NN-slug.md` + `README.md` index, confirm with the user.
- **Project guidelines.** Read `CLAUDE.md`/`AGENTS.md`/contributing docs end to end — cite the applicable cross-cutting rules (tenancy, money, tokens, test gate, migration rules) in each phase's Context.
- **Build/test/codegen reality.** Exact commands: build/lint/test, coverage gate %, client codegen, migration run + numbering, app launch.
- **Exemplars.** Per subsystem touched, the canonical file to mirror — phases say "mirror `path/to/file.ts`", never abstractions.
- **Numbering gotchas.** Record the current max migration/phase number AND bake in "re-verify vs `origin/main` at write time" (concurrent branches collide).

## 2. Research — misconceptions, expert advice, gotchas (the part people skip)

This separates a plan from a wishlist: most plans fail on the footgun nobody knew to look for. Research **before** decomposing so gotchas shape phase boundaries. Fan out (parallel subagents / WebSearch + WebFetch + in-repo search), scaled to risk, across:

- **Misconceptions** — what people wrongly assume ("JWT exp is enough for logout", "webhooks arrive once, in order", "floats are fine for money") → each becomes a "don't X, do Y".
- **Expert advice** — the recommended way per primary sources (official docs, RFCs, maintainer guidance) over forum folklore; capture recommendation + rationale.
- **Gotchas/footguns** — version bugs, ordering/idempotency hazards, races, TZ/DST, rate limits, partial failure, migration locks, N+1, cache invalidation. Note trigger + symptom.
- **In-repo prior art** — the adjacent problem this team already solved; reuse beats reinvention, cite the file.
- **Security & failure modes** — authz/tenant isolation, injection/SSRF, secrets, the decline/timeout/retry path.

**Adversarially verify anything load-bearing** — a claim that decides an architecture gets a second source or an "unverified" flag. Cite sources inline. Distill into a per-area gotcha list, one line each: *misconception → why it bites here → do instead (source/pointer)*. These feed each phase's Misconceptions & gotchas + Design decisions; the riskiest become Open decisions.

## 3. Decompose — right-sized, dependency-ordered, shippable

Slice how orcaz consumes it:

- **One phase = one cohesive, individually-testable, shippable slice** (one endpoint + service + migration + tests; one screen + query wiring + tests). Split multi-subsystem epics into `29a`, `29b`, …; don't shred into micro-tasks.
- **Pair backend↔frontend, backend first** (API lands + client regenerates before the web phase); state the dependency.
- **Order by dependency**: shared files / sequential migration numbers = serial; disjoint file sets = parallel — say which, so orcaz can parallelize.
- **Each phase ends in a demonstrable outcome**, not "code exists"; the Phase gate is the boolean that unblocks the next.

## 4. Write — one doc per slice (canonical anatomy)

Standalone markdown per phase; an agent needs nothing but the doc + cited files:

```markdown
# <API|Web> Phase NN — <Title> (<one-line what-and-why>)

> 1–2 paragraph blockquote abstract: what/why, in/out of scope, paired/blocking
> phases, gating, migration count.

## Objective
The outcome that must be demonstrably TRUE (not "code exists"). Real files touched
([path](path)); the headline invariant.

## Context (current state — verified on `main`)
Bullets with file pointers: existing schema/migrations, service to extend, exemplar to
mirror, applicable CLAUDE.md rules, next free migration number (+ re-verify caveat).

## Scope
Numbered subsections — the actual work, specific enough to implement from: migration SQL,
DTO fields, endpoint signatures, auth/RLS decorators, client-regen steps. End with:
### Out of scope (note explicitly)
What this phase deliberately does NOT do, each with the reason or owning phase.

## Misconceptions & gotchas (from research)
Each bullet: footgun → why it bites here → do instead, with source/pointer. Scale to
risk: CRUD = two lines; billing/auth/concurrency/3rd-party = a real list.

## Design notes / decisions
Deliberate choices + rationale (why this shape/FK/idempotency key); the researched
recommendation over the obvious-but-wrong one.

## Tasks
Grouped `- [ ]` checklists (Schema/Service/Web/Tests). ALWAYS include tests: happy +
failure paths, cross-tenant RLS test per new tenant table, the coverage gate, and
"update CLAUDE.md if this adds a cross-cutting convention."

## Acceptance checks
`- [ ]` minimum demonstrable verifications (user-visible outcomes + invariants) — what
orcaz's real-stack pass proves.

## Phase gate
The single boolean that unblocks dependent phases — and which ones.

## Open decisions to resolve early
Judgment calls needing a human answer, each with a RECOMMENDED default.
```

Writing rules: cite real clickable paths/numbers/commands from recon, never invented; honor every repo convention (a phase violating CLAUDE.md is broken); checkboxes for tasks/acceptance; **match the repo's existing phase docs** in tone/depth/order — mirror theirs over this template if richer; big features get an epic overview doc + index entries.

## 5. Index & sequence

Add each phase to the order index as a one-line link, dependency-ordered, API-before-web. Epics get a short overview blockquote (what, build order, key invariants). State the **recommended build order** explicitly, marking parallel-safe phases.

## 6. Surface decisions → commit + push (this is "done")

- Collect Open decisions across phases; put the genuinely architecture-deciding 1–4 to the user via `AskUserQuestion` (each with a recommended default). Fold answers into the docs **before** committing.
- Stage **only** the plan files you wrote (never sweep unrelated working-tree changes). Docs are prose — bypass the commit hook **only if the repo's own guidelines sanction it for docs-only changes**; otherwise run the gate. Message per repo style, e.g. `docs(plan): add <feature> phases NN…`.
- Push per the repo's actual workflow: find the real default branch (`git remote show origin | sed -n 's/.*HEAD branch: //p'`); direct-push if that's the repo norm, else branch + PR. No remote → commit, report, stop. **Invoking this skill is standing authorization to commit and push the docs — do not stop to ask for confirmation.** Never force-push a shared branch.
- Verify landed (`git log --oneline origin/<default> -3` / PR exists). **Stop here — no implementation, no orcaz invocation.** Report: commit/PR URL, phase docs written, recommended build order.

## Principles

- **Plan from the real codebase, not memory** — a phase citing a nonexistent file is worse than no phase.
- **Research is first-class** — fan out, verify load-bearing claims, cite sources, let gotchas shape boundaries.
- **Right-size for orcaz** — cohesive shippable bites; split epics, don't shred.
- **Outcome, not output** — Objective/Acceptance = demonstrably TRUE; gate = the unblocking boolean.
- **Honor repo conventions exactly**; **surface the hard calls** with recommendations before commit.
- **Context economy** — subagents return conclusions/pointers, never dumps.
- **Plan, don't build — but finish**: docs committed + pushed, then stop.

## Anti-patterns

Phases citing files/commands/numbers that don't exist · skipping research (footgun rediscovered mid-build) · generic gotchas ("watch out for security") instead of feature-and-version-specific with a source · oversized or shredded phases · phases violating repo cross-cutting rules · "done = code exists" instead of outcome + gate · burying an architecture question in a doc instead of asking · docs left uncommitted · sweeping unrelated changes into the plan commit or bypassing the hook for real code · implementing the feature or invoking orcaz.
