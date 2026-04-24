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
        port='/dev/ttyAMA0', # /dev/ttyAMA0 ou /dev/ttyAMA10
        baudrate=9600,
        bytesize=serial.SEVENBITS,
        stopbits=serial.STOPBITS_ONE,
        parity=serial.PARITY_EVEN,
        timeout=1
        )
print(f"Connected to {ser.name}")


s1 = 0 # S1 = 0, pour comapraison avec S0

while True:
    #s0 = time.strftime("%-S")
    s0 = datetime.datetime.now() # defini S0 à l'heure actuelle
    # print("s0 = ", s0.strftime("%S.%f"), ", s0 = ", s0) #debug
    print("s0 = ",s0.strftime("%-S.%f") ," s1 = ", s1) # debug
    
    # si la seconde actuelle (s0)  n'est pas égale à la seconde enregistrée en fin
    # de boucle (s1), la seconde à changé, on entre dans la boucle. Si la seconde est 
    # identique, on ne refait pas un télegramme et on attends un dixième de seconde.
    if s0.strftime("%-S") != s1:

        # creation du telegrame
        tgrm = "OAL" + s0.strftime("%y%m%dF%H%M%S") + "\r"

        tgrm_encoded = tgrm.encode(encoding='ascii') # encodage

        tgrm_hex = tgrm_encoded.hex() #encodage pour debug
        print("telegram ascii : ", tgrm_encoded, ", hex : ", tgrm_hex) # affiche pour debug
        
        ser.write(tgrm_encoded) # envoyer sur port série

        s1 = s0.strftime("%-S") # defini s1 pour comparaison avec s0
        time.sleep(.9) 
    else:
        time.sleep(.1) # attente un dixième de seconde
        
