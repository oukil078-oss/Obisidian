---
skill: "graphify-usage"
category: "software-development"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\software-development\graphify-usage\SKILL.md"
vault_path: "Skills/software-development/graphify-usage.md"
tags: ["software-development", "hermes-skill", "skill"]
trigger_keywords: ["turn", "codebase", "docs", "folder", "into", "queryable", "knowledge", "graph", "when", "user"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---
# graphify usage

---
name: graphify-usage
description: "Turn a codebase or docs folder into a queryable knowledge graph. Use when the user asks for architecture mapping, codebase understanding, structural analysis, or 'graphify'."
triggers:
  - graphify
  - knowledge graph
  - architecture map
  - codebase structure
  - module dependency graph
  - god nodes
---

# Graphify Usage

Turn a codebase or docs folder into a queryable knowledge graph.

## Quick start
```bash
uv tool install graphifyy
cd /path/to/project
graphify update . --no-cluster
graphify query "core architecture" --budget 500
```

## Verified commands
See `references/verified-commands.md` for tested commands, Windows notes, and output descriptions from a live ZakOS trial (703 nodes, 976 edges, 52 communities).

## What it produces

```
graphify-out/
├── graph.html       # Interactive D3 graph
├── graph.json       # Full queryable graph
├── GRAPH_REPORT.md  # Human-readable insights
└── manifest.json    # Corpus stats
```

## Install

```bash
uv tool install graphifyy
# or
pipx install graphifyy
```

Verify:
```bash
graphify --version
```

## Core workflow

### 1. Quick structural scan (no LLM needed)
```bash
cd /path/to/project
graphify update . --no-cluster
```
This rebuilds `graph.json` with AST-only extraction. Fast, free, no API key.

### 2. Full clustering + naming
```bash
graphify cluster-only .
graphify label .
```
Without an LLM key, communities stay as `Community N`. With a key (`GOOGLE_API_KEY`, `ANTHIMIC_API_KEY`, etc.), `label .` names them.

### 3. Query the graph
```bash
graphify query "Where is auth wired?"
graphify explain GoogleService
graphify path "Frontend" "Backend"
graphify affected SomeNode --relation calls --depth 2
```

### 4. View the report
Read `graphify-out/GRAPH_REPORT.md`. It contains:
- **God nodes** — most-connected core abstractions
- **Surprising connections** — cross-module links ranked by unexpectedness
- **Communities** — clustered modules with cohesion scores
- **Knowledge gaps** — isolated nodes (≤1 connection)
- **Suggested questions** — high-value queries the graph can answer

## Flags and options

| Flag | Purpose |
|------|---------|
| `--no-cluster` | Skip community detection; raw extraction only |
| `--no-viz` | Skip `graph.html` generation (large graphs) |
| `--force` | Overwrite even if rebuild has fewer nodes (after refactors) |
| `--backend <name>` | LLM for community naming: `gemini`, `claude`, `openai`, `deepseek`, `kimi`, `ollama` |
| `--model <name>` | Specific model for the backend |
| `--json` | Machine-readable output (for scripting) |

## Windows notes

- Run from Git Bash / MSYS2 shell for best compatibility with paths.
- Use `--no-cluster` first to avoid needing an LLM key.
- Graphify auto-detects file types via tree-sitter; no extra config needed.

## Integration with Hermes

- Store graph outputs in `Projects/<name>/graphify-out/` in the vault.
- Re-run `graphify update .` after significant refactors.
- Use `graphify query` from the project directory to explore architecture.

## Trial insight (ZakOS, 2026-06-24)

- **703 nodes · 976 edges · 52 communities** extracted from 86 code + 7 docs.
- **God nodes**: `GoogleService`, `useAppStore`, `compilerOptions`, `ZakOS PRD`, `BrainService`, `_load_token()`, `TestCoreAPIs`
- **Surprising connections**: `obsidian_service.py` ↔ `server.js`, `HomePage` ↔ `useAppStore`
- **Knowledge gaps**: 226 isolated nodes flagged
- **Core value**: surfaces architectural links missed by linear file reading. Best used as a periodic deep-dive, not a daily driver.

---
#knowledge-base #skills #software-development

