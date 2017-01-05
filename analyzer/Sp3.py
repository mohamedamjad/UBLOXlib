#! /usr/bin/python
# Classe pour parser les fichiers Sp3
import numpy as np
import os

class Sp3:

    def __init__(self, file_path):
        self.sp3_data_matrix = []
        self.parse_sp3_file(file_path)
        a = np.array(self.sp3_data_matrix)
        print(a.shape)

    def parse_sp3_file(self, file_path):
        if os.path.isfile( file_path ) != True:
            print ("Fichier SP3 introuvable !!")
            return

        f = open(file_path, 'r')
        tmp_vector = []

        for line in f:
            if line[0] in '*': # Debut d une epoque
                tmp_vector.append(int(line[3:7]))
                tmp_vector.append(int(line[7:10]))
                tmp_vector.append(int(line[10:13]))
                tmp_vector.append(int(line[13:16]))
                tmp_vector.append(int(line[16:19]))
                tmp_vector.append(float(line[19:31]))
                for i in range(0,31):
                    line = f.next()
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

                    if line[69:73] not in '   ':
                        tmp_vector.append(int(line[69:73]))
                    else:
                        tmp_vector.append(0)

                    if line[73:76] not in '   ':
                        tmp_vector.append(1)
                    else:
                        tmp_vector.append(0)

                    if line[76:80] not in '   ':
                        tmp_vector.append(1)
                    else:
                        tmp_vector.append(0)

                    self.sp3_data_matrix.append(tmp_vector[0:18])
                    if len(self.sp3_data_matrix)
                    tmp_vector = tmp_vector[0:7]

    def getSatEph(self, prn):

Sp3("/home/anonyme/rtklib/RTKLIB/app/rtkrcv/gcc/temp/igu19285_12.sp3")