#include "ublox_api.h"

//
UBLOX::UBLOX(std::string filename){
    file.open(filename);
}


//
std::ifstream* UBLOX::getfile(){
    return &file;
}

UBLOX::~UBLOX(){
    file.close();
}
