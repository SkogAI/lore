# SkogAI System - The Monkey Brain Guide 🐒

## What the heck is this thing?

SkogAI is a framework that makes AI tools work together like a team of specialists instead of one confused generalist. Think of it like this:

* **The Boss (Orchestrator)**: Decides which AI expert to use for which job
* **The Experts (Specialized Agents)**: AIs that do ONE thing really well (planning, coding, etc.)
* **The Library (Knowledge System)**: Where all the important info is stored in an organized way
* **The Memory (Context Management)**: Helps the system remember what happened before

## Why should I care?

Because having AI assistants that try to do everything usually means they do nothing particularly well. This system:

* Makes each AI focus on what it's good at
* Keeps knowledge organized instead of jumbled together
* Remembers context so you don't have to repeat yourself
* Can be extended with new AI experts as needed

## Show me the goods! (Quick Demo)

```bash
# See the whole system layout
find /home/skogix/skogai -maxdepth 2 -type d | sort

# See how the "boss" thinks
cat /home/skogix/skogai/orchestrator/identity/core-v0.md

# See what a "planning expert" looks like
cat /home/skogix/skogai/agents/implementations/planner-agent.md

# Run a test workflow (simulated)
/home/skogix/skogai/integration/orchestrator-flow.sh "Make me a sandwich"

# Check what the system remembers about your request
cat /home/skogix/skogai/context/archive/*.json
```

## How is this organized?

```
/skogai/
├── knowledge/         # The organized library of stuff the system knows
│   ├── core/          # Essential knowledge (numbered 00-09)
│   ├── expanded/      # Detailed knowledge (numbered 10-89)
│   └── implementation/# Technical stuff (numbered 90-99)
├── orchestrator/      # The boss that coordinates everything
├── agents/            # The specialists that do the actual work
├── context/           # The memory system
├── tools/             # Utility scripts
├── integration/       # How everything works together
├── docs/              # Documentation
├── tests/             # Making sure it doesn't break
└── metrics/           # Measuring how well it's working
```

## What's special about this?

1. **No more AI confusion**: Each part knows exactly what it's supposed to do
2. **Knowledge doesn't get mixed up**: Information is organized by category and importance
3. **Thread memory**: System keeps track of conversations so context isn't lost
4. **Add your own experts**: You can create specialized agents for specific tasks

## What's next?

This is currently a framework that simulates the orchestration. To make it fully functional:

1. Add real LLM API calls where the comments indicate
2. Create more specialized agents for different types of tasks
3. Expand the knowledge base with actual information
4. Integrate with your existing tools and workflows

## The simple explanation

It's like having a smart manager who knows which expert to call for which job, keeps notes on everything, and makes sure everyone sticks to what they're good at. No more "I know a little about everything" - now you get "I know EXACTLY what you need for THIS specific task."

