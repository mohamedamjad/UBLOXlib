#! /usr/bin/python
import argparse

class Analysis:
    def __init__(self):
        parser = argparse.ArgumentParser(description="PyG : The Python Geocube Library.")


###########################################################################
def parseConfigFile(self, config_file_path):
    """Fonction pour parser le fichier de configuration"""
    parser = SafeConfigParser()
    parser.read(config_file_path)
    self.seuil_snr = int(parser.get('seuils', 'snr'))
    self.seuil_elev_sat = int(parser.get('seuils', 'sat_elevation'))

    # nav data path
    self.nav_data_file = parser.get('data', 'nav')

    # obs data paths
    self.obs_data_file = parser.get('data', 'obs').split(",")