#!/usr/bin/python

# Authoren uprusch&mpoehl

# Funktions-Modul fuer mux.py
# Sucht in altem Logfile nach dem letzt geschaltetem Ventil und counter

import os

# liest letzte Zeile des Logfiles als Array
logfilename = 'mux.log'

if os.path.isfile(logfilename):
        a = open(logfilename, "r").readlines()
        line = a[-1].split(' ')
        Val = int(line[3])
        counter = int(line[0])
        if Val == 68:
                Val=69
else:
        text_file = open(logfilename, "a")
        text_file.write("Cycle" + " " + "Date" + " " + "Time" + " " + "open_pin" + " " + "closed_pin" + " " + "Chamber" + " " + "gnu" + " " + "Record" + " " + "Unix_Timestamp" +"\n")
        text_file.close()
        counter=0
        Val=86

#---------------------Funktionen--------------------------#
# Funktion Filename
def file():
        return logfilename

# Funktion counter() aus Datei
def count():
        return counter

# Funktion Val() aus Datei
def Valve():
        return Val
