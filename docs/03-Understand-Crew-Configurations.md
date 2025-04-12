# Understanding Crew Configurations

This guide explains how Techies crews are structured and how to analyze their configurations.

---

## Dump a Crew Configuration

Use the following command to inspect the definition of any built-in crew:

```bash
techies dump <crewname>
```

Example:

```bash
techies dump hierarchy_crew_v2
```

This creates a folder named `hierarchy_crew_v2/` in your current directory, containing three files:

- `agents.yml` – defines the personas, goals, and tools of each agent
- `tasks.yml` – defines the logical steps and agent assignments
- `crews.yml` – defines which agents and tasks are grouped together

You can safely explore these files without modifying anything.

---

## File Overview

---

### `agents.yml`

This file defines the roles, personalities, and tool access of each agent.

```yaml
# Available tools (built-in):
# - read_file
# - write_file
# - list_files
# - batch_read_files
# ...

_common: &common
  verbose: true
  allow_delegation: true

_no_deleg: &no_deleg
  <<: *common
  allow_delegation: false

hierarchy_architect_v2:
  <<: *common
  goal: |
    Create the foundational structure of the game hierarchy based on the game specification.
  backstory: |
    An expert in game architecture who excels at modular, expandable design.
  tools:
    - list_files
    - read_file
    - write_file
```

> You can also define and use [custom tools](./06-Create-Your-Own-Tool.md) in your agent configurations.

### Delegation Behavior

- `_common` agents **can delegate** tasks to others in the same crew  
- `_no_deleg` agents must **complete their tasks independently**
- Delegated agents **cannot delegate again**

---

### `tasks.yml`

Defines task logic and links each task to the appropriate agent.

```yaml
_task_common: &task_common
  human_input: false
  async_execution: false

game_hierarchy_representation_v2:
  <<: *task_common
  agent: hierarchy_architect_v2
  description: |
    Generate a structured game_hierarchy.xml file based on the provided specification.
  expected_output: >
    I have created the game_hierarchy.xml file as per the provided specifications.
  callback: xml_formatter  # Optional: Process task output using a callback function
  depends_on: [previous_task]  # Optional: Define task dependencies
```

Each task:
- Is executed by a single agent
- Has a clearly described goal
- May have validation logic via `expected_output`
- Can optionally specify a `callback` to process its output
- Can optionally define dependencies using `depends_on`

### Task Dependencies

The `depends_on` field allows you to build a task execution flow where outputs from previous tasks are passed as context to dependent tasks.

```yaml
task_a:
  agent: agent_a
  description: |
    Generate initial data.

task_b:
  agent: agent_b
  description: |
    Process the data from task_a.
  depends_on: [task_a]  # Output of task_a becomes context for task_b
```

When a task specifies `depends_on`, it will receive the outputs of the referenced tasks as context input.

### Task Callbacks

Callbacks are functions that process a task's output string before it's delivered to dependent tasks. Each task can have at most one callback.

When a task includes a `callback` key, the specified callback function will receive the task output and transform it before passing it on.

```yaml
mytask:
  agent: myagent
  description: |
    Generate a JSON summary of the analysis.
  callback: json_formatter  # ID of a registered callback function
```

> For more details on creating and using callbacks, see [Using Callbacks in Tasks](./07-Using-Callbacks-in-Tasks.md).

---

### `crews.yml`

Defines a complete crew — the agents and tasks involved, and how they're executed.

```yaml
_crew_common: &crew_common
  cache: false
  memory: false
  max_iter: 100
  input_args: []

hierarchy_crew_v2:
  <<: *crew_common
  agents:
    - hierarchy_architect_v2
    - hierarchy_validator
  tasks:
    - game_hierarchy_representation_v2
    - game_hierarchy_validation
  input_args:
    - game_description
```

Each crew is an execution pipeline — a collection of agents performing tasks in order.

#### Input Arguments

The `input_args` key allows crews to accept command-line arguments when run:

```yaml
mycrew:
  # ... other configuration ...
  input_args:
    - myagent_knowledge
    - mytask_focus
```

When a crew defines `input_args`, you can pass values directly on the command line:

```bash
techies run mycrew "value for first arg" "value for second arg"
```

These values will be accessible in the crew's tasks as template variables.

---

## Comparing Agent Definition vs. Self-Introduction

The `techies introduce <crewname>` command gives a high-level overview of the crew, including auto-generated agent introductions.

### Agent YAML (Definition)

```yaml
hierarchy_architect_v2:
  goal: |
    Create the foundational structure of the game hierarchy...
  backstory: |
    An expert in modular, expandable design.
  tools:
    - write_file
    - read_file
```

### Introduction Output

```
hierarchy_architect_v2: An expert in game architecture focusing on creating clear, modular structures for complex projects. Key characteristics include logical organization and the ability to design expandable game hierarchies. Uses dedicated tools for managing and updating files.
```

### Why This Matters

- The introduction is generated from the agent's `goal`, `backstory`, and tools
- It reflects the **professional tone and scope** of the agent's role
- It's a great way to validate your intent and ensure consistency in design

> Try this yourself after dumping a crew:
> ```bash
> techies introduce hierarchy_crew_v2
> ```

---

## Summary

- Crews are composed of agents and tasks defined in three YAML files
- Each file supports multiple definitions under unique keys
- `techies dump` is the best way to learn the internal structure of a crew
- `techies introduce` gives you a real-world glimpse of how agents communicate
- Crews can accept command-line arguments via the `input_args` configuration

---

## Next Step

Ready to make your own changes?

➡️ [Modifying Existing Crews](./04-Modifying-Existing-Crews.md)

Or start fresh from a scaffold:

➡️ [Create Your Own Crew](./05-Create-Your-Own-Crew.md)

Want to extend functionality with custom tools?

➡️ [Create Your Own Tool](./06-Create-Your-Own-Tool.md)