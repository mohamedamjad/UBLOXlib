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
  printf("-m : parse a specific message (optional)\n");
  printf("-o : set output file (mandatory)\n");
  printf("-p : plot charts\n");
  printf("-r : generate a report after parsing the ubx file(optional)\n");
  printf("-v : get program version\n");
}


/*-------------------------------------------------------------------------*/
//                            main function                                //
/*------------------------------------------------------------------------ */
int main(int argc, char *argv[]){
  int opt;
  short unsigned int generate_report = 0;
  short unsigned int generate_charts = 0;
  char *input_file_name, *output_file_name;

  while ((opt = getopt(argc, argv, "grvm:hi:o:")) != -1) {
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
      case 'g':
        printf("Plot charts: YES\n");
        generate_charts = 1;
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
      iToW_01_21, year, month, day, hour, min, sec, valid_01_21, tAcc, nano,
      iToW_02_10, week_number, numSV, reserved1, sv, mesQI, cno, lli,
      iToW_01_20, fToW, leap_seconds, validity_flag;
  double cpMes, prMes;
  float doMes;

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
    if( (ubx_msg.message_class != 0x01 || ubx_msg.message_id != 0x02) && (ubx_msg.message_class != 0x01 || ubx_msg.message_id != 0x21) && (ubx_msg.message_class != 0x02 || ubx_msg.message_id != 0x10) ) continue;
    length = (ubx_msg.message_length[1]<<8)|ubx_msg.message_length[0];
    fread(&ubx_msg.payload,sizeof(unsigned char),length,ubx_file);
    fread(&ubx_msg.checksum_A,sizeof(unsigned char),1,ubx_file);
    fread(&ubx_msg.checksum_B,sizeof(unsigned char),1,ubx_file);

    /////////////////////////////////////////////////////////////////////////
    //iToW_01_21 = (signed long)
    if((ubx_msg.message_class == 0x01 && ubx_msg.message_id == 0x21)){
        //printf("message de type 0x01 0x21\n");
        iToW_01_21 = (signed long)((ubx_msg.payload[3]<<24)|(ubx_msg.payload[2]<<16)|(ubx_msg.payload[1]<<8)|ubx_msg.payload[0]);
        tAcc = (signed long)((ubx_msg.payload[7]<<24)|(ubx_msg.payload[6]<<16)|(ubx_msg.payload[5]<<8)|ubx_msg.payload[4]);
        nano = (signed long)((ubx_msg.payload[11]<<24)|(ubx_msg.payload[10]<<16)|(ubx_msg.payload[9]<<8)|ubx_msg.payload[8]);
        year = ((ubx_msg.payload[13]<<8)|ubx_msg.payload[12]);
        month = ubx_msg.payload[14];
        day = ubx_msg.payload[15];
        hour = ubx_msg.payload[16];
        min = ubx_msg.payload[17];
        sec = ubx_msg.payload[18];
        valid_01_21 = ubx_msg.payload[19];
        fprintf(output_file, "NAV_TIMEUTC %d %d %d %d %d %d %d %d %d %d\n", iToW_01_21, tAcc, nano, year, month, day, hour, min, sec, valid_01_21);
    }
    /////////////////////////////////////////////////////////////////////////

    else if(ubx_msg.message_class == 0x01 && ubx_msg.message_id == 0x02){
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
	fprintf(output_file, "NAV_POSLLH %d %d %d %d %d %d %d\n",iToW_01_02,longitude,latitude,height,hMSL,hAcc,vAcc);
	//////////////////////////////////////////////////////////////////////////
    }
    else if (ubx_msg.message_class == 0x02 && ubx_msg.message_id == 0x10){
        iToW_02_10 = (signed long)((ubx_msg.payload[3]<<24)|(ubx_msg.payload[2]<<16)|(ubx_msg.payload[1]<<8)|ubx_msg.payload[0]);
        week_number = ((ubx_msg.payload[5]<<8)|ubx_msg.payload[4]);
        numSV = ubx_msg.payload[6];
        reserved1 = ubx_msg.payload[7];
        fprintf(output_file, "RXM_RAW %d %d %d %d\n", iToW_02_10, week_number, numSV, reserved1);
        for(int j = 0; j<numSV; j++){
            //cpMes = ((ubx_msg.payload[15+j*24]<<56)|(ubx_msg.payload[14+j*24]<<48)|(ubx_msg.payload[13+j*24]<<40)|(ubx_msg.payload[12+j*24]<<32)|(ubx_msg.payload[11+j*24]<<24)|(ubx_msg.payload[10+j*24]<<16)|(ubx_msg.payload[9+j*24]<<8)|ubx_msg.payload[8+j*24]);
            memcpy( &cpMes, ubx_msg.payload+8+j*24, sizeof(double));
            memcpy( &prMes, ubx_msg.payload+16+j*24, sizeof(double));
            memcpy(&doMes, ubx_msg.payload+24+j*24, sizeof(float));
            sv = ubx_msg.payload[28+j*24];
            mesQI = ubx_msg.payload[29+j*24];
            cno = ubx_msg.payload[30+j*24];
            lli = ubx_msg.payload[31+j*24];
            fprintf(output_file," %.3f %.3f %.3f %d %d %d %d\n", cpMes, prMes, doMes, sv, mesQI, cno, lli);
        }

    }
    /////////////////////////////////////////////////////////////////////////////
    else if (ubx_msg.message_class == 0x01 && ubx_msg.message_id == 0x20){
        iToW_01_20    = (signed long)((ubx_msg.payload[3]<<24)|(ubx_msg.payload[2]<<16)|(ubx_msg.payload[1]<<8)|ubx_msg.payload[0]);
        fToW          = (signed long)((ubx_msg.payload[7]<<24)|(ubx_msg.payload[6]<<16)|(ubx_msg.payload[5]<<8)|ubx_msg.payload[4]);
        week_number   = ((ubx_msg.payload[9]<<8)|ubx_msg.payload[8]);
        leap_seconds  = ubx_msg.payload[10];
        validity_flag = ubx_msg.payload[11];
        tAcc          = (signed long)((ubx_msg.payload[15]<<24)|(ubx_msg.payload[14]<<16)|(ubx_msg.payload[13]<<8)|ubx_msg.payload[12]);
        fprintf(output_file, "NAV_TIMEGPS %d %d %d %d %d %d", iToW_01_20, fToW, week_number, leap_seconds, validity_flag, tAcc);
    }
  }
  if(generate_report == 1){
    printf("ANALYSIS REPORT:\n");
  }
  if(generate_charts == 1){
    gnuplot_ctrl * ptr_plot;
    ptr_plot = gnuplot_init();
    
    gnuplot_setstyle(ptr_plot, "lines");
    gnuplot_set_xlabel(ptr_plot, "epochs");
    gnuplot_set_ylabel(ptr_plot, "clock accuracy estimation in ns");
        gnuplot_cmd(ptr_plot, "plot sin(x)");

    gnuplot_cmd(ptr_plot, "set term png");
    gnuplot_cmd(ptr_plot, "set output \"out.png\"");
    gnuplot_cmd(ptr_plot, "replot");
    gnuplot_cmd(ptr_plot, "set term x11");
    gnuplot_cmd(ptr_plot, "plot sin(x)");
    
    gnuplot_close(ptr_plot);
  }
  fclose(ubx_file);
  fclose(output_file);
  return 0;
}
