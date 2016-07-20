/**
 * @author: Mohamed-Amjad LASRI
 */
#include"global.h"
#include"gnuplot_i.h"


/*-------------------------------------------------------------------------*/
//                            Display help                                 //
/*------------------------------------------------------------------------ */
void displayHelp(){
  printf("\nuBlox Lib Version 0.0.1\n\n");
  
  printf("Arguments :\n");
  printf("-h : display this help (optional)\n");
  printf("-i : set input file (mandatory)\n");
  printf("-m : parse a specific message (optional)");
  printf("-o : set output file (mandatory)\n");
  printf("-p : plot charts\n");
  printf("-r : generate a report after parsing the ubx file(optional)");
  printf("-v : get program version\n");
}


/*-------------------------------------------------------------------------*/
//                            main function                                //
/*------------------------------------------------------------------------ */
int main(int argc, char *argv[]){
  int opt;
  short unsigned int generate_report = 0;
  char *input_file_name, *output_file_name;

  while ((opt = getopt(argc, argv, "g:rvm:phi:o:")) != -1) {
    switch (opt) {
      case 'i':
        input_file_name = (char*)malloc(strlen(optarg));
        strncpy( input_file_name, optarg, strlen(optarg));
        printf("Input file: %s\n", input_file_name);
        break;
      case 'm':
        printf("Looking for a specific µbx message: YES");
        break;
      case 'o':
        output_file_name = (char*) malloc(strlen(optarg));
        strncpy( output_file_name, optarg, strlen(optarg));
        printf("Output file: %s\n", output_file_name);
        break;
      case 'h':
        displayHelp();
        break;
      case 'v':
        printf("µBlox Lib version 0.0.1\n");
        break;
      case 'r':
        printf("Generate detailed report: YES\n");
        generate_report = 1;
        break;
      case 'p':
        printf("Plot charts: YES\n");
        break;
      default:
        fprintf(stderr, "Usage: %s -i input_file -o output_file [-h]\n",
                argv[0]);
        displayHelp();
        exit(EXIT_FAILURE);
    }
  }



  FILE *ubx_file;
  FILE *output_file;
  int length=0;
  ubx_message ubx_msg;
  //double e_square, N, x, y, z;
  int longitude, latitude, height, hMSL, hAcc, vAcc, iToW_01_02,
      iToW_01_21, fToW, week, leapS, valid, tAcc;
  ubx_file = fopen(input_file_name, "rb");
  output_file = fopen( output_file_name, "wa");
  
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
    if( (ubx_msg.message_class != 0x01 || ubx_msg.message_id != 0x02) || (ubx_msg.message_class != 0x01 || ubx_msg.message_id != 0x21) ) continue;
    length = (ubx_msg.message_length[1]<<8)|ubx_msg.message_length[0];
    fread(&ubx_msg.payload,sizeof(unsigned char),length,ubx_file);
    fread(&ubx_msg.checksum_A,sizeof(unsigned char),1,ubx_file);
    fread(&ubx_msg.checksum_B,sizeof(unsigned char),1,ubx_file);

    /////////////////////////////////////////////////////////////////////////
    iToW_01_21 = (signed long)
    


    /////////////////////////////////////////////////////////////////////////


    /////////////////////////////////////////////////////////////////////////
    // Sortir la valeur du GPS millisecondtime of week
    iToW_01_02 = (signed long)((ubx_msg.payload[3]<<24)|(ubx_msg.payload[2]<<16)|(ubx_msg.payload[1]<<8)|ubx_msg.payload[0]);
    longitude = (signed long)((ubx_msg.payload[7]<<24)|(ubx_msg.payload[6]<<16)|(ubx_msg.payload[5]<<8)|ubx_msg.payload[4]);
    latitude = (signed long)((ubx_msg.payload[11]<<24)|(ubx_msg.payload[10]<<16)|(ubx_msg.payload[9]<<8)|ubx_msg.payload[8]);
    height = (signed long)((ubx_msg.payload[15]<<24)|(ubx_msg.payload[14]<<16)|(ubx_msg.payload[13]<<8)|ubx_msg.payload[12]);
    hMSL = (signed long)((ubx_msg.payload[19]<<24)|(ubx_msg.payload[18]<<16)|(ubx_msg.payload[17]<<8)|ubx_msg.payload[16]);
    hAcc = (signed long)((ubx_msg.payload[23]<<24)|(ubx_msg.payload[22]<<16)|(ubx_msg.payload[21]<<8)|ubx_msg.payload[20]);
    vAcc = (signed long)((ubx_msg.payload[27]<<24)|(ubx_msg.payload[26]<<16)|(ubx_msg.payload[25]<<8)|ubx_msg.payload[24]);

    // Convertir en coordonnées cartésiennes:
    //e_square = (double)(2.0*f_WGS84-f_WGS84*f_WGS84);
    //printf("\ne2 = %f\n", e_square);
    //printf("\nlatitude double = %f\n", (double)latitude);
    //N = (double)(a_WGS84/sqrt(1.0 - e_square * sin(PI*(double)latitude*1e-7/180.0)*sin(PI*(double)latitude*1e-7/180.0)));
    
    //x = (N + (double)h*1e-3)*cos(PI*(double)longitude*1e-7/180.0)*cos(PI*(double)latitude*1e-7/180.0);
    //y = (N + (double)h*1e-3)*sin(PI*(double)longitude*1e-7/180.0)*cos(PI*(double)latitude*1e-7/180.0);
    //z = (N * (double)(1.0-e_square) + (double)h*1e-3)*sin(PI*(double)latitude*1e-7/180.0);
    //printf("%de-7 %de-7 %d\n",longitude,latitude,h);
    //printf("%f %f %f %d %d\n",x,y,z,hAcc,vAcc);
    fprintf(output_file, "%d %d %d %d %d %d %d\n",iToW,longitude,latitude,height,hMSL,hAcc,vAcc);
    //////////////////////////////////////////////////////////////////////////

  }
  if(generate_report == 1){
    printf("PARSING REPORT:\n");
  }
  fclose(ubx_file);
  fclose(output_file);
  return 0;
}
