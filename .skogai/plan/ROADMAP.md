# Roadmap: Lore Integration

## Overview

Wire the existing 5-step pipeline to run end-to-end with Ollama, producing quality narrative lore from git activity. The pieces exist — this milestone connects them into a working system.

## Domain Expertise

- Shell scripting and integration patterns
- LLM prompt engineering (Ollama-specific constraints)

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [x] **Phase 1: Verify Pipeline** - End-to-end smoke test with Ollama (DONE 2026-01-05)
- [ ] **Phase 2: Quality Prompts** - Tune prompts for Village Elder quality output
- [ ] **Phase 3: Auto-trigger** - Git hooks fire the pipeline automatically
- [ ] **Phase 4: Polish** - Context continuity and relationship linking

## Phase Details

### Phase 1: Verify Pipeline
**Goal**: Confirm lore-flow.sh works end-to-end with Ollama, producing a real entry
**Depends on**: Nothing (first phase)
**Research**: Unlikely (existing tools)
**Plans**: 1 (Fix bug + verify)

Key validations:
- Ollama responds correctly to pipeline calls
- Entry JSON written with actual content (Issue #6 fixed)
- Book and persona linking works

### Phase 2: Quality Prompts
**Goal**: Extract embedded prompts from shell scripts into external files to enable iteration
**Depends on**: Phase 1
**Research**: Unlikely (simple refactoring)
**Plans**: 2 (llama-lore-creator.sh, llama-lore-integrator.sh)

Scope:
- Extract 7 prompts from llama-lore-creator.sh, llama-lore-integrator.sh, lore-flow.sh
- Move to agents/prompts/ following repository standards (YAML frontmatter, categories, examples)
- Update scripts to read from external files
- Verify functionality unchanged

Key outcomes:
- Prompts externalized and documented
- Scripts read from agents/prompts/ directory
- Iteration enabled without touching shell code
- Foundation for future prompt quality improvements (Issue #5 fixes come after)

### Phase 3: Auto-trigger
**Goal**: Git commits automatically generate lore without manual intervention
**Depends on**: Phase 2
**Research**: Unlikely (git hooks are standard)
**Plans**: TBD

Key outcomes:
- post-commit hook installed and working
- Background execution (non-blocking)
- Error handling for failed generations

### Phase 4: Polish
**Goal**: New entries connect to existing lore, personas maintain continuity
**Depends on**: Phase 3
**Research**: Unlikely (existing relationship tools)
**Plans**: TBD

Key outcomes:
- analyze-connections runs on new entries
- Session context preserved between runs
- Chronicle books auto-updated

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Verify Pipeline | 1/1 | **DONE** | 2026-01-05 |
| 2. Quality Prompts | 1/2 | **In progress** | - |
| 3. Auto-trigger | 0/TBD | Not started | - |
| 4. Polish | 0/TBD | Not started | - |
