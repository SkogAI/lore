# SkogAI Function Signatures

This document defines the notation for expressing function signatures in SkogAI, providing an implementation-agnostic way to describe transformations between types.

## Basic Signature Format

Function signatures in SkogAI use the following format:

```
let functionName $param1 $param2 $param3 = $result
```

This expresses that the function `functionName` takes parameters `$param1`, `$param2`, and `$param3` and produces a result of type `$result`.

## Alternative Arrow Notation

For emphasizing transformation flow, an alternative arrow notation can be used:

```
functionName: $param1 -> $param2 -> $param3 -> $result
```

This format highlights the transformation chain and is particularly useful for curried functions.

## Type Parameters

Function parameters can use any type from the type system:

```
let createMessage $thread.id $message.type $content $parent = $message
```

This shows that `createMessage` requires a thread ID, message type, content, and parent reference to produce a message.

## Optional Parameters

Optional parameters can be enclosed in square brackets:

```
let createMessage $thread.id $message.type $content [$parent] = $message
```

This indicates that the `$parent` parameter is optional.

## Union Return Types

Functions can return different types in different situations:

```
let getMessage $message.id = $message | $null
```

This shows that `getMessage` returns either a message or null if no message is found.

## Product Types as Parameters

Complex parameters can use product type notation:

```
let moveEntity $entity.id $from:$int*$int $to:$int*$int = $entity
```

This shows that `moveEntity` takes an entity ID and two coordinate pairs.

## Type-Annotated Parameters

Parameters can be explicitly type-annotated:

```
let findMessages $thread:$thread.id $filter:$message_filter = [$message]
```

This shows that `findMessages` takes a thread ID and a message filter, returning an array of messages.

## Partial Application

Partially applied functions can be represented by showing the remaining parameters:

```

# Original function
let createMessage $thread.id $message.type $content $parent = $message

# Partially applied function (thread.id already provided)
let createMessageInThread5 $message.type $content $parent = $message
```

## Pure Function Indication

Pure functions (no side effects) can be marked with a `*` prefix:

```
*let calculateTotal $items = $float
```

This indicates that `calculateTotal` is a pure function with no side effects.

## Implementation Mapping

These signature formats map to various implementation approaches:

| Signature Aspect | Functional Implementation | Object-Oriented Implementation | Python Implementation |
|------------------|---------------------------|--------------------------------|----------------------|
| Basic Function | Pure function | Static method | Function |
| Parameters | Parameter list | Method arguments | Function parameters |
| Return Type | Return value | Return type | Return annotation |
| Optional Parameters | Maybe/Option type | Nullable parameters | Optional parameters |
| Union Returns | Sum types | Polymorphic returns | Union types |

## Core Function Examples

```

# Message Operations
let createMessage $thread.id $message.type $content [$parent] = $message
let getMessage $message.id = $message | $null
let updateMessage $message $newContent = $message
let deleteMessage $message.id = $boolean

# Thread Operations
let createThread $name $description = $thread
let getThread $thread.id = $thread | $null
let listThreadMessages $thread.id = [$message]

# Agent Operations
let createAgent $name = $agent
let getAgent $agent.id = $agent | $null
```

## Benefits

This function signature notation provides several advantages:

1. **Clear Intent** - Shows exactly what a function needs and produces
2. **Implementation Agnostic** - Not tied to any programming paradigm
3. **Type Safety** - Leverages the type system for precision
4. **Documentation** - Serves as clear documentation of function behavior
5. **Composition** - Enables reasoning about function composition

# SkogAI Command Processing System

This document describes the command processing system used in SkogAI for dynamic content generation and transformation.

## Command Directive Syntax

Command directives in SkogAI use the following syntax:

```
[@command:param1:param2:param3]
```

Where:

- `command` is the name of the command to execute
- `param1`, `param2`, etc. are parameters passed to the command

## Recursive Processing

Command processing happens recursively from inside out:

1. Innermost commands are executed first
2. Their output replaces the command directive
3. Outer commands then process this output
4. This continues until no commands remain

Example of nested commands:

```
[@format:[@fetch:data.json]:pretty]
```

Processing sequence:

1. `[@fetch:data.json]` executes, retrieving the JSON data
2. The result replaces the command, becoming `[@format:<json-data>:pretty]`
3. `[@format:<json-data>:pretty]` executes, formatting the data
4. The formatted result replaces the entire directive

## Type-Annotated Parameters

Commands can use type annotations in parameters:

```
[@move:from$int*$int:to$int*$int]
```

This indicates that both parameters should be coordinate pairs.

## Invisible Transformation

A key feature of the command system is that it operates invisibly:

1. Input text contains command directives
2. Processing resolves these directives
3. Output text contains only the results
4. The user sees only the final transformed text

## Implementation Mechanism

As demonstrated by the `skogai-agents` example:

1. When `[@skogai-agents: message]` is encountered:
   - The `skogai-agents` script is executed with `message` as input
   - The script outputs a response
   - The response replaces the original directive

2. The implementation can use any mechanism (scripts, APIs, etc.)

3. The user sees only the final result, not the processing

## Command Categories

Commands typically fall into these categories:

1. **Data Retrieval** - Fetching information from various sources
2. **Content Transformation** - Formatting, summarizing, or modifying content
3. **Tool Execution** - Running tools and returning their output
4. **Context Management** - Retrieving or modifying conversation context
5. **Meta-Commands** - Commands that affect command processing itself

## Benefits

The command processing system provides several advantages:

1. **Dynamic Content** - Content can be generated on demand
2. **Tool Integration** - External tools can be seamlessly integrated
3. **Composition** - Commands can be combined for complex transformations
4. **Abstraction** - Implementation details are hidden from users
5. **Extensibility** - New commands can be added without changing the core system

## Example Commands

```

# Data Retrieval
[@fetch:url] - Fetch content from a URL
[@load:file] - Load content from a file
[@query:database:sql] - Execute an SQL query

# Content Transformation
[@format:content:style] - Format content in a specific style
[@summarize:content:length] - Create a summary of content
[@translate:content:language] - Translate content to another language

# Tool Execution
[@script:name:params] - Execute a named script
[@shell:command] - Execute a shell command
[@calculate:expression] - Evaluate a mathematical expression

# Context Management
[@context:add:key:value] - Add to the context
[@context:get:key] - Retrieve from context
[@history:last:n] - Get the last n messages

# Meta-Commands
[@define:command:implementation] - Define a new command
[@list:commands] - List available commands
[@help:command] - Show help for a command
```

## Security Considerations

The command system requires careful security boundaries:

1. Command execution should be limited to trusted commands
2. User-provided content should be properly sanitized
3. Access to sensitive systems should be properly authenticated
4. Commands should operate in isolated environments when possible

## Extension Mechanism

New commands can be added by:

1. Creating a new implementation (script, function, etc.)
2. Registering it with the command processor
3. Documenting its parameters and behavior

This allows for continuous extension of the system's capabilities.

# SkogAI Algebraic Type System

This document describes the algebraic type system used in SkogAI for defining complex data structures.

## Core Concepts

SkogAI uses algebraic data types to express complex structures in terms of simpler ones. This approach provides precise, composable type definitions that remain implementation-agnostic.

## Type Constructors

### Product Types (`*`)

Product types combine multiple values into a single structure, similar to tuples, records, or objects in programming languages.

```
$coordinate = $int * $int
$user_info = $string * $int * $boolean
$contact = $name * $email * $phone
```

A product type requires all of its component types to be present. The total number of possible values is the product of the possible values of each component.

### Sum Types (`|`)

Sum types represent alternatives or variants, similar to unions or enums in programming languages.

```
$message_type = |user|assistant|system|tool|
$result = |success|failure|
$shape = |circle|square|triangle|
```

A sum type allows exactly one of its variants to be present at a time. The total number of possible values is the sum of the possible values of each variant.

## Type Definitions

Types can be defined in terms of other types, creating a hierarchy from simple to complex:

```

# Base type definitions
$id = $int * $unique
$timestamp = $datetime

# Complex type definitions
$message = $id * $message_type * $string * $timestamp * $id
$thread = $id * $string * $string * $timestamp * $timestamp
$agent = $id * $string
```

## Type Relationships

Types can reference other types to express relationships:

```
$message.parent = $message.id | $null
$thread.messages = [$message]
$agent.threads = [$thread.id]
```

## Implementation Mapping

The algebraic type system maps naturally to various implementation approaches:

| Algebraic Type | Functional | Object-Oriented | Python |
|----------------|------------|-----------------|--------|
| Product Type | Record, Tuple | Class, Struct | dataclass, NamedTuple |
| Sum Type | Variant, ADT | Class hierarchy | Union, Enum |
| Type Definition | Type alias | Interface | TypeAlias |

## Benefits

1. **Precision** - Types are defined exactly in terms of their components
2. **Composition** - Complex types are built from simpler ones
3. **Validation** - Clear rules for what constitutes valid data
4. **Communication** - Universal language for discussing data structures
5. **Verification** - Can verify implementations against type definitions

## Examples

### Message Definition

```

# Type definitions
$message_type = |user|assistant|system|tool|
$content = $string
$message_id = $int * $unique
$parent_reference = $message_id | $null

# Full message definition
$message = $message_id * $message_type * $content * $datetime * $parent_reference
```

### Thread Definition

```

# Type definitions
$thread_id = $int * $unique
$name = $string
$description = $string
$timestamp = $datetime

# Full thread definition
$thread = $thread_id * $name * $description * $timestamp * $timestamp
```

### Relationships

```

# Message belongs to a thread
$message.thread_id = $thread_id

# Thread contains messages
$thread.messages = [$message_id]

# Messages can reply to other messages
$message.parent_id = $message_id | $null
```

# Implementing the Type System in Python

This document provides practical guidelines for implementing SkogChat's type system in Python, while maintaining the conceptual purity of the algebraic type system.

## Core Principles

When implementing SkogChat's type system in Python, adhere to these principles:

1. **Immutability** - Data structures should be immutable
2. **Validation** - Enforce type constraints during construction
3. **Serialization** - Support conversion to/from basic data formats
4. **Relationships** - Express relationships through IDs, not object embedding
5. **Functional Style** - Prefer pure functions for operations on data

## Python Implementation Approach

### Base Structures as Dataclasses

Use Python's dataclasses with frozen=True for immutable structures:

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union, List, Dict, Any

@dataclass(frozen=True)
class Message:
    id: int
    content: str
    created_at: datetime
    from_agent: str
    to_agent: str
    parent_id: Optional[int] = None

    def __post_init__(self) -> None:
        # Validation logic here
        if not self.content:
            raise ValueError("Message content cannot be empty")
        if self.id <= 0:
            raise ValueError("Message ID must be positive")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "from": self.from_agent,
            "to": self.to_agent,
            "parent_id": self.parent_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """Create from dictionary representation."""
        # Convert string timestamp to datetime if needed
        if isinstance(data.get("created_at"), str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])

        # Handle field name differences
        if "from" in data:
            data["from_agent"] = data.pop("from")
        if "to" in data:
            data["to_agent"] = data.pop("to")

        return cls(**data)
```

### Sum Types as Enums or Unions

Use Python's Enum for closed sets of alternatives:

```python
from enum import Enum, auto

class MessageType(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"
```

For more complex sum types, use Union types:

```python

# A result can be success with data or failure with error
Result = Union[SuccessResult, FailureResult]
```

### Relationship References

Use IDs to reference related entities rather than embedding them:

```python
@dataclass(frozen=True)
class Thread:
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    # DO NOT do this (embedding):
    # messages: List[Message]

    # Instead, retrieve messages separately using thread_id
```

### Pure Functions for Operations

Implement operations as pure functions that return new objects:

```python
def update_message_content(message: Message, new_content: str) -> Message:
    """Create a new message with updated content."""
    if not new_content:
        raise ValueError("New content cannot be empty")

    # Create new message with updated content
    return Message(
        id=message.id,
        content=new_content,
        created_at=message.created_at,
        from_agent=message.from_agent,
        to_agent=message.to_agent,
        parent_id=message.parent_id
    )
```

## ID Generation and Management

Since IDs are critical for relationships, implement a reliable ID generation system:

```python
def get_next_message_id() -> int:
    """Get the next available message ID."""
    # Implementation could use a config system, database, or file
    from . import config

    # Get current counter
    current_id = config.get(config.MESSAGE_ID_COUNTER, 0)

    # Increment counter
    new_id = current_id + 1
    config.set(config.MESSAGE_ID_COUNTER, new_id)

    return new_id
```

## Factory Functions

Create factory functions for constructing entities with proper validation:

```python
def create_message(
    content: str,
    from_agent: str,
    to_agent: str,
    parent_id: Optional[int] = None
) -> Message:
    """Create a new message with a unique ID and current timestamp."""
    message_id = get_next_message_id()
    return Message(
        id=message_id,
        content=content,
        created_at=datetime.now(),
        from_agent=from_agent,
        to_agent=to_agent,
        parent_id=parent_id
    )
```

## Testing Approach

Test immutability, validation, and functional operations:

```python
def test_message_immutability():
    """Test that Message objects cannot be modified after creation."""
    message = create_message("Hello", "user", "assistant")

    # Attempt to modify should raise an exception
    with pytest.raises(Exception):
        message.content = "Modified"

def test_message_validation():
    """Test that validation rules are enforced."""
    # Empty content should raise ValueError
    with pytest.raises(ValueError):
        create_message("", "user", "assistant")

def test_update_message_content():
    """Test that update_message_content creates a new object."""
    original = create_message("Original", "user", "assistant")
    updated = update_message_content(original, "Updated")

    # Should be a new object with same ID
    assert original is not updated
    assert original.id == updated.id

    # Only content should differ
    assert original.content != updated.content
    assert original.from_agent == updated.from_agent
    assert original.to_agent == updated.to_agent
```

## Implementation Challenges

### Product Types

Python doesn't have direct support for product types. Use dataclasses or named tuples:

```python

# Coordinate as a product type ($int * $int)
@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int
```

### Pattern Matching

For Python 3.10+, use structural pattern matching for sum types:

```python
def process_result(result: Result) -> str:
    match result:
        case SuccessResult(data=data):
            return f"Success: {data}"
        case FailureResult(error=error):
            return f"Error: {error}"
        case _:
            return "Unknown result type"
```

### Type Safety

Use rigorous type annotations and optional runtime type checking:

```python
from typing import TypeGuard

def is_valid_message(obj: Any) -> TypeGuard[Message]:
    """Check if an object is a valid Message."""
    return (
        isinstance(obj, Message) and
        isinstance(obj.id, int) and
        isinstance(obj.content, str) and
        isinstance(obj.created_at, datetime) and
        isinstance(obj.from_agent, str) and
        isinstance(obj.to_agent, str) and
        (obj.parent_id is None or isinstance(obj.parent_id, int))
    )
```

## Schema Compatibility

Ensure that Python implementations remain compatible with the abstract schema definition:

1. Use the same field names as in the schema
2. Respect type constraints defined in the schema
3. Implement validation according to schema rules
4. Maintain relationships as specified in the schema

## Conclusion

By following these guidelines, you can implement SkogChat's algebraic type system in Python while maintaining its conceptual purity and benefits. The implementation will be:

- Immutable and safe from unexpected modification
- Well-validated to enforce data integrity
- Compatible with the abstract schema definition
- Easily testable due to pure functions
- Maintainable through clear separation of concerns

---

# SkogAI Notation for Common Patterns

### **1. Entity Definition (Core Types)**

#### Original Python

```python
class Entity:
    id: int
    name: str
    type: str
    properties: dict
    created_at: datetime
```

#### SkogSyntax Representation

```
$entity = $id * $name * $entity_type * $properties * $timestamp
$id = $int * $unique
$name = $string[1..100]
$entity_type = |user|agent|message|thread|
$properties = { $string : $any }
$timestamp = $datetime
```

---

### **2. Immutable Update Pattern**

#### Original Python

```python
def update_entity_name(entity: Entity, new_name: str) -> Entity:
    return Entity(..., name=new_name)
```

#### SkogSyntax Function Signature

```
*let update_entity_name $entity $new_name = $entity'
where
  $entity' = $entity.id * $new_name * $entity.type * ...
```

---

### **3. Error Handling with Results**

#### Original Python

```python
Result = Union[SuccessResult, ErrorResult]
```

#### SkogSyntax Representation

```
$result[T] = |success:$T|error:$error_info|
$error_info = $code * $message * $details
```

---

### **4. Collection Operations**

#### Original Python

```python
def mark_messages_as_read(messages: List[Message]) -> List[Message]:
    return [msg._replace(read=True) for msg in messages]
```

#### SkogSyntax Representation

```
$message' = $message.read_by -> set.add($entity_id)
$messages' = map($messages, λmsg.msg.read_by -> set.add($entity_id))
```

---

### **5. Command Pattern**

#### Original Python

```python
def parse_command(command: str) -> Dict[str, Any]:
```

#### SkogSyntax Representation

```
$command = @command:$command_name:[$param...]
$param = $value | $key:$value
```

---

### **What Fits Perfectly**

1. **Entity Definitions**
   Product types (`*`) perfectly model your data classes:

   ```
   $message = $id * $content * $thread_id * $parent_id
   ```

2. **Validation Constraints**
   Native type constraints:

   ```
   $username = $string[3..20] * $no_special_chars
   ```

3. **Immutable Updates**
   Built into the type system:

   ```
   $updated_message = $message.content -> replace("old", "new")
   ```

4. **Function Signatures**
   Pure function notation:

   ```
   *let send_message $thread_id $content = $message
   ```

---

### **What Needs Adaptation**

1. **I/O Operations**
   SkogSyntax's pure type system needs boundary definitions:

   ```
   -- Boundary definitions
   !effect io_send_message $message = $ok | $error
   ```

2. **Caching**
   Requires monadic extension:

   ```
   $cached[T] = $T * $expiry_time
   *let get_cached $key = $cached[T] | $null
   ```

3. **CLI Interactions**
   Needs command syntax extension:

   ```
   @cli command:$name params:[$param...] => $result
   ```

---

### **Full Translation Example**

#### Original Python

```python
def create_message(content: str, user_id: int) -> Message:
    validate_content(content)
    return Message(id=gen_id(), content=content, user_id=user_id)
```

#### SkogSyntax Implementation

```
-- Type definitions
$message = $id * $content * $user_id * $timestamp
$id = $uuid_v4  -- Changed to UUID per our discussion
$content = $string[1..1000] * $no_malicious_code
$user_id = $existing_user_id

-- Function signature
*let create_message $user_id $content =
  $message'
where
  $valid_content = $content | $invalid_content_error
  $message' = $uuid_v4 * $valid_content * $user_id * $now

-- Boundary
!effect persist_message $message = $ok | $error
```

---

### **Unrepresentable Concepts**

1. **Mutable State**
   Can't directly represent:

   ```python
   self.counter += 1
   ```

   Requires state monad pattern:

   ```
   $state_action[S,T] = $S -> ($T * $S')
   ```

2. **Inheritance**
   SkogSyntax uses composition instead:

   ```
   $admin_user = $user * $admin_permissions
   ```

3. **Loops**
   Must use recursive functions:

   ```
   *let rec process_all $items $acc =
     match $items with
     | [] -> $acc
     | x::xs -> process_all xs (acc ++ process_item x)
   ```

---

### **Key Insights**

1. **Your Type System is Turing-Complete**
   With recursion and pattern matching, you can express any computable function

2. **Implementation Details Become Boundary Definitions**
   What you called "impure" becomes clearly marked effects:

   ```
   !effect database_query $sql = $result | $error
   ```

3. **The Big Win**
   **All core business logic becomes pure type transformations** - exactly what you wanted for LLM safety and verification!
