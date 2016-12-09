#! /usr/bin/python
# -*- coding: utf-8 -*-
import math
from Geocube import Geocube
from ephemeris import Ephemeris
from ConfigParser import SafeConfigParser
import numpy as np

# Constants
LAMBDA_L1 = 0.190293672798

class Analyzer:

    ###########################################################################

    def __init__(self, config_file_path):
        print("PyG V 0.0.1 .. ")
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

        self.cleanObservations()
        print("SEUIL SNR: "+str(self.seuil_snr)+"\n")
        print("SEUIL ELEVATION SATELLITE: " + str(self.seuil_elev_sat) + "\n")
        print("OBS FILE LIST: "+ str(self.obs_data_file) +"\n")
        self.buildDoubleDifferences()


    ###########################################################################
    def parseConfigFile(self, config_file_path):
        """Fonction pour parser le fichier de configuration"""
        parser = SafeConfigParser()
        parser.read(config_file_path)
        self.seuil_snr = int(parser.get('seuils', 'snr'))
        self.seuil_elev_sat = int(parser.get('seuils','sat_elevation'))

        # nav data path
        self.nav_data_file = parser.get('data','nav')

        # obs data paths
        self.obs_data_file = parser.get('data','obs').split(",")

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

#    def buildDoubleDifferences(self):
#        """Construire les doubles differences. Pour construire les DD on va choisir un cube pivot et un satellite pivot
#        Le choix du satellite pivot se base sur l'élevation, le cube pivot est choisit par l'utilisateur. C'est le prem-
#        ier cube renseigné dans la liste des cubes"""


    ###########################################################################
    def sat_rec_vector(self, x_s, y_s, z_s, x_r, y_r, z_r):
        """Calculer le vecteur recepteur -> satellite"""
        V = []
        V.append(x_s - x_r)
        V.append(y_s - y_r)
        V.append(z_s - z_r)
        return V

Analyzer("/home/anonyme/UBLOXlib/analyzer/config.ini")