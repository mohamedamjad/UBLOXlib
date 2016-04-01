#include"global.h"
#include<iostream>
#include<fstream>

int main(){
  std::cout<<"starting program\n";
  std::ifstream inputStream("file");
  if(!stream.is_open()) std::cout<<"Problem occured when trying to open the file\n";
  else{
    int length=0;
    char c;
    ubx_message ubx_msg;
    while(1){
        if(!inputStream.get(&msg_ubx.header[0])) return 0;
        if(msg_ubx.header[0]!=0xB5) continue;
        inputStream.read( ubx_msg.header+1, 5);
        if(ubx_msg.header[1]!=0x62 || (ubx_msg.length[1]<<8)|ubx_msg.length[0] > 2000)
            continue;
        
    }
  }
}
*

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

