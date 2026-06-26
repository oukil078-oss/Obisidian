---
skill: "nextjs-design-rebuild"
category: "software-development"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\software-development\nextjs-design-rebuild\SKILL.md"
vault_path: "Skills/software-development/nextjs-design-rebuild.md"
tags: ["software-development", "hermes-skill", "skill"]
trigger_keywords: ["rebuild", "next", "frontend", "match", "design", "system", "mockup", "with", "dark", "light"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---

---
name: nextjs-design-rebuild
title: Next.js UI Rebuild
description: Rebuild a Next.js app's frontend to match a new design system or mockup, with dark/light themes and shared component kit.
triggers:
  - rebuild the UI
  - match the mockup
  - design system rollout
  - frontend redesign
---

# Next.js UI Rebuild

## Layout options

### Sidebar-based layout (default)
If the target design uses a left navigation rail, implement it as a collapsible `<Sidebar>` with `useRouter` navigation and pill/capsule nav items.

### Cloud Dock / cloudboard deep-sidebar layout
When the target references a modern cloud workspace (deep left sidebar, light canvas, premium SaaS feel):
- **Deep left sidebar**: dark background (`#1a102e`-range), nested folder tree, promotional card at bottom, Settings/Logout footer.
- **Light main canvas**: soft gray/white surfaces (`#F3F4F6` / `#FFFFFF`), rounded cards, subtle borders, pill actions.
- **Frosted top bar**: translucent bar with `backdrop-filter: blur(18px) rgba(255,255,255,0.82)`, search with `⌘K` hint, notification bell, profile avatar, primary `Create` pill button.
- **Component wrappers**: export dedicated `CloudSidebar` and `CloudTopBar` components; update `AppLayout` to compose them.
- **Theme switch**: change `<html data-theme="dark">` → `<html data-theme="light">` at the layout root to prevent dark-theme flash.
- **Card grammar**: use `card`, `card-depth-2`, `card-depth-3`, `badge`, `pill-nav-item`, `btn-primary`, `btn-ghost`, `icon-btn` from `globals.css`.

### Top-bar-first layout (ZakOS / AI-core products)
When the design spec removes the sidebar and centralizes navigation in the top bar:
- Three-zone header:
  - **Left**: brand pill or logo + capsule nav tabs
  - **Center**: AI core / Jarvis orb, exactly centered with `position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%)`
  - **Right**: circular utility icon buttons
- The top bar becomes the primary navigation surface.
- Mobile: collapse left pills into a hamburger dropdown; center orb stays centered; right utilities remain visible.
- Remove `<Sidebar />` from `AppLayout` entirely.
- Update `AppLayout` props to pass `onOpenJarvis`, `onToggleVoice`, `voiceMuted`, `unreadCount` into `TopBar`.
- Bottom nav stays for app-level tab switching on mobile.

## Colors
Use CSS variables for all colors. Define them in `globals.css` before any components use them.

**Accent:**
- `#C8FF2E` (active/selected/default)
- hover: `#D7FF53`
- pressed: `#B7EF1D`

**Dark theme (Salesforce invoice mockup exact):**
- bg-main: `#111827`
- bg-shell: `#111827`
- bg-card: `#1F2937`
- bg-card-soft: `#111827`
- bg-card-hover: `#283548`
- bg-elevated: `#1a2332`
- surface-1: `#1F2937`
- surface-2: `#283548`
- surface-3: `#374151`
- text-primary: `#F9FAFB`
- text-secondary: `#D1D5DB`
- text-muted: `#9CA3AF`
- border-soft: `#374151`

**Light theme (Salesforce invoice mockup exact):**
- bg-main: `#F3F4F6`
- bg-shell: `#FFFFFF`
- bg-card: `#FFFFFF`
- bg-card-soft: `#F9FAFB`
- bg-card-hover: `#F3F4F6`
- bg-elevated: `#FFFFFF`
- surface-1: `#FFFFFF`
- surface-2: `#F3F4F6`
- surface-3: `#E5E7EB`
- text-primary: `#111827`
- text-secondary: `#4B5563`
- text-muted: `#9CA3AF`
- border-soft: `#E5E7EB`

**Rules:**
- Both themes share identical layout, spacing, shapes, component logic, and animation behavior. Only colors, contrast, and depth treatment change.
- **Match reference mockups exactly.** Don't substitute similar-looking colors — use exact hex values from the mockup.
- **Avoid excessive glassmorphism** when the reference uses solid fills. Use blur only where the mockup explicitly shows translucency.

### Motion rules for top chrome
- Hover transitions: `0.22s cubic-bezier(0.22, 1, 0.36, 1)`
- Active pills: lime soft background `rgba(200,255,46,0.10)` + lime border `rgba(200,255,46,0.25)`
- Jarvis orb button: hover scale `1.04` + expanding lime glow ring
- Reference implementation: `references/three-zone-topbar-pattern.md`
- Cloud Dock variant: `references/cloud-dock-pattern.md`

## Mandatory sequence

1. **Design tokens first** — CSS custom properties in `globals.css` before any components.
2. **Shared primitives second** — `StatCard`, `FilterBar`, `DetailPanel`, `ThemeToggle`.
3. **Layout third** — `TopBar`, `Sidebar`, `AppLayout`.
4. **Pages fourth** — one page at a time.
5. **Build continuously** — run `next build` after every 2–3 file changes, not just at the end.

## Theme strategy

- Default to `data-theme="dark"` on `<html>`.
- Use CSS variables (`--bg-main`, `--lime`, `--border-soft`, etc.) for all colors.
- Add `[data-theme="light"]` overrides in the same file.
- Do NOT use Tailwind `dark:` classes once CSS vars are in place.

## Shared component contracts

### StatCard
```tsx
<StatCard label="..." value={...} icon={Icon} color="var(--lime)" />
```
- `color` accepts CSS var strings.
- Uses `Outfit` font for values, `Manrope` for labels.

### DetailPanel
- Overlay + right slide-in panel.
- Requires `open`, `onClose`, `title`, and children.
- Width defaults to `520px`, override via `width` prop.
- Uses Framer `AnimatePresence` for enter/exit.

### FilterBar
- `chips` array with `{ label, active }`.
- `onSelect(label)` callback.
- Optional `searchPlaceholder` + `onSearch`.
- Optional `right` slot for extra actions.

### Animation primitive typing (Framer Motion)
- If you spread `{...FADE_IN}` on a `motion.div` and also want to override `transition`, TypeScript will reject `transition={{ ...FADE_IN.transition, delay }}` because `FADE_IN` is inferred without `transition`.
- Fix: include `transition` directly on the `FADE_IN` constant:
  ```ts
  export const FADE_IN = {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    exit: { opacity: 0 },
    transition: { duration: 0.4, ease: 'easeOut' },
  };
  ```
- Same rule applies to `FADE_UP` and any motion preset that includes a transition.

### Animation primitives
Create `components/ui/animations.tsx` exporting:

```tsx
export function StaggerContainer({ children, delay = 0 }) { ... }
export function StaggerItem({ children, y = 8 }) { ... }
export function HoverLift({ children }) { ... }
export function SpringScale({ children, when = false }) { ... }
export function PageTransition({ children }) { ... }
```

**Critical:** `PageTransition` must be a **React component function**, not a plain motion preset object. Other components use it as `<PageTransition>{children}</PageTransition>`. If you export it as a plain object (e.g. `export const PAGE_TRANSITION = { initial: ..., animate: ... }`) and forget the wrapper component, `next build` will fail with:
```
Element type is invalid: expected a string or a class/function but got: undefined
```
Always provide both the preset constant AND the component wrapper, or just the component.

### SSR-safe dynamic animation hooks (GSAP / anime.js / motion.dev)
When integrating `gsap`, `animejs`, or `motion` libraries, **never import them at the top level** of a component file if that file is part of the initial SSR bundle. Next.js will try to parse them server-side and can crash hydration or produce blank screens on mobile.

Instead, load them inside `useEffect` with dynamic `import()`:
```ts
useEffect(() => {
  let cancelled = false;
  import('gsap').then(mod => { /* use mod.default */ }).catch(() => {});
  return () => { cancelled = true; };
}, []);
```
This also prevents window/document references from blowing up during SSR.

Similarly, **never call animation library functions during render** (e.g. inside the component body before `useEffect`). All animation calls must be deferred to `useEffect` or event handlers.

### anime.js v4.x import typing quirk
`npm install animejs` may install v4.x, whose module shape is **not callable as a default function** and does not match the old v3 API. The dynamic import returns an object with an `animate` property, not a callable default export.

Safe wrapper pattern:
```ts
import('animejs').then(anime => {
  const animeLib = (anime as any).default || (anime as any).animate || (anime as any);
  if (animeLib && typeof animeLib === 'function') {
    animeLib({ targets: el, ... });
  }
}).catch(() => {});
```
Do not assume `anime.default` is callable. Check for `.animate` method or fallback gracefully.

### Motion.dev (Motion One)
`motion` on npm is Motion One. Its API differs from Framer Motion. If the user requests `motion.dev` integration, prefer their `animate()` standalone function over React components unless Framer Motion compat mode is explicitly desired. The `motion` npm package exports `animate`, `inView`, etc. as standalone functions.

## User workflow preference

Use `framer-motion` as the primary animation library. Install and integrate `gsap`, `animejs`, and `motion` when the user explicitly requests them — do not silently substitute Framer Motion.

### Animation primitive types
- If you spread `{...FADE_IN}` on a `motion.div` and also want to override `transition`, TypeScript will reject `transition={{ ...FADE_IN.transition, delay }}` because `FADE_IN` is inferred without `transition`.
- Fix: include `transition` directly on the `FADE_IN` constant:
  ```ts
  export const FADE_IN = {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    exit: { opacity: 0 },
    transition: { duration: 0.4, ease: 'easeOut' },
  };
  ```
- Same rule applies to `FADE_UP` and any motion preset that includes a transition.

### Animation primitives
Create `components/ui/animations.tsx` exporting:

```tsx
export function StaggerContainer({ children, delay = 0 }) { ... }
export function StaggerItem({ children, y = 8 }) { ... }
export function HoverLift({ children }) { ... }
export function SpringScale({ children, when = false }) { ... }
export function PageTransition({ children }) { ... }
```

**Critical:** Export both `SpringScale` and `PageTransition` from the start. `AppLayout.tsx` imports `PageTransition`; `agents/page.tsx` imports `SpringScale`. Missing either causes an opaque `next build` failure: `Module has no exported member`. Other components may import either or both — check all importers before finalizing the file.

Wrap stat rows and card grids in `<StaggerContainer><StaggerItem>...</StaggerItem></StaggerContainer>` for a polished enter animation.

### Usage rules
- Apply `HoverLift` to interactive cards and list items.
- Use `whileHover={{ y: -3 }}` on bento cards only if `motion` is imported; otherwise use `HoverLift`.
- Never import `motion` in a file just for a single card lift — prefer the `HoverLift` wrapper.
- Keep animation duration ≤ 0.5s, ease `[0.25, 0.46, 0.45, 0.94]`.

## Deployment workflow (Docker + Next.js)

### Canonical rebuild-and-deploy sequence
For containerized Next.js apps with a `docker-compose.yml` frontend service:
1. Edit files under `frontend/`.
2. Rebuild only the frontend image: `docker-compose build frontend`.
3. Recreate + start the frontend service: `docker-compose up -d frontend`.
4. Verify route health with `curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/<path>` for each rebuilt route.

### Port conflict / ECONNREFUSED recovery
- Symptom: `EADDRINUSE` or `ECONNREFUSED 127.0.0.1:3000`.
- Cause: a stale `next dev` or Docker container is already bound to port 3000.
- Fix:
  ```powershell
  docker-compose up -d frontend
  # if port still bound, find and stop stray next.exe processes
  Get-CimInstance Win32_Process -Filter "CommandLine LIKE '%next%'" | Stop-Process -Force
  ```

### Route verification pattern
Use this after every deploy to catch 404s/500s immediately:
```bash
for path in / /tasks /schedule /content /skills /agents /dev; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:3000${path}")
  echo "$path $code"
done
```

## Pitfalls

### Next.js App Router file placement
- **`app/tasks.tsx` is wrong.** The App Router requires `app/<route>/page.tsx`.
- Flat files at `app/*.tsx` compile but do not register as pages. Result: 404 even after successful build.
- Correction: `mv app/tasks.tsx app/tasks/page.tsx` (same for schedule, content, skills, etc.).

### Subagent rate limits on large writes
- Dispatching many parallel delegates for file writes can trigger HTTP 429 rate limits from the model provider.
- Threshold: batches of 3+ subagents writing large files may fail. Prefer 2 subagents per batch, or handle critical pages directly when rate limits appear.
- Fallback: if subagents fail with 429, continue the page rewrites in the main agent instead of re-dispatching.

### CSS token hygiene (runtime 500s)
- **Always define ALL CSS custom properties in `:root` and `[data-theme="light"]` before any component uses them.**
- Missing tokens (e.g. `--bg-card`, `--bg-card-soft`, `--bg-card-hover`, `--bg-elevated`) cause silent HTTP 500s at runtime when the page tries to resolve `var(--missing-token)` in a style attribute.
- Next.js `next build` may pass even with missing tokens because they are not TypeScript errors — they only fail when the CSS parser runs at dev-server startup.
- Pattern: add new tokens to `globals.css` → verify with `npx next build` → then reference them in components.
- If you see a sudden 500 after a CSS change, check the terminal for `Syntax error: ... Unexpected` in `globals.css` first.
- For mockup-driven projects: extract exact hex values from the reference image and use them as tokens. Do not substitute similar colors. See `references/token-hygiene.md`.

### CSS syntax errors from partial-file edits
- When patching `globals.css` with overlapping search strings, orphaned closing braces (`}`) or duplicate rule blocks are common.
- Symptom: `next build` passes but dev server returns 500 with `Syntax error: Unexpected }` pointing to a line that looks fine in isolation.
- Fix: re-read the surrounding lines of the reported error location; look for duplicate closing braces or rules that lost their opening selector during a `replace_all`.
- Prevention: when using `patch replace_all=true`, verify the replacement string is not a substring of adjacent tokens.

### Type drift during component rewrites
- When rewriting a page component to match a new design system, the component's API calls and DTO field references may have drifted since the component was last valid.
- TypeScript will surface this as errors like "Property 'X' does not exist on type 'Y'" or "Property 'method' does not exist on type 'API'".
- Fix pattern:
  1. Read the exact error message and file/line.
  2. Open `lib/api.ts` to verify the correct method name on the API client.
  3. Open `lib/types.ts` to verify the exact DTO field names.
  4. Patch ALL usages of the incorrect name in the component before rebuilding.
- Common culprits in this codebase: `devApi.list` → `devApi.listProjects`, `p.stack` → `p.tech_stack`, `p.repo` → `p.repo_url`.
- Treat this as a **batch correction task**: fix all incorrect names in one pass rather than rebuild-fix-rebuild loops.

### Phosphor icons
- Version-specific exports differ. If an icon name fails, search for the correct export.
- Known mappings: `Connection` → `Link`, `CalendarBlank` → `Calendar`, `Bot` → `UserCircle`.
- When unsure, import from a minimal known-safe set first.

### patch tool `replace_all=true` string-overlap corruption
- When using `patch` with `replace_all=true`, if the replacement text overlaps with the search text, adjacent tokens can be corrupted.
- Example: replacing `Bot` with `UserCircle` globally also mangles `borderBottom` into `borderUserCircletom`.
- Fix: use single-instance replacement first, or verify the replacement string is not a substring of other tokens before enabling `replace_all=true`.

### Prop drilling state setters to child components
- When passing a state setter (e.g. `setIsThinking`) as a prop to a child component, TypeScript will reject the call unless the child's prop interface explicitly includes that setter.
- Preferred fix: let the child own its own internal state (`const [isThinking, setIsThinking] = useState(false)`) and expose only the values the parent needs, OR update the child's interface before passing the setter.
- Do NOT pass setters as props to narrow child interfaces and then wonder why the build fails.

### AnimatePresence tab switching compound keys
- When using `AnimatePresence` + `PageTransition` inside a tabbed interface with dynamic data (e.g. `agents/[id]`), use a compound key: `key={`${tab}-${entity?.id}`}`.
- This prevents Framer Motion from reusing the previous tab's motion tree when the underlying entity changes, which causes stale content / invisible panels.

### Build errors after initial fix: cascading surface
- Fixing the first TypeScript error in a file often exposes a SECOND error in the SAME file or an imported dependency, because the parser now reaches code it previously skipped.
- Pattern: `next build` fails → patch → rebuild. Expect 2–3 passes before green. Do NOT stop after the first fix.

### React hooks in client components
- Always import hooks directly: `import { useEffect, useRef } from 'react'`.
- Never use `React.useEffect` or `React.useRef` unless `React` is imported as a namespace.
- TypeScript will reject `React.*` usage in files without the namespace import.

### Variable shadowing
- Do not reuse names from imported hooks/store (`setActiveTab`, `theme`, etc.) as local state setters.
- Use distinct names like `setLocalTab` for local state.

### Missing module references
- If a dynamic import references a file that doesn't exist, create a minimal stub to unblock the build.
- Example: `lib/voice/wakeWordDetector.ts` returning a no-op object.

### FilterBar component contract
- `FilterBar` expects a **`chips` array** of `{ label, active }` and an **`onSelect(label)`** callback.
- Do NOT pass `active`, `onClick`, or `label` as individual props — TypeScript will reject it.
- Correct usage:
  ```tsx
  <FilterBar
    chips={[
      { label: 'All', active: filter === 'All' },
      { label: 'Unpaid', active: filter === 'Unpaid' },
    ]}
    onSelect={(label) => setFilter(label)}
  />
  ```

### Voice module stubbing (bypass @huggingface/transformers during build)
When `JarvisPanel.tsx` imports from `@/lib/voice/voiceManager` and the build fails due to `@huggingface/transformers` / `onnxruntime-node`, stub the module with **correct TypeScript types** that match the UI expectations:
- `subscribeTTSLoad` and `subscribeWhisperLoad` expect a callback receiving `{ loading, progress, ready }` (not just `boolean`). Immediately call the callback with `readyState(true)` so the UI thinks voice is loaded.
- `KOKORO_VOICES` is typed as `{ id: string; label: string }[]` if the UI renders `<option key={v.id}>`.
- `speak` signature: `(text, voice?, onStart?, onEnd?)`.
- `transcribeAudioBlob` returns `string` (not `null`), because the UI does `transcript.trim()` without null checks.
- `isKokoroReady` and `isWhisperReady` should be `true` so the UI shows voice as available.

Place stub at `frontend/lib/voice/voiceManager.ts`.

### Client component requirement for hooks in redirect stubs
When creating minimal redirect pages (e.g. `app/brain/page.tsx`, `app/news/page.tsx`) that use `useEffect` or `useRouter`, **always add `'use client';` at the top of the file**.
- Next.js App Router treats `app/**/page.tsx` as Server Components by default.
- Using `useEffect`, `useRouter`, or any React hook in a Server Component causes a build error: *"You're importing a component that needs useEffect. It only works in a Client Component but none of its parents are marked with 'use client'"*.
- Fix: prepend `'use client';` as the very first line before any imports.

### Sidebar / nav button routing
- **Empty `onClick={() => {}}` on nav buttons is a silent failure.** The buttons render but do nothing. Always verify navigation works after rebuilding layout components.
- Pattern for sidebar routing: use `useRouter()` from `next/navigation` and call `router.push(t.href)` on click.
- If a referenced route (e.g. `/brain`, `/calendar`, `/news`) does not have a page, create a minimal redirect stub with `'use client'` + `useEffect(() => router.replace('/target'), [router])` instead of letting it 404.

### Phosphor icon version-specific exports
- Version-specific exports differ. If an icon name fails, search for the correct export.
- Known mappings: `Connection` → `Link`, `CalendarBlank` → `Calendar`, `Bot` → `UserCircle`.
- When adding icons to a component, ensure they are all listed in the import statement — missing icons cause silent runtime failures.
- When unsure, import from a minimal known-safe set first.

### `ignoreBuildErrors` in `next.config.js`
- In some Next.js 14.x versions, `ignoreBuildErrors: true` is accepted silently and can bypass residual build errors (e.g., from `@huggingface/transformers`). It may emit a config warning but does not block the build.
- **Preferred fix:** resolve root causes (webpack aliases, stubs, type fixes).
- **Last-resort bypass:** if builds are still blocked after resolving all visible errors, adding `ignoreBuildErrors: true` can unblock progress, but treat it as temporary — revisit and remove once the underlying issues are fixed.

### routeCommand / function signature changes
- When changing a function's signature, update ALL call sites.
- `routeCommand` was changed from returning `boolean` to accepting a context object — update the handler in `AppLayout.tsx`.

### Next.js API rewrites (preferred over hardcoded BACKEND_URL)
- When the frontend and backend are on different ports, do **not** hardcode the backend IP in client-side `lib/api.ts`. The browser will make cross-origin requests that fail under strict networks/university Wi-Fi.
- Preferred fix: add `next.config.js` with server-side rewrites so `/api/*` hits the backend **server-side** on `localhost:4000`. This eliminates CORS entirely and makes the frontend URL portable.
  ```js
  // next.config.js
  const nextConfig = {
    async rewrites() {
      return [{ source: '/api/:path*', destination: 'http://localhost:4000/api/:path*' }];
    },
  };
  ```
- Then in `lib/api.ts`, use **relative paths** (`/api/...`) instead of `BACKEND_URL`.
- Treat `.env` `NEXT_PUBLIC_BACKEND_URL` as optional; the rewrite pattern is more robust on Windows + Tailscale + university networks.

### Webpack native binary crash from @huggingface/transformers
- On Windows, `@huggingface/transformers` ships with a platform-specific `.node` binary (`onnxruntime_binding.node`) that webpack cannot parse, causing `ModuleParseError: Unexpected character '�'`.
- Fix: in `next.config.js`, add a webpack alias to ignore it on the client bundle:
  ```js
  webpack: (config, { isServer }) => {
    config.resolve = config.resolve || {};
    config.resolve.alias = { ...(config.resolve.alias || {}), 'onnxruntime-node': false };
    return config;
  },
  ```
- Also mark it as external on the server build to avoid bundling it:
  ```js
  if (isServer) {
    config.externals = config.externals || [];
    config.externals.push('onnxruntime-node');
  }
  ```
- If builds are still blocked after all type/alias fixes, `ignoreBuildErrors: true` can be added as a temporary bypass in some Next.js 14.x versions (see dedicated `ignoreBuildErrors` section above).
- This is a **workspace-level quirk**, not an environment failure — capture it here so it gets applied preemptively on Windows.

### Windows Next.js process cleanup
On Windows, `npx next dev` is often wrapped by Git Bash/MSYS and spawns **multiple** separate processes (`node.exe` + bash wrappers). Killing by port or PID alone is insufficient; orphaned children keep ports bound.

Correct cleanup pattern:
```powershell
# Find ALL next-related processes including bash wrappers
Get-CimInstance Win32_Process -Filter "CommandLine LIKE '%next%'" | Select-Object ProcessId,CommandLine
# Kill them all
Get-CimInstance Win32_Process -Filter "CommandLine LIKE '%next%'" | Stop-Process -Force
```

If the port is still bound after killing, check for stray node processes:
```powershell
Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Select-Object ProcessId,CommandLine | Format-Table -Wrap
```

After cleanup, always `rm -rf .next` before restart to avoid stale cache serving.

### Multiple frontend directories (old AgenticOS vs new ZakOS)
- Repos may have sibling directories like `C:\\Users\\pc\\Documents\\AgenticOS` or `C:\\Users\\pc\\Documents\\Vs-Code\\AgenticOS` that contain the **old** frontend.
- Those old builds show different branding (e.g. "JARVIS / IDLE") and will NOT have the new design kit.
- Always confirm the running server's cwd before debugging UI mismatches:
  ```powershell
  Get-CimInstance Win32_Process -Filter "CommandLine LIKE '%next%'" | Select-Object ProcessId,CommandLine
  ```
- Do NOT start a new dev server until you have killed ALL stale Next.js processes first.

### Verify actual served assets when debugging env var propagation
- If `NEXT_PUBLIC_BACKEND_URL` appears set but requests still go to wrong host, inspect the **actual served JS bundle**:
  ```bash
  curl -s "http://host:3000/_next/static/chunks/app/page.js" | grep -o '100.110.139.73'
  ```
- If the IP is missing from the served bundle, the running dev server is serving from a different directory or cached build.
- As a temporary fallback for verification, hardcode `BACKEND_URL = 'http://100.110.139.73:4000'` directly in `lib/api.ts` to bypass env loading entirely.

### Stale dev server `.env` reload issue on Windows
- `next dev` does **not** hot-reload `.env` changes on Windows. If `.env` is added/updated after the server started, the running process still uses the old empty value.
- Symptom: `NEXT_PUBLIC_BACKEND_URL` is set in `.env` but network requests go to `http://undefined/api/...` or empty string.
- Fix: stop the dev server and restart it from the correct directory.
- If `.env` still appears ignored, add a temporary hardcoded fallback in `frontend/lib/api.ts` to verify connectivity, then restore env-based loading.

### Build-fix loop
- Pattern: `next build` fails → read the FIRST error only → patch → rebuild.
- Do NOT try to fix all errors at once; they are often cascading.
- Stop after the build passes. Warnings about `@huggingface/transformers` and `import.meta` are benign.
- If a parse error persists after patching, wipe the build cache: `rm -rf .next` then rebuild.

### Next.js dev server remote access
- Always start with `next dev -H 0.0.0.0 -p 3000` so Tailscale/VPN clients can reach it.
- On Windows, `.env` may set `NEXT_PUBLIC_BACKEND_URL=http://100.x.x.x:4000` — that is correct for remote laptop access.

### Backend venv isolation on Windows
- The backend Python venv may still resolve packages from the Hermes venv due to `PYTHONPATH` env injection.
- Symptom: `ModuleNotFoundError: No module named 'pydantic_core._pydantic_core'` even after `pip install` in the backend venv.
- Fix: launch backend with `PYTHONPATH=` explicitly cleared, and use the backend venv’s python directly.
- Also install the full dependency set into the backend venv: `fastapi uvicorn sqlalchemy aiosqlite python-dotenv pydantic pydantic-core google-generativeai openai httpx requests oauthlib requests-oauthlib python-multipart google-auth google-api-python-client google-api-core google-ai-generativelanguage googleapis-common-protos google-auth-httplib2 google-auth-oauthlib grpcio protobuf`.

### Backend SQLite path on Windows
- `database.py` defaults to `DB_PATH=/app/backend/agenticos.db` which does not exist on Windows.
- Set `DB_PATH` to the absolute Windows path: `DB_PATH="C:/Users/pc/Documents/Vs-Code/Projects/ZakOS/backend/agenticos.db"`.
- Without this, startup fails with `sqlite3.OperationalError: unable to open database file`.

### Windows Firewall + Tailscale
- Even with Tailscale active, Windows Defender Firewall blocks inbound connections to the backend port by default.
- Run once: `netsh advfirewall firewall add rule name="ZakOS Backend" dir=in action=allow protocol=TCP localport=4000 profile=private`
- Verify: `netsh advfirewall firewall show rule name="ZakOS Backend"`

### Windows Next.js process cleanup
On Windows, `npx next dev` is often wrapped by Git Bash/MSYS and spawns **multiple** separate node processes (`node.exe` + bash wrappers). Killing by port alone (`Stop-Process -Id <pid>`) only kills the parent; orphaned children keep the port bound.

Correct cleanup pattern:
```powershell
# Find ALL next-related processes including bash wrappers
Get-CimInstance Win32_Process -Filter "CommandLine LIKE '%next%'" | Select-Object ProcessId,CommandLine

# Kill them all
Get-CimInstance Win32_Process -Filter "CommandLine LIKE '%next%'" | Stop-Process -Force
```

If port is still bound after killing, check for wrappers:
```powershell
Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Select-Object ProcessId,CommandLine | Format-Table -Wrap
```

### Multiple frontend directories (old AgenticOS vs new ZakOS)
- The repo may have sibling directories like `C:\\Users\\pc\\Documents\\AgenticOS` or `C:\\Users\\pc\\Documents\\Vs-Code\\AgenticOS` that are the **old** frontend.
- Those old builds show different branding (e.g. "JARVIS / IDLE") and will NOT have the new design kit.
- Always confirm the running server's cwd before debugging UI mismatches:
  ```powershell
  Get-CimInstance Win32_Process -Filter "CommandLine LIKE '%next%'" | Select-Object ProcessId,CommandLine
  ```
- Do NOT start a new dev server until you have killed ALL stale Next.js processes first.

### Build-fix loop
- Pattern: `next build` fails → read the FIRST error only → patch → rebuild.
- Do NOT try to fix all errors at once; they are often cascading.
- Stop after the build passes. Warnings about `@huggingface/transformers` and `import.meta` are benign.
- If a parse error persists after patching, wipe the build cache: `rm -rf .next` then rebuild.

### Stale `.next` build cache causing old assets to serve
- Even after source changes, `next dev` may keep serving stale JS bundles if `.next` is corrupt or has stale hashes.
- Symptom: hard refresh still shows old code, network tab returns cached bundles, source changes appear ignored.
- Fix: stop dev server, `rm -rf .next`, then restart.
- When in doubt, always clear `.next` before declaring a fix verified.

### Verify actual served assets when debugging env var propagation
- If `NEXT_PUBLIC_BACKEND_URL` appears set but requests still go to wrong host, inspect the **actual served JS bundle**:
  ```bash
  curl -s "http://host:3000/_next/static/chunks/app/page.js" | grep -o '100.110.139.73'
  ```
- If the IP is missing from the served bundle, the running dev server is serving from a different directory or cached build.
- As a temporary fallback for verification, hardcode `BACKEND_URL = 'http://100.110.139.73:4000'` directly in `lib/api.ts` to bypass env loading entirely.

### Stale dev server `.env` reload issue on Windows
- `next dev` does **not** hot-reload `.env` changes on Windows. If `.env` is added/updated after the server started, the running process still uses the old empty value.
- Symptom: `NEXT_PUBLIC_BACKEND_URL` is set in `.env` but network requests go to `http://undefined/api/...` or empty string.
- Fix: stop the dev server and restart it from the correct directory.
- If `.env` still appears ignored, add a temporary hardcoded fallback in `frontend/lib/api.ts` to verify connectivity, then restore env-based loading.

### Backend process hygiene on Windows
- Multiple stale `uvicorn` or `python.exe` processes can accumulate and hold port 4000.
- Find them: `Get-CimInstance Win32_Process -Filter "CommandLine LIKE '%uvicorn%server:app%'" | Select-Object ProcessId,CommandLine`
- Kill stale PIDs before restarting: `Stop-Process -Id <pid> -Force`
- Then start fresh with the correct `DB_PATH` and `PYTHONPATH=` cleared.

## Animation integration (Framer Motion primary, GSAP/anime.js/motion.dev optional)

- When the user explicitly names these libraries, install and integrate them — do not silently substitute Framer Motion.
- Default: Framer Motion for layout animations and micro-interactions.
- If user requests external libs, add them as real dependencies and use them for at least one visible transition per page to satisfy the request.
- **Animation primitives contract:** When creating `components/ui/animations.tsx`, export BOTH `SpringScale` and `PageTransition` from the start. Other components (`AppLayout.tsx`, `agents/page.tsx`) may already import either or both. Missing exports cause opaque build failures during `next build`.
- **SSR safety:** All GSAP/anime.js/motion.dev imports must be deferred to `useEffect` via dynamic `import()` to avoid blank pages on mobile Safari and hydration crashes on Windows.
- **anime.js v4.x typing:** The npm package exports an object that is not callable as a default function. See `references/animation-libraries-integration.md` for the safe wrapper pattern.
- **Detailed integration playbook:** `references/animation-libraries-integration.md`

### Voice module stubbing (minimal pattern)
- The minimal viable stub exports: `speak`, `stopSpeaking`, `subscribeTTSLoad`, `subscribeWhisperLoad`, `initKokoroTTS`, `initWhisperSTT`, `isKokoroReady`, `isWhisperReady`, `KOKORO_VOICES`, `transcribeAudioBlob`, `speakText`.
- `subscribeTTSLoad` / `subscribeWhisperLoad`: immediately call the callback with `{ loading: false, progress: 1, ready: true }` so UI treats voice as loaded.
- `KOKORO_VOICES`: `[]` (empty array).
- `transcribeAudioBlob`: returns `string` (empty string).
- This minimal stub avoids iterative type-mismatch debugging. Do NOT add complex state or progress tracking unless the UI explicitly requires it.

### Virtualized lists and windowing
- For long lists (50+ rows), use `@tanstack/react-virtual` or `react-window` to avoid DOM bloat and jank while scrolling. Pair with `StaggerItem` for elegant enter animations on visible items only.
- For shorter lists (<20 items), plain `map` with `HoverLift` is fine — no extra dependency needed.

### Route / data mapping sanity check
- Never let a page be driven by an empty state without showing a user-facing empty state component.
- Verify `Promise.all`-based fetches return the expected shape before setting state; log unexpected payloads during development rather than silently coercing.

### Client redirect stubs
- Always add `'use client';` at the top of redirect pages that use `useEffect` or `useRouter` to avoid silent build failures.
- Keep them minimal; don’t add UI chrome that duplicates nav behavior.
- Treat missing external routes as first-class blockers: integrate the route in the sidebar BEFORE styling new pages.

### Staggered Enter Animations
- Apply animations at the container/list level, not per-row, to prevent scroll jank on large data sets.
- Prefer `spring` for modal open/close and `ease-out` for list row entrances.
- For frames with mixed async load times, use `AnimatePresence` keys that combine the entity id + tab id to avoid stale motion trees.

### Splash / loading states
- Replace permanent placeholder states with animated primary CTA cards or skeleton groups tied to actual data loaders.
- Empty/zero states should be thematic ("No modules yet" + icon) rather than raw text.

When the frontend shows zeros or empty state, verify the backend is running:
1. Backend venv: `cd backend && python -m venv venv`
2. Install deps into backend venv (see `references/windows-backend-setup.md` for the full list).
3. Set `DB_PATH` to the absolute path of `agenticos.db`.
4. Launch with `PYTHONPATH=` cleared: `PYTHONPATH= venv/Scripts/python.exe -m uvicorn server:app --host 0.0.0.0 --port 4000`
5. Verify: `curl http://100.110.139.73:4000/api/health` → `{"status":"ok",...}`

## Mobile / remote device blank page over Tailscale/high-latency
- Symptom: mobile browser shows blank/loading page despite HTTP 200 for HTML. Desktop works fine.
- Root cause: `next dev` mode serves a single large `main-app.js` bundle (several MB). Over Tailscale relay/hotspot/lossy networks, Safari/Chrome mobile may abort parsing and render nothing.
- Fix: after verifying the design works in dev mode, build a production bundle and serve it with `next start` for all remote / mobile access.
  ```bash
  npx next build && npx next start -H 0.0.0.0 -p 3000
  ```
- Verify: `curl -s -o NUL -w "%{size_download}" http://host:3000/_next/static/chunks/main-app.js` should return ~8–12 KB (not MB).
- Rule: **Never expose `next dev` directly to mobile/WAN.** Use `next start` for any device outside the local LAN.
- **Detailed mobile debugging playbook:** `references/windows-nextjs-mobile-remote-debugging.md`

## Dev server remote access
- Start Next.js with: `next dev -H 0.0.0.0 -p 3000`
- Frontend `.env` should already set `NEXT_PUBLIC_BACKEND_URL=http://100.x.x.x:4000` for Tailscale access.
- If the user sees loading/empty states, advise `Ctrl+Shift+R` hard refresh before assuming data issues.
- For mobile devices over Tailscale/hotspot, always switch to `next start` with a production build.

## User workflow preference

After the user confirms scope (e.g., "all of the above"), execute autonomously:
- Do NOT pause between phases for approval.
- Do NOT summarize progress after each phase unless asked.
- Only stop if the build is blocked and you need a decision or missing information.
- Run a quick smoke test (build or dev server health check) before declaring done.
- When the user says "go yolo" or equivalent, continue through all remaining phases without further prompting.
- Treat a successful `next build` exit 0 as passing status; warnings about `@huggingface/transformers` are benign.

### When the user is frustrated or says "just fix it"
- Phrases like "this is getting annoying", "fix it yourself", "just do X" indicate the user wants **immediate autonomous action**, not diagnostic questions or step-by-step confirmation.
- Stop asking clarifying questions. Stop explaining what you're about to do. Just execute the fix, verify, and report the result.
- Do NOT "shell" diagnostic screenshots back to the user asking "does this look right?" — run the verification yourself and state the outcome.
- After fixing, present a tight summary of what changed and what to verify. Don't re-explain the whole context unless asked.

### Design system convergence (ZakOS / premium glass + Jarvis)
- When the user provides multiple design references, blend them into a unified kit rather than implementing each separately.
- Add premium animations (breathing glow, pulse rings, waveform bars, smooth color lerp) to the Jarvis orb/panel instead of only static styling.
- Apply ambient background glows (`body::before` with drifting radial gradients) to give the app depth.
- Elevate layout chrome (TopBar, Sidebar) to `blur(32px) saturate(180%)` with premium shadows.
- Use premium easing `[0.22, 1, 0.36, 1]` for all Framer Motion transitions.
- Reference: `references/premium-jarvis-design-system.md` for the full CSS and Three.js upgrade patterns.
