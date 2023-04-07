import usys as sys
import lvgl as lv
lv.init()

import SDL
SDL.init(w=320,h=240)

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

lv.scr_act().set_style_bg_opa(100, 0)
lv.disp_get_default().set_bg_opa(50)


while(1):
    lv.timer_handler()
    time.sleep(1 / 200)
