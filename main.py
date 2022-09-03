import usys as sys
import lvgl as lv
lv.init()

import SDL
SDL.init(w=320,h=240)

import time

from libs.data_manager import DataManager
from libs.PageManager import PageManager

scr = lv.obj()
lv.scr_load(scr)
scr.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
scr.clear_flag(scr.FLAG.SCROLLABLE)


pagemanager = PageManager()




while(1):
    lv.timer_handler()
    time.sleep(1 / 200)
