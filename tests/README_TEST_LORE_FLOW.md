# Lore Flow Content Test

## Purpose
Tests that `integration/lore-flow.sh` correctly populates the `content` field in generated lore entries.

## Background
Issue #6: Pipeline was creating entry JSON files with empty `content` fields due to a variable naming bug in the Python inline script.

## Running the Test

```bash
# From repository root
./tests/test_lore_flow_content.sh
```

## What It Tests
1. Creates a mock LLM integrator that returns predictable JSON output
2. Runs the lore-flow.sh pipeline with manual input
3. Verifies that the created entry has non-empty content field
4. Validates content matches expected narrative pattern

## Expected Output
```
✅ TEST PASSED: Content field is populated with narrative
Content length: 200 characters
Content validation successful!
```

## Test Strategy
- Mocks `llama-lore-integrator.sh` to avoid dependency on external LLM services
- Creates temporary entries that are cleaned up after test
- Focuses specifically on the content field population bug
- Ignores unrelated warnings (e.g., missing chronicle books)

## Test Files
- `tests/test_lore_flow_content.sh` - Main test script
- Creates mock in `/tmp/lore-flow-test-*`
- Temporarily backs up original integrator
