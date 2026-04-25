#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Synchronisation d'une horloge Mobatime BU190(t) S 230 avec un Raspberry PI

Created on Mon Feb  9 08:44:43 2026

@author: christophe
"""

import time
import datetime
import serial
import logging
import sys

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

ser = serial.Serial(
        port='/dev/ttyAMA0', # /dev/ttyAMA0 ou /dev/ttyAMA10
        baudrate=9600,
        bytesize=serial.SEVENBITS,
        stopbits=serial.STOPBITS_ONE,
        parity=serial.PARITY_EVEN,
        timeout=1
        )
logger.info(f"Connecté à {ser.name}")
# print(f"Connected to {ser.name}")


while True:

    s0 = datetime.datetime.now() # defini S0 à l'heure actuelle

    # creation du telegrame
    tgrm = "OAL" + s0.strftime("%y%m%dF%H%M%S") + "\r"

    tgrm_encoded = tgrm.encode(encoding='ascii') # encodage

    # tgrm_hex = tgrm_encoded.hex() #encodage pour debug
    print(datetime.datetime.now(), " : telegram ascii : ", tgrm_encoded) # affiche pour debug
    # print("telegram ascii : ", tgrm_encoded, ", hex : ", tgrm_hex) # affiche pour debug

    ser.write(tgrm_encoded) # envoyer sur port série

    time.sleep(60) 
