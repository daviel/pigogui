#!/usr/bin/micropython -i
import usys as sys
import lvgl as lv
lv.init()

import SDL
SDL.init(w=320,h=240)

import time

from libs.data_manager import DataManager
from libs.PageManager import PageManager
from libs.imagetools2 import get_png_info, open_png

# Register PNG image decoder
decoder = lv.img.decoder_create()
decoder.info_cb = get_png_info
decoder.open_cb = open_png


scr = lv.obj()
lv.scr_load(scr)


pagemanager = PageManager()


while(1):
    lv.timer_handler()
    time.sleep(1 / 200)
