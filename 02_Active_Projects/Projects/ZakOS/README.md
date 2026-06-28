---
tags: []
aliases: []
created: 2026-06-27
---
# AgenticOS — Jarvis-Style AI Operating System

A fully local AI OS dashboard — voice control, multi-agent orchestration, obsidian knowledge graph sync, university tools, and dev project management. Inspired by Iron Man's JARVIS.

---

## Features

| Module | Description |
|---|---|
| **Jarvis AI** | Orbital 3D orb, STT/TTS voice, wake word "Hello Jarvis", NIM-powered streaming chat |
| **UniBuddy** | Study modules, progress tracking, grade management, exam countdowns |
| **DevBuddy** | Dev project management, task boards, repo tracking |
| **Agents Manager** | Custom AI agents with any LLM/provider, per-agent system prompts |
| **Knowledge Map** | D3.js force graph of your obsidian brain repo |
| **Calendar** | Google Calendar integration with voice readout |
| **Gmail** | AI importance scoring (NIM), voice inbox summary |
| **Voice System** | Web Speech API (Chrome) + Kokoro-JS TTS neural voice (82MB, loads once) |
| **Terminal** | Whitelisted OS commands via Jarvis panel |

---

## Quick Start (Docker)

```bash
# 1. Clone
git clone https://github.com/your-repo/agentcos.git
cd agenticos

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Start
docker compose up --build

# 4. Open browser
open http://localhost:3000
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in:

```env
# Required: NVIDIA NIM API (AI chat)
NIM_API_KEY=your_nvapi_key_here

# Optional: GitHub Brain Repo (Obsidian sync)
GITHUB_TOKEN=your_github_token
GITHUB_REPO=username/your-obsidian-repo

# Optional: Google OAuth (Calendar + Gmail)
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret

# App mode
MODE=local                    # local | hosted
FRONTEND_URL=http://localhost:3000
APP_URL=http://localhost:3000  # Used for Google OAuth redirect
```

---

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or use existing)
3. Enable APIs:
   - `Calendar API`
   - `Gmail API`
4. Create credentials → OAuth 2.0 Client ID → Web application
5. Add authorized redirect URI: `http://localhost:3000/api/auth/google/callback`
6. Copy Client ID + Secret to `.env`
7. In the app: **Settings** → Connect Google Account
8. Calendar and Gmail will auto-populate in Jarvis panel

---

## Adding Your Brain (obsidian Sync)

1. Create a GitHub repo with your obsidian vault (or any Markdown files)
2. Generate a GitHub Personal Access Token with `repo` scope
3. Set in `.env`:
   ```env
   GITHUB_TOKEN=ghp_your_token_here
   GITHUB_REPO=username/my-obsidian-vault
   ```
4. In the app: **Knowledge** page → Sync Brain
5. The D3 force graph will populate with your notes as nodes

---

## Connecting Local AI Proxies

### OpenClaw / free-claude-code

1. Start your local proxy server (e.g., on port 8080)
2. In the app: **Agents** → Add Agent
   - Provider: `openai-compat`
   - Base URL: `http://localhost:8080/v1`
   - Model: whatever your proxy exposes

### Hermes (LM Studio / Ollama)

1. Start LM Studio / Ollama locally
2. Add Agent in the app:
   - Base URL: `http://localhost:11434/v1` (Ollama) or `http://localhost:1234/v1` (LM Studio)
   - Model: `hermes-2-pro` (or any installed model)

### Nvidia NIM

The default provider. Requires `NIM_API_KEY` set in `.env`.
Get a free API key at [build.Nvidia.com](https://build.Nvidia.com).

---

## Voice System Notes

### STT (Speech to Text)
- **Chrome/Edge**: Uses Web Speech API (instant, no download)
- **Firefox/other**: Falls back to Whisper.js (downloads ~50MB model on first use)
- Wake word: Say **"Hello Jarvis"** anywhere in the app

### TTS (Text to Speech) — Kokoro-JS
- **First load**: Downloads ~82MB ONNX model (shown with progress bar in Jarvis panel)
- **Subsequent loads**: Cached in browser, instant
- **Voice**: `af_bella` by default — change in the voice selector in the Jarvis input area
- **Fallback**: If Kokoro fails, uses browser's built-in SpeechSynthesis

### Voice Commands
| Say | Action |
|---|---|
| "Hello Jarvis" | Open Jarvis panel |
| "Jarvis, stop" | Close Jarvis |
| "Jarvis, go to dev" | Navigate to DevBuddy |
| "Jarvis, read my emails" | Switch to email tab |
| "Jarvis, what's today" | Read calendar events |
| "Jarvis, remember [text]" | Push note to brain |
| "Jarvis, run [cmd]" | Execute OS command |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14 (App Router), React 18, TypeScript |
| 3D/Viz | React Three Fiber, Three.js, D3.js |
| Animations | Framer Motion |
| State | Zustand |
| Backend | Python FastAPI (uvicorn) |
| Database | SQLite (aiosqlite + SQLAlchemy) |
| AI | Nvidia NIM (meta/llama-3.1-8b-instruct) |
| Voice STT | Web Speech API + @xenova/transformers (Whisper) |
| Voice TTS | kokoro-js (Kokoro-82M neural voice) |
| Deployment | Docker Compose |
| Knowledge Sync | GitHub + obsidian vault integration |

---

## Development

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn server:app --reload --port 8001

# Frontend
cd frontend
yarn install
yarn dev
```

Backend runs on port 8001, frontend on port 3000.

---

## Docker Compose Services

| Service | Port | Description |
|---|---|---|
| frontend | 3000 | Next.js app |
| backend | 8001 | FastAPI server |

Persistent volumes:
- `./data` → SQLite database
- `./brain` → Cloned brain repo

---

## License

MIT

---
#active-projects #projects #zakos

