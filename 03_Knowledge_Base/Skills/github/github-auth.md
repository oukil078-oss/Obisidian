---
skill: "github-auth"
category: "github"
source_path: "C:\Users\pc\AppData\Local\hermes\skills\github\github-auth\SKILL.md"
vault_path: "Skills/github/github-auth.md"
tags: ["github", "hermes-skill", "skill", "GitHub", "Authentication", "Git", "gh-cli", "SSH", "Setup"]
trigger_keywords: ["github", "auth", "setup", "https", "tokens", "keys", "login"]
last_synced: "2026-06-25T09:50:59.662609"
type: "hermes-skill"
---
# github auth

---
name: github-auth
description: "GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    Tags: [GitHub, Authentication, Git, gh-cli, SSH, Setup]
    related_skills: [github-pr-workflow, github-code-review, github-issues, github-repo-management]
---

# GitHub Authentication Setup

This skill sets up authentication so the agent can work with GitHub repositories, PRs, issues, and CI. It covers two paths:

- **`git` (always available)** — uses HTTPS personal access tokens or SSH keys
- **`gh` CLI (if installed)** — richer GitHub API access with a simpler auth flow

## Detection Flow

When a user asks you to work with GitHub, run these checks first:

```bash
# 1. Check for gh CLI at default path
if gh --version &>/dev/null; then
  echo "✅ gh CLI detected at default path: $(gh --version | head -1)"
fi

# 2. Check custom install location (common Windows scenario)
if [ -f "$LOCALAPPDATA\Programs\gh\gh.exe" ]; then
  export PATH="$LOCALAPPDATA\Programs\gh:$PATH"
  gh --version &>/dev/null && echo "✅ gh CLI found at custom path!"
fi

# 3. Check git credential helper status
git config --global credential.helper 2>/dev/null || echo "⚠️ No git credential helper configured"

# 4. Check auth state if gh is available
gh auth status &>/dev/null && echo "✅ gh is authenticated" || echo "ℹ️ gh not authenticated (need to set up)"
```

**Decision tree:**
1. **`gh auth status` shows authenticated** → ✅ Use `gh` for all GitHub operations
2. **`gh` binary exists but not authenticated** → Use Method 2 (gh CLI authentication)
3. **No `gh` binary found anywhere** → Fall back to Method 1 (git-only authentication)

---

## Method 1: Git-Only Authentication (No gh, No sudo)

This works on any machine with `git` installed. No root access needed.

### Option A: HTTPS with Personal Access Token (Recommended)

This is the most portable method — works everywhere, no SSH config needed.

**Step 1: Create a personal access token**

Tell the user to go to: **https://github.com/settings/tokens**

- Click "Generate new token (classic)"
- Give it a name like "hermes-agent"
- Select scopes:
  - `repo` (full repository access — read, write, push, PRs)
  - `workflow` (trigger and manage GitHub Actions)
  - `read:org` (if working with organization repos)
- Set expiration (90 days is a good default)
- Copy the token — it won't be shown again

**Step 2: Configure git to store the token**

```bash
# Set up the credential helper to cache credentials
# "store" saves to ~/.git-credentials in plaintext (simple, persistent)
git config --global credential.helper store

# Now do a test operation that triggers auth — git will prompt for credentials
# Username: <their-github-username>
# Password: <paste the personal access token, NOT their GitHub password>
git ls-remote https://github.com/<their-username>/<any-repo>.git
```

After entering credentials once, they're saved and reused for all future operations.

**Alternative: cache helper (credentials expire from memory)**

```bash
# Cache in memory for 8 hours (28800 seconds) instead of saving to disk
git config --global credential.helper 'cache --timeout=28800'
```

**Alternative: set the token directly in the remote URL (per-repo)**

```bash
# Embed token in the remote URL (avoids credential prompts entirely)
git remote set-url origin https://<username>:<token>@github.com/<owner>/<repo>.git
```

**Step 3: Configure git identity**

```bash
# Required for commits — set name and email
git config --global user.name "Their Name"
git config --global user.email "their-email@example.com"
```

**Step 4: Verify**

```bash
# Test push access (this should work without any prompts now)
git ls-remote https://github.com/<their-username>/<any-repo>.git

# Verify identity
git config --global user.name
git config --global user.email
```

### Option B: SSH Key Authentication

Good for users who prefer SSH or already have keys set up.

**Step 1: Check for existing SSH keys**

```bash
ls -la ~/.ssh/id_*.pub 2>/dev/null || echo "No SSH keys found"
```

**Step 2: Generate a key if needed**

```bash
# Generate an ed25519 key (modern, secure, fast)
ssh-keygen -t ed25519 -C "their-email@example.com" -f ~/.ssh/id_ed25519 -N ""

# Display the public key for them to add to GitHub
cat ~/.ssh/id_ed25519.pub
```

Tell the user to add the public key at: **https://github.com/settings/keys**
- Click "New SSH key"
- Paste the public key content
- Give it a title like "hermes-agent-<machine-name>"

**Step 3: Test the connection**

```bash
ssh -T git@github.com
# Expected: "Hi <username>! You've successfully authenticated..."
```

**Step 4: Configure git to use SSH for GitHub**

```bash
# Rewrite HTTPS GitHub URLs to SSH automatically
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

**Step 5: Configure git identity**

```bash
git config --global user.name "Their Name"
git config --global user.email "their-email@example.com"
```

---

## Method 2: gh CLI Authentication (Requires Installation)

**⚠️ Note:** The `gh` CLI tool provides richer GitHub API access but installation can be tricky on Windows without sudo/admin privileges.

### Installation Methods (Try in Order)

1. **Official installer (Recommended for first-time install)**
   ```bash
   # Download official Windows installer from:
   curl -sSLO https://github.com/cli/cli/releases/latest/download/gh-windows-amd64.msi
   # Run the MSI installer with admin rights, or copy gh.exe manually
   # After install: gh --version
   ```

2. **winget (Desktop Windows)**
   ```bash
   winget install GitHub.cli
   # If prompted with terms/agreements: type 'y' and press Enter
   ```

3. **Chocolatey (requires Chocolatey package manager)**
   ```bash
   choco install -y gh-cli
   ```

4. **Manual download of portable executable**
   ```bash
   curl -sSLO "https://github.com/cli/cli/releases/latest/download/gh-windows-amd64.exe"
   mkdir -p "$LOCALAPPDATA\Programs\gh"
   mv gh-windows-amd64.exe "$LOCALAPPDATA\Programs\gh\gh.exe"
   
   # Add to PATH (run once per session)
   export PATH="$LOCALAPPDATA\Programs\gh:$PATH"
   ```

### Detection: Check if gh is available anywhere on the system

```bash
# Method A: Try command first
gh --version 2>/dev/null && echo "gh CLI detected at default path"

# Method B: If that fails, check for manual install location
if [ -f "$LOCALAPPDATA\Programs\gh\gh.exe" ]; then
  export PATH="$LOCALAPPDATA\Programs\gh:$PATH"
  gh --version && echo "gh CLI detected at custom path"
fi

# Method C: Search all locations (last resort)
which gh 2>/dev/null || find "$HOME" -name "gh.exe" 2>/dev/null | head -1
```

### Interactive Browser Login (Desktop)

```bash
gh auth login
# Select: GitHub.com → HTTPS → Authenticate via browser
```

### Token-Based Login (Headless / SSH Servers)

```bash
echo "<THEIR_TOKEN>" | gh auth login --with-token

# Set up git credentials through gh
gh auth setup-git
```

### Verify and Troubleshoot Installation Issues

```bash
gh auth status  # Shows authentication state
gh version      # Confirm CLI is working
```

**Common Windows installation problems:**
| Problem | Solution |
|---------|----------|
| `winget` prompts for agreement manually | Type `y` then Enter when prompted |
| `choco` package not found | Use official installer or manual download instead |
| Permission denied during install | Download gh.exe and place in `$LOCALAPPDATA\Programs\gh` manually |
| `gh: command not found` after install | Add to PATH: `export PATH="$LOCALAPPDATA\Programs\gh:$PATH"` |

### Authenticate with gh CLI

Once installed, authenticate:

```bash
gh auth login
# OR for headless environments:
echo "<THEIR_TOKEN>" | gh auth login --with-token

# Configure git to use gh's credential manager
gh auth setup-git
```

Verify authentication:
```bash
gh auth status
# Expected output shows authenticated state with username
```

---

## Using the GitHub API Without gh
---\n\n## Using the GitHub API Without gh

When `gh` is not available, you can still access the full GitHub API using `curl` with a personal access token. This is how the other GitHub skills implement their fallbacks.

### Setting the Token for API Calls

```bash
# Option 1: Export as env var (preferred — keeps it out of commands)
export GITHUB_TOKEN="<token>"

# Then use in curl calls:
curl -s -H "Authorization: token $GITHUB_TOKEN" \\\n  https://api.github.com/user
```

### Extracting the Token from Git credentials

If git credentials are already configured (via credential.helper store), the token can be extracted:

```bash
# Read from git credential store
grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\\([^@]*\\)@.*|\\1|'
```

### Helper: Detect Auth Method

Use this pattern at the start of any GitHub workflow:

```bash
# Try gh first, fall back to git + curl
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  echo "AUTH_METHOD=gh"
elif [ -n "$GITHUB_TOKEN" ]; then
  echo "AUTH_METHOD=curl"
elif _hermes_env="${HERMES_HOME:-$HOME/.hermes}/.env"; [ -f "$_hermes_env" ] && grep -q "^GITHUB_TOKEN=" "$_hermes_env"; then
  export GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" "$_hermes_env" | head -1 | cut -d= -f2 | tr -d '\\n\\r')
  echo "AUTH_METHOD=curl"
elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
  export GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials | head -1 | sed 's|https://[^:]*:\\([^@]*\\)@.*|\\1|')
  echo "AUTH_METHOD=curl"
else
  echo "AUTH_METHOD=none"
  echo "Need to set up authentication first"
fi
```

---

## Windows-Specific Troubleshooting

### gh CLI Installation Issues (Windows)

**Problem:** `winget install --id GitHub.cli` fails with agreement prompts or errors.

**Solutions:**
1. **Manual yes for winget prompts:**
   ```bash
   echo "y" | winget install GitHub.cli
   ```

2. **Use manual download (works anywhere):**
   ```bash
   curl -sSLO "https://github.com/cli/cli/releases/latest/download/gh-windows-amd64.exe"
   mkdir -p "$LOCALAPPDATA\Programs\gh"
   mv gh-windows-amd64.exe "$LOCALAPPDATA\Programs\gh\gh.exe"
   export PATH="$LOCALAPPDATA\Programs\gh:$PATH"
   ```

3. **Verify installation:**
   ```bash
   which gh 2>/dev/null || findstr /S /I "gh.exe" C:\Windows\System32;C:\Users\*
   ```

### Git Credential Helper on Windows

**Problem:** `git config --global credential.helper` shows as configured but still prompts.

**Solution:**
- Check the actual helper: `git config --list | findstr credential`
- Windows may need: `git config --global core.longpaths true`
- For HTTPS URLs, consider using token in URL: `git remote set-url origin https://user:token@github.com/...`

### PATH Issues on Windows

**Problem:** Commands like `gh` not found even after installation.

**Solution:** Add to PATH and verify:
```bash
export PATH="$LOCALAPPDATA\Programs\gh:$PATH"
echo $PATH  # Verify it includes the gh path
which gh     # Should show full path if in PATH
```

---

## Troubleshooting

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `git push` asks for password | GitHub disabled password auth. Use a personal access token as the password, or switch to SSH |
| `remote: Permission to X denied` | Token may lack `repo` scope — regenerate with correct scopes |
| `fatal: Authentication failed` | Cached credentials may be stale — run `git credential reject` then re-authenticate |
| `ssh: connect to host github.com port 22: Connection refused` | Try SSH over HTTPS port: add `Host github.com` with `Port 443` and `Hostname ssh.github.com` to `~/.ssh/config` |
| credentials not persisting | Check `git config --global credential.helper` — must be `store` or `cache` |
| Multiple GitHub accounts | Use SSH with different keys per host alias in `~/.ssh/config`, or per-repo credential URLs |
| `gh: command not found` + no sudo | Use git-only Method 1 above — no installation needed |

---
#github #knowledge-base #skills

