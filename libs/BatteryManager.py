from libs.ffishell import *

class BatteryManager:
    measure_value = 0
    measure_voltage = 0
    measure_soc = 0 # 1=100% 0=0%

    # TODO: voltage-to-soc relation is not linear
    # values retrieved from real measurements
    # voltage_soc_relation = [
    #     3.9825,
    #     3.94,
    #     3.915,
    #     3.9,
    #     3.8975,
    # ]

    max_voltage = 4.1
    min_voltage = 3.0
    
    address = "/dev/i2c-1"
    file = None

    def __init__(self):
        self.setup()

    def setup(self):
        print("setting up i2c connection")
        self.file = open(self.address, O_RDWR)
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
        
    def measure(self):
        data = bytearray()
        data.append(0x00)
        data.append(0x00)
        
        if(read(self.file, data, 2) != 2):
            print("Error : Input/Output Error")
        else:
            self.measure_value = ((data[0] & 0x0F) * 256) + data[1]
            self.calc_voltage()
            self.calc_soc()

    def calc_voltage(self):
        self.measure_voltage = (self.measure_value+504)/0.4/1000
    
    def calc_soc(self):
        self.measure_soc = (self.measure_voltage - self.min_voltage) / (self.max_voltage - self.min_voltage)

    def get_voltage(self):
        return self.measure_voltage
    
    def get_soc(self):
        return self.measure_soc