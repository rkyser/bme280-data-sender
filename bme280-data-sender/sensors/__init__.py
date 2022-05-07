from abc import ABCMeta, abstractmethod
from smbus2 import SMBus
from bme280 import BME280
from data_models import BME280SensorSample
import time

def temp_c_to_f(temp_c: float):
    """Converts a Celsius temperature to Fahrenheit"""
    return (temp_c * 9/5) + 32.0

class AbstractBME280Sensor(metaclass = ABCMeta):
    @property
    @abstractmethod
    def name(self):
        """Returns the name of the sensor"""
        pass

    @abstractmethod
    def get_sample(self):
        """Reads and returns a single sample from the sensor"""
        pass


class FakeBME280Sensor(AbstractBME280Sensor):
    """This class is a fake sampler used for 
    testing on hosts where no sampler is present"""

    @property
    def name(self):
        return "FakeBME280"

    def get_sample(self):
        celsius = 16.5
        return BME280SensorSample(
            timestamp = time.time_ns(),
            humidity = 65.0,
            temp_c = celsius,
            temp_f = temp_c_to_f(celsius),
            pressure = 992.15
        )

class BME280Sensor(AbstractBME280Sensor):
    def __init__(self, bus_num: int = 1, i2c_addr: int = 0x77):
        self._bus = SMBus(bus_num)
        self._bme280 = BME280(i2c_addr=i2c_addr, i2c_dev=self._bus)

    @property
    def name(self):
        return "BME280"

    def get_sample(self):
        celsius = self._bme280.get_temperature()
        return BME280SensorSample(
            timestamp = time.time_ns(),
            humidity = self._bme280.get_humidity(),
            temp_c = celsius,
            temp_f = temp_c_to_f(celsius),
            pressure = bme280.get_pressure()
        )