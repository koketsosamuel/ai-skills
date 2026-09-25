# Photos — placeholders now, the real image from the owner later

Claude does not invent, generate or download photographs for lessons. Where a real photo is
needed (graphics.md has the test), the lesson gets a **placeholder** and the owner gets a
**shopping list**. The owner finds or takes the photo and uploads it through the admin.

## Why not just grab one

- Copyright: most images online are not free to reuse; textbooks and past papers are copyrighted.
- Accuracy: an AI-made "photo" of a specimen, rock or historical scene is a fabrication, and a
  learner cannot tell.
- Consent: a recognisable child needs written consent from a parent or guardian.
- Uploads go through the admin's image pipeline (decoded, resized, stored immutably). That
  needs the owner signed in, which Claude never does.

## In the build script

```js
import { photo, writePhotoRequests, image } from '../../../../kit/blocks.mjs'; // from src/NN-name/

blocks.push(
  photo('onion-cells', {
    shows: 'Red onion skin cells under a light microscope at x400, in tap water and in salt water',
    why: 'Learners see real cells shrink, which a drawing cannot prove',
    alt: 'Two microscope views of red onion cells. In salt water the purple part has shrunk away from the cell wall.',
    caption: 'Onion cells in tap water (left) and in salt water (right).',
    orientation: 'landscape',          // 'portrait' | 'square'
    label: 'Onion cells under a microscope',   // ≤ 40 chars, shown inside the frame
  }),
);
// …after all lessons are written:
writePhotoRequests(topicDirPath);      // → <topic-folder>/photos.json
```

- `id`: kebab-case, unique across the whole build (`photo-needed-<id>` becomes the svg's `id`,
  the one attribute that survives the sanitizer, so the placeholder is findable in the database).
- `shows`: specific enough that someone can find or shoot exactly that (subject, angle, what must
  be visible). `why`: the teaching reason. `alt`: what a screen reader says (describe, don't
  interpret). `caption`: what the learner should notice — the same caption the real photo keeps.
- The placeholder draws a neutral "Photo coming soon" frame, readable in both themes.
- Put the teaching in the text around it: a lesson must still make sense before the photo arrives.
- Ask for a photo only where it earns its place: typically 0–2 per lesson, none in maths.

## After building

```
node <kit>/photos.mjs <set>/IMAGES-NEEDED.md <set>/<topic-folders…>
```

It lists every placeholder with lesson, position, what to show, alt text and caption, plus where
to find images legally and how to swap one in. It fails if a placeholder has no request or a
request is unused.

The loader (`scripts/lessons/load.sh`) inserts a lesson that still holds a placeholder **hidden**
(`is_active = false`) in every environment, so "Photo coming soon" never reaches a learner.

## When the photo arrives — production is where it matters

Uploads live in each environment's own storage bucket, so a photo uploaded locally does not exist
in production. The owner uploads in the **production** admin (where learners are). Then:

1. The owner gives you the uploaded photo's public https URL (from the admin image block).
2. In the source, replace `photo('<id>', {…})` with
   `image({ url: '<https URL>', alt: '<same alt>', caption: '<same caption>' })` — every
   environment now shows the same file. Don't use `imageId`: it only means something in one
   database.
3. Rebuild, run the gates, regenerate IMAGES-NEEDED.md (the photo drops off the list).
4. The production lesson was edited in the admin, so the loader protects it. Give the owner
   `DATABASE_URL=<prod> ./scripts/lessons/load.sh <set> --overwrite-edited=<lesson id>` and ask
   them to switch the lesson on in the admin once every photo it needs is in.

## Tell the owner — every time

The final report ends with the photo list: how many, which lessons, and the path to
IMAGES-NEEDED.md, and says plainly that those lessons stay hidden until the photos are in.
The owner can:

1. Upload each photo in the production admin lesson editor (Image block above the placeholder →
   upload → paste alt and caption → delete the placeholder → save), then hand Claude the photo URLs
   so the source catches up (above), or
2. Put the files in a folder named by id (`photos/onion-cells.jpg`) and ask Claude to prepare the
   swap — the upload itself still needs the owner signed in to the admin.

## Where the owner can get photos (put this in the report when asked)

- Their own photos, or a colleague's with permission.
- Wikimedia Commons: public domain, CC0, CC BY, CC BY-SA. CC BY / BY-SA need a credit in the
  caption ("Photo: Jane Doe, CC BY-SA 4.0").
- Unsplash, Pexels: free licences.
- Not Google Images, textbook or past-paper scans, news sites, or AI image generators for
  anything presented as real.
