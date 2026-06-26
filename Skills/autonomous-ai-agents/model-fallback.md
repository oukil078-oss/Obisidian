---
skill: "model-fallback"
category: "autonomous-ai-agents"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\autonomous-ai-agents\model-fallback\SKILL.md"
vault_path: "Skills/autonomous-ai-agents/model-fallback.md"
tags: ["autonomous-ai-agents", "hermes-skill", "skill"]
trigger_keywords: ["configure", "free", "cloud", "fallback", "chains", "hermes", "agent", "optimal", "providers", "ordering"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---

---
name: model-fallback
description: "Configure free cloud LLM fallback chains for Hermes Agent: optimal providers, ordering, and setup for Telegram, coding, and GitHub workflows."
---

# Model Fallback — Free Cloud Stack

## Recommended free fallback chain

For coding, Telegram (voice/images/files), and GitHub work:

```yaml
model: google/gemini-2.5-flash
fallback_providers:
  - provider: groq
    model: llama-3.3-70b-versatile
  - provider: openrouter
    model: openrouter/free
```

### Why this order
| Position | Model | Strength |
|----------|-------|----------|
| Primary | Google Gemini 2.5 Flash | Best multimodal (Telegram images), 1M ctx, no credit card |
| Fallback 1 | Groq: Llama 3.3 70B | Fastest (~320 tok/s), good coding, 30 RPM / 1K/day |
| Fallback 2 | OpenRouter free router | Auto-selects best available free model (Nemotron, Gemma, Qwen, etc.) |

Combined free quota: ~2.5K requests/day before paid models.

## Setup

**Interactive:**
```bash
hermes model   # pick Google AI Studio (Gemini)
hermes fallback add groq llama-3.3-70b-versatile
hermes fallback add openrouter openrouter/free
```

**Direct config** (`~/.hermes/config.yaml`):
```yaml
model: google/gemini-2.5-flash
fallback_providers:
  - provider: groq
    model: llama-3.3-70b-versatile
  - provider: openrouter
    model: openrouter/free
```

## Free provider cheat sheet

| Provider | Quota | Speed | Best for |
|----------|-------|-------|----------|
| Google AI Studio | 15 RPM, 1.5K/day | Medium | Vision, long context (1M) |
| Groq | 30 RPM, 1K/day | ~320 tok/s | Fast replies, real-time |
| OpenRouter | 20 RPM, 200/day | Varies | Variety, failover router |
| NVIDIA NIM | ~1K/day, credits | Fast | Nous models (Hermes 3 405B) |
| Cerebras | 30 RPM, ~1M/day | Fast | Batch, high volume |
| Mistral | ~1B/month | Medium | Coding (Codestral) |

## Auto-switching behavior

Hermes automatically falls back on:
- Rate limits (HTTP 429)
- Server errors (500, 502, 503)
- Auth failures (401, 403)
- Not found (404)

Zero context loss on switch. Manually switch back with `/model` when limits reset.

## Adding GLM-5.2 or other models

If GLM-5.2 free tier is available (check OpenRouter or HuggingFace):
```yaml
fallback_providers:
  - provider: groq
    model: llama-3.3-70b-versatile
  - provider: openrouter
    model: z-ai/glm-5
  - provider: openrouter
    model: openrouter/free
```

HuggingFace Inference Providers: free monthly credits, slow cold starts — better for batch than live chat.
