#include"global.h"
#include<iostream>
#include<fstream>
#include <iomanip>
int main(){
  std::cout<<"starting program\n";
  std::basic_ifstream<unsigned char> inputStream("16040407.ubx", std::fstream::binary);
  if(!inputStream.is_open()) std::cout<<"Problem occured when trying to open the file\n";
  else{
    int length=0;
    char c;
    ubx_message ubx_msg;
    std::cout<<"Avant d'entrer dans la boucle principale\n";
    //std::cout<<inputStream.get(ubx_msg.header[0])<<"\n";
    while(!inputStream.get(ubx_msg.header[0])){
        //if(inputStream.read(&ubx_msg.header[0], 1)) return 0;
        //inputStream.get(ubx_msg.header);
        printf("%X", ubx_msg.header[0]);
        if(ubx_msg.header[0]!=0xb5) continue;
        std::cout<<"a new message header";
        inputStream.read( ubx_msg.header+1, 5);
        if(ubx_msg.header[1]!=0x62 || (ubx_msg.message_length[1]<<8)|ubx_msg.message_length[0] > 2000)
            continue;
        inputStream.read(ubx_msg.payload, (ubx_msg.message_length[1]<<8)|ubx_msg.message_length[0]);
        break;
    }
  }
}
/*

  while (1) {
  do {
    if !(read(&ubxm.header[0],1) return 0;
  }while ubxm.header[0]!= 0xB5;
  read(&ubxm.header[1],5)   read(ubxm.header+1,5)
  if (ubxm.header[1] != 0x62) or length > 2000 )
	continue;
  read(&ubxm.payload,length);
  read(&ubxm.checksum_A,2);
  if (check != chek_calc)
   continue;
  return 1;
}



typedef struct{
    unsigned char header[2];
    unsigned char message_class;
    unsigned char message_id;
    unsigned char message_length[2];
    unsigned char payload[1000]; // payload et checksum
}ubx_message, *pubx_message;
*/
