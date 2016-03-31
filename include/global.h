// Message class
#define RXM 0x02
#define NAV 0x01

// Message ID
#define RAW 0x10
#define TIMEUTC 0x21
#define POSLLH 0x02

// new types
typedef struct{
    unsigned char header[2];
    unsigned char message_class;
    unsigned char message_id;
    unsigned char message_length[2];
    unsigned char *payload;
    unsigned char checksum[2];
}ubx_message, *pubx_message;
