# ai-skills

A collection of [Claude Code](https://claude.com/claude-code) skills.

Each skill lives in its own directory with a `SKILL.md` (name + description frontmatter,
followed by the instructions Claude loads when the skill is invoked).

## Skills

### [`orcaz/`](orcaz/SKILL.md)

Orchestrate a large / multi-phase feature build as the **conductor of subagents**:

- **Decompose** the spec into right-sized, individually testable phases (not one giant chunk, not trivial micro-tasks).
- **Implement** each phase with a BUILDER (`sonnet`) subagent that ships code *and* unit tests together — small models (haiku / GPT-mini class) never do implementation, fixes, review, or verification.
- **Verify** every checkpoint with a JUDGE (`opus`) verifier agent (re-runs build/tests/coverage, commits) — the orchestrator never verifies by hand, and the repo's own rules (commit-gate policy, branch flow) always outrank the skill.
- **Review** in parallel with JUDGE reviewers, lenses derived from what the change touches (e.g. security/tenancy, correctness/lifecycle, frontend/integration).
- **Fix** findings with BUILDER agents split so no two touch the same files.
- **Manual-test on a real stack** — bring it up on **random ports** (parallel-safe), smoke-test the real API with `curl`, drive the real UI with `playwright-cli`.
- **Ship** by integrating into the repo's default branch and pushing — that push *is* the definition of "done" (with authorization from the user's words or the repo's docs).
- **Tear down** every server / DB / Docker container the run started, and close out the tracking tasks.
- **Context economy** throughout: the orchestrator reads structured summaries and evidence pointers, never raw logs, full diffs, or coverage dumps.

A short sound plays when a phase lands and again when the work ships.

### [`orcaz-plan/`](orcaz-plan/SKILL.md)

Turn a fuzzy feature request into the **implementation-ready phase docs** that `orcaz` builds from:

- **Recon** the codebase first — real conventions, exemplar files to mirror, migration numbering, test gates. Phases cite real paths, never assumptions.
- **Research** the problem space (web + in-repo, fan-out): common misconceptions, expert advice from primary sources, version-specific footguns — adversarially verifying load-bearing claims. The gotchas shape the phase boundaries.
- **Decompose** into right-sized, dependency-ordered, individually-shippable slices (paired API-before-web where the repo does that).
- **Write** one markdown doc per phase using a canonical anatomy: Objective, Context, Scope (+ out-of-scope), Misconceptions & gotchas, Design decisions, checkbox Tasks and Acceptance checks, Phase gate, Open decisions.
- **Surface** the architecture-deciding open questions to the user (with recommended defaults) before committing, then **commit + push the docs** — that's the deliverable; it never writes feature code or invokes `orcaz` itself.

## Installing a skill

Copy a skill directory into your Claude Code skills folder:

```bash
# user-level (all projects)
cp -r orcaz ~/.claude/skills/

# or project-level
cp -r orcaz /path/to/project/.claude/skills/
```

Then invoke it (e.g. `/orcaz`) or let Claude trigger it from the description.
