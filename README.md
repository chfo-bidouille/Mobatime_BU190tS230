### Pilotage d'une horloge Mobatime BU190(t) S 230 depuis un Raspberry PI 5 via une liaison RS-232 avec un script python.

Script mobatime.py executé par un timer systemd 2 minutes après un redémarrage puis toutes les heures aux .59 (*-*-* *:59:00)

__Raccordement__ :

 - Raspberry PIN 6 (GND) vers pin 2 du connecteur RJ12 de l'horloge
 - Raspberry PIN 8 (UART0 Tx) vers pin 1 du connecteur RJ12 de l'horloge
 - Raspberry PIN 10 (UART0 Rx) vers pin 3 du connecteur RJ12 de l'horloge
