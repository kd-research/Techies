<p align="center">
  <img src="https://raw.githubusercontent.com/kd-research/Techies/main/docs/assets/techies-logo.png" alt="Techies Logo" height="100">
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

Originally designed for research at [KD Research](https://github.com/kd-research), Techies is led by [Kaidong Hu](https://hukaidong.com).

---

## 📦 Installation

Install via Git:

```bash
VERSION=0.1.2
pip install git+https://github.com/kd-research/Techies.git@${VERSION}
```

This will install both:

- ✅ `techies` — original stable CLI
- 🧪 `techiex` — new **experimental CLI** (Click-based)

---

## 🧰 Environment Setup

Set the following environment variables before running Techies:

```bash
# OpenAI API Key (for LLM-powered agents)
export OPENAI_API_KEY=<your-api-key>

# AgentOps API Key (monitoring, logging)
export AGENTOPS_API_KEY=<your-api-key>

# Freesound API Key (optional audio assets)
export FREESOUND_CLIENT_API_KEY=<your-api-key>
```

---

## ⚙️ CLI Tools

### ✅ `techies`: Original CLI

Stable, battle-tested interface.

```bash
techies list_crews
techies introduce my_crew
techies run hierarchy_crew_v2 --game tictactoe
```

> See [Getting Started with Techies](./Getting-Started-With-Techies.md) for full usage.

---

### 🧪 `techiex`: Experimental CLI (Drop-in Replacement)

Click-based CLI designed to **match and extend** `techies`. Supports dynamic crew detection and automatic argument validation.

```bash
techiex list_crews
techiex introduce my_crew
techiex run hierarchy my_crew --game tictactoe
techiex run html5 html5_crew game_hierarchy.xml
techiex run my_custom_crew
```

> To test it as your default CLI, use:
> ```bash
> alias techies="techiex"
> ```

> ⚠️ `techiex` will **eventually replace** `techies`.

---

## 📄 Documentation

- [Getting Started with Techies](./Getting-Started-With-Techies.md)
- [Running Predefined Crews](./Running-Predefined-Crew.md)
- [Modifying Existing Crews](./Modifying-Existing-Crew.md)
- [Create Your Own Crew](./Create-Your-Own-Crew.md)

---

## 🛠 Development

### Clone & Install Locally

```bash
git clone https://github.com/kd-research/Techies.git
cd Techies
pip install -e .
```

> Recommended Python version: **3.12.4**

This gives you access to both `techies` and `techiex` command-line tools.

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

## 🤝 License

Licensed under the [MIT License](./LICENSE).
Created and maintained by [Kaidong Hu](https://hukaidong.com) at [KD Research](https://github.com/kd-research).
