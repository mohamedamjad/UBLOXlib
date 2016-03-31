#include<stdlib.h>
#include"global.h"
#include<string>
#include<vector>
#include<fstream>

class UBLOX{
  private:
    std::ifstream file;
    std::vector<ubx_message> *ubxs;
  public:
    UBLOX(std::string);
    std::ifstream* getfile();
    void setfile(std::ifstream*);
    void insert(ubx_message);
    std::vector<ubx_message> *getMessages();
    std::vector<ubx_message> *getMessagesByID(unsigned char message_class, unsigned char message_ID);
    std::vector<ubx_message> *getMessagesByClass(unsigned char message_class, unsigned char message_ID);
    ~UBLOX();
};
