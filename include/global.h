#include <stdlib.h>
#include <stdio.h>
#include <math.h>
// Constantes geodesiques
#define a_WGS84 (6377397.00)
#define b_WGS84 (6356752.30)
#define f_WGS84 (0.00335281066)
#define PI (3.141592653589793)

// Message class
#define RXM 0x02
#define NAV 0x01

// Message ID
#define RAW 0x10
#define TIMEUTC 0x21
#define POSLLH 0x02

// State machine
#define MSG_SYNC 0x01
#define MSG_HEADER 0x02
#define MSG_DATA 0x03
#define MSG_CHECK_1 0x04
#define MSG_CHECK_2 0x05

// new types
typedef struct{
    unsigned char header[2];
    unsigned char message_class;
    unsigned char message_id;
    unsigned char message_length[2];
    unsigned char payload[7000]; // taille maxi
    unsigned char checksum_A;
    unsigned char checksum_B;
}ubx_message, *pubx_message;

// functions
unsigned char getChar();
