# ai-skills

A collection of [Claude Code](https://claude.com/claude-code) skills.

Each skill lives in its own directory with a `SKILL.md` (name + description frontmatter,
followed by the instructions Claude loads when the skill is invoked).

## Skills

### [`orcaz/`](orcaz/SKILL.md)

Orchestrate a large / multi-phase feature build as the **conductor of subagents**:

- **Decompose** the spec into right-sized, individually testable phases (not one giant chunk, not trivial micro-tasks).
- **Implement** each phase with a `sonnet` subagent that ships code *and* unit tests together.
- **Verify** every checkpoint with an `opus` verifier agent (re-runs build/tests/coverage, commits) — the orchestrator never verifies by hand.
- **Review** in parallel with `opus` reviewers by dimension (security/tenancy, correctness/lifecycle, frontend/integration).
- **Fix** findings with `sonnet` agents split so no two touch the same files.
- **Manual-test on a real stack** — bring it up on **random ports** (parallel-safe), smoke-test the real API with `curl`, drive the real UI with `playwright-cli`.
- **Ship** by integrating into the repo's default branch and pushing — that push *is* the definition of "done".
- **Tear down** every server / DB / Docker container the run started, and close out the tracking tasks.

A short sound plays when a phase lands and again when the work ships.

## Installing a skill

Copy a skill directory into your Claude Code skills folder:

```bash
# user-level (all projects)
cp -r orcaz ~/.claude/skills/

# or project-level
cp -r orcaz /path/to/project/.claude/skills/
```

Then invoke it (e.g. `/orcaz`) or let Claude trigger it from the description.
