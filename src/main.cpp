#include"ublox_api.h"
#include<iostream>
int main(){
  UBLOX ubx("../test");
  std::cout<<"OK\n"<<ubx.getfile()->is_open();
}
