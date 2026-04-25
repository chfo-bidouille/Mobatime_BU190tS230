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
import signal

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration des constantes
SERIAL_PORT = '/dev/ttyAMA0'  # /dev/ttyAMA0 ou /dev/ttyAMA10
BAUD_RATE = 9600
SEND_INTERVAL = 60  # secondes
TELEGRAM_PREFIX = "OAL"
EXPECTED_TELEGRAM_LENGTH = 21  # "OAL" (3) + date/heure (14) + "\r" (1) + "F" (1) = 20 + 1 padding


def signal_handler(sig, frame):
    """Gestionnaire d'arrêt gracieux du programme."""
    logger.info("Arrêt du programme...")
    sys.exit(0)


def create_telegram(timestamp):
    """
    Crée un télégrame au format Mobatime.
    
    Args:
        timestamp: objet datetime
        
    Returns:
        str: télégrame au format "OAL" + YYMMDDFhhmmss + "\r"
    """
    tgrm = TELEGRAM_PREFIX + timestamp.strftime("%y%m%dF%H%M%S") + "\r"
    return tgrm


def main():
    """Fonction principale."""
    # Configuration du gestionnaire de signal pour Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Ouverture du port série avec context manager
        with serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            bytesize=serial.SEVENBITS,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_EVEN,
            timeout=1
        ) as ser:
            if not ser.is_open:
                logger.error("Le port série ne s'est pas ouvert correctement")
                sys.exit(1)
            
            logger.info(f"Connecté à {ser.name}")
            
            while True:
                try:
                    # Récupère l'heure actuelle
                    s0 = datetime.datetime.now()
                    
                    # Crée le télégrame
                    tgrm = create_telegram(s0)
                    
                    # Valide la longueur du télégrame
                    if len(tgrm) != EXPECTED_TELEGRAM_LENGTH:
                        logger.warning(f"Longueur inattendue du télégrame: {len(tgrm)} (attendu: {EXPECTED_TELEGRAM_LENGTH})")
                    
                    # Encode en ASCII
                    tgrm_encoded = tgrm.encode(encoding='ascii')
                    
                    # Affiche pour debug
                    logger.debug(f"Télégrame envoyé: {tgrm_encoded}")
                    
                    # Envoie sur le port série
                    ser.write(tgrm_encoded)
                    logger.info(f"Télégrame envoyé: {tgrm.strip()}")
                    
                    # Attends avant le prochain envoi
                    time.sleep(SEND_INTERVAL)
                    
                except serial.SerialException as e:
                    logger.error(f"Erreur lors de l'écriture sur le port série: {e}")
                    time.sleep(5)  # Attends 5 secondes avant de réessayer
                except UnicodeEncodeError as e:
                    logger.error(f"Erreur d'encodage: {e}")
                    
    except serial.SerialException as e:
        logger.error(f"Erreur lors de l'ouverture du port série: {e}")
        logger.error(f"Vérifiez que le port {SERIAL_PORT} existe et est accessible")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Interruption utilisateur détectée")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erreur inattendue: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()