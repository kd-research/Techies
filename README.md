<p align="center">
  <img src="https://raw.githubusercontent.com/kd-research/Techies/main/docs/assets/techies-logo.png" alt="Techies Logo" height="120">
</p>

<h1 align="center">Techies</h1>

<p align="center">
  A modular agent framework for collaborative creativity and structured workflows.
</p>

<p align="center">
  <a href="https://github.com/kd-research/Techies/releases">
    <img src="https://img.shields.io/github/v/tag/kd-research/Techies?label=version&color=blue" alt="Latest Version">
  </a>
  <a href="https://github.com/kd-research/Techies/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/kd-research/Techies" alt="License">
  </a>
  <img src="https://img.shields.io/badge/python-3.12.4%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/cli-techies-orange" alt="CLI Interface">
</p>

---

## What is Techies?

**Techies** is a flexible agent framework for designing and running collaborative, multi-agent workflows. It supports dynamic planning, modular task execution, and structured agent coordination — ideal for creative tasks such as game design, code generation, and more.

Developed by the [KD Research](https://github.com/kd-research) organization, led by [Kaidong Hu](https://hukaidong.com).

---

## Installation

```bash
# Install latest version
pip install git+https://github.com/kd-research/Techies.git

# For specific version (uncomment and modify)
# pip install git+https://github.com/kd-research/Techies.git@1.0.0
```

This installs:

- `techies` — comprehensive CLI for all Techies functionality

---

## Environment Setup

Set the following environment variables before running Techies:

```bash
# Required for LLMs (default: OpenAI)
export OPENAI_API_KEY=<your-api-key>

# Optional (AgentOps monitoring/debugging)
export AGENTOPS_API_KEY=<your-api-key>

# Optional (audio support)
export FREESOUND_CLIENT_API_KEY=<your-api-key>

# Recommended: Specify your model and provider
export MODEL=openai/gpt-4o
```

> Visit [LiteLLM's model list](https://docs.litellm.ai/docs/providers) for supported providers.

> If you're using another LLM provider (e.g. Groq, Anthropic, Mistral), you'll need to export its matching API key too.

---

## CLI Tools

### `techies`: CLI Interface

The powerful CLI interface for running and managing crews:

```bash
techies list_crews
techies run hierarchy_crew_v2 --game tictactoe
techies introduce hierarchy_crew_v2
```

Techies CLI also supports:

- `scaffold` — create new custom crews
- `dump` — extract and modify existing crews
- `TECHIES_RUNTIME` — define custom runtime paths

```bash
techies scaffold my_crew
techies dump hierarchy_crew_v2
techies run mycrew
```

---

## Documentation

- [Getting Started with Techies](./docs/01-Getting-Started-With-Techies.md)
- [Running Predefined Crews](./docs/02-Running-Predefined-Crews.md)
- [Understand Crew Configurations](./docs/03-Understand-Crew-Configurations.md)
- [Modifying Existing Crews](./docs/04-Modifying-Existing-Crews.md)
- [Create Your Own Crew](./docs/05-Create-Your-Own-Crew.md)
- [Create Your Own Tool](./docs/06-Create-Your-Own-Tool.md)
- [Using Callbacks in Tasks](./docs/07-Using-Callbacks-in-Tasks.md)

---

## Development

### Clone & Install Locally

```bash
git clone https://github.com/kd-research/Techies.git
cd Techies
pip install -e .
```

> Requires Python `3.12.4+`

---

## Best Practices

- Use `techies scaffold` to start your own crew
- Define a clean working directory for each run
- Use `TECHIES_RUNTIME` to load external crew folders
- Set `MODEL` and relevant API keys for your LLM provider

---

## License & Credits

Techies is open-source and licensed under the [GPLv3 License](./LICENSE).  
Created and maintained by [Kaidong Hu](https://hukaidong.com) at [KD Research](https://github.com/kd-research).
