#!/usr/bin/micropython -i
import lvgl as lv
lv.init()

import SDL
SDL.init(w=320,h=240)

import time

from libs.data_manager import DataManager
from gui.pages.GamesOverviewPage import GamesOverviewPage
from gui.pages.LaunchScreen import LaunchScreen


scr = lv.obj()
lv.scr_load(scr)

#gamesOverviewPage = GamesOverviewPage()
#launchScreen = LaunchScreen()


import usys as sys
from libs.imagetools2 import get_png_info, open_png
#from imagetools import get_png_info, open_png


# Register PNG image decoder
decoder = lv.img.decoder_create()
decoder.info_cb = get_png_info
decoder.open_cb = open_png


try:
    with open('./imgs/launchscreens/10.png','rb') as f:
        png_data = f.read()
except:
    print("Could not find img_cogwheel_argb.png")
    sys.exit()

img_cogwheel_argb = lv.img_dsc_t({
    'data_size': len(png_data),
    'data': png_data
})

img1 = lv.img(lv.scr_act())
img1.set_src(img_cogwheel_argb)
img1.align(lv.ALIGN.CENTER, 0, 0)
img1.set_size(320, 240)

img2 = lv.img(lv.scr_act())
img2.set_src(lv.SYMBOL.OK + "Accept")
img2.align_to(img1, lv.ALIGN.OUT_BOTTOM_MID, 0, -20)




while(1):
    lv.timer_handler()
    time.sleep(1 / 200)
