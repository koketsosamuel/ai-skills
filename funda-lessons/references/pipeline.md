# Pipeline — a lesson set from source to production

Every lesson is written **for production from the first line**. Lessons are built in the Funda
repo as a *lesson set*, checked, loaded locally, checked on the phone, committed, and later loaded
into production by the owner with the same loader. The full contract is the repo's
`scripts/lessons/README.md` — read it at the start of every run; it wins over this file if they
ever disagree.

`<kit>` below is `<Funda>/scripts/lessons/kit`. The kit renders maths with the API's own MathJax
install and imports the API's own maths parser, so a check is what the phone receives.

## A set

```
scripts/lessons/<subject-slug>/grade-<n>/
  lessons.config.json        grade, subject, publish, replacesTopics, topics[] (id, folder, name,
                             description, icon, category = paper, pacing = [term, weekStart, weekEnd],
                             lessons = { "<file>": "<lesson uuid>" })
  src/NN-<name>/build.mjs    the source; writes lesson JSON into ../../<topic-folder>/
  <topic-folder>/SS-LL-slug.json   { "title", "blocks" } — sorted order = lesson order
  <topic-folder>/photos.json       photo requests (writePhotoRequests)
```

- Build scripts are the source of truth; never hand-edit the JSON (the next build undoes it).
  Import the kit relatively: `import { p, h2, … } from '../../../../kit/blocks.mjs'`.
- `SS` = the source file's number, `LL` = the lesson within it; `00-00-introduction` opens a topic.
- `src/` folders run in name order, and a later one may rewrite a topic an earlier one wrote —
  number them deliberately.
- Draft in the session scratchpad if the work is exploratory, but the finished set lives in the
  repo. Never leave the only copy of lessons in a scratchpad.

## Production rules that shape the writing

- **Ids are forever.** Every topic and lesson has a fixed UUID in the config. The same id is the
  same lesson in every environment (share links, deep links, progress). New file →
  `node <kit>/generate-sql.mjs <set> --assign-ids` once. **Renamed file → move its id**, never
  mint a new one (production would get a second copy).
- **Nothing is ever deleted.** A lesson's progress, bookmarks and reading sessions cascade from
  it. Don't plan a restructure that needs deletes; retire a lesson by switching it off in the
  admin. Don't move a lesson between topics (the loader refuses: progress records the topic).
- **Topics** match CAPS teaching order. Production's topics come from the curriculum loader
  (`scripts/insert-topics-and-categories.sql`, broad FundaSA topics). A set that splits them
  into finer CAPS topics lists the broad names in `replacesTopics`, and the loader hides them.
  Check what production has for the grade and subject before choosing topic names — ask the owner
  if it would change what learners see.
- **The grade, subject and paper category must exist in production** (curriculum loader).
  Join is by name — use the exact names from `scripts/insert-*.sql`.
- **Publishing**: `"publish": true` inserts live on first load; after that `is_active` belongs to
  the admin. Lessons holding a photo placeholder always go in hidden.
- **Admin edits win.** The loader only updates a lesson whose stored content is a version the
  repo produced. After an owner edits a lesson in production (e.g. swaps in a photo), bring that
  change into the source and load with `--overwrite-edited=<id>`.
- **Photos are per environment** (each has its own bucket). Placeholders now; the owner uploads
  in the production admin; the source then references the upload by its https URL with
  `image({ url, alt, caption })` so every environment shows the same file (photos.md).
- **Never run anything against production yourself.** Loading production is the owner's step,
  with their credentials. Give them the exact command (below).

## Gates — all clean before loading

```
node <kit>/build.mjs <set>                                  # every src/*/build.mjs, then fit viewBoxes
node <kit>/check-math.mjs  <set>/<topic-folders…>           # every expression renders as the API renders it
node <kit>/check-svg.mjs   <set>/<topic-folders…>           # XML, viewBox, sanitizer allowlist, no tspans
node <kit>/check-contrast.mjs <set>/<topic-folders…>        # every label 4.5:1, light AND dark theme
node <kit>/validate.mjs    <set>/<topic-folders…>           # the admin editor's own schema + lint
node <kit>/render-svgs.mjs <png-dir> <set>/<topic-folders…> # then Read EVERY PNG
node <kit>/render-svgs.mjs --dark <png-dir> <set>/<topic-folders…>  # and every dark one
node <kit>/photos.mjs <set>/IMAGES-NEEDED.md <set>/<topic-folders…>
node <kit>/generate-sql.mjs <set> --assign-ids --out /dev/null   # ids for new files
```

Then read each lesson once as the learner would: every step shown, every term explained, every
piece of maths in `$…$`, one idea per lesson.

## Load locally and look (lead only)

```
./scripts/lessons/load.sh <subject>/grade-<n> --dry-run     # outcome, rolled back
./scripts/lessons/load.sh <subject>/grade-<n>               # local DB + local cache bump
node <kit>/api-check.mjs scripts/lessons/<subject>/grade-<n>   # what the API actually serves
```

Then the iOS Simulator (never Expo web): `xcrun simctl openurl <udid>
"fundasa://learn/lesson/<id>"`. Check diagrams, tables, maths on the text baseline, dark mode, a
reveal and a quickcheck.

- The app caches a lesson for 5 minutes (persisted) — pull to refresh after a load.
- `pnpm --filter @fundasa/database seed` truncates the local database; run `load.sh` again after.
- The lesson ETag is `updatedAt` + a renderer version (`math-vN`) in both
  `apps/api/src/modules/lessons/lessons.controller.ts` and mobile `hooks/useLessons.ts`. A change
  to what the API serves for UNCHANGED rows (sanitizer, maths renderer) needs both bumped.
- The local API rate-limits bursts; `api-check.mjs` paces itself.
- If the app wants a sign-in, ask the owner; never type a password.

## Hand-off

1. Commit the set (sources, JSON, config, IMAGES-NEEDED.md) — only when the owner asks, and never
   while other agents are writing.
2. Give the owner the production commands:

   ```bash
   DATABASE_URL=<prod> ./scripts/lessons/load.sh <subject>/grade-<n> --dry-run
   DATABASE_URL=<prod> VALKEY_URL=<prod valkey> ./scripts/lessons/load.sh <subject>/grade-<n>
   node scripts/lessons/kit/api-check.mjs scripts/lessons/<subject>/grade-<n> https://<prod api>
   ```

3. The photo list, and that those lessons stay hidden until the photos are in.
