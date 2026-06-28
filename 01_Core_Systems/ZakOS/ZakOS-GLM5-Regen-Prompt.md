---
tags: []
aliases: []
created: 2026-06-27
---
# ZakOS — Full Website Regeneration Prompt for GLM 5.2

## 1. Project Identity
- **App name:** ZakOS
- **Tagline:** AI Operating System
- **Style:** Jarvis-inspired cinematic dark UI
- **Branding rule:** Everywhere the app is named, it must say **ZakOS**, never AgenticOS. This includes logo text, titles, HTML `<title>`, manifest, error screens, and any visible app name.
- **Tone:** Premium, futuristic, responsive, with a teal/lime accent palette on a dark background.

## 2. High-Level Architecture
- **Frontend:** Next.js 14 (App Router) + TypeScript + Tailwind CSS
- **State:** Zustand
- **UI patterns:** Client-side animated panels, streaming chat, push-to-talk voice, 3D orb, bento-grid dashboard
- **Backend:** FastAPI (Python 3.11), SQLAlchemy, async SQLite, route modules mounted under `/api`
- **Deployment:** Docker Compose (frontend, backend, optional services)
- **Remote access:** Designed to be exposed over Tailscale; frontend must be able to call backend via a configurable public/tailscale IP.

## 3. Environment & Config
- Frontend env:
  - `NEXT_PUBLIC_BACKEND_URL` — base URL for all API calls (must be configurable, not hardcoded to localhost)
  - `NEXT_PUBLIC_MODE` — `hosted` or similar
  - `NEXT_PUBLIC_GOOGLE_CLIENT_ID`
- Backend env:
  - `NIM_API_KEY`, `GITHUB_TOKEN`, `GITHUB_BRAIN_REPO`
  - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
  - `OPENCLAW_PORT`, `HERMES_PORT`, `FREE_CLAUDE_PORT`
  - `MODE=hosted`
  - `DB_PATH=/data/agenticos.db`
  - `SECRET_KEY`
  - `APP_URL` (frontend origin)
- **Important:** Do NOT bake `localhost` into the frontend bundle. Use `NEXT_PUBLIC_BACKEND_URL` everywhere.

## 4. Pages & Routes
- `/` — Dashboard
- `/study` — UniBuddy (study modules)
- `/study/[module]` — Module detail
- `/dev` — DevBuddy (projects)
- `/dev/[project]` — Project detail
- `/agents` — Agents
- `/agents/[id]` — Agent detail
- `/knowledge` — Knowledge / obsidian brain sync
- `/settings` — Settings
- `/integrations/*` — future integrations
- `/calendar` — Calendar events
- `/news` — News
- `/memory` — Memory
- `/projects` — Projects list
- `/analytics` — Analytics
- `/cyber` — Cyber-themed module/page

## 5. Core UI Components & Features
### 5.1 Sidebar (desktop) + Bottom Nav (mobile)
- Desktop: collapsible left sidebar with icon + label nav items
- Mobile: fixed bottom navigation with icon + label tabs
- Branding: show **ZakOS** logo text + icon in sidebar header
- Sections in nav:
  - Home (Dashboard)
  - Study / UniBuddy
  - Dev / DevBuddy
  - Agents
  - Knowledge / Brain
  - Settings

### 5.2 Dashboard
- Top bar with:
  - Page title
  - Jarvis status indicator (idle/speaking/thinking)
  - Provider status pills (NIM, Brain, Google)
  - Mobile Jarvis button
- Bento-grid cards:
  - Study modules count (link to `/study`)
  - Dev projects count (link to `/dev`)
  - Events today (link to `/calendar`)
  - Unread emails count
  - Quick actions grid:
    - Ask Jarvis
    - Agents
    - Calendar
    - Knowledge
  - System status panel:
    - NIM AI, Brain, Google indicators (ON/OFF)
- Skeleton loading states for cards when data is loading.

### 5.3 Jarvis Panel (floating/overlay)
- Triggered from sidebar or mobile button
- Chat interface with:
  - Message bubbles (user right, AI left)
  - Markdown rendering for AI responses
  - Streaming text support (`typing-cursor` effect)
  - Interim transcript display while listening
- Voice controls:
  - Push-to-talk mic button
  - Mute/unmute TTS button
  - Voice selector dropdown (legacy Kokoro voices)
  - Whisper loading bar with progress %
- Tabs inside panel:
  - chat
  - calendar
  - email
  - (extensible)
- Legacy voice stack:
  - TTS: Kokoro-based `speak(text, voice, onStart, onEnd)`
  - STT: Whisper-based `transcribeAudioBlob(blob, language)`
  - Init functions: `initKokoroTTS()`, `initWhisperSTT()`
  - State subscriptions: `subscribeTTSLoad`, `subscribeWhisperLoad`
  - Voice list: `KOKORO_VOICES`
  - Compatibility alias: `speakText` for legacy call sites
- Do NOT use any OmniVoice adapter or `/api/voice/*` backend proxy in this regeneration. Use browser-native/Web APIs for voice unless explicitly requested later.

### 5.4 3D Jarvis Orb (JarvisBlob3D)
- Component: `JarvisBlob3D.tsx`
- Must render a cinematic audio-reactive orb
- Use Three.js / react-three-fiber or similar
- Orb should pulse/glow based on:
  - Idle state
  - Listening state
  - Speaking state
  - Thinking state
- Mobile: center-or-bottom placement when panel is open
- Desktop: can be embedded in topbar or panel header

## 6. Data Models (TypeScript)
```ts
type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  streaming?: boolean;
};

type JarvisState = 'idle' | 'listening' | 'thinking' | 'speaking';
type JarvisMode = 'general' | 'study' | 'dev';
type PanelTab = 'chat' | 'calendar' | 'email';

type Email = {
  id: string;
  subject: string;
  sender: string;
  snippet: string;
  score: number;
  action: string;
  score_reason?: string;
};

type CalendarEvent = {
  id: string;
  title: string;
  start?: string;
  location?: string;
};
```

## 7. Backend API Surface
All routes mounted under `/api`.

### 7.1 Core
- `GET /api/health` — app health + feature flags
- `POST /api/chat` or streaming endpoint — chat completions
- `POST /api/brain/sync` — trigger obsidian vault sync/index
- `GET /api/brain/files` — list indexed files
- `GET /api/brain/search` — semantic search over indexed notes

### 7.2 Email (Google)
- `GET /api/email/messages?score=true`
- `GET /api/email/{id}`
- `POST /api/email/{id}/read`
- `GET /api/email/summary`
- `GET /api/email/unread`

### 7.3 Calendar (Google)
- endpoints under `/api/calendar/` or `/api/email/` depending on design

### 7.4 OS / Agents
- `POST /api/os/command`
- `/api/agents/*`
- `/api/study/*`
- `/api/dev/*`
- `/api/knowledge/*`
- `/api/settings/*`

### 7.5 Voice (legacy path)
- **Do not implement `/api/voice/health`, `/api/voice/tts`, `/api/voice/stt`** unless explicitly requested. The frontend legacy voice stack should use browser APIs by default.

## 8. Styling & Theme
- Dark mode only
- CSS variables for:
  - `--bg-main`, `--bg-elevated`, `--bg-card-soft`
  - `--text-main`, `--text-soft`, `--text-dim`
  - `--lime`, `--lime-soft`, `--lime-border`
  - `--teal`, `--purple`, `--orange`, `--blue-accent`
  - `--danger`, `--border-soft`
- Fonts:
  - `Outfit` for display/headings
  - `Manrope` for body
  - `JetBrains Mono` for code/status
- Components:
  - Rounded-xl / rounded-2xl cards
  - Glassmorphism where appropriate
  - Subtle borders `rgba(255,255,255,0.06)` to `0.1`
  - Smooth transitions (`transition-all`, `duration-300`)

## 9. Mobile Behavior
- Sidebar hidden on mobile; replaced by bottom nav
- Jarvis orb bottom-centered on mobile when active
- Safe area insets respected (`safe-area-inset-bottom`)
- Touch targets >= 44px
- Responsive grid:
  - 1 col mobile
  - 2 cols md
  - 3 cols xl for dashboard

## 10. Observability & Brain Sync
- Brain service indexes an obsidian vault (GitHub repo configured via `GITHUB_BRAIN_REPO`)
- Show indexed file count in health (`brain_files`)
- Search should be semantic/keyword hybrid if possible
- Vault path example: `C:\Users\pc\Documents\Vs-Code\Mind-Galaxy`
- Treat vault as long-term second brain:
  - Link related notes
  - Avoid duplicates
  - Update notes only when adding real value

## 11. Deployment Details
- Backend container maps host port 4000 -> container 8001
- Frontend container maps host port 3000 -> container 3000
- All stateful data in `./data` bind mount + named volumes
- Restart policy: `unless-stopped`
- For Tailscale exposure:
  - Frontend `NEXT_PUBLIC_BACKEND_URL` must use the Tailscale IP (example `http://100.110.139.73:4000`)
  - Backend must listen on all interfaces (`0.0.0.0` inside container)
- Dockerfiles keep things minimal; prefer multi-stage where helpful.

## 12. What to Build in One Go
Please generate the **entire codebase** that implements the above, including:
1. `docker-compose.yml`
2. Backend `Dockerfile.backend`, `requirements.txt`, `main.py` (FastAPI app), `routes/*`, `models/*`, `services/*`
3. Frontend `Dockerfile.frontend`, `package.json`, `tsconfig.json`, `tailwind.config.*`
4. Next.js app structure under `frontend/app/` with all routes
5. Reusable UI components under `frontend/components/`
6. State management (`frontend/store/index.ts`)
7. API client (`frontend/lib/api.ts`)
8. Legacy voice module (`frontend/lib/voice/voiceManager.ts` + backup)
9. Command router (`frontend/lib/voice/commandRouter.ts`)
10. Types (`frontend/lib/types.ts`)
11. Global styles (`frontend/app/globals.css`)
12. Any required assets (`public/manifest.json`, icons)

## 13. Quality Bar
- The rebuilt site must look and feel like a premium Jarvis-style OS dashboard.
- Chat must stream realistically.
- Voice panel must have working push-to-talk UI hooks (even if voice is browser-native).
- Dashboard cards must load real backend data, not just static HTML.
- Mobile layout must be polished: bottom nav, bottom-centered orb, safe areas.
- No broken API calls in browser console.
- Branding must say **ZakOS** everywhere.

---
#core-systems #zakos

