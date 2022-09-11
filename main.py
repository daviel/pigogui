import usys as sys
import lvgl as lv
lv.init()

import SDL
SDL.init(w=320,h=240)

import time

from libs.DataManager import DataManager
from libs.PageManager import PageManager


lv.theme_default_init(lv.disp_get_default(), 
                      lv.palette_main(lv.PALETTE.GREEN), 
                      lv.palette_main(lv.PALETTE.GREY), 
                      True, 
                      lv.font_montserrat_16)

pagemanager = PageManager()


while(1):
    lv.timer_handler()
    time.sleep(1 / 200)
