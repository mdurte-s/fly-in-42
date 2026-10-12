import time
import pygame
from sys import exit
from ..models import Hub, Drone, Graph
from ..parsing import Config
from ..display import SimulationGUI
from .pathfinding import PathFinder
from .simulation_error import PathFindingError


class SimulationEngine:
    """ Simulation engine responsible for forwarding the drones shift
    by shift. """

    def __init__(self, cfg: Config, enable_gui: bool = True) -> None:
        self._cfg: Config = cfg
        self._hubs: list[Hub] = cfg.hubs
        self._connections: list[Hub] = cfg.connections
        self._start_hub: Hub = self._hubs[0]
        self._end_hub: Hub = self._hubs[-1]
        self._drones: list[Drone] = [
            Drone(id=i + 1, start_hub=self._start_hub)
            for i in range(cfg._nb_drones)
        ]
        self._nb_turns: int = 0

        self._graph: Graph = Graph.from_config(cfg)
        self._enable_gui: bool = enable_gui
        self._display: SimulationGUI | None = None

        if self._enable_gui:
            self._display = SimulationGUI(self._graph)

    def run(self) -> None:
        """ Run the simulation until all drones reach the destination. """
        p_finder: PathFinder = PathFinder(self._hubs, self._connections)
        paths: list[list[Hub]] = p_finder.find_paths(
            self._start_hub.name, self._end_hub.name, 5
            )
        if not paths[0]:
            raise PathFindingError("No valid path found")

        self._simulate(paths)

    def _simulate(self, paths: list[list[Hub]]) -> None:
        """ Manages the movement of drones along multiple paths.
        (we wish) """
        path = paths[0]
        next_hub_map: dict[str, Hub] = {
            path[i].name: path[i + 1] for i in range(len(path) - 1)
        }
        hub_occupancy: dict[str, int] = {h.name: 0 for h in self._hubs}
        for drone in self._drones:
            if drone.current_hub.name != self._start_hub.name:
                hub_occupancy[drone.current_hub.name] += 1

        active_drones = list(self._drones)
        clock = pygame.time.Clock()

        if self._display:
            self._display.update_simulation_state(self._nb_turns, self._drones)
            self._display.render_frame()
            time.sleep(0.5)

        while active_drones:
            turn_movements: list[str] = []
            moved_in_this_turn: set = set()

            for drone in active_drones:
                current_name = drone.current_hub.name

                if current_name in next_hub_map:
                    target_hub = next_hub_map[current_name]
                    target_name = target_hub.name

                    # check hub cap
                    is_end = (target_name == self._end_hub.name)
                    has_capacity = (
                        is_end or
                        hub_occupancy[target_name] < target_hub.max_drones
                    )

                    if has_capacity and drone.name not in moved_in_this_turn:
                        if current_name != self._start_hub.name:
                            hub_occupancy[current_name] -= 1

                        drone._current_hub = target_hub  # move th drone
                        if not is_end:
                            hub_occupancy[target_name] += 1
                        else:
                            drone._arrived = True

                        moved_in_this_turn.add(drone.name)
                        turn_movements.append(f"{drone.name}-{target_name}")

            active_drones = [d for d in active_drones if not d._arrived]

            if turn_movements:
                self._nb_turns += 1
                print(" ".join(turn_movements))

                if self._display:
                    self._display.update_simulation_state(
                        self._nb_turns, self._drones
                        )
                    running = self._display.render_frame()
                    if not running:
                        break
                    time.sleep(0.5)
            else:
                break

        if self._display:
            self._display.update_simulation_state(self._nb_turns, self._drones)

            print("\nSimulation complete. Close the GUI window to exit.")
            clock = pygame.time.Clock()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit(0)

                clock.tick(10)
