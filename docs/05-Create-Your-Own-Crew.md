# Create Your Own Crew

Techies is built to be modular and hackable — you can define your own agents, tasks, and crews using simple YAML files.

This guide walks you through how to scaffold a new custom crew from scratch, link together its components, and run it locally or globally.

> ⚠️ This feature is only available in the experimental CLI (`techiex`).  
> Make sure you've aliased it:
> ```bash
> alias techies="techiex"
> ```

---

## Step 1: Scaffold a New Crew

Use the `techies scaffold <crewname>` command to generate a starter configuration:

```bash
techies scaffold my_crew
```

This creates a folder `my_crew/` with three editable files:

- `agents.yml`
- `tasks.yml`
- `crews.yml`

Each includes a minimal working example:
- `myagent`
- `mytask`
- `mycrew`

> You can define and append as many agents, tasks, and crews as you need.

---

## Folder Structure

```bash
my_crew/
├── agents.yml   # Agent definitions
├── tasks.yml    # Task definitions
└── crews.yml    # Crew orchestration
```

Each file supports multiple entries, structured by unique keys.

---

## `agents.yml`

Defines agent behaviors, goals, tools, and delegation settings.

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

myagent:
  <<: *common
  goal: |
    Summarize all text files in the working directory.
  backstory: |
    You are a summarization expert. You have information about { myagent_knowledge }.
  tools:
    - list_files
    - read_file
```

### Delegation Rules

- Agents using `_common` can delegate tasks to **other agents in the crew**
- Agents using `_no_deleg` **must work independently**
- Delegation is **not nested** — delegated agents must complete their task on their own

---

## `tasks.yml`

Defines what tasks should be done and which agent does them.

```yaml
_task_common: &task_common
  human_input: false
  async_execution: false

mytask:
  <<: *task_common
  agent: myagent
  description: |
    Read all `.txt` files and write a summary about { mytask_focus } to summary.txt
  expected_output: >
    summary.txt is created with the combined summary.
```

Use `_task_common` to keep your task definitions clean and DRY.

---

## `crews.yml`

Defines how agents and tasks work together in a structured execution plan.

```yaml
_crew_common: &crew_common
  cache: false
  memory: false
  max_iter: 50
  input_args: []

mycrew:
  <<: *crew_common
  agents:
    - myagent
  tasks:
    - mytask
  input_args:
    - myagent_knowledge
    - mytask_focus
```

Crews are the entry points for running workflows.

### Command-line Arguments

Adding `input_args` allows your crew to accept direct command-line arguments:

```bash
techies run mycrew "Some input data" "Additional context info"
```

The arguments are passed in the same order as defined and will be available to the crew as template variables.

---

## Step 2: Run Your Custom Crew

### From inside the crew folder:

```bash
techies run mycrew
```

Techies will automatically detect your YAMLs and load local overrides.

---

### From anywhere using `TECHIES_RUNTIME`:

```bash
export TECHIES_RUNTIME=/absolute/path/to/my_crew
techies run mycrew
```

> This disables built-in crews and agents unless you include the system runtime path:

```bash
export TECHIES_RUNTIME=$(techies get_runtime_path):/absolute/path/to/my_crew
```

Use this if:
- You want to **reuse** built-in agents or tasks
- You want to **introduce** your crew (see below)
- You want to run **predefined** crews alongside your custom one

---

## (Optional) Step 3.5: Introduce Your Crew

You can test your custom crew using `techies introduce`:

```bash
techies introduce mycrew
```

This will run a built-in task where your crew introduces itself.

> ⚠️ Requires built-in runtime path:

```bash
export TECHIES_RUNTIME=$(techies get_runtime_path):/absolute/path/to/my_crew
```

A TODO is in place to remove this dependency in the future.

---

## List Available Tools

Your `agents.yml` scaffold will include commented tool names.

You can list them manually using:

```bash
techies list_tools
```

> Custom tool support is a **work in progress** — stay tuned!

---

## Best Practices

- Use `_common`, `_no_deleg`, `_task_common`, and `_crew_common` anchors for reusable settings
- Match agents, tasks, and crews using unique keys
- Run each crew inside its own clean working directory
- Use absolute paths in `TECHIES_RUNTIME` for global overrides
- Avoid editing built-in YAML files — work entirely in your own folder

---

## See Also

- [Understand Crew Configurations](./Understand-Crew-Configurations.md)
- [Modifying Existing Crews](./Modifying-Existing-Crew.md)
- [Running Predefined Crews](./Running-Predefined-Crew.md)
