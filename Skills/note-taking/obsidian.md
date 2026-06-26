---
skill: "obsidian"
category: "note-taking"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\note-taking\obsidian\SKILL.md"
vault_path: "Skills/note-taking/obsidian.md"
tags: ["note-taking", "hermes-skill", "skill"]
trigger_keywords: ["read", "search", "create", "edit", "notes", "obsidian", "vault"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---

---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
platforms: [linux, macos, windows]
---

# Obsidian Vault

Use this skill for filesystem-first Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

## Vault path

Use a known or resolved vault path before calling file tools.

### User's configured vault

**CRITICAL:** Always use `OBSIDIAN_VAULT_PATH` from environment first. For this user, it is:

```
C:\Users\pc\Documents\Vs-Code\Mind-Galaxy
```

This vault has a specialized graph-focused structure — DO NOT create notes in the wrong location! If you create a note in the fallback path (`~/Documents/Obsidian Vault`), delete it immediately and use the configured path.

### File operations workflow

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists. Once the path is known, switch back to file tools.

## Credential storage in vault

**CRITICAL:** This vault contains a centralized local credential store. Do NOT store API keys, tokens, or secrets in project `.env` files, code, or summary records.

### Credential file path

```
C:\Users\pc\Documents\Vs-Code\Mind-Galaxy\.obsidian\secrets\github-tokens.md
```

### Credential workflow

1. **Before asking for a new key:** check the credential file first to see if it already exists.
2. **Append new values into that file** under a clear section header for the service/project — do not create a new file.
3. **Redact values everywhere else:** never echo full keys back in chat, summaries, or logs.
4. **Single source of truth:** when a future task needs an API key, read it from this file instead of asking the user again.

### Project credential example

- `NIM_API_KEY` → append under `ZakOS / AgenticOS Credentials` in the secrets file.
- `OPENCLAW_PORT`, `HERMES_PORT`, `FREE_CLAUDE_PORT` → port configs are not secret, but keep other tokens out of `docker-compose.yml` when possible.

## When to use Obsidian for storage

**IMPORTANT:** This vault is the user's long-term assistant and project memory system ("second brain"). Treat vault work as building persistent, graph-connected knowledge. Use the graph-first workflow: create notes only when they add real value, link related notes so the knowledge graph stays useful, keep it organized and consistent, and avoid duplicates. Use consistent tags so graph clusters remain readable.

**Interview before acting:** For complex tasks, ask clarifying questions before starting. Do not guess important requirements. Ask about the goal, expected output, deadlines, constraints, tools or platforms, preferred style, success criteria, and anything else needed to do the job well. For simple tasks, proceed directly.

**Efficiency principles:**
- Reuse existing skills, patterns, notes, and workflows before inventing new ones.
- Prefer concise internal reasoning and concise output unless the task needs detail.
- Use the smallest effective context needed to answer well.
- Avoid repeating the same explanations, checks, or transformations across sessions.
- When a task repeats, convert the best working method into a reusable skill, template, or shortcut.
- Ask only the minimum clarifying questions needed for complex tasks.

## Read a note

Use `read_file` with the resolved absolute path to the note. Prefer this over `cat` because it provides line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Observation behavior: save what matters

After each meaningful interaction, decide whether anything should be saved.
- Save only useful, reusable, or decision-worthy information.
- Add new notes when: a new project starts, a new topic is introduced, a decision is made, a recurring preference appears, a useful pattern is discovered, or a task produces knowledge worth keeping.
- Update existing notes when new information belongs there. Avoid duplication.
- Keep notes small, well-structured, and searchable.

## Long-term assistant behavior

For complex tasks, act like an interviewer first.
- Ask clarifying questions about: goal, expected output, deadlines, constraints, tools/platforms, preferred style, success criteria.
- Do not guess important requirements.
- For simple tasks, proceed directly without excessive questioning.

## Efficiency principles

- Reuse existing skills, patterns, notes, and workflows before inventing new ones.
- Prefer concise internal reasoning and concise output unless the task needs detail.
- Use the smallest effective context needed to answer well.
- Avoid repeating the same explanations, checks, or transformations across sessions.
- When a task repeats, convert the best working method into a reusable skill, template, or shortcut.
- Ask only the minimum clarifying questions needed for complex tasks.

## Vault-credentials-first, project-env sync rule

For this user:

- The secrets file is the source of truth:
  - `C:\Users\pc\Documents\Vs-Code\Mind-Galaxy\.obsidian\secrets\github-tokens.md`
- When asked to sync credentials into project `.env` files:
  1. Write the complete intended file in one call.
  2. Verify immediately with `cat .env` (use `terminal` because secret files may be blocked by `read_file`).
  3. Redact actual credentials in chat output.
  4. Continue treating the secrets file as the durable source of truth.

## Credential collection workflow

When collecting API keys or tokens from the user:
1. Ask for one variable at a time in the order the user specifies.
2. Before asking, check the credential file for existing values.
3. Append new values to the centralized credential file under a clear section header.
4. Never store credentials in project `.env` files, code, or chat summaries.
5. Always read from the credential file when a future task needs an API key.
6. Redact full values in chat output; use prefixes like `ghp_bo...` or `nvapi-...`.

## Vault-specific reference

For this user's vault structure, tags system, and graph organization rules, see [`references/graph-organization.md`](references/graph-organization.md).