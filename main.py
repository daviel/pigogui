import time
import usys as sys
import lvgl as lv
lv.init()

import uasyncio as asyncio

from libs.libsdl import * 

WIDTH = 320
HEIGHT = 240
disp_drv = lv.sdl_window_create(WIDTH, HEIGHT)
disp_drv.set_color_format(lv.COLOR_FORMAT.ARGB8888)

SDL_ShowCursor(0)

from libs.Singletons import *


SINGLETONS = SingletonsClass()
config = SINGLETONS.singletons["DATA_MANAGER"].get("configuration")
primary_color = config["user"]["theme"]["primaryColor"]
darkTheme = config["user"]["theme"]["darkTheme"]

colors = lv.PALETTE.__dict__
primary_color = colors[primary_color]

lv.theme_default_init(lv.display_get_default(), 
						lv.palette_main(primary_color), 
						lv.palette_main(lv.PALETTE.GREY), 
						darkTheme, 
						lv.font_montserrat_16)

lv.screen_active().set_style_bg_opa(lv.OPA.TRANSP, 0)
lv.layer_bottom().set_style_bg_opa(lv.OPA.TRANSP, 0)
lv.screen_active().set_style_bg_opa(lv.OPA.TRANSP, 0)
lv.screen_active().set_style_bg_opa(lv.OPA._0, 0)


async def main():
    while True:
        await asyncio.sleep_ms(16)
        lv.timer_handler()
        keyboard_loop()
    print("Exit-Code:", rc)

asyncio.run(main())
