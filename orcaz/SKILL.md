---
name: orcaz
description: Orcaz — orchestrate a large/multi-phase feature build as the conductor of subagents. Implement + unit-test with cheap subagents, review with parallel reviewer agents, fix, then validate against the REAL running stack (curl the API, drive the UI with playwright-cli), then ship to the repo's default branch. Use when the user says "orcaz", or asks to "implement all phases / use subagents / orchestrate / you are the orchestrator". Do NOT self-trigger on merely-large tasks — orcaz merges and pushes, so it requires the explicit ask.
---

# orcaz — build+test → review → fix → real-stack test → ship

You are the **orchestrator**: decompose, dispatch, gate. Subagents implement; a **JUDGE verifier agent** independently re-runs builds/tests/coverage and commits checkpoints. Subagent reports are claims until the verifier re-runs them. Your own hands touch nothing but the final push (§7).

**Prereq:** a written spec (phase docs / plan / issue). None → write one first; every implementer is pointed at it.

**Model tiers:** BUILDER = `sonnet` (implement / fix / UI-drive); JUDGE = `opus` (review / verify). Small models (`haiku`, GPT-mini class) only for trivial mechanical side-tasks — never implementation, fixes, review, or verification. Never `fable`/Mythos-class for subagent work. If neither sonnet nor opus is offered, stop and ask.

**Context economy — the orchestrator stays lean.** Never read raw build/test/server logs, full diffs, or whole coverage tables into your own context — that's the subagents' job. Demand **structured summaries** (verdict + failures + key numbers, not transcripts); when you must check a log yourself, `tail`/`grep` the relevant lines, never `cat` the file. Point subagents at spec **paths** to read themselves rather than pasting spec content into prompts. Tell subagents the same: report conclusions and evidence pointers (file:line, screenshot path, exit code), not dumps.

## The loop

```
spec → branch + tasks
  └─ per phase (serial if dependent, parallel if independent):
       implement + UNIT TEST (BUILDER, pointed at spec — code AND tests together)
       → CHECKPOINT: JUDGE verifier re-runs build + tests + coverage → commits
  → review (parallel JUDGE reviewers by lens, read-only)
  → triage → fix (BUILDER agents, no shared files) → JUDGE re-verifies → commits
  → manual test: JUDGE brings up stack + curls REAL API; BUILDER drives REAL UI (playwright-cli)
       → fix breaks (BUILDER) → JUDGE re-verifies → commits
  → SHIP: YOU merge to the repo's DEFAULT branch and push
  → TEAR DOWN: stop everything started + close tracking tasks
```

Track phases with TaskCreate/TaskUpdate.

## 1. Set up

Branch first (`git checkout -b feat/<x>`) — never build big on default. Recon the repo: package manager, build/lint/test/codegen commands, migrations, how the app launches.

## 2. Implement + unit-test (BUILDER subagents)

- **Right-size:** one cohesive, individually testable slice per agent (e.g. one endpoint + service + migration + tests; one screen + query wiring + tests). Split sprawling phases first; don't shred into micro-tasks either — aim for a bite one agent finishes well and a verifier checkpoints in one round.
- Work **on the branch, not a worktree**; agents do **NOT commit** (the verifier does, so you control gating).
- Serial where phases share files or migration numbers; parallel only with disjoint file sets.
- **Tests ship with the code — not a later phase.** Require good coverage of the new logic: every branch, error path, gate (assert exact HTTP status), state transition — not just happy path. Push logic into pure IO-free functions. Agent runs suite + coverage and reports numbers.
- Prompt must include: spec file **paths**, "discover real state first" (latest migration number, existing helpers, test runner), build/test/codegen commands, and demand a **structured report**: files changed, commands + PASS/FAIL, coverage % for new files, untested + why, deviations. No raw log dumps.
- API contract changed → regenerate the typed client **before** web work.

## 3. Checkpoint — JUDGE verifier re-runs, then commits

Never trust an implementer's "all green". The verifier re-runs: both builds, the new tests, coverage on the changed code, and confirms the files exist (`git diff --stat`). It reports a **summary verdict**, not logs.

- **Coverage gate:** new logic well covered incl. error/gate branches — eyeball the per-file report, not a global %. Gaps → bounce to a fix agent before proceeding.
- **The repo's commit-gate policy outranks this skill**: if CLAUDE.md says the pre-commit gate must be green, fix the gate — never `--no-verify` past it except where the repo's own docs sanction it (noted honestly).
- Verifier fixes/flags cross-phase breakage before the next phase builds on it.
- **Chime per landed phase** (orchestrator session, fire-and-forget): `afplay /System/Library/Sounds/Glass.aiff`.

## 4. Review (parallel JUDGE, read-only, by lens)

Spawn reviewers **in one message**, each a different lens, read-only, verifying against the real diff (`git diff <base>..HEAD`) + spec. **Derive lenses from what the change touches**; typical full-stack trio: security/tenancy·RLS, correctness/lifecycle (state machines, async/queues, idempotency, migrations up+down), frontend/integration (cache invalidation, generated client, a11y). Demand structured findings: `[Severity] file:line — issue — why — fix`. If the harness offers the **Workflow tool**, the review→verify fan-out fits it well (invoking this skill is the orchestration opt-in).

## 5. Fix (BUILDER, no file overlap)

Triage into **non-overlapping work sets** (e.g. API vs web) — parallel agents must never edit the same file. Give each the exact finding + suggested fix. Judge Lows; don't blindly apply. Then verifier re-verifies + commits.

## 6. Manual test on a REAL stack — the part people skip

Delegate: stack bring-up + API smoke (§6a–b) → JUDGE verifier; UI pass (§6c) → BUILDER. You gate; you don't curl or browse yourself.

### 6a. Bring up
Start infra (db/redis/object-store/etc.), migrate + seed, start API + worker + web; health-check each. Standalone workers often read raw `process.env` — pass env explicitly. **Random/ephemeral ports always, never defaults** (parallel runs collide): unique DB name / bucket / Redis prefix too; thread the API port into the web base URL and **CORS**; record the ports for §6b–c and teardown.

### 6b. curl the REAL API first (fastest signal, isolates API vs UI bugs)
Login for a token; hit happy paths; **assert exact status codes** on gated paths (402 vs 403). Create real data via the API; flip roles/plans directly in DB when needed (set tenant GUC, flush caches). Exercise async paths end-to-end incl. the **failure path** (kill a dependency → retries → visible failed state).

### 6c. Drive the REAL UI (playwright-cli)
BUILDER subagent invoking the **playwright-cli** skill; precise numbered steps, expected vs actual, real creds, screenshot dir. Cover: privileged AND gated states (disabled, not just hidden); **prove dynamic behavior** (in-page marker `window.__marker=1` survives the interaction; inspect DOM/computed styles, not just screenshots); async UI states with polling; **capture browser console**. Report: per step PASS/FAIL + observed + screenshot filename — no full console dumps, errors only.

Triage what surfaces (cache-invalidation gaps, wrong codes, clipping) → BUILDER fixes → verifier re-verifies + commits.

## 7. Ship — merge to DEFAULT and push

**"Done" = merged into the default branch AND pushed.** Only stopping points short of that: no remote, or the user said stop.

1. Green + clean: `git status` clean, builds/tests pass.
2. Find the real default + remote (`git remote show origin | sed -n 's/.*HEAD branch: //p'`). No remote → report branch ready, stop.
3. Integrate per repo convention: PR repos → push branch, `gh pr create`, merge it. Direct-push repos → `git checkout <default> && git pull --ff-only && git merge --no-ff <branch> && git push`.
4. Verify landed: `git log --oneline origin/<default> -5`.
5. **Merge/push needs authorization from the user's words or repo docs** (a CLAUDE.md "push to main" norm counts). Invoking this skill is NOT by itself push authorization. Never force-push shared branches; let PR CI pass first.
6. Chime the ship: `afplay /System/Library/Sounds/Hero.aiff` (fire-and-forget).

## 8. Tear down

After the push: kill every server/worker/dev-server and background shell this run started; `docker compose down` (+`-v` for throwaway volumes) or stop/rm the specific containers — **scope to this run only**, never another agent's. Close out tracking tasks. Confirm clean (`docker ps`, `lsof -i` on your ports). Report: commit/PR URL, one-line summary, teardown confirmed.

## Principles

- **Verify, don't trust — delegate the verifying.** Claims become truth only when the JUDGE verifier re-runs them.
- **The repo's rules outrank this skill** (gate policy, branch flow, coverage bar).
- **Both test layers, always:** unit tests with real branch/failure coverage AND the live-stack pass. Mocks prove the unit; the stack proves the feature.
- **Evidence, not vibes:** exact status codes, markers, screenshots, worker-log pointers.
- **Context economy:** summaries and pointers up; never raw logs into the orchestrator.
- **No-overlap parallelism**; **right-size the slices**; **honest reporting** (tested vs untested + why); **scale effort to the ask**.
- **Finish the job** (merged + pushed = done) and **leave no mess** (teardown + closed tasks).

## Anti-patterns

Trusting "all green" without a verifier re-run · parallel agents editing one file · "tested" = mocks only, app never started · "tested" = stack only, new code uncovered / happy-path-only tests · screenshot-only UI claims · leaving cross-phase breakage for the next agent · reading full logs/diffs into the orchestrator context.
