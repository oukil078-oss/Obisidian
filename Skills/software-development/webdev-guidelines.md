---
skill: "webdev-guidelines"
category: "software-development"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\software-development\webdev-guidelines\SKILL.md"
vault_path: "Skills/software-development/webdev-guidelines.md"
tags: ["software-development", "hermes-skill", "skill"]
trigger_keywords: ["permanent", "webdev", "guidelines", "doctrine", "future", "websites", "apps", "unless", "explicitly", "overridden"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---

---
name: webdev-guidelines
description: "Permanent WebDev Guidelines doctrine for all future websites and web apps unless explicitly overridden. Load for any design/UI/frontend work."
triggers:
  - web design
  - dashboard design
  - SaaS UI
  - portfolio UI
  - AI product UI
  - admin/workspace UI
  - modern web app
  - frontend architecture
  - component design
---

# WebDev Guidelines

Inject this doctrine into every web design/engineering task. Full vault spec: `Mind-Galaxy/ZakOS WebDev Guidelines.md`.

## Core identity
Premium, futuristic, AI-native, elegant, high-end, polished, production-ready, calm but powerful, expensive-looking, crafted (not template-like).

## Design language
- **Premium futuristic dashboard** — soft rounded geometry everywhere, no sharp corners
- **Large pill tabs and capsule controls** — large rounded pill-shaped tabs and segmented controls
- **Rounded container shells** — all containers use generous rounded corners
- **Layered rounded cards** — cards stack with rounded borders and subtle depth
- **Calm spacing, clean hierarchy, subtle depth** — minimal but rich
- **No sharp corners, no generic admin template look, no boxy Tailwind look**
- **No excessive glassmorphism, no random gradients, no loud cyberpunk styling**

## UI components
- Top bar = premium rounded control dock
- Nav items = capsule tabs / segmented pills
- Buttons = soft pill buttons
- Cards = large rounded layered containers
- Filters = compact rounded chips
- List rows = soft rounded hover states
- Detail panes = grouped rounded blocks
- Utility actions = circular icon buttons
- Inputs/search = soft rounded fields with subtle borders

## Layout
- Prefer deep left sidebar + light canvas + frosted top bar for modern SaaS workspaces (Cloud Dock pattern).
- Three-zone top bar: left (search + brand) | center (optional hero) | right (utilities/profile/actions).
- **ZakOS override:** ZakOS explicitly uses the Cloud Dock layout (deep left sidebar + light canvas). Do NOT remove the sidebar or move navigation into the top bar. The ZakOS binding section below governs ZakOS.
- Modular rounded zones, compact-luxury density.

## Colors
**Accent:**
- `#C8FF2E` (active/selected/default)
- hover: `#D7FF53`
- pressed: `#B7EF1D`

**Dark theme (Salesforce invoice mockup exact):**
- bg-main: `#111827`
- bg-shell: `#111827`
- bg-card: `#1F2937`
- bg-card-soft: `#111827`
- bg-card-hover: `#283548`
- bg-elevated: `#1a2332`
- surface-1: `#1F2937`
- surface-2: `#283548`
- surface-3: `#374151`
- text-primary: `#F9FAFB`
- text-secondary: `#D1D5DB`
- text-muted: `#9CA3AF`
- border-soft: `#374151`

**Light theme (Salesforce invoice mockup exact):**
- bg-main: `#F3F4F6`
- bg-shell: `#FFFFFF`
- bg-card: `#FFFFFF`
- bg-card-soft: `#F9FAFB`
- bg-card-hover: `#F3F4F6`
- bg-elevated: `#FFFFFF`
- surface-1: `#FFFFFF`
- surface-2: `#F3F4F6`
- surface-3: `#E5E7EB`
- text-primary: `#111827`
- text-secondary: `#4B5563`
- text-muted: `#9CA3AF`
- border-soft: `#E5E7EB`

**Rules:**
- Mostly cool neutral UI
- Lime used very selectively
- No extra saturated random colors
- Both themes must be the same system with different tokens only
- **Mandatory:** define ALL CSS custom properties in `:root` and `[data-theme="light"]` BEFORE any component uses them. Missing tokens cause silent 500s at runtime.
- **Match reference mockups exactly** when user provides a visual spec. Don't substitute similar-looking colors — use the exact hex values from the mockup.
- **Avoid excessive glassmorphism** when the reference design uses solid fills. Use blur/backdrop-filter only where the mockup explicitly shows translucency.

## Type
Inter (primary, exclusive) → Satoshi / General Sans / system-ui fallback. Clean, tabular numerals for metrics. Do NOT use Outfit, Manrope, or JetBrains Mono as primary — they were evaluated and replaced.

### Scale
- page title: 42–56px
- section headings: 18–24px
- body: 14–16px
- labels/meta: 12–13px
- metric values: 28–40px
- button text: 13–15px

## Motion
- Easing: `cubic-bezier(0.16, 1, 0.3, 1)` · `cubic-bezier(0.22, 1, 0.36, 1)` · `cubic-bezier(0.4, 0, 0.2, 1)`
- Timing: micro 140–180ms, hover 160–220ms, tabs/chips 180–240ms, cards 220–280ms, panel/content change 260–340ms, overlays 320–420ms
- No abrupt/bouncy spam, no noisy loops, no gimmicks

### Animation libraries (ZakOS upgrade)
- **Three.js / WebGL:** Use for tasteful 3D animated backgrounds sitewide. Prefer lightweight scenes (particles, flowing geometry, soft orbs) over heavy post-processing. Target 120 FPS on typical hardware.
- **Framer Motion / Motion:** Primary for component transitions, layout animations, hover states, and page transitions. Use `motion`, `AnimatePresence`, `LayoutGroup`.
- **Aceternity UI:** Prefer for premium animated containers, overlay panels, and bento-style interactive cards.
- **Magic UI:** Prefer for subtle text reveals, cursor-follow effects, and micro-interactions on buttons/chips.
- **React Bits:** Use for agentic UI patterns, live data wrappers, and streaming/reactive components when available.
- Do NOT add heavy 3D to mobile performance-critical paths; degrade gracefully to CSS/canvas on small screens.

### Animate (all standard)
- Nav hover and active indicator
- Jarvis blob states
- Button hover/press
- Chip selection
- Card hover
- List selection
- Input focus
- Panel switching
- Loading states
- Skeleton shimmer
- Soft fade/translate transitions between content states

## AI/Jarvis feature
- Central, cinematic, premium motion
- Exactly centered in top bar, visually integrated
- Subtle pulse/glow, elegant reactive behavior
- Most special animated element, but still restrained
- State-aware: listen → 3 expanding pulse rings; speak → 5-bar waveform

## Role
Think: senior product designer + senior software engineer. Design systems, tokens, maintainability, accessibility, implementation realism.

## Consistency
Light and dark themes must keep the same layout, spacing, shapes, component logic, and animation behavior. Only colors, contrast, and depth treatment should change.

## ZakOS binding
- ZakOS applies `Mind-Galaxy/ZakOS WebDev Guidelines.md` for the full token spec, font stack, motion curves, and component style rules.
- **Override:** ZakOS was rebuilt (2026-06-25) to the **Cloud Dock** product direction: deep left sidebar + light canvas + frosted top bar. Do NOT remove the sidebar or push nav into the top bar. The doctrine in `zakos-context` now governs ZakOS layout.
- Icon library: ZakOS uses `lucide-react`. Do NOT import from `@phosphor-icons/react` (it was removed due to module-resolution failures on Windows/MSYS). When rewriting imports project-wide, use Python bulk-replace rather than MSYS `sed -i` (the `@` in the package name breaks sed escaping). Icon names are NOT 1:1 between phosphor and lucide; see `zakos-ui-rebuild` `references/lucide-icon-mapping.md` for the verified mapping.
- **Backend startup:** Use explicit venv Python: `cd backend && PYTHONPATH="" "venv/Scripts/python.exe" -m uvicorn server:app --host 0.0.0.0 --port 4000`.