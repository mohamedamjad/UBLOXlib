#! /usr/bin/python
# -*- coding: utf-8 -*-
import math
from Geocube import Geocube
from ephemeris import Ephemeris

# Constants
LAMBDA_L1 = 0.190293672798


class Analyzer:

    def __init__(self):
        print("PyG V 0.0.1 .. ")
        g1 = Geocube("../bin/outt")
        eph = Ephemeris("/home/anonyme/Téléchargements/brdc2940.16n")
        g2 = Geocube("../bin/outt")

    def simpleDifference(self, phase_r1_s1, phase_r1_s2):
        """Fonction pour calculer les simples differences"""
        sd = phase_r1_s1 - phase_r1_s2
        return sd

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

    def buildDoubleDifferences(self):
        """Construire les doubles differences"""

        for i in range(0, )


Analyzer()