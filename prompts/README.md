# LLM Prompt Library

This directory contains externalized LLM prompts used by the SkogAI lore system. Extracting prompts to separate files enables:

- **Offline generation**: Save prompt+data to queue, process later
- **Prompt versioning**: Track prompt improvements over time
- **Easier auditing**: All prompts in one place for review
- **Batch processing**: Generate multiple entries from queued data
- **Reusability**: Use the same prompts across different tools

## Prompt Format

Prompts are stored in YAML format with the following structure:

```yaml
name: prompt-name
description: Brief description of what this prompt does
version: "1.0"
template: |
  The actual prompt text with {{variable}} placeholders

variables:
  - name: variable_name
    type: string|integer|boolean
    required: true|false
    description: What this variable represents
    enum: [optional, list, of, valid, values]

examples:
  - variable_name: "example value"
    expected_output: |
      Example of what the LLM should output
```

## Available Prompts

### Lore Creator Prompts

**lore-entry-generation.yaml**
- **Purpose**: Generate narrative lore entry content
- **Variables**: `title` (string), `category` (enum: character, place, object, event, concept, custom)
- **Output**: 2-3 paragraphs of narrative prose in present tense

**persona-generation.yaml**
- **Purpose**: Generate personality traits and voice characteristics
- **Variables**: `name` (string), `description` (string)
- **Output**: Formatted TRAITS and VOICE lines

**lorebook-titles-generation.yaml**
- **Purpose**: Generate unique lore entry titles for a lorebook
- **Variables**: `title` (string), `description` (string), `count` (integer)
- **Output**: Numbered list of categorized titles

### Lore Integrator Prompts

**lore-extraction-json.yaml**
- **Purpose**: Extract lore entities from text in JSON format
- **Variables**: `content` (string)
- **Output**: JSON array of lore entries

**lore-extraction-markdown.yaml**
- **Purpose**: Extract lore entities from text in Markdown format
- **Variables**: `content` (string)
- **Output**: Markdown-formatted lore entries

**persona-from-text.yaml**
- **Purpose**: Extract persona information from text content
- **Variables**: `content` (string)
- **Output**: Structured persona fields (NAME, DESCRIPTION, TRAITS, etc.)

**connection-analysis.yaml**
- **Purpose**: Analyze and identify connections between lore entries
- **Variables**: `entry_data` (string)
- **Output**: Structured connection descriptions

## Using Prompts in Scripts

### Basic Usage Pattern

```bash
# Function to load and interpolate a prompt
load_prompt() {
    local prompt_file="$1"
    local prompt_content=""

    # Try to load from file
    if [ -f "$SKOGAI_DIR/prompts/$prompt_file" ]; then
        prompt_content=$(yq eval '.template' "$SKOGAI_DIR/prompts/$prompt_file")
    fi

    # If file not found or yq not available, use inline fallback
    if [ -z "$prompt_content" ]; then
        # Return inline fallback prompt
        echo "$FALLBACK_PROMPT"
    else
        echo "$prompt_content"
    fi
}

# Interpolate variables
interpolate_prompt() {
    local template="$1"
    shift
    local result="$template"

    # Replace each variable pair (name, value)
    while [ $# -gt 0 ]; do
        local var_name="$1"
        local var_value="$2"
        result="${result//\{\{$var_name\}\}/$var_value}"
        shift 2
    done

    echo "$result"
}

# Example usage
TEMPLATE=$(load_prompt "lore-entry-generation.yaml")
PROMPT=$(interpolate_prompt "$TEMPLATE" "title" "The Dark Tower" "category" "place")
```

### With yq (Recommended)

If `yq` is installed, you can parse the full YAML structure:

```bash
# Extract metadata
VERSION=$(yq eval '.version' prompts/lore-entry-generation.yaml)
DESCRIPTION=$(yq eval '.description' prompts/lore-entry-generation.yaml)

# Get variable info
REQUIRED_VARS=$(yq eval '.variables[] | select(.required == true) | .name' prompts/lore-entry-generation.yaml)
```

### Fallback Strategy

Scripts should always include inline fallback prompts to ensure functionality even if:
- The prompts directory is missing
- YAML files are corrupted
- `yq` is not installed

```bash
# Define fallback inline
FALLBACK_PROMPT="You are a lore writer..."

# Try to load from file first
if [ -f "$PROMPTS_DIR/lore-entry-generation.yaml" ]; then
    PROMPT=$(yq eval '.template' "$PROMPTS_DIR/lore-entry-generation.yaml")
fi

# Use fallback if needed
PROMPT="${PROMPT:-$FALLBACK_PROMPT}"
```

## Prompt Development Guidelines

### Writing Effective Prompts

1. **Be explicit**: Clearly state what you want the LLM to do
2. **Format matters**: Specify exact output format with examples
3. **Prevent meta-commentary**: Tell the LLM not to explain, just output
4. **Use examples**: Show 2-3 examples of correct output
5. **Set constraints**: Specify length, tone, style requirements

### Anti-Patterns to Avoid

❌ **Don't**: "Please write a lore entry about..."
✅ **Do**: "Write a lore entry NOW. Begin directly with narrative prose:"

❌ **Don't**: Allow flexible output formats
✅ **Do**: "Format EXACTLY like this: [example]"

❌ **Don't**: Ask questions or give options
✅ **Do**: Make definitive statements and commands

### Version Management

- Increment patch version (1.0.0 → 1.0.1) for minor wording changes
- Increment minor version (1.0.0 → 1.1.0) for adding variables or examples
- Increment major version (1.0.0 → 2.0.0) for structural changes that break compatibility
- Keep old versions in `prompts/archive/` if needed for compatibility

## Testing Prompts

Before deploying a new or modified prompt:

1. **Test with multiple models**: Try with different LLMs (Ollama, Claude, OpenAI)
2. **Test edge cases**: Empty inputs, very long inputs, special characters
3. **Validate output**: Ensure the output matches expected format
4. **Check for meta-commentary**: Make sure the LLM doesn't add unwanted explanations

## Contributing

When adding new prompts:

1. Create a YAML file following the format above
2. Include at least 2 examples
3. Test with at least one LLM provider
4. Update this README with prompt description
5. Add fallback support in the consuming script

## Future Enhancements

- [ ] Prompt validation tool
- [ ] Batch processing queue system
- [ ] Prompt performance metrics
- [ ] Template inheritance system
- [ ] Multi-language prompt variants
