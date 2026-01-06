# Lore Project - Codebase Analysis

**Generated:** 2026-01-05
**Coverage:** Complete repository analysis

## Overview

This directory contains a comprehensive analysis of the Lore project codebase. The Lore system transforms work sessions (git commits, code changes, chat logs) into mythological narrative entries stored as JSON, creating persistent memory for AI agents across sessions.

**Core Philosophy:** "Automate EVERYTHING so we can drink mojitos on a beach"

## Quick Navigation

| Document | Purpose | Start Here If... |
|----------|---------|------------------|
| [ARCHITECTURE.md](./ARCHITECTURE.md) | System design, data flow, components | Understanding how things work |
| [STRUCTURE.md](./STRUCTURE.md) | Directory layout, file organization | Finding where code lives |
| [CONVENTIONS.md](./CONVENTIONS.md) | Code style, patterns, best practices | Writing new code |
| [CONCERNS.md](./CONCERNS.md) | Technical debt, bugs, issues | Fixing problems |
| [INTEGRATIONS.md](./INTEGRATIONS.md) | External APIs, LLM providers | Setting up environment |
| [TESTING.md](./TESTING.md) | Test practices, coverage | Adding tests |
| [STACK.md](./STACK.md) | Languages, dependencies | Understanding tech choices |

## Key Findings

### Strengths
- Well-documented (CLAUDE.md is canonical)
- Clear separation of concerns (layered architecture)
- Schema-driven validation (JSON schemas as contracts)
- Shell tools are primary, stable interface
- Pre-commit hooks prevent bad commits
- Multiple LLM provider support (ollama, claude, openai)
- Comprehensive jq transformation tests (100+ tests)

### Critical Issues
- **Issue #6:** Pipeline creates entries with empty content (line 263 typo)
- Variable interpolation without escaping (security risk)
- No file locking (multi-user data loss risk)

### High Priority Concerns
- No schema validation in pipeline
- Temporary file race conditions
- Duplicate `run_llm()` implementations (6 copies)
- Inconsistent error handling

## Production Readiness

| Scenario | Status | Notes |
|----------|--------|-------|
| **Single-user manual workflows** | Ready | Direct tool usage works well |
| **Automated pipelines** | Not ready | Issue #6 blocks auto-generation |
| **Multi-user scenarios** | At risk | No file locking, race conditions |
| **Current scale (1.2k entries)** | Ready | Performance acceptable |
| **Future scale (10k+ entries)** | Not ready | Need pagination, indexing |

## Current State (2026-01-05)

**Data Volume:**
- 1,202 lore entries
- 107 lore books
- 92 personas
- 13 active session contexts
- 5 archived session contexts

**Verified Working:**
- lore-flow.sh pipeline (5 steps)
- All 3 LLM providers (claude, openai, ollama)
- Shell tool CRUD operations
- argc CLI coverage
- Session context tracking

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

See [CONCERNS.md](./CONCERNS.md) for complete priority list with 38 identified issues.

## Issue Summary

| Category | Count | Severity |
|----------|-------|----------|
| Critical Issues | 3 | Production blocker |
| High Severity | 8 | Must fix before scale |
| Medium Severity | 4 | Quality issues |
| Architectural Debt | 4 | Maintenance burden |
| Known Bugs | 2 | Blocks auto-generation |
| Security | 3 | Exploit risk |
| Scalability | 3 | Blocks 10k+ entries |
| Features | 5 | Incomplete system |
| Quality | 3 | Hard to debug |
| Documentation | 3 | Operational risk |
| **TOTAL** | **38** | |

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

## References

- **Main Documentation:** `/home/skogix/lore/CLAUDE.md`
- **Current Understanding:** `/home/skogix/lore/docs/CURRENT_UNDERSTANDING.md`
- **System Map:** `/home/skogix/lore/docs/SYSTEM_MAP.md`
- **GitHub Repository:** https://github.com/SkogAI/lore
- **GitHub Issues:** https://github.com/SkogAI/lore/issues

## Maintenance

**Update this analysis when:**
- Significant architectural changes occur
- Major refactoring is completed
- New components are added
- Documentation becomes stale

**Last Updated:** 2026-01-05
