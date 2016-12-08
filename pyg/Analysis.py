#! /usr/bin/python
import argparse
import os.path
import sys
import configparser


class Analysis:
    def __init__(self):
        self.tableDD = []
        parser = argparse.ArgumentParser(description="PyG : The Python Geocube Library.")
        parser.add_argument("--conf", help="Path to configuration file")
	try:
            args = parser.parse_args()
        except:
            parser.print_help()
            sys.exit(0)
        if os.path.isfile(args.conf):
            self.parseConfigFile(args.conf)
            sef.buildDD()
            print('OK')
        else:
            print("Bad Exit Return 1: Config file not found")

###########################################################################
    def parseConfigFile(self, config_file_path):
        """Fonction pour parser le fichier de configuration"""
        parser = configparser.SafeConfigParser()
        parser.read(config_file_path)
        self.seuil_snr = int(parser.get('seuils', 'snr'))
        self.seuil_elev_sat = int(parser.get('seuils', 'sat_elevation'))

        # nav data path
        self.nav_data_file = parser.get('data', 'nav')

        print(self.nav_data_file)

        # obs data paths
        self.obs_data_file = parser.get('data', 'obs').split(",")

        print(self.obs_data_file)

##########################################################################
    def buildDD(self):
        # Le nombre de DD = Nbre_de_cube - 1
        for i in range(1, len(self.obs_data_file)):
            self.tableDD.append(DoubleDifference(self.obs_data_file[0], self.obs_data_file[i]))

Analysis()
