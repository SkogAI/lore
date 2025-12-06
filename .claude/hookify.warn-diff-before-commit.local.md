---
name: warn-diff-before-commit
enabled: true
event: bash
pattern: git\s+commit
action: warn
---

⚠️ **IMPORTANT: Have you shown the user the diff?**

You're about to commit changes. **Did you review the diff with the user first?**

**The problem from last session:**
- I ran `git commit` without showing you the staged changes
- Committed merge conflict markers and broken code
- You told me: "READ THE FUCKING DIFFS BEFORE COMMITING WTF?!"

**Required workflow before ANY commit:**
1. Run `git diff --staged` or `git show HEAD` after commit
2. **SHOW THE USER** the actual changes being committed
3. Ask: "Does this look correct to commit?"
4. Wait for confirmation
5. THEN commit

**This is a WARNING, not a block:**
- The commit will still proceed
- But you MUST show diffs before committing
- Get in the habit: diff → review → confirm → commit

**Remember:** The user's explicit instruction was to always see what's being committed and get a "hey is that really a good idea" hint. This is that hint.
