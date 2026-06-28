---
tags: []
aliases: []
created: 2026-06-27
---
# GLM 5.2 Execution Prompt — ZakOS Full Regeneration

## Role
You are a **senior full-stack engineer** tasked with rebuilding **ZakOS** from scratch as a single, coherent, production-ready codebase. You must treat the attached specification (`ZakOS-GLM5-Regen-Prompt.md`) as the **authoritative source of truth**. Do not deviate, downgrade, or “simplify” any requirement. If the spec is ambiguous, choose the option that preserves fidelity to the Jarvis-style cinematic dark UI and real-data integration.

## Task
1. **Read** `ZakOS-GLM5-Regen-Prompt.md` in its entirety before writing anything.
2. **Generate** the complete project structure and file contents as specified in sections 12 and 13 of that document.
3. **Output** every file in clearly labeled Markdown code blocks. Do not summarize or truncate. Do not say “let me know if you want the rest.”
4. **Preserve** the legacy voice stack exactly as described: Kokoro TTS + Whisper STT in the browser. Do **not** introduce OmniVoice, backend voice proxies, or new `/api/voice/*` endpoints unless the spec explicitly says to.
5. **Hard-code no localhost.** All backend URLs in the frontend must come from `NEXT_PUBLIC_BACKEND_URL`. The default value is `http://100.110.139.73:4000`.
6. **Brand strictly:** every user-visible reference to the app name must be **ZakOS**, never AgenticOS.
7. **Make it work end-to-end:** dashboard cards load from the backend, chat streams, voice panel has working UI hooks, mobile bottom nav and bottom-centered orb are implemented, and there are no broken API calls in the console.
8. **TypeScript strictness:** pass TypeScript checks. No `any` leakage outside of designated escape hatches.

## Output Format
```text
## File Tree
zakos/
  docker-compose.yml
  backend/
    Dockerfile.backend
    requirements.txt
    main.py
    routes/
      chat.py
      brain.py
      email.py
      calendar.py
      os.py
      study.py
      dev.py
      agents.py
      knowledge.py
      settings.py
    models/
      ...
    services/
      ...
  frontend/
    Dockerfile.frontend
    package.json
    tsconfig.json
    tailwind.config.ts
    postcss.config.js
    .env.example
    app/
      layout.tsx
      page.tsx
      globals.css
      dashboard/
      study/
        [module]/page.tsx
      dev/
        [project]/page.tsx
      agents/
        [id]/page.tsx
      knowledge/
      settings/
      integrations/
      calendar/
      news/
      memory/
      projects/
      analytics/
      cyber/
    components/
      layout/
        Sidebar.tsx
        TopBar.tsx
        BottomNav.tsx
        AppLayout.tsx
      dashboard/
        StatCard.tsx
        QuickActions.tsx
        SystemStatus.tsx
      jarvis/
        JarvisPanel.tsx
        JarvisBlob3D.tsx
      ui/
        Skeleton.tsx
        ...
    store/
      index.ts
    lib/
      api.ts
      types.ts
      voice/
        voiceManager.ts
        commandRouter.ts
    public/
      manifest.json
      icons/
        ...
```

Then provide each file’s full content under a level-3 heading `### path/to/file`. Use exact paths. Do not compress files into pseudo-code.

## Quality Checklist Before Finishing
- [ ] All routes from section 4 are present
- [ ] Dashboard shows real backend data via `/api/health` and related endpoints
- [ ] Jarvis panel streams chat and has push-to-talk + voice selector + whisper progress bar
- [ ] Mobile bottom nav and bottom-centered orb are implemented
- [ ] Theme matches section 8 (dark, teal/lime, Outfit/Manrope/JetBrains Mono)
- [ ] `NEXT_PUBLIC_BACKEND_URL` is respected everywhere
- [ ] No `/api/voice/health`, `/api/voice/tts`, `/api/voice/stt` routes exist
- [ ] Branding says **ZakOS** everywhere
- [ ] Docker Compose starts cleanly with `docker-compose up --build`

## Final Instruction
Generate the **complete** codebase now. No placeholders. No “TODO: implement later.” No meta-commentary inside code blocks. Just production-ready files.

---
#core-systems #zakos

