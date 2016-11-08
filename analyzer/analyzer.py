#! /usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
import os.path
import sys

class Analyzer:

    def __init__(self, input_file):
        if os.path.isfile(input_file) != True:
            sys.exit("Fichier introuvable!\n")

        self.input_file = input_file;
        self.rxm_raw = []
        self.nav_timeutc = []
        self.nav_timegps = []
        self.nav_posllh = []
        self.build_matrix()
        self.nav_timegps = np.array(self.nav_timegps)
        self.nav_timeutc = np.array(self.nav_timeutc)
        self.nav_posllh = np.array(self.nav_posllh)
        self.rxm_raw = np.array(self.rxm_raw)
        print("Dimensions de la matrice NAV_TIMEGPS:"+str(self.nav_timegps.shape))
        print("Dimensions de la matrice NAV_TIMEUTC:"+str(self.nav_timeutc.shape))
        print("Dimensions de la matrice NAV_POSLLH:"+str(self.nav_posllh.shape))
        print("Dimensions de la matrice RXM_RAW:"+str(self.rxm_raw.shape))
        self.satData = np.array(self.getDataBySat(5))

        self.buildCube(1, 1000, 1000, 1000, 500)
        
        self.plot_data()

    def build_matrix(self):
        line = ''
        tmp_array = []
        sat_tmp_array = []

        f = open(self.input_file, 'r')
        for line in f:
            #line = f.readline()

            if "TIMEGPS" in line:
                tmp_array = line.split(" ");
                tmp_array[1] = int(tmp_array[1])
                tmp_array[2] = int(tmp_array[2])
                tmp_array[3] = int(tmp_array[3])
                tmp_array[4] = int(tmp_array[4])
                tmp_array[5] = int(tmp_array[5])
                tmp_array[6] = int(tmp_array[6])
                self.nav_timegps.append(tmp_array[1:7]);

            elif "TIMEUTC" in line:
                tmp_array = line.split(" ");
                tmp_array[1] = int(tmp_array[1])
                tmp_array[2] = int(tmp_array[2])
                tmp_array[3] = int(tmp_array[3])
                tmp_array[4] = int(tmp_array[4])
                tmp_array[5] = int(tmp_array[5])
                tmp_array[6] = int(tmp_array[6])
                tmp_array[7] = int(tmp_array[7])
                tmp_array[8] = int(tmp_array[8])
                tmp_array[9] = int(tmp_array[9])
                tmp_array[10] = int(tmp_array[10])
                self.nav_timeutc.append(tmp_array[1:11])

            elif "RAW" in line:
                tmp_array = line.split(" ");
                tmp_array[1] = int(tmp_array[1])
                tmp_array[2] = int(tmp_array[2])
                tmp_array[3] = int(tmp_array[3])
                tmp_array[4] = int(tmp_array[4])
                # Repeated block
                for i in range(0,int(tmp_array[3])):
                    line = f.next()
                    #line = f.readline()
                    #print(line)
                    #print(tmp_array[3])
                    tmp_array[5:13] = line.split(" ");
                    #print(tmp_array[5:13])
                    tmp_array[5] = float(tmp_array[6])
                    tmp_array[6] = float(tmp_array[7])
                    tmp_array[7] = float(tmp_array[8])
                    tmp_array[8] = int(tmp_array[9])
                    tmp_array[9] = int(tmp_array[10])
                    tmp_array[10] = int(tmp_array[11])
                    tmp_array[11] = int(tmp_array[12])
                    # fill the matrix
                    self.rxm_raw.append(tmp_array[1:12])

            elif "POSLLH" in line:
                tmp_array = line.split(" ");
                tmp_array[1] = int(tmp_array[1])
                tmp_array[2] = int(tmp_array[2])
                tmp_array[3] = int(tmp_array[3])
                tmp_array[4] = int(tmp_array[4])
                tmp_array[5] = int(tmp_array[5])
                tmp_array[6] = int(tmp_array[6])
                tmp_array[7] = int(tmp_array[7])
                self.nav_posllh.append(tmp_array[1:8])

    def buildCube(self, step, x_center, y_center, z_center, a):
        """Construire le cube qui permettera de fixer les ambiguites"""
        x = []
        y = []
        z = []

        for i in range(-a/2,a/2,1):
            x.append(i+x_center)
            y.append(i+y_center)
            z.append(i+z_center)

    def plot_data(self):
        """Fonction pour dessiner les graphs"""
        plt.plot(self.satData[:,2])
        plt.ylabel('satellite number')
        plt.show()

    def getDataBySat(self, prn):
        """Retourne une matrice d observation par satellite"""
        satData = []
        for i in range(0,self.rxm_raw.shape[0]):
            if ( self.rxm_raw[i,7] == prn):
                satData.append(self.rxm_raw[i,:])

        return satData

Analyzer("../bin/outt");
