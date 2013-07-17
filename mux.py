#!/usr/bin/python

#Authoren uprusch&mpoehl

#Multiplexer mit 16 Ausgaengen, die Hardware ist ein IO/32 von http://www.abelectronics.co.uk. an einem Raspberry PI Version B
#Die Schaltung wurde um einen Photomosfet(AQY210EH) und eine Relaiskarte je IO erweitert.
#Somit lassen Spannungen von bis zu 125V mit 3A beliebig schalten. Die Schaltspannung ist galvanisch vom Raspberry PI getrennt.


#Beginnt jeden Zyklus in einer vollen Minute
#Schaltet einen Zyklus mit 14 Ventilen in 1:30 Stunden:Minuten
#gegen Mitternacht zwischen 00:00 und 01:31 wird ein zusaetzliches Ventil anstatt Ch1 einmalig angesteuert
#Zeichnet die Schaltvorgaenge in einer Datei auf

import os
import sys
import wiringpi2
import time
import datetime


import read_file as rf

pin_base = 65
i2c_addr = 0x20
i2c_addr_2 = 0x21

wiringpi2.wiringPiSetup()
wiringpi2.mcp23017Setup(pin_base,i2c_addr)
wiringpi2.mcp23017Setup(pin_base+16,i2c_addr_2)

#reset_mux.reset()
for pin in range(65,96):
        wiringpi2.pinMode(pin,1)
        wiringpi2.digitalWrite(pin,0)

#oeffne Ambient 1 bis zum start
wiringpi2.digitalWrite(66,1)

logfilename = rf.file()

timecheck = False

rec = 0
counter = rf.count()
#sleep = 3              # fast
#sleep = 10*60/14       # 5 Minuten / Ventilanzahl
sleep = 90*60/14-0.2    #90 minuten

Sl = 65         #Hauptventil Chambers
Valve = [66, 69, 70, 71, 72, 73, 74, 67, 81, 82, 83, 84, 85, 86]
Chamber =["Ambient1", "Ch1", "Ch2", "Ch3", "Ch4", "Ch5", "Ch6", "Ambient2", "Ch7", "Ch8", "Ch9", "Ch10", "Ch11", "Ch12"]
gnu =[-1, 1, 2, 3, 4, 5, 6, -2, 7, 8, 9, 10, 11, 12]
Chamber = Chamber[Valve.index(rf.Valve())+1:]+Chamber[:Valve.index(rf.Valve())+1]
gnu = gnu[Valve.index(rf.Valve())+1:]+gnu[:Valve.index(rf.Valve())+1]
Valve = Valve[Valve.index(rf.Valve())+1:]+Valve[:Valve.index(rf.Valve())+1]


try:                                                                            #kontrollierter Abbruch durch ^C
#       while timecheck == False:
        while True:
                lt = time.localtime()
                if lt[5] ==0:                                                   #Beginn jede volle Minute nach Ende des Zyklus
                        counter = counter + 1
                        if lt[3] ==0 or lt[3] ==1  and lt[4] < 31:              #Mitternacht Cal-Gas
                                Valve=[68 if x==69 else x for x in Valve]
                                Chamber=["Cal-Gas" if x=="Ch1" else x for x in Chamber]
                                gnu=[-3 if x==1 else x for x in gnu]
                        else:
                                Valve = [66, 69, 70, 71, 72, 73, 74, 67, 81, 82, 83, 84, 85, 86] #Pins des Chips
                                Chamber =["Ambient1", "Ch1", "Ch2", "Ch3", "Ch4", "Ch5", "Ch6", "Ambient2", "Ch7", "Ch8", "Ch9", "Ch10", "Ch11", "Ch12"] #Kammern analog zu pin
                                gnu =[-1, 1, 2, 3, 4, 5, 6, -2, 7, 8, 9, 10, 11, 12]
                                Chamber = Chamber[Valve.index(rf.Valve())+1:]+Chamber[:Valve.index(rf.Valve())+1]               # shuffle den Array auf die naechste Kammer nachdem Val=letzte Kammer aus der Datei ist
                                gnu = gnu[Valve.index(rf.Valve())+1:]+gnu[:Valve.index(rf.Valve())+1]                                           # tue dies auch mit den Alias
                                Valve = Valve[Valve.index(rf.Valve())+1:]+Valve[:Valve.index(rf.Valve())+1]                             # ebenso fur gnuplot

                        for i in range(len(Valve)):
                                rec = rec +1
                                text_file = open(logfilename, "a")
                                currentdatetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                ds = str(counter), currentdatetime, str(Valve[i]), str(Valve[i-1]), str(Chamber[i]), str(gnu[i]), str(rec), time.time()
                                print (counter, currentdatetime, Valve[i], Valve[i-1], Chamber[i], rec)
                                text_file.write(ds[0] + " " + ds[1] + " " + ds[2] + " " + ds[3] + " " + ds[4] + " " + ds[5] + " " + ds[6] + " " + str(ds[7]).replace(".", ",") + "\n")
                                text_file.close()
                                if Valve[i] == 66 or Valve[i] == 67 or Valve[i] ==68:   #Ref Gase Ambient sind am Port 66 und 67 angeschlossen Cal-Gas=68
                                        wiringpi2.digitalWrite(Valve[i],1)      #oeffnet aktuelles Ventil
                                        wiringpi2.digitalWrite(Valve[i-1],0)    #schliesst vorheriges Ventil
                                        wiringpi2.digitalWrite(Sl,0)            #schliesst Probenventil
                                        time.sleep(sleep)                       #wartet und laesst das aktuelle Ventil solange offen
                                else:
                                        wiringpi2.digitalWrite(Sl,1)            #oeffnet Probenventil
                                        wiringpi2.digitalWrite(Valve[i],1)      #oeffnet aktuelles Ventil
                                        wiringpi2.digitalWrite(Valve[i-1],0)    #schliesst vorheriges Ventil
                                        time.sleep(sleep)                       #wartet und laesst das aktuelle Ventil solange offen
                                if counter == 10000:                            #macht das Ganze vorerst xxx zyklen
                                        timecheck = True
except KeyboardInterrupt:
        #reset mux after ^C
#       for pin in range(65,96):
#               wiringpi2.pinMode(pin,1)
#               wiringpi2.digitalWrite(pin,0)
        #oeffne Ambient 1 bis zum start
#       wiringpi2.digitalWrite(66,1)
        print '\n' 'Programm wurde durch den Benutzer abgebrochen'

