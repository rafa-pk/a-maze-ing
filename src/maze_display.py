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

    def key_hook(self, *args) -> Any:
        return self.lib.mlx_key_hook(*args)

    def hook(self, *args) -> Any:
        return self.lib.mlx_hook(*args)
    
    def image_to_window(self, *args) -> Any:
        return self.lib.mlx_put_image_to_window(*args)

    def do_sync(self, *args) -> Any:
        return self.lib.mlx_do_sync(*args)

    def put_pixel(self, *args) -> Any:
        return self.lib.mlx_pixel_put(*args)

    def putstr(self, *args) -> Any:
        return self.lib.mlx_string_put(*args)

    def exit(self, *args) -> Any:
        return self.lib.mlx_loop_exit(*args)

class MLXHandler:
    def __init__(self, settings: "MazeParser"):
        self.mlx = MlxWrapper()
        self.ptr = self.mlx.init()
        self.cell_size = self._get_cell_size(settings.width, settings.height)
        self.window_height = settings.height * self.cell_size + 2
        self.window_width = settings.width * self.cell_size + 2
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
        ptr, window, image = args
        self.mlx.image_to_window(ptr, window, image, 0, 0)
        self.mlx.do_sync(ptr)

    def pixel_to_buff(self, x: int, y: int, color: int):
        if 0 <= x < self.window_width and 0 <= y < self.window_height:
            offset = (y * self.bpr) + (x * (self.bpp // 8))
            self.image_buffer[offset] = color & 0XFF
            self.image_buffer[offset + 1] = (color >> 8) & 0XFF
            self.image_buffer[offset + 2] = (color >> 16) & 0XFF
            self.image_buffer[offset + 3] = 0xFF 

    def draw_rect(self, color: int, start_x: int, start_y: int, width: int, height: int) -> None:
        for y in range(start_y, start_y + height):
            for x in range(start_x, start_x + width):
                self.pixel_to_buff(x, y, color)
   
    def close(self, param: any) -> Any:
        self.mlx.exit(self.ptr)
 
    def event_manager(self, program: "AMazeIng") -> None:
        self.mlx.expose_hook(self.window, program.maze_view, (self.ptr, self.window, self.image))
        self.mlx.key_hook(self.window, program.key_handler, program)
        #self.mlx.mouse_hook()
        #self.mlx.expose_hook()
        self.mlx.hook(self.window, 33, 0, self.close, None)
        #self.mlx.loop_hook(self, self.window, self.image))
        self.mlx.loop(self.ptr)
        sys.exit(0)
