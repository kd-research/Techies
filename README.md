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
  <img src="https://img.shields.io/badge/cli-techies%20%7C%20techiex-orange" alt="CLI Interface">
</p>

---

## 🚀 What is Techies?

**Techies** is a flexible agent framework for designing and running collaborative, multi-agent workflows. It supports dynamic planning, modular task execution, and structured agent coordination — ideal for creative tasks such as game design, code generation, and more.

Developed by the [KD Research](https://github.com/kd-research) organization, led by [Kaidong Hu](https://hukaidong.com).

---

## 📦 Installation

Install Techies from GitHub:

```bash
VERSION=1.0.0
pip install git+https://github.com/kd-research/Techies.git@${VERSION}
```

This installs both:

- ✅ `techies` — original stable CLI
- 🧪 `techiex` — new **experimental CLI** (Click-based)

> To alias `techiex` as your default CLI:
> ```bash
> alias techies="techiex"
> ```

---

## 🧰 Environment Setup

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

> 🔍 Visit [LiteLLM's model list](https://docs.litellm.ai/docs/providers) for supported providers.

> If you're using another LLM provider (e.g. Groq, Anthropic, Mistral), you'll need to export its matching API key too.

---

## ⚙️ CLI Tools

### ✅ `techies`: Original CLI

Stable, tested interface for running built-in crews.

```bash
techies list_crews
techies run hierarchy_crew_v2 --game tictactoe
techies introduce hierarchy_crew_v2
```

### 🧪 `techiex`: Experimental CLI (Drop-in Replacement)

Fully modular CLI with support for:

- 🛠️ `scaffold` — create new custom crews
- 🧠 `dump` — extract and modify existing crews
- 🌍 `TECHIES_RUNTIME` — define custom runtime paths

```bash
techiex scaffold my_crew
techiex dump hierarchy_crew_v2
techiex run mycrew
```

> `techiex` supports everything `techies` does — and more.

---

## 📄 Documentation

- 📘 [Getting Started with Techies](./docs/Getting-Started-With-Techies.md)
- 🚀 [Running Predefined Crews](./docs/Running-Predefined-Crews.md)
- 🧩 [Understand Crew Configurations](./docs/Understand-Crew-Configurations.md)
- 🔧 [Modifying Existing Crews](./docs/Modifying-Existing-Crews.md)
- 🏗 [Create Your Own Crew](./docs/Create-Your-Own-Crew.md)

---

## 🛠 Development

### Clone & Install Locally

```bash
git clone https://github.com/kd-research/Techies.git
cd Techies
pip install -e .
```

> ✅ Requires Python `3.12.4+`

---

## 🗂 Directory Overview

```
techies/
├── cli/               # Click-based experimental CLI
│   ├── commands/      # Subcommands: run, introduce, etc.
│   ├── utils/         # Crew dispatching, helpers
│   └── main.py        # CLI entry point
├── agent.py
├── task.py
├── crew.py
└── ...
```

---

## ✅ Best Practices

- Use `techiex` with `scaffold` to start your own crew
- Define a clean working directory for each run
- Use `TECHIES_RUNTIME` to load external crew folders
- Set `MODEL` and relevant API keys for your LLM provider

---

## 🤝 License & Credits

Techies is open-source and licensed under the [GPLv3 License](./LICENSE).  
Created and maintained by [Kaidong Hu](https://hukaidong.com) at [KD Research](https://github.com/kd-research).
