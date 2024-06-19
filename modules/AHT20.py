from machine import Pin
from machine import SoftI2C
from time import sleep
import os
from math import pow

AHT20_ADDR = 0x38

machine = os.uname().machine

i2c1 = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
   
def read():
    try:
        i2c1.writeto(AHT20_ADDR, b'\xAC\x33\x00')
        sleep(0.1)
        data = i2c1.readfrom(AHT20_ADDR, 6)
        if data[0] & 0x80:
            i2c1.writeto(AHT20_ADDR, b'\xBE')
            sleep(0.1)
            return (-999, -999)
        h = ((data[1] << 12) | (data[2] << 4) | ((data[3] & 0xF0) >> 4)) / pow(2, 20) * 100.0;
        t = (((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]) / pow(2, 20) * 200.0 - 50.0;
        return (round(t, 2), round(h, 2))
    except:
        return (-999, -999)
