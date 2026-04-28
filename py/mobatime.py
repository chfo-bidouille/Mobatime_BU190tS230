#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 08:44:43 2026

@author: christophe
"""

import time
import datetime
import serial

ser = serial.Serial( # ouvrir et configurer le port série
        port='/dev/ttyAMA0', # /dev/ttyAMA0 ou /dev/ttyAMA10
        baudrate=9600,
        bytesize=serial.SEVENBITS,
        stopbits=serial.STOPBITS_ONE,
        parity=serial.PARITY_EVEN,
        timeout=1
        )
print(f"Connecté à {ser.name}")

'''
Attendre l'heure exacte 

attend ( 100000 - "le nombre de microsecondes actuelles" / 100000) = attend le nombre de 
microsecondes jusqu'au début de la seconde suivante
'''
time.sleep((1000000-int(datetime.datetime.now().strftime("%f"))) / 1000000)

'''
Création et envoi du télégramme

tgrm = le télégramme
ser.write = encode le télégramme en ascii et envoie sur le port série
ser.close = ferme le port série
'''
tgrm = "OAL" + datetime.datetime.now().strftime("%y%m%dF%H%M%S") + "\r"
ser.write(tgrm.encode(encoding='ascii'))

print(datetime.datetime.now(), ": télégramme envoyé = ", tgrm.encode(encoding='ascii'))

ser.close()
print(f"Connection à {ser.name} fermée")
