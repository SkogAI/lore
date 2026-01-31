# INTEGRATION

Automated pipelines transforming work sessions into narrative lore.

## OVERVIEW

Orchestrates git commits → persona selection → LLM narrative → lore storage. The bridge between technical activity and mythology.

## STRUCTURE

```
integration/
├── lore-flow.sh             # Main pipeline (git → lore)
├── orchestrator-flow.sh     # Alternative orchestration
├── persona-mapping.conf     # Git author → persona mapping
├── persona-bridge/          # Persona context loading
│   └── persona-manager.py   # Load/render persona prompts
├── services/                # Service configurations
└── workflows/               # Workflow scripts
    └── test-workflow.sh     # Integration tests
```

## WHERE TO LOOK

| Task | File | Notes |
|------|------|-------|
| Generate from git | `lore-flow.sh git-diff HEAD` | Main pipeline |
| Manual lore input | `lore-flow.sh manual "description"` | Direct input |
| From log file | `lore-flow.sh log /path/to/file` | Extract from logs |
| Map author → persona | `persona-mapping.conf` | Configure mappings |
| Load persona context | `persona-bridge/persona-manager.py` | Python API |

## PIPELINE FLOW

```
Git Commit/Log/Manual
        ↓
[1] Extract Content (git diff + commit message + author)
        ↓
[2] Select Persona (author → persona-mapping.conf → fallback DEFAULT)
        ↓
[3] Load Persona Context (persona-manager.py --render-prompt)
        ↓
[4] Generate Narrative (llama-lore-integrator.sh extract-lore)
        ↓
[5] Create & Store (manage-lore.sh create-entry + link to persona chronicle)
        ↓
Lore Entry Saved!
```

## CONVENTIONS

**persona-mapping.conf:**
```bash
skogix=persona_1744992765      # Amy Ravenwolf
other-author=persona_XXXXX
DEFAULT=persona_1763820091     # Village Elder (fallback)
```

**PersonaManager Usage:**
```python
from integration.persona_bridge.persona_manager import PersonaManager
manager = PersonaManager()
prompt = manager.render_persona_prompt("persona_123")
context = manager.get_persona_lore_context("persona_123")
```

**CLI:**
```bash
python3 persona-bridge/persona-manager.py --list
python3 persona-bridge/persona-manager.py --persona persona_123 --render-prompt
```

## ANTI-PATTERNS

| DO NOT | Why |
|--------|-----|
| Skip persona mapping | Unmapped authors get generic Village Elder voice |
| Generate without persona context | Content lacks consistent voice/traits |
| Modify archived lore | Historical preservation is critical |

## COMMANDS

```bash
# Main pipeline
./lore-flow.sh manual "Amy implemented quantum mojito generator"
./lore-flow.sh git-diff HEAD
./lore-flow.sh git-diff HEAD~3

# Persona management
python3 persona-bridge/persona-manager.py --list
python3 persona-bridge/persona-manager.py --persona persona_123 --get-name

# Test workflow
./workflows/test-workflow.sh
```

## NOTES

**Output Example:**
```
=== Lore Generation Complete ===
Entry ID: entry_1764315234_a4b3c2d1
Persona: Amy Ravenwolf (persona_1744992765)
Chronicle: book_1764315000
Session: 1764315234
```

**Automation:** Add to `.git/hooks/post-commit`:
```bash
#!/bin/bash
./integration/lore-flow.sh git-diff HEAD &
```

**Known Issue #6:** Pipeline creates entries with empty content field - use `llama-lore-creator.sh` directly as workaround.
