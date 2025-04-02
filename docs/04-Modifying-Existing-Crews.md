# Modifying Existing Crews

This guide walks you through extending or modifying existing crews to customize their behavior.

Once you understand how Techies crews are structured, you can start customizing them to better suit your needs.

This guide walks you through how to **safely modify an existing crew**, override agents or tasks, and extend behavior using local configuration files.

---

## Step 1: Dump a Crew for Editing

To begin, choose a crew to modify and dump its configuration:

```bash
techies dump hierarchy_crew_v2
```

This creates a folder named `hierarchy_crew_v2/` in your current working directory containing:

- `agents.yml`
- `tasks.yml`
- `crews.yml`

These files represent the full configuration of the crew and can now be modified locally.

---

## Step 2: Make Your Modifications

You can now open and edit the dumped YAML files:

- **agents.yml** — change agent goals, tools, or backstory
- **tasks.yml** — adjust instructions, expected output, or execution flow
- **crews.yml** — change task order, crew members, or iteration limits

> Any matching agent/task/crew key defined locally will override the system version automatically.

---

## Step 3: Run the Modified Crew

After editing, run the crew from the same directory:

```bash
techies run hierarchy_crew_v2 --game word2048
```

Techies will prioritize the local files over built-in definitions when resolving the crew configuration.

---

## How Overrides Work

Techies loads configurations in the following order **by default**:

1. Built-in system definitions
2. Definitions in the **current working directory**

If an agent/task/crew key is found in both, the **local version takes precedence**.

---

## Step 4: Control Crew Discovery with `TECHIES_RUNTIME`

You can override the default discovery behavior using the `TECHIES_RUNTIME` environment variable.

### Overrides CWD and System

When defined, Techies will **only** use the paths listed in `TECHIES_RUNTIME` to load definitions — and skip built-in and CWD.

```bash
export TECHIES_RUNTIME=/absolute/path/to/custom_crews
```

> Make sure to use **absolute paths**. Relative paths like `./my_crews` will not be included unless you're working from that directory.

### Include Built-Ins Manually

To include built-ins alongside your custom definitions:

```bash
export TECHIES_RUNTIME=$(techies get_runtime_path):/absolute/path/to/custom_crews
```

This restores access to all predefined crews while allowing you to layer your overrides.

### Path Priority

Paths are evaluated **in order**. Later paths override earlier ones if the same keys are defined.

---

## Best Practices

- Always dump a crew before modifying — never edit built-ins
- Use `_common` blocks and anchors to avoid duplication
- Use unique, descriptive keys when creating new agents or tasks
- Use absolute paths in `TECHIES_RUNTIME`
- Run from a clean working directory for each crew

---

## Example: Modify an Agent

1. Dump a crew:
    ```bash
    techies dump hierarchy_crew_v2
    ```

2. Edit `agents.yml`:
    ```yaml
    hierarchy_architect_v2:
      goal: |
        In addition to XML, also generate a summary in Markdown format.
      tools:
        - write_file
        - read_file
        - markdown_parser
    ```

3. Run the crew:
    ```bash
    techies run hierarchy_crew_v2 --game pong
    ```

Your local changes will be picked up automatically.

---

## Resetting to Default

To revert to the original system version of a crew:

- Delete the local `<crewname>/` folder
- Or unset/remove the `TECHIES_RUNTIME` variable

---

## Modifying Agent Definitions

One of the most common customizations is changing which tools an agent has access to.

1. Open the dumped `agents.yml` file
2. Locate the agent you want to modify
3. Add or remove tools from the `tools` list:

```yaml
my_modified_agent:
  goal: |
    Search for information and analyze data.
  backstory: |
    A research specialist with data analysis skills.
  tools:
    - read_file
    - write_file
    - list_files
    # Add other tools here
```

> Need more specialized functionality? You can also [create custom tools](./06-Create-Your-Own-Tool.md) and make them available to your agents.

---

## See Also

- [Understand Crew Configurations](./03-Understand-Crew-Configurations.md)
- [Create Your Own Crew](./05-Create-Your-Own-Crew.md)
- [Create Your Own Tool](./06-Create-Your-Own-Tool.md)
