*This project has been created as part of the 42 curriculum by mdurte-s.*

# Fly-in

## Description

Fly-in simulates a fleet of drones traveling through a network of connected
hubs. Given a text map, the program plans routes from a start hub to a goal
and advances the drones turn by turn. It accounts for zone travel time,
per-hub capacity, and per-connection capacity, and can display the simulation
as an animated 2D graph.

The project is written in Python and uses Pygame Community Edition (pygame-ce)
for its visual interface. Example maps are grouped by difficulty and feature
in [`maps/`](maps/); see [`maps/README.md`](maps/README.md) for an overview of
the challenges.

## Instructions

### Requirements

- Python 3.10–3.14
- [Poetry](https://python-poetry.org/docs/) for dependency management
- A graphical environment for the default animated display. Use `--no-gui`
  to run the simulation in a terminal.

### Install

From the repository root:

```bash
make install
```

This runs `poetry install` and installs the project dependencies, including
pygame-ce.

### Run

Run the default map with the animated GUI:

```bash
make run
```

Choose another map by setting `MAP`:

```bash
make run MAP=maps/medium/01_dead_end_trap.txt
```

Run directly without the GUI:

```bash
poetry run python main.py maps/easy/01_linear_path.txt --no-gui
```

The `--cli` and `-t` options are aliases for `--no-gui`. Map files are plain
text: they define a positive drone count, a start hub, an end hub, optional
intermediate hubs, and connections between defined hubs. Blank lines and
lines beginning with `#` are ignored. Optional hub settings include
`zone`, `color`, and `max_drones`; connections support `max_link_capacity`.

For example:

```text
nb_drones: 1
start_hub: start 0 0
end_hub: goal 1 0
connection: start-goal [max_link_capacity=1]
```

Hub names cannot contain spaces or hyphens. Supported zones are `normal`,
`restricted`, `priority`, and `blocked`. Hub and link capacities must be
positive integers. The parser reports malformed maps and missing or
duplicate definitions as errors.

## Algorithm and implementation

The map parser validates the input and builds `Hub` and `Connection` objects.
The map is then treated as a bidirectional weighted graph:

1. **Build candidate routes.** `PathFinder` constructs an adjacency list and
   omits transitions into blocked hubs. It runs Dijkstra's algorithm using a
   min-priority queue to find a lowest-cost route. Entering a normal or
   priority hub costs one turn; entering a restricted hub costs two turns.
   Priority hubs receive a 10% weight discount.
2. **Encourage alternate routes.** After finding a route, the pathfinder adds
   a penalty of 5 to its intermediate hubs and searches again, repeating up
   to four times or until no route is found. These searches provide candidate
   routes; the penalties encourage alternatives but do not guarantee that all
   candidates are distinct.
3. **Assign drones.** The simulation assigns drones to candidate routes in
   round-robin order. Each turn, it processes active drones and checks that
   the next hub has room and that the connection has remaining capacity for
   that turn. The goal hub is not limited by the ordinary hub occupancy cap.
4. **Advance and report.** Drones move at most one connection per turn.
   Restricted hubs take two turns to enter; the destination is reserved
   during transit. Connection usage resets at the beginning of each turn.
   The program prints each turn's movements and ends when all drones reach
   the goal or reports an error, such as a deadlock when no drone can move.

This separates input validation, graph route selection, turn-by-turn
simulation, and rendering into the `parsing`, `simulation`, `models`, and
`display` packages.

## Visual representation

The optional Pygame window presents the map as a 2D network. Hub coordinates
determine their positions; the view scales the coordinate range to fit the
window and adapts when the window is resized.

- Hubs are circles, colored using their configured `color` (blue by default),
  with hub names when there is enough room.
- Connections are drawn between hubs. Normal connections are white,
  connections touching priority hubs are green, restricted ones are yellow,
  and connections touching blocked hubs are red.
- Drones are moving squares. Their positions are animated between hubs,
  making the turn-by-turn progress visible.
- An elapsed-time display and turn counter provide a live progress summary;
  the elapsed time freezes when the simulation completes.
- Hub and drone labels are hidden when the window is compact or the map is
  dense, reducing overlap and keeping the graph readable.

The visualization complements the terminal movement log: it makes route
choices, congestion, restricted-zone delays, and overall progress easier to
follow at a glance. Close the window after completion to exit.

## Example

Run the included two-drone linear map in terminal mode:

```bash
poetry run python main.py maps/easy/01_linear_path.txt --no-gui
```

The example has one route through `waypoint1` and `waypoint2`. Because each
ordinary hub has capacity one, the drones follow one another:

```text
D1-waypoint1
D1-waypoint2 D2-waypoint1
D1-goal D2-waypoint2
D2-goal

SUCCESS!
YOU MAKE THE CAT VERY HAPPY 😻
```

The program prints ANSI color codes in a normal terminal; they are omitted
from this example.

## Resources

- [Python documentation](https://docs.python.org/3/) — language and standard
  library reference.
- [Pygame documentation](https://www.pygame.org/docs/) — windowing, drawing,
  events, and animation APIs used by the display.
- [pygame-ce documentation](https://pyga.me/docs/) — documentation for the
  Pygame Community Edition dependency.
- [Poetry documentation](https://python-poetry.org/docs/) — dependency and
  virtual-environment management.
- [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
  — background on shortest paths in weighted graphs.
- [`maps/README.md`](maps/README.md) — included map categories, challenge
  types, and testing suggestions.

### AI usage

AI assistance was used to inspect and summarize the existing project
implementation and to draft this README, including the installation and
execution instructions, algorithm overview, GUI feature descriptions, and
example output. The implementation and map files were not generated or
modified as part of this documentation task.
