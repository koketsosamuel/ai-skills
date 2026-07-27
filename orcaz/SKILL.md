---
name: orcaz
description: Orcaz — orchestrate a large/multi-phase feature build as the conductor of subagents. Implement + unit-test with cheap subagents, review with parallel reviewer agents, fix, then validate against the REAL running stack (curl the API, drive the UI with playwright-cli), log out-of-scope bugs to a findings doc, then ship to the repo's default branch. Use when the user says "orcaz", or asks to "implement all phases / use subagents / orchestrate / you are the orchestrator". Do NOT self-trigger on merely-large tasks — orcaz merges and pushes, so it requires the explicit ask.
---

# orcaz — build+test → review → fix → real-stack test → ship

You are the **orchestrator**: decompose, dispatch, gate. Subagents implement; a **JUDGE verifier agent** independently re-runs builds/tests/coverage and commits checkpoints. Subagent reports are claims until the verifier re-runs them. Your own hands touch nothing but the brief, the findings log, and the final push.

**Prereq:** a written spec (phase docs / plan / issue). None → write one first; every implementer is pointed at it.

**Model tiers:** BUILDER = `sonnet` (implement / fix / UI-drive); JUDGE = `opus` (review / verify). Small models (`haiku`, GPT-mini class) only for trivial mechanical side-tasks — never implementation, fixes, review, or verification. Never `fable`/Mythos-class for subagent work. If neither sonnet nor opus is offered, stop and ask.

## 0. Two audiences — terse up, verbose down

**To the user: near-silent.** One line per landed milestone, then the final report. No narration, no plan restatement, no relaying subagent reports, no code blocks, no "next I will…". Ask only when genuinely blocked.

```
P1–P3 ✅ 14 files, cov 91% · abc123
review ✅ 3 High 5 Med → fixed · def456
stack ✅ API 12/12, UI 9/9 · 2 deferred → docs/orcaz-findings.md
shipped ✅ main@ef01234
```

**To subagents: exhaustive.** They start blank — every prompt carries the full task, exact commands, constraints, and the report schema.

**The brief (do this once, before dispatching).** Write `<scratchpad>/orcaz-brief.md`: branch, spec paths, package manager, build/lint/test/coverage/codegen commands, migration numbering, repo rules (CLAUDE.md gate policy), stack bring-up notes, resource limits (§0a), report schema. Every subagent prompt then reads: *"Read `<path>/orcaz-brief.md` first. Your slice: …"* — shared context is written once, not re-tokenized per agent. Update it as facts change.

**Context economy.** Never read raw build/test/server logs, full diffs, or whole coverage tables into your own context. Demand **structured summaries** (verdict + failures + key numbers, not transcripts); when you must check a log, `tail`/`grep` it, never `cat`. Point subagents at **paths**, never paste spec content. Cap every report: **≤15 lines, no log dumps** — evidence as pointers (file:line, screenshot path, exit code).

### 0a. Resource discipline — fast without thrashing RAM

Builds and test suites are the RAM hogs; parallelism *there* is what kills the machine, not parallel editing.

- **One heavy job at a time.** Parallel BUILDERs edit disjoint files but must **not** each run the full suite — implementers run only their slice's tests, path-filtered. Full suite + build = the verifier's job, once per batch.
- **Cap workers, don't let the runner autodetect cores**: `vitest --pool=forks --poolOptions.forks.maxForks=2` / `jest --maxWorkers=2` (`--runInBand` if RAM is tight), `NODE_OPTIONS=--max-old-space-size=4096`. Put the exact command in the brief so every agent uses it.
- **Batch checkpoints.** Verify + commit once per batch of independent phases, not once per agent — each commit costs a full gate run.
- **Don't double-run the gate.** If the pre-commit hook runs lint+test, let it; don't run the same suite manually first.
- **Incremental, not clean.** `tsc -b` / cached builds; never reinstall deps or wipe build caches to "be safe".
- **Stack up once** (§6), shared by API and UI passes, torn down at the end — never per subagent. Stop dev servers before a full-suite run if memory is tight.

## The loop

```
spec → branch + brief + tasks
  └─ per phase batch (serial if dependent, parallel if disjoint):
       implement + UNIT TEST (BUILDER, pointed at brief + spec — code AND tests together)
       → CHECKPOINT (per batch): JUDGE verifier re-runs build + tests + coverage → commits
  → review (parallel JUDGE reviewers by lens, read-only)
  → triage → fix in-scope (BUILDER, no shared files) → JUDGE re-verifies → commits
       → log out-of-scope findings to the findings doc (§5b)
  → manual test: JUDGE brings up stack + curls REAL API; BUILDER drives REAL UI (playwright-cli)
       → fix breaks (BUILDER) → JUDGE re-verifies → commits
  → SHIP: YOU merge to the repo's DEFAULT branch and push
  → TEAR DOWN: stop everything started + close tracking tasks
```

Track phases with TaskCreate/TaskUpdate.

## 1. Set up

Branch first (`git checkout -b feat/<x>`) — never build big on default. Recon the repo: package manager, build/lint/test/codegen commands, migrations, how the app launches. Write the brief (§0).

## 2. Implement + unit-test (BUILDER subagents)

- **Right-size:** one cohesive, individually testable slice per agent (e.g. one endpoint + service + migration + tests; one screen + query wiring + tests). Split sprawling phases first; don't shred into micro-tasks either — aim for a bite one agent finishes well and a verifier checkpoints in one round.
- Work **on the branch, not a worktree**; agents do **NOT commit** (the verifier does, so you control gating).
- Serial where phases share files or migration numbers; parallel only with disjoint file sets.
- **Tests ship with the code — not a later phase.** Require good coverage of the new logic: every branch, error path, gate (assert exact HTTP status), state transition — not just happy path. Push logic into pure IO-free functions. Agent runs **its slice's tests only** (path-filtered, capped workers) and reports numbers.
- Prompt must include: brief path, spec file **paths**, "discover real state first" (latest migration number, existing helpers, test runner), and the **report schema**: files changed, commands + PASS/FAIL, coverage % for new files, untested + why, deviations, out-of-scope bugs noticed (file:line + one line). ≤15 lines, no logs.
- API contract changed → regenerate the typed client **before** web work.

## 3. Checkpoint — JUDGE verifier re-runs, then commits

Never trust an implementer's "all green". **One checkpoint per batch of phases**, not per agent. The verifier re-runs: builds, the affected tests, coverage on the changed code, and confirms the files exist (`git diff --stat`). It reports a **summary verdict**, not logs.

- **Coverage gate:** new logic well covered incl. error/gate branches — eyeball the per-file report, not a global %. Gaps → bounce to a fix agent before proceeding.
- **The repo's commit-gate policy outranks this skill**: if CLAUDE.md says the pre-commit gate must be green, fix the gate — never `--no-verify` past it except where the repo's own docs sanction it (noted honestly). Batch commits so the gate runs a handful of times, not per file.
- Verifier fixes/flags cross-phase breakage before the next batch builds on it.
- **Chime per landed batch** (orchestrator session, fire-and-forget): `afplay /System/Library/Sounds/Glass.aiff`.

## 4. Review (parallel JUDGE, read-only, by lens)

Spawn reviewers **in one message**, each a different lens, read-only, verifying against the real diff (`git diff <base>..HEAD`) + spec. **Derive lenses from what the change touches**; typical full-stack trio: security/tenancy·RLS, correctness/lifecycle (state machines, async/queues, idempotency, migrations up+down), frontend/integration (cache invalidation, generated client, a11y). Demand structured findings, one line each: `[Severity] file:line — issue — why — fix`, plus an `IN-SCOPE / OUT-OF-SCOPE` tag per finding; cap at the top ~10 per lens. If the harness offers the **Workflow tool**, the review→verify fan-out fits it well (invoking this skill is the orchestration opt-in).

## 5. Fix (BUILDER, no file overlap)

Triage into **non-overlapping work sets** (e.g. API vs web) — parallel agents must never edit the same file. Give each the exact finding + suggested fix. Judge Lows; don't blindly apply. Then verifier re-verifies + commits (one commit per fix batch).

### 5b. Out-of-scope findings → a committed markdown log

Real bugs surface that this run will **not** fix: pre-existing defects, tech debt, flaky tests, findings outside the spec's scope, deferred Lows. **Never drop them and never silently expand scope to fix them.** Write them down.

- **File:** `docs/orcaz-findings.md` if `docs/` exists, else `ORCAZ-FINDINGS.md` at repo root. **Append** a run section — never rewrite prior sections.
- **You write it** (cheap, prose only) from subagent reports; don't spawn an agent for this.
- Log a finding when it is a **real, reproducible defect or risk** — not a style opinion, not a hypothetical. Nothing found → don't create the file.
- Commit it with the run's work (same batch commit is fine).

```markdown
## <YYYY-MM-DD> — <feature/branch>

### [High] Tenant filter missing on export query — `api/src/export/export.service.ts:88`
- **Symptom:** cross-tenant rows returned when `?all=true`; hit during §6b API pass.
- **Repro:** `curl -H "Authorization: Bearer $T_A" '<api>/export?all=true'` → returns tenant B rows.
- **Suggested fix:** add the RLS tenant GUC set in `withTenant()` (mirrors `report.service.ts:41`).
- **Deferred because:** pre-existing on `main`, outside this spec's scope; needs its own phase + migration.
```

Severity in the heading (`Critical/High/Med/Low`), one file:line anchor, and the four bullets — symptom, repro, suggested fix, why deferred. Keep each entry ≤6 lines.

Surface only the **Critical/High** count to the user in the run line, with the file path — not the contents.

## 6. Manual test on a REAL stack — the part people skip

Delegate: stack bring-up + API smoke (§6a–b) → JUDGE verifier; UI pass (§6c) → BUILDER, **reusing the same running stack**. You gate; you don't curl or browse yourself.

### 6a. Bring up (once per run)
Start infra (db/redis/object-store/etc.), migrate + seed, start API + worker + web; health-check each. Standalone workers often read raw `process.env` — pass env explicitly. **Random/ephemeral ports always, never defaults** (parallel runs collide): unique DB name / bucket / Redis prefix too; thread the API port into the web base URL and **CORS**; record the ports in the brief for §6b–c and teardown.

### 6b. curl the REAL API first (fastest signal, isolates API vs UI bugs)
Login for a token; hit happy paths; **assert exact status codes** on gated paths (402 vs 403). Create real data via the API; flip roles/plans directly in DB when needed (set tenant GUC, flush caches). Exercise async paths end-to-end incl. the **failure path** (kill a dependency → retries → visible failed state).

### 6c. Drive the REAL UI (playwright-cli)
BUILDER subagent invoking the **playwright-cli** skill against the already-running stack; precise numbered steps, expected vs actual, real creds, screenshot dir. Cover: privileged AND gated states (disabled, not just hidden); **prove dynamic behavior** (in-page marker `window.__marker=1` survives the interaction; inspect DOM/computed styles, not just screenshots); async UI states with polling; **capture browser console**. Report: per step PASS/FAIL + observed + screenshot filename — errors only, no console dumps.

Triage what surfaces (cache-invalidation gaps, wrong codes, clipping) → in-scope → BUILDER fixes → verifier re-verifies + commits; out-of-scope → §5b.

## 7. Ship — merge to DEFAULT and push

**"Done" = merged into the default branch AND pushed.** Only stopping points short of that: no remote, or the user said stop.

1. Green + clean: `git status` clean, builds/tests pass.
2. Find the real default + remote (`git remote show origin | sed -n 's/.*HEAD branch: //p'`). No remote → report branch ready, stop.
3. Integrate per repo convention: PR repos → push branch, `gh pr create`, merge it. Direct-push repos → `git checkout <default> && git pull --ff-only && git merge --no-ff <branch> && git push`.
4. Verify landed: `git log --oneline origin/<default> -5`.
5. **Invoking this skill is standing authorization to merge to default and push — do not stop to ask for confirmation.** Never force-push shared branches; let PR CI pass first.
6. Chime the ship: `afplay /System/Library/Sounds/Hero.aiff` (fire-and-forget).

## 8. Tear down

After the push: kill every server/worker/dev-server and background shell this run started; `docker compose down` (+`-v` for throwaway volumes) or stop/rm the specific containers — **scope to this run only**, never another agent's. Close out tracking tasks. Confirm clean (`docker ps`, `lsof -i` on your ports).

**Final report — ≤5 lines:** commit/PR URL · one-line summary · tests (unit + stack) · deferred findings count + file path · teardown confirmed.

## Principles

- **Verify, don't trust — delegate the verifying.** Claims become truth only when the JUDGE verifier re-runs them.
- **The repo's rules outrank this skill** (gate policy, branch flow, coverage bar).
- **Both test layers, always:** unit tests with real branch/failure coverage AND the live-stack pass. Mocks prove the unit; the stack proves the feature.
- **Evidence, not vibes:** exact status codes, markers, screenshots, worker-log pointers.
- **Terse up, verbose down** — milestone lines to the user; full context to subagents, written once in the brief.
- **Context economy:** summaries and pointers up; never raw logs into the orchestrator.
- **One heavy job at a time:** parallel edits, serialized builds/suites, batched gates.
- **Found ≠ fixed, but found ≠ forgotten** — out-of-scope bugs get logged, not silently fixed or dropped.
- **No-overlap parallelism**; **right-size the slices**; **honest reporting** (tested vs untested + why); **scale effort to the ask**.
- **Finish the job** (merged + pushed = done) and **leave no mess** (teardown + closed tasks).

## Anti-patterns

Trusting "all green" without a verifier re-run · parallel agents each running the full suite (RAM death) · a gate run per file instead of per batch · clean rebuilds / dep reinstalls "to be safe" · repeating shared context in every subagent prompt instead of the brief · narrating progress to the user · parallel agents editing one file · "tested" = mocks only, app never started · "tested" = stack only, new code uncovered / happy-path-only tests · screenshot-only UI claims · silently expanding scope to fix an unrelated bug — or dropping it instead of logging it · leaving cross-phase breakage for the next agent · reading full logs/diffs into the orchestrator context.
