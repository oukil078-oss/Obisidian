# AgenticOS – Project Spec

## 1. Vision

AgenticOS is a **local‑only, Jarvis‑style operating system for my life**, combining:

- Top AI models (via **NVIDIA NIM**, **free‑Claude‑Code**, and **OpenClaw**)
- A rich **web dashboard** with chat + terminal views
- Deep integration with:
  - **Study** (modules, grades, notes)
  - **Dev** (projects, repos, tasks)
  - **Personal systems** (Google Calendar, Gmail, Obsidian, filesystem)
- **Hermes Agent** for persistent, long‑running tasks
- Full **voice control** and **talk‑back**, like a personal Jarvis

Everything runs **locally** on my machine (no public hosting), but the design should be clean enough to demo to clients as a serious, production‑grade system.

---

## 2. Core Personas / Modes

AgenticOS has three main “personas” plus one global assistant:

### 2.1 Jarvis (Global Assistant)

Jarvis is the global orchestrator:

- Always available via:
  - A central animated “AI blob” button at the top‑center of the UI
  - Voice wake phrase: **“Hello Jarvis…”**
- Capabilities:
  - Answer general questions and perform reasoning (via NIM / Claude backend)
  - Read and summarize **Google Calendar**:
    - “What’s on my schedule today?”
  - Read and summarize **emails** on request:
    - “Jarvis, read my latest emails.”
  - Manage **OS‑level tasks**:
    - Open apps, run scripts, manage files (within safety limits)
  - Route tasks to other components:
    - UniBuddy (study)
    - DevBuddy (dev)
    - Hermes (long‑running work)
    - OpenClaw (multi‑agent workflows)

Jarvis is the main “face” of AgenticOS and is controlled by both text and voice.

### 2.2 UniBuddy (Study Assistant)

UniBuddy focuses on **university life**:

- Covers all **M1 CYB modules**, exams, grades, and study sessions
- For each module:
  - Dedicated page with:
    - Chat area for explanations, exam prep, Q&A
    - Notes and key concepts
    - Grades overview
    - Resources (PDFs, slides, lab sheets)
- Every UniBuddy chat is:
  - Stored in the local DB
  - Mirrored into **Obsidian** as markdown notes:
    - Example path: `UniBuddy/<Module>/<YYYY-MM-DD>.md`
    - Proper tags so Obsidian’s graph view shows connections

UniBuddy is the “study OS” layer of AgenticOS.

### 2.3 DevBuddy (Developer Assistant)

DevBuddy is the dev‑focused assistant:

- Manages **dev projects**:
  - Pulls repositories from GitHub
  - Allows cloning and working on them locally
  - Tracks tasks, bugs, and features
- AI capabilities:
  - Uses **Claude Code** through **free‑Claude‑Code** proxy for:
    - Explaining code, refactoring, tests, and scripts
  - Can also use **NIM coding models** when desired
- Project pages include:
  - Repo metadata
  - Task/issue list
  - AI “coding terminal” where DevBuddy can:
    - Run commands (through backend)
    - Suggest patches
    - Track changes in a Changelog

DevBuddy is the “development OS” layer.

### 2.4 Agents Manager

Agents Manager is where all AI agents are configured:

- Manages:
  - NIM agents
  - Claude agents (via free‑Claude‑Code)
  - Hermes agents
  - OpenClaw agents
  - Local models (Ollama/LM Studio later if needed)
- For each agent:

**Chat tab**  
- Direct chat interface with that specific agent  
- Shows responses and tool usage clearly  

**Settings tab**  
- Provider:
  - NVIDIA NIM
  - Claude via free‑Claude‑Code
  - Hermes
  - OpenClaw
  - Local/OpenAI‑compatible
- Configuration:
  - API key & base URL (stored server‑side)
  - Model list:
    - For NIM: fetched from `/v1/models`
    - For Claude proxy: list of configured backends
  - System prompt/persona text
  - Permissions (allowed tools, OS scope)

**Models**  
- Attach multiple models to one agent
- Optionally define:
  - Default model
  - Fallback model
  - Use‑case rules (e.g., long context vs short context)

Agents Manager is your control center for all AI “brains”.

---

## 3. Architecture Overview

### 3.1 Layered Architecture

AgenticOS is built in four layers:

1. **Frontend (local web UI)**
2. **Backend Orchestrator (local server)**
3. **Local Data OS**
4. **Voice + Conversation Layer**

#### 3.1.1 Frontend

Tech stack:

- React (Vite or Next.js)
- Either Tailwind CSS or carefully designed CSS

Main sections:

- **Jarvis HUD**
  - Central animated blob button
  - Shows live status (listening, thinking, speaking)
  - Opens Jarvis panel (chat + terminal view)

- **UniBuddy**
  - Dashboard with modules & exams
  - Module detail pages with chat and notes

- **DevBuddy**
  - Project dashboard (GitHub + local repos)
  - Project pages with AI coding terminal

- **Agents Manager**
  - List + detail pages for all agents
  - Model selection and configuration

- **Knowledge Map**
  - Visualization of Obsidian graph / local note graph

#### 3.1.2 Backend Orchestrator

Tech option 1: Node.js (Express/Fastify)  
Tech option 2: Python (FastAPI)

Responsibilities:

- **Routing / LLM orchestration**
  - NVIDIA NIM (OpenAI‑compatible)
  - free‑Claude‑Code proxy (Anthropic‑like)
  - OpenClaw (multi‑agent backend)
  - Hermes Agent (long‑running tasks)

- **Data services**
  - Manage study & dev data models
  - Manage agent configs and chat history

- **Integrations**
  - Google Calendar API
  - Gmail API
  - Obsidian vault (filesystem)
  - Git & GitHub APIs

- **OS control**
  - File read/write
  - Command execution (with safeties)
  - Launching apps / scripts

#### 3.1.3 Local Data OS

Storage:

- Initial version: SQLite or JSON
- Later: PostgreSQL if needed

Key entities:

- `Module`:
  - name, code, exam date, status, notes
- `Grade`:
  - module, assessment type, score, max score, date
- `StudySession`:
  - module, date, duration, goals, summary
- `Project`:
  - name, repo URL, local path, status, next action
- `Task`:
  - project, description, status, priority
- `Agent`:
  - name, provider, models, prompts, permissions
- `Chat`:
  - mode (Jarvis/UniBuddy/DevBuddy/Agent), transcript, metadata

Obsidian vault:

- Directory structure:
  - `UniBuddy/<Module>/<Date>.md`
  - `DevBuddy/<Project>/<Date>.md`
  - `Jarvis/<Topic>.md`
- Notes contain:
  - YAML front‑matter with tags, module/project IDs
  - Content with chat transcripts + summaries
- Graph is built from these notes using links and tags.

#### 3.1.4 Voice + Conversation Layer

Voice In:

- Option 1:
  - Browser Web Speech API (fast to implement)
- Option 2:
  - Local ASR (Pipecat + NIM or other ASR model)

Voice Out:

- Browser `speechSynthesis` as first implementation
- Later, optionally:
  - Backend TTS (NIM or external) with audio streaming

Conversation Flow:

- Jarvis endpoint accepts:
  - Text + optional audio metadata
- Recognizes mode (study / dev / system / agent)
- Routes to appropriate backend:
  - NIM model
  - free‑Claude‑Code proxy
  - Hermes / OpenClaw
- Returns text + optional structured actions:
  - OS commands
  - DB updates
  - Notifications

---

## 4. Integrations

### 4.1 NVIDIA NIM

- Base URL:
  - `https://integrate.api.nvidia.com/v1`
- Auth:
  - `NIM_API_KEY` stored as env var
- Endpoints used:
  - `/v1/chat/completions` for chat/assistant behavior
  - `/v1/models` to fetch available models
- Use cases:
  - Jarvis general reasoning
  - Some coding tasks with long context
  - Complex study explanations

### 4.2 free‑Claude‑Code

- Local proxy for Anthropic‑style API
- Runs at:
  - `http://localhost:<port>` (often 8082)
- Used for:
  - DevBuddy coding operations
  - Some agents in Agents Manager
- Setup:
  - Claude Code and Antigravity can be pointed to this proxy
  - Backend uses it as an Anthropic provider:
    - `ANTHROPIC_BASE_URL = http://localhost:8082`
    - `ANTHROPIC_AUTH_TOKEN = freecc` (for example)

### 4.3 Hermes Agent

- Self‑hosted AI agent with persistent memory
- Runs as:
  - A local server with HTTP/WebSocket API
- Used for:
  - Long‑running tasks:
    - Multi‑day study planning
    - Continuous improvement of workflows
- Integrated as:
  - A provider type in Agents Manager
  - A Jarvis target for “ongoing” projects

### 4.4 OpenClaw

- Multi‑agent orchestration system (CLI/Discord‑like)
- Runs locally on a port (e.g. `http://localhost:9000`)
- Connects to:
  - free‑Claude‑Code
  - NIM
  - Other providers
- AgenticOS:
  - Treats OpenClaw as a special agent
  - Exposes `/openclaw/chat` or similar backend endpoint
  - Jarvis uses OpenClaw for:
    - Complex dev workflows
    - Multi‑step planning

### 4.5 Obsidian

- Vault path configured in AgenticOS settings
- Backend writes notes to vault:
  - Study chats → module files
  - Dev sessions → project files
- Graph:
  - Obsidian’s own graph view when using the vault manually
  - AgenticOS can also:
    - Build a JSON graph from notes
    - Render a custom interactive graph in the browser

### 4.6 Google Calendar & Gmail

- Uses OAuth for:
  - Calendar
  - Gmail
- Backend:
  - `GET /calendar/today`:
    - Map to events with time and title
  - `GET /emails/unread`:
    - Summaries of unread emails
- Jarvis can:
  - Read schedule aloud
  - Summarize inbox

---

## 5. UX / UI Design

### 5.1 Global Layout

- **Top bar**:
  - Center: Jarvis blob (animated circle with label “Jarvis”)
  - Left: App name “AgenticOS”
  - Right: User avatar, settings icon, status indicator (online/offline)
- **Left sidebar**:
  - Tabs:
    - UniBuddy
    - DevBuddy
    - Agents
    - Knowledge Map
    - Settings
- **Main content**:
  - Changes based on tab
- **Bottom bar** (optional):
  - Logs / notifications
  - System messages

### 5.2 Jarvis Panel

Features:

- Chat timeline (user + Jarvis)
- Mode indicator (General / UniBuddy / DevBuddy / System / Agent)
- Toggle between:
  - Chat view
  - Terminal view (commands & outputs)
- Controls:
  - Mic button
  - Stop / cancel button
  - Settings shortcut

### 5.3 UniBuddy UI

- **Dashboard**:
  - Card grid of modules:
    - Module name
    - Exam date
    - Status (Planned / In Progress / Revised / Completed)
  - Upcoming exam timeline
- **Module page**:
  - Chat panel
  - Notes area (editable text + AI summaries)
  - Grades table
  - Resources list
  - Button: “Open in Obsidian”

### 5.4 DevBuddy UI

- **Dashboard**:
  - Repos list:
    - GitHub icon, repo name, local path status
  - Filters: Active / Paused / Done
- **Project page**:
  - Summary:
    - README preview
    - Tech stack
    - Next actions
  - Tasks list (with status)
  - AI coding terminal:
    - Chat + commands
  - Logs:
    - AI changes
    - Shell commands run

### 5.5 Agents Manager UI

- **Agents list**:
  - Cards with:
    - Name
    - Provider icon (NIM, Claude, Hermes, OpenClaw)
    - Default model
    - Status indicator
- **Agent detail**:
  - Tabs:
    - Chat
    - Settings
    - Activity
  - Settings:
    - Provider drop‑down
    - API key & base URL fields (not visible to frontend when possible)
    - Model selection (with dropdown fed by provider)
    - System prompt box
    - Permissions toggles

---

## 6. Voice & Jarvis Interaction Design

### 6.1 Voice Input Flow

1. User clicks Jarvis blob or says “Hello Jarvis”
2. Browser:
   - Starts recording audio
   - Uses Web Speech API or sends audio to backend ASR
3. Transcript is sent to `POST /jarvis`
4. Backend:
   - Determines intent & mode:
     - Study related → UniBuddy
     - Dev related → DevBuddy
     - OS control → System
     - Agent specific → Agents Manager
5. Backend calls appropriate provider:
   - NIM, Claude proxy, OpenClaw, Hermes, etc.

### 6.2 Voice Output Flow

1. Backend returns:
   - Response text
   - Optional structured actions (e.g. “show calendar”)
2. Frontend:
   - Displays text in chat
   - Uses `speechSynthesis` for TTS
3. Jarvis ensures:
   - Short, clear responses by default
   - Follow‑up details when asked

---

## 7. Phased Implementation Plan

### Phase 0 – Foundations

- Choose backend language (Node or Python)
- Initialize repo:
  - `agentic-os-backend`
  - `agentic-os-frontend`
- Implement:
  - Simple “Hello world” route: `/health`
  - Basic React page calling that route

**Goal:** Working full stack skeleton.

---

### Phase 1 – Core Backend & LLM Routing

Implement backend routes:

- `POST /chat/jarvis`
- `POST /chat/unibuddy`
- `POST /chat/devbuddy`
- `GET /nim/models`

Integrate:

- NIM client:
  - Reads `NIM_API_KEY`
  - Calls `/v1/chat/completions` and `/v1/models`
- free‑Claude‑Code client:
  - Base URL: `http://localhost:8082`
  - Sends Anthropic‑style payloads

Routing logic:

- Jarvis decides:
  - If mode is DevBuddy → Claude proxy by default
  - If mode is General / Study → NIM by default
  - Allow override per agent or per user preference

**Goal:** Text‑only Jarvis, UniBuddy, DevBuddy through backend.

---

### Phase 2 – Data Models for UniBuddy & DevBuddy

Implement storage (SQLite or JSON) for:

- Modules:
  - name, code, exam date, status, notes
- Grades:
  - module, type, score, max, date
- Study sessions:
  - module, date, duration, notes
- Projects:
  - name, repo URL, local path, status, next action
- Tasks:
  - project, description, status, priority

Frontend:

- UniBuddy:
  - Module dashboard
  - Module detail pages
- DevBuddy:
  - Project dashboard
  - Project detail pages

**Goal:** Persistent study and dev data with basic UI.

---

### Phase 3 – Obsidian Integration & Graph

Backend:

- Config: `OBSIDIAN_VAULT_PATH`
- Function to write markdown files:
  - `POST /obsidian/note`
  - Fields: path, title, content, tags
- Save:
  - UniBuddy chats per module
  - DevBuddy sessions per project
  - Important Jarvis conversations

Graph:

- Script to scan vault and build JSON graph:
  - Nodes = files
  - Edges = links / tags
- Frontend:
  - Knowledge Map page
  - Renders graph using D3.js or Cytoscape.js

**Goal:** Every major interaction becomes a node in Obsidian; you have a visual knowledge map.

---

### Phase 4 – Agents Manager

Backend:

- `Agent` model:
  - name, provider, baseUrl, apiKeyRef, models, systemPrompt, permissions
- CRUD endpoints:
  - `GET /agents`
  - `POST /agents`
  - `PUT /agents/:id`
  - `DELETE /agents/:id`
- `POST /agents/:id/chat`

Frontend:

- Agents list:
  - Cards with provider icons & status
- Agent detail:
  - Chat tab
  - Settings tab (provider, models, etc.)

**Goal:** Full control over multiple AI agents from one UI.

---

### Phase 5 – Jarvis Voice

Frontend:

- Implement mic controls & transcription:
  - Use Web Speech API for first version
- Implement TTS:
  - Use `speechSynthesis`
- Update Jarvis panel:
  - Show listening / thinking / speaking states

Backend:

- Jarvis handles voice commands:
  - Calendar queries
  - Email summaries
  - OS actions (with confirmations)

**Goal:** Talk to Jarvis and receive spoken responses.

---

### Phase 6 – Hermes & OpenClaw Integration

Hermes:

- Run Hermes server locally
- Add Hermes as provider in Agents Manager
- Jarvis:
  - Delegates long‑term tasks to Hermes

OpenClaw:

- Run OpenClaw as local service
- Add “OpenClaw” agent in Agents Manager
- Backend:
  - `POST /openclaw/chat` → call OpenClaw API
- Jarvis:
  - Uses OpenClaw for complex multi‑step workflows

**Goal:** Multi‑agent orchestration inside AgenticOS.

---

### Phase 7 – OS Control & Safety

Backend:

- Implement OS command service:
  - Whitelist allowed commands
  - Log every command (who, when, what)
- Jarvis:
  - Always confirms dangerous actions
  - Example:
    - “Jarvis, delete folder X” → “Are you sure? (yes/no)”

Frontend:

- OS log panel:
  - List of commands run
  - Status (success/fail)

**Goal:** Powerful but safe “war machine” capabilities.

---

### Phase 8 – Polish & Portfolio Readiness

- Visual polish:
  - Modern dark theme, consistent typography
  - Smooth animations for Jarvis blob, transitions
- Documentation:
  - README, architecture diagram
  - Short demo video script
- Demo scenarios:
  - Study: UniBuddy helps prep an exam
  - Dev: DevBuddy + Claude proxy refactors code
  - Jarvis: voice interaction with calendar & email
  - Agents: NIM + Hermes + OpenClaw all visible and configurable

**Goal:** A showpiece project ready for your portfolio and demos.

---

## 8. How to Use This Spec in Future Chats

When returning to this project:

- Paste relevant sections of `AgenticOS.md` into the chat
- Then say something like:
  - “Let’s implement Phase 1 backend in Node.”
  - “Design the UniBuddy DB schema from Phase 2.”
  - “Help me wire Jarvis voice control from Phase 5.”
- This keeps context consistent and avoids repeating the whole design each time.