---
name: block-git-push-force
enabled: true
event: bash
pattern: git\s+push\s+(-f|--force)
action: block
---

🛑 **BLOCKED: git push --force is dangerous**

Force-pushing rewrites remote history and can destroy other people's work.

**Why this is blocked:**
- Overwrites remote commits without merging
- Can lose work from other developers
- Breaks shared repository history

**What to do instead:**
1. Ask the user: "Do you want me to force-push? This will rewrite remote history."
2. Show what commits will be overwritten
3. Only proceed with explicit permission

**Safer alternatives:**
- `git push --force-with-lease` (checks for remote changes first)
- Rebase and push normally
- Ask the user what they prefer
