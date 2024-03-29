import usys as sys
import lvgl as lv
lv.init()

from libs.libsdl import SDL_ShowCursor 

WIDTH = 320
HEIGHT = 240
disp_drv = lv.sdl_window_create(WIDTH, HEIGHT)



import time
import libs.Singletons as SINGLETONS

config = SINGLETONS.DATA_MANAGER.get("configuration")
primary_color = config["user"]["theme"]["primaryColor"]
darkTheme = config["user"]["theme"]["darkTheme"]

colors = lv.PALETTE.__dict__
primary_color = colors[primary_color]

lv.theme_default_init(lv.disp_get_default(), 
						lv.palette_main(primary_color), 
						lv.palette_main(lv.PALETTE.GREY), 
						darkTheme, 
						lv.font_montserrat_16)

lv.scr_act().set_style_bg_opa(0, 0)
#lv.disp_get_default().set_bg_opa(50)
SDL_ShowCursor(0)

while(1):
    lv.timer_handler()
    SINGLETONS.DOWNLOAD_MANAGER.update()
    time.sleep(1 / 200)
