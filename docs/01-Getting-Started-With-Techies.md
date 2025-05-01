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
# Note: agentops is optional and requires manual installation:
# pip install agentops
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
techies list crews

# List all available agents
techies list agents

# List all available tasks
techies list tasks

# List predefined game specifications
techies list game_specs

# List available tools
techies list tools

# List available callbacks (requires --allow-load-scripts flag)
techies --allow-load-scripts list callbacks
```

> Note: Legacy commands like `list_crews`, `list_agents` are still available but will be deprecated in v2.0.

---

## Introduce a Crew

Use the `introduce` command to preview what a crew does and how it works: