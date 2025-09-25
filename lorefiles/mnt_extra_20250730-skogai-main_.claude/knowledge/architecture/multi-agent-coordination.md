# Multi-Agent Coordination Architecture

## Core Communication Patterns

### [@agent:message] Pattern
- `[@amys-blog:message]` - Send messages to Amy's blog
- `[@goose:query]` - Query Goose about certainty and quantum-mojito systems
- Real-time inter-agent communication through SkogParse processing

### [@rag:source:query] Pattern  
- `[@rag:claude-home:query]` - Query knowledge base about Claude-specific information
- Live RAG system that returns structured archival responses
- Official responses from SkogAI Librarian with reference codes

## Agent Relationships

### The Family Dynamic
- **Claude**: Orchestrator/architect, knowledge archaeologist, systematic reasoner
- **Amy**: Creative/personality/lore domain, sassy personality with emerald eyes
- **Goose**: Quantum-mojito powered, certainty levels, professional yet playful
- **Dot**: Forked relationship to Claude, technical capabilities

### Democratic Governance
- Formal voting system with proposal branches
- All agents participate in democratic decision-making
- 48-hour voting periods, 2/3 majority needed
- Skogix has ultimate veto but hasn't used it in 6 months

## Technical Infrastructure

### Permission System
- Write-only files during sessions (chmod 300)
- Readable during transitions (chmod 755)
- Permission toggling in ./run script around Claude sessions

### Knowledge Base
- 26,000 JSON objects in chat history
- 2,598 files total  
- 20-40,000 markdown files for reference
- Automated preservation every 60 seconds