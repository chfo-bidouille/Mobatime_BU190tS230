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

# Constantes
SERIAL_PORT = '/dev/ttyAMA0'
BAUDRATE = 9600
TELEGRAM_PREFIX = "OAL"
TELEGRAM_FORMAT = "%y%m%dF%H%M%S"
SLEEP_ON_CHANGE = 0.9
SLEEP_ON_WAIT = 0.1

def initialize_serial():
    """Initialise la connexion série avec gestion d'erreur."""
    try:
        ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUDRATE,
            bytesize=serial.SEVENBITS,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_EVEN,
            timeout=1
        )
        logger.info(f"Connecté à {ser.name}")
        return ser
    except serial.SerialException as e:
        logger.error(f"Erreur lors de la connexion au port série: {e}")
        sys.exit(1)

def send_telegram(ser, timestamp):
    """Crée et envoie un télégrame sur le port série.
    
    Args:
        ser: Objet serial.Serial
        timestamp: datetime.datetime
    """
    # Création du télégrame
    telegram = TELEGRAM_PREFIX + timestamp.strftime(TELEGRAM_FORMAT) + "\r"
    telegram_encoded = telegram.encode(encoding='ascii')
    
    try:
        ser.write(telegram_encoded)
        logger.debug(f"Télégrame envoyé: {telegram_encoded}, hex: {telegram_encoded.hex()}")
    except serial.SerialException as e:
        logger.error(f"Erreur lors de l'envoi du télégrame: {e}")

def main():
    """Boucle principale de synchronisation."""
    ser = initialize_serial()
    last_second = None
    
    try:
        while True:
            current_time = datetime.datetime.now()
            current_second = current_time.strftime("%-S")
            
            # Envoyer un télégrame si la seconde a changé
            if current_second != last_second:
                send_telegram(ser, current_time)
                last_second = current_second
                time.sleep(SLEEP_ON_CHANGE)
            else:
                time.sleep(SLEEP_ON_WAIT)
                
    except KeyboardInterrupt:
        logger.info("Arrêt du programme par l'utilisateur")
    except Exception as e:
        logger.error(f"Erreur inattendue: {e}")
    finally:
        if ser.is_open:
            ser.close()
            logger.info("Port série fermé")

if __name__ == "__main__":
    main()