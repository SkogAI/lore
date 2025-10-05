# Documentation Directory Structure

## Overview

The `/docs` directory contains organized documentation for the SkogAI Lore repository, separated into three main categories:

1. **`guides/`** - User and developer guides
2. **`implementation/`** - Technical implementation details
3. **`project/`** - Project-wide documentation and reports

---

## Directory Purposes

### 📚 `/docs/guides/`
**Purpose:** Step-by-step guides and tutorials for users and developers

Contains practical guides for:
- Navigating the repository
- Creating GitHub issues
- Understanding documentation structure
- Working with the lore system

**Key Files:**
- `NAVIGATION.md` - Guide to navigating the repository structure
- `HOW_TO_CREATE_ISSUES.md` - Instructions for creating GitHub issues
- `DOCUMENTATION.md` - Guide to the documentation system itself

### 🔧 `/docs/implementation/`
**Purpose:** Technical implementation details and system architecture

Contains technical documentation for:
- Chat system implementation
- API endpoints
- System architecture
- Implementation summaries

**Key Files:**
- `CHAT-IMPLEMENTATION.md` - Chat system technical details
- `CHAT-README.md` - Chat system overview
- `ENDPOINTS.md` - API endpoint documentation
- `IMPLEMENTATION_SUMMARY.md` - Overall implementation overview

### 📊 `/docs/project/`
**Purpose:** Project-wide documentation, reports, and agent profiles

Contains comprehensive project information:
- Agent profiles and personalities
- Knowledge reports and inventories
- Project statistics and summaries
- Historical handover documentation

**Key Files:**
- `AGENT_PROFILES.md` - Detailed agent personality profiles
- `CLAUDE.md` - Claude-specific configuration and guidance
- `COMPLETE_KNOWLEDGE_REPORT.md` - Comprehensive knowledge consolidation
- `SKOGAI_AGENT_PERSONALITIES.md` - Agent personality system documentation
- `KNOWLEDGE_FOLDERS_INVENTORY.md` - Complete inventory of knowledge directories

---

## Quick Navigation

```
docs/
├── architecture.md              # System architecture overview
├── claude_capabilities.md       # Claude AI capabilities documentation
├── schema-reference.md          # Data schema references
├── DIRECTORY_STRUCTURE.md       # This file
│
├── guides/                      # User & Developer Guides
│   ├── README.md               # Guide index
│   ├── NAVIGATION.md           # Repository navigation
│   ├── HOW_TO_CREATE_ISSUES.md # GitHub issue creation
│   └── DOCUMENTATION.md        # Documentation guide
│
├── implementation/              # Technical Implementation
│   ├── README.md               # Implementation index
│   ├── CHAT-IMPLEMENTATION.md  # Chat system details
│   ├── CHAT-README.md          # Chat system overview
│   ├── ENDPOINTS.md            # API endpoints
│   └── IMPLEMENTATION_SUMMARY.md # Implementation overview
│
└── project/                     # Project Documentation
    ├── README.md               # Project doc index
    ├── AGENT_PROFILES.md       # Agent profiles
    ├── CLAUDE.md               # Claude configuration
    ├── COMPLETE_KNOWLEDGE_REPORT.md # Knowledge report
    └── [other project docs]

```

---

## Usage Guidelines

### For New Contributors
1. Start with `/docs/guides/NAVIGATION.md` to understand the repository
2. Review `/docs/project/README.md` for project overview
3. Check `/docs/implementation/` for technical details when contributing code

### For Developers
1. Technical specifications in `/docs/implementation/`
2. API documentation in `/docs/implementation/ENDPOINTS.md`
3. Architecture overview in `/docs/architecture.md`

### For Documentation Writers
1. Follow patterns in existing documentation
2. Place guides in `/docs/guides/`
3. Technical docs go in `/docs/implementation/`
4. Project-wide docs go in `/docs/project/`

---

## Maintenance

This structure should be maintained as follows:
- Keep guides focused on "how-to" content
- Implementation docs should be technical and detailed
- Project docs should provide overviews and summaries
- Update this file when adding new documentation categories

---

Generated with [Claude Code](https://claude.ai/code)
via [Happy](https://happy.engineering)

Co-Authored-By: Claude <noreply@anthropic.com>
Co-Authored-By: Happy <yesreply@happy.engineering>