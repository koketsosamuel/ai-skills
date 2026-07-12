# Universal technical SEO playbook

Framework-agnostic. Load-bearing claims verified against Google Search Central docs, July 2026. This file is the audit backbone — stack files (astro.md, nextjs.md, html-css.md) say HOW to implement each item on a given stack.

## What matters vs myths (don't waste the user's time)

**Confirmed by Google:** helpful, people-first content is the center of gravity (Helpful Content System folded into core ranking since March 2024 — originality and first-hand experience win); Core Web Vitals ARE a ranking input but modest — "no single signal", relevance beats page experience; HTTPS mandatory; mobile-first indexing universal (mobile HTML is what gets indexed).

**Myths — skip and say why:** meta keywords (ignored since 2009; Bing treats stuffing as spam signal — delete it); keyword density targets; meta description as ranking factor (CTR lever only); sitemap `priority`/`changefreq` (Google ignores both — omit); a single "page experience score"; llms.txt as a ranking lever (see llms-txt.md).

**AI Overviews reality:** on ~48% of queries; organic CTR drops ~61% when present; being cited inside the answer is the new position #1. Google's official position: no special "AI SEO" exists — normal indexability + helpful content + structured data are the inputs. `nosnippet`/`data-nosnippet`/`max-snippet` limit what AI features quote; `Google-Extended` only affects Gemini training, never Search.

## Crawlability & indexing

- **robots.txt is NOT a de-indexing tool.** A disallowed URL can still be indexed (URL-only) from external links. To keep a page out: `noindex` or auth. **Fatal combo: Disallow + noindex on the same URL** — the block prevents Google from ever seeing the noindex. Other gotchas: fail-open on 404 but persistent 5xx on robots.txt halts crawling; never block CSS/JS needed for rendering; case-sensitive.
- **Sitemaps**: 50,000 URLs / 50 MB per file, then a sitemap index. `lastmod` honesty is enforced — Google only trusts it if "consistently and verifiably accurate"; stamping every URL on every deploy teaches Google to ignore it. Only canonical, indexable, 200-status URLs. Plain-text one-URL-per-line format is valid (good for hand-maintained sites). Discovery hint, not an indexing guarantee.
- **Canonicals**: strong hint, not directive. Self-referencing canonical on every page (cheap insurance against parameter/scheme/slash duplication); absolute URLs; head only; one per page. Signal strength: redirects > rel=canonical > sitemap inclusion. Cross-domain supported (syndication).
- **noindex**: meta robots for HTML; `X-Robots-Tag` header for PDFs/images.
- **Redirects**: 301/308 permanent (strong canonical signal) vs 302/307 temporary (weak). Server-side > meta refresh (`0;url=` reads permanent) > JS redirect (last resort). Googlebot follows 10 hops max; keep chains ≤3 — flatten to single hops during migrations.
- **404 vs 410**: Google treats them near-identically; either is fine for gone content. Never redirect dead pages to home (soft-404). Soft 404s (200 + error content) get flagged and dropped.
- **Faceted/parameter URLs**: robots.txt disallow is Google's recommended tool for non-indexable facets (canonical/nofollow "less effective long term"), or `#` fragments for filter state (ignored entirely). Indexable facets: consistent param order, 404 for empty results.

## On-page

- **Title**: the highest-leverage on-page element. No official char limit; ~50–60 chars displays intact. Unique per page, front-load the topic, brand at the end. Google rewrites bad titles drawing from H1/og:title/anchors — the defense is a title that already matches the visible H1.
- **Meta description**: CTR lever, not ranking. ~120–160 chars displays reliably; unique; concrete value (price, date, what the reader gets). Google substitutes page text when it thinks that's better.
- **Headings**: one clear H1 matching title intent, logical h2/h3 outline — headings feed passage ranking and AI-answer chunk extraction. Never choose heading level for font size.
- **Semantic HTML5** (`<main>`, `<nav>`, `<article>`): no confirmed ranking bonus, but helps Google separate main content from boilerplate, and real text in HTML always beats text-in-images or JS-injected text.
- **Internal linking**: real `<a href>` only (crawlers don't click buttons); descriptive anchors ("pricing for X", never "click here"); every important page ≤3 clicks from home; orphan pages go unindexed. A curated related-links block is the cheapest ranking lever on most sites.
- **Images**: factual alt text (ranking input for Images; anchor text when the image is a link); `alt=""` only for decorative; descriptive filenames.
- **URLs**: readable words, hyphens, lowercase, stable forever. One host/scheme/trailing-slash convention, 301 the rest.

## Structured data (2026 state)

- **JSON-LD in a script tag is Google's recommended format.** Markup must match visible content — invisible/inflated markup risks a manual action.
- **Worth implementing** for typical sites: Article/BlogPosting (bylines + dates), Organization (logo, `sameAs` — knowledge panel + brand disambiguation in AI answers), BreadcrumbList, Product+Offer+AggregateRating (highest-CTR rich result left), LocalBusiness, Event, VideoObject, Recipe, ProfilePage (author pages).
- **Dead — do not implement for rich results:** HowTo (killed 2023), **FAQ (fully ended May 2026**, reporting removed from GSC), sitelinks search box (2024), and the June 2025 purge (Book Actions, Course Info, Claim Review, Estimated Salary, Learning Video, Special Announcement, Vehicle Listing). FAQPage content still matters for passage retrieval — only the SERP widget is gone. Leftover deprecated markup is harmless but dead weight.
- Validate: Rich Results Test (Google eligibility) + validator.schema.org (correctness); monitor GSC enhancement reports.

## Social meta (table stakes, per page)

```html
<meta property="og:title"       content="Page-specific title">
<meta property="og:description" content="Page-specific description">
<meta property="og:image"       content="https://example.com/img/page-card.jpg"> <!-- 1200x630, absolute -->
<meta property="og:url"         content="https://example.com/page/">  <!-- = canonical -->
<meta property="og:type"        content="article">
<meta property="og:site_name"   content="Site Name">
<meta name="twitter:card"       content="summary_large_image">
```

X falls back to OG for everything else. Also in every head: charset, viewport, canonical, `<html lang>`, favicon set (Google shows favicons in SERPs; provide 48×48-multiple).

## Core Web Vitals

Set unchanged since INP replaced FID (March 2024); assessed at p75 of real Chrome users:

| Metric | Good | Poor |
|---|---|---|
| LCP | ≤ 2.5 s | > 4.0 s |
| INP | ≤ 200 ms | > 500 ms |
| CLS | ≤ 0.1 | > 0.25 |

Levers in ROI order: (1) right-size images, AVIF/WebP, srcset; (2) never lazy-load the LCP image — `fetchpriority="high"` on the hero; (3) explicit width/height or aspect-ratio on every img/iframe, reserve embed space; (4) self-host WOFF2 + `font-display: swap` + preload the critical face (or use the system stack); (5) inline critical CSS, no `@import`; (6) `Cache-Control: public, max-age=31536000, immutable` on fingerprinted assets; (7) CDN with HTTP/2+/Brotli; (8) Speculation Rules API (`<script type="speculationrules">`, prefetch `"eagerness": "moderate"`) — near-instant next-page navigations, Chromium-only, zero build step. Judge by field data (CrUX/GSC), not Lighthouse lab scores.

## i18n, pagination, E-E-A-T

- **hreflang**: head tags, HTTP Link header, or sitemap xhtml:link (best for static sites — one file to maintain). Silent breakers: sets must be bidirectional; every page lists itself + all alternates; `en-GB` style codes (region alone invalid); include `x-default`. Each locale self-canonical.
- **Pagination**: rel=prev/next dead since 2019. Unique URL per page, real anchor links between pages, each page self-canonical — NEVER canonical pages 2+ to page 1. Infinite scroll is invisible to Googlebot — provide paginated fallbacks.
- **E-E-A-T on-page**: bylines with real author bio pages (Person + ProfilePage schema, `sameAs`); visible dates consistent with `datePublished`/`dateModified` and sitemap lastmod; About/Contact/editorial-policy pages linked in the footer; first-hand experience markers (original photos, "we measured" specifics); outbound citations to primary sources; consistent Organization entity.

## Measurement

- **Google Search Console** (non-negotiable): Performance (16 months; AI Mode traffic folded into "Web" type), URL Inspection + request indexing, Page indexing report ("Crawled – not indexed", canonical mismatches), Sitemaps, CWV report.
- **Bing Webmaster Tools**: one-click import from GSC; the index behind a slice of the AI-assistant ecosystem.
- **IndexNow**: one ping (`api.indexnow.org` + key file at root) propagates to Bing, Yandex, Seznam, Naver, Yep. **Google does not participate** — for Google it's sitemaps + crawling only. A one-line curl in the deploy script; cheap, do it.
- AI visibility measurement: see llms-txt.md.
