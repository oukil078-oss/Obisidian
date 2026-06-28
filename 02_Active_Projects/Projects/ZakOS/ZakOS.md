---
tags: [project, ai, docker, fullstack, voice]
aliases: [AgenticOS]
created: 2026-06-22
status: active
priority: high
relatedProjects:
  - "DawaDzLink"
githubRepo: ""
techStack:
  - Next.js
  - React
  - TypeScript
  - Three.js
  - D3.js
  - FastAPI
  - Python
  - Docker
  - SQLite
  - Google AI (Gemini) - Primary
  - NVIDIA NIM - Fallback
  - Kokoro-JS
notes: |
  Jarvis-style AI OS dashboard with voice control, multi-agent orchestration,
  Obsidian knowledge graph sync, university tools, and dev project management.
  Configured to use Google AI (Gemini) API as the primary LLM provider with
  automatic fallback routing to NVIDIA NIM if rate-limits or token exhausts occur.
links:
  - "Projects"
  - "Zakarya Oukil"
  - "DawaDzLink"
---
# ZakOS — Project Reference

> **Main Documentation Hub** for the ZakOS / AgenticOS project

---

## Overview

ZakOS (AgenticOS) is a fully local AI operating system dashboard inspired by Iron Man's JARVIS. It combines voice-controlled AI interaction, multi-agent orchestration, obsidian knowledge graph synchronization, university study tools, and development project management into a unified interface.

### Key Modules
- 🧠 **Jarvis AI** — 3D orbital orb, STT/TTS voice, wake word activation, streaming chat via Google AI (Gemini) with Nvidia NIM fallback.
- 📚 **UniBuddy** — Study modules, progress tracking, grade management, exam countdowns.
- 🛠️ **DevBuddy** — Developer project management, task boards, repository tracking.
- 🤖 **Agents Manager** — Custom AI agents with any LLM/provider, per-agent system prompts.
- 🕸️ **Knowledge Map** — D3.js force graph visualization of your obsidian brain repo.
- 📅 **Calendar** — Google Calendar integration with voice readout.
- 📧 **Gmail** — AI importance scoring, voice inbox summary.
- 🖥️ **Terminal** — Whitelisted OS commands via Jarvis panel.

### AI Provider Strategy
- **Primary Engine**: Google AI (Gemini) API (`gemini-1.5-pro` / `gemini-1.5-flash`).
- **Resilient Fallback**: Automatically fall back to NVIDIA NIM API (e.g. `meta/llama-3.1-70b-instruct`) in real-time upon encounter of rate limits, quota issues, or token exhaustion, ensuring seamless voice operation without interruption.

---

## 🚀 Quick Start

```bash
# 1. Start all services
docker compose up --build

# 2. Open browser
open http://localhost:3000
```

---

## 📂 Documentation Structure

| File | Purpose | Link |
|------|---------|------|
| `README.md` | Main project guide and quick start | ZakOS/README |

---

## 🏗️ Architecture

See [ZakOS README](./README) for full service diagram and data flows.

---

## 🔗 Related

- Projects — All my GitHub projects
- Zakarya Oukil — My personal Profile
- DawaDzLink — Medication distribution platform

---

## 🏷️ Tags

`#zakos` `#agenticos` `#jarvis` `#ai` `#voice` `#docker` `#nextjs` `#python` `#fastapi` `#obsidian` `#knowledge-graph` `#fullstack`

---

*Last updated: June 22, 2026*

---
#active-projects #projects #zakos

