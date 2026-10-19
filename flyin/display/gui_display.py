import sys
import time
import pygame
from ..models import Hub, Drone, Graph


class SimulationGUI:
    """Renders the 2D visual simulation using Pygame with adaptive scaling."""

    COLOR_MAP: dict[str, tuple[int, int, int]] = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "blue": (130, 165, 180),
        "red": (225, 115, 125),
        "green": (145, 188, 148),
        "purple": (160, 148, 190),
        "yellow": (225, 220, 110),
        "orange": (225, 165, 110),
        "cyan": (130, 198, 200),
        "magenta": (205, 115, 155),
        "gold": (210, 185, 95),
        "brown": (160, 125, 95),
        "lime": (155, 210, 155),
        "pink": (225, 160, 175),
        "grey": (30, 30, 30)
    }

    MIN_WIDTH, MIN_HEIGHT = 800, 600
    MAX_WIDTH, MAX_HEIGHT = 1920, 1080

    def __init__(
            self, graph: Graph, drones: list[Drone],
            width: int = 800, height: int = 600,
            animation_speed: float = 0.5
            ) -> None:
        pygame.init()
        pygame.font.init()

        self._graph: Graph = graph
        self._hubs: list[Hub] = list(self._graph.hubs.values())
        self._width: int = max(self.MIN_WIDTH, min(width, self.MAX_WIDTH))
        self._height: int = max(self.MIN_HEIGHT, min(height, self.MAX_HEIGHT))

        self._screen: pygame.Surface = pygame.display.set_mode(
            (self._width, self._height), pygame.RESIZABLE
        )
        pygame.display.set_caption("Fly-in Simulation")

        try:
            self._font: pygame.font.Font = pygame.font.SysFont(
                "Arial", 11, bold=True
            )
            self._title_font: pygame.font.Font = pygame.font.SysFont(
                "Arial", 20, bold=True
            )
        except Exception:
            self._font = pygame.font.Font(None, 14)
            self._title_font = pygame.font.Font(None, 24)

        self._is_finished: bool = False
        self._start_time: float = time.time()
        self._turn_start_time: float = time.time()
        self._final_time: float | None = None
        self._animation_speed: float = animation_speed
        self._current_turn: int = 0
        self._drones: list[Drone] = drones

        self._drone_positions: dict[str, tuple[float, float]] = {
            drone.name: drone.current_hub.coordinates for drone in drones
        }
        self._drone_trajectories: dict[
            str, tuple[tuple[float, float], tuple[float, float]]
            ] = {}

        self._min_x: float = 0.0
        self._max_x: float = 1.0
        self._min_y: float = 0.0
        self._max_y: float = 1.0

        self._update_coordinate_bounds()

    @property
    def _is_small_window(self) -> bool:
        """Check if window size is below threshold for compact display."""
        return self._width < 1000 or self._height < 700

    @property
    def _hub_radius(self) -> int:
        """ Calculate hub radius based on screen size
        (12px for small, 20px for normal).
        """
        return 12 if self._is_small_window else 20

    @property
    def _connection_thickness(self) -> int:
        """Connection thickness is strictly equal to the diameter of the hub.
        """
        return self._hub_radius * 2

    def update_simulation_state(
            self, turn: int, drones: list[Drone]
            ) -> None:
        """ Calculate start and end coordinates for every active drone this
        turn."""
        self._current_turn = turn
        self._turn_start_time = time.time()

        for drone in drones:
            start_coords = self._drone_positions.get(
                drone.name, drone.current_hub.coordinates
            )

            if drone.is_in_intermediate_transit and drone.in_transit_to:
                dest_coords = drone.in_transit_to.coordinates
                end_coords = (
                    (start_coords[0] + dest_coords[0]) / 2.0,
                    (start_coords[1] + dest_coords[1]) / 2.0
                )
            elif drone.in_transit_to:
                end_coords = drone.in_transit_to.coordinates
            else:
                end_coords = drone.current_hub.coordinates

            self._drone_trajectories[drone.name] = (start_coords, end_coords)

    def animate_turn(self, clock: pygame.time.Clock, fps: int = 60) -> bool:
        """Smoothly render frames and finalize drone arrival coordinates."""
        while True:
            elapsed = time.time() - self._turn_start_time

            if not self.render_frame():
                return False
            clock.tick(fps)

            if elapsed >= self._animation_speed:
                break

        for d in self._drones:
            if d.name in self._drone_trajectories:
                _, end_coords = self._drone_trajectories[d.name]
                self._drone_positions[d.name] = end_coords

        return True

    def mark_completed(self) -> None:
        """ Freeze timer when all drones arrive at goal. """
        if not self._is_finished:
            self._is_finished = True
            self._final_time = time.time() - self._start_time

    def _get_drone_current_pixel_pos(self, drone: Drone) -> tuple[int, int]:
        """ Interpolate real-time pixel position between start and end hubs.
        """
        if drone.name not in self._drone_trajectories:
            return self._map_to_screen(*drone.current_hub.coordinates)

        start_coords, end_coords = self._drone_trajectories[drone.name]

        pos_start = self._map_to_screen(*start_coords)
        pos_end = self._map_to_screen(*end_coords)

        elapsed = time.time() - self._turn_start_time
        t = min(1.0, max(0.0, elapsed / self._animation_speed))

        curr_x = int(pos_start[0] + (pos_end[0] - pos_start[0]) * t)
        curr_y = int(pos_start[1] + (pos_end[1] - pos_start[1]) * t)

        return curr_x, curr_y

    def _update_coordinate_bounds(self) -> None:
        """Calculate graph bounds with independent non-uniform scaling."""
        x_coords = [hub.coordinates[0] for hub in self._graph.hubs.values()]
        y_coords = [hub.coordinates[1] for hub in self._graph.hubs.values()]

        if not x_coords or not y_coords:
            return

        min_x, max_x = float(min(x_coords)), float(max(x_coords))
        min_y, max_y = float(min(y_coords)), float(max(y_coords))

        range_x = max(1.0, max_x - min_x)
        range_y = max(1.0, max_y - min_y)

        margin_x = max(0.8, range_x * 0.04)
        margin_y = max(0.4, range_y * 0.10)

        self._min_x = min_x - margin_x
        self._max_x = max_x + margin_x
        self._min_y = min_y - margin_y
        self._max_y = max_y + margin_y

    def _map_to_screen(self, x: float, y: float) -> tuple[int, int]:
        """Convert Cartesian points to pixel window coordinates."""
        margin_x = 50
        margin_y = 100

        draw_w = self._width - 2 * margin_x
        draw_h = self._height - 2 * margin_y

        range_x = self._max_x - self._min_x
        range_y = self._max_y - self._min_y

        scale_x = draw_w / range_x if range_x > 0 else 1.0
        scale_y = draw_h / range_y if range_y > 0 else 1.0

        screen_x = int(margin_x + (x - self._min_x) * scale_x)
        screen_y = int(self._height - margin_y - (y - self._min_y) * scale_y)

        return screen_x, screen_y

    def _get_rgb_color(
            self, color_name: str, default: tuple[int, int, int]
            ) -> tuple[int, int, int]:
        """Convert color name string to an RGB tuple."""
        return self.COLOR_MAP.get(color_name.lower(), default)

    def _draw_connections(self) -> None:
        """Draw connection lines with thickness matching the hub diameter."""
        thickness = self._connection_thickness

        for conn in self._graph.connections:
            pos1 = self._map_to_screen(*conn.hub1.coordinates)
            pos2 = self._map_to_screen(*conn.hub2.coordinates)

            zones = {conn.hub1.zone, conn.hub2.zone}

            if "blocked" in zones:
                pygame.draw.line(
                    self._screen, self.COLOR_MAP["red"], pos1, pos2,
                    thickness
                )
            elif "restricted" in zones:
                pygame.draw.line(
                    self._screen, self.COLOR_MAP["yellow"], pos1, pos2,
                    thickness
                )
            elif "priority" in zones:
                pygame.draw.line(
                    self._screen, self.COLOR_MAP["green"], pos1, pos2,
                    thickness
                )
            else:
                pygame.draw.line(
                    self._screen, self.COLOR_MAP["white"], pos1, pos2,
                    thickness
                )

    def _should_hide_label(self) -> bool:
        """ Determines if labels will overlap based on window size and
        node density. """
        if self._width >= 1000 and self._height >= 750:
            return False

        if len(self._hubs) < 2:
            return False

        min_pixel_distance = float("inf")
        for conn in self._graph.connections:
            pos1 = self._map_to_screen(*conn.hub1.coordinates)
            pos2 = self._map_to_screen(*conn.hub2.coordinates)

            dx = abs(pos1[0] - pos2[0])
            if 0 < dx < min_pixel_distance:
                min_pixel_distance = dx

        sample_label = self._hubs[0].name
        lable_pixel_width = self._font.size(sample_label)[0]

        return bool(min_pixel_distance < lable_pixel_width + 10)

    def _draw_hubs(self) -> None:
        """ Draw hub circles and conditionally render names based on window
        size. """
        radius: int = self._hub_radius
        show_names: bool = not self._should_hide_label()

        for i, hub in enumerate(self._hubs):
            pos = self._map_to_screen(*hub.coordinates)
            hub_color = self._get_rgb_color(hub.color, self.COLOR_MAP["blue"])

            # Outer boundary and filled circle
            pygame.draw.circle(self._screen, hub_color, pos, radius)
            pygame.draw.circle(self._screen, hub_color, pos, radius, 2)

            # Only draw hub names if the window is large enough
            if show_names:
                offset_pattern = [-32, 32, -44, 44]
                y_offset = offset_pattern[i % len(offset_pattern)]

                text_surf = self._font.render(
                    hub.name, True, self.COLOR_MAP["grey"]
                    )
                text_rect = text_surf.get_rect(
                    center=(pos[0], pos[1] + y_offset)
                    )
                self._screen.blit(text_surf, text_rect)

    def _draw_square_drone(
            self, pos: tuple[int, int]
            ) -> None:
        """Draw drone square scaled proportionally to the hub radius."""
        size = int(self._hub_radius * 0.6)
        x, y = pos
        points = [
            (x - size, y + size),
            (x - size, y - size),
            (x + size, y - size),
            (x + size, y + size),
        ]
        pygame.draw.polygon(self._screen, (65, 90, 130), points)
        pygame.draw.polygon(self._screen, (65, 90, 130), points, 1)

    def _draw_drones(self) -> None:
        """ Render drones at interpolated flight coordinates. """
        for drone in self._drones:
            pos = self._get_drone_current_pixel_pos(drone)
            self._draw_square_drone(pos)

            if not self._should_hide_label():
                label = self._font.render(
                    drone.name, True, self.COLOR_MAP["white"]
                )
                self._screen.blit(label, (pos[0] - 8, pos[1] - 5))

    def _draw_info(self) -> None:
        """Display elapsed time and turn count."""
        if self._is_finished and self._final_time is not None:
            elapsed_time = self._final_time
        else:
            elapsed_time = time.time() - self._start_time
        time_str = f"Elapsed time: {elapsed_time:.1f} s"
        turn_str = f"Turns: {self._current_turn}"

        time_ = self._title_font.render(time_str, True, self.COLOR_MAP["grey"])
        turn_ = self._title_font.render(turn_str, True, self.COLOR_MAP["grey"])

        self._screen.blit(time_, (20, 20))
        self._screen.blit(turn_, (20, 50))

    def render_frame(self) -> bool:
        """ Process Pygame events and adjust to window resize bounds. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            elif event.type == pygame.VIDEORESIZE:
                self._width = max(self.MIN_WIDTH, min(event.w, self.MAX_WIDTH))
                self._height = max(
                    self.MIN_HEIGHT, min(event.h, self.MAX_HEIGHT)
                    )
                self._screen = pygame.display.set_mode(
                    (self._width, self._height), pygame.RESIZABLE
                )

        self._screen.fill((193, 225, 193))
        self._draw_connections()
        self._draw_hubs()
        self._draw_drones()
        self._draw_info()

        pygame.display.flip()
        return True
