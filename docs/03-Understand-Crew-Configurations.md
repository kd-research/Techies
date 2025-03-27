# Understand Crew Configurations

Before modifying or creating your own crew, it’s important to understand how a Techies crew is structured. This guide will help you explore existing crews using `techies dump`, and walk you through how agents, tasks, and crews are defined in YAML.

> ⚠️ This feature requires the **experimental CLI** (`techiex`)  
> Make sure you’ve aliased it in your shell:
> ```bash
> alias techies="techiex"
> ```

---

## 🧪 Dump a Crew Configuration

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

## 📁 File Overview

---

### 👤 `agents.yml`

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

### 🔄 Delegation Behavior

- `_common` agents **can delegate** tasks to others in the same crew  
- `_no_deleg` agents must **complete their tasks independently**
- Delegated agents **cannot delegate again**

---

### 🧠 `tasks.yml`

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
```

Each task:
- Is executed by a single agent
- Has a clearly described goal
- May have validation logic via `expected_output`

---

### 🧩 `crews.yml`

Defines a complete crew — the agents and tasks involved, and how they're executed.

```yaml
_crew_common: &crew_common
  cache: false
  memory: false
  max_iter: 100

hierarchy_crew_v2:
  <<: *crew_common
  agents:
    - hierarchy_architect_v2
    - hierarchy_validator
  tasks:
    - game_hierarchy_representation_v2
    - game_hierarchy_validation
```

Each crew is an execution pipeline — a collection of agents performing tasks in order.

---

## 🤖 Comparing Agent Definition vs. Self-Introduction

The `techies introduce <crewname>` command gives a high-level overview of the crew, including auto-generated agent introductions.

### 📘 Agent YAML (Definition)

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

### 💬 Introduction Output

```
hierarchy_architect_v2: An expert in game architecture focusing on creating clear, modular structures for complex projects. Key characteristics include logical organization and the ability to design expandable game hierarchies. Uses dedicated tools for managing and updating files.
```

### 🔍 Why This Matters

- The introduction is generated from the agent’s `goal`, `backstory`, and tools
- It reflects the **professional tone and scope** of the agent’s role
- It’s a great way to validate your intent and ensure consistency in design

> 🧪 Try this yourself after dumping a crew:
> ```bash
> techies introduce hierarchy_crew_v2
> ```

---

## ✅ Summary

- Crews are composed of agents and tasks defined in three YAML files
- Each file supports multiple definitions under unique keys
- `techies dump` is the best way to learn the internal structure of a crew
- `techies introduce` gives you a real-world glimpse of how agents communicate

---

## 🚀 Next Step

Ready to make your own changes?

➡️ [Modifying Existing Crews](./Modifying-Existing-Crews.md)

Or start fresh from a scaffold:

➡️ [Create Your Own Crew](./Create-Your-Own-Crew.md)
