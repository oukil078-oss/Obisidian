---
skill: "vault-ops"
category: "note-taking"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\note-taking\vault-ops\SKILL.md"
vault_path: "Skills/note-taking/vault-ops.md"
tags: ["note-taking", "hermes-skill", "skill"]
trigger_keywords: ["obsidian", "vault", "conventions", "paths", "tagging", "note", "governance"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---

---
name: vault-ops
description: "Obsidian vault conventions, paths, tagging, and note governance."
---

# Vault Ops

## Paths
- Vault root: `C:\Users\pc\Documents\Vs-Code\Mind-Galaxy`
- Credentials file: `.obsidian/secrets/github-tokens.md`
- Default project clone dir: `C:\Users\pc\Documents\Vs-Code\Projects`

## Live API access (preferred when Obsidian is running)
- Plugin: **Local REST API with MCP** (Adam Coddington)
- Endpoint: `http://127.0.0.1:27123/`
- Auth: Bearer token in `Authorization` header
- **CRITICAL**: Use Python `urllib.request`, NOT `curl.exe` on Windows (curl fails auth with this plugin)
- Note read path: `/vault/<filename>` (NOT `/vault/note/<filename>`)
- Skill: `obsidian-api` — use it for all live vault reads/searches
- Prefer API reads over filesystem reads when Obsidian is running

## Governance
- Treat vault as a long-term second brain.
- Create/update notes only when they add real value.
- Link related notes; avoid duplicates.
- Keep notes organized and consistent.
- Use vault graph conventions: link projects to Profile, tag consistently (e.g., `#project`, `#ai`, `#docker`, `#voice`).
- Reference `.obsidian/templates/` when creating structured notes.
- Reference `.obsidian/templates/` when creating structured notes.
