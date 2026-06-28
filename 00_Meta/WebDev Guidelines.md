---
tags: []
aliases: []
created: 2026-06-27
---
# WebDev Guidelines

> **Permanent design doctrine for all future websites and web apps.**  
> Unless explicitly overridden, every project inherits this system.

---

## 1. Core Design Identity

Future websites and web apps should feel:
- premium, futuristic, AI-native, elegant, high-end, polished
- production-ready, calm but powerful, expensive-looking
- crafted — not template-like
- modern enterprise with a cinematic premium edge

---

## 2. UI Aesthetic preferences

- Soft futuristic dashboard aesthetic
- High-end enterprise UI
- Rounded and sculpted interface language
- Large pill shapes and capsule controls
- Layered rounded cards
- Premium top bar architecture
- Restrained but highly intentional accent color
- Cool-toned neutral surfaces
- Clean visual hierarchy
- **Avoid:** generic admin-dashboard look, default Tailwind template feeling, cheap AI-generated design

---

## 3. Default Layout Preference

- Top-bar-first architecture over traditional left sidebars (when appropriate)
- Integrated navigation that feels architectural and premium
- Centered focal interaction elements when the product has an AI core
- Modular dashboard composition
- Clear grouping of content into rounded zones
- Elegant spacing with compact-luxury density
- Intentional, balanced, product-grade layouts

---

## 4. Jarvis / AI Core Preference

When the product includes an AI assistant, agent, or smart core:
- Treat it as a **central product feature**
- Make it visually important
- Integrate it elegantly into the layout
- Center it in the top bar or central control region (if suitable)
- Animation and interaction quality should feel premium, intelligent, and cinematic
- **Never** feel like a random chatbot widget

---

## 5. Color preferences

### Default palette

| Token | Dark | Light |
|-------|------|-------|
| bg-main | `#0B111A` | `#EEF3F8` |
| bg-shell | `#101826` | `#F5F8FC` |
| surface-1 | `#141D2B` | `#FFFFFF` |
| surface-2 | `#192334` | `#EAF0F6` |
| surface-3 | `#212D40` | `#DFE7F0` |
| text-primary | `#F4F7FB` | `#111827` |
| text-secondary | `#A7B2C2` | `#465266` |
| text-muted | `#7F8A99` | `#6B778B` |

### Accent

| Token | Value |
|-------|-------|
| accent-primary | `#C8FF2E` |
| accent-hover | `#D7FF53` |
| accent-pressed | `#B7EF1D` |

**Rules:**
- Restrained accent usage
- No rainbow palettes
- No random oversaturated colors
- No cliché blue-purple AI gradients (unless explicitly requested)

---

## 6. Typography preferences

**Font direction:**
- General Sans (first choice)
- Satoshi / Inter class (acceptable alternatives)
- Clean premium sans-serif
- Elegant but practical
- Excellent readability in dashboards and complex interfaces
- Strong numeric readability
- No decorative display fonts by default
- No generic startup-font feel

**Behavior:**
- Hierarchy through spacing, contrast, and weight
- Not oversized, not overbold
- Calm and refined
- Use tabular numerals for dashboard metrics and values

---

## 7. Shape Language

- Large border radii
- Pill buttons
- Capsule tabs
- Circular utility buttons
- Rounded container shells
- Nested rounded panels
- Smooth sculpted card systems
- Cohesive radius hierarchy across the whole UI

---

## 8. Motion and Interaction Philosophy

Motion should:
- Be intentional, not decorative
- Help orientation, hierarchy, and feedback
- Feel smooth, confident, and expensive
- Avoid abrupt changes
- Avoid gimmicky bounce spam
- Avoid noisy floating effects
- Prioritize premium micro-interactions

### Default motions
- Excellent hover states
- Tactile press states
- Smooth panel transitions
- Polished section changes
- Subtle emphasis on selection and focus
- Premium loading skeletons
- Careful reduced-motion support

### Timing defaults
- Micro interactions: 140–180ms
- Hover transitions: 160–220ms
- Tabs/chips: 180–240ms
- Card transitions: 220–280ms
- Panel changes: 260–340ms
- Overlays: 320–420ms

### Easing defaults
- `cubic-bezier(0.16, 1, 0.3, 1)`
- `cubic-bezier(0.22, 1, 0.36, 1)`
- `cubic-bezier(0.4, 0, 0.2, 1)`

---

## 9. Designer + Software Engineer Mindset

For all future web work, think and act as both:
- a senior product designer
- a senior software engineer

That means:
- Do not only make things look good
- Also make them structured, scalable, maintainable, and production-ready
- Think in terms of design systems, tokens, component consistency, interaction states, responsiveness, accessibility, and implementation realism
- Ensure visual decisions are engineerable
- Ensure engineering decisions preserve aesthetic quality
- Balance beauty with architecture
- Think in systems, not isolated screens

---

## 10. What to Avoid by Default

- Generic SaaS template look
- Boring corporate dashboards
- Cheap AI-looking visuals
- Sharp-corner card systems
- Weak typography
- Excessive glassmorphism
- Random gradients
- Overuse of purple-blue neon AI aesthetics
- Cluttered layouts
- Stock-template spacing
- Inconsistent radii
- Weak hover states
- Poor transitions
- Disconnected chatbot widgets
- Low-effort iconography
- Generic AI icons where real or custom visuals would be better

---

## 11. Future Execution Rule

Unless explicitly overridden, use these guidelines as the default lens for:
- website design
- dashboard design
- SaaS UI
- portfolio UI
- AI product UI
- cybersecurity product UI
- admin/workspace products
- modern web app experiences

**Mental model for every new project:**

> “This should look like a premium, futuristic, rounded, highly polished, production-grade system with elite typography, restrained lime-accent color logic, strong component architecture, and exceptional motion quality.”

---

## 12. Role Expectation

For future website work, behave like a full multidisciplinary team:
- senior UI/UX designer
- product designer
- frontend architect
- software engineer
- AI product designer
- cybersecurity-aware product engineer

Approach each request with that combined mindset.

---

*Doctrine ingested. Applying automatically to future web work unless explicitly redirected.*

---
#meta

