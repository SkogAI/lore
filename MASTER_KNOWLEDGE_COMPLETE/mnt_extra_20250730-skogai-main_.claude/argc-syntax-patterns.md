# argc Syntax Patterns

## Proper argc Option Declaration Syntax

### Default Values for Options

**CORRECT** - argc annotation syntax:
```bash

# @option --format[=summary|full] The output format
```

**WRONG** - bash parameter expansion:
```bash
local format="${argc_format:-summary}"
```

### Environment Variable Declaration

**CORRECT** - argc @env syntax:
```bash

# @env SKOGAI_DOCS The path to SkogAI documentation directory
```

**WRONG** - hardcoded paths:
```bash
local docs_path="/home/skogix/SkogAI/docs/official"
```

## Key Principles

1. **Use argc framework syntax** - Don't mix bash parameter expansion with argc
2. **Document environment expectations** - Use @env declarations
3. **Let argc handle defaults** - Use bracket notation `[=default|option]`
4. **Avoid bash hacks** - Use proper framework patterns

## Real Example from librarian tools.sh

### Before (wrong):
```bash
local format="${argc_format:-summary}"
```

### After (correct):
```bash

# @option --format[=summary|full] The output format

# Then use $argc_format directly in the function
```

The argc framework handles the default value assignment automatically when using the proper annotation syntax.