#include"global.h"

int main(int argc, char *argv[]){
  
  FILE *ubx_file;
  int length=0;
  ubx_message ubx_msg;
  double e_square, N, x, y, z;
  int longitude, latitude, h, hAcc, vAcc;

  ubx_file = fopen(argv[1], "rb");
  
  if(!ubx_file){
    printf("Probleme occured when I tried to open the UBLOX file\n");
    return 1;
  }
  while(fread(&ubx_msg.header[0],sizeof(unsigned char),1,ubx_file)){
    //fread(&ubx_msg.header[0],sizeof(unsigned char),1,ubx_file);
    if (ubx_msg.header[0]!=0xb5) continue;
    fread(&ubx_msg.header[1],sizeof(unsigned char),1,ubx_file);
    if (ubx_msg.header[1]!=0x62) continue;
    fread(&ubx_msg.message_class,sizeof(unsigned char),4,ubx_file);
    if( ubx_msg.message_class != 0x01 || ubx_msg.message_id != 0x02) continue;
    length = (ubx_msg.message_length[1]<<8)|ubx_msg.message_length[0];
    fread(&ubx_msg.payload,sizeof(unsigned char),length,ubx_file);
    fread(&ubx_msg.checksum_A,sizeof(unsigned char),1,ubx_file);
    fread(&ubx_msg.checksum_B,sizeof(unsigned char),1,ubx_file);
    
    // Sortir la valeur du GPS millisecondtime of week
    longitude = (signed long)((ubx_msg.payload[7]<<24)|(ubx_msg.payload[6]<<16)|(ubx_msg.payload[5]<<8)|ubx_msg.payload[4]);
    latitude = (signed long)((ubx_msg.payload[11]<<24)|(ubx_msg.payload[10]<<16)|(ubx_msg.payload[9]<<8)|ubx_msg.payload[8]);
    h = (signed long)((ubx_msg.payload[15]<<24)|(ubx_msg.payload[14]<<16)|(ubx_msg.payload[13]<<8)|ubx_msg.payload[12]);
    hAcc = (signed long)((ubx_msg.payload[23]<<24)|(ubx_msg.payload[22]<<16)|(ubx_msg.payload[21]<<8)|ubx_msg.payload[20]);
    vAcc = (signed long)((ubx_msg.payload[27]<<24)|(ubx_msg.payload[26]<<16)|(ubx_msg.payload[25]<<8)|ubx_msg.payload[24]);

    // Convertir en coordonnées cartésiennes:
    e_square = (double)(2.0*f_WGS84-f_WGS84*f_WGS84);
    //printf("\ne2 = %f\n", e_square);
    //printf("\nlatitude double = %f\n", (double)latitude);
    N = (double)(a_WGS84/sqrt(1.0 - e_square * sin(PI*(double)latitude*1e-7/180.0)*sin(PI*(double)latitude*1e-7/180.0)));
    
    x = (N + (double)h*1e-3)*cos(PI*(double)longitude*1e-7/180.0)*cos(PI*(double)latitude*1e-7/180.0);
    y = (N + (double)h*1e-3)*sin(PI*(double)longitude*1e-7/180.0)*cos(PI*(double)latitude*1e-7/180.0);
    z = (N * (double)(1.0-e_square) + (double)h*1e-3)*sin(PI*(double)latitude*1e-7/180.0);
    //printf("%de-7 %de-7 %d\n",longitude,latitude,h);
    printf("%f %f %f %d %d\n",x,y,z,hAcc,vAcc);
    
  }
  fclose(ubx_file);
  return 0;
}
