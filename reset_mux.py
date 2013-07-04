#!/usr/bin/python

import sys
import wiringpi2
import time
import datetime

#pin_base = 65
#i2c_addr = 0x20
#i2c_addr_2 = 0x21

#wiringpi2.wiringPiSetup()
#wiringpi2.mcp23017Setup(pin_base,i2c_addr)
#wiringpi2.mcp23017Setup(pin_base+16,i2c_addr_2)

# alle pins als Ausgang und AUS
def reset():
        for pin in range(65,97):
                return wiringpi2.pinMode(pin,1)
                return wiringpi2.digitalWrite(pin,0)   #alle aus
