---
skill: "ui-library-integration"
category: "software-development"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\software-development\ui-library-integration\SKILL.md"
vault_path: "Skills/software-development/ui-library-integration.md"
tags: ["software-development", "hermes-skill", "skill"]
trigger_keywords: ["class-level", "integration", "guide", "copying", "react", "component", "libraries", "into", "next", "when"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---

---
name: ui-library-integration
description: Class-level integration guide for copying React component libraries into a Next.js app when npm packages and CLI init are blocked or incomplete (e.g., Aceternity UI, Magic UI, React Bits). Covers registry auth, GitHub raw fetch, shim dependencies, and TypeScript fixes for Motion/particles/ogl/cobe.
---

# UI Library Integration (Manual Registry + GitHub Path)

Use this skill when the library’s npm package or CLI installer fails to yield usable source code, registries return stubs without JSX, or CLIs require unavailable API keys/telemetry. The proven path is: configure `components.json` auth when available, fetch registry JSON for Aceternity, then fall back to raw GitHub component files for Magic UI and React Bits.

## when to use
- `npx shadcn init` or `npx magicui-cli init` hangs, requires interactive prompts, or fails on missing keys
- `npm install @aceternity-ui / magicui / @react-bits/registry` resolves missing packages or returns stubs
- You need the actual copy-paste component source, not a published package

## sequence
1. Install core engine deps: `framer-motion`, `clsx`, `tailwind-merge`, `three`, `@react-three/fiber`, `@react-three/drei`, `gsap`.
   Install library-specific runtime deps per component: `@tabler/icons-react`, `cobe`, `ogl`, `@tsparticles/react`, `@tsparticles/engine`, `@tsparticles/slim`, `@radix-ui/react-icons`.
2. Create `frontend/lib/utils.ts` with the `cn()` helper.
3. Create `frontend/components/ui/button.tsx` shim if library components expect `@/components/ui/button`.
4. Add Aceternity registry auth to `components.json` if provided.
5. Fetch Aceternity components from `https://ui.aceternity.com/registry/<name>.json` with auth header, write file content verbatim.
6. Fetch React Bits components from `https://raw.githubusercontent.com/DavidHDev/react-bits/main/src/ts-default/...`.
7. Fetch Magic UI components from `https://raw.githubusercontent.com/magicuidesign/magicui/main/apps/www/registry/magicui/<name>.tsx`.
8. Patch TS incompatibilities:
   - Cast `GLOBE_CONFIG` to `any` before passing into `createGlobe(...) as any`
   - `// @ts-ignore` for `initParticlesEngine` import when CJS/ESM mismatch persists
   - Cast particles options objects and inner `attract`/`fill`/`shape` literals to `any`
   - If tsParticles v4 types still block, remove the type imports for `SingleOrMultiple` / `Container` and use `any` casts around option objects
   - For Magic UI bento-grid, the props shape may differ from Aceternity’s (`items` vs `children`); inspect the fetched component and use the correct prop shape, or wrap it so the consumer doesn’t have to match the library’s exact type
9. Build with `npx tsc --noEmit` then `npm run build`. Fix any missing deps or path aliases.

## references
- `references/registry-setup.md` — exact `components.json` shapes and auth header format
- `references/library-source-paths.md` — validated GitHub paths and expected component file names for Aceternity/Magic UI/React Bits, plus TypeScript fix patterns

## templates
- `templates/components.json` registry auth template
- `templates/lib-utils.ts` `cn()` helper
