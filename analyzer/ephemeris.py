#! /usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import os.path
import sys
import math
import pandas as pd
from timing import Timing

class Ephemeris:

    def __init__(self, file_path):
        self.nav_data = np.array([])
        self.parseRinexNav(file_path)
        #print (self.nav_data[0])
        self.getSatXYZ_m(3, 0, 1)

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
        ome = 7.2921151467e-5

        # variables
        sqrt_a = sat_nav[17] # sqrt of semi major axis
        toe = sat_nav[18]    # Time of Ephemeris (gps seconds of week)
        delta_n = sat_nav[12]  # correction of mean motion (rad/s)
        M0 = sat_nav[13]
        e = sat_nav[15]
        omega = sat_nav[24]
        Cus = sat_nav[16]
        Cuc = sat_nav[14]
        Crc = sat_nav[23]
        Crs = sat_nav[11]
        Cic = sat_nav[19]
        Cis = sat_nav[21]
        i0 = sat_nav[22]
        IDOT = sat_nav[26]
        OMEGA = sat_nav[20]
        OMEGA_dot = sat_nav[25]

        # reference: 1995-SPS-signal-specification document, page 38
        a = math.pow(sqrt_a,2) # Semi-major axe
        n0 = math.sqrt(mu/pow(a,3)) # mean motion (rad/sec)
        tk = t - toe
        n = n0 + delta_n
        Mk = M0 + n * tk

        # Keppler equation resolution
        Em = Mk
        for i in range(0,30):
            E = Mk + e * math.sin(Em)
            Em = E
        # The true anomaly
        vk = 2 * math.atan(math.sqrt((1 + e) / (1 - e)) * math.tan(E / 2))

        # Eccentric anomaly
        Ek = math.acos((e + math.cos(vk)) / (1 + e * math.cos(vk)))

        # Argument of latitude
        phik = vk + omega

        # Second harmonic perturbations
        delta_uk = Cus * math.sin(2 * phik) + Cuc * math.cos(2 * phik) # Argument of latitude correction
        delta_rk = Crc * math.cos(2 * phik) + Crs * math.sin(2 * phik) # Radius correction
        delta_ik = Cic * math.cos(2 * phik) + Cis * math.sin(2 * phik) # Correction to inclination

        uk = phik + delta_uk # Corrected argument of latitude
        rk = a * (1 - e * math.cos(Ek)) + delta_rk # Corrected radius
        ik = i0 + delta_ik + IDOT * tk

        # Positions in orbital plane
        xk_diff = rk * math.cos(uk)
        yk_diff = rk * math.sin(uk)

        # Corrected longitude of ascending node
        OMEGAk = OMEGA + (OMEGA_dot - ome) * tk - ome * toe

        # ECEF
        xk = xk_diff * math.cos(OMEGAk) - yk_diff * math.cos(ik) * math.sin(OMEGAk)
        yk = xk_diff * math.sin(OMEGAk) + yk_diff * math.cos(ik) * math.cos(OMEGAk)
        zk = yk_diff * math.sin(ik)

        return [xk, yk, zk]

    def getSatXYZ_m(self, prn, t_start, t_end):
        time = Timing()
        df_ephemeris = pd.DataFrame(self.nav_data, columns=['prn', 'year', 'month', 'day', 'hour', 'min', 'sec',
                                                            'sv_clock_bias', 'sv_clock_drift', 'sv_clock_drift_rate',
                                                            'IODE', 'Crs', 'Delta_n', 'M0', 'Cuc', 'e', 'Cus', 'sqrt_A',
                                                            'Toe', 'Cic', 'OMEGA', 'CIS', 'i0', 'Crc', 'omega',
                                                            'OMEGA_DOT', 'IDOT', 'Codes_L2_channel', 'GPS_week',
                                                            'L2_P_data_flag', 'SV_accuracy', 'SV_health', 'TGD',
                                                            'IODC', 'transmission_time', 'fit_interval'])
        df_ephemeris["UnixGPSTime"] = time.iso_ToGPSUnixTime(df_ephemeris.year, df_ephemeris.month, df_ephemeris.day)
        subDataFrame = df_ephemeris.query('prn == @prn')

Ephemeris('/home/anonyme/Téléchargements/brdc2060.16n')