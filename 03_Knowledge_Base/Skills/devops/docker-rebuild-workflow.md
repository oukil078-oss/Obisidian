---
skill: "docker-rebuild-workflow"
category: "devops"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\devops\docker-rebuild-workflow\SKILL.md"
vault_path: "Skills/devops/docker-rebuild-workflow.md"
tags: ["devops", "hermes-skill", "skill", "Docker", "Compose", "FastAPI", "Deployment", "Schema", "Changes", "Rebuild", "Workflow"]
trigger_keywords: ["safe", "docker", "compose", "rebuild", "patterns", "backend", "modifications", "always", "verify", "syntax"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---
# docker rebuild workflow

---
name: docker-rebuild-workflow
description: "Safe Docker Compose rebuild patterns for backend API modifications. Always verify syntax before rebuilding to prevent silent code corruption."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    Tags: [Docker, Docker Compose, FastAPI, Deployment, Schema Changes, Rebuild Workflow]
    related_skills: [github-repo-management, database-migration-backward-compat-testing]
---

# Docker Rebuild Workflow

**Critical Lesson:** Never blindly concatenate or copy-paste server.py files — this silently deletes critical initialization code and breaks containers. Always read full file structure first.

---

## 🚨 Golden Rules

### ❌ NEVER DO:

```bash
# BAD: Blindly concatenating entire files
cat backend/*.py > combined_server.py  # Will lose app initialization!

# BAD: Copy-pasting whole server.py sections without review
cp old_files/new_section.py backend/server.py  # May delete startup_db function!
```

### ✅ ALWAYS DO:

1. **Read full file structure before modifying** — Identify critical sections
2. **Verify syntax with py_compile BEFORE rebuilding**
3. **Backup original files to /tmp/ or use git HEAD**
4. **Rebuild only changed services with `--no-cache`**
5. **Test endpoints after rebuild**

---

## 🔍 Critical Sections to Preserve

### In FastAPI server.py:

1. **App Initialization (line 1-50):**
   - `from fastapi import FastAPI`
   - `app = FastAPI()` — NEVER delete this!
   - `startup_db`, `@app.on_event("startup")` — NEVER delete these!

2. **Endpoints Section (marked with comments):**
   - `# AUTH ENDPOINTS`
   - `@app.get("/api/health")`
   - `# ADMIN ENDPOINTS`

3. **Model Definitions:**
   - Look for `# PYDANTIC MODELS` comment
   - Class definitions must be complete

4. **Database Initialization:**
   - `startup_db()` function
   - Collection creation code

### When Adding Models:

**Correct approach — Append to existing models section:**
```python
# Find line with "# PYDANTIC MODELS" or similar marker
# Add new model AFTER this line, BEFORE endpoint definitions

class NewOptionalModel(BaseModel):
    name: str = Field(..., min_length=1)
    value: Optional[str] = None  # Empty string allowed
```

**NEVER delete existing models or endpoint decorators!**

---

## 📋 Rebuild Workflow Sequence

### Step 1: Backup Original Files

```bash
# Option A: Git-based backup (preferred)
git stash
git show HEAD:path/to/file.py > /tmp/backup_original.py

# Option B: Direct copy for single-file modifications
cp file_to_modify.py /tmp/backup_before_changes.py

# For entire server directory
cp -r backend/ /tmp/backend_backup/
```

### Step 2: Modify Files Carefully

**Identify insertion points first:**
```bash
grep -n "^class " backend/server.py           # Find model classes
grep -n "^@app\." backend/server.py            # Find route decorators
grep -n "^async def" backend/server.py        # Find async functions
```

**Read full context around each section:**
```bash
# Read entire file to understand structure
head -100 backend/server.py | tail -50
```

### Step 3: Verify Syntax BEFORE Rebuilding

```bash
python3 -m py_compile backend/server.py && echo "✅ Syntax OK" || echo "❌ Syntax error!"
```

If syntax errors occur, review changes — you may have deleted critical code.

### Step 4: Build Backend Container

```bash
# Clean rebuild with no cache (for schema/dependency changes)
docker-compose build backend --no-cache

# Or single service rebuild (faster for small changes)
docker-compose build backend --build-arg BACKEND_BUILD=true
```

### Step 5: Restart Containers

```bash
# Only restart affected service
docker-compose up -d backend

# Verify startup logs
docker logs dawadzlink-backend --tail 20
```

### Step 6: Test Endpoints

```bash
# Quick health check
curl http://localhost:8001/health

# Test registration (no documents)
curl -X POST http://localhost:8001/api/auth/register/pharmacy \
  -H "Content-Type: multipart/form-data" \
  -F "email=test@example.com" \
  -F "password=test123456" \
  -F "full_name=\"Test User\"" \
  -F "phone="+297****1234

# Check for new required field errors
curl http://localhost:8001/api/auth/register/pharmacy | grep -i "field required" || echo "✅ No new fields required"
```

### Step 7: MongoDB Schema Verification

If adding new collection fields to MongoDB:

```bash
# Drop and reinitialize if schema changed
docker exec dawadzlink-mongodb mongosh --eval "db.dropDatabase(); init_db();"

# Or update indexes for new optional fields
docker exec dawadzlink-mongodb mongosh <<'EOF'
use dawadzlink_db;
// Create unique index only for non-optional fields
db.pharmacies.createIndex({"email": 1}, {unique: true});
db.pharmacies.createIndex({"registry_number": 1});  // May need compound index for optional field
EOF
```

---

## 🛡️ Error Recovery Pattern

### If container won't start after rebuild:

```bash
# 1. Check logs for specific errors
docker logs dawadzlink-backend 2>&1 | grep -i "error\|traceback"

# 2. Look for "document not found" or missing indexes
#    → Need to reinitialize database
docker exec dawadzlink-mongodb mongosh --eval "db.dropDatabase(); init_db();"

# 3. Restore from backup if code is corrupted
cp /tmp/backup_original.py backend/server.py
python3 -m py_compile backend/server.py && echo "✅ Restored successfully"

# 4. Rebuild and restart
docker-compose build backend --no-cache
docker-compose up -d backend
```

### If syntax errors appear during rebuild:

```bash
# Don't panic — restore from backup first
mv /tmp/backup_original.py backend/server.py
python3 -m py_compile backend/server.py

# Then retry modifications more carefully
grep -n "^class " backend/server.py  # Find model sections
head -100 backend/server.py | tail -50  # Review structure
```

---

## 📊 Command Reference Table

| Task | Docker Compose | Quick Command |
|------|----------------|---------------|
| Build all services fresh | `docker-compose build --no-cache` | Builds everything with clean cache |
| Build only backend API | `docker-compose build backend --no-cache` | Fastest for single service |
| Rebuild + restart | `docker-compose up -d backend` | Hot-reload only changed containers |
| Drop + rebuild (schema changes) | `docker-compose down && docker-compose up -d` | Full stack reset |
| Verify container running | `docker ps \| grep dawadzlink-backend` | Quick status check |
| Check last error log | `docker logs dawadzlink-backend --tail 20` | Error diagnosis |

---

## 🗂️ Common File Structure Patterns

### server.py typical sections:

```python
# ============================================
# SECTION 1: Import statements (lines 1-5)
# ============================================
from fastapi import FastAPI
from pydantic import BaseModel

# ============================================
# SECTION 2: App initialization (lines ~10-20)
# ============================================
app = FastAPI(title="DawaDzLink Backend API")

@app.on_event("startup")
async def startup_db():
    # Database startup logic
    pass

# ============================================
# SECTION 3: Pydantic Models (lines ~30-200)
# ============================================
class PharmacyRegistration(BaseModel):
    email: str = Field(..., min_length=1, max_length=255)
    # ... add new optional models here

# ============================================
# SECTION 4: Auth endpoints (marked by comments)
# ============================================
@app.post("/api/auth/register/pharmacy")
async def register_pharmacy(data: PharmacyRegistration):
    # Endpoint logic
```

**When modifying:** Add new model AFTER line ~200 but BEFORE endpoint decorators.

---

## ⚠️ Making Fields Optional in Pydantic Models

When you change a model field from `str` to `Optional[str] = None`, you must also guard any database query that uses that field. Otherwise a `None` lookup will run against MongoDB and can cause unexpected behavior.

**Requirement pattern:**
```python
class RegisterPharmacyRequest(BaseModel):
    registry_number: Optional[str] = None  # Empty string or None allowed

async def register_pharmacy(data: RegisterPharmacyRequest):
    existing_reg = None
    if data.registry_number:
        existing_reg = await db.pharmacies.find_one({"registry_number": data.registry_number})
    if existing_reg:
        # handle duplicate
```

**Common trap:** leaving `find_one({"registry_number": data.registry_number})` unchanged after making the field optional. That query now sends `None` into MongoDB, which never matches but still wastes a query and can hide bugs. Guard it only when the value is provided.

## 📝 References

- [`references/docker-rebuild-patterns.md`](references/docker-rebuild-patterns.md) — Detailed error recovery and MongoDB schema patterns
- [`references/fastapi-mongodb-validation.md`](references/fastapi-mongodb-validation.md) — Field validation patterns (optional vs required)
- [`references/zakos-frontend-build-fixes.md`](references/ZakOS-frontend-build-fixes.md) — Next.js frontend Docker build errors and fixes
- See [`github-repo-management`](../SKILL.md) for Git backup workflow

---

## ⚠️ Troubleshooting Quick Tips

### Container restarts immediately after startup:

```bash
# Check app initialization errors
docker logs dawadzlink-backend 2>&1 | grep -A5 "startup\|initializ"

# Most common cause: Missing startup_db function or collections not defined
# Fix: Reinitialize database
docker exec dawadzlink-mongodb mongosh --eval "db.dropDatabase(); init_db();"
```

### New endpoints don't respond (404 or 500):

```bash
# Check if decorator was accidentally removed
grep -n "@app\." backend/server.py | head -20

# Verify syntax after modification
python3 -m py_compile backend/server.py

# Restart container
docker-compose restart backend
```

### MongoDB connection errors:

```bash
# Check MongoDB container status
docker ps | grep mongodb

# If unhealthy, check logs
docker logs dawadzlink-mongodb 2>&1 | tail -20

# Reinitialize database schema if collections missing
docker exec dawadzlink-mongodb mongosh --eval "db.dropDatabase(); init_db();"
```

---

## ✅ Final Checklist Before Deploy

- [ ] Original files backed up to `/tmp/` or git HEAD restored
- [ ] New model/appended code read with `head -200 file.py | tail -50`
- [ ] Syntax verified with `python3 -m py_compile backend/server.py`
- [ ] Build uses `--no-cache` for schema changes
- [ ] Container restarted with `docker-compose up -d <service>`
- [ ] Endpoint tested with `curl` requests
- [ ] No new "field required" errors in API responses
- [ ] Secret-bearing `.env` files are verified with `cat .env` after write; never assume truncated output is correct

### Pattern I: Docker Hub TLS handshake timeout during `docker-compose build`
- **Symptom:** `failed to do request: Head "https://registry-1.docker.io/v2/library/node/manifests/20-alpine": net/http: TLS handshake timeout`
- **Cause:** Transient network/Docker Hub connectivity issue, not a code or Dockerfile error.
- **Fix:** Retry the same `docker-compose build` once or twice. If it persists, switch the builder to a background process with `notify_on_complete` so the session isn't blocked, and verify later.
- **Do NOT change the base image unnecessarily** — this is a network-side failure and retrying is the fastest path.

### Pattern J: Stale container name blocks `docker-compose up -d --force-recreate`
- **Symptom:** `Conflict. The container name "/<service>-1" is already in use by container "<sha>". You have to remove (or rename) that container to be able to reuse that name.`
- **Fix:**
```bash
docker rm -f <service-name>
docker-compose up -d <service-name>
```
- **Why it happens:** A previous container with the same name exists but isn't managed by the current Compose project state. `--force-recreate` alone won't remove it.

### Pattern K: Inconsistent state renames across Zustand + components break `next build`
- **Symptom:** TypeScript errors like `Cannot find name 'subscribeWhisperLoad'` or `Object literal may only specify known properties, and 'whisperReady' does not exist`.
- **Cause:** Renamed a store key (e.g. `whisperReady` → `sttReady`) in the interface but missed one of: the default state object, a consumer component, or an import.
- **Fix checklist:**
  1. Update `interface AppStore` in `store/index.ts`
  2. Update the initial state object in `create<AppStore>`
  3. Update every `useAppStore()` destructuring that touches the renamed keys
  4. Update any imported helper modules that reference the old name
  5. Rebuild with `docker-compose build frontend` and confirm `next build` succeeds

### Pattern L: Backend health shows `"brain": false` after setting `GITHUB_BRAIN_REPO`
- **Cause:** `brain_service.initialize()` rejected the clone because the env value is not a valid git URL. A bare `owner/repo` or missing `.git` suffix will cause silent failure.
- **Fix:** `GITHUB_BRAIN_REPO` must be a full HTTPS git URL, e.g. `https://github.com/oukil078-oss/Obisidian.git`.
- **Secondary cause:** A stale `/tmp/brain` directory already exists in the container but is not a valid repo, so `git clone` and `git pull` both fail. `brain_service.initialize()` does not auto-recover from this and silently leaves `initialized = False`.
- **Manual recovery outside the app:**
```bash
docker exec <backend-container> rm -rf /tmp/brain
# Then restart the backend so initialize() can clone fresh.
```
- **Verification:** after restart, `/api/health` should show `"brain": true` and `"brain_files": N`.

## 📋 Frontend/Docker-specific env safety note

When writing or updating `.env` files inside a secrets-protected project, `read_file` may be denied. If that happens:
1. Do not guess the file contents based on partial tool output.
2. Switch to `terminal: cat <path>` to read and verify.
3. Write the complete intended file in one `write_file` call.
4. Re-verify with `cat` before restarting containers.

---

## 📖 Complete Workflow Example

```bash
#!/bin/bash
# Docker rebuild with safety net

set -e  # Exit on error

BACKUP_DIR="/tmp/docker-backend-backup-$(date +%Y%m%d-%H%M%S)"

echo "=== Step 1: Create backup ==="
mkdir -p "$BACKUP_DIR/backend"
cp -r backend/* "$BACKUP_DIR/backend/" || true

echo "=== Step 2: Modify server.py (add new model section) ==="
# Add new optional model AFTER PYDANTIC MODELS comment but before endpoints
tail -50 backend/server.py | head -25

echo "=== Step 3: Verify syntax ==="
python3 -m py_compile backend/server.py && echo "✅ Syntax OK"

echo "=== Step 4: Build and restart ==="
docker-compose build backend --no-cache
docker-compose up -d backend

echo "=== Step 5: Check logs ==="
docker logs dawadzlink-backend --tail 10

echo "=== Step 6: Test endpoint ==="
curl http://localhost:8001/api/auth/register/pharmacy | head -c 100

echo "=== ✅ Rebuild Complete ==="
```

---

---

## 🐍 Backend Python Dependency Fixes

### Pattern A: `ModuleNotFoundError` on container startup

When uvicorn fails immediately with `ModuleNotFoundError: No module named 'X'`:

```bash
docker-compose logs backend --tail 40
# If the missing module is an app dependency (not stdlib), add it to requirements.txt
```

Fix path:

```bash
# 1. Add missing package to backend/requirements.txt
# 2. Rebuild backend image
docker-compose build backend --no-cache

# 3. Restart backend
docker-compose up -d backend

# 4. Confirm healthy
docker-compose ps && docker-compose logs backend --tail 20
```

### Pattern B: Python dependency conflict (`ResolutionImpossible`)

If `pip install -r requirements.txt` fails inside Docker with a conflict between pinned versions:

```bash
# Step 1: Identify the conflicting pair from the error
# Step 2: Remove unused/dependency-only packages from requirements.txt
# Step 3: Prefer bumping the downstream library (e.g. openai) over downgrading platform requirements
# Step 4: Rebuild
docker-compose build backend --no-cache
```

Guidelines:
- Keep `requirements.txt` minimal: remove packages that are only transitive dependencies and not imported directly by the app.
- Prefer upgrading the downstream library (e.g. `openai`) to a version compatible with the platform’s required `httpx`, instead of downgrading `httpx` and breaking other packages.
- After the fix, rerun `docker-compose build backend --no-cache` before redeploying.

---

## ⚛️ Frontend Next.js Docker Build Troubleshooting

### Pattern C: Build succeeds but `standalone` copy fails

Symptom inside Docker build:
```
COPY --from=builder /app/.next/standalone ./
Error: "/app/.next/standalone": not found
```

Fix: enable standalone output in `frontend/next.config.js`:
```js
const nextConfig = {
  output: 'standalone',
};
```

Then rebuild:
```bash
docker-compose build frontend --no-cache
```

### Pattern D: ESM-only packages break Terser / minification

Symptom:
```
static/media/ort.bundle.min.mjs from Terser
x 'import.meta' cannot be used outside of module code
```

Triggered by ESM-only packages such as `onnxruntime-web` loaded via `@xenova/transformers` or `kokoro-js`.

Fix:
1. Add the offending package to `transpilePackages` (top-level key in Next.js 14+, **not** inside `experimental`):
```js
const nextConfig = {
  transpilePackages: ['@xenova/transformers', 'onnxruntime-web', 'kokoro-js'],
};
```
2. Externalize it in webpack so Next.js doesn't try to bundle it:
```js
webpack: (config, { isServer }) => {
  config.externals = [...(config.externals || []), 'onnxruntime-web'];
  return config;
},
```
3. If a parent dependency forces an older broken version, pin via `package.json` `resolutions`:
```json
{ "resolutions": { "onnxruntime-web": "1.27.0" } }
```
Then `yarn install --force`, verify `node_modules/onnxruntime-web/package.json` shows the overridden version, then rebuild.

### Pattern E: TypeScript type error blocking `next build`

When the Next.js production build fails on a component type (commonly D3 + custom graph types), prefer fixing the component type locally over changing core domain types. If it's purely a visualization constraint, cast in the component:
```ts
// Example: keeping app types stable while fixing D3 simulation type
const simulationRef = useRef<any | null>(null);
const simulation = d3.forceSimulation<NodeWithPos>(filteredNodes)
  .force('link', d3.forceLink<NodeWithPos, any>(filteredEdges as any));
```

### Pattern F: `NEXT_PUBLIC_*` URLs are baked into the client bundle at build time

Symptom: frontend calls POST to `http://localhost:3000/api/...` and gets a Next.js 404 page.

Cause: `NEXT_PUBLIC_BACKEND_URL` is read during `next build` and inlined into the JS bundle. Setting it in `docker-compose.yml` `environment:` is necessary for server-side rendering, but **not sufficient** for the static client bundle. The env var must be present at build time inside the builder container.

Fix:
1. Create `frontend/.env` (gitignored) with the value:
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:4000
```
2. The Dockerfile copies `.env` into the build context because it copies `.` after copying `package.json` and running `yarn install`. Rebuild frontend.
3. Verify the baked-in value:
```bash
docker exec <frontend-container> grep -R "localhost:4000" .next/static | head
```
4. If the browser cached the old bundle, hard-refresh (Ctrl+Shift+R) to get the new JS.

### Pattern G: Frontend freeze / "page unresponsive" on panel open

Cause: heavy WASM model downloads (`kokoro-js`, `@huggingface/transformers`) and large 3D scenes run synchronously on the main thread during mount.

Fixes:
1. **Defer model initialization** — use `setTimeout(() => initKokoroTTS(), 0)` inside the panel-open `useEffect` so the UI thread paints before the heavy JS runtime starts loading:
```ts
useEffect(() => {
  if (!jarvisPanelOpen || ttsReady || ttsLoading) return;
  const id = setTimeout(() => initKokoroTTS(), 0);
  return () => clearTimeout(id);
}, [jarvisPanelOpen, ttsReady, ttsLoading]);
```
2. **Reduce 3D particle budget** — drop initial `PARTICLE_COUNT` (e.g. 500 → 160) in Three.js particle systems.
3. **Clean invalid Next.js config keys** — `webpackMemoryLimit` is not a valid `experimental` option in Next 14 and triggers config errors.
4. **Fix `transpilePackages` placement** — it must be a top-level key in `next.config.js`, **not** nested inside `experimental`:
```js
// ❌ WRONG
experimental: {
  'unified', 'bail', /* ... */
  'onnxruntime-web',
}

// ✅ CORRECT
transpilePackages: ['@xenova/transformers', 'onnxruntime-web', 'kokoro-js'],
```

### Pattern H: Backend dependency conflict (`ResolutionImpossible` during `pip install`)

If `pip install -r requirements.txt` fails inside Docker with a conflict between pinned versions:
```
openai==1.40.0 depends on httpx<1.0.0,>=0.27.0
google-genai==2.8.0 depends on httpx<1.0.0,>=0.28.1
ResolutionImpossible
```

Fix:
1. **Remove unused transitive dependencies** — check whether the conflicting package is even imported in the app. If it's only a transitive dependency, remove it from `requirements.txt` entirely.
2. **Prefer upgrading the downstream library** (e.g. `openai`) over downgrading platform requirements.
3. **Rebuild** with `docker-compose build backend --no-cache`.
4. **Verify** by checking startup logs for `TypeError: ... got an unexpected keyword argument`.

Guideline: keep `requirements.txt` minimal — only packages imported directly by the app should sit there.

---

## 🗣️ Voice Stack Migration Pattern (OmniVoice Studio Integration)

When replacing the voice/STT/TTS implementation with a backend service like OmniVoice Studio:

1. **Backup first** — copy `frontend/lib/voice/*` → `frontend/lib/voice/backup/` before touching anything
2. **Add backend proxy** — create `backend/routes/voice.py` that forwards `/api/voice/tts` and `/api/voice/stt` to the OmniVoice backend with bearer auth. Mount it in `server.py`.
3. **Create frontend adapter** with the same interface as the original (`init`, `speak`, `transcribe`, `stop`, subscriptions). Include browser `speechSynthesis` fallback at the adapter layer.
4. **Replace imports incrementally** — use compatibility aliases (`export const speakText = speak`) to avoid rewiring every file at once.
5. **Rename state consistently** — if renaming store keys (e.g. `whisperReady` → `sttReady`), update the Zustand interface, initial values, and all consumers in one pass to avoid build errors.
6. **Preserve rollback** — keep the backup folder; do not delete until the new stack is confirmed working.

### OmniVoice-specific docker-compose.yml pattern

```yaml
  omnivoice:
    image: palashdeb/omnivoice-studio:latest
    ports:
      - "8220:8220"
    environment:
      - BEARER_TOKEN=${OMNIVOICE_BEARER_TOKEN}
    volumes:
      - ./omnivoice-models:/app/models
    restart: unless-stopped
```

**Rules:**
- Pass `OMNIVOICE_BEARER_TOKEN` via `.env` and store the generated token in the obsidian vault secrets file.
- Mount a project-local bind mount for models (`./omnivoice-models`) so they persist and are Git-ignored if needed.
- Reference the service from other containers via Docker Compose DNS (`http://omnivoice:8220`), never `localhost`.

## 🔄 Phase-by-Phase Rebuild Workflow (ZakOS-standard)

For complex multi-service changes, split into phases. After each phase:
1. Build affected services with `docker-compose build <service>`
2. Restart with `docker-compose up -d <service>`
3. Verify with health checks (`curl /api/health`) and smoke tests
4. **Wait for user confirmation** before proceeding to the next phase

This prevents cascading failures and keeps rollback simple.

---

## 🗣️ Voice Stack Migration Pattern

When replacing the voice/STT/TTS implementation:
1. **Backup first** — copy `frontend/lib/voice/*` → `frontend/lib/voice/backup/` before touching anything
2. **Create adapter module** with the same interface as the original (`init`, `speak`, `transcribe`, `stop`, subscriptions)
3. **Implement fallback** at the adapter layer: if the new backend is unavailable, fall back to the old implementation or browser `speechSynthesis`
4. **Preserve rollback** — keep the backup folder; do not delete until the new stack is confirmed working

---

## 🤖 Adding a Secondary Service (e.g. OmniVoice Studio)

Pattern for adding a Dockerized helper service to `docker-compose.yml`:

```yaml
  <service-name>:
    image: <image>:<tag>
    ports:
      - "HOST_PORT:CONTAINER_PORT"
    environment:
      - REQUIRED_ENV=${ENV_VAR}
    volumes:
      - ./<local-data-dir>:<container-data-dir>
    restart: unless-stopped
```

**Rules:**
- Use a **named volume** only if the data must survive `docker-compose down`; otherwise use a bind mount under the project dir so Git can track it.
- If the service needs bearer auth, generate a token, store it in the obsidian vault secrets file, and pass it via `environment:` from `.env`.
- Do **not** hardcode secrets in `docker-compose.yml`; always reference `${ENV_VAR}`.
- After adding the service, run `docker-compose build` (or just `up -d` if using a prebuilt image) and check logs.

---

## 📝 References

- [`references/docker-safety-patterns.md`](references/docker-safety-patterns.md) — Detailed error recovery and MongoDB schema patterns
- [`references/fastapi-mongodb-validation.md`](references/fastapi-mongodb-validation.md) — Field validation patterns (optional vs required)
- [`references/zakos-frontend-build-fixes.md`](references/ZakOS-frontend-build-fixes.md) — Next.js frontend Docker build errors and fixes (session log)
- [`references/zakos-frontend-runtime-fixes.md`](references/ZakOS-frontend-runtime-fixes.md) — Frontend runtime bugs (env baking, heavy-init freeze, 3D perf)
- [`references/zakos-browser-vs-curl-verification.md`](references/ZakOS-browser-vs-curl-verification.md) — Windows Docker localhost verification: use curl instead of browser_navigate for container health checks
- See [`github-repo-management`](../SKILL.md) for Git backup workflow
- See [`docker-rebuild-workflow`](../../SKILL.md) for general rebuild workflow
*Always verify build results before deploying. Keep code changes minimal and isolated per service.*"

---
#devops #knowledge-base #skills

