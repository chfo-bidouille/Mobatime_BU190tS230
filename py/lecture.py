#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 08:44:43 2026

@author: christophe
"""

import time
import datetime
import serial

ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        )
print(f"Connected to {ser.name}")

reponse = ser.read(5)

print(reponse)
