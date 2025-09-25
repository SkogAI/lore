# Basic message structure
.role + ": " + .content

# Messages with thinking blocks
select(.content | test("<thinking>.*</thinking>"))

# Messages with tool commands
select(.content | test("```(shell|ipython|save|append|patch|morph|tmux)"))

# Messages with multiple code blocks
select(.content | test("```.*```.*```"))

# Pure text responses (no markup)
select(.content | test("^[^<`*#]") and (contains("<thinking>") | not) and (contains("```") | not))

# Mixed content (thinking + tools)
select(.content | test("<thinking>") and test("```"))

# Messages with markdown formatting
select(.content | test("\\*\\*|__|##|\\[|\\]"))

# System messages
select(.role == "system")

# Extract all unique tool types
select(.content | match("```([a-z]+)").captures[0].string) | unique

# Count message types
group_by(.role) | map({key: .[0].role, count: length})
