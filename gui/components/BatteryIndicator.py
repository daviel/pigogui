import lvgl as lv
import time
from libs.Singletons import *


class BatteryIndicator(lv.label):
    timer = ""

    def __init__(self, container):
        super().__init__(container)
        self.set_text(lv.SYMBOL.BATTERY_FULL)
        self.timer = lv.timer_create(self.update_state, 5000, self)

    def update_state(obj, timer):
        soc = BATTERY_MANAGER.get_soc()
        voltage = BATTERY_MANAGER.get_voltage()

        if(soc <= 15):
            obj.set_text(lv.SYMBOL.BATTERY_EMPTY)
        elif(soc <= 40):
            obj.set_text(lv.SYMBOL.BATTERY_1)
        elif(soc <= 60):
            obj.set_text(lv.SYMBOL.BATTERY_2)
        elif(soc <= 80):
            obj.set_text(lv.SYMBOL.BATTERY_3)
        else:
            obj.set_text(lv.SYMBOL.BATTERY_FULL)
