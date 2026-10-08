from ..models import Hub, Drone
from ..parsing import Config
from .pathfinding import PathFinder
from .simulation_error import PathFindingError


class SimulationEngine:
    """ Simulation engine responsible for forwarding the drones shift
    by shift. """

    def __init__(self, cfg: Config) -> None:
        self._cfg: Config = cfg
        self._hubs: list[Hub] = cfg._hubs
        self._start_hub: Hub = self._hubs[0]
        self._end_hub: Hub = self._hubs[-1]
        self._drones: list[Drone] = [
            Drone(id=i + 1, start_hub=self._start_hub)
            for i in range(cfg._nb_drones)
        ]
        self._nb_turns: int = 0

    def run(self) -> None:
        """ Run the simulation until all drones reach the destination. """
        p_finder: PathFinder = PathFinder(self._hubs, self._cfg._connections)
        paths: list[list[Hub]] = p_finder.find_paths(
            self._start_hub.name, self._end_hub.name, 5
            )
        if not paths[0]:
            raise PathFindingError("No valid path found")

        self._simulate(paths)

    def _simulate(self, paths: list[list[Hub]]) -> None:
        """ Manages the movement of drones along multiple paths. """
        # Mapeia cada hub para o seu próximo hub no caminho
        path = paths[0]
        next_hub_map: dict[str, Hub] = {
            path[i].name: path[i + 1] for i in range(len(path) - 1)
        }

        # Controlo de ocupação atual dos hubs
        hub_occupancy: dict[str, int] = {h.name: 0 for h in self._hubs}
        for drone in self._drones:
            if drone.current_hub.name != self._start_hub.name:
                hub_occupancy[drone.current_hub.name] += 1

        active_drones = list(self._drones)

        while active_drones:
            turn_movements: list[str] = []
            moved_in_this_turn: set = set()

            # Processar drones que já se moveram para que libertem espaço nos
            # hubs
            for drone in active_drones:
                current_name = drone.current_hub.name

                if current_name in next_hub_map:
                    target_hub = next_hub_map[current_name]
                    target_name = target_hub.name

                    # Verificar capacidade do hub de destino (start e end_hub
                    # têm capacidade ilimitada)
                    is_end = (target_name == self._end_hub.name)
                    has_capacity = (
                        is_end or
                        hub_occupancy[target_name] < target_hub.max_drones
                    )

                    if has_capacity and drone.name not in moved_in_this_turn:
                        # Libertar capacidade do hub atual
                        # (exceto no start_hub)
                        if current_name != self._start_hub.name:
                            hub_occupancy[current_name] -= 1

                        # Mover o drone
                        drone._current_hub = target_hub
                        if not is_end:
                            hub_occupancy[target_name] += 1
                        else:
                            drone._arrived = True

                        moved_in_this_turn.add(drone.name)
                        turn_movements.append(f"{drone.name}-{target_name}")

            # Remover drones entregues no objetivo
            active_drones = [d for d in active_drones if not d._arrived]

            if turn_movements:
                self._nb_turns += 1
                print(" ".join(turn_movements))
            else:
                # Evitar loop infinito em caso de bloqueio total
                break
