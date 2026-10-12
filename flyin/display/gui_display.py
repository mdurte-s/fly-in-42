import time
import pygame
from ..models import Drone, Graph


class SimulationGUI:
    """Renders the 2D visual simulation using Pygame. """

    COLOR_MAP: dict[str, tuple[int, int, int]] = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "red": (220, 53, 69),
        "green": (40, 167, 69),
        "blue": (0, 123, 255),
        "yellow": (255, 193, 7),
        "gray": (108, 117, 125),
        "cyan": (23, 162, 184),
        "orange": (253, 126, 20),
    }

    def __init__(
            self, graph: Graph, width: int = 800, height: int = 600
            ) -> None:
        """ Initialize the Pygame display and calculate coordinate scaling. """
        pygame.init()
        pygame.font.init()

        self._graph: Graph = graph
        self._width: int = width
        self._height: int = height
        self._screen: pygame.Surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Fly-in Simulation")
        print("[GUI DEBUG] Window Created Successfully!")

        self._font: pygame.font.Font = pygame.font.SysFont("Arial", 18)
        self.title_font: pygame.font.Font = pygame.font.SysFont(
            "Arial", 22, bold=True
            )

        self._start_time: float = time.time()
        self._current_time: int = 0
        self._drones: list[Drone] = []

        self._padding: int = 100
        self._min_x = 0
        self._max_x = 1
        self._min_y = 0
        self._max_y = 1
        self._update_coordinate_bounds()

    def _update_coordinate_bounds(self) -> None:
        """ Update Graph bounds to scale cartesian points onto the window """
        x_coords = [hub.coordinates[0] for hub in self._graph.hubs.values()]
        y_coords = [hub.coordinates[1] for hub in self._graph.hubs.values()]

        if not x_coords or not y_coords:
            return

        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)

        self._min_x = min_x - 1 if min_x == max_x else min_x
        self._max_x = max_x + 1 if max_x == min_x else max_x
        self._min_y = min_y - 1 if min_y == max_y else min_y
        self._max_y = max_y + 1 if max_y == min_y else max_y

    def update_simulation_state(
            self, turn: int, drones: list[Drone]
            ) -> None:
        """ Update the dynamic simulation values for real-time rendering.
        """
        self.current_turn = turn
        self.drones = drones

    def _map_to_screen(self, x: float, y: float) -> tuple[int, int]:
        """ Converts graph cartesian coordinates to screen pixel coordinates.
        """
        margin = 100
        draw_width = self._width - 2 * margin
        draw_height = self._height - 2 * margin

        range_x = self._max_x - self._min_x
        range_y = self._max_y - self._min_y

        scale_x = draw_width / range_x if range_x > 0 else draw_width
        scale_y = draw_height / range_y if range_y > 0 else draw_height

        if range_x > 0 and range_y > 0:
            scale = min(scale_x, scale_y)
        elif range_x > 0:
            scale = scale_x
        elif scale_y > 0:
            scale = scale_y
        else:
            scale = 100

        offset_x = margin + float((draw_width - range_x * scale) / 2)
        offset_y = margin + float((draw_height - range_y * scale) / 2)

        screen_x = int((x - self._min_x) * scale + offset_x)
        screen_y = int(self._height - (y - self._min_y) * scale - offset_y)

        return screen_x, screen_y

    def _get_rgb_color(
            self, color_name: str, default: tuple[int, int, int]
            ) -> tuple[int, int, int]:
        """Convert color name string to an RGB tuple."""
        return self.COLOR_MAP.get(color_name.lower(), default)

    def _draw_dashed_line(
            self, color: tuple[int, int, int], start: tuple[int, int],
            end: tuple[int, int], dash_len: int = 10, space_len: int = 5
            ) -> None:
        """ Draw a dashed line between two points. """
        pass

    def _draw_dotted_line(
            self, color: tuple[int, int, int], start: tuple[int, int],
            end: tuple[int, int], dot_spacing: int = 8
            ) -> None:
        """ Draw a dotted line between two points. """
        pass

    def _draw_cross_line(
            self, color: tuple[int, int, int], start: tuple[int, int],
            end: tuple[int, int], spacing: int = 20
            ) -> None:
        """ Draw a line with cross marks for blocked connections. """
        pass

    def _draw_connections(self) -> None:
        """ Draw connection lines based on their style type (Layer 1 - Bottom).
        """
        # Normal: Solid white line
        # Priority: Dotted green line
        # Restricted: Dashed yellow line
        # Blocked: Red line with cross pattern
        for conn in self._graph.connections:
            # print(conn.hub1.name, conn.hub2.name)
            pos1 = self._map_to_screen(*conn.hub1.coordinates)
            pos2 = self._map_to_screen(*conn.hub2.coordinates)

            target_zone = conn.hub2.zone

            if target_zone == "priority":
                # Dotted green line
                # self._draw_dotted_line(self.COLOR_MAP["green"], pos1, pos2)
                pygame.draw.line(
                    self._screen, self.COLOR_MAP["green"], pos1, pos2, 2
                    )
            elif target_zone == "restricted":
                # Dashed yellow line
                # self._draw_dashed_line(self.COLOR_MAP["yellow"], pos1, pos2)
                pygame.draw.line(
                    self._screen, self.COLOR_MAP["yellow"], pos1, pos2, 2
                    )
            elif target_zone == "blocked":
                # Red line with crosses
                # self._draw_cross_line(self.COLOR_MAP["red"], pos1, pos2)
                pygame.draw.line(
                    self._screen, self.COLOR_MAP["red"], pos1, pos2, 2
                    )
            else:
                # Solid white line (Normal)
                pygame.draw.line(
                    self._screen, self.COLOR_MAP["white"], pos1, pos2, 2
                    )

    def _draw_hubs(self) -> None:
        """ Draw hub circles at their Cartesian coordinates (Layer 2 - Middle).
        """
        for hub in self._graph.hubs.values():
            pos = self._map_to_screen(*hub.coordinates)
            hub_color = self._get_rgb_color(hub.color, self.COLOR_MAP["blue"])

            # Outer boundary and filled circle
            # pygame.draw.circle(surface, color, center, radius, width=0)
            pygame.draw.circle(self._screen, hub_color, pos, 20)
            pygame.draw.circle(
                self._screen, self.COLOR_MAP["white"], pos, 20, 2
                )

            # Hub label text
            text_surf = self._font.render(
                hub.name, True, self.COLOR_MAP["white"]
                )
            text_rect = text_surf.get_rect(center=(pos[0], pos[1] - 30))
            self._screen.blit(text_surf, text_rect)

    def _draw_drones(self) -> None:
        """ Draw drone triangles overlapping hubs and lines (Layer 3 - Top).
        """
        pass

    def _draw_hud_info(self) -> None:
        """ Display elapsed time and turn count (Layer 4 - Foreground). """
        pass

    def render_frame(self) -> bool:
        """ Process Pygame events and render one frame. """
        pygame.event.pump()  # Essential for macOS window event queue

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         return False

        self._screen.fill((30, 30, 30))
        self._draw_connections()
        self._draw_hubs()
        # self._draw_drones()
        # self._draw_hud_info()

        pygame.display.flip()
        return True
