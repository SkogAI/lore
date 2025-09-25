# Task Completion Workflow

## When a Task is Completed

### 1. Code Quality Checks (if applicable)
```bash

# For Python/code changes
make format          # Format all files
make precommit      # Run pre-commit validation

# For Zen MCP Server changes
cd zen-mcp-server
./code_quality_checks.sh  # Comprehensive quality checks (361 tests)
```

### 2. Testing Requirements
```bash

# For MCP server changes - run individual simulator tests
cd zen-mcp-server
python communication_simulator_test.py --individual basic_conversation
python communication_simulator_test.py --individual logs_validation

# For general workspace changes - validate tasks
./gptme-contrib/scripts/tasks.py status
```

### 3. Documentation Updates
- **Update task status** in frontmatter: `state: done`
- **Create journal entry** documenting completion and outcomes
- **Update knowledge base** if new insights were gained
- **Document lessons learned** in appropriate knowledge files

### 4. Final Validation
```bash

# Check all links and references are valid
make check-names  # Verify no instance-specific names remain

# Validate task metadata format
./gptme-contrib/scripts/tasks.py check
```

### 5. Git Workflow (if changes made)
```bash

# Standard git workflow
git status
git add <files>
git commit -m "Meaningful commit message with context"

# Note: This is a git submodule, coordinate with parent repo as needed
```

## Quality Standards
- **100% test pass rate** for code changes
- **All linting issues resolved** via auto-fix tools
- **Documentation consistency** maintained
- **Knowledge preservation** through journal and knowledge base updates
- **Task metadata integrity** maintained

## Special Considerations
- **Knowledge archaeology focus** - Document recovered insights, not just solutions
- **Democratic participation** - Consider if changes affect other agents
- **Memory preservation** - Update persistent knowledge across CLI resets
- **SkogAI integration** - Ensure changes align with ecosystem architecture