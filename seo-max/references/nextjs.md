# Next.js SEO playbook

Verified against Next.js 16.2 docs (July 2026). App Router is the default; a short Pages Router mapping is at the end. If the project is on an older major, check which APIs exist before applying — `params` became a Promise and `middleware.ts` became `proxy.ts` in v16.

## Metadata API (App Router)

- Static values → `export const metadata: Metadata = {...}`. Dynamic → `export async function generateMetadata({ params, searchParams }, parent)`. Server Components only; never both from one segment; `searchParams` only in `page.tsx`. `await params` on v16+.
- `fetch` inside `generateMetadata` is memoized with the page's fetch — no double-fetch penalty. Use React `cache()` for non-fetch data.
- Call `notFound()` inside `generateMetadata` for phantom slugs — otherwise nonexistent URLs render a shell with default metadata (soft-404 factory).
- **Title template** in the root layout: `title: { template: '%s | Site', default: 'Site' }` — `default` is required or the template never applies. Escape hatch per page: `title: { absolute: '...' }`.
- **`metadataBase`** once in the root layout. Beware `new URL(process.env.VERCEL_URL)` leaking `*.vercel.app` preview hosts into production canonicals — hard-code the production origin or use `VERCEL_PROJECT_PRODUCTION_URL` gated on `VERCEL_ENV === 'production'`.
- Merging is **shallow** top-down: a page that sets any `openGraph` field replaces the parent's entire `openGraph` object. Share a spread from a common module when pages extend layout OG data.
- Canonical + hreflang per page:

```ts
alternates: {
  canonical: '/pricing',
  languages: { 'en-US': '/en-US/pricing', 'de-DE': '/de-DE/pricing', 'x-default': '/pricing' },
}
```

- `viewport`/`themeColor`/`colorScheme` moved out of `metadata` → separate `viewport` export / `generateViewport` (codemod: `metadata-to-viewport-export`).
- Streaming metadata (v15.2+): slow `generateMetadata` streams tags into the `<body>`. Fine for Googlebot; HTML-limited bots (facebookexternalhit, Twitterbot) are auto-detected and get blocking in-head metadata. Tune with `htmlLimitedBots` in next.config if OG scrapers misbehave.

## File conventions (all in `app/`)

| File | Serves | Notes |
|---|---|---|
| `sitemap.ts` | `/sitemap.xml` | Return `MetadataRoute.Sitemap`. Supports `alternates.languages` (hreflang in sitemap), `images`, honest `lastModified`. >50k URLs → `generateSitemaps()`. |
| `robots.ts` | `/robots.txt` | Return `MetadataRoute.Robots`; array of rules for per-bot policy (AI crawlers). Point `sitemap:` at the absolute sitemap URL. |
| `manifest.ts` | `/manifest.webmanifest` | PWA manifest. |
| `opengraph-image.tsx` / `twitter-image.tsx` | per-segment OG images | Return `ImageResponse` from `next/og`; export `alt`, `size` (1200×630), `contentType`. Satori: flex layout only, fonts via `fs.readFile`. Static `opengraph-image.png` + `.alt.txt` also works. |
| `favicon.ico`, `icon.png/svg/tsx`, `apple-icon` | icons | `favicon.ico` root-only and cannot be code-generated; `icon.tsx` can. |

File-based metadata overrides the `metadata` object for the same fields. Generate `sitemap.ts` from the same data source as the pages — only canonical, indexable, 200-status URLs.

## Rendering strategy

Google renders JS (median render-queue delay ~10s, tail hours), but Bing only partially and **AI crawlers mostly execute no JS at all** — server-rendered HTML matters more in the AI-search era, not less. Hierarchy: SSG ≥ ISR ≥ SSR (all SEO-equivalent in content terms) ≫ pure CSR.

`'use client'` is NOT CSR — client components still SSR on first load. What actually removes content from the HTML:

- Data fetched in `useEffect`/SWR/React Query with no server-rendered fallback.
- `next/dynamic` with `ssr: false` around indexable content.
- Hydration guards (`useIsMounted`, `typeof window` gates) around primary content.
- `noindex` in initial HTML — Google then skips rendering entirely; you cannot un-noindex from client JS.

Fix pattern: keep `page.tsx` a Server Component (so it can export metadata + render content), push interactivity into leaf client components. Verify with `curl <url>` — title, meta, content, and links must be in the raw HTML.

With Cache Components/PPR (`cacheComponents: true` + `"use cache"`), keep primary content and metadata in the static shell.

## JSON-LD

Official pattern — a native script tag in the page/layout Server Component body (not `next/script`, not the head; Google parses it anywhere in the DOM):

```tsx
<script type="application/ld+json"
  dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd).replace(/</g, '\\u003c') }} />
```

The `<` escape is the docs' own XSS mitigation. Type with `schema-dts` (`WithContext<Product>`). Organization/WebSite in root layout; Article/Product/BreadcrumbList/FAQPage per route, built from the same fetched data as the page.

## Core Web Vitals levers

- **LCP**: `priority` on the hero `next/image` (preload + no lazy-load); static/PPR shell; `loading.tsx`/Suspense so the shell paints early; `ReactDOM.preload`/`preconnect` for critical cross-origin assets (the Metadata API deliberately doesn't do resource hints).
- **CLS**: `next/image` enforces dimensions; `next/font` (self-hosted, `size-adjust` fallback metrics, `display: 'swap'`) kills font shift; reserve space for ads/embeds.
- **INP**: third-party JS is the #1 killer — `next/script` with `afterInteractive`/`lazyOnload`, `@next/third-parties` for GTM/GA/YouTube/Maps; push `'use client'` to leaves; React Compiler (stable v16, `reactCompiler: true`) for automatic memoization.
- v16 `next/image` default changes to audit on upgrade: `qualities: [75]`, `minimumCacheTTL` 4h, `images.domains` deprecated → `remotePatterns`.
- Measure with `useReportWebVitals` + CrUX field data, not lab scores alone.

## llms.txt

No built-in convention — use a route handler generated from the same content source as the sitemap:

```ts
// app/llms.txt/route.ts
export async function GET() {
  const posts = await getAllPosts()
  const body = [
    '# Site Name', '> One-line summary of the site.', '',
    '## Blog',
    ...posts.map(p => `- [${p.title}](https://site.com/blog/${p.slug}): ${p.summary}`),
  ].join('\n')
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'public, max-age=3600' } })
}
```

Add `app/llms-full.txt/route.ts` (full markdown content) for docs-heavy sites. Packages exist (`next-llms-txt`, `@turbodocx/next-plugin-llms`, `continuedev/next-geo` for per-page `.md` variants) but are young — the hand-rolled handler is the safe default. See [llms-txt.md](llms-txt.md) for format and honest expectations.

## i18n

No built-in App Router i18n routing. Pattern: `app/[lang]/` segment + locale redirect in `proxy.ts` (`Negotiator` + `@formatjs/intl-localematcher`); `next-intl` is the de-facto library and emits hreflang automatically. Declare hreflang in both page metadata (`alternates.languages` incl. `x-default`) and `sitemap.ts` entries. Sets must be bidirectional and self-referencing; each locale self-canonical — never canonicalize all locales to one language.

## Pagination

`rel=prev/next` is dead (Google ignores it since 2019). Each paginated page self-canonicalizes (build canonical from params in `generateMetadata`), stays indexable, and is internally linked. Never canonicalize page 2+ to page 1. Filter/sort query params → canonical to the clean URL.

## Top Next.js SEO mistakes

1. Preview/staging hostname in `metadataBase` → wrong canonicals in production.
2. Trailing-slash disagreement between `trailingSlash` config, canonicals, sitemap, and internal links → 308 chains + duplicate-content flags in GSC.
3. Staging indexation: Vercel noindexes `*.vercel.app` previews but NOT custom domains on non-production branches — gate `robots` metadata on `VERCEL_ENV`.
4. Shipping the staging noindex to production (check after every launch: `curl -sI` for `X-Robots-Tag`, view-source for `<meta name="robots"`).
5. Phantom slugs rendering default-metadata shells instead of `notFound()`.
6. Page-level `openGraph` shallow-merge silently wiping layout OG fields; missing `title.default`.
7. Critical content only in `useEffect`/`ssr:false` — invisible to Bing and AI crawlers.
8. Sitemap containing redirects, noindexed, or non-canonical URLs.
9. Disallowing `/_next/` in robots.txt — Google needs the JS/CSS to render; never block `_next/static`.

## Pages Router (legacy) mapping

`next/head` + `key` prop for dedupe (no template/merge system) · `next-seo` package OK here, do NOT adopt for App Router · `next-sitemap` for sitemap/robots (works but unmaintained since ~2023; alternative: `getServerSideProps`-based `/sitemap.xml.tsx`) · `@vercel/og` in an API route for OG images · ISR via `revalidate` in `getStaticProps`.
