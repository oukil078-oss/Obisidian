---
tags: []
aliases: []
created: 2026-06-27
---
# ZakOS Design System

> Premium dark canvas + lime accent + white contrast panel workspace aesthetic.
> Extracted from HubSpot CRM UI Kit reference, applied to ZakOS identity.

## Design Tokens

### Background layers
```css
--bg-canvas:        #0F0F0F
--bg-app:           #141414
--surface-1:        #1A1A1A
--surface-2:        #202020
--surface-3:        #272727
--surface-4:        #2E2E2E
--border-subtle:    rgba(255, 255, 255, 0.06)
--border-soft:      rgba(255, 255, 255, 0.10)
--border-emphasis:  rgba(255, 255, 255, 0.16)
```

### White summary panels
```css
--panel-white-bg:           #FFFFFF
--panel-white-surface:      #F7F7F7
--panel-white-border:       rgba(0, 0, 0, 0.08)
--panel-white-text-primary: #111111
--panel-white-text-secondary: #555555
--panel-white-text-muted:   #888888
```

### Lime / chartreuse accent
```css
--accent:           #A8FF3E
--accent-hover:     #BEFF57
--accent-pressed:   #96EE2C
--accent-muted:     rgba(168, 255, 62, 0.14)
--accent-border:    rgba(168, 255, 62, 0.30)
--accent-text:      #0F0F0F
```

### Text tokens
```css
--text-primary:   #F2F2F2
--text-secondary: #A8A8A8
--text-muted:     #6A6A6A
--text-faint:     #3E3E3E
--text-on-lime:   #0F0F0F
--text-on-white:  #111111
```

### Semantic status colors (muted for dark canvas)
```css
--status-green:   rgba(74, 222, 128, 0.70)
--status-yellow:  rgba(250, 204, 21, 0.70)
--status-red:     rgba(248, 113, 113, 0.70)
--status-blue:    rgba(96, 165, 250, 0.70)
```

### Radius scale
```css
--radius-xs:   6px
--radius-sm:   10px
--radius-md:   14px
--radius-lg:   20px
--radius-xl:   26px
--radius-2xl:  32px
--radius-pill: 9999px
```

### Motion tokens
```css
--duration-micro:  150ms
--duration-fast:   200ms
--duration-base:   260ms
--duration-slow:   360ms
--duration-xslow:  480ms
--ease-enter:  cubic-bezier(0.16, 1, 0.3, 1)
--ease-exit:   cubic-bezier(0.4, 0, 0.2, 1)
--ease-spring: cubic-bezier(0.22, 1, 0.36, 1)
```

## Component Blueprints

### Pill nav
- height 34–38px
- active: lime fill `#A8FF3E` / dark text `#0F0F0F`
- inactive: transparent / muted text
- hover: surface-2 / text-primary

### Standard card
```css
background: var(--surface-1);
border: 1px solid var(--border-subtle);
border-radius: var(--radius-lg);
padding: 20px;
hover:
  border-color: var(--border-emphasis);
  background: var(--surface-2);
  box-shadow: var(--shadow-md);
```

### White panel
```css
background: #FFFFFF;
border-radius: 24–32px;
padding: 24–28px;
```

### Avatar stack
- size 28–32px
- circle
- overlap -8 to -10px
- max 3–5 then +N

## Typography
- Primary: Inter / General Sans
- Body 14–15px weight 400 line-height 1.55
- Hierarchy via weight + size + opacity, not bold everywhere

## Layout Rules
- Top bar-first
- Pill navigation in top bar
- Jarvis blob centered in top bar
- No generic left sidebar
- Multi-column bento grid
- White summary panel on right for context
- No blue gradient hero
- No purple/teal accent
- No generic glassmorphism panels

## Key Files
- Frontend project: `C:\Users\pc\Documents\Vs-Code\Projects\ZakOS`
- Tokens: `frontend/app/globals.css`
- Layout: `frontend/components/layout/AppLayout.tsx`
- Top bar: `frontend/components/layout/TopBar.tsx`

## Anti-Patterns
- Glowing orb backgrounds
- Gradient hero sections
- Blue/Teal as primary accent
- Glassmorphism as core pattern
- Stock AI icons
- Default shadcn/ui without restyling
- Generic flat icon grids

---
#core-systems #zakos

