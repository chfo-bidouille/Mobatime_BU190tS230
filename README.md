### Pilotage d'une horloge Mobatime BU190(t) S 230 depuis un Raspberry PI 5 via une liaison RS-232 avec un script python.

 - Script mobatime.py executé par un timer systemd
 - Télégramme IF485 envoyé 5 fois avec une pause de quelques secondes.
 - Un télégramme avec une grande différence d'heure est ignoré par le mouvement. (changement d'heure été/hiver)
 - Possibilité de simuler un changement d'heure en décommentant la ligne h = datetime.now() + timedelta(hours=1)

__Raccordement__ :

 - Raspberry PIN 6  (GND) vers pin 2 du connecteur RJ12 de l'horloge
 - Raspberry PIN 8  (UART0 Tx) vers pin 1 du connecteur RJ12 de l'horloge
 - Raspberry PIN 10 (UART0 Rx) vers pin 3 du connecteur RJ12 de l'horloge
