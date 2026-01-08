# Phase 2 Context: Quality Prompts

**Created:** 2026-01-06  
**Vision:** Transform technical content into connected lore entities that carry real meaning

## How This Works

Phase 2 is about **meaningful extraction and connection**, not pretty prose.

The pipeline (`lore-flow.sh`) already works:
```
Input (README, commit, etc.)
  → LLM prompt
  → Narrative output
  → Entry creation
```

Phase 2 tunes the **LLM prompt** so that Ollama can:
1. Extract multiple entities from technical content (characters, places, concepts)
2. Create entries that connect to each other
3. Generate functional mythological framing (not necessarily Village Elder poetry)
4. Populate relationship metadata (`entry.relationships[]`)

## What's Essential

### Test-Driven Development

**Test 0.1: Baseline**
- Simple input → single output entry
- Proves basic prompt structure works with Ollama
- Document: input used, output received, what worked/didn't

**Test 0.2: README Extraction**
- Five README files from different projects (can be made up for simplicity)
- **Expected outcome:** Each README → 3-5 connected entries
- Entries should:
  - Extract meaningful entities (not just summarize the README)
  - Connect to each other via `relationships[]` metadata
  - Have mythological framing that makes technical concepts memorable

### All Types of Connections

Success means entries connect across **all dimensions**:

1. **Technical connections**: "git hooks entry relates to automation entry"
2. **Narrative connections**: "Village Elder witnessed both the Hook Installation and the Automation Ritual"  
3. **Relationship metadata**: Actual JSON `relationships` array with `target_id` + `relationship_type`
4. **Book organization**: Entries grouped into meaningful books, not random collections
5. **Whatever else emerges**: The interesting part is discovering new connection types

### Quality = Meaningful Connection

Not about:
- ❌ "Say three sentences that sound fantasy"
- ❌ Perfect Village Elder prose
- ❌ Beautiful writing

About:
- ✅ Extracting entities that matter
- ✅ Creating links that hold value
- ✅ Building a connected knowledge graph through narrative

## What's Out of Scope

Explicitly NOT solving in Phase 2:

- **Auto-trigger from git commits** → Phase 3
- **Perfect prose quality** → Functional narrative is enough, Village Elder poetry not required
- **Relationship discovery to existing entries** → Phase 4 (new entries connecting to each other is fine)
- **Production-ready error handling** → Happy path testing only

## Success Looks Like

After Phase 2 completion:
- ✅ Test 0.1 documented with results
- ✅ Test 0.2 documented: 5 READMEs → 15-25 connected entries
- ✅ Prompts tuned for Ollama (not just Claude)
- ✅ Entries have populated `relationships[]` metadata
- ✅ Clear understanding of what "quality" means in concrete terms
- ✅ Examples of all connection types working

## The Interesting Part

Phase 2 is exploration: **what connections emerge when you feed real technical content into a mythological narrative pipeline?**

Document everything. The tests will reveal what works.
