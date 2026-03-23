from __future__ import annotations
import sys
from typing import Any
from maze_parser import MazeParser

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from a_maze_ing import AMazeIng

try:
    from mlx import Mlx  # type:ignore
except ImportError:
    print("Error: failed to import 'mlx' library")


# =============================================================================
# MLX WRAPPER
# =============================================================================
class MlxWrapper:
    """Wrap the Mlx library to provide a clean Python interface.

    Delegates all calls to the underlying Mlx instance, exposing
    window creation, image handling, event hooks and rendering.
    """

    def __init__(self) -> None:
        """Initialize the Mlx library instance."""
        self.lib = Mlx()

    def init(self) -> Any:
        """Initialize the Mlx connection and return the instance."""
        return self.lib.mlx_init()

    def new_window(self, *args: Any) -> Any:
        """Create and return a new window."""
        return self.lib.mlx_new_window(*args)

    def new_image(self, *args: Any) -> Any:
        """Create and return a new image buffer."""
        return self.lib.mlx_new_image(*args)

    def get_image_data(self, *args: Any) -> Any:
        """Return the raw pixel data address of an image."""
        return self.lib.mlx_get_data_addr(*args)

    def loop(self, *args: Any) -> Any:
        """Start the Mlx event loop."""
        return self.lib.mlx_loop(*args)

    def expose_hook(self, *args: Any) -> Any:
        """Register a callback for window expose events."""
        return self.lib.mlx_expose_hook(*args)

    def loop_hook(self, *args: Any) -> Any:
        """Register a callback called on each loop iteration."""
        return self.lib.mlx_loop_hook(*args)

    def key_hook(self, *args: Any) -> Any:
        """Register a callback for window expose events."""
        return self.lib.mlx_key_hook(*args)

    def hook(self, *args: Any) -> Any:
        """Register a callback for key press events."""
        return self.lib.mlx_hook(*args)

    def image_to_window(self, *args: Any) -> Any:
        """Register a generic event hook."""
        return self.lib.mlx_put_image_to_window(*args)

    def do_sync(self, *args: Any) -> Any:
        """Synchronize the display buffer with the window."""
        return self.lib.mlx_do_sync(*args)

    def put_pixel(self, *args: Any) -> Any:
        """Render an image buffer to the window."""
        return self.lib.mlx_pixel_put(*args)

    def putstr(self, *args: Any) -> Any:
        """Render a string to the window."""
        return self.lib.mlx_string_put(*args)

    def exit(self, *args: Any) -> Any:
        """Exit the Mlx event loop."""
        return self.lib.mlx_loop_exit(*args)


# =============================================================================
# MLX HANDLER
# =============================================================================
class MLXHandler:
    """Handle the MLX window, image buffer, rendering and event loop.

    Manages window and image creation, pixel drawing, color schemes,
    solution animation and event registration.
    """

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------
    def __init__(self, settings: MazeParser) -> None:
        """Initialize the MLX window and image buffer from maze settings.

        Computes cell size and window dimensions, creates the window and
        image buffer, and sets up animation and color scheme state.
        """
        self.mlx = MlxWrapper()
        self.ptr = self.mlx.init()
        self.cell_size = self._get_cell_size(settings.width, settings.height)
        self.window_height = settings.height * self.cell_size + self.cell_size
        self.window_width = settings.width * self.cell_size
        self.window = self.mlx.new_window(self.ptr, self.window_width,
                                          self.window_height + 3 *
                                          self.cell_size,
                                          "A_Maze_Ing@19")
        self.image = self.mlx.new_image(self.ptr, self.window_width,
                                        self.window_height)
        self.data_tup = self.mlx.get_image_data(self.image)
        self.image_buffer = self.data_tup[0]
        self.bpp: int = self.data_tup[1]
        self.bpr: int = self.data_tup[2]
        self.color_scheme: dict[int, dict[str, int]] = {
                        1: {
                            "border": 0X1919A6,
                            "logo": 0XFFFFFF,
                            "path": 0XFF0000,
                            "bg": 0X000000,
                        },
                        2: {
                            "border": 0XFF5C00,
                            "logo": 0XC11C84,
                            "path": 0X228B22,
                            "bg": 0X000000,
                        },
                        3: {
                            "border": 0X8FD9FB,
                            "logo": 0XFFF01F,
                            "path": 0XFF00FF,
                            "bg": 0X000000,
                        },
                        4: {
                            "border": 0XFF3131,
                            "logo": 0x000000,
                            "path": 0X1F51FF,
                            "bg": 0XA9A9A9,
                        }
            }
        self.solving: bool = False
        self.solution_steps: list[tuple[int, int]] = []
        self.step_index: int = 0
        self.frame_counter: int = 0
        self.frame_delay: int = 3
        self._scheme: int = 1
        self.steps_per_frame: int = 1

    # -------------------------------------------------------------------------
    # Window & Cell Size
    # -------------------------------------------------------------------------
    def _get_cell_size(self, width: int, height: int) -> int:
        """Compute the cell size in pixels to fit the maze in the window."""
        window_size = (1600, 1000)

        scale_x = window_size[0] // width
        scale_y = window_size[1] // height
        return max(2, min(scale_x, scale_y))

    # -------------------------------------------------------------------------
    # Pixel & Rectangle Drawing
    # -------------------------------------------------------------------------
    def write_to_window(self, *args: Any) -> None:
        """Push the image buffer to the window and sync the display."""
        if not self.window:
            return
        ptr, window, image = args
        self.mlx.image_to_window(ptr, window, image, 0, 0)
        self.mlx.do_sync(ptr)

    def pixel_to_buff(self, x: int, y: int, color: int) -> None:
        """Write a pixel color into the image buffer at (x, y)."""
        if 0 <= x < self.window_width and 0 <= y < self.window_height:
            offset = (y * self.bpr) + (x * (self.bpp // 8))
            self.image_buffer[offset] = color & 0XFF
            self.image_buffer[offset + 1] = (color >> 8) & 0XFF
            self.image_buffer[offset + 2] = (color >> 16) & 0XFF
            self.image_buffer[offset + 3] = 0xFF

    def draw_rect(self, color: int, start_x: int, start_y: int, width: int,
                  height: int) -> None:
        """Fill a rectangle in the image buffer with a solid color."""
        for y in range(start_y, start_y + height):
            for x in range(start_x, start_x + width):
                self.pixel_to_buff(x, y, color)

    def _draw_solution_cell(self, col: int, row: int, color: int) -> None:
        """Draw a colored inset square inside a maze cell."""
        inset = max(1, self.cell_size // 6)
        px = col * self.cell_size + inset
        py = row * self.cell_size + inset
        size = self.cell_size - 2 * inset
        if size > 0:
            self.draw_rect(color, px, py, size, size)

    def start_solve_animation(self, solution_steps: list[tuple[int, int]],
                              scheme: int = 1,
                              frame_delay: int = 1,
                              steps_per_frame: int = 1) -> None:
        """Configure and start the step-by-step solution animation."""
        self.solution_steps = solution_steps
        self.step_index = 0
        self.frame_counter = 0
        self.frame_delay = max(1, frame_delay)
        self._scheme = scheme
        self.steps_per_frame = steps_per_frame
        self.solving = True

    def step_render(self, param: Any) -> int:
        """Render the next animation step on each loop iteration."""
        if not self.solving:
            return 0
        self.frame_counter += 1
        if self.frame_counter < self.frame_delay:
            return 0
        self.frame_counter = 0

        if self.step_index >= len(self.solution_steps):
            self.solving = False
            return 0

        for _ in range(self.steps_per_frame):
            if self.step_index >= len(self.solution_steps):
                self.solving = False
                break
            col, row = self.solution_steps[self.step_index]
            path_color = self.color_scheme[self._scheme]["path"]
            self._draw_solution_cell(col, row, path_color)
            self.step_index += 1
        self.mlx.image_to_window(self.ptr, self.window, self.image, 0, 0)
        self.mlx.do_sync(self.ptr)
        return 0

    def close(self, param: Any) -> None:
        self.mlx.exit(self.ptr)

    def event_manager(self, program: AMazeIng) -> None:
        """Register all event hooks and start the MLX loop.

        Binds expose, key, close and loop hooks then starts the
        event loop. Exits the program when the loop ends.
        """
        self.mlx.expose_hook(
            self.window,
            program.maze_view,
            (self.ptr, self.window, self.image, False)
        )
        self.mlx.key_hook(self.window, program.key_handler, program)
        self.mlx.hook(self.window, 33, 0, self.close, None)

        self.mlx.loop_hook(self.ptr, self.step_render, None)

        self.mlx.loop(self.ptr)
        sys.exit(0)
