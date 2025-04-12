# Create Your Own Crew

This guide walks you through creating a completely new crew from scratch.

Techies is built to be modular and hackable — you can define your own agents, tasks, and crews using simple YAML files.

This guide walks you through how to scaffold a new custom crew from scratch, link together its components, and run it locally or globally.

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

### Assigning Tools to Agents

The `agents.yml` defines which tools each agent can use:

```yaml
my_agent:
  goal: |
    Perform specialized data analysis.
  backstory: |
    A data specialist with analysis expertise.
  tools:
    - list_files
    - read_file
    - write_file
    # Add more tools from the available tool list
```

> For advanced functionality, you can [create your own custom tools](./06-Create-Your-Own-Tool.md) to extend what your agents can do.

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
  callback: my_callback  # Optional: process task output before delivery to dependent tasks
  depends_on: [previous_task]  # Optional: Define task dependencies
```

Use `_task_common` to keep your task definitions clean and DRY.

### Task Dependencies

Tasks can define dependencies on other tasks using the `depends_on` array. When a task depends on another, it receives the output from the dependent task as context.

```yaml
first_task:
  agent: research_agent
  description: |
    Research and collect data about the topic.

analysis_task:
  agent: analysis_agent
  description: |
    Analyze the data collected by the research team.
  depends_on: [first_task]  # Output of first_task becomes context for analysis_task
```

This creates a workflow where:
1. `first_task` executes first
2. Its output is captured
3. `analysis_task` receives this output as context
4. `analysis_task` executes with access to the first task's results

For complex workflows, you can depend on multiple tasks:

```yaml
final_report:
  agent: report_agent
  description: |
    Create a comprehensive report based on the research and analysis.
  depends_on: [first_task, analysis_task]  # Receives outputs from both tasks
```

### Task Callbacks

Tasks can have an optional callback function that processes the task output before it's delivered to dependent tasks. 

To assign a callback to a task, add the `callback` key with the ID of a registered callback function:

```yaml
mytask:
  # ... other task configuration ...
  callback: format_json_output
```

> **IMPORTANT:** 
> 1. Callbacks must be defined in a `callbacks.py` file or in files within a `callbacks/` directory in your runtime directories
> 2. The `--allow-load-scripts` flag **must** be enabled when running the crew to load and use callbacks:
>    ```bash
>    techies --allow-load-scripts run mycrew
>    ```

For more information on creating and using callbacks, see [Using Callbacks in Tasks](./07-Using-Callbacks-in-Tasks.md).

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

- [Understand Crew Configurations](./03-Understand-Crew-Configurations.md)
- [Modifying Existing Crews](./04-Modifying-Existing-Crews.md)
- [Running Predefined Crews](./02-Running-Predefined-Crews.md)
- [Create Your Own Tool](./06-Create-Your-Own-Tool.md)
