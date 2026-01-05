# Lore Project - Codebase Analysis

**Generated:** 2026-01-05
**Analysis Method:** Parallel Explore agents (4 concurrent agents)
**Coverage:** Complete repository analysis

## Overview

This directory contains a comprehensive analysis of the Lore project codebase, generated using parallel exploration agents. The analysis covers:

- Technology stack and dependencies
- System architecture and design patterns
- Directory structure and organization
- Code conventions and style standards
- Testing practices and validation
- External integrations
- Technical concerns and known issues

## Documents

### [STACK.md](./STACK.md)
**Languages, frameworks, and dependencies**
- Python 3.12+ (core APIs, agents, orchestrator)
- Bash/Shell (primary operational interface)
- jq (JSON operations)
- Key dependencies: anthropic, openai, requests, streamlit, gradio
- Build tools: uv, pre-commit, argc

### [INTEGRATIONS.md](./INTEGRATIONS.md)
**External APIs and services**
- LLM providers: Ollama (local), OpenRouter (cloud), Anthropic, OpenAI
- Data storage: JSON file-based (no database)
- Git integration for workflow automation
- jq CRUD operations library
- Environment configuration and API keys

### [ARCHITECTURE.md](./ARCHITECTURE.md)
**System design and components**
- Orchestrator layer (session coordination)
- Integration pipeline (5-step lore generation)
- Agent APIs (CRUD operations, LLM integration)
- Shell tools (primary interface)
- Knowledge system (numbered organization)
- Context management (session binding)

### [STRUCTURE.md](./STRUCTURE.md)
**Directory layout and organization**
- Complete directory tree with file counts
- Module organization by layer
- Key locations for data, schemas, tools
- File naming conventions
- Current data volume: 368 entries, 88 books, 53 personas

### [CONVENTIONS.md](./CONVENTIONS.md)
**Code style and naming standards**
- Python: snake_case functions, PascalCase classes
- Shell: kebab-case CLI commands, ALL_CAPS constants
- JSON: timestamp-based naming patterns
- Documentation patterns (docstrings, comments, markdown)
- Path handling standards
- Anti-patterns to avoid

### [TESTING.md](./TESTING.md)
**Testing philosophy and practices**
- Validation-first, schema-driven approach
- Pre-commit hooks for path/syntax validation
- GitHub Actions for integration testing
- Manual testing procedures
- Known testing gaps and recommendations

### [CONCERNS.md](./CONCERNS.md)
**Technical issues and debt**
- 30 identified issues across 8 categories
- 3 critical production blockers (including Issue #6)
- 5 high severity issues
- Security, performance, and scalability concerns
- Immediate action items prioritized
- Production readiness assessment

## Quick Start

### Understanding the System
1. Read [ARCHITECTURE.md](./ARCHITECTURE.md) for high-level system design
2. Check [STRUCTURE.md](./STRUCTURE.md) to navigate the codebase
3. Review [CONVENTIONS.md](./CONVENTIONS.md) before making changes

### Working with the Codebase
1. Check [STACK.md](./STACK.md) for dependencies
2. Review [INTEGRATIONS.md](./INTEGRATIONS.md) for API setup
3. See [TESTING.md](./TESTING.md) for validation procedures

### Addressing Issues
1. Review [CONCERNS.md](./CONCERNS.md) for known issues
2. Check Priority 0 items (critical blockers)
3. See immediate action items for fixes

## Key Findings

### Strengths
- ✅ Well-documented (CLAUDE.md is canonical)
- ✅ Clear separation of concerns (layered architecture)
- ✅ Schema-driven validation (JSON schemas as contracts)
- ✅ Shell tools are primary, stable interface
- ✅ Pre-commit hooks prevent bad commits
- ✅ Multiple LLM provider support (ollama, claude, openai)

### Critical Issues
- ❌ **Issue #6:** Pipeline creates entries with empty content (line 263 typo)
- ❌ Variable interpolation without escaping (security risk)
- ❌ No file locking (multi-user data loss risk)

### High Priority Concerns
- ⚠️ No schema validation in pipeline
- ⚠️ Temporary file race conditions
- ⚠️ Duplicate `run_llm()` implementations (6 copies)
- ⚠️ Inconsistent error handling

## Production Readiness

| Scenario | Status | Notes |
|----------|--------|-------|
| **Single-user manual workflows** | ✅ Ready | Direct tool usage works well |
| **Automated pipelines** | ❌ Not ready | Issue #6 blocks auto-generation |
| **Multi-user scenarios** | ⚠️ At risk | No file locking, race conditions |
| **Current scale (1.2k entries)** | ✅ Ready | Performance acceptable |
| **Future scale (10k+ entries)** | ❌ Not ready | Need pagination, indexing |

## Current State (2026-01-05)

**Data Volume:**
- 368 lore entries
- 88 lore books
- 53 active personas
- 13 active session contexts
- 5 archived session contexts

**Verified Working:**
- ✅ lore-flow.sh pipeline (5 steps)
- ✅ All 3 LLM providers
- ✅ Shell tool CRUD operations
- ✅ argc CLI coverage
- ✅ Session context tracking

**Known Blockers:**
- Issue #5: LLM meta-commentary (workaround exists)
- Issue #6: Empty content in pipeline (critical fix needed)

## Immediate Actions Required

### Fix Now (Priority 0)
1. Fix variable typo in `integration/lore-flow.sh:263`
2. Add explicit error checking after ID extraction
3. Use `mktemp` for secure temp file creation

### Fix This Week (Priority 1)
4. Add schema validation in pipeline
5. Implement file locking
6. Fix variable escaping in Python interpolation
7. Consolidate duplicate `run_llm()` functions

See [CONCERNS.md](./CONCERNS.md) for complete priority list.

## Analysis Methodology

This codebase map was generated using the `/skogai:map-codebase` command with 4 parallel Explore agents:

1. **Agent 1:** Stack + Integrations (technology focus)
2. **Agent 2:** Architecture + Structure (organization focus)
3. **Agent 3:** Conventions + Testing (quality focus)
4. **Agent 4:** Concerns (issues focus)

Each agent analyzed the codebase independently with fresh context, ensuring comprehensive coverage without token limitations.

## Maintenance

**Update Frequency:** Run `/skogai:map-codebase` when:
- Significant architectural changes occur
- Major refactoring is completed
- New components are added
- Documentation becomes stale

**Last Updated:** 2026-01-05
**Next Review:** After Issue #6 fix and file locking implementation

## References

- **Main Documentation:** `/home/skogix/lore/CLAUDE.md`
- **Current Understanding:** `/home/skogix/lore/docs/CURRENT_UNDERSTANDING.md`
- **System Map:** `/home/skogix/lore/docs/SYSTEM_MAP.md`
- **GitHub Repository:** https://github.com/SkogAI/lore
- **GitHub Issues:** https://github.com/SkogAI/lore/issues

## Notes

This analysis provides a snapshot of the codebase at a specific point in time. Always refer to the actual code and CLAUDE.md for the most current information.

The analysis focuses on **what exists** (structure, patterns, issues) rather than **what should exist** (recommendations, roadmap). For future planning, see project documentation in `/home/skogix/lore/docs/`.
