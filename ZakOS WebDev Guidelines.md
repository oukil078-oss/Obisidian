# ZakOS WebDev Guidelines

## Design Language
- Premium futuristic dashboard
- Soft rounded geometry everywhere — no sharp corners
- Large pill tabs and capsule controls
- Rounded container shells, layered rounded cards
- Calm spacing, clean hierarchy, subtle depth
- Minimal but rich
- Avoid generic admin templates, boxy Tailwind defaults, excessive glassmorphism, random gradients, cyberpunk styling

## Color System

### Accent
- `#C8FF2E` — active states, selected chips, key CTA, focused AI/Jarvis highlight
- Hover: `#D7FF53`
- Pressed: `#B7EF1D`
- Used very selectively

### Dark Theme Tokens
- `--bg-main: #0B111A`
- `--bg-shell: #101826`
- `--surface-1: #141D2B`
- `--surface-2: #192334`
- `--surface-3: #212D40`
- `--text-primary: #F4F7FB`
- `--text-secondary: #A7B2C2`
- `--text-muted: #7F8A99`

### Light Theme Tokens
- `--bg-main: #EEF3F8`
- `--bg-shell: #F5F8FC`
- `--surface-1: #FFFFFF`
- `--surface-2: #EAF0F6`
- `--surface-3: #DFE7F0`
- `--text-primary: #111827`
- `--text-secondary: #465266`
- `--text-muted: #6B778B`

### Rules
- Mostly cool neutral UI
- Lime used very selectively
- No extra saturated random colors
- Both themes use same system with different tokens only

## Typography
- Primary: **General Sans** (or Satoshi)
- Acceptable fallback: **Inter**
- Clean, premium, modern sans-serif
- Highly readable
- Elegant at large title sizes
- Not overbold, not oversized
- Tabular numerals for metrics

### Scale
- Page title: 42–56px
- Section headings: 18–24px
- Body: 14–16px
- Labels/meta: 12–13px
- Metric values: 28–40px
- Button text: 13–15px

## Component Style
- Top bar = premium rounded control dock
- Nav items = capsule tabs / segmented pills
- Buttons = soft pill buttons
- Cards = large rounded layered containers
- Filters = compact rounded chips
- List rows = soft rounded hover states
- Detail panes = grouped rounded blocks
- Utility actions = circular icon buttons
- Inputs/search = soft rounded fields with subtle borders

## Motion + Transitions
World-class micro-interactions with purpose: orientation, hierarchy, feedback, delight.
- Smooth, restrained, premium
- No bounce spam, no abrupt jumps, no noisy loops, no gimmicks

### Timing
- Micro: 140–180ms
- Hover: 160–220ms
- Tabs/chips: 180–240ms
- Cards: 220–280ms
- Panel/content change: 260–340ms
- Overlays: 320–420ms

### Easing
- `cubic-bezier(0.16, 1, 0.3, 1)`
- `cubic-bezier(0.22, 1, 0.36, 1)`
- `cubic-bezier(0.4, 0, 0.2, 1)`

### Animate
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

## Jarvis Blob
- Central AI core of the interface
- Exactly centered in the top bar
- Visually integrated, not floating randomly
- Premium ambient motion
- Subtle pulse/glow
- Elegant reactive behavior
- Most special animated element, but still restrained

## Consistency
- Light and dark themes keep the same layout, spacing, shapes, component logic, and animation behavior
- Only colors, contrast, and depth treatment change

## Default Preferences
- Premium futuristic rounded UI
- Top-bar-first architecture when suitable
- Jarvis/AI core treated as a central product element
- Cool neutral surfaces + restrained lime accent
- General Sans / Satoshi / Inter direction
- Strong design system thinking
- Elite motion quality
- Polished production-ready result
- Think as both a senior product designer and a senior software engineer
- Optimize for beauty, structure, scalability, responsiveness, accessibility, and implementation realism

## Avoid By Default
- Generic SaaS templates
- Boring admin dashboards
- Cheap AI visuals
- Sharp rectangles
- Weak typography
- Clutter
- Bad transitions
- Disconnected chatbot widgets

## Final Expectation
Adapt this design language to content while preserving premium aesthetic, rounded shape language, top-bar architecture, lime-accent restraint, and world-class motion quality.
