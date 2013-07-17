mux
===

Multiplexer with Raspberry PI Python


Dieser Code ist zum Schalten eines Gasmultiplexers gedacht. 
Hinter dem Multiplexer sind Gasanalysatoren die die jeweilige Probenluft analysieren sollen.
(FTIR, Picarro, Vaisalla) 


Zur Hardware werden ein Raspberry PI Model B und ein IO32 Extension board benötigt.
Des Weiteren benötigt man für jeden gesteuerten Ausgang entsprechende Hardware.
Bei mir sind das PhotoMosfets und Relaiplatinen, die derzeit 125V mit 3 A schalten können.
Meine Ventile sind von Sirai Modell:Z030A 24V - 3 Wege


Geschaltet werden 12 Probenventile, 1 Hauptventil für die Proben, 2 Referenzgase, 1 Kalibrier-Gas
Insgesamt 16 Ventile wobei das Hauptventil für die Messungen der 12 Probenventile offen steht.

Ein Durchlauf = Zyklus dauert 1:30 Stunde (es werden immer 14 Gase gemessen)
Ein Zyklus beginnt immer zur vollen Minute.
Um Mitternacht erfolgt ein Ventiltausch, sodass ein Kalibriergas anstatt der 1. Probe gemessen wird

[die Zykuszeit wir derzeit noch mit einer sleep. erledigt, das ist recht unelegant und soll noch ersetztwerden]

Wird das Skript zu ersten Mal gestartet, legt es eine Datei namens 'mux.log' an. In die erste Zeile werden Header-Informationen
geschrieben. Danach dann die Schaltzustände des Multiplexers.

Ist diese Logdatei schon vorhanden, so holt sich das Skript alle nötigen 
Informationen aus der Datei und fährt an der letzten Stelle fort.

Damit die Anlage kein Vakuum in das System zieht, ist immer ein Ventil offen. Bei Abbruch des Programms bleibt das letzt gemessene
Ventil offen.



ToDo:
-Upgrade auf min. 40 Proben-Ventile von Sirai Z530A 24V
-sleep mit einer Real-Time funktion ersetzen
-IO Platine selbst erstellen mit 128 I/O durch 8 MCP23017, da die IO 32 Varriante beim Kaskadenaufbau recht wackelig ist.  
