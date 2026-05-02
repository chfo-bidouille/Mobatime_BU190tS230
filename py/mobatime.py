#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 08:44:43 2026

@author: christophe
"""

import time
from datetime import datetime, timedelta
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
Faire une boucle pour envoyer plusieurs fois de suite un télégramme.
Un seul télégramme différent n'est pas pris en compte
(situation au changement d'heure été/hiver)
'''
i = 0
while i < 5:

    '''
    Attendre l'heure exacte 

    attend ( 100000 - "le nombre de microsecondes actuelles" / 100000) = attend le nombre de 
    microsecondes jusqu'au début de la seconde suivante
    '''
    time.sleep((1000000-int(datetime.now().strftime("%f"))) / 1000000)

    '''
    Création et envoi du télégramme

    h = l'heure actuelle
    h = l'heure actuelle ajustée avec timedelta peut ajouer ou soustraire du temps)
    ser.write = génère, encode le télégramme en ascii et envoie sur le port série
    ser.close = ferme le port série
    '''
    h = datetime.now()
    #h = datetime.now() + timedelta(hours=1) # crée un décalage
    ser.write(h.strftime("OAL%y%m%dF%H%M%S\r").encode(encoding='ascii'))

    print("Télégramme Mobatime [",h.strftime("OAL%y%m%dF%H%M%S\r").encode(encoding='ascii'),"] envoyé à :",h.strftime("%H:%M:%S,%f"))

    time.sleep(4)

    i +=1
    
ser.close()
print(f"Connection à {ser.name} fermée")
