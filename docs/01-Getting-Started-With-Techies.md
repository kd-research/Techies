# Getting Started with Techies

Welcome to **Techies** — a modular framework for building and orchestrating collaborative agents. This guide walks you through how to get up and running with the `techies` CLI and run your first crew.

> Latest Version: `1.0.0`  
> Recommended Python: `3.12.4`

---

## What Is a Crew?

In Techies, a **crew** is a team of intelligent agents working together to complete a creative task. Each crew is made up of:

- **Agents** — specialized AI components
- **Tasks** — modular logic blocks assigned to agents
- **Crew configuration** — a predefined or custom setup that determines who does what

Crews are fully configurable and can be extended or created from scratch.

---

## Installation

```bash
# Install latest version
pip install git+https://github.com/kd-research/Techies.git

# For specific version (uncomment and modify)
# pip install git+https://github.com/kd-research/Techies.git@v1.0.0
```

This installs:

- `techies` — the comprehensive CLI for all Techies functionality

---

## Environment Setup

Before running anything, set the following environment variables:

```bash
# Required (for default LLM behavior)
export OPENAI_API_KEY=<your-api-key>

# Optional (AgentOps for debugging/monitoring)
export AGENTOPS_API_KEY=<your-api-key>

# Optional (Freesound for audio)
export FREESOUND_CLIENT_API_KEY=<your-api-key>

# Required to specify LLM model/provider (default shown)
export MODEL=openai/gpt-4o
```

> Visit [https://docs.litellm.ai/docs/providers](https://docs.litellm.ai/docs/providers) to choose a different model/provider.

> If you're using another provider (e.g. Groq, Mistral, Anthropic), you must also export the appropriate API key (e.g. `GROQ_API_KEY`, `ANTHROPIC_API_KEY`).

---

## Explore Available Crews, Agents & Tasks

Once installed, use the CLI to explore what's available:

```bash
# List all registered crews
techies list_crews

# List all available agents
techies list_agents

# List all available tasks
techies list_tasks

# List predefined game specifications
techies list_game_specs
```

---

## Introduce a Crew

Use the `introduce` command to preview what a crew does and how it works:

```bash
techies introduce hierarchy_crew_v2
```

This runs a special **self-introduction task** and will generate a natural-language explanation of the crew.

> Warning: Requires access to system runtime path. If you're using a custom `TECHIES_RUNTIME`, make sure to include:
> ```bash
> export TECHIES_RUNTIME=$(techies get_runtime_path):/your/custom/path
> ```

---

## Run a Crew

You can run a predefined crew using the `run` command.

### Step 1: Run a Hierarchy Crew

This generates a structured XML hierarchy for a game idea.

```bash
techies run hierarchy_crew_v2 --game tictactoe
```

- This uses a built-in game spec (`tictactoe`)
- You can also provide a custom `.txt` file:

```bash
techies run hierarchy_crew_v2 my_game.txt
```

> Output: `game_hierarchy.xml` will be created in the current directory.

---

### Step 2: Run the HTML5 Crew

Once `game_hierarchy.xml` has been generated, you can use it to build a playable game:

```bash
techies run html5_crew game_hierarchy.xml
```

This will generate:

- `index.html`, `style.css`, `script.js`
- `game.html` (merged version)
- Optional: `.mp3` sound files (if defined)

> Open `game.html` in a browser to play.

---

## Working Directory Rules

Techies crews are **sandboxed** to the current working directory:

- All outputs are written directly here
- Crews can read/write any file in the directory
- Hidden files/folders (starting with `.`) are ignored
- Do **not** run crews in your home directory or root repo

### Recommended Workflow

```bash
# 1. Create a new clean working directory
mkdir working_dir && cd working_dir

# 2. Run a hierarchy crew to generate game logic
techies run hierarchy_crew_v2 --game tictactoe

# 3. Use the output to run the HTML5 crew
techies run html5_crew game_hierarchy.xml

# 4. Open the output (game.html) in your browser
```

> Always use a clean folder when running crews. Crews write all outputs into the current directory.

---

## Need Help?

To view help for any command:

```bash
techies --help
techies run --help
techies introduce --help
```

---

## Next Steps

- [Running Predefined Crews](./02-Running-Predefined-Crews.md)
- [Understand Crew Configurations](./03-Understand-Crew-Configurations.md)
- [Modifying Existing Crews](./04-Modifying-Existing-Crews.md)
- [Create Your Own Crew](./05-Create-Your-Own-Crew.md)
- [Create Your Own Tool](./06-Create-Your-Own-Tool.md)
- [Using Callbacks in Tasks](./07-Using-Callbacks-in-Tasks.md)

---

Techies is developed by [Kaidong Hu](https://hukaidong.com) at [KD Research](https://github.com/kd-research).
