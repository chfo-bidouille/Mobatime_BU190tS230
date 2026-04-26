#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 08:44:43 2026

@author: christophe
"""

import time
import datetime
import serial

ser = serial.Serial( # ouvrir et configurer le port séri
        port='/dev/ttyAMA0', # /dev/ttyAMA0 ou /dev/ttyAMA10
        baudrate=9600,
        bytesize=serial.SEVENBITS,
        stopbits=serial.STOPBITS_ONE,
        parity=serial.PARITY_EVEN,
        timeout=1
        )
print(f"Connected to {ser.name}")

'''
Attendre l'heure exacte 
'''
now = datetime.datetime.now() # heure actuelle exacte
micro = int(now.strftime("%f")) # microseconde actuelle

# print(micro)

# combien de microsecondes à attendre avant la seconde suivante, converti en seconde, pour avoir "seconde,000000"
wait = (1000000-micro) / 1000000

# print(wait)

time.sleep(wait) # attend le nombre de microsecondes nécessaire (converti en seconde)

'''
Création et envoi du télégramme
'''
h = datetime.datetime.now() # defini h à l'heure actuelle

# creation du telegrame
tgrm = "OAL" + h.strftime("%y%m%dF%H%M%S") + "\r"

tgrm_encoded = tgrm.encode(encoding='ascii') # encodage

ser.write(tgrm_encoded) # envoyer sur port série

# tgrm_hex = tgrm_encoded.hex() #encodage pour debug
# print("telegram ascii : ", tgrm_encoded, ", hex : ", tgrm_hex) # affiche pour debug
print(datetime.datetime.now(), " : telegram ascii : ", tgrm_encoded) # affiche le télégramme envoyé

ser.close() # fermer le port série
