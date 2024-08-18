#include <usbhid.h>
#include <Mouse.h>
#include <hiduniversal.h>
#include <SPI.h>
#include "hidmouserptparser.h"
#include <Keyboard.h>

USB Usb;
HIDUniversal Hid(&Usb);
HIDMouseEvents MouEvents;
HIDMouseReportParser Mou(&MouEvents);

static const int8_t ZERO = 127;
static const int8_t MIN_VALUE = -127;
static const int8_t MAX_VALUE = 127;

signed char delta[3] = {0, 0, 0};

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  Usb.Init();
  Hid.SetReportParser(0, &Mou);
  Mouse.begin();
}

void loop() {
  delta[0] = 0;
  delta[1] = 0;
  delta[2] = 0;

  Usb.Task();
  handleSerialCommands();
  mouse_task();
}

void handleSerialCommands() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    switch (command) {
      case 'M': // Di chuyển chuột
        handleMoveCommand();
        break;
      case 'C': // Click chuột
        Mouse.click();
        break;
      // Thêm các lệnh khác tại đây nếu cần
    }
  }
}

void handleMoveCommand() {
  int8_t moves[2];
  if (Serial.available() >= 2) {
    moves[0] = Serial.read();
    moves[1] = Serial.read();
    Mouse.move(moves[0], moves[1], 0);
  }
}

void mouse_task() {
  uint8_t recv[2];
  if (polling_data(recv)) {
    int8_t moves[2];
    if (parse_data(&moves[0], &moves[1], &recv[0], &recv[1])) {
      Mouse.move(moves[0], moves[1], 0);
    }		
  }
  
  if (polling_inverso(recv)) {
    int8_t moves[2];
    if (parse_data(&moves[0], &moves[1], &recv[0], &recv[1])) {
      Mouse.move(-moves[0], -moves[1], 0);
    }		
  }  
  
  if (polling_shttt(recv)) {
     Mouse.click(); 
  }
}

bool polling_data(uint8_t *data) {
  if (Serial.available() >= 4) {
    byte bytes[4];
    for (byte i = 0; i < 4; i++) {
      bytes[i] = Serial.read();
    }
    if ( (bytes[0] == 0x7E) && (bytes[3] == 0x7E)) {
      data[0] = bytes[1];
      data[1] = bytes[2];
      return true;
    }
  }
  return false;
}

bool polling_shttt(uint8_t *data) {
  if (Serial.available() >= 4) {
    byte bytes[4];
    for (byte i = 0; i < 4; i++) {
      bytes[i] = Serial.read();
    }
    if ( (bytes[0] == 0x5E) && (bytes[3] == 0x5E)) {
      return true;
    }
  }
  return false;
}

bool polling_inverso(uint8_t *data) {
  if (Serial.available() >= 4) {
    byte bytes[4];
    for (byte i = 0; i < 4; i++) {
      bytes[i] = Serial.read();
    }
    if ( (bytes[0] == 0x7B) && (bytes[3] == 0x7B)) {
      return true;
    }
  }
  return false;
}

bool parse_data(int8_t *mouse_x, int8_t *mouse_y, uint8_t *read_x, uint8_t *read_y) {
  if ( (*mouse_x != ZERO) || (*mouse_y != ZERO) ) {
    *mouse_x = *read_x - ZERO;
    *mouse_y = *read_y - ZERO;
    data_correction(mouse_x, mouse_y);
    return true;
  }
  return false;
}

void data_correction(int8_t *mouse_x, int8_t *mouse_y) {
  if (*mouse_x <= MIN_VALUE) {  
    *mouse_x = MIN_VALUE;
  }
  if (*mouse_x >= MAX_VALUE) {
    *mouse_x = MAX_VALUE;
  }
  if (*mouse_y <= MIN_VALUE) {
    *mouse_y = MIN_VALUE;
  }
  if (*mouse_y >= MAX_VALUE) {
    *mouse_y = MAX_VALUE;
  }
}