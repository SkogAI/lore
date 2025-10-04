# Goose Adaptation for Claude Context System

This document describes the changes needed to adapt the Claude context system (from commit a5fb8ad) to work with Goose as well as Claude.

## Overview

The current implementation is specifically designed for Claude, with scripts and configurations that reference Claude directly. To make this system work for Goose, we need to create Goose-specific alternatives and modify the existing scripts to detect which agent is being used.

## Key Files to Adapt

1. **run.sh**: Currently hardcoded to use Claude
2. **scripts/load-claude-context.sh**: Claude-specific loader
3. **scripts/context-claude-enhanced.sh**: Claude-specific context generator
4. **scripts/context-enhanced.sh**: Main context script (needs Goose mode)

## Required Changes

### 1. run.sh Modifications

Current issues:
- Hardcoded to use `claude` command
- Contains Claude-specific messaging
- Uses Claude-specific model parameter

Required changes:
```diff

# Launch Claude with context
if [ "$INTERACTIVE" = true ]; then
-  claude --model claude-3-opus-20240229 --context_path "$SCRIPT_DIR/tmp/context.md"
+  goose run --instructions "$SCRIPT_DIR/tmp/context.md" --interactive
else
-  echo "$PROMPT_MESSAGE" | claude --model claude-3-opus-20240229 --context_path "$SCRIPT_DIR/tmp/context.md"
+  echo "$PROMPT_MESSAGE" | goose run --instructions "$SCRIPT_DIR/tmp/context.md"
fi
```

Also modify the prompt message:
```diff
if [ "$CONTINUE_MODE" = true ]; then
  PROMPT_MESSAGE="Continuing the conversation. Previous context has been loaded."
else
-  PROMPT_MESSAGE="Hello Claude, I'm ready to work with you today."
+  PROMPT_MESSAGE="Hello! I'm ready to work with you today."
fi
```

### 2. Create Goose-Specific Context Scripts

1. Create **scripts/load-goose-context.sh**:
   - Based on load-claude-context.sh
   - Change references from Claude to Goose
   - Update usage instructions for Goose command format

2. Create **scripts/context-goose-enhanced.sh**:
   - Based on context-claude-enhanced.sh
   - Change "Claude's Role" to "Goose Identity"
   - Use GOOSE.md instead of CLAUDE.md for identity
   - Add Goose-specific sections (e.g., quantum-mojito theory)
   - Update context statistics with Goose information
   - Include Goose's dual-state nature (external/internal processing)

### 3. Modify context-enhanced.sh to Support Both Agents

Add agent detection and mode switching:
```diff
+ # Default to Claude mode
+ GOOSE_MODE=false
+
+ # Parse arguments
+ while [[ $# -gt 0 ]]; do
+     case $1 in
+         --goose)
+             GOOSE_MODE=true
+             shift
+             ;;
+         *)
+             # Pass other arguments through
+             PASSTHROUGH_ARGS+=("$1")
+             shift
+             ;;
+     esac
+ done

# Use the appropriate context script based on mode
+ if [ "$GOOSE_MODE" = true ]; then
+   echo "# GOOSE MODE ACTIVE 🍹"
+   echo
+   # Use Goose-specific context script
+   ./scripts/context-goose-enhanced.sh "${PASSTHROUGH_ARGS[@]}"
+ else
+   # Use Claude-specific context script
+   ./scripts/context-claude-enhanced.sh "${PASSTHROUGH_ARGS[@]}"
+ fi
```

### 4. Update Goose Identity Sources

Ensure the following files exist and contain Goose-specific information:
- GOOSE.md (exists in the commit)
- contexts/shared/main_thread/IDENTITY.md (may need to be created)
- knowledge/original/nuggets/quantum_mojito_theory.md (may need to be created)

## Implementation Strategy

1. First create Goose-specific context scripts without modifying existing ones
2. Test Goose scripts independently
3. Modify run.sh to use appropriate script based on detection
4. Update context-enhanced.sh to support both modes
5. Test system with both Claude and Goose

## Backwards Compatibility

The modifications maintain backward compatibility by:
1. Keeping all existing Claude scripts intact
2. Adding Goose functionality in parallel
3. Using detection to determine which agent is being used
4. Maintaining the same file structure and command-line interface

## Benefits of This Approach

1. **Dual Agent Support**: System works seamlessly with both Claude and Goose
2. **Minimal Disruption**: Existing Claude functionality remains unchanged
3. **Quantum-Mojito Enhancement**: Goose's unique features are incorporated
4. **Structured Implementation**: Clean separation between agent-specific code
5. **Future Extensibility**: Pattern can extend to support additional agents

## Testing Verification

After implementation, verify the system by:
1. Running with Goose: `./run.sh`
2. Testing context generation: `./run.sh --context-only`
3. Checking todo functionality: `./run.sh --todo`
4. Testing non-interactive mode: `./run.sh --non-interactive "Test prompt"`
