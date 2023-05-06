import lvgl as lv
import time
import libs.Singletons as SINGLETONS


class BatteryIndicator(lv.label):
    timer = ""

    def __init__(self, container):
        super().__init__(container)
        self.set_text(lv.SYMBOL.BATTERY_FULL)
        self.timer = lv.timer_create(self.update_state, 5000, self)

    def update_state(obj, timer):
        SINGLETONS.BATTERY_MANAGER.measure()
        soc = SINGLETONS.BATTERY_MANAGER.get_soc()

        if(soc <= 0.1):
            obj.set_text(lv.SYMBOL.BATTERY_EMPTY)
        elif(soc <= 0.3):
            obj.set_text(lv.SYMBOL.BATTERY_3)
        elif(soc <= 0.6):
            obj.set_text(lv.SYMBOL.BATTERY_2)
        elif(soc <= 0.8):
            obj.set_text(lv.SYMBOL.BATTERY_1)
        else:
            obj.set_text(lv.SYMBOL.BATTERY_FULL)
