#include"global.h"

int main(int argc, char *argv[]){
  FILE *ubx_file;
  int length=0;
  ubx_message ubx_msg;
  double e_square, N, x, y, z;
  int  longitude, latitude, h;

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
    //printf("%.2x",ubx_msg.header[0]);
    if (ubx_msg.header[0]!=0xb5) continue;
    fread(&ubx_msg.header[1],sizeof(unsigned char),1,ubx_file);
    //printf("%.2x",ubx_msg.header[1]);
    fread(&ubx_msg.message_class,sizeof(unsigned char),4,ubx_file);
    if( ubx_msg.message_class != 0x01 && ubx_msg.message_id != 0x02) continue;
    length = (ubx_msg.message_length[1]<<8)|ubx_msg.message_length[0];
    fread(&ubx_msg.payload,sizeof(unsigned char),length,ubx_file);
    fread(&ubx_msg.checksum_A,sizeof(unsigned char),1,ubx_file);
    fread(&ubx_msg.checksum_B,sizeof(unsigned char),1,ubx_file);
    
    // Sortir la valeur du GPS millisecondtime of week
    //printf("\nGPS millisecond time of week: %lu", (unsigned long)(ubx_msg.payload[3]<<24)|(ubx_msg.payload[2]<<16)|(ubx_msg.payload[1]<<8)|ubx_msg.payload[0]);
    longitude = (signed long)(ubx_msg.payload[7]<<24)|(ubx_msg.payload[6]<<16)|(ubx_msg.payload[5]<<8)|ubx_msg.payload[4];
    //printf("\nLongitude: %li", (signed long)longitude);
    latitude = (signed long)(ubx_msg.payload[11]<<24)|(ubx_msg.payload[10]<<16)|(ubx_msg.payload[9]<<8)|ubx_msg.payload[8];
    //printf("\nLatitude: %li", (signed long)latitude);
    h = (signed long)(ubx_msg.payload[15]<<24)|(ubx_msg.payload[14]<<16)|(ubx_msg.payload[13]<<8)|ubx_msg.payload[12];
    //printf("\nHeight above elipsoid: %li", (signed long)h);
    //printf("\nHeight above mean sea level: %li",(signed long)(ubx_msg.payload[19]<<24)|(ubx_msg.payload[18]<<16)|(ubx_msg.payload[17]<<8)|ubx_msg.payload[16]);
    //printf("\nHorizontal Accuracy Estimate: %lu",(unsigned long)(ubx_msg.payload[23]<<24)|(ubx_msg.payload[22]<<16)|(ubx_msg.payload[21]<<8)|ubx_msg.payload[20]);
    //printf("\nVertical Accuracy Estimate: %lu\n", (unsigned long)(ubx_msg.payload[27]<<24)|(ubx_msg.payload[26]<<16)|(ubx_msg.payload[25]<<8)|ubx_msg.payload[24]);

    // Convertir en coordonnées cartésiennes:
    e_square = (double)(2.0*f_WGS84-f_WGS84*f_WGS84);
    //printf("\ne2 = %f\n", e_square);
    //printf("\nlatitude double = %f\n", (double)latitude);
    N = (double)(a_WGS84/sqrt(1.0 - e_square * sin(PI*(double)latitude*1e-7/180.0)));
    
    x = (N + (double)h*1e-3)*cos(PI*(double)longitude*1e-7/180.0)*cos(PI*(double)latitude*1e-7/180.0);
    y = (N + (double)h*1e-3)*sin(PI*(double)longitude*1e-7/180.0)*cos(PI*(double)latitude*1e-7/180.0);
    z = (N * (1-e_square) + (double)h*1e-3)*sin(PI*(double)latitude*1e-7/180.0);
    printf("%f %f %f\n",x,y,z);
    break;
  }
  return 0;
}
