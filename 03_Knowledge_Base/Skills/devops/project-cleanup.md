---
skill: "project-cleanup"
category: "devops"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\devops\project-cleanup\SKILL.md"
vault_path: "Skills/devops/project-cleanup.md"
tags: ["devops", "hermes-skill", "skill"]
trigger_keywords: ["audit", "working", "tree", "changes", "separate", "valid", "work", "from", "accidents", "clean"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---
# project cleanup

---
name: project-cleanup
description: "Audit working tree changes, separate valid work from accidents, clean up binary/irrelevant files, and produce a clean commit+push. Use before any commit when the user reports uncommitted changes, asks to review changes, or says the page is blank/broken and may be caused by dirty state."
---

# Project Cleanup

## Trigger
- User reports N uncommitted changes in VS Code and asks you to review/cancel accidental ones.
- User suspects accidental edits, wrong files staged, or garbage in the working tree.
- Page is blank/breaking and the cause may be a corrupted build cache or dirty tree.
- Any "looks broken, can you check?" message where the root cause is untracked/binary/stray files.

## Workflow

### 1. Inventory
- Run `git status --short` to see staged, modified, and untracked files.
- Run `git diff --stat HEAD` to see actual content changes in modified files.
- Categorize:
  - **Valid completed work** — intentional UI/code changes that match the agreed design/spec.
  - **Accidental edits** — typos, test rewrites, wrong files, or half-finished refactors that should be reverted.
  - **Irrelevant files** — build artifacts, caches, local env files, binary dbs, venvs, pycache, lockfiles that shouldn't be tracked.

### 2. Cleanup irrelevant files first
- Update `.gitignore` to exclude anything that keeps showing up: `.next/`, `node_modules/`, `.env`, `__pycache__/`, `*.pyc`, `*.db`, `*.sqlite`, `*.log`, `data/`, `omnivoice-models/`, backend venv dirs.
- For tracked files that should now be ignored: `git rm --cached <file>` and `echo "<file>" >> .gitignore`.
- For untracked irrelevancies: just delete them from disk (`rm -rf`).

### 3. Fix accidental edits
- For tracked files with wrong content: `git checkout -- <file>` to restore HEAD.
- For untracked files that shouldn't exist: `rm` them.
- Confirm with `git status --short` that only valid work remains.

### 4. Stage and commit
- Stage explicitly: `git add <good-files>` rather than `git add -A` unless the tree is already clean.
- Commit message should describe the user-visible outcome, not the churn.
- If user explicitly asked before push: confirm commit list, then push.

### 5. Verify
- Run the app/build (`npx next build`, backend startup, etc.) to ensure the committed state actually works.
- Return to user: commit hash, what was cancelled, and confirmation that the pushed state matches their expectation.

## Principles
- **Be decisive.** When the user asks you to review changes and cancel accidents, don't over-explain each file. Categorize, cancel the noise, and report only the meaningful delta.
- **Verify before pushing.** Run the build and hit the live routes; don't rely on "passes locally" alone.
- **Clean tree = clean history.** A repo with 29 unstaged changes and binary DB files is a cleanup task, not a commit task.

## Pitfalls

### Next.js + heavy WASM deps in build
- Libraries like `@xenova/transformers` and `onnxruntime-web` bundle large `.wasm` binaries that Next.js webpack may fail to parse during build.
- If voice/ML features aren't ready, **stub** the importing module instead of letting dynamic imports pull in the heavy packages.
- A `voiceManager.ts` stub is fine for build stability; restore the real implementation only when the feature is ready to ship.

### Blank page after build failures
- If the app returns 500/blank after a failed build: the `.next` cache is likely corrupted.
- Fix: kill the dev server, `rm -rf .next`, `npx next build`, then restart dev.
- Missing dynamic imports (e.g. deleted `wakeWordDetector.ts` still referenced in `AppLayout.tsx`) will also break the build — search for all imports of removed files and clean them up.

### Binary DB files
- SQLite/local DB files (`*.db`, `*.sqlite`) must never be committed.
- If tracked: `git rm --cached <db-file>` and add to `.gitignore` immediately.

### Port conflicts after rebuild
- After deleting `.next` and rebuilding, stale Node processes may still hold port 3000/4000.
- Kill them (`taskkill //F //PID <pid>` on Windows, `kill` on *nix) before restarting dev server.

---
#devops #knowledge-base #skills

