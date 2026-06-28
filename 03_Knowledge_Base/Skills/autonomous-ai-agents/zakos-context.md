---
skill: "zakos-context"
category: "autonomous-ai-agents"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\autonomous-ai-agents\zakos-context\SKILL.md"
vault_path: "Skills/autonomous-ai-agents/zakos-context.md"
tags: ["autonomous-ai-agents", "hermes-skill", "skill"]
trigger_keywords: ["zakos", "project", "continuity", "branding", "ports", "remote", "access", "backend", "host", "bring-up"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---
# ZakOS context

---
name: ZakOS-context
description: "ZakOS project continuity, branding, ports, remote access, backend host bring-up, frontend recovery, and Windows-specific gotchas."
---

# ZakOS Context

## Design system doctrine
See `Mind-Galaxy/ZakOS WebDev Guidelines.md` for the full design system. Also `Mind-Galaxy/ZakOS Design Principles.md`.

## Project continuity
- Stay current on ZakOS state across sessions.
- Remember running services, ports, latest fixes, active goals without asking status questions.
- Treat as long-running context — phase-by-phase execution; rebuild and confirm each phase before proceeding.

## Architecture / layout
- **Cloud Dock layout.** Deep left sidebar + light canvas + frosted top bar.
- Left sidebar: brand (`cloudboard`), search with `⌘K`, nested folder tree, upgrade card, Settings/Logout.
- Top bar: sticky, frosted glass (`rgba(255,255,255,0.82)` + `blur(18px)`), search, notifications, Profile pill, Create action.
- Main canvas: light gray (`#F3F4F6`), soft cards, generous rounded corners, file tables, clean data hierarchy.
- Mobile: sidebar hidden, bottom nav preserved for app tabs.
- **This overrides the previous top-bar-first / no-sidebar doctrine for ZakOS.** The user explicitly switched to the Cloud Dock product direction (2026-06-25) and will correct any revert to the old layout.

## Branding
- UI must say **ZakOS**, never "AgenticOS".
- Applies to: logo, titles, manifest, error screen, any visible app name.

## Color tokens (Salesforce invoice mockup exact)
- Accent: `#C8FF2E` (hover `#D7FF53`, pressed `#B7EF1D`)
- Dark bg-main: `#111827`, bg-card: `#1F2937`, bg-elevated: `#1a2332`, surface-1: `#1F2937`, surface-2: `#283548`, surface-3: `#374151`, text-primary: `#F9FAFB`, text-secondary: `#D1D5DB`, text-muted: `#9CA3AF`, border-soft: `#374151`
- Light bg-main: `#F3F4F6`, bg-card: `#FFFFFF`, bg-elevated: `#FFFFFF`, surface-1: `#FFFFFF`, surface-2: `#F3F4F6`, surface-3: `#E5E7EB`, text-primary: `#111827`, text-secondary: `#4B5563`, text-muted: `#9CA3AF`, border-soft: `#E5E7EB`
- See `Mind-Galaxy/ZakOS WebDev Guidelines.md` for full token spec

## Ports / remote access
- Frontend: `:3000`
- Backend: `:4000`
- Tailscale IP: `100.110.139.73`
- `frontend/.env` → `NEXT_PUBLIC_BACKEND_URL=http://100.110.139.73:4000`
- Next.js dev server must bind `0.0.0.0` to accept Tailscale traffic.
- Frontend `.env` changes require server restart.

## Windows backend bring-up checklist
1. Create/use venv (`python -m venv venv`)
2. `PYTHONPATH=` (clear it)
3. `DB_PATH` must resolve to an **absolute Windows path** using `Path(__file__).with_name("agenticos.db").resolve()` — MSYS path translation maps `/data` to `C:\data`, which breaks sqlite
4. Firewall rule: allow inbound TCP `4000`
5. If uvicorn exits silently with no output, the most common cause is `PYTHONPATH` pointing to Hermes venv. Recreate venv cleanly and always unset.

See `references/windows-build-troubleshooting.md` for detailed error transcripts and exact command sequences.

## Frontend recovery pattern (500 / blank page / webpack errors)
When the browser shows 500s on `webpack.js:1`, `main.js:1`, `_error.js:1`, or a blank white screen:
1. `netstat -ano | findstr ":3000" | findstr LISTENING` → get PID
2. `taskkill //F //PID <pid>` to kill stale process
3. `rm -rf .next` to purge corrupted cache
4. Restart: `cd frontend && npx next dev -H 0.0.0.0 -p 3000`
5. Wait 20–30s for full compile, then verify routes with `curl`

## Common frontend build failures and fixes
- **"name is defined multiple times"** → duplicate `'use client'` or duplicate imports in a `.tsx` file. Remove the duplicate block at the top of the file.
- **"Cannot find name 'X'"** (useEffect, useState, etc.) → missing React import after a partial patch. Add `import { useEffect, useState } from 'react'`.
- **"Property 'catch' does not exist on type 'void'"** → `.catch()` chained on the wrong expression. The promise's `.then()` returns void when the callback returns void. Fix: `await promise.then(...)` or `promise.then(...).catch(...)`.
- **"Unexpected token `<AppLayout>`"** → stale `.next` cache from a previous broken state. Purge `.next` and rebuild. If the file looks correct, it's almost always cache.
- **TypeScript errors after patch** → TypeScript flagging real type gaps. Either add the missing property to the interface in `lib/types.ts` or use safe fallbacks (`?? 0`, `|| {}`).
- **Duplicate 'use client'** → happens when a page file has two `'use client'` directives. Keep only one, at the very top.

## Git workflow
- User checks VS Code Source Control for uncommitted changes count.
- Must manually review all uncommitted changes before commit.
- Cancel accidental/unnecessary edits per user request.
- Commit and push only after user confirms work is correct.
- **User explicitly requires "pushed to github" confirmation before next upgrade phase.**

## Real API wiring pattern
- Wire endpoints progressively; each page should handle empty/error states gracefully.
- Frontend `lib/api.ts` is the single source of truth for API calls.
- Backend routes must be included in `server.py` main router with correct prefix.
- When backend token/env not configured, API returns empty — frontend must show fallback data or empty state, not crash.
- obsidian/GitHub note parsing: prefer `python-frontmatter` over `frontmatter` package.

## Recurring failure modes
- **Port 3000 already in use (EADDRINUSE)** — kill PID before restart. See frontend recovery pattern.
- **Stale .next cache causes blank pages / build errors** — always clean before dev restart.
- **Backend uvicorn exits silently** — almost always Hermes `PYTHONPATH` pollution. Recreate venv and use `unset PYTHONPATH`.
- **Windows MSYS path translation** — POSIX paths like `/data` silently map to `C:\data`. Always use `pathlib.Path(...).resolve()` for absolute paths.
- **TypeScript build fails but dev server works** — dev server is more lenient. Fix the TS errors before declaring victory.

## Graphify architecture radar
Optional but useful. Graphify turns the codebase into a queryable knowledge graph (`703 nodes · 976 edges` on last run).

**Files:**
- `graphify-out/graph.json` — full machine-readable graph (≈549 KB)
- `graphify-out/GRAPH_REPORT.md` — human-readable highlights: god nodes, surprising connections, suggested questions

**Commands:**
```bash
cd "C:/Users/pc/Documents/Vs-Code/Projects/ZakOS"
graphify update . --no-cluster        # re-extract code only (no LLM needed)
graphify cluster-only . --no-viz      # rebuild communities without LLM labels
graphify label .                       # label communities with LLM (needs API key)
```
**Last run:** code-only extraction (no semantic LLM). 52 communities, 226 isolated nodes (≤1 connection) noted as potential documentation gaps.

See `references/graphify-architecture-radar.md` for interpretation notes.

## Vault note
`Projects/ZakOS/ZakOS.md`

---
#autonomous-ai-agents #knowledge-base #skills

