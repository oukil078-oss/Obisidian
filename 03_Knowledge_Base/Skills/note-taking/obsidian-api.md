---
skill: "obsidian-api"
category: "note-taking"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\note-taking\obsidian-api\SKILL.md"
vault_path: "Skills/note-taking/obsidian-api.md"
tags: ["note-taking", "hermes-skill", "skill"]
trigger_keywords: ["obsidian", "local", "rest", "integration", "live", "vault", "intelligence", "vault", "listing", "note"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---
# obsidian api

---
name: obsidian-api
description: "obsidian Local REST API integration for live vault intelligence: vault listing, note reading, Tags."
version: 1.1.0
---

# obsidian API Skill

Use the obsidian Local REST API (`obsidian-local-rest-api` by Adam Coddington, v4.1.3) via Python `urllib.request`.

## Supporting docs

- API contract + Windows gotchas: `references/obsidian-api-contract.md`

## Why Python, not curl

1. Plugin installed and enabled in obsidian: **Local REST API with MCP**
2. HTTP server enabled in plugin settings
3. API key copied
4. Stored in vault secrets: `C:\Users\pc\Documents\Vs-Code\Mind-Galaxy\.obsidian\secrets\github-tokens.md`
   - obsidian REST API Key: `<your-key>`
Use the obsidian Local REST API (`obsidian-local-rest-api` by Adam Coddington, v4.1.3) via Python `urllib.request`.

## Supporting docs

- API contract + Windows gotchas: `references/obsidian-api-contract.md`

## Why Python, not curl

`curl.exe` on Windows fails to send `Authorization: Bearer …` correctly with this plugin/OS combo (401 even with the exact key). Use `urllib.request` in Python — verified working.

**Do NOT disable auth as a workaround.** The correct pattern is:
1. Keep HTTP server enabled in plugin settings
2. Keep the API key set
3. Use Python `urllib.request` with `Authorization: Bearer <key>` header
## Why Python, not curl

`curl.exe` on Windows fails to send `Authorization: Bearer <key>` correctly with this plugin/OS combo (401 even with the exact key). Use `urllib.request` in Python — verified working.

## Verified endpoints (v4.1.3)

### Server info (no auth required)
`GET http://127.0.0.1:27123/`

### List vault files
`GET http://127.0.0.1:27123/vault/`
Returns JSON: `{ "files": ["…"] }`

### Read a note (raw markdown)
`GET http://127.0.0.1:27123/vault/<path>`
- Path is vault-relative, percent-encode spaces
- Note: this is `/vault/<filename>` NOT `/vault/note/<filename>`
- Example: `/vault/WebDev%20Guidelines.md`
- Directories may return JSON file list
- Notes return raw markdown body (no JSON wrapper)

### Tags
`GET http://127.0.0.1:27123/tags/`
Returns JSON: `{ "tags": [ { "name": "...", "count": N }, … ] }`

### Pitfalls
- `/vault/note/<path>` → 404. Use `/vault/<path>` instead.
- `curl.exe -H "Authorization: Bearer ..."` → 401 on Windows. Use Python urllib.
- Backlinks/links endpoints require `Target-Type` header; for now parse `[[]]` manually from note content if needed.

## Python helper

```python
import urllib.request, json
from urllib.parse import quote

KEY = "<YOUR KEY HERE>"
BASE = "http://127.0.0.1:27123"

def obs_get(path):
    req = urllib.request.Request(BASE + path)
    req.add_header("Authorization", f"Bearer {KEY}")
    r = urllib.request.urlopen(req, timeout=10)
    return r.status, r.read().decode()

def obs_note(filename):
    return obs_get("/vault/" + quote(filename, safe=""))

def obs_list():
    code, body = obs_get("/vault/")
    return code, json.loads(body)
```

## Usage rules

1. Read the API key from the vault secrets file before making calls.
2. Always percent-encode file paths with spaces or non-ASCII.
3. Note reads return raw markdown; parse frontmatter yourself if needed.
4. For bulk operations, list first, then read individual notes.
5. For backlinks, rely on the bundled `obsidian` filesystem skill or parse `[[]]` links manually from note content.

---
#knowledge-base #note-taking #skills

