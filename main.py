import time
import io
import json
import usys as sys
import lvgl as lv

import uasyncio as asyncio

from libs.libsdl import * 

WIDTH = 320
HEIGHT = 240
disp_drv = lv.sdl_window_create(WIDTH, HEIGHT)
disp_drv.set_color_format(lv.COLOR_FORMAT.ARGB8888)

SDL_ShowCursor(0)

from libs.Singletons import *

try:
    _f = io.open("./data/configuration.json", "r")
except Exception:
    _f = io.open("./data/configurationDefault.json", "r")
_cfg = json.loads(" ".join(map(str, _f.readlines())))
_f.close()
_colors = lv.PALETTE.__dict__
_primary = _colors[_cfg["user"]["theme"]["primaryColor"]]
_dark = _cfg["user"]["theme"]["darkTheme"]

lv.theme_default_init(lv.display_get_default(),
                        lv.palette_main(_primary),
                        lv.palette_main(lv.PALETTE.GREY),
                        _dark,
                        lv.font_montserrat_16)

SINGLETONS = SingletonsClass()


async def main():
    while True:
        await asyncio.sleep_ms(16)
        lv.timer_handler()
        keyboard_loop()

asyncio.run(main())
