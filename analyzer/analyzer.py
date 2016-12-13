#! /usr/bin/python
# -*- coding: utf-8 -*-
import math
from timing import Timing
from Geocube import Geocube
from generic_functions import *
from ephemeris import Ephemeris
from ConfigParser import SafeConfigParser
import numpy as np
import math

# Constants
LAMBDA_L1 = 0.190293672798

class Analyzer:

    ###########################################################################

    def __init__(self, config_file_path):
        print("PyG V 0.0.1 .. ")
        self.coord_pivot = [0.0, 0.0, 0.0]
        self.coord_mobile = [0.0, 0.0, 0.0]
        self.seuil_snr = 0
        self.seuil_elev_sat = 0
        self.nav_data_file = ""
        self.obs_data_file = []
        self.obs = [] # Tableau contient les observations par cube
        self.dd = [] # Structure contient les DD par cube

        self.parseConfigFile(config_file_path)


        self.eph = Ephemeris(self.nav_data_file)

        # Instanciation des Geocubes en utilisant la liste des paths renseignée dans le fichier de conf.
        for i in range(0,len(self.obs_data_file)):
            self.obs.append(Geocube(self.obs_data_file[i]))

        #self.cleanObservations()
        print("SEUIL SNR: "+str(self.seuil_snr)+"\n")
        print("SEUIL ELEVATION SATELLITE: " + str(self.seuil_elev_sat) + "\n")
        print("OBS FILE LIST: "+ str(self.obs_data_file) +"\n")
        self.buildDoubleDifferences()


    ###########################################################################
    def parseConfigFile(self, config_file_path):
        """Fonction pour parser le fichier de configuration"""
        parser = SafeConfigParser()
        parser.read(config_file_path)
        self.seuil_snr      = int(parser.get('seuils', 'snr'))
        self.seuil_elev_sat = int(parser.get('seuils','sat_elevation'))

        # nav data path
        self.nav_data_file  = parser.get('data','nav')
        self.coord_pivot    = [float(parser.get('data','x_pivot')), float(parser.get('data','y_pivot')), float(parser.get('data','z_pivot'))]
        self.coord_mobile   = [float(parser.get('data','x_mobile')), float(parser.get('data','y_mobile')), float(parser.get('data','z_mobile'))]

        # obs data paths
        self.obs_data_file  = parser.get('data','obs').split(",")

    ###########################################################################
    def simpleDifference(self, phase_r1_s1, phase_r1_s2):
        """Fonction pour calculer les simples differences"""
        sd = phase_r1_s1 - phase_r1_s2
        return sd

    ###########################################################################
    def cleanObservations(self):
        j=0
        """Fonction pour supprimer les observations qui ne respectent pas les seuils"""

        for i in range(0, len(self.obs)):
            # Suppression des données avec SNR
            for raw in self.obs[i].rxm_raw:
                j+=1
                if raw[9] <= self.seuil_snr:
                    self.obs[i].rxm_raw = np.delete(self.obs[i].rxm_raw, j)
                    j-=1

    def doubleDifference(self, phase_r1_s1, phase_r1_s2, phase_r2_s1, phase_r2_s2):
        """Fonction pour calculer les doubles differences"""
        dd = self.simpleDifference(phase_r1_s1, phase_r1_s2) - self.simpleDifference(phase_r2_s1, phase_r2_s2)
        return dd

    def getRo(self, x_sat, y_sat, z_sat, x_rec, y_rec, z_rec):
        """Calculer la pseudo distance entre le recepteur et le satellite"""
        return math.sqrt(pow(x_sat - x_rec, 2) + pow(y_sat - y_rec, 2) + pow(z_sat - z_rec, 2))

    def getRMS(self, phase_double_difference, pseudorange_double_difference):
        """Fonction pour calculer le RMS"""
        return (phase_double_difference - (1/LAMBDA_L1 * pseudorange_double_difference + math.floor(phase_double_difference - 1/LAMBDA_L1 * pseudorange_double_difference)))

    ###########################################################################
    def sat_rec_vector(self, x_s, y_s, z_s, x_r, y_r, z_r):
        """Calculer le vecteur recepteur -> satellite"""
        V = []
        V.append(x_s - x_r)
        V.append(y_s - y_r)
        V.append(z_s - z_r)
        return V

    ###########################################################################
    """and math.fabs(t.weekToW_ToGPSUnixTime(
                        self.obs[0].rxm_raw[i,1], self.obs[0].rxm_raw[i,0]) - t.iso_ToGPSUnixTime(
                        year, month, day, hour, minute, sec
                    )) < 3600"""
    def buildDoubleDifferences(self):
        """Construire les doubles differences"""
        coord_sat_tmp = [0.0, 0.0, 0.0]
        t = Timing()
        # Il faut d'abord choisir le satellite pivot
        for i in range(0, self.obs[0].rxm_raw.shape[0]):

            for j in range(0, self.eph.nav_data.shape[0]):

                year = int(self.eph.nav_data[j, 1]) + 2000
                month = int(self.eph.nav_data[j, 2])
                day = int(self.eph.nav_data[j, 3])
                hour = int(self.eph.nav_data[j, 4])
                minute = int(self.eph.nav_data[j, 5])
                sec = int(self.eph.nav_data[j, 6])

                if self.obs[0].rxm_raw[i,7] == self.eph.nav_data[j,0] and math.fabs(t.weekToW_ToGPSUnixTime(
                        self.obs[0].rxm_raw[i,1], self.obs[0].rxm_raw[i,0]) - t.iso_ToGPSUnixTime(
                        year, month, day, hour, minute, sec
                        )) < 3600000:
                    print(math.fabs(t.weekToW_ToGPSUnixTime(
                        self.obs[0].rxm_raw[i,1], self.obs[0].rxm_raw[i,0]) - t.iso_ToGPSUnixTime(
                        year, month, day, hour, minute, sec
                        )))

        for i in range(1, len(self.obs)):
            # Le nombre des DD = Nbre de cubes fixes x Nbre de cube mobile
            print("OK2")

    ###########################################################################
    def getSatElevation(self, x_s, y_s, z_s, x_r, y_r, z_r):
        """Calculer l elevation d un satellite"""
        sat_rec_geoc = self.sat_rec_vector(x_s, y_s, z_s, x_r, y_r, z_r)
        sat_rec_loc  = geocentrique2local(sat_rec_geoc[0], sat_rec_geoc[1], sat_rec_geoc[2])
        norm = math.sqrt( sat_rec_loc[0,0] * sat_rec_loc[0,0] + sat_rec_loc[1,0] * sat_rec_loc[1,0] + sat_rec_loc[2,0] * sat_rec_loc[2,0] )
        elevation = math.asin(sat_rec_geoc[2] / norm )
        return elevation

    ###########################################################################

a = Analyzer("/home/anonyme/UBLOXlib/analyzer/config.ini")
a.getSatElevation(13416746.195,-22186753.441,6248864.499,4201792.2950,177945.2380,4779286.6850)