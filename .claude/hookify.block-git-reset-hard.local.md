---
name: block-git-reset-hard
enabled: true
event: bash
pattern: git\s+reset\s+--hard
action: block
---

🛑 **BLOCKED: git reset --hard is destructive**

This command permanently discards changes without recovery.

**Why this is blocked:**
- In the previous session, I used `git reset --hard HEAD` and caused data loss
- This operation cannot be undone
- Changes are lost permanently

**What to do instead:**
1. Ask the user explicitly: "Should I run git reset --hard?"
2. Wait for their permission
3. Only proceed if they say yes

**If you need to discard changes:**
- Show the user what will be lost first
- Get explicit confirmation
- Consider `git stash` instead for recovery options
