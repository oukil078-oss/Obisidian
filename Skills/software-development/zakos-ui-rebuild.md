---
skill: "zakos-ui-rebuild"
category: "software-development"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\software-development\zakos-ui-rebuild\SKILL.md"
vault_path: "Skills/software-development/zakos-ui-rebuild.md"
tags: ["software-development", "hermes-skill", "skill"]
trigger_keywords: ["rebuild", "entire", "zakos", "next", "frontend", "match", "hubspot", "workspace", "aesthetic", "extracted"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---

---
name: zakos-ui-rebuild
description: Rebuild the entire ZakOS Next.js frontend to match the HubSpot workspace aesthetic extracted in zakos-hermes-ui-kit-spec.md.
---

# ZakOS UI Rebuild

Rebuild the entire ZakOS Next.js frontend to match the HubSpot workspace aesthetic extracted in `zakos-hermes-ui-kit-spec.md`.

## Procedure (MANDATORY)
This is a multi-phase rebuild. Work in phases, rebuild and verify after each phase, and **wait for user confirmation before proceeding to the next tab/feature**.

1. Read `zakos-hermes-ui-kit-spec.md` and study the attached reference image.
2. Audit existing pages under `frontend/app/*/page.tsx` for generic patterns.
3. Rewrite each route to use:
   - bento grid layouts (not uniform grids)
   - surface depth system (surface-1, surface-2, surface-3)
   - white summary panels on the right (`white-panel`)
   - pill navigation with lime active state
   - component tokens from `globals.css` (`card`, `badge`, `chip`, `icon-btn`, `btn-primary`, `btn-ghost`)
4. **Wire live data:** Replace all `SAMPLE_*` constants and hardcoded arrays with real API calls via `frontend/lib/api.ts`. Use the existing `apiFetch` wrapper and route-specific API objects (`devApi`, `studyApi`, `agentsApi`, etc.). Remove sample fallbacks; on fetch failure, show empty state or error UI, not fake data.
5. **Deploy via Docker** (production-grade rebuild):
   ```bash
   cd C:/Users/pc/Documents/Vs-Code/Projects/ZakOS
   docker-compose build frontend
   docker-compose up -d frontend
   ```
   On Windows, `next dev` directly often hits port conflicts and MSYS path issues. Docker is the reliable path.
6. Save design system to Obsidian vault at `C:\\Users\\pc\\Documents\\Vs-Code\\Mind-Galaxy\\ZakOS Design System.md`.
7. Update Hermes memory with the new tokens and vault path.
8. Verify backend is running on port 4000 before declaring live data complete.

### Step-by-step rule
After each phase (backend integration, background upgrade, tab rebuild):
- Run the production build or restart containers
- Confirm health endpoints return 200
- Confirm the specific tab/page renders
- THEN wait for user confirmation before the next phase

## Frontend Foundation Upgrade
### 3D Animated Background
Replace the old `ParticlesBackground` canvas with a tasteful Three.js WebGL background:
- File: `frontend/components/dashboard/ZakosBackground.tsx`
- Uses `@react-three/fiber` + `@react-three/drei`
- Floating icosahedrons + torus knots in lime/teal/violet accents
- Fog + atmospheric radial-gradient overlays + subtle dot-grid SVG texture for depth
- Mounted in `AppLayout.tsx` in place of `ParticlesBackground`
- Keep performance in mind: limit shape count, use `dpr={[1,2]}`, avoid heavy post-processing

### Animation Libraries
Use these aggressively for text effects, shapes, transitions, and animations:
- **Motion / Framer Motion** — already in `package.json`; use `motion.div`, `AnimatePresence`, layout transitions
- **Aceternity UI** — component patterns: `AnimatedBeam`, `BackgroundBeams`, `Lens`, `Sparkles`
- **Magic UI** — component patterns: `BlurFade`, `ShimmerButton`, `ParticleText`
- **React Bits** — component patterns: modern agentic UI primitives

Map the Hermes template design language onto these libraries rather than writing custom CSS animations.

## References
- spec doc: `zakos-hermes-ui-kit-spec.md`
- design tokens: `frontend/app/globals.css`
- layout shell: `frontend/components/layout/AppLayout.tsx`
- top bar: `frontend/components/layout/TopBar.tsx`
- backend API map: `references/backend-api.md`
- lucide icon mapping: `references/lucide-icon-mapping.md`
- backend integration patterns: `references/backend-integration-patterns.md`
- overview metrics spec: `references/overview-metrics.md`

## Pitfalls
- **Icon library fallback (Windows/MSYS):** `@phosphor-icons-react` can fail module resolution inside Next.js on Windows even when installed. If you see `Module not found: Can't resolve '@phosphor-icons-react'`, switch the codebase to `lucide-react` (already in `package.json`) and remap icon names. Icon names are NOT 1:1 between the two libraries; see `references/lucide-icon-mapping.md` for the mapping used in this project. Bulk replacements across `.tsx`/`.ts` files are more reliable with Python than with MSYS `sed -i`, which cannot reliably escape `@phosphor-icons-react` in the pattern. Use `python -c \"import os; ... oswalk replace ...\"` for bulk rewrites.
- **Bulk import rewrite gotcha (Windows/MSYS):** After bulk file edits, verify every targeted file actually changed with `grep -rln \"old string\" path`. MSYS/Python `sed -i` and even `node -e fs.writeFileSync` can appear to succeed while leaving files unchanged if the file is locked or the encoding mismatches. Re-read critical files and grep again before rebuilding.
- **lucide-react missing-icon trap:** Common phosphor icons that do not exist in lucide-react: `UserCircle` → `User`, `EnvelopeSimple` → `Mail`, `SpeakerSimpleSlash` → `VolumeX`, `SpeakerSimpleHigh` → `Volume2`, `Stop` → `Square`, `SpinnerGap` → `Loader`/`Loader2`, `CaretRight` → `ChevronRight`, `ArrowsOut` → `MoveDiagonal`, `Robot` → `Bot`, `Chat` → `MessageCircle`, `Graph` → `Network`, `MoreVertical` → `Menu`, `BarChart` → `ChartBar`. Always verify existence with `node -e \"const icons = require('...'); console.log(icons.Name ? 'EXISTS' : 'MISSING')\"` before assuming the name is valid.
- **Frontend 500 from Framer Motion:** `<AnimatePresence>` must be imported alongside `motion` in every file that uses it. Missing import causes runtime 500.
- **Backend route registration:** After adding a new `backend/routes/*.py`, import it in `backend/server.py` and call `app.include_router(..., prefix=\"/api\")`. Otherwise the endpoint 404s even though the file exists.
- **Backend missing endpoints:** If the frontend needs a route that doesn’t exist yet (e.g. `/api/models`, `/api/cyber/findings`), add a small router in `backend/routes/` with static/demo data, register it, and restart backend.
- **Live data wiring — API shape mismatches:** Backend endpoints often wrap arrays in a dict object (e.g. `{ "events": [...], "date": "..." }`, `{ "repos": [...] }`, `{ "nodes": [...] }`, `{ "emails": [...], "count": N }`). The frontend must unwrap these shapes before state assignment. Calling `.filter()` or `.map()` directly on the response object causes runtime `TypeError: X is not a function`. Pattern: `setEvents((data?.events || []) as Event[])` rather than `setEvents(data as Event[])`.
- **Frontend proxy:** Never call `http://localhost:4000` directly from the browser. Use relative paths (`/api/...`) so Next.js rewrites work. `next.config.js` already maps `/api/:path*` to the backend.
- **Avoid generic aesthetics:** No blue/teal/purple accents, no glassmorphism panels, no gradient hero sections. Lime accent only, dark canvas, white contrast panels.
- **Mobile Dev page selector:** On mobile, the hidden (`md:hidden`) left sidebar means repos are unreachable. Add a visible `<select>` dropdown above the empty-state/main panel when `!selected && mobile`, and a back button (`ArrowLeft`) in the repo header visible only on mobile to clear selection. Keep the desktop sidebar intact.
- **Backend dependency alignment (Windows/MSYS):** `backend/requirements.txt` can contain unresolvable protobuf conflicts. Do NOT install with `pip install -r requirements.txt`. Instead install core deps individually: `fastapi uvicorn sqlalchemy aiosqlite httpx python-dotenv python-frontmatter openai pydantic`.
- **Backend venv isolation:** Always recreate venv clean and run uvicorn with PYTHONPATH empty. Hermes venv state leaks into subprocesses and breaks imports. Command: `cd backend && rm -rf venv && python -m venv venv && PYTHONPATH=\"\" venv/Scripts/python.exe -m pip install fastapi uvicorn openai httpx pydantic sqlalchemy aiosqlite python-dotenv python-frontmatter`.
- **Backend database path (Windows/MSYS):** MSYS translates `/data` to `C:\data` and `/app` to `C:\app`, breaking sqlite. Use `Path(__file__).with_name("agenticos.db").resolve()` instead of hardcoded POSIX paths.
- **Frontend recovery for 500/webpack failures:** If Next.js returns 500 or webpack errors, use the recovery sequence: taskkill PID on :3000, `rm -rf .next`, then `npx next dev -H 0.0.0.0 -p 3000`. First request may timeout while compiling; wait 20-30s.
- **TypeScript/runtime discipline:** After patching, verify TypeScript compiles and routes return 200 on first compile. If you see `TypeError: X is not a function` on `/` or health-check pages, an API shape mismatch or missing lucide icon is still present. Fix the root cause before declaring the task complete.
- **Post-migration import verification:** After bulk icon library migration (e.g. phosphor → lucide), don’t trust automated replacements blindly. Run `grep -rln "old-lib-name" path` and `grep -rln "from 'lucide-react'" path` to find remaining old imports and files that still need patching. Some files (e.g. `JarvisPanel.tsx`) can get their JSX tags renamed while the import statement is left pointing at the old package, causing `Module not found` on every route that imports them.
- **Icon name validation:** Before committing to a renamed icon, verify it exists in the target library with `node -e "const icons = require('...'); console.log(icons.Name ? 'EXISTS' : 'MISSING')"`. Lucide-react names that don’t exist: `ArrowsOutFromLine`, `CaretRight`, `UserCircle`, `EnvelopeSimple`, `SpeakerSimpleSlash`, `SpeakerSimpleHigh`, `Stop`, `SpinnerGap`. Map them to `MoveDiagonal`, `ChevronRight`, `User`, `Mail`, `VolumeX`, `Volume2`, `Square`, `Loader` instead.
- **Backend liveness bribery:** After any backend restart or port kill/restart cycle, verify health with `curl http://localhost:4000/api/health` before assuming frontend data fetches will work. A dead backend returns connection refused, which frontend `fetch()` rejects silently unless you log it.
- **Component-level `setState` during render:** If the console shows `Warning: Cannot update a component while rendering a different component`, the culprit is almost always a `useEffect` that calls a Zustand setter during render rather than inside an effect body. Check for `useEffect(() => { someAsyncFn().then(setX); }, [])` where `someAsyncFn` is accidentally synchronous or the dependency array is empty on a component that re-renders frequently.

- **Automation click limitation:** Browser automation clicks (`browser_click`) on React-rendered list items don't always trigger Zustand/React state updates. For reliable testing, navigate directly to the route (e.g. `/dev/{id}`) instead of clicking sidebar cards. Use `browser_console` to confirm `window.location.href` changed.

- **App Router file placement (flat-file 404 trap):** `app/<route>.tsx` does not register as a page in Next.js App Router. Pages must live at `app/<route>/page.tsx`. After restructuring, rebuild and curl-check every route before declaring the tab live.

- **Subagent rate limits on bulk file writes:** Dispatching 3+ parallel delegates for file rewrites can trigger HTTP 429 from the model provider. Prefer 2 subagents per batch for large write workloads, and fall back to direct main-agent edits if rate limits fire.

- **Deployment via Docker is preferred:** For ZakOS, `docker-compose build frontend && docker-compose up -d frontend` is the reliable deploy path. Running `npx next dev` directly on Windows frequently hits `EADDRINUSE` and MSYS path translation issues. Do not switch to local dev-server mode until Docker is ruled out.

- **Missing import after route rewrite:** When replacing a route file entirely (e.g. `backend/routes/agents.py`), ensure all stdlib imports used in the new body are present. Missing `import os` causes silent import failure in uvicorn startup.

- **API client naming conventions:** The `frontend/lib/api.ts` methods use short names, not always matching the URL path exactly. Common mismatches:
  - `scheduleApi.list()` → `/api/schedule/events` (not `scheduleApi.events()`)
  - `contentApi.list()` → `/api/content/docs` (not `contentApi.listDocs()`)
  - `activityApi.feed()` → `/api/activity/feed`
  TypeScript will catch these at build time, but the error message only says `Property X does not exist` — check the API client object shape, not the backend route.

- **Docker build auth timeout fallback:** If `docker-compose build --no-cache` fails with `DeadlineExceeded: failed to fetch oauth token` from Docker Hub, retry **without** `--no-cache`. Docker Desktop can use the local image/build cache base layers and skip the registry auth call entirely. Command: `docker-compose build frontend` (no flags).

- **Three.js background component:** When adding a new WebGL background, create a dedicated component (e.g. `ZakosBackground.tsx`) under `components/dashboard/`, import it in `AppLayout.tsx`, and replace the old background component there. Keep it tasteful: limit geometry count, use `dpr={[1,2]}`, avoid heavy post-processing chains.

- **Animation library mandate:** For modern premiums, aggressively use Aceternity UI, Magic UI, Motion/Framer Motion, and React Bits component patterns. Do not write custom CSS keyframe animations when these libraries provide the same effect with less code and better performance.
