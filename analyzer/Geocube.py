#! /usr/bin/python

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os.path
import sys
import math


class Geocube:
    def __init__(self, input_file):
        if os.path.isfile(input_file) != True:
            sys.exit("Fichier introuvable!\n")

        self.x_cube_vector = []
        self.y_cube_vector = []
        self.z_cube_vector = []
        self.rms_cube_vector = []

        self.input_file = input_file

        self.rxm_raw = []
        self.nav_timeutc = []
        self.nav_timegps = []
        self.nav_posllh = []

        self.build_matrix()

        self.nav_timegps = np.array(self.nav_timegps)
        self.nav_timeutc = np.array(self.nav_timeutc)
        self.nav_posllh = np.array(self.nav_posllh)
        self.rxm_raw = np.array(self.rxm_raw)
        print("Dimensions de la matrice NAV_TIMEGPS:" + str(self.nav_timegps.shape))
        print("Dimensions de la matrice NAV_TIMEUTC:" + str(self.nav_timeutc.shape))
        print("Dimensions de la matrice NAV_POSLLH:" + str(self.nav_posllh.shape))
        print("Dimensions de la matrice RXM_RAW:" + str(self.rxm_raw.shape))

        self.posllh_posxyz()

        self.buildCube(1000, 1000, 1000, 1, 10)


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
                tmp_array[2] = float(tmp_array[2])
                tmp_array[3] = float(tmp_array[3])
                tmp_array[4] = float(tmp_array[4])
                tmp_array[5] = int(tmp_array[5])
                tmp_array[6] = int(tmp_array[6])
                tmp_array[7] = int(tmp_array[7])
                self.nav_posllh.append(tmp_array[1:8])

    def posllh_posxyz(self):
        """Construire le cube qui permettera de fixer les ambiguites"""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        cart = [1.0,1.0,1.0]

        for i in range(0, self.nav_posllh.shape[0]):
            [cart[0], cart[1], cart[2]] = self.geo2cart(self.nav_posllh[i,1]*math.pow(10,-7), self.nav_posllh[i,2]*math.pow(10,-7), self.nav_posllh[i,3]*math.pow(10,-3))
            self.nav_posllh[i, 1] = float(cart[0])
            self.nav_posllh[i, 2] = float(cart[1])
            self.nav_posllh[i, 3] = float(cart[2])
        ax.scatter(self.nav_posllh[:,1], self.nav_posllh[:,2], self.nav_posllh[:,3], zdir='z', s=8, c="g", depthshade=True)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("Distribution des positions (cartesiennes) naviguees sur 24h")
        plt.show()

    def geo2cart(self, lon, lat, height):
        """Transformer les coordonnees geographiques en cartesiennes"""
        cart = [1.0,1.0,1.0]
        cosLat = math.cos(lat * math.pi / 180.0)
        sinLat = math.sin(lat * math.pi / 180.0)
        cosLon = math.cos(lon * math.pi / 180.0)
        sinLon = math.sin(lon * math.pi / 180.0)
        rad = 6378137.0
        f = 1.0 / 298.257224
        C = 1.0 / math.sqrt(cosLat * cosLat + (1 - f) * (1 - f) * sinLat * sinLat)
        S = (1.0 - f) * (1.0 - f) * C
        cart[0] = (rad * C + height) * cosLat * cosLon
        cart[1] = (rad * C + height) * cosLat * sinLon
        cart[2] = (rad * S + height) * sinLat
        return cart

    def plot_data(self):
        """Fonction pour dessiner les graphs"""
        plt.plot(self.nav_posllh[:,3])
        plt.ylabel('satellite number')
        plt.show()

    def getDataBySat(self, prn):
        """Retourne une matrice d observation par satellite"""
        satData = []
        for i in range(0,self.rxm_raw.shape[0]):
            if ( self.rxm_raw[i,7] == prn):
                satData.append(self.rxm_raw[i,:])

        return satData

    def buildCube(self, x_center, y_center, z_center, step, cote):
        """Fonction qui retourne un cube centre autour d un point defini par (x_center, y_center, z_center)"""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for i in range(-cote/2, cote/2, step):
            for j in range(-cote/2, cote/2, step):
                for k in range(-cote / 2, cote / 2, step):
                    self.z_cube_vector.append(k + z_center)
                    self.y_cube_vector.append(j + y_center)
                    self.x_cube_vector.append(i + x_center)

        ax.scatter(self.x_cube_vector, self.y_cube_vector, self.z_cube_vector, s=8, c="g", depthshade=True)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("Le cube")
        plt.show()