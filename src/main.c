#include"global.h"

int main(){
  FILE *ubx_file;
  int length=0;
  ubx_message ubx_msg;

  ubx_file = fopen("16040407.ubx", "rb");
  
  if(!ubx_file){
    printf("Probleme occured when I tried to open the UBLOX file\n");
    return 1;
  }
  /*fread(&ubx_msg.header[0],sizeof(unsigned char),1,ubx_file);
  printf("%2x",ubx_msg.header[0]);
  fread(&ubx_msg.header[1],sizeof(unsigned char),1,ubx_file);
  printf("%2x",ubx_msg.header[1]);*/
  while(1){
    fread(&ubx_msg.header[0],sizeof(unsigned char),1,ubx_file);
    printf("%.2x",ubx_msg.header[0]);
    if (ubx_msg.header[0]!=0xb5) continue;
    fread(&ubx_msg.header[1],sizeof(unsigned char),1,ubx_file);
    printf("%.2x",ubx_msg.header[1]);
    fread(&ubx_msg.message_class,sizeof(unsigned char),4,ubx_file);
    printf("%.2x",ubx_msg.message_class);
    printf("%.2x",ubx_msg.message_id);
    printf("%.2x",ubx_msg.message_length[0]);
    printf("%.2x",ubx_msg.message_length[1]);
    length = (ubx_msg.message_length[0]<<8)|ubx_msg.message_length[1];
    printf("LENGTH: %i", length);
    break;
  }
  return 0;

;}
