# llms.txt + AI-search (GEO) playbook

State of play verified July 2026 against llmstxt.org, vendor crawler docs, and log-data studies. This space is hype-dense — the honest evidence hierarchy below is the point of this file. Tell the user the truth: ship llms.txt because it's nearly free and helps coding agents, not because it ranks.

## llms.txt format (llmstxt.org spec)

Markdown file at `/llms.txt` (site root). It is a curated inference-time map for LLMs, not a directives file and not a sitemap. Structure, in order:

1. `# H1` — site/project name (the only required element)
2. `> blockquote` — short summary with the key context to interpret the rest
3. Optional plain paragraphs of detail (no headings)
4. `## H2` sections of link lists: `- [name](url): notes`
5. A special `## Optional` section — links safe to skip when context is short

```markdown
# Acme Analytics

> Acme is a privacy-first web analytics platform. Docs cover the JS snippet,
> REST API, and self-hosting. Current stable version: 4.x.

## Docs

- [Quickstart](https://acme.dev/docs/quickstart.md): install the snippet, first events in 5 min
- [REST API](https://acme.dev/docs/rest-api.md): auth, endpoints, rate limits

## Optional

- [Changelog](https://acme.dev/changelog.md)
```

Companions (ecosystem convention, not spec): `llms-full.txt` — all docs content inlined in one file (can exceed context windows; some tools add `llms-small.txt`); and the **`.md` page variant** — serve a clean markdown twin of each page at `<url>.md`. The `.md` twins are the most useful part for agents. Generate all of it from the same content source as the sitemap so it never goes stale. Curate — an uncurated crawl-dump llms.txt is worse than none.

## Honest expectations (say this to the user)

- **Confirmed by log studies (Ahrefs 137k domains, June 2026):** 97% of llms.txt files get zero requests; AI retrieval bots are ~1% of what little traffic exists. Google is on record (Illyes, Mueller) that it does not use llms.txt and its AI-features doc says "you don't need to create new machine readable files… to appear in these features." No engine has committed to reading it.
- **The real consumers today:** coding/IDE agents (Cursor @Docs, Claude Code, MCP doc servers) pointed at docs sites. For dev-tools/docs sites it's genuinely worth shipping; for a general marketing site it's a few minutes of insurance, nothing more.
- Never present llms.txt as a ranking lever. Present it as: cheap, useful-to-agents, and optionality if engines adopt it.

## AI crawler landscape — the three classes

The distinction that drives every decision:

1. **Training crawlers** (bulk ingestion): `GPTBot`, `ClaudeBot`, `CCBot`, `Bytespider`, `meta-externalagent`, `Amazonbot`. Blocking these does NOT remove you from AI answers today.
2. **Search-index crawlers** (build AI answer retrieval indexes): `OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`.
3. **Live user-triggered fetchers** (fetch when a user's question needs your page — these produce citations and clicks): `ChatGPT-User`, `Claude-User`, `Perplexity-User`.

Vendor notes: OpenAI/Anthropic publish IP JSONs (`openai.com/gptbot.json`, `claude.com/crawling/bots.json`) for verifying spoofers. Perplexity's robots.txt compliance is documented as partial. Bytespider routinely ignores robots.txt — block at WAF/edge if it matters. `Google-Extended` is a robots.txt token only (controls Gemini training/grounding), never affects Google Search or AI Overviews; AI Overviews eligibility is just normal Googlebot indexing + snippet eligibility.

## robots.txt stance for a site that WANTS AI visibility

Allow classes 2 and 3 unconditionally; training-bot policy is a separate business decision — ask the user rather than deciding for them:

```
# AI retrieval + live fetchers: ALLOW (these produce citations/traffic)
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

# Training crawlers (GPTBot, ClaudeBot, CCBot, Bytespider, meta-externalagent,
# Applebot-Extended): user's call — Disallow here if they opt out of training.
# Blocking them does not affect AI-answer citations today.

Sitemap: https://example.com/sitemap.xml
```

Default-allow (no rules at all) is also maximum-visibility. Never blanket `Disallow: /` for `*` and then allowlist — some AI fetchers treat missing specific rules conservatively. Also check the CDN: Cloudflare blocks AI training crawlers by default on new zones — edge settings can silently override the robots.txt you write.

## What actually earns AI citations (evidence-ranked)

1. **Server-rendered, clean HTML** — the binary gate. No major AI crawler executes JavaScript (Vercel's 500M-fetch study: GPTBot downloads JS ~11.5% of the time, never runs it; only Google's AI surfaces render). A CSR SPA is a blank page to every non-Google AI engine. Verify with `curl` — the answerable content must be in the raw HTML.
2. **Rank in classic search** — OAI-SearchBot and Perplexity retrieve largely via conventional indexes; Google's AI surfaces ride on normal indexing. Classic SEO gates everything; GEO is additive, not a replacement.
3. **Statistics, quotations, and cited sources in the content** — the Princeton GEO paper (Aggarwal et al., arXiv:2311.09735, KDD 2024) measured +30–40% generated-answer visibility for each; keyword stuffing did nothing. Directional (lab conditions), but the best controlled evidence that exists.
4. **Question-shaped H2/H3 + a self-contained 40–80-word direct answer under each** — maps onto how retrieval chunks pages. Strong practitioner consensus, no controlled study; cheap, do it.
5. **Presence on the sources engines actually cite** — Reddit (~#1 overall, dominates Perplexity), Wikipedia (dominates ChatGPT), YouTube/Google properties (dominate AI Overviews). Only ~11% of domains are cited by both ChatGPT and Perplexity — third-party presence is its own channel. Out of on-site scope, but tell the user.
6. **Schema/JSON-LD**: matters for Google surfaces; Ahrefs' causal study (1,885 pages) found NO citation uplift on ChatGPT/Perplexity from adding schema alone. Do it for Google, don't oversell it for AI.
7. **Fast TTFB + visible dates/freshness** — plausible (live fetchers have latency budgets), unproven thresholds. Treat as hygiene.

## Measuring AI visibility

- **Referral traffic**: GA4 custom channel group on source regex `chatgpt\.com|perplexity\.ai|claude\.ai|gemini\.google\.com|copilot\.microsoft\.com` (GA4 got a native "AI Assistant" channel May 2026). Undercounts badly — 35–70% of AI-origin sessions arrive referrer-less.
- **Log KPI**: hits from `ChatGPT-User` / `Claude-User` / `Perplexity-User` are the signal that real users' questions pulled your pages — track separately from training-bot noise. Verify UAs against published IP lists.
- Answer-side monitors (Profound, Otterly, Ahrefs Brand Radar) are prompt-sampling based — directional only.
