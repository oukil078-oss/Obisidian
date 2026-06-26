---
skill: "github-repo-management"
category: "github"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\github\github-repo-management\SKILL.md"
vault_path: "Skills/github/github-repo-management.md"
tags: ["github", "hermes-skill", "skill", "GitHub", "Repositories", "Git", "Releases", "Secrets", "Configuration"]
trigger_keywords: ["clone", "create", "fork", "repos", "manage", "remotes", "releases"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---

---
name: github-repo-management
description: "Clone/create/fork repos; manage remotes, releases."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Repositories, Git, Releases, Secrets, Configuration]
    related_skills: [github-auth, github-pr-workflow, github-issues]
---

# GitHub Repository Management

Create, clone, fork, configure, and manage GitHub repositories. Each section shows `gh` first, then the `git` + `curl` fallback.

## Prerequisites

- Authenticated with GitHub (see `github-auth` skill)

### Setup

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  if [ -z "$GITHUB_TOKEN" ]; then
    if _hermes_env="${HERMES_HOME:-$HOME/.hermes}/.env"; [ -f "$_hermes_env" ] && grep -q "^GITHUB_TOKEN=" "$_hermes_env"; then
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" "$_hermes_env" | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    fi
  fi
fi

# Get your GitHub username (needed for several operations)
if [ "$AUTH" = "gh" ]; then
  GH_USER=$(gh api user --jq '.login')
else
  GH_USER=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | python3 -c "import sys,json; print(json.load(sys.stdin)['login'])")
fi
```

If you're inside a repo already:

```bash
REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

---

## 1. Cloning Repositories

Cloning is pure `git` — works identically either way:

```bash
# Clone via HTTPS (works with credential helper or token-embedded URL)
git clone https://github.com/owner/repo-name.git

# Clone into a specific directory
git clone https://github.com/owner/repo-name.git ./my-local-dir

# Shallow clone (faster for large repos)
git clone --depth 1 https://github.com/owner/repo-name.git

# Clone a specific branch
git clone --branch develop https://github.com/owner/repo-name.git

# Clone via SSH (if SSH is configured)
git clone git@github.com:owner/repo-name.git
```

**With gh (shorthand):**

```bash
gh repo clone owner/repo-name
gh repo clone owner/repo-name -- --depth 1
```

### Clone Directory Convention

**Projects MUST be cloned into their own dedicated subfolder within a main projects directory:**

```bash
# ✅ CORRECT: Create project folder, then clone into it
mkdir -p "C:/Users/pc/Documents/Vs-Code/Projects"
git clone https://github.com/oukil078-oss/DawaDzLinkk.git DawaDzLinkk

# ❌ WRONG: Don't clone directly to root!
git clone https://github.com/owner/repo.git C:/Users/pc/Documents/Vs-Code/Projects/repo  # BAD!
```

**Pattern:** `PROJECTS_DIR/REPO_NAME/` (not `PROJECTS_DIR/repo-name`)

This keeps each project organized with its own folder rather than cluttering the projects root.

### Post-Clone Cleanup

After cloning, remove unnecessary files that come from Bolt AI or initial setup:

```bash
cd "C:/Users/pc/Documents/Vs-Code/Projects/DawaDzLinkk"

# Remove unnecessary documentation and guides
rm -f README.md AI_PROMPT_FULL_REBUILD.md BACKEND_SETUP.md \
      COPY_PASTE_PROMPT.txt FIX_LOGIN_NOW.md QUICK_FIX_LOGIN.md \
      SETUP_INSTRUCTIONS.md src/Attributions.md src/guidelines/Guidelines.md

# Remove docs folder with deliverable guides  
rm -rf ./docs/

# Remove .gitignore if it's the default template one (optional)
rm -f ./.gitignore

# Remove generated/test directories (keep tests themselves)
rm -rf test_reports/ uploads/ .bolt/

# Remove unnecessary files from public/ and memory/
rm -f ./public/robots.txt ./memory/PRD.md 2>/dev/null || true
```

**Keep:**
- ✅ Source code (`backend/`, `frontend/`, `src/`)
- ✅ Config files (`docker-compose.yml`, `nginx.conf`, etc.)
- ✅ Dependency files (`requirements.txt`, `package.json`, `vite.config.ts`)
- ✅ Test source files (in their test directories)

**Remove:**
- ❌ Prompt/copy-paste `.txt` files
- ❌ Setup/quick-fix/guide `.md` documents
- ❌ Generated deliverable guides in `docs/`
- ❌ `.bolt/` project metadata folder
- ❌ Empty `uploads/` and `test_reports/` folders
- ❌ Template `.gitignore`, `.env*` files

**Note:** Always verify before bulk delete by listing MD/TXT files first.

## 2. Creating Repositories

### Obsidian Vault Push Workflow

**Scenario:** pushing an existing local Obsidian vault to a GitHub repo.

```bash
# 1. Init repo locally (if not already)
cd <vault-path>
git init

# 2. Stage everything
git add -A

# 3. First commit (if this is the first push)
git commit -m "chore: add Obsidian vault"

# 4. Add remote using token auth when `gh` is unavailable
git remote add origin 'https://<token>@github.com/owner/repo.git'
git branch -M main

# 5. If remote already has commits, rebase instead of force-pushing
git pull --rebase origin main
git push -u origin main
```

**Pitfall:** If the remote already contains work, `git push` will be rejected. ALWAYS `git pull --rebase origin main` first, then push. Force-pushing to a shared remote can destroy other contributors' work.

**Pitfall — Brain repo env value:** When configuring `GITHUB_BRAIN_REPO` for Obsidian brain sync, use the **full HTTPS git URL**, not a bare `owner/repo` handle. Example:
```env
GITHUB_BRAIN_REPO=https://github.com/oukil078-oss/Obisidian.git
```
A bare handle causes `git clone` to fail and the backend silently reports `brain: false`.

### With gh:

```bash
# Create a public repo and clone it
gh repo create my-new-project --public --clone

# Private, with description and license
gh repo create my-new-project --private --description "A useful tool" --license MIT --clone

# Under an organization
gh repo create my-org/my-new-project --public --clone

# From existing local directory
cd /path/to/existing/project
gh repo create my-project --source . --public --push
```

**With git + curl:**

```bash
# Create the remote repo via API
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos \
  -d '{
    "name": "my-new-project",
    "description": "A useful tool",
    "private": false,
    "auto_init": true,
    "license_template": "mit"
  }'

# Clone it
git clone https://github.com/$GH_USER/my-new-project.git
cd my-new-project

# -- OR -- push an existing local directory to the new repo
cd /path/to/existing/project
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/$GH_USER/my-new-project.git
git push -u origin main
```

To create under an organization:

```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/orgs/my-org/repos \
  -d '{"name": "my-new-project", "private": false}'
```

### From a Template

**With gh:**

```bash
gh repo create my-new-app --template owner/template-repo --public --clone
```

**With curl:**

```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/template-repo/generate \
  -d '{"owner": "'"$GH_USER"'", "name": "my-new-app", "private": false}'
```

## 3. Forking Repositories

**With gh:**

```bash
gh repo fork owner/repo-name --clone
```

**With git + curl:**

```bash
# Create the fork via API
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo-name/forks

# Wait a moment for GitHub to create it, then clone
sleep 3
git clone https://github.com/$GH_USER/repo-name.git
cd repo-name

# Add the original repo as "upstream" remote
git remote add upstream https://github.com/owner/repo-name.git
```

### Keeping a Fork in Sync

```bash
# Pure git — works everywhere
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

**With gh (shortcut):**

```bash
gh repo sync $GH_USER/repo-name
```

## 4. Repository Information

**With gh:**

```bash
gh repo view owner/repo-name
gh repo list --limit 20
gh search repos "machine learning" --language python --sort stars
```

**With curl:**

```bash
# View repo details
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO \
  | python3 -c "
import sys, json
r = json.load(sys.stdin)
print(f\"Name: {r['full_name']}\")
print(f\"Description: {r['description']}\")
print(f\"Stars: {r['stargazers_count']}  Forks: {r['forks_count']}\")
print(f\"Default branch: {r['default_branch']}\")
print(f\"Language: {r['language']}\")"

# List your repos
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/user/repos?per_page=20&sort=updated" \
  | python3 -c "
import sys, json
for r in json.load(sys.stdin):
    vis = 'private' if r['private'] else 'public'
    print(f\"  {r['full_name']:40}  {vis:8}  {r.get('language', ''):10}  ★{r['stargazers_count']}\")"

# Search repos
curl -s \
  "https://api.github.com/search/repositories?q=machine+learning+language:python&sort=stars&per_page=10" \
  | python3 -c "
import sys, json
for r in json.load(sys.stdin)['items']:
    print(f\"  {r['full_name']:40}  ★{r['stargazers_count']:6}  {r['description'][:60] if r['description'] else ''}\")"
```

## 5. Repository Settings

**With gh:**

```bash
gh repo edit --description "Updated description" --visibility public
gh repo edit --enable-wiki=false --enable-issues=true
gh repo edit --default-branch main
gh repo edit --add-topic "machine-learning,python"
gh repo edit --enable-auto-merge
```

**With curl:**

```bash
curl -s -X PATCH \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO \
  -d '{
    "description": "Updated description",
    "has_wiki": false,
    "has_issues": true,
    "allow_auto_merge": true
  }'

# Update topics
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.mercy-preview+json" \
  https://api.github.com/repos/$OWNER/$REPO/topics \
  -d '{"names": ["machine-learning", "python", "automation"]}'
```

## 6. Branch Protection

```bash
# View current protection
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/branches/main/protection

# Set up branch protection
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/branches/main/protection \
  -d '{
    "required_status_checks": {
      "strict": true,
      "contexts": ["ci/test", "ci/lint"]
    },
    "enforce_admins": false,
    "required_pull_request_reviews": {
      "required_approving_review_count": 1
    },
    "restrictions": null
  }'
```

## 7. Secrets Management (GitHub Actions)

**With gh:**

```bash
gh secret set API_KEY --body "your-secret-value"
gh secret set SSH_KEY < ~/.ssh/id_rsa
gh secret list
gh secret delete API_KEY
```

**With curl:**

Secrets require encryption with the repo's public key — more involved via API:

```bash
# Get the repo's public key for encrypting secrets
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/secrets/public-key

# Encrypt and set (requires Python with PyNaCl)
python3 -c "
from base64 import b64encode
from nacl import encoding, public
import json, sys

# Get the public key
key_id = '<key_id_from_above>'
public_key = '<base64_key_from_above>'

# Encrypt
sealed = public.SealedBox(
    public.PublicKey(public_key.encode('utf-8'), encoding.Base64Encoder)
).encrypt('your-secret-value'.encode('utf-8'))
print(json.dumps({
    'encrypted_value': b64encode(sealed).decode('utf-8'),
    'key_id': key_id
}))"

# Then PUT the encrypted secret
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/secrets/API_KEY \
  -d '<output from python script above>'

# List secrets (names only, values hidden)
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/secrets \
  | python3 -c "
import sys, json
for s in json.load(sys.stdin)['secrets']:
    print(f\"  {s['name']:30}  updated: {s['updated_at']}\")"
```

Note: For secrets, `gh secret set` is dramatically simpler. If setting secrets is needed and `gh` isn't available, recommend installing it for just that operation.

## 8. Releases

**With gh:**

```bash
gh release create v1.0.0 --title "v1.0.0" --generate-notes
gh release create v2.0.0-rc1 --draft --prerelease --generate-notes
gh release create v1.0.0 ./dist/binary --title "v1.0.0" --notes "Release notes"
gh release list
gh release download v1.0.0 --dir ./downloads
```

**With curl:**

```bash
# Create a release
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/releases \
  -d '{
    "tag_name": "v1.0.0",
    "name": "v1.0.0",
    "body": "## Changelog\n- Feature A\n- Bug fix B",
    "draft": false,
    "prerelease": false,
    "generate_release_notes": true
  }'

# List releases
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/releases \
  | python3 -c "
import sys, json
for r in json.load(sys.stdin):
    tag = r.get('tag_name', 'no tag')
    print(f\"  {tag:15}  {r['name']:30}  {'draft' if r['draft'] else 'published'}\")"

# Upload a release asset (binary file)
RELEASE_ID=<id_from_create_response>
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/octet-stream" \
  "https://uploads.github.com/repos/$OWNER/$REPO/releases/$RELEASE_ID/assets?name=binary-amd64" \
  --data-binary @./dist/binary-amd64
```

## 9. GitHub Actions Workflows

**With gh:**

```bash
gh workflow list
gh run list --limit 10
gh run view <RUN_ID>
gh run view <RUN_ID> --log-failed
gh run rerun <RUN_ID>
gh run rerun <RUN_ID> --failed
gh workflow run ci.yml --ref main
gh workflow run deploy.yml -f environment=staging
```

**With curl:**

```bash
# List workflows
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/workflows \
  | python3 -c "
import sys, json
for w in json.load(sys.stdin)['workflows']:
    print(f\"  {w['id']:10}  {w['name']:30}  {w['state']}\")"

# List recent runs
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/actions/runs?per_page=10" \
  | python3 -c "
import sys, json
for r in json.load(sys.stdin)['workflow_runs']:
    print(f\"  Run {r['id']}  {r['name']:30}  {r['conclusion'] or r['status']}\")"

# Download failed run logs
RUN_ID=<run_id>
curl -s -L \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/logs \
  -o /tmp/ci-logs.zip
cd /tmp && unzip -o ci-logs.zip -d ci-logs

# Re-run a failed workflow
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/rerun

# Re-run only failed jobs
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/rerun-failed-jobs

# Trigger a workflow manually (workflow_dispatch)
WORKFLOW_ID=<workflow_id_or_filename>
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/workflows/$WORKFLOW_ID/dispatches \
  -d '{"ref": "main", "inputs": {"environment": "staging"}}'
```

## 10. Gists

**With gh:**

```bash
gh gist create script.py --public --desc "Useful script"
gh gist list
```

**With curl:**

```bash
# Create a gist
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/gists \
  -d '{
    "description": "Useful script",
    "public": true,
    "files": {
      "script.py": {"content": "print(\"hello\")"}
    }
  }'

# List your gists
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/gists \
  | python3 -c "
import sys, json
for g in json.load(sys.stdin):
    files = ', '.join(g['files'].keys())
    print(f\"  {g['id']}  {g['description'] or '(no desc)':40}  {files}\")"
```

## Quick Reference Table

| Action | gh | git + curl |
|--------|-----|-----------|
| Clone | `gh repo clone o/r` | `git clone https://github.com/o/r.git` |
| Create repo | `gh repo create name --public` | `curl POST /user/repos` |
| Fork | `gh repo fork o/r --clone` | `curl POST /repos/o/r/forks` + `git clone` |
| Repo info | `gh repo view o/r` | `curl GET /repos/o/r` |
| Edit settings | `gh repo edit --...` | `curl PATCH /repos/o/r` |
| Create release | `gh release create v1.0` | `curl POST /repos/o/r/releases` |
| List workflows | `gh workflow list` | `curl GET /repos/o/r/actions/workflows` |
| Rerun CI | `gh run rerun ID` | `curl POST /repos/o/r/actions/runs/ID/rerun` |
| Set secret | `gh secret set KEY` | `curl PUT /repos/o/r/actions/secrets/KEY` (+ encryption) |

---

## Backend API Development Patterns (FastAPI + MongoDB)

Handle optional fields by storing empty strings, not null. Use conditional duplicate checks and remove unique indexes when making fields truly optional.

**Schema change rebuild pattern:** After modifying schema in Docker containers:
```bash
docker rm -f dawadzlink-backend && \
docker exec dawadzlink-mongodb mongosh --eval "db.dropDatabase(); init_db();" && \
docker-compose up -d
```

**See [`references/fastapi-mongodb-validation.md`](references/fastapi-mongodb-validation.md) for complete pattern library.**

---

## Backend API Development Patterns

FastAPI + MongoDB integration: schema design, optional fields, duplicate validation.

### MongoDB Schema Design with Optional Fields

When adding optional fields (like `registry_number`, `email`, `phone`) to existing MongoDB collections in FastAPI apps:

#### ✅ **CORRECT Pattern:** Handle optional vs required separately

```python
# ❌ WRONG: Treats optional field as required during validation
@router.post("/api/auth/register/pharmacy")
async def register_pharmacy(data: PharmacyRegistration):
    # User without registry_number fails here!
    user = await db.documents.create_one({
        "email": data.email,
        "registry_number": data.registry_number  # Will store None or raise error
    })

# ✅ CORRECT: Validate optional fields separately
@router.post("/api/auth/register/pharmacy")
async def register_pharmacy(data: PharmacyRegistration):
    # Check if optional field is provided before duplicate validation
    registry_number = data.registry_number.strip() if data.registry_number else ""
    
    # Only validate uniqueness if registry_number is non-empty
    if registry_number:
        existing = await db.documents.find_one(
            {"registry_number": registry_number}
        )
        if existing and not existing.get("is_deleted"):
            raise HTTPException(status_code=409, detail="Register number already taken")
    
    # Now create document with empty string for missing optional fields
    user = await db.documents.create_one({
        "email": data.email,
        "registry_number": registry_number if registry_number else ""  # Empty string, not None
    })
```

#### Key Rules:
1. **Empty string (`""`) != `None`** for MongoDB storage — always store `""` for optional fields
2. **Conditional duplicate checks** — only validate uniqueness if the optional field is provided and non-empty
3. **Remove unique indexes** when making a field truly optional (or use compound indexes)

#### Example: Removing Unique Indexes for Optional Fields

```bash
# Remove unique index on registry_number to allow multiple users without it
docker exec dawadzlink-mongodb mongosh --eval "
db.users.dropIndex('registry_number_1');
db.suppliers.dropIndex('registry_number_1');"
```

### FastAPI + MongoDB Rebuild Pattern

**After changing database schema in production:**

```bash
# 1. Remove existing containers (images are cached, no need to rebuild immediately)
docker rm -f dawadzlink-backend dawadzlink-mongodb

# 2. Re-initialize database and collections
docker exec dawadzlink-mongodb mongosh <<EOF
use dawadzlink_db;
db.dropDatabase();
init_db();  # Re-creates indexes with new schema
EOF

# 3. Restart containers
docker-compose up -d
```

**Why?** MongoDB unique indexes must be recreated after schema changes.

### API Response Format Convention

For REST APIs in this project:

```python
# Registration endpoints return registration token + user partial data
@router.post("/api/auth/register/pharmacy", response_model=RegistrationResponse)
async def register_pharmacy(data: PharmacyRegistration):
    await db.documents.create_one({
        "email": data.email,
        "role": "pharmacy"
    })
    
    # Generate JWT registration token
    access_token = create_access_token(
        data={"email": data.email, "type": "pharmacy"}
    )
    
    # Return both for client to use immediately
    return {
        "message": "Registration successful",
        "access_token": access_token,
        "user": {
            "id": str(user_id),  # Don't expose sensitive fields
            "email": data.email,
            "full_name": data.full_name
        }
    }
```

### Reference: API Validation Patterns

See [`references/fastapi-mongodb-validation.md`](references/fastapi-mongodb-validation.md) for complete pattern library.

---

## Troubleshooting Quick Tips

### Container won't start after code changes?

```bash
# Check for missing dependencies or schema issues
docker logs dawadzlink-backend 2>&1 | grep -i error

# If "document not found" errors, reinitialize database
docker exec dawadzlink-mongodb mongosh --eval "db.dropDatabase(); init_db();"
```

### MongoDB connection refused?

```bash
# Check if mongodb container is running
docker ps | grep mongodb

# Restart entire stack
docker-compose down && docker-compose up -d
```
