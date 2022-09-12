import usys as sys
import lvgl as lv
lv.init()

import SDL
SDL.init(w=320,h=240)

import time
from libs.Singletons import PAGE_MANAGER, DATA_MANAGER, NOTIFICATION_MANAGER

lv.theme_default_init(lv.disp_get_default(), 
                      lv.palette_main(lv.PALETTE.GREEN), 
                      lv.palette_main(lv.PALETTE.GREY), 
                      True, 
                      lv.font_montserrat_16)


while(1):
    lv.timer_handler()
    time.sleep(1 / 200)
