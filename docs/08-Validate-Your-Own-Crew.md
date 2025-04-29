# Validating Your Configurations

This guide explains how to use Techies' validation features to ensure your crews, tasks, and agents are correctly configured.

---

## Overview

Validation helps you catch errors early by checking:

- Configuration schema adherence
- Existence of referenced components
- Cyclical dependencies
- Task execution order
- Tool and callback availability

---

## Using the `check` Command

The `techies check` command provides a simple way to validate different components:

```bash
# Validate a crew
techies check crew my_crew

# Validate a specific task
techies check task my_task

# Validate an agent
techies check agent my_agent

# Validate a tool
techies check tool read_file

# Validate a callback
techies check callback json_formatter
```

Each command performs comprehensive validation of the referenced component and its dependencies.

---

## Recursive vs. Non-Recursive Validation

By default, validation is **recursive**, meaning it checks not only the target component but also all its dependencies:

- For **crews**: validates all agents and tasks
- For **tasks**: validates the agent, callback, and dependent tasks
- For **agents**: validates all tools they use

You can disable recursive validation with the `--no-recursive` flag (or `-r` shorthand):

```bash
techies check crew my_crew --no-recursive
techies check task some_task -r
```

This is useful when you want to validate only a specific component without checking its dependencies.

---

## What Gets Validated

### Crews

- **Schema validation**: Checks if the crew configuration has all required fields and correct data types
- **Agent validation**: Verifies all referenced agents exist and are valid
- **Task validation**: Ensures all tasks exist and are properly configured
- **Topological order**: Confirms tasks are listed in a valid execution order based on dependencies

### Tasks

- **Schema validation**: Checks the task configuration against the required schema
- **Agent validation**: Ensures the assigned agent exists and is valid
- **Callback validation**: If a callback is specified, verifies it exists
- **Dependency validation**: Checks that all dependent tasks exist and there are no circular dependencies

### Agents

- **Schema validation**: Verifies the agent configuration meets the required schema
- **Tool validation**: Ensures all tools referenced by the agent exist

### Tools and Callbacks

- **Existence check**: Verifies that the tool or callback is registered in the system

---

## Validation Messages

The validation output tells you exactly what went wrong:

```
Checked crew 'my_crew' (recursive=True): FAILED - Crew 'my_crew' has invalid tasks:
Task 'generate_code': Task 'generate_code' references invalid agent: Agent 'nonexistent_agent' not found
```

Successful validation produces:

```
Checked agent 'ui_designer' (recursive=True): OK
```

---

## Programmatic Validation

You can also use the validation functions in your own code:

```python
from techies.crew import Crew
from techies.task import Task
from techies.agent import Agent

# Validate a crew
ok, reason = Crew.validate("my_crew", recursive=True)
if not ok:
    print(f"Crew validation failed: {reason}")

# Validate a task
ok, reason = Task.validate("my_task")
if not ok:
    print(f"Task validation failed: {reason}")

# Validate an agent
ok, reason = Agent.validate("my_agent")
if not ok:
    print(f"Agent validation failed: {reason}")
```

---

## Best Practices

- **Validate early and often** during development to catch configuration errors
- **Start with specific components** before validating entire crews
- Always **check for cycles in task dependencies** using recursive validation
- Use validation when **modifying existing crews** to ensure backward compatibility
- After validation errors, **fix issues incrementally** and revalidate

---

## Dependencies and Schema

Techies validates configurations against JSON schemas that enforce:

- **Crew schema**: Requires `agents` and `tasks` lists
- **Task schema**: Requires `agent` and `description` fields
- **Agent schema**: Requires `goal`, `backstory`, and `tools` fields

The validation also checks for proper task dependency ordering to prevent runtime errors due to missing context data.

---

## Summary

- The `techies check` command helps validate your configurations
- Validation is recursive by default, checking all dependencies
- Schema validation catches missing or incorrectly typed fields
- Dependency validation ensures proper execution order
- Clear error messages help you identify and fix issues quickly

---

## Next Steps

Ready to explore more Techies features?

➡️ [Create Your Own Crew](./05-Create-Your-Own-Crew.md)
➡️ [Create Your Own Tool](./06-Create-Your-Own-Tool.md)
➡️ [Using Callbacks in Tasks](./07-Using-Callbacks-in-Tasks.md) 