#include <XBee.h>
#include <LiquidCrystal.h>

XBee xbee = XBee();
Rx64Response rx = Rx64Response() ;
Tx64Request tx;
XBeeAddress64 addr;
uint8_t sdata[30] ;
uint8_t* rdata;

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

void setup() {

	delay(100);
	Serial.begin(38400);
	xbee.setSerial(Serial);
	delay(100);
	lcd.begin(16, 2);
	lcd.setCursor(0,0);


}
