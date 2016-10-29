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
        self.nav_rxm_raw = np.array(self.rxm_raw)
        print(self.nav_timegps.shape)
        print(self.nav_timeutc.shape)
        print(self.nav_posllh.shape)
        #print(self.rxm_raw.shape)

    def build_matrix(self):
        line = ''
        tmp_array = []

        f = open(self.input_file, 'r')
        for line in f:
            line = f.readline()

            if "TIMEGPS" in line:
                tmp_array = line.split(" ");
                tmp_array[1] = int(tmp_array[1])
                tmp_array[2] = int(tmp_array[2])
                tmp_array[3] = int(tmp_array[3])
                tmp_array[4] = int(tmp_array[4])
                tmp_array[5] = int(tmp_array[5])
                tmp_array[6] = int(tmp_array[6])
                self.nav_timegps.append(tmp_array[1:6]);

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
                self.nav_timeutc.append(tmp_array[1:10])

            elif "RAW" in line:
                continue;

            elif "POSLLH" in line:
                tmp_array = line.split(" ");
                tmp_array[1] = int(tmp_array[1])
                tmp_array[2] = int(tmp_array[2])
                tmp_array[3] = int(tmp_array[3])
                tmp_array[4] = int(tmp_array[4])
                tmp_array[5] = int(tmp_array[5])
                tmp_array[6] = int(tmp_array[6])
                tmp_array[7] = int(tmp_array[7])
                self.nav_posllh.append(tmp_array[1:7])

Analyzer("../bin/outt");
