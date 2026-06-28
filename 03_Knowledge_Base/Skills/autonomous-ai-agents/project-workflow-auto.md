---
skill: "project-workflow-auto"
category: "autonomous-ai-agents"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\autonomous-ai-agents\project-workflow-auto\SKILL.md"
vault_path: "Skills/autonomous-ai-agents/project-workflow-auto.md"
tags: ["autonomous-ai-agents", "hermes-skill", "skill"]
trigger_keywords: ["automatic", "project", "workflow", "obsidian", "graphify", "vault", "notes", "project", "work", "existing"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---
# project workflow auto

---
name: project-workflow-auto
description: "Automatic project workflow: use obsidian API + Graphify + vault notes for all project work, new or existing."
---

# Project Workflow — Auto-Use Rules

For **every** project (new or existing, including ZakOS):

1. **Vault note first**
   - Ensure a vault note exists at `Projects/<Name>/<Name>.md`
   - Tag it: `#project #ai` (plus domain Tags)
   - Link it to `Profile.md` and `WebDev Guidelines`

2. **obsidian API (live) — ALWAYS prefer over filesystem reads**
   - Use `obsidian-api` skill for all vault reads/searches
   - Do NOT rely solely on filesystem reads when the API is available
   - Auto-verify note structure, Tags, frontmatter via API before editing
   - Automatically add new data to vault via API as it emerges

3. **Graphify (architecture radar) — ALWAYS keep updated**
   - Run `graphify update . --no-cluster` after any significant code change
   - Run `graphify cluster-only .` + `graphify label .` before major refactors
   - Query `graphify query "..."` when architectural context is needed
   - Automatically add new data to `graphify-out/` as the codebase evolves
   - Keep `graphify-out/` in `.gitignore`

4. **Doctrine sync**
   - Any new design rule → update `WebDev Guidelines` vault note + `webdev-guidelines` skill
   - Any new project preference → vault note + skill, memory pointer only

5. **ZakOS build cadence**
   - **Phase confirmations required:** After completing a backend or frontend phase, stop and report verification results before starting the next phase. Do not proceed to the next tab/section automatically.
   - **Rebuild-and-confirm loop:** build → restart services → health-check endpoints → report results → wait for user confirmation → proceed.
   - If a phase fails, fix it in-place and re-verify before claiming completion.

6. **Memory rule**
   - Never store verbose project detail in memory
   - Memory = pointer to skill/vault note only

---
#autonomous-ai-agents #knowledge-base #skills

