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
        soc = SINGLETONS.BATTERY_MANAGER.get_soc()
        voltage = SINGLETONS.BATTERY_MANAGER.get_voltage()

        print("soc: ", soc)
        print("voltage: ", voltage)

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
