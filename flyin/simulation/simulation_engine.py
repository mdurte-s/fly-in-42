import sys
import pygame
from typing import Any
from ..models import Hub, Connection, Drone, Graph
from ..parsing import Config
from ..display import SimulationGUI
from .pathfinding import PathFinder
from .simulation_error import SimulationError, PathFindingError


class SimulationEngine:
    """Simulation engine responsible for forwarding the drones turn by turn."""

    def __init__(self, cfg: Config, enable_gui: bool = True) -> None:
        self._cfg: Config = cfg
        self._hubs: list[Hub] = cfg.hubs
        self._connections: dict[int, Connection] = {
            conn.id: conn for conn in cfg.connections
            }

        self._start_hub: Hub = self._hubs[0]
        self._end_hub: Hub = self._hubs[-1]

        self._drones: list[Drone] = [
            Drone(id=i + 1, start_hub=self._start_hub)
            for i in range(cfg.nb_drones)
        ]

        self._nb_turns: int = 0
        self._turn_movements: list[str] = []
        self._moved_in_this_turn: set[str] = set()

        self._graph: Graph = Graph.from_config(cfg)
        self._display: SimulationGUI | None = None

        if enable_gui:
            self._display = SimulationGUI(self._graph, self._drones)

    def run(self) -> None:
        """Run the simulation until all drones reach the destination."""
        p_finder: PathFinder = PathFinder(
            self._hubs, list(self._connections.values())
        )

        paths: list[list[Hub]] = p_finder.find_paths(
            self._start_hub.name,
            self._end_hub.name,
            5
        )

        if not paths or not paths[0]:
            raise PathFindingError("No valid path found")

        self._simulate(paths)

    def _simulate(self, paths: list[list[Hub]]) -> None:
        """ Manages the movement of drones along multiple paths concurrently.
        """

        next_hub_maps: list[dict[str, Hub]] = [
            {path[i].name: path[i + 1] for i in range(len(path) - 1)}
            for path in paths
        ]

        for drone_id, drone in enumerate(self._drones):
            drone.set_path_id(drone_id % len(paths))

        active_drones: list[Drone] = list(self._drones)
        clock = pygame.time.Clock()

        if isinstance(self._display, SimulationGUI):
            self._display.update_simulation_state(self._nb_turns, self._drones)
            self._display.render_frame()

        while active_drones:
            self._init_new_turn()

            for drone in active_drones:

                if drone.turns_remaining == 1 and drone.in_transit_to:
                    self._drone_turn_to_target(drone)
                    continue

                current: Hub = drone.current_hub
                assigned_map: dict[str, Hub] = next_hub_maps[drone.path_id]

                if current.name in assigned_map:
                    target: Hub = assigned_map[current.name]
                    id: int = self._find_conn_id(current.name, target.name)
                    conn: Connection = self._connections[id]

                    turn_available: bool = (
                        (target.name == self._end_hub.name or
                         target.occupancy < target.max_drones) and
                        drone.name not in self._moved_in_this_turn and
                        conn.link_capacity < conn.max_link_capacity
                    )

                    if turn_available:
                        drone.set_turns_remaining(max(1, target.cost))
                        drone.set_in_transit_to(target)

                        if current.name != self._start_hub.name:
                            current.set_occupancy(current.occupancy - 1)

                        if target.name != self._end_hub.name:
                            target.set_occupancy(target.occupancy + 1)

                        if drone.turns_remaining == 2:
                            self._first_drone_turn_to_restricted_target(drone)
                        else:
                            self._drone_turn_to_target(drone)

            if self._turn_movements:
                self._show_turn_movements(clock)

            active_drones = [d for d in active_drones if d.is_active]
            if not active_drones:
                break

        if isinstance(self._display, SimulationGUI):
            self._end_display(clock)

    def _drone_turn_to_target(self, drone: Drone) -> None:
        current: Hub = drone.current_hub
        target: Hub | None = drone.in_transit_to

        if isinstance(target, Hub):
            id: int = self._find_conn_id(current.name, target.name)

            self._turn_movements.append(f"{drone.name}-{target.name}")
            self._moved_in_this_turn.add(drone.name)

            drone.set_current_hub(target)
            drone.set_in_transit_to(None)
            drone.set_turns_remaining(0)

            if (target.name == self._end_hub.name):
                drone.set_arrived(True)

            self._connections[id].increase_link()

        else:
            raise SimulationError()

    def _first_drone_turn_to_restricted_target(self, drone: Drone) -> None:
        current: Hub = drone.current_hub
        target: Hub | None = drone.in_transit_to

        if isinstance(target, Hub):
            id: int = self._find_conn_id(current.name, target.name)

            self._turn_movements.append(
                f"{drone.name}-{current.name}-{target.name}"
                )
            self._moved_in_this_turn.add(drone.name)

            drone.set_turns_remaining(1)

            self._connections[id].increase_link()

        else:
            raise SimulationError()

    def _init_new_turn(self) -> None:
        self._turn_movements = []
        self._moved_in_this_turn = set()

        for conn in self._connections.values():
            conn.reset_link()

    def _show_turn_movements(self, clock: Any) -> None:
        self._nb_turns += 1
        print(" ".join(self._turn_movements))

        if isinstance(self._display, SimulationGUI):
            self._display.update_simulation_state(
                self._nb_turns, self._drones
            )
            self._display.animate_turn(clock, fps=60)

    def _end_display(self, clock: Any) -> None:

        if isinstance(self._display, SimulationGUI):
            self._display.mark_completed()
            self._display.update_simulation_state(self._nb_turns, self._drones)

            print("\nSimulation complete. Close the GUI window to exit.")

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)

                self._display.render_frame()
                clock.tick(30)

        else:
            raise SimulationError()

    def _find_conn_id(self, hub_a: str, hub_b: str) -> int:

        for connection in self._connections.values():
            if {hub_a, hub_b} == {connection.hub1.name, connection.hub2.name}:
                return connection.id

        raise SimulationError()
