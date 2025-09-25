# Unix Exit Codes: Don't Reinvent the Wheel

## The Unix Standard

**"Every system in the history of Linux uses shell exit codes and warnings. Almost NONE of the systems today use 'Claude's helpful error messages'"**

## Standard Exit Code Pattern

### Basic Pattern:
- **0** = Success
- **1** = General failure
- **2** = Misuse of shell command
- **126** = Command cannot execute
- **127** = Command not found
- **128+n** = Signal n received

### How Unix Tools Use This:

```bash

# These tools follow exit code standards
cat file.txt && echo "Success" || echo "Failed"
ls /nonexistent 2>/dev/null; echo $?  # Returns 2
grep "pattern" file.txt; echo $?       # Returns 1 if no match
```

## Wrong Approach: Custom Error Handling

### DON'T DO THIS:
```bash
if [[ ! -f "$file" ]]; then
    echo "ERROR: File '$file' not found at path $PWD"
    echo "Please check the file exists and try again"
    echo "Valid files are: $(ls -1)"
    exit 1
fi
```

### Problems:
1. **Information disclosure** - Leaks filesystem details
2. **Verbose output** - Breaks Unix composition patterns
3. **Custom behavior** - Doesn't follow established patterns
4. **Reinventing wheels** - Unix already handles this

## Right Approach: Use Unix Standards

### DO THIS INSTEAD:
```bash

# Let cat handle the error reporting via exit codes
cat "$file" 2>/dev/null || exit 1

# Or even simpler - let the shell handle it
cat "$file"
```

### Benefits:
1. **Standard behavior** - Works like all Unix tools
2. **Composable** - Fits Unix pipe/redirect patterns
3. **Secure** - No information disclosure
4. **Simple** - Less code, fewer bugs

## Real Examples

### Standard Unix Tools Pattern:
```bash

# All these tools use exit codes, not verbose messages
cat nonexistent.txt    # Silent failure, exit code 1
ls /invalid/path       # Minimal stderr, exit code 2
grep "missing" file    # No match, exit code 1
cp src dest           # Permission denied, exit code 1
```

### Testing Exit Codes:
```bash

# Proper way to handle errors in scripts
if ! cat "$file" 2>/dev/null; then
    exit 1  # Let caller handle the error appropriately
fi

# Or use short-circuit evaluation
cat "$file" 2>/dev/null || exit 1
```

## Why This Matters

### Unix Philosophy:
1. **Do one thing well** - Tools handle their own error reporting
2. **Composability** - Exit codes work with all shell constructs
3. **Standardization** - Consistent behavior across all tools
4. **Simplicity** - Less custom code means fewer bugs

### Modern Systems:
- systemd uses exit codes for service status
- Container orchestrators check exit codes
- CI/CD pipelines depend on exit codes
- Monitoring systems alert on non-zero exits

## Implementation Rule

**When tools fail, use standard Unix exit codes and let the calling context decide how to handle errors.**

Don't reinvent error handling that Unix has standardized for 50+ years.