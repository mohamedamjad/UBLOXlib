/* ------------------------------------------------------------------------*/
//                                 includes                                //
/*-------------------------------------------------------------------------*/
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <unistd.h>
#include <string.h>
// Constantes geodesiques
#define a_WGS84 (6378137.00)
#define b_WGS84 (6356752.30)
#define f_WGS84 (1.0/298.257223563)
#define PI (3.141592653589793)

// Message class
#define RXM 0x02
#define NAV 0x01

// Message ID
#define RAW 0x10
#define TIMEUTC 0x21
#define POSLLH 0x02

#define MAX_PAYLOAD_SIZE 1000

/* ------------------------------------------------------------------------*/
//                                structures                               //
/*-------------------------------------------------------------------------*/
// UBX message
typedef struct{
    unsigned char header[2];
    unsigned char message_class;
    unsigned char message_id;
    unsigned char message_length[2];
    unsigned char payload[MAX_PAYLOAD_SIZE]; // taille maxi
    unsigned char checksum_A;
    unsigned char checksum_B;
}ubx_message, *pubx_message;

/* ------------------------------------------------------------------------*/
//                                functions                                //
/*-------------------------------------------------------------------------*/


