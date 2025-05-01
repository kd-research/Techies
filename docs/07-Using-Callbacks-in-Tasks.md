# Using Callbacks in Tasks

This guide explains how to create and use callbacks to process task outputs in Techies.

---

## What Are Callbacks?

Callbacks in Techies are functions that process a task's output before it's delivered to dependent tasks. Each task can have at most one callback function associated with it.

Key points about callbacks:
- A callback processes the output string from a task
- It returns a modified string that will be delivered to dependent tasks
- Callbacks are registered and loaded similarly to tools
- Each task can have at most one callback
- **Callbacks must be defined in dedicated files** (in `callbacks.py` or in the `callbacks/` directory)
- **The `--allow-load-scripts` flag is required** to load and use callbacks

---

## How Callbacks Work

1. **Task Execution**: A task runs and produces an output string
2. **Callback Processing**: If a callback is assigned, the output passes through it
3. **Modified Output**: The callback returns a transformed version
4. **Delivery**: The modified output is delivered to dependent tasks

```
┌────────┐    output string   ┌────────────┐    modified output   ┌─────────────┐
│  Task  │ ─────────────────► │  Callback  │ ───────────────────► │ Dependent   │
│        │                    │  Function  │                      │ Tasks       │
└────────┘                    └────────────┘                      └─────────────┘
```

### Callbacks in Task Dependencies Flow

Callbacks fit into the task dependency flow as follows:

1. Task A produces output
2. Task A's callback (if any) processes this output
3. The processed output is stored
4. Task B (which depends on Task A) receives this processed output as context

```
                        ┌─────────────┐
                        │  Task A's   │
                        │  Callback   │
                        └──────┬──────┘
                               │ 
                               ▼ processed output
┌──────────┐   output   ┌─────────────┐             ┌──────────┐
│  Task A  ├───────────►│  Storage    ├────────────►│  Task B  │
└──────────┘            └─────────────┘             │(depends  │
                                                    │on Task A)│
                                                    └──────────┘
```

This approach ensures that the downstream tasks always receive data in a consistent, properly formatted way, as determined by the upstream task's callback.

---

## Creating Custom Callbacks

Creating a custom callback is simple - it's just a Python function that takes a string input and returns a string output.

### Callback Files Location

Callbacks can be defined in two locations:
- A `callbacks.py` file in any runtime directory
- Any Python file within a `callbacks/` directory in any runtime directory

### Creating a Simple Callback

```python
# Example callback file: callbacks.py or callbacks/my_callback.py

# This function is automatically available in callback files
from techies.callbacks import register_callback

def format_json_output(output: str) -> str:
    """
    Formats the output as JSON and adds proper structure.
    This callback ensures consistent JSON formatting.
    """
    import json
    
    # Try to extract JSON content if it exists
    try:
        # Look for content between triple backticks
        import re
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', output)
        
        if json_match:
            json_str = json_match.group(1)
            # Parse and reformat to ensure valid JSON
            data = json.loads(json_str)
            return json.dumps(data, indent=2)
    except Exception:
        pass
    
    # If no valid JSON found or error occurred, return original
    return output

# Register the callback
register_callback(format_json_output)
```

### Callback Registration

When you create a callback, it must be registered using the `register_callback` function:

```python
register_callback(callback_function)
```

By default, the callback ID will be the snake_case version of the function name. You can specify a custom ID:

```python
register_callback(format_json_output, callback_id="json_formatter")
```

---

## Loading Callbacks

### Required Flag

To load and use custom callbacks, you **must** use the `--allow-load-scripts` flag when running Techies:

```bash
techies --allow-load-scripts run mycrew
```

Without this flag, no custom callbacks will be loaded, and any task that references a callback will not be able to find it.

To list all available callbacks:

```bash
techies --allow-load-scripts list callbacks
```

---

## Assigning Callbacks to Tasks

To assign a callback to a task, add a `callback` key in your `tasks.yml` file with the exact callback ID:

```yaml
# tasks.yml
_task_common: &task_common
  human_input: false
  async_execution: false

task_a:
  <<: *task_common
  agent: first_agent
  description: |
    Generate initial JSON data.
  callback: format_json_output  # Must match a registered callback ID

task_b:
  <<: *task_common
  agent: second_agent
  description: |
    Process the formatted JSON data from task_a.
  depends_on: [task_a]  # Receives the formatted JSON output
```

> **Warning:** The callback ID (`format_json_output` in the example) must exactly match the ID of a callback registered in your `callbacks.py` file or one of your `callbacks/` directory files, and the `--allow-load-scripts` flag must be used when running the crew.

---

## Best Practices

1. **Single Responsibility**: A callback should do one thing well
2. **Error Handling**: Always handle exceptions to prevent task failures
3. **Idempotence**: A callback should be idempotent (repeated application produces same result)
4. **Documentation**: Include descriptive docstrings for your callbacks
5. **Validation**: Validate input and output to ensure correct format

---

## Example Use Cases

- **Format Conversion**: Convert between different formats (e.g., XML to JSON)
- **Data Extraction**: Extract specific information from larger outputs
- **Text Processing**: Clean, format, or standardize text outputs
- **Validation**: Verify outputs meet certain criteria before passing to next task
- **Enrichment**: Add additional information to the output

---

## Testing Callbacks

You can test your callbacks in isolation:

```python
# Test script for callback
from my_callback_file import format_json_output

test_input = '''Here's my JSON output:
```json
{"name": "Test", "value": 123}
```
'''

print(format_json_output(test_input))
```

---

## See Also

- [Understand Crew Configurations](./03-Understand-Crew-Configurations.md)
- [Create Your Own Crew](./05-Create-Your-Own-Crew.md)
- [Create Your Own Tool](./06-Create-Your-Own-Tool.md) 