import os
import sys
from typing import Any


try:
    from mlx import Mlx
except ImportError:
    print("Error: failed to import 'mlx' library")


class MlxWrapper:
    def __init__(self) -> None:
        self.lib = Mlx()
    
    def init(self) -> any:
        return self.lib.mlx_init()

    def new_window(self, *args) -> Any:
        return self.lib.mlx_new_window(*args)
    
    def new_image(self, *args) -> Any:
        return self.lib.mlx_new_image(*args)    

    def get_image_data(self, *args) -> Any:
        return self.lib.mlx_get_data_addr(*args)

    def loop(self, *args) -> Any:
        return self.lib.mlx_loop(*args)

    def expose_hook(self, *args) -> Any:
        return self.lib.mlx_expose_hook(*args)

    def loop_hook(self, *args) -> Any:
        return self.lib.mlx_loop_hook(*args)

    def image_to_window(self, *args) -> Any:
        return self.lib.mlx_put_image_to_window(*args)

    def do_sync(self, *args) -> Any:
        return self.lib.mlx_do_sync(*args)

    def put_pixel(self, *args) -> Any:
        return self.lib.mlx_pixel_put(*args)

    def putstr(self, *args) -> Any:
        return self.lib.mlx_string_put(*args)


class MLXHandler:
    def __init__(self, settings: "MazeParser"):
        self.mlx = MlxWrapper()
        self.ptr = self.mlx.init()
        self.cell_size = self._get_cell_size(settings.width, settings.height)
        self.window_height = settings.height * self.cell_size
        self.window_width = settings.width * self.cell_size
        self.window = self.mlx.new_window(self.ptr, self.window_width,
                                          self.window_height,
                                          "A_Maze_Ing@19")
        self.image = self.mlx.new_image(self.ptr, self.window_width,
                                        self.window_height)
        self.data_tup = self.mlx.get_image_data(self.image)
        self.image_buffer = self.data_tup[0]
        self.bpp = self.data_tup[1]
        self.bpr = self.data_tup[2]

    def _get_cell_size(self, width: int, height: int) -> int:
        window_size = (1600, 1000)

        scale_x = window_size[0] // width
        scale_y = window_size[1] // height
        return max(2, min(scale_x, scale_y))

    def write_to_window(self, *args: any) -> None:
        if not self.window:
            return
        self.mlx.image_to_window(self.ptr, self.window, self.image, 0, 0)
        self.mlx.do_sync(self.ptr)

    def event_manager(self, program: "AMazeIng") -> None:
        self.mlx.expose_hook(self.window, self.write_to_window, None)
        # self.mlx.loop_hook(self.ptr, ?, None) #program.create_maze
        self.mlx.loop(self.ptr)

