#include<stdlib.h>
#include <stdio.h>


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
    unsigned char payload[100]; // taille maxi
    unsigned char checksum_A;
    unsigned char checksum_B;
}ubx_message, *pubx_message;

// functions
unsigned char getChar();
