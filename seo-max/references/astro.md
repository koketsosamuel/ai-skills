# Astro SEO playbook

Verified against Astro v6/v7 docs and npm (July 2026; v7.0.7 current). Astro 6 removed legacy content collections and `<ViewTransitions />` (now `<ClientRouter />`); Astro 7 swapped the markdown pipeline (Sätteri) and stopped auto-correcting invalid HTML nesting. Many online guides target 5.x — check the project's major version before applying version-specific advice.

## Why Astro wins by default — and the four ways it loses

Zero-JS static HTML + islands means crawlers get complete markup and CWV is nearly free. The failure modes are all opt-in:

1. **`client:only` islands skip server rendering entirely** — headings, copy, or links inside them are invisible in the initial HTML. Content never goes in `client:only`.
2. **`<ClientRouter />` (view transitions)** turns the MPA into a soft SPA: bundled scripts run once, analytics pageviews stop firing. Fix: listen for `astro:page-load` or mark scripts `data-astro-rerun`.
3. **SSR/on-demand routes**: HTML is still server-rendered, but `@astrojs/sitemap` cannot include SSR dynamic routes (prerendered pages only) — use `customPages` or a hand-rolled sitemap endpoint.
4. **Synchronous third-party scripts** (consent managers, chat widgets) — the top CWV killer on otherwise-fast Astro sites; defer or offload (Partytown).

## The canonical config

```js
// astro.config.mjs
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
export default defineConfig({
  site: 'https://example.com',   // REQUIRED — without it sitemap errors and canonicals break
  trailingSlash: 'never',        // default 'ignore' is a duplicate-content footgun; pick one
  integrations: [sitemap({
    filter: (page) => !page.includes('/drafts/'),
    i18n: { defaultLocale: 'en', locales: { en: 'en-US', fr: 'fr-CA' } }, // emits xhtml:link hreflang
  })],
});
```

- Missing `site` is the single most common Astro SEO bug.
- `trailingSlash` must agree with `build.format` (`'directory'` → slash URLs, `'file'` → `.html`) and with every internal link.
- Sitemap outputs `sitemap-index.xml`; reference that absolute URL from robots.txt.

**robots.txt**: static `public/robots.txt` for 95% of sites. When it should derive from `site` (multi-env), use the documented endpoint:

```ts
// src/pages/robots.txt.ts
import type { APIRoute } from 'astro';
export const GET: APIRoute = ({ site }) =>
  new Response(`User-agent: *\nAllow: /\n\nSitemap: ${new URL('sitemap-index.xml', site)}`);
```

Do NOT install `astro-robots-txt` — dead since Sept 2023 despite tutorials still recommending it.

## Head management: hand-rolled SEO component

Astro has no built-in head manager (claims that v6 added one are wrong). Best practice is a hand-rolled `SEO.astro` in the base layout — zero dependency risk, exactly as capable as any package. (`astro-seo` v1.1.0 is maintained and fine if the project already uses it; `@astrolib/seo` is stale — avoid.)

```astro
---
interface Props { title: string; description: string; image?: string; noindex?: boolean; type?: string; }
const { title, description, image = '/og-default.png', noindex = false, type = 'website' } = Astro.props;
const canonical = new URL(Astro.url.pathname, Astro.site);  // pathname only — strips query params
const ogImage = new URL(image, Astro.site);
---
<title>{`${title} | Site Name`}</title>
<meta name="description" content={description} />
{noindex ? <meta name="robots" content="noindex, nofollow" /> : <link rel="canonical" href={canonical} />}
<meta property="og:title" content={title} />
<meta property="og:description" content={description} />
<meta property="og:url" content={canonical} />
<meta property="og:image" content={ogImage} />
<meta property="og:type" content={type} />
<meta name="twitter:card" content="summary_large_image" />
```

Refinements: omit canonical when `noindex` (as above); `og:url` must equal the canonical; Twitter tags fall back to OG for everything except `twitter:card`.

## JSON-LD

Officially documented pattern — `set:html` + `JSON.stringify` (avoids Astro processing the script, escapes safely):

```astro
<script type="application/ld+json" set:html={JSON.stringify({
  '@context': 'https://schema.org',
  '@type': 'BlogPosting',
  headline: post.data.title,
  datePublished: post.data.pubDate.toISOString(),
  dateModified: (post.data.updatedDate ?? post.data.pubDate).toISOString(),
  mainEntityOfPage: new URL(Astro.url.pathname, Astro.site).href,
})} />
```

One small schema component per collection type (`BlogPostingSchema.astro`, `ProductSchema.astro`) mapping frontmatter → schema fields; site-wide `WebSite`/`Organization` in the base layout. Link entities via `@id` (WebSite ↔ Person ↔ BlogPosting ↔ BreadcrumbList) rather than isolated blobs.

## Content collections as the SEO pipeline

Zod is the underrated SEO tool: SERP-unsafe frontmatter fails the build.

```ts
// src/content.config.ts
schema: ({ image }) => z.object({
  title: z.string().max(65),                 // SERP-safe title length, enforced at build
  description: z.string().min(70).max(200),  // real meta description, enforced
  pubDate: z.coerce.date(),
  updatedDate: z.coerce.date().optional(),
  heroImage: image().optional(),
  draft: z.boolean().default(false),
  noindex: z.boolean().default(false),
}),
```

One flow: `[...slug].astro` → `getCollection` → `entry.data` spreads into `<SEO>` + JSON-LD + OG-image URL. Filter drafts out of routes, sitemap, RSS, and llms.txt from the same predicate.

## Images, RSS, OG images, redirects, 404, i18n

- **Images**: `<Image />`/`<Picture />` from `astro:assets` — emits dimensions (CLS) and lazy-loads. The one override that matters: the LCP hero needs `loading="eager"` + `fetchpriority="high"` (default lazy-load on the hero is an LCP regression). Remote images need `image.domains` allowlisting.
- **RSS**: `@astrojs/rss` endpoint at `src/pages/rss.xml.js` from the same collection; add autodiscovery `<link rel="alternate" type="application/rss+xml">`. Full-content feeds also serve AI-agent consumption.
- **OG images**: `astro-og-canvas` (maintained, Starlight-core author) or DIY satori + resvg in an image endpoint (`src/pages/og/[...slug].png.ts`), 1200×630.
- **Redirects**: `redirects: { '/old': '/new' }` in config — but static output emits meta-refresh pages; prefer host-level redirects (adapter/Netlify/Vercel) for real 301s on migrations.
- **404**: `src/pages/404.astro` served with a real 404 status. Never redirect 404s to home (soft-404s).
- **i18n**: Astro's i18n routing does NOT emit hreflang — wire it yourself via the sitemap `i18n` option (xhtml:link) and/or `<link rel="alternate" hreflang>` tags incl. `x-default`. Each locale self-canonical.

## llms.txt in Astro

Zero-dependency endpoint from the same collections (packages: `astro-llms-md` is maintained; `starlight-llms-txt` for Starlight docs; original `astro-llms-txt` is dead):

```ts
// src/pages/llms.txt.ts
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
export const GET: APIRoute = async ({ site }) => {
  const posts = (await getCollection('blog', ({ data }) => !data.draft))
    .sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
  const body = `# Site Name\n> One-line description\n\n## Posts\n${posts
    .map((p) => `- [${p.data.title}](${new URL(`/blog/${p.id}/`, site)}): ${p.data.description}`)
    .join('\n')}`;
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
```

Format, honest expectations, and the robots.txt AI-crawler stance: see [llms-txt.md](llms-txt.md).

## Top Astro SEO mistakes

1. `site` unset → broken sitemap and canonicals (the #1).
2. `trailingSlash: 'ignore'` left as-is + mixed internal link styles → duplicate content.
3. Analytics dead after `<ClientRouter />` (no `astro:page-load` listener).
4. Content inside `client:only` islands.
5. Expecting SSR routes in `@astrojs/sitemap` output.
6. Lazy-loaded hero (LCP) or plain `<img>` without dimensions (CLS).
7. Installing dead packages (`astro-robots-txt`, `@astrolib/seo`) off stale tutorials.
8. `og:url` ≠ canonical; canonicals carrying query params.
9. 404 redirecting to home.
10. i18n routing without hreflang wiring.
