import usys as sys
import lvgl as lv
lv.init()

import SDL
SDL.init(w=320,h=240)

import time


lv.theme_default_init(lv.disp_get_default(), 
                      lv.palette_main(lv.PALETTE.GREEN), 
                      lv.palette_main(lv.PALETTE.GREY), 
                      True, 
                      lv.font_montserrat_16)

import libs.Singletons as SINGLETONS

lv.scr_act().set_style_bg_opa(100, 0)
lv.disp_get_default().set_bg_opa(50)


while(1):
    lv.timer_handler()
    time.sleep(1 / 200)
