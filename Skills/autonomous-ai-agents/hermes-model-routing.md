---
skill: "hermes-model-routing"
category: "autonomous-ai-agents"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\autonomous-ai-agents\hermes-model-routing\SKILL.md"
vault_path: "Skills/autonomous-ai-agents/hermes-model-routing.md"
tags: ["autonomous-ai-agents", "hermes-skill", "skill"]
trigger_keywords: ["configure", "hermes", "model", "backends", "auxiliary", "task", "routing", "fallback", "provider", "chains"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---

---
name: hermes-model-routing
description: "Configure Hermes model backends, auxiliary task routing, and fallback provider chains for multi-provider setups."
---

# Hermes Model Routing

Configure primary models, auxiliary task models, and fallback chains in Hermes.

## Primary model setup

Use the interactive picker:
```bash
hermes model
```

For custom endpoints (e.g., Groq, self-hosted):
1. Select provider by number (e.g., `29` for `custom`, or `34` for manual URL)
2. Provide `base_url` (OpenAI-compatible endpoint, no trailing slash)
3. Provide API key when prompted
4. Select or type the model slug
5. Confirm display name

### Groq primary model example

```bash
hermes model
# 29 (custom)
# Base URL: https://api.groq.com/openai/v1
# API: <groq-key>
# Model: llama-3.3-70b-versatile
# Name: Groq-Hermes
```

## Auxiliary models (vision, compression, MCP reasoning, etc.)

Route specific side tasks to different providers/models:
```bash
hermes fallback
# 36 (Configure auxiliary models...)
# 1 (Vision) → Custom endpoint → base URL + key + model slug
```

### Google Gemini 2.5 Flash for vision

```
Base URL: https://generativelanguage.googleapis.com/v1beta/openai
Model: gemini-2.5-flash
```

Notes:
- This is an API base URL, not a webpage. A 404 in a browser is expected.
- Use OpenAI-compatible mode (`/chat/completions`), not Anthropic mode.

## Fallback provider chain

Hermes auto-switches to fallbacks on 429/500/401 with zero context loss.

### Setup (interactive — no CLI arguments)

```bash
hermes fallback add
# Pick provider + model via the same picker as `hermes model`
```

**Important:** `hermes fallback add` takes **no positional arguments**. It is fully interactive.

Fallback order: first entry is tried first after primary fails.

### Verify chain

```bash
hermes fallback list
```

### Edit manually (config.yaml)

For complex setups or key pools:
```yaml
fallback_providers:
  - provider: openrouter
    model: openrouter/free
  - provider: stepfun
    model: stepfun/step-3.7-flash
```

Full provider key names: `openrouter`, `groq`, `google`/`gemini`, `anthropic`, `openai`, `deepseek`, `nvidia`, `stepfun`, `qwen`, `mistral`, `custom`, etc.

## Recommended free provider patterns

| Role | Provider | Model | Free quota |
|------|----------|-------|------------|
| Primary (fast text/coding) | Groq | `llama-3.3-70b-versatile` | 30 RPM, 1K/day |
| Vision / images | Google AI Studio | `gemini-2.5-flash` | 15 RPM, 1.5K/day |
| Overflow / auto-pick | OpenRouter | `openrouter/free` | 200/day, 20 RPM |
| Last resort | StepFun | `stepfun/step-3.7-flash` | Stable per-session quota |

### Quota patterns
- Groq: fastest free inference (~320 tok/s); ideal for real-time Telegram/coding.
- OpenRouter `:free` models: 20 RPM, 200/day per model; meta-router `openrouter/free` picks best available.
- StepFun: known per-session quota via Nous Portal or direct key; use as guaranteed floor.
- Google AI Studio: generous daily limit; best for vision when Groq hits ceiling.

## Multi-provider setup pattern

For maximum uptime:
1. Set fastest model as **primary** (Groq)
2. Set **vision** auxiliary to best multimodal (Gemini Flash)
3. Set **fallbacks** in priority order: OpenRouter free router → StepFun
4. Verify: `hermes fallback list` shows the chain

## Pitfalls

- `hermes fallback add` **is interactive** — do not pass positional arguments.
- StepFun may not appear in `hermes model` provider list unless configured via Nous Portal or `custom` endpoint.
- Groq's free tier is aggressive on rate limits; design your task flow to use vision on a separate provider so it doesn't consume Groq quota.
- `OPENROUTER_API_KEY` env var is required before running `hermes fallback add openrouter ...`.
- Windows + Obsidian API + `curl.exe` = auth failures (401). Use Python `urllib` for vault API calls.
