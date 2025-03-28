# Running Predefined Crews

Techies comes with several **predefined crews** designed for creative workflows like game design and web development. This guide walks you through how to use each one effectively.

> These crews are preconfigured and available immediately after installation.

---

## Available Crews

Run the following to list available crews:

```bash
techies list_crews
```

Example output:

```
[Available crews]
hierarchy_crew
code_crew
html5_crew
hierarchy_crew_v2
```

---

## Working Directory Rules

When running any crew, Techies assumes the **current working directory** is a clean, isolated workspace.

- Crews have **full permission to read/write** all files in the directory.
- Files and folders **starting with a dot (`.`)** (e.g. `.env`, `.git/`) will be ignored.
- Any outputs, including HTML files, code, or intermediate artifacts, will be written here.
- **Do not run crews in your home folder or a project root** — always use a temporary or dedicated folder.

### Recommended

```bash
mkdir working_dir
cd working_dir
techies run hierarchy_crew_v2 --game word2048
```

---

## 1. `hierarchy_crew`

This is the original hierarchy-planning crew.

### Purpose:
Breaks down a game concept into a structured **game hierarchy tree**, representing game mechanics and sub-components.

### Input:
- Either a **predefined game spec** via `--game`, or
- A custom game prompt via file (`.txt`)

### Output:
- `game_hierarchy.xml`

### Example:

```bash
techies run hierarchy_crew --game tictactoe
```

or

```bash
techies run hierarchy_crew my_game_idea.txt
```

---

## 2. `hierarchy_crew_v2` (Recommended)

An improved version of `hierarchy_crew` with refined agents and logic.

### Purpose:
Same goal as `hierarchy_crew`, but with better decomposition and structure. Preferred for most workflows.

### Input:
- Same as `hierarchy_crew`

### Output:
- `game_hierarchy.xml` (in current directory)

### Example:

```bash
techies run hierarchy_crew_v2 --game snake
```

---

## 3. `html5_crew`

Generates a full playable HTML5 game based on a game hierarchy structure.

### Purpose:
Converts a `game_hierarchy.xml` file (from a hierarchy crew) into a playable game using HTML, CSS, JS, and sounds.

### Input:
- `game_hierarchy.xml` must exist in the current directory

### Output:
- `index.html`
- `style.css`
- `script.js`
- `game.html` (merged)
- Optional: `.mp3` sound files

### Example:

```bash
techies run html5_crew game_hierarchy.xml
```

> If `game.html` doesn't exist, it will scaffold it using a built-in template.

---

## 4. `code_crew`

Generates Python code components from a given game hierarchy.

### Purpose:
Transforms game structure (in `.xml`) into basic playable code components, focusing on **game logic and mechanics**.

### Input:
- `game_hierarchy.xml` file in current directory

### Output:
- Python modules/files related to the game's logic

### Example:

```bash
techies run code_crew game_hierarchy.xml
```

> The generated code can be extended manually or used in further pipelines.

---

## Recommended Workflow

To keep things clean and isolated, use a fresh working directory for each project:

```bash
# 1. Create and enter a clean working directory
mkdir working_dir && cd working_dir

# 2. Generate the game plan
techies run hierarchy_crew_v2 --game pong

# 3. Visualize it as an HTML5 game
techies run html5_crew game_hierarchy.xml

# 4. (Optional) Generate Python code
techies run code_crew game_hierarchy.xml
```

> All outputs will be saved directly into the working directory.

---

## Debugging Tips

- Use `techies introduce <crew>` to get a natural language explanation of what a crew does.
- Ensure you are inside a writable working directory.
- Missing output? Check for:
  - Correct input file paths
  - Required environment variables (especially `MODEL` and `OPENAI_API_KEY`)

---

## Next Steps

- [Modifying Existing Crews](./Modifying-Existing-Crew.md)
- [Create Your Own Crew](./Create-Your-Own-Crew.md)
