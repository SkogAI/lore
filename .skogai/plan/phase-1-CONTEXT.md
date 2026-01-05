# Phase 1: Verify Pipeline - Context

**Gathered:** 2026-01-05
**Status:** Ready for research

<vision>
## How This Should Work

One command. One book with entries. One persona attached.

I run `lore-flow.sh` manually, and out comes a complete unit of lore: a book containing entries, linked to a persona. The content doesn't need to be great yet — it just needs to exist.

This is original SkogAI heritage. A 3800-token agent built this to make git diffs enjoyable. Getting it working honors that origin. It matters not just for lore but for SkogAI as a whole.

</vision>

<essential>
## What Must Be Nailed

- **lore-flow.sh produces entries with actual content** - Not empty, not error messages. Real narrative text in the JSON.
- **Ollama responds correctly** - The local LLM integration works. Prompts go in, content comes out.
- **Book + persona linking** - A book of entries exists, linked to a persona. This is the complete unit, the MVP.

</essential>

<boundaries>
## What's Out of Scope

- Content quality — that's Phase 2 (prompt tuning for Village Elder richness)
- Automatic triggering — that's Phase 3 (git hooks)
- Relationship linking between entries — that's Phase 4 (analyze-connections)
- Over-engineering — MVP means MVP, keep it simple

</boundaries>

<specifics>
## Specific Ideas

- Respect the original agent's work — this was built by a constrained agent, don't bloat it
- Simple smoke test: run one command, verify output exists and is linked correctly
- Issue #6 (empty content) was flagged but may already be fixed — verify current state before assuming

</specifics>

<notes>
## Additional Context

This is heritage work. The original SkogAI agent had 3800 tokens of context. It built this system to transform boring git diffs and documentation into something meaningful.

The value is twofold:
1. The lore itself (agents having persistent memory through narrative)
2. For SkogAI as a whole (proving local LLMs can do real work)

Keep it simple. Honor the origin.

</notes>

---

*Phase: 01-verify-pipeline*
*Context gathered: 2026-01-05*
