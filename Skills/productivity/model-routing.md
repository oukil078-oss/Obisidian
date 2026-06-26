---
skill: "model-routing"
category: "productivity"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\productivity\model-routing\SKILL.md"
vault_path: "Skills/productivity/model-routing.md"
tags: ["productivity", "hermes-skill", "skill"]
trigger_keywords: ["task-based", "model", "routing", "fallback", "chains", "provider", "config", "hermes", "agent"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---

---
name: model-routing
description: "Task-based model routing, fallback chains, and provider config for Hermes Agent."
---

# Model Routing

## User's preferred free-cloud routing

Configure Hermes so the right model handles each task type, with auto-failover and a stable last resort.

### Task routing

| Task type | Model / provider | Notes |
|-----------|-----------------|-------|
| Main Telegram chat + coding | Groq: `llama-3.3-70b-versatile` | 320 tok/s, 30 RPM, 1K/day |
| Image scanning / vision | Google Gemini 2.5 Flash | Native multimodal, 1.5K/day |
| Auto fallback pool | OpenRouter `openrouter/free` router | Picks best available free model |
| Last resort / steady hand | StepFun Step 3.7 Flash | Known stable fallback, no quota risk |

### Config shape

```yaml
model: groq/llama-3.3-70b-versatile  # or configured via `hermes model`

auxiliary:
  vision: google/gemini-2.5-flash

fallback_providers:
  - provider: openrouter
    model: openrouter/free
  - provider: stepfun
    model: stepfun/step-3.7-flash:free
```

### Setup notes

- Groq is not in Hermes' native provider list — set it up as **Custom endpoint** via `hermes model` → custom → `https://api.groq.com/openai/v1` → `llama-3.3-70b-versatile` → Chat Completions mode.
- Gemini for vision requires its own API key (`GOOGLE_API_KEY` or `GEMINI_API_KEY`) and the custom endpoint `https://generativelanguage.googleapis.com/v1beta/openai`.
- OpenRouter free router needs `OPENROUTER_API_KEY` (no credits required for `:free` models).
- StepFun already works for this session (`STEPFUN_API_KEY` already set).

### Switching / monitoring

```bash
hermes model            # interactive primary model switcher
hermes fallback list    # view current fallback chain
hermes fallback add ... # add fallback entries
hermes fallback rm ...  # remove entries
```

Track usage at provider dashboards (OpenRouter activity, Groq console, Google AI Studio).  
When Groq 1K/day fills, Hermes auto-falls back to OpenRouter free router, then StepFun.

## Auto-failover behavior

- Hermes switches on 429/500/401 mid-session with **zero context loss**.
- `hermes fallback` manages the ordered chain interactively.
- Each entry needs `provider` + `model`. Custom endpoints also accept `base_url` and `key_env`.
