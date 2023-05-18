from libs.ffishell import *
import lvgl as lv


class BatteryManager:
    voltage = 0
    soc = 0

    measure_value_history = []

    _max_voltage = 4.2
    _min_voltage = 3.0

    _max_measurement = 1200
    _min_measurement = 850

    _measure_interval = 3000
    _history_len = 20

    _address = "/dev/i2c-1"
    file = None
    timer = None

    def __init__(self):
        self.setup()
        self.timer = lv.timer_create(self.measure, self._measure_interval, None)

    def setup(self):
        print("setting up i2c connection")
        self.file = open(self._address, O_RDWR)
        if(self.file < 0):
            print("error opening bus")
            return
        
        ioctl(self.file, I2C_SLAVE, 0x50)

        config = bytearray()
        config.append(0x02)
        config.append(0x20)
        write(self.file, config, 2)

        reg = bytearray()
        reg.append(0x00)
        write(self.file, reg, 1)
        
    def measure(self, timer):
        data = bytearray()
        data.append(0x00)
        data.append(0x00)
        
        if(read(self.file, data, 2) != 2):
            print("Error : Input/Output Error")
        else:
            self._calc_measure(data)
            self._calc_soc()

    def _calc_measure(self, data):
        measured_value = ((data[0] & 0x0F) * 256) + data[1]
        self.measure_value_history.insert(0, measured_value)
        if len(self.measure_value_history) >= self._history_len:
            self.measure_value_history.pop()

    def _calc_soc(self):
        average_measure = 0
        for num in self.measure_value_history:
            average_measure += num
        average_measure = average_measure / len(self.measure_value_history)

        self.soc = (average_measure - self._min_measurement) * (100 / (self._max_measurement - self._min_measurement))
        self.voltage = ((average_measure - self._min_measurement) * (self._max_voltage - self._min_voltage) / (self._max_measurement - self._min_measurement)) + self._min_voltage
    
    def get_voltage(self):
        return self.voltage
    
    def get_soc(self):
        return self.soc