---
name: warn-git-reset
enabled: true
event: bash
pattern: git\s+reset(?!\s+--hard)
action: warn
---

⚠️ **WARNING: git reset operation detected**

You're about to run a git reset command.

**Why this warning:**
- In the previous session, I ran git reset operations without permission
- Reset operations change repository state
- Users should be aware when this happens

**Before proceeding:**
1. Consider if this is what the user asked for
2. If unsure, ask: "Should I run this git reset command?"
3. Explain what the reset will do

**Note:** This is a warning only - the command will still run.
For destructive operations like `git reset --hard`, there's a separate blocking rule.
