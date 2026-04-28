#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 08:44:43 2026

@author: christophe
"""

import time
import datetime
import serial

'''
Ouvre et configure le port série

/dev/ttyAMA0 ou /dev/ttyAMA10
9600 bits/s
7 bits de données
1 bit d'arrêt
parité paire
'''
ser = serial.Serial(
        port='/dev/ttyAMA0',
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
(utilse 999900 pour compenser le temps d'execution du programme (~100 - 150 microsecondes))
'''
time.sleep((999900-int(datetime.datetime.now().strftime("%f"))) / 1000000)

'''
Création et envoi du télégramme

h = l'heure prise en compte pour le télégramme
ser.write = génère, encode le télégramme en ascii et envoie sur le port série
ser.close = ferme le port série
'''
h = datetime.datetime.now()
ser.write(h.strftime("OAL%y%m%dF%H%M%S\r").encode(encoding='ascii'))

print(h, ": télégramme envoyé")

ser.close()
print(f"Connection à {ser.name} fermée")
