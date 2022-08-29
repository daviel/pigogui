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
launchScreen = LaunchScreen()


while(1):
    lv.timer_handler()
    time.sleep(1 / 200)
