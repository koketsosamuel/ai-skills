# Pure HTML/CSS static site playbook

No framework, no build step. These sites start with structural advantages most frameworks must earn back: everything is in the initial HTML (no JS rendering dependency — perfect for Google AND for AI crawlers that never execute JS), near-automatic INP pass, fast TTFB on any CDN host. Every characteristic failure mode is process, not technology. The universal checklist lives in [technical-seo.md](technical-seo.md); this file covers what's different without a framework.

## The head-tag drift problem (failure mode #1)

Every page hand-carries its own title, description, canonical, and OG block — drift (stale canonicals after renames, duplicated titles from copied templates) is THE classic hand-rolled-site failure. Fixes in increasing tooling order:

1. **A canonical `_template.html` skeleton** with placeholder comments for every per-page field, plus a **pre-deploy check script** — grep that fails on duplicate `<title>` values, missing canonicals, or canonicals not matching the file's own path. ~20 lines of shell, catches 90% of drift. Write this script for the user; it's the highest-value deliverable on a hand-rolled site:

```bash
#!/usr/bin/env bash
# seo-check.sh — run before deploy; exits 1 on drift
set -e
fail=0
# duplicate titles
dups=$(grep -rhoP '(?<=<title>).*?(?=</title>)' ./*.html **/*.html 2>/dev/null | sort | uniq -d)
[ -n "$dups" ] && { echo "DUPLICATE TITLES:"; echo "$dups"; fail=1; }
# pages missing canonical / description / og:image
for f in $(find . -name '*.html' -not -path './node_modules/*'); do
  grep -q 'rel="canonical"' "$f" || { echo "NO CANONICAL: $f"; fail=1; }
  grep -q 'name="description"' "$f" || { echo "NO DESCRIPTION: $f"; fail=1; }
done
exit $fail
```

2. **Server-side includes** where hosting allows (Apache/Nginx SSI, PHP include) for shared head fragments — no build step, per-page titles preserved.
3. Honest escalation: if the site keeps growing, a minimal generator (Eleventy) exists precisely for this tax. Say so; don't force it.

## Sitemaps without a build step

- Small sites (<~50 pages): a **plain-text sitemap** — one absolute URL per line, UTF-8 — is fully valid per Google and has nothing to get syntactically wrong. Or minimal XML, adding `<lastmod>` only when a page genuinely changes (dishonest lastmod teaches Google to ignore it).
- Growing sites: `npx sitemap-generator-cli https://example.com`, Screaming Frog (free ≤500 URLs), or a 10-line script over the HTML directory wired into deploy.
- Reference it in robots.txt (`Sitemap: https://example.com/sitemap.xml`), submit in GSC + Bing Webmaster Tools.

## Redirects & headers by host (know before promising anything)

| Host | Redirects | Custom headers | Notes |
|---|---|---|---|
| Apache shared | `.htaccess` `Redirect 301` / `RewriteRule` | `.htaccess` `Header set` | Watch accidental chains |
| Netlify | `_redirects` file (`/old /new 301`) or netlify.toml | `_headers` file | Real 301s; host canonicalization too |
| Cloudflare Pages | `_redirects` + dashboard Redirect Rules | `_headers` | Free CDN, HTTP/3, Brotli |
| Vercel | `vercel.json` redirects | `vercel.json` headers | 308 for permanent |
| **GitHub Pages** | **NONE** — no server redirects, no custom headers, fixed `Cache-Control: max-age=600` | **NONE** | Only meta-refresh + canonical pages. Fine if URLs never change; wrong host if migrations are ever likely. Flag this to the user. |

Hosting affects SEO through exactly four things: TTFB/CDN, redirect+header capability, uptime (persistent 5xx throttles crawling), HTTPS. Server geography is irrelevant in the CDN era; platform brand carries zero ranking weight.

## Performance levers specific to no-build sites

- Inline critical CSS — a static site's whole stylesheet often fits inline; no `@import` (serializes requests).
- Hero image: `<img fetchpriority="high" width=... height=...>`, AVIF/WebP with `srcset`; `loading="lazy"` below the fold only.
- Fonts: system stack (zero problem) or self-hosted WOFF2 + `font-display: swap` + one preload.
- **Speculation Rules** — the free 2026 lever for static MPAs, paste-in, no build:

```html
<script type="speculationrules">
{ "prefetch": [{ "where": { "href_matches": "/*" }, "eagerness": "moderate" }] }
</script>
```

- Long-cache fingerprinted assets only if filenames change on content change; otherwise short cache for HTML, medium for assets.

## llms.txt without a build step

Hand-write it — the spec is markdown and a small curated file beats a generated dump (format in [llms-txt.md](llms-txt.md)). Maintain it alongside the sitemap in the same deploy checklist; stale links in llms.txt are worse than no file. Optionally hand-write `.md` twins for the handful of pages agents would actually want.

## The bottom line for this stack

Technical SEO on a hand-written site is a checklist, then discipline: unique titles, honest sitemap, self-canonicals on every page, one-hop 301s (on a host that can do them), sized images, preloaded hero, JSON-LD Article/Organization, GSC + Bing + IndexNow ping in deploy. Once that's in place, content quality and E-E-A-T are the whole game — exactly as Google's ranking systems intend.
