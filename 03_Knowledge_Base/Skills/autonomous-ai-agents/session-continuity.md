---
skill: "session-continuity"
category: "autonomous-ai-agents"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\autonomous-ai-agents\session-continuity\SKILL.md"
vault_path: "Skills/autonomous-ai-agents/session-continuity.md"
tags: ["autonomous-ai-agents", "hermes-skill", "skill"]
trigger_keywords: ["structure", "long-running", "agent", "state", "across", "sessions", "memory", "consolidation", "packaging", "vault"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---
# session continuity

---
name: session-continuity
description: "How to structure long-running agent state across sessions: memory consolidation, skill packaging, vault note governance."
triggers:
  - skill update
  - memory full
  - vault note
  - persistent doctrine
  - long-running project
---

# Session Continuity

How to structure long-running agent state across sessions.

## Memory consolidation rule (CRITICAL)

Never store verbose detail in memory. Memory has a hard char budget (~2,200 chars). The only durable pattern:

1. **New doctrine/rule/workflow** → create/update a **skill** + **vault note**
2. **Memory entry** → replace with a **short pointer** to the skill/vault note

Format example:
```
ZakOS continuity rules → skill zakos-context + vault Projects/ZakOS/ZakOS.md
```

When memory is near full:
- Merge overlapping entries (e.g., combine ports + branding into one skill)
- Remove stale entries
- Never add verbose text to memory

This is not optional. The user will check.

## The Three-Layer Rule

| Layer | Purpose | Budget | Lifetime |
|-------|---------|--------|----------|
| **Memory** | Activation cues and cross-references only | 2,200 chars per target | Session-to-session |
| **Skills** | Operational rules, procedures, values, triggers | Unlimited | Permanent |
| **Vault notes** | Long-form doctrine, session history, detailed specs | Unlimited | Permanent |

## When to leave a pointer vs. full detail

- **Memory**: always a pointer. Typed like `Topic → skill <name> + vault <note path>`.
- **Skill SKILL.md**: class-level rules, triggers, step sequences, pitfalls. Not one-off narratives.
- **Skill references/**: session-specific notes, transcripts, condensed research, code samples, configs.
- **Vault**: full doctrine, design systems, project history, session summaries with real value.

## Consolidation protocol

When memory is approaching limit or after a session with significant new doctrine:
1. **Inventory** all memory entries.
2. **Read** associated skills and vault notes.
3. **Create** missing umbrella skills for novel topics.
4. **Write** missing vault notes where doctrine needs long-form storage.
5. **Replace** verbose memory entries with lean pointers.
6. **Verify** memory usage drops below ~50%.

## Reference files by type

- `references/<topic>.md` — session detail, error transcripts, research extracts, domain notes
- `templates/<name>.<ext>` — starter files to copy and modify
- `scripts/<name>.<ext>` — deterministic re-runnable actions (verify, probe, fixture)

## Overlap handling

If two skills cover overlapping territory, consolidating them is fine — but it is not required to wait. The background curator handles bulk consolidation. Local patches can proceed freely.

---
#autonomous-ai-agents #knowledge-base #skills

