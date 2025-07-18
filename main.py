import usys as sys
import lvgl as lv
lv.init()

from libs.libsdl import SDL_ShowCursor 

WIDTH = 320
HEIGHT = 240
disp_drv = lv.sdl_window_create(WIDTH, HEIGHT)



import time
from libs.Singletons import *

config = DATA_MANAGER.get("configuration")
primary_color = config["user"]["theme"]["primaryColor"]
darkTheme = config["user"]["theme"]["darkTheme"]

colors = lv.PALETTE.__dict__
primary_color = colors[primary_color]

lv.theme_default_init(lv.display_get_default(), 
						lv.palette_main(primary_color), 
						lv.palette_main(lv.PALETTE.GREY), 
						darkTheme, 
						lv.font_montserrat_16)

disp_drv.set_color_format(lv.COLOR_FORMAT.ARGB8888)
#scr.set_style_bg_opa(lv.OPA.TRANSP, 0)
lv.layer_bottom().set_style_bg_opa(lv.OPA.TRANSP, 0)
lv.screen_active().set_style_bg_opa(lv.OPA.TRANSP, 0)
lv.screen_active().set_style_bg_opa(lv.OPA._0, 0)
SDL_ShowCursor(0)


while(1):
    lv.timer_handler()
    DOWNLOAD_MANAGER.update()
    time.sleep(1 / 200)
