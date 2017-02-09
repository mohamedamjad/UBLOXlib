#! /usr/bin/python
# Classe pour parser les fichiers Sp3

import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from timing import Timing
from mpl_toolkits.mplot3d import Axes3D

class Sp3:

    def __init__(self, file_path):
        self.sp3_data_matrix = []
        self.parse_sp3_file(file_path)
        self.sp3_data_matrix = pd.DataFrame(self.sp3_data_matrix, columns=["year", "month", "day", "hour", "minute", "seconds", "type",
                                                        "prn","x","y","z","clock","stdx","stdy","stdz","stdc","flagE",
                                                        "flagP1","flagM","flagP2","UnixGpsTime"])
        unix_gps_time = self.extractSat(16)
        print("%.2f" % unix_gps_time['UnixGpsTime'].iloc[10])
        self.getSatXYZ(5,1418005900)

    def parse_sp3_file(self, file_path):
        t = Timing()
        if not os.path.isfile(file_path):
            print ("Fichier SP3 introuvable !!")
            return

        f = open(file_path, 'r')

        for line in f:
            if line[0:1] in '*': # Debut d une epoque
                tmp_vector = [int(line[3:7]), int(line[7:10]), int(line[10:13]), int(line[13:16]), int(line[16:19]),
                              float(line[19:31])]
                for i in range(0,31):
                    line = f.next()
                    if line[0:1] in 'P':
                        tmp_vector.append(1)
                    else:
                        tmp_vector.append(0)
                    tmp_vector.append(int(line[2:4]))
                    tmp_vector.append(float(line[4:18]))
                    tmp_vector.append(float(line[18:32]))
                    tmp_vector.append(float(line[32:46]))
                    tmp_vector.append(float(line[46:60]))
                    if line[60:63] not in '   ':
                        tmp_vector.append(int(line[60:63]))
                    else:
                        tmp_vector.append(0)
                    if line[63:66] not in '   ':
                        tmp_vector.append(int(line[63:66]))
                    else:
                        tmp_vector.append(0)

                    if line[66:69] not in '   ':
                        tmp_vector.append(int(line[66:69]))
                    else:
                        tmp_vector.append(0)

                    if line[69:73] not in '    ':
                        tmp_vector.append(int(line[69:73]))
                    else:
                        tmp_vector.append(0)

                    if line[73:75] not in '  ':
                        tmp_vector.append(1)
                    else:
                        tmp_vector.append(0)

                    if line[75:76] not in ' ':
                        tmp_vector.append(1)
                    else:
                        tmp_vector.append(0)

                    if line[76:79] not in '   ':
                        tmp_vector.append(1)
                    else:
                        tmp_vector.append(0)

                    if line[79:80] not in ' ':
                        tmp_vector.append(1)
                    else:
                        tmp_vector.append(0)
                    # Ajout de l'unix gps time: le temps en secondes ecoule depuis 06/01/1980
                    tmp_vector.append(t.iso_ToUnixTime(tmp_vector[0], tmp_vector[1], tmp_vector[2], tmp_vector[3],
                                                          tmp_vector[4], int(tmp_vector[5])))
                    self.sp3_data_matrix.append(tmp_vector[0:21])
                    tmp_vector = tmp_vector[0:6]
            elif line[0:3] in 'EOF':
                return

    def extractSat(self, prn):
        sat_data = self.sp3_data_matrix.query('prn == @prn')
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(sat_data['x'], sat_data['y'], sat_data['z'], s=8, c="g", depthshade=True)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("IGS predicted ephemeris (IGU) - 2days")
        plt.show()
        """
        return sat_data

    def getSatXYZ(self, prn, unix_gps_time):
        t = Timing()
        pts = self.sp3_data_matrix.query('prn == @prn & abs(@unix_gps_time - UnixGpsTime)<=20000')
        t_mean = pts['UnixGpsTime'].mean()
        pts_validate = pts.query('index % 2 == 0')
        pts_train = pts.query('index % 2 == 1')
        regres_1 = np.poly1d(np.polyfit((pts_train['UnixGpsTime']-t_mean), (pts_train['x']),16))
        print (regres_1)
        xp = np.linspace(float(pts_train['UnixGpsTime'].min() - t_mean),
                         float(pts_train['UnixGpsTime'].max() - t_mean), 10000)
"""
        plt.plot((pts['UnixGpsTime'] - t_mean), pts['x'], '.', xp, regres_1(xp), '-')
        plt.show()

        plt.plot((pts_validate['UnixGpsTime'] - t_mean), (pts_validate['x'] - regres_1(pts_validate['UnixGpsTime'] - t_mean)))
        plt.show()
"""
        
Sp3("/home/anonyme/rtklib/RTKLIB/app/rtkrcv/gcc/temp/igu18222_00.sp3")