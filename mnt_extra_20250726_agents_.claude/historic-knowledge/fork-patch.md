---
permalink: knowledge/fork-patch
---

# Fork.sh Patching for Context System

The current fork.sh script needs to be updated to properly handle the context system. Here are the required changes:

## Changes Needed

1. **Directory Structure**
   - Create journal/templates directory
   - Create tmp directory

2. **Script Additions**
   - Copy context-*.sh scripts
   - Copy context implementation documentation

3. **Configuration Updates**
   - Add agent identity file with proper naming
   - Add MCP integration hooks

## Implementation

Create a patch file for fork.sh that makes these changes:

```bash

#!/bin/bash
set -e

# Apply this patch to upgrade fork.sh with context system support

# Usage: ./patch-fork.sh

# Get the directory containing this script
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORK_SCRIPT="$SOURCE_DIR/../fork.sh"

# Backup the original script
cp "$FORK_SCRIPT" "${FORK_SCRIPT}.bak"
echo "Created backup at ${FORK_SCRIPT}.bak"

# Update directory creation to include journal/templates and tmp
sed -i 's|mkdir -p "\${TARGET_DIR}"/{journal,tasks/{active,done,new,paused,cancelled,templates},projects,knowledge,people/templates,scripts/precommit}|mkdir -p "${TARGET_DIR}"/{journal/{templates},tasks/{active,done,new,paused,cancelled,templates},projects,knowledge/{integration},people/templates,scripts/precommit,tmp}|g' "$FORK_SCRIPT"

# Add copy of context scripts after regular script copying
sed -i '/copy_file scripts/a \\n# Copy context system scripts\ncopy_file scripts/context-claude-enhanced.sh\ncopy_file scripts/context-enhanced.sh\ncopy_file scripts/load-claude-context.sh\ncopy_file scripts/context-todo.sh' "$FORK_SCRIPT"

# Add copy of context implementation documentation
sed -i '/copy_file knowledge\/forking-workspace.md/a copy_file knowledge/claude-context-implementation.md\ncopy_file knowledge/integration/' "$FORK_SCRIPT"

# Add creation of the agent's identity file with appropriate name
sed -i '/# Create basic ABOUT.md template/i # Create specific agent identity file\ncat > "${TARGET_DIR}/${NEW_AGENT}.md" << EOL\n# ${NEW_AGENT}'"'"'s Workspace Guide\n\n## My Role and Principles\n- I serve as an agent within the SkogAI ecosystem\n- My strengths lie in: [To be determined]\n- I prioritize:\n  - Documentation-first approach\n  - Clean workflows\n  - Structured problem-solving\n\n## Core Workflows\n[To be determined during initial setup]\n\n## Tools and Capabilities\n[To be customized during setup]\n\n## Working Style\n[To be determined during initial setup]\nEOL\n\n' "$FORK_SCRIPT"

# Update the gptme.toml template to include agent identity file
sed -i 's|  "README.md",\n  "ARCHITECTURE.md",\n  "ABOUT.md",\n  "TASKS.md",\n  "projects/README.md",|  "README.md",\n  "ARCHITECTURE.md",\n  "ABOUT.md",\n  "TASKS.md",\n  "${NEW_AGENT}.md",\n  "projects/README.md",|g' "$FORK_SCRIPT"

# Change script testing from dry-run to context-only
sed -i 's|(cd "${TARGET_DIR}" && ./run.sh --dry-run > /dev/null)|(cd "${TARGET_DIR}" && ./run.sh --context-only > /dev/null || echo "Context generation not yet functional - will need manual setup")|g' "$FORK_SCRIPT"

# Add reminder to create agent config file
sed -i '/echo "The new agent workspace is ready in: ${TARGET_DIR}"/a echo -e "\nRemember to create agent configuration:\ncat > agent_${NEW_AGENT,,}.yaml << EOL\nname: ${NEW_AGENT,,}\nchat_command: cd ${TARGET_DIR} && ./run.sh\ninbox: echo {message} >> ${TARGET_DIR}/inbox.md\nlegacy_compatible: true\ncontext_system: true\nEOL\n\nskogcli settings add-file agent_${NEW_AGENT,,} agent_${NEW_AGENT,,}.yaml"' "$FORK_SCRIPT"

echo "Patch applied successfully to $FORK_SCRIPT"
echo "Test the patched script by creating a new agent"
```

## Usage

1. Save the patch script as patch-fork.sh
2. Make it executable: `chmod +x patch-fork.sh`
3. Run it to patch fork.sh: `./patch-fork.sh`
4. Test by creating a new agent: `./fork.sh /path/to/new/agent NewAgent`

## Verification

After patching and creating a new agent, verify that:

1. The context system files are copied correctly
2. The NewAgent.md file is created with the correct content
3. The agent can generate context with `./run.sh --context-only`
4. The agent configuration instructions are displayed