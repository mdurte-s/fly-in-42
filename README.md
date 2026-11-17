*This project has been created as part of the 42 curriculum by mdurte-s.*

<div align="center">

# Fly-In 🛸
### Multi-Agent Drone Fleet Routing & Real-Time Visualization Engine

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Pygame-CE](https://img.shields.io/badge/GUI-pygame--ce%20%3E%3D%202.5.0-green?logo=pygame&logoColor=white)](https://pyga.me/)
[![Poetry](https://img.shields.io/badge/Dependencies-Poetry-blueviolet?logo=poetry&logoColor=white)](https://python-poetry.org/)
[![42 School](https://img.shields.io/badge/42-Curriculum-black?logo=42&logoColor=white)](https://42.fr/)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black%20%7C%20Flake8-black)](https://github.com/psf/black)

<p align="center">
  A high-performance drone simulation engine built in Python that plans conflict-free multi-agent routes across constrained networks and renders turn-by-turn traffic dynamics through a real-time animated Pygame GUI.
</p>

[Visual Demo](#-simulation-visualization-demo) •
[Features](#-key-features) •
[Installation](#-installation) •
[Quickstart](#-quickstart--usage) •
[Map Configuration](#-map-format--configuration) •
[Algorithm](#-routing-algorithm--simulation-engine) •
[Challenge Maps](#-benchmark-suite--challenge-maps) •
[Project Structure](#-project-architecture)

</div>

---

## 🎥 Simulation Visualization Demo

<!-- ================================================================= -->
<!-- 🎬 VIDEO INSERTION SECTION                                        -->
<!-- Place your demo video file in assets/ or paste a hosted URL below -->
<!-- ================================================================= -->

<p align="center">
  <video src="assets/flyin.webm" width="85%" controls autoplay loop muted>
    <p>Your browser does not support the video tag. Watch the demo video file at <code>assets/flyin_demo.mp4</code>.</p>
  </video>
</p>

<p align="center">
  <em>Real-time visualization demonstrating multi-agent route execution, node capacity management, and restricted zone transit.</em>
</p>

> [!TIP]
> **How to insert your video:**
> - **GitHub Direct Upload (Recommended):** When editing this README on GitHub, drag and drop your `.mp4`, `.mov`, or `.webm` recording directly into the text editor. GitHub will host the video and generate a permanent URL you can paste into the `<video src="...">` tag above.
> - **Local repository file:** Place your exported video at `assets/flyin_demo.mp4` (or `.webm`) in the repository root.
> - **Animated GIF alternative:** To display an animated GIF instead, use:
>   ```markdown
>   ![Fly-in Simulation Demo](assets/flyin_demo.gif)
>   ```

### 🔍 Visualization Features in Action
- **Adaptive Coordinate Mapping:** Window coordinates automatically normalize and re-scale based on hub Cartesian positions, preserving aspect ratios and adapting dynamically to window resizing (supports 800×600 up to 1920×1080).
- **Color-Coded Corridor Status:**
  - 🟢 **Green:** Priority corridors (optimal routes with path cost discounts).
  - 🟡 **Yellow:** Restricted transit zones (multi-turn transit delays).
  - 🔴 **Red:** Blocked corridors (inaccessible to all drones).
  - ⚪ **White:** Standard normal routes.
- **Smooth Trajectory Interpolation:** 60 FPS continuous animation between discrete turns, including midpoint pauses for multi-turn restricted zone arrivals.
- **Dynamic Heads-Up Display (HUD):** Live elapsed mission timer and turn tracker that freeze automatically upon mission completion.
- **Intelligent Label Decluttering:** Hub names and drone identifiers automatically hide when the window size or node density would cause visual collisions.

---

## ✨ Key Features

- **Multi-Agent Pathfinding:** Shortest path route discovery via Dijkstra's algorithm augmented with iterative node penalties to disperse drone traffic across non-interfering candidate paths.
- **Discrete Turn Simulation Engine:** Step-by-step turn coordination respecting individual hub occupancy limits (`max_drones`) and connection throughput caps (`max_link_capacity`).
- **Zone Classifications:**
  - `normal`: 1 turn traversal, standard weight.
  - `priority`: 1 turn traversal, receives a 10% path weight discount.
  - `restricted`: 2 turn traversal requiring intermediate transit and reservation lock.
  - `blocked`: Completely impassable; excluded during graph construction.
- **Interactive 2D Pygame GUI:** Adaptive, resizable graphical interface built with `pygame-ce` featuring real-time animation and HUD telemetry.
- **Performance Telemetry (`--statistics`):** Built-in analytical metrics providing total mission turns, average turns per drone, and average drone throughput per turn.
- **Robust Error Diagnostics & Deadlock Detection:** Detects unreachable targets, syntax/structural config errors, and traffic deadlocks with clean ANSI terminal reporting.

---

## 📦 Requirements & Installation

### Requirements

- **Python:** Version `3.10` to `3.14`
- **Dependency Manager:** [Poetry](https://python-poetry.org/docs/)
- **Display Server:** Graphical environment (X11 / Wayland / macOS / Windows) for GUI mode; terminal mode runs headlessly anywhere.

### Installation

Clone the repository and install the project dependencies using Poetry:

```bash
# Clone the repository
git clone https://github.com/mdurte-s/flyin.git
cd flyin

# Install dependencies via Makefile (calls poetry install)
make install
```

Alternatively, invoke Poetry directly:

```bash
poetry install
```

---

## 🚀 Quickstart & Usage

The project provides both a rich graphical interface and a high-speed terminal mode. You can execute simulations either through the convenient `Makefile` targets or directly via `poetry run python main.py`.

### 1. Graphical Mode (GUI)

Launch the visual simulation window with animated drones and live telemetry:

```bash
# Run default map with GUI
make display

# Run a specific map with GUI
make display MAP=maps/medium/03_priority_puzzle.txt

# Or run directly via Poetry
poetry run python main.py maps/hard/01_maze_nightmare.txt --gui
```

### 2. Terminal / CLI Mode

Run headlessly in the terminal to inspect turn-by-turn text movements:

```bash
# Run default map in terminal
make run

# Run a specific map
make run MAP=maps/easy/01_linear_path.txt

# Or run directly via Poetry
poetry run python main.py maps/easy/01_linear_path.txt
```

### 3. Simulation Statistics Mode

Compute and display comprehensive traffic performance metrics at the end of the run:

```bash
# Run with performance statistics via Makefile
make statistics MAP=maps/medium/03_priority_puzzle.txt

# Or run directly via Poetry
poetry run python main.py maps/challenger/01_the_impossible_dream.txt --statistics
```

---

## 🛠️ CLI Reference & Make Targets

### Command Line Arguments

```text
python main.py <map_path> [--gui | --statistics]
```

| Argument / Flag | Type | Description |
| :--- | :--- | :--- |
| `<map_path>` | Positional (Required) | Path to the map configuration file (e.g. `maps/easy/01_linear_path.txt`). |
| `--gui` | Flag (Optional) | Opens the interactive Pygame 2D animated graphical window. |
| `--statistics` | Flag (Optional) | Prints summary telemetry (total turns, average turns/drone, drones/turn). |

> [!NOTE]
> `--gui` and `--statistics` are mutually exclusive CLI arguments in the runner. Running without flags defaults to clean terminal execution.

### Makefile Targets

| Target | Description | Example |
| :--- | :--- | :--- |
| `make install` | Installs project dependencies using Poetry. | `make install` |
| `make run` | Runs simulation in terminal mode (default or `MAP=...`). | `make run MAP=maps/easy/02_simple_fork.txt` |
| `make display` | Runs simulation in animated Pygame GUI mode. | `make display MAP=maps/medium/01_dead_end_trap.txt` |
| `make statistics`| Runs simulation and outputs performance statistics. | `make statistics MAP=maps/hard/02_capacity_hell.txt` |
| `make debug` | Launches the interactive Python debugger (`pdb`). | `make debug MAP=maps/easy/01_linear_path.txt` |
| `make lint` | Validates code style and types with `flake8` and `mypy`. | `make lint` |
| `make lint-strict`| Runs strict type verification (`mypy --strict`). | `make lint-strict` |
| `make clean` | Cleans Python bytecode and cache directories. | `make clean` |

---

## 🗺️ Map Format & Configuration

Maps are plain text files defining drone counts, hub positions, zone rules, and connections. Lines beginning with `#` and blank lines are ignored.

### Directive Grammar

```text
nb_drones: <positive_integer>
start_hub: <name> <x> <y> [optional_criteria]
end_hub: <name> <x> <y> [optional_criteria]
hub: <name> <x> <y> [optional_criteria]
connection: <hub1>-<hub2> [optional_criteria]
```

### Configurable Attributes

| Element | Parameter | Allowed Values | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Hub** | `zone` | `normal`, `priority`, `restricted`, `blocked` | `normal` | Movement cost and routing behavior. |
| **Hub** | `color` | Named color (`blue`, `red`, `green`, `yellow`, `pink`, etc.) | `blue` | Circle render color in GUI. |
| **Hub** | `max_drones`| Positive integer | `1` | Maximum simultaneous drone occupancy (ignored for `end_hub`). |
| **Connection** | `max_link_capacity` | Positive integer | `1` | Maximum drones allowed to cross the edge simultaneously in a turn. |

### Zone Rules Summary

- **`normal` (Cost: 1 turn):** Standard movement corridor.
- **`priority` (Cost: 1 turn):** Preferred transit route; PathFinder applies a **10% cost discount** during path computation.
- **`restricted` (Cost: 2 turns):** Slow zone requiring 2 turns to enter. On turn 1, the drone enters transit and reserves its target spot; on turn 2, the arrival completes.
- **`blocked` (Cost: ∞):** Completely inaccessible zone; skipped during graph construction.

### Example Map File

```text
# Configuration: Priority Puzzle
nb_drones: 5

start_hub: start 0 0 [color=green]
hub: slow_path1 1 -1 [zone=restricted color=red]
hub: slow_path2 2 -1 [color=red]
hub: fast_junction 1 0 [zone=priority color=blue max_drones=2]
hub: fast_path 2 0 [zone=priority color=blue]
hub: merge_point 3 0 [color=yellow max_drones=3]
end_hub: goal 4 0 [color=green]

connection: start-slow_path1
connection: start-fast_junction
connection: slow_path1-slow_path2
connection: slow_path2-merge_point
connection: fast_junction-fast_path
connection: fast_path-merge_point
connection: merge_point-goal [max_link_capacity=2]
```

---

## 🧠 Routing Algorithm & Simulation Engine

The engine models the network as a bidirectional weighted graph and coordinates drones turn by turn:

```
┌──────────────┐     ┌──────────────┐     ┌───────────────────────┐     ┌────────────────────┐
│  Map Parser  │ ──> │ Graph Models │ ──> │ Multi-Path Dijkstra   │ ──> │ Simulation Engine  │
│ (.txt file)  │     │ (Hubs/Links) │     │ (Iterative Penalties) │     │ (Discrete Turns)   │
└──────────────┘     └──────────────┘     └───────────────────────┘     └─────────┬──────────┘
                                                                                  │
                                                ┌─────────────────────────────────┴─────────────────┐
                                                ▼                                                   ▼
                                     ┌─────────────────────┐                             ┌─────────────────────┐
                                     │   CLI Log Stream    │                             │ Pygame 2D GUI HUD   │
                                     └─────────────────────┘                             └─────────────────────┘
```

1. **Adjacency Construction:** Bidirectional links are established while omitting any inbound connections to `blocked` hubs.
2. **Dijkstra Pathfinding with Node Penalties:**
   - The pathfinder runs Dijkstra's algorithm with a min-priority queue to identify the lowest-cost path.
   - Priority hubs receive a 10% weight discount (`weight * 0.9`).
   - To discover alternative non-overlapping or semi-independent paths, an iterative penalty of `+5.0` is added to intermediate hubs of chosen paths, repeating for up to 4 candidate routes.
3. **Round-Robin Drone Dispatch:**
   - Drones are distributed across discovered candidate paths in a round-robin schedule (`drone_id % len(paths)`).
4. **Turn Execution & Collision Prevention:**
   - Every turn, active drones verify that the target hub has available capacity (`occupancy + spots_reserved < max_drones`) and that the connection has remaining capacity (`link_capacity < max_link_capacity`).
   - For `restricted` hubs, transit is split over 2 turns, locking a reservation slot during intermediate flight.
   - Connection throughput resets each turn.
   - If active drones remain but none can move, the engine cleanly halts and flags a **Deadlock Error**.

---

## 🏆 Benchmark Suite & Challenge Maps

The [`maps/`](maps/) directory includes test scenarios graded by difficulty to evaluate routing efficiency and edge-case handling:

| Category | Maps | Highlights & Key Challenges |
| :--- | :--- | :--- |
| 🟢 **Easy** | `01_linear_path.txt`<br>`02_simple_fork.txt`<br>`03_basic_capacity.txt` | Basic connectivity, path splitting, and initial capacity constraints (2–4 drones). |
| 🟡 **Medium** | `01_dead_end_trap.txt`<br>`02_circular_loop.txt`<br>`03_priority_puzzle.txt` | Dead-end trap avoidance, cyclic loops, and priority zone cost optimization (5–6 drones). |
| 🔴 **Hard** | `01_maze_nightmare.txt`<br>`02_capacity_hell.txt`<br>`03_ultimate_challenge.txt` | Multi-path mazes, extreme bottleneck timing, and comprehensive stress testing (8–15 drones). |
| ⚫ **Challenger** | `01_the_impossible_dream.txt` | Research-grade stress test featuring 25 drones and dense constraints.<br>🏆 **Reference Record to Beat: 45 turns**. |

See [`maps/README.md`](maps/README.md) for full descriptions, design rationale, and benchmark details.

---

## 📂 Project Architecture

```text
flyin/
├── display/                     # Graphical interface
│   ├── __init__.py
│   └── gui_display.py           # Pygame 2D renderer, HUD, interpolation & event handling
├── models/                      # Domain graph entities
│   ├── __init__.py
│   ├── connection.py            # Edge representation & per-turn capacity tracking
│   ├── drone.py                 # Drone state, trajectory status & turn accounting
│   └── hub.py                   # Node attributes, zone classifications & occupancy
├── parsing/                     # Map ingestion & validation
│   ├── __init__.py
│   ├── config.py                # Tokenizer, type parsers & configuration store
│   ├── config_error.py          # Syntax and structural validation exceptions
│   └── map_parser.py            # Orchestrator for file reading and validation
├── simulation/                  # Core simulation and routing
│   ├── __init__.py
│   ├── pathfinding.py           # Dijkstra pathfinding with iterative node penalties
│   ├── simulation_engine.py     # Turn progression, collision checking & deadlock detection
│   └── simulation_error.py      # Simulation and routing runtime exceptions
├── utils/                       # Shared helpers and terminal formatting
│   ├── __init__.py
│   └── utils.py                 # ANSI styling, error formatting, and colored labels
├── maps/                        # Challenge and benchmark map suite
├── main.py                      # Main entrypoint & CLI argument router
├── Makefile                     # Build, run, display, lint, and test shortcuts
└── pyproject.toml               # Poetry dependencies and package configuration
```

---

## 📊 Sample Outputs

### Standard Terminal Simulation (`make run`)

```text
1. configuration file parsing: [OK]

2. starting engine: [OK]

3. running engine:

Turn 1: D1-waypoint1
Turn 2: D1-waypoint2 D2-waypoint1
Turn 3: D1-goal D2-waypoint2
Turn 4: D2-goal

[OK] ✅

SUCCESS!
YOU MAKE THE CAT VERY HAPPY 😻 
```

### Telemetry & Statistics Mode (`make statistics`)

```text
1. configuration file parsing: [OK]

2. starting engine: [OK]

3. running engine:

Turn 1: D1-fast_junction D2-slow_path1
Turn 2: D1-fast_path D2-slow_path1-slow_path2 D3-fast_junction
Turn 3: D1-merge_point D2-slow_path2 D3-fast_path D4-fast_junction
Turn 4: D1-goal D2-merge_point D3-merge_point D4-fast_path D5-fast_junction
...

[OK] ✅

4. Statistics:
 • Total turns: 9
 • Average turns per drone: 5
 • Average drones per turn: 3

SUCCESS!
YOU MAKE THE CAT VERY HAPPY 😻 
```

---

## 📚 Resources

- [Python Documentation](https://docs.python.org/3/) — Language specification and standard library reference.
- [pygame-ce Documentation](https://pyga.me/docs/) — Pygame Community Edition rendering, event loop, and vector drawing APIs.
- [Poetry Documentation](https://python-poetry.org/docs/) — Packaging and virtual environment management.
- [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) — Shortest-path routing in weighted directed/undirected graphs.
- [`maps/README.md`](maps/README.md) — Comprehensive guide to the challenge suite maps and benchmarks.

### AI Usage Disclosure

In compliance with 42 school guidelines, AI assistance was used to analyze the codebase structure, review and correct CLI/Makefile command documentation, format markdown components, and draft comprehensive documentation for the simulation engine and visualization features. Core algorithmic logic, simulation mechanics, and map definitions represent the original work of the author.
