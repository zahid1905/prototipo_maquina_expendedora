/*
 * Typical pin layout used:
 * -----------------------------------------------------------------------------------------
 *             MFRC522      Arduino       Arduino   Arduino    Arduino          Arduino
 *             Reader/PCD   Uno/101       Mega      Nano v3    Leonardo/Micro   Pro Micro
 * Signal      Pin          Pin           Pin       Pin        Pin              Pin
 * -----------------------------------------------------------------------------------------
 * SPI SS      SDA(SS)      10            53        D10        10               10
 * SPI MOSI    MOSI         11 / ICSP-4   51        D11        ICSP-4           16
 * SPI MISO    MISO         12 / ICSP-1   50        D12        ICSP-1           14
 * SPI SCK     SCK          13 / ICSP-3   52        D13        ICSP-3           15
 * RST         RST          x  / ICSP-3   4         x          x                x
 */

#include <MFRC522v2.h>
#include <MFRC522DriverSPI.h>
#include <MFRC522DriverPinSimple.h>
#include <MFRC522Debug.h>

MFRC522DriverPinSimple ss_pin(53); // Configurable, see typical pin layout above.

MFRC522DriverSPI driver{ss_pin}; // Create SPI driver.
MFRC522 mfrc522{driver};  // Create MFRC522 instance.

int pin_interrupcion = 5; 

void setup() {
  Serial.begin(115200);  // Initialize serial communications with the PC for debugging.
  while (!Serial);     // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4).
  mfrc522.PCD_Init();  // Init MFRC522 board.
  pinMode(pin_interrupcion, OUTPUT);
  digitalWrite(pin_interrupcion, LOW);
}

void loop() {
	// Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
	if ( !mfrc522.PICC_IsNewCardPresent()) {
    delay(1000);
		return;
	}
  Serial.println("Card Detected");
  digitalWrite(pin_interrupcion, HIGH);
  delay(10);
  digitalWrite(pin_interrupcion, LOW);
}
