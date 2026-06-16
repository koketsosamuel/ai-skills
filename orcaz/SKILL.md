---
name: orcaz
description: Orcaz — orchestrate a large/multi-phase feature build as the conductor of subagents. Implement with sonnet subagents (each writing unit tests to good coverage), review with parallel opus reviewer agents, fix with sonnet agents, then manually test by hitting the REAL running API (curl) and driving the REAL UI with playwright-cli, then ship by merging to the repo's default branch and pushing. Use when the user says "orcaz", asks to "implement all phases / use subagents / orchestrate / you are the orchestrator", when a build is large enough to decompose into phases, or whenever changes must be validated against a live stack and real browser, not just unit tests.
---

# orcaz — orchestrated implementation (build+test → review → fix → real-stack test → ship)

You are the **orchestrator**, not the implementer — and not the verifier either. You decompose the work, dispatch subagents, and **launch an opus verifier agent** that independently re-runs builds/tests/coverage, commits the checkpoints, and validates against a **running stack** (real API via curl). Subagent reports are claims; the opus verifier's re-run is what turns them into truth. **The only step you perform with your own hands is the final push to the default branch (§7)** — everything else is delegated.

Prereq: there should be a **written spec** (phase docs / plan / issue). If there isn't one, write it first (or run the planning flow) — every implementation subagent is pointed at it. A vague spec produces vague code across N agents.

## The loop

```
spec → branch + tasks
  └─ for each phase (sequential if dependent, parallel if independent):
       implement + UNIT TEST (sonnet subagent, pointed at the spec — code AND tests land together)
       → CHECKPOINT: an OPUS VERIFIER agent re-runs build + the new unit tests + coverage → commits
  → review (parallel opus reviewers by dimension, read-only)
  → triage → fix (sonnet agents, split so no two touch the same files)
       → opus verifier re-verifies → commits
  → manual test: opus verifier brings up stack + smoke-tests REAL API (curl); sonnet agent drives REAL UI (playwright-cli)
       → fix what breaks (sonnet) → opus verifier re-verifies → commits
  → SHIP: YOU integrate the feature branch into the repo's DEFAULT branch and push it
  → TEAR DOWN: stop every test server/process/container you started + close out the tracking tasks
```

Use the Task tools (TaskCreate/TaskUpdate) to track the phases so progress is visible.

## 1. Set up

- **Branch first** (`git checkout -b feat/<x>`); never build a big change on the default branch. Commit a checkpoint after each green phase so you always have a restore point.
- Recon the repo: package manager, build/lint/test scripts, how the API client is generated (e.g. an OpenAPI codegen step), how migrations run, how the app is launched. You need these for the checkpoints.

## 2. Implement + unit-test (sonnet subagents)

- **Right-size the chunk before dispatching — no agent gets a giant phase.** One subagent should own a unit of work it can do *well* in a single focused pass, not a sprawling multi-subsystem epic. If a phase is too big (many files across several subsystems, multiple migrations, API + worker + web all at once, or a spec section that reads like several features), **break it into smaller, independently shippable sub-phases first**, then dispatch those. A too-large chunk is where agents cut corners, lose the thread, and skimp on tests. But **don't over-split** — slicing into trivial one-function tasks adds coordination/checkpoint overhead and loses coherence. Aim for the middle: each bite is a cohesive, individually testable slice (e.g. one endpoint + its service + migration + tests; one screen + its query wiring + tests). When in doubt, prefer a bite a single agent can finish and a verifier can checkpoint in one round.
- One subagent per phase. **`model: sonnet`** for implementation. Work **on the branch, not in a worktree** (you want integrated work), and tell the agent **NOT to commit** — you commit at checkpoints so you control gating and messages.
- Sequence by dependency: phases that share files or migration numbering must be serial. Truly independent phases can run in parallel (separate file sets).
- **Code and unit tests ship together — testing is part of "implement", not a later phase.** The prompt must require the agent to write unit tests alongside the code, with **good coverage of the logic it adds**: every new pure function / branch / error path / guard, each entitlement or permission gate (assert the exact outcome, e.g. the HTTP status), state-machine transitions, and the failure paths — not just the happy path. Push the heavy logic into **pure, IO-free functions** so it's testable without a DB/network (fast, deterministic), and cover the wiring with integration/e2e tests. Tell it to **run the suite + a coverage report** and include the numbers in its report; a phase isn't "done" if its new code is largely uncovered.
- The prompt must also: point at the spec file(s) in full; tell the agent to **discover real state first** (latest migration number, existing helpers, the project's test runner + coverage command) because the spec drifts as earlier phases land; list build/test/codegen commands; and demand a **structured report** (files changed, commands run + PASS/FAIL, **coverage % for new files**, what's untested + why, deviations).
- After an API contract changes, regenerate the typed client **before** the web work so the UI sees new endpoints/types.

## 3. Checkpoint — the opus verifier re-runs, then commits

You do not verify by hand — **launch an opus verifier agent** to run the checkpoint. **Never trust the implementing subagent's "all green" or its coverage numbers.** Tell the verifier to re-run the key checks itself and commit only when they pass:

```bash
pnpm <api:build> && pnpm <web:build>           # both compile
<run the new unit/integration tests yourself>  # they actually pass
<run coverage on the changed code>             # e.g. jest --coverage --collectCoverageFrom='<new globs>'
git diff --stat; ls <expected new files>       # code AND test files are really there
```

- **Coverage gate:** the phase's new logic should be well covered (aim high on lines/branches for new files — match or beat the repo's existing bar). If a new module has tests but they skip the error/gate/failure branches, that's not covered — the verifier reports the gap and you bounce it back to a fix agent to add the missing cases before moving on. The verifier eyeballs the coverage report for the new files, it doesn't just trust a global %.
- Only then does the verifier commit. If the project has a flaky pre-commit gate, it commits with `--no-verify` **after** its targeted suites pass (noted honestly). Have the verifier fix (or flag for a fix agent) any cross-phase breakage the implementing agent introduced before the next phase — otherwise the next agent builds on a broken base.
- **Chime when a phase lands.** Once you (the orchestrator) confirm the verifier's checkpoint committed cleanly, play a short sound so the user knows a phase is done — on macOS: `afplay /System/Library/Sounds/Glass.aiff`. **Play it from the orchestrator session, not a subagent** (only the main session reaches the user's speakers). Fire-and-forget; never let a missing audio tool fail the run.

## 4. Review (parallel, read-only, by dimension)

Spawn **independent reviewers in one message** (parallel), **`model: opus`** for the sharpest review, each a different lens, each told **read-only / do not edit** and to **verify against the real diff** (`git diff <base>..HEAD`) and the spec — not to hallucinate. Typical lenses for a full-stack change:
- **Security + multi-tenant isolation** — authz, RLS/tenancy, injection/XSS, upload validation, SSRF, secret/URL handling.
- **Correctness + lifecycle** — state machines, async/worker/queue paths, idempotency, migrations (up+down), enum/contract consistency, the headline invariants.
- **Frontend + integration** — query/cache invalidation, gating UI, generated-client sync, a11y/UX, error handling.

Ask each for **structured findings**: `[Severity] file:line — issue — why — concrete fix`, plus an overall verdict.

## 5. Fix (sonnet agents, no file overlap)

Triage findings into **non-overlapping work sets** (e.g. API-only vs web-only) so agents can run in parallel **without editing the same files** — concurrent edits to one file corrupt each other. `model: sonnet`. Give each the exact finding + file:line + the reviewer's suggested fix. Then re-verify (build + tests) and commit. Don't blindly apply every Low — judge.

## 6. Manual test on a REAL stack — the part people skip

Unit tests with mocks are not enough. Stand up the real thing and exercise it. **Delegate the stack bring-up and API smoke test (§6a–6b) to the opus verifier agent; delegate the UI pass (§6c) to a sonnet agent.** You orchestrate and gate — you don't run curl or the browser yourself.

### 6a. Bring up the stack
The opus verifier agent starts infra (containers: db/redis/object-store/any service deps), runs **migrations + seed**, then starts **API + worker + web**. Verify each is healthy (`curl .../health`, web returns 200, worker logs "ready"). Standalone **workers often read raw `process.env`** (no dotenv) — pass DB/bucket/service env explicitly or they silently hit the wrong database.

- **Always bind to RANDOM/ephemeral ports, never the project's default ones.** Another orcaz run (or another agent) may be exercising the same repo in parallel and squatting the defaults — a fixed port is a guaranteed collision and cross-contamination. Pick a high random port per service at bring-up (and a unique DB name / object-store bucket / Redis prefix where the stack allows it), then thread those choices through: point the web's API base URL at the API's chosen port, and **allow the web origin in CORS** (cookies are port-agnostic on localhost, but CORS is origin-specific). Record the ports you chose so §6b/§6c hit the right ones and §8 tears down exactly what you started.

### 6b. Smoke-test the REAL API with curl first (highest signal, fastest)
Before the browser, the opus verifier hits the actual endpoints — this isolates API bugs from UI bugs:
```bash
TOK=$(curl -s -X POST .../auth/login -d '{...}' | jq -r .accessToken)
curl -s -H "Authorization: Bearer $TOK" .../resource | jq          # happy path
curl -s -o /dev/null -w "%{http_code}\n" -X PATCH ... .../gated     # assert the EXACT status (e.g. 402 vs 403)
```
- Set up **real data + real states**: create accounts via the signup API; flip plan/entitlement/role states directly in the DB when needed (respect RLS — set the tenant GUC in-session; flush the entitlements cache after). Test the states the UI can't easily reach.
- Exercise **async paths end-to-end**: enqueue the job, poll the status field, read the worker logs. Verify the **failure path too** (kill/stop a dependency → confirm retries → confirm the visible failed state) — a failure path you can actually reproduce is as valuable as the success path.

### 6c. Drive the REAL UI with playwright-cli
Delegate browser testing to a **`model: sonnet`** subagent that invokes the **playwright-cli** skill (it has it), or drive it yourself if the flow is fragile and you need to react. Give precise, numbered steps with **expected vs actual**, real credentials, and a screenshot dir (e.g. `/tmp/<x>-shots/`). Cover:
- The happy path for the privileged state (e.g. paid plan) AND the gated state (e.g. free plan shows locks/upgrade prompts, disabled — not just hidden — controls).
- **Prove dynamic behavior, don't assume it**: to prove "updates without reload", plant an in-page marker (`window.__marker = 1`) and confirm it survives the interaction; inspect the actual DOM/CSS-vars/computed styles, not just a screenshot.
- The async UI states (loading/generating → done/failed → retry), with **polling** so the UI actually advances.
- **Capture the browser console** and report JS errors.
- Demand a **structured report**: per step PASS/FAIL/PARTIAL + what was observed + screenshot filename.

Triage what the real-stack testing surfaces (these are the bugs unit tests miss — e.g. cache-invalidation/refresh gaps, layout clipping, wrong HTTP codes) to sonnet fix agents; the opus verifier then re-verifies and commits.

## 7. Ship — integrate to the DEFAULT branch and push

**Pushing to the default branch is the definition of "done." Never report the work as done, finished, complete, or shipped until it is merged into the repo's default branch AND pushed to the remote — a green feature branch is not done.** The ONLY acceptable stopping points short of that are: there is no remote (nothing to push to), or the user explicitly told you to stop before shipping. In every other case, finishing the loop means completing this step. Do it as the final, deliberate step — only after everything is committed and every checkpoint is green.

1. **Confirm green + clean.** Working tree clean (`git status`), builds/tests pass, branch holds all the checkpoint commits.
2. **Find the default branch and remote**, don't assume "main":
   ```bash
   git remote get-url origin                                   # is there a remote at all?
   git remote show origin | sed -n 's/.*HEAD branch: //p'      # the real default (main/master/develop)
   ```
   If there's **no remote**, say so and stop — there's nothing to push to; report the branch is ready to push once a remote exists.
3. **Integrate.** Prefer the path the repo actually uses:
   - **PR-based repos** (most): push the feature branch (`git push -u origin <branch>`), open a PR with `gh pr create` (title + body summarizing phases, review, and manual-test evidence), then **merge it** (`gh pr merge --squash` or per repo convention). The merge is what lands it on the default branch.
   - **Direct-push repos** (no PR flow / solo): `git checkout <default> && git pull --ff-only && git merge --no-ff <branch> && git push origin <default>`.
4. **Verify it landed**: `git log --oneline origin/<default> -5` shows the work; the PR shows merged.
5. **Pushing to a shared default branch is outward-facing and hard to reverse** — confirm with the user before the merge/push **unless** they've already said to ship to default (this skill being invoked with that standing instruction counts). Never force-push a shared branch. If CI runs on the PR, let it pass before merging.
6. **Chime on the ship.** Once the work has actually landed on the default branch and the push succeeded, play the completion sound from the orchestrator session — on macOS: `afplay /System/Library/Sounds/Glass.aiff` (use a distinct sound from the per-phase chime if you want, e.g. `Hero.aiff`, so "shipped" sounds different from "phase done"). Fire-and-forget; a missing audio tool must never fail the ship.

## 8. Tear down — stop everything you started

**After the push lands, leave no running processes behind.** The manual-test stack and any background tasks were only for verification — once the work is on the default branch they must all be stopped:

- **Stop every server/process the testing brought up** — API, worker, web dev server. Kill the background shells you launched and free the alternate/random ports you ran on. Don't leave an orphaned dev server squatting on a port for the next session.
- **Stop and remove every Docker container/DB this run started** — the db, redis, object-store, pdf, and any other infra the verifier spun up in §6a. Take down the compose stack with `docker compose down` (add `-v` if you created throwaway volumes for this run); for hand-started containers, `docker stop` then `docker rm` them. Scope the teardown to **only what this run created** (use the project/run name or the specific container ids you started — never blanket-kill another agent's containers). Don't leave a Postgres/Redis container holding a port or RAM after the work has shipped.
- **Close out the tracking tasks** — mark the TaskCreate/TaskUpdate phases completed (or cancelled if dropped) so nothing is left dangling `in_progress`.
- **Confirm it's clean** — `docker ps` shows none of this run's containers still up, no stray listeners on the ports you used (`lsof -i`), no leftover volumes from this run.

Report the final result: the commit/PR URL on the default branch, a one-line summary of what shipped, and confirmation that the test stack and tasks are torn down.

## Principles

- **Verify, don't trust — but delegate the verifying.** The orchestrator never re-runs builds/tests/coverage by hand; it launches an **opus verifier agent** that re-runs them at every checkpoint and commits. A subagent saying "94 tests pass, 95% coverage" is a claim until the verifier sees it. The orchestrator's own hands touch nothing but the final push to default (§7).
- **Both layers of testing, always.** Unit/integration tests with **good coverage of the new logic** (gates, branches, error/failure paths — not just happy path) are the base and ship *with* the code in each phase; the real-stack API+UI pass is the top. One without the other is incomplete: mocks prove the unit, the live stack proves the feature.
- **Real API + real UI.** curl the live endpoints and assert exact status codes; drive the actual browser. Mocked tests prove the unit; the stack proves the feature.
- **Evidence.** Screenshots, status-code assertions, worker logs, surviving in-page markers — not "looks fine".
- **Right-size the work.** No agent gets a giant chunk — split an oversized phase into cohesive, individually testable bites before dispatching, but don't shred it into trivial micro-tasks. The sweet spot is one slice an agent can finish well and a verifier can checkpoint in one round.
- **No-overlap parallelism.** Parallel agents must not touch the same files; split by area.
- **Honest reporting.** Say what was tested vs untested and why (e.g. "success path mocked because the image wouldn't pull; failure path verified live"). Don't paper over gaps.
- **Scale effort to the ask.** A small change needs one implementer + a quick curl + a screenshot; a multi-phase epic needs the full loop.
- **Finish the job.** "Done" means landed on the default branch and pushed to the remote — full stop. A green feature branch is NOT done; never call the work done/finished/shipped until §7 has actually merged to default and pushed. The only exceptions are no remote, or the user told you to stop short.
- **Leave no mess.** After the push, tear down everything the testing started — servers, workers, containers, background shells, alternate ports — and close out the tracking tasks (§8). Done means shipped *and* cleaned up, not a pile of orphaned dev servers.

## Anti-patterns

- Trusting subagent "all green" and committing without re-running anything.
- Parallel fix agents editing the same file → corrupted edits.
- "Tested" meaning only unit tests with mocks — never started the app.
- "Tested" meaning only the real stack — no unit tests / new code left largely uncovered (happy-path-only tests that skip the gate/error/failure branches).
- Screenshot-only UI claims with no DOM/marker proof of dynamic behavior.
- Leaving cross-phase breakage for the next agent to build on.
