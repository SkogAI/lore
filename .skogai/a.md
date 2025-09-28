Here’s a concise, practical overview of the project with a dependency map and a suggested
split into smaller parts.

Overview

- Purpose: A knowledge/lore + agent orchestration system. It combines: - Small local-model agents via Ollama for content workflows (research → outline →
  writing). - A lore and persona management layer (JSON-backed, CLI + Python API). - Prototype chat UI (Gradio/Streamlit) for interacting with local or API models. - Documentation and architecture drafts for a fuller orchestrator (“Goose”) and multi-
  agent variants.

Core Modules and Responsibilities

- Small Model Agents (Ollama) - File: agents/implementations/small_model_agents.py - Functionality: - Wraps local LLMs (“llama3.\*”) to run specialized agents: research, outline,
  writing. - Provides prompt templates, context formatting, and response extraction helpers. - Dependencies: subprocess → ollama run, local prompt dir, simple parsing via regex. - Used by: demo/small_model_workflow.py, skogai-agent-small-service.sh
- Agent API (API-based content agents) - File: agents/api/agent*api.py - Functionality: - High-level workflow logic per phase (research/outline/writing). - Builds prompts, calls OpenAI-compatible chat endpoint, parses JSON structure,
  persists per-session artifacts under demo/content_creation*<session>. - Dependencies: requests (OpenAI-style API), config path, environment for API key. - Used by: standalone (example in main), intended for orchestrator integration.
- Lore/Persona API - File: agents/api/lore_api.py - Functionality: - Create/read/list lore entries, lore books, personas as JSON files. - Link entries to books and books to personas; search and import lorebooks; gather
  persona context. - Dependencies: Local filesystem (knowledge/expanded/\*), JSON schemas in knowledge/core/
  persona|lore. - Used by: st-lore-export.py, tools/manage-lore.sh, tools/create-persona.sh, llama lore
  tools.
- Lore CLI Tools - Files: - tools/manage-lore.sh: list/create/show/add-to-book/link-to-persona/search - tools/create-persona.sh: create/list/show/edit/delete personas - tools/llama-lore-creator.sh: generate entries/books/personas using Ollama;
  integrate with manage-lore.sh and create-persona.sh - tools/llama-lore-integrator.sh: import/extract/analyze (not fully reviewed here
  but referenced) - Dependencies: jq, Ollama (for generation), filesystem paths under knowledge/expanded/
  \*.
- Chat UI - File: skogai-chat.py (Gradio) - Functionality: - Unified chat UI supporting local Ollama and API (Anthropic, OpenAI) models. - System prompts, temperature, persistence of history and settings, save/load chat
  logs. - Dependencies: gradio, requests, local config dir ~/.config/skogai-chat, Ollama
  endpoint. - Note: ENDPOINTS.md suggests moving chat files to a separate repo (../skogchat). Also a
  Streamlit variant indicated by CHAT-IMPLEMENTATION.md and start-chat-ui.sh.
- Demos and Services - demo/small_model_workflow.py: End-to-end 3-phase content generation using
  SmallModelAgents. - skogai-agent-small-service.sh: long-running pipe-based service to run the small model
  workflow on demand. - st-lore-export.py: Export lore to SillyTavern format using LoreAPI (books/persona
  bundles). - integration/\*: shell scripts illustrating planned orchestrator flow/test workflow.
- Documentation - docs/architecture.md: High-level orchestrator/agent/knowledge architecture. - ENDPOINTS.md: Working components checklist and next steps. - SKOGAI_COMPLETE_DOCUMENTATION.md, DOCUMENTATION.md, README.md: System narrative,
  structure, and usage.

Dependency Map (high level)

- Runtime dependencies
  - Ollama: used by small_model_agents.py, llama lore tools, small-agent service, demos.
  - requests/gradio/streamlit: chat UI and AgentAPI (remote LLM).
  - jq, bash tools: CLI management scripts.
- Internal dependencies
  - SmallModelAgents ← demo/small_model_workflow.py, skogai-agent-small-service.sh
  - LoreAPI ← st-lore-export.py, manage-lore.sh (conceptually), create-persona.sh
  - AgentAPI ← intended for orchestrator; standalone usage demonstrated
  - Knowledge schemas (knowledge/core/\*) ← LoreAPI validation loading

Functional Walkthroughs

- Small model content workflow (local LLM)
  - Start: demo/small_model_workflow.py
  - Steps:
    - Research → extract key_facts, concepts
    - Outline → extract structure
    - Writing → extract content sections; save final markdown
  - Inputs: topic; uses SmallModelAgents with ollama run.
  - Outputs: demo/small*model_content*<timestamp>/\*
- Small model service - Start: ./skogai-agent-small-service.sh llama3 - Accepts topics via named pipe; runs the demo workflow per request; logs in logs/;
  saves outputs under demo/small*model_content*\*.
- Lore management (local JSON) - Create/list/show books and entries: tools/manage-lore.sh - Create/list/show/edit personas: tools/create-persona.sh - Generate with LLM: tools/llama-lore-creator.sh uses Ollama to produce content and wire
  it via the CLIs. - Export to SillyTavern: st-lore-export.py uses LoreAPI and writes ST-compatible JSON.
- Chat UI - Local models: uses Ollama /api/generate with formatted history. - API models: OpenAI and Anthropic via requests; settings persisted in ~/.config/skogai-
  chat. - Save/load chat history; quick system prompts.

Proposed Split Into Smaller Parts

- skogai-core (foundation)
  - agents/api/lore_api.py
  - agents/api/agent_api.py
  - knowledge/core/\* (schemas, templates)
  - docs/architecture.md, ENDPOINTS.md
  - Rationale: Stable core APIs and schemas, independent of UI.
- skogai-agents-local (Ollama agents) - agents/implementations/small_model_agents.py - demo/small_model_workflow.py - skogai-agent-small-service.sh - tools/llama-lore-creator.sh, tools/llama-lore-integrator.sh (if Ollama-coupled) - Rationale: All local LLM-driven agent flows grouped, easy to ship for offline/local
  use.
- skogai-lore-cli (JSON-backed tooling)
  - tools/manage-lore.sh
  - tools/create-persona.sh
  - st-lore-export.py
  - Rationale: CLI-first management and exports, depends only on local JSON and jq.
- skogchat (UI) - skogai-chat.py (Gradio) - start-chat-ui.sh, streamlit_chat.py, skogai-chat.desktop, CHAT-IMPLEMENTATION.md - Rationale: Clean UI project that can evolve separately; ENDPOINTS.md already suggests
  this move.
- skogai-orchestrator (future) - orchestrator/, integration/, agents/implementations/content/\*.md, planning/
  implementation variants - Rationale: Experimental/roadmap area for a full “Goose” orchestrator, fed by skogai-
  core APIs.

Recommended Internal Module Boundaries

- APIs and schemas: Keep strict interfaces in agents/api/.py and knowledge/core/
- Local agents: No direct filesystem coupling to lore/personas unless explicitly needed;
  pass context in/out via APIs or defined contracts.
- UI: Treat model providers as pluggable backends; isolate provider code paths.
- CLI tools: Keep shell/JQ utilities in their own package; ensure they use LoreAPI paths
  consistently.

Known Cross-Cutting Dependencies

- Paths: Many scripts hardcode base paths like /home/skogix/skogai or rely on relative ../.
  If splitting repos, introduce config/env vars (e.g., SKOGAI_BASE_DIR) and read them
  consistently in: - agents/api/agent_api.py (config_path) - agents/api/lore_api.py (base_dir) - demos/tools referencing absolute paths
- Model/provider keys: skogai-chat.py expects API keys in settings; AgentAPI reads from env
  or config file.

Quick “Foo does Bar” Cheat Sheet

- SmallModelAgents.run_agent: runs “research|outline|writing” locally via Ollama and returns
  raw text.
- SmallModelAgents.extract\_\*: parses model text into structured JSON for each phase.
- AgentAPI.process_agent_request: builds prompt, calls LLM API, normalizes JSON, persists
  per-phase outputs.
- LoreAPI.create\_\* and list/get/link: CRUD for lore entries/books/personas as JSON files
  under knowledge/expanded.
- manage-lore.sh/create-persona.sh: user-facing shell wrappers around the JSON files; good
  for ops use.
- st-lore-export.py: turns lore books/persona-linked lore into SillyTavern lorebooks.
- skogai-agent-small-service.sh: daemon-style pipe listener that runs the small model
  workflow.
- skogai-chat.py: Gradio chat client for Ollama or remote APIs with history and settings.

If you want, I can:

- Produce a diagram mapping module boundaries and flows.
- Add a config loader to remove hardcoded absolute paths.
- Draft a repo split checklist (folders, README updates, minimal shim scripts).
