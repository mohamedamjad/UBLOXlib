#! /usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import os.path
import sys
import math

class Ephemeris:

    def __init__(self, file_path):
        self.nav_data = np.array([])
        self.parseRinexNav(file_path)
        print(self.nav_data[452,0])

    def parseRinexNav(self, file_path):
        if os.path.isfile(file_path) != True:
            sys.exit("Fichier introuvable!\n")

        f = open(file_path, 'r')
        end_header_flag = False
        epoch_buffer = ""
        nav_matrix = []
        for line in f:
            if "END OF HEADER" in line:
                end_header_flag = True
            elif end_header_flag == False:
                continue
            elif line[5] == " " and line[8] == " " and end_header_flag == True:
                epoch_buffer += line
                for i in range(0,7):
                    line = f.next()
                    epoch_buffer += line
                tupple = []
                epoch_buffer = epoch_buffer.replace("D", "e")
                epoch_buffer = epoch_buffer.replace("\n"," ")
                tupple = [int(epoch_buffer[0:2]), int(epoch_buffer[2:5]), int(epoch_buffer[5:8]),
                          int(epoch_buffer[8:11]), int(epoch_buffer[11:14]), int(epoch_buffer[14:17]),
                          float(epoch_buffer[17:22]), float(epoch_buffer[22:41]), float(epoch_buffer[41:60]),
                          float(epoch_buffer[60:79]), float(epoch_buffer[83:102]), float(epoch_buffer[102:121]),
                          float(epoch_buffer[121:140]), float(epoch_buffer[140:159]), float(epoch_buffer[163:182]),
                          float(epoch_buffer[182:201]), float(epoch_buffer[201:220]), float(epoch_buffer[220:239]),
                          float(epoch_buffer[243:262]), float(epoch_buffer[262:281]), float(epoch_buffer[281:300]),
                          float(epoch_buffer[300:319]), float(epoch_buffer[323:342]), float(epoch_buffer[342:361]),
                          float(epoch_buffer[361:380]), float(epoch_buffer[380:399]), float(epoch_buffer[403:422]),
                          float(epoch_buffer[422:441]), float(epoch_buffer[441:460]), float(epoch_buffer[460:479]),
                          float(epoch_buffer[483:502]), float(epoch_buffer[502:521]), float(epoch_buffer[521:540]),
                          float(epoch_buffer[540:559]), float(epoch_buffer[563:582])]
                if len(epoch_buffer) > 584:
                    tupple.append(float(epoch_buffer[582:601]))
                else:
                    tupple.append(0.0)
                nav_matrix.append(tupple)
                epoch_buffer = ""
        self.nav_data = np.array(nav_matrix)


    def getSatXYZ(self, t, sat_nav):

        # constantes
        mu = 3.986005e+14

        # variables
        sqrt_a = sat_nav[17] # sqrt of semi major axis
        toe = sat_nav[18]    # Time of Ephemeris (gps seconds of week)
        delta_n = sat_nav[12]  # correction of mean motion (rad/s)
        M0 = sat_nav[13]
        e = sat_nav[15]

        # reference: 1995-SPS-signal-specification document, page 38
        a = math.pow(sqrt_a,2) # Semi-major axe
        n0 = math.sqrt(mu/pow(a,3)) # mean motion (rad/sec)
        tk = t - toe
        n = n0 + delta_n
        Mk = M0 + n * tk

        # Keppler equation resolution
        Em = Mk
        for i in range(0,30):
            E = Mk + e * sin(Em)
            Em = E
        # The true anomaly
        


Ephemeris("/home/anonyme/Téléchargements/brdc2940.16n")