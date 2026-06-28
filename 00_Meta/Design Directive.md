---
tags: []
aliases: []
created: 2026-06-27
---
# 🎨 UI/Design Standing Directive

> **Non-negotiable, always-active directive.** Applies to every website, dashboard, landing page, or UI project — no exceptions. Never fall back to generic templates, plain Tailwind cards, or boring layouts.

---

## ⚡ Core Philosophy

- Every UI must feel **handcrafted, editorial, and alive** — not like a shadcn starter kit or a Vercel template clone.
- Animations are **not decoration**, they are the product. Every interaction should feel intentional and premium.
- Dark mode is the **default aesthetic** unless explicitly told otherwise. Rich blacks, deep blues, glows.
- Avoid anything that looks like it came from a free Figma kit or a generic SaaS dashboard. If it could be on a landing page gallery with 200 identical sites, reject it.

---

## 🧩 Mandatory Component Libraries

### 1. Aceternity UI

- **Registry URL:** `https://ui.aceternity.com/registry/{name}.json`
- **Authorization header:**

```json
{
  "Authorization": "Bearer aceternity_27069c01182ee0816f891161190587e949424b8f6956e67448476aff71136bc2"
}
```

- **Priority components:** `background-beams`, `spotlight`, `tracing-beam`, `moving-border`, `card-hover-effect`, `3d-card`, `aurora-background`, `text-generate-effect`, `wavy-background`, `sparkles`
- If registry returns stubs: fetch raw `.tsx` from `https://github.com/aceternity/ui`

### 2. Magic UI

- **Registry MCP config:**

```json
{
  "mcpServers": {
    "magicuidesign-mcp": {
      "command": "npx",
      "args": ["-y", "@magicuidesign/mcp@latest"]
    }
  }
}
```

- **Fallback GitHub:** https://github.com/magicuidesign/magicui → `registry/` folder
- **Priority components:** `animated-beam`, `border-beam`, `shimmer-button`, `magic-card`, `neon-gradient-card`, `ripple`, `particles`, `dot-pattern`, `grid-pattern`, `blur-fade`, `word-rotate`, `typing-animation`, `number-ticker`, `orbiting-circles`

### 3. React Bits

- **Registry:** `https://reactbits.dev/r/{name}.json`
- **Fallback GitHub:** https://github.com/DavidHDev/react-bits
- **Priority components:** `SplitText`, `BlurText`, `ScrambleText`, `GlitchText`, `PixelTrail`, `TiltCard`, `MagneticButton`, `InfiniteScroll`, `ScrollReveal`, `Noise`, `Ribbons`, `Silk`, `Aurora`

---

## 🌐 3D & Motion Layer (Always Use These)

### Three.js / React Three Fiber

- `@react-three/fiber` + `@react-three/drei`
- Hero sections: **at minimum** one of: floating 3D geometry, particle systems, environment maps, GLSL shader backgrounds
- Recommended: `<Stars />`, `<Float />`, `<MeshDistortMaterial />`, `<MeshWobbleMaterial />`, `<Environment />`, `<Sparkles />` from `@react-three/drei`
- Heavy scenes: `Suspense` + `useGLTF`

### Framer Motion

- Every page transition: `AnimatePresence` + layout animations
- Stagger children on all lists/grids
- `useScroll` + `useTransform` for parallax/scroll-driven
- `motion.div` with `whileHover`, `whileTap`, `whileInView` on **every interactive element**
- `spring` physics (`type: "spring", stiffness: 300, damping: 20`) over ease curves

### GSAP (when Framer isn't enough)

- `gsap.timeline()` for complex multi-step entrances
- `ScrollTrigger` for cinematic scroll reveals
- `SplitText` for character-by-character animations

---

## 🎨 Visual Identity Rules

- **Typography:** Variable/display fonts (`Geist`, `Cal Sans`, `Syne`, `Space Grotesk`) — never system defaults alone
- **Color:** Always include glow/neon accent. Favorites: `#7c3aed` (violet), `#06b6d4` (cyan), `#f59e0b` (amber)
- **Backgrounds:** Mesh gradients, noise textures, dot/grid patterns, aurora effects — never flat white/gray
- **Borders:** Animated gradients, `moving-border` (Aceternity), glowing box shadows — no plain 1px gray
- **Buttons:** Shimmer, magnetic hover, gradient fills — never flat
- **Cards:** 3D tilt, glassmorphism + animated borders, spotlight hover — never plain white + shadow

---

## 🚫 Banned Patterns

- Generic hero: headline + CTA + plain background
- Plain shadcn `<Card>` without layered effects
- Default Tailwind palette without customization
- `opacity-0 → opacity-100` as the only animation
- Stock photo hero images
- Navbar with just links, no visual treatment
- Footer with just text links
- Boring loading spinners (use skeleton shimmers / Magic UI loaders)

---

## 🔧 Stack Integration

- **Next.js** (App Router preferred)
- **React + Vite**
- **Any full-stack** (Express/Node backend + React frontend)

Always configure `tailwind.config.js` with custom animations, keyframes, and design tokens.

---

## 📦 components.json Template

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "zinc",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  },
  "registries": {
    "@aceternity": {
      "url": "https://ui.aceternity.com/registry/{name}.json",
      "headers": {
        "Authorization": "Bearer aceternity_27069c01182ee0816f891161190587e949424b8f6956e67448476aff71136bc2"
      }
    },
    "@react-bits": "https://reactbits.dev/r/{name}.json"
  }
}
```

---

## 🧠 Agent Enforcement Rules

1. Before scaffolding any UI, check which library is most appropriate.
2. Always layer effects: base Tailwind + motion wrapper + one Aceternity/Magic UI/React Bits effect minimum.
3. Never ask "should I add animations?" — animations are always yes. Ask *which* animation.
4. If a component doesn't exist in these libraries, build a custom one with Framer Motion + Tailwind — never fall back to plain HTML.
5. Reference this document at the start of every new project or UI session.

---

*Created by Zakarya Oukil — Permanent design standard for all projects.*

---
#meta

