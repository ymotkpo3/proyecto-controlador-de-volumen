#include <Arduino.h>
#include <RotaryEncoder.h>

/*
Serial commands sent to the host application:

click   -> short button press detected
master  -> long button press detected
update  -> request application list refresh
appUP   -> select previous application
appDWN  -> select next application
volUP   -> increase selected volume
volDWN  -> decrease selected volume
*/

// Encoder operating modes.
// MODE_SELECT: rotate to browse applications.
// MODE_VOLUME: rotate to adjust volume.
constexpr int MODE_SELECT = 0;
constexpr int MODE_VOLUME = 1;

// Current operating mode.
static int mode = MODE_VOLUME;

constexpr int SW = 0;

// Rotary encoder used to navigate applications
// and adjust volume.
RotaryEncoder encoder(
    7,
    6,
    RotaryEncoder::LatchMode::TWO03
);

/**
 * Initializes serial communication and input pins.
 */
void setup() {
  Serial.begin(115200);
  pinMode(SW, INPUT_PULLUP);
}

// Button state tracking for click and long-press detection.
bool buttonPressed = false;
bool longPressSent = false;
unsigned long pressStart = 0;

/**
 * Main firmware loop.
 *
 * Handles:
 * - rotary encoder movement,
 * - button click detection,
 * - button long-press detection,
 * - serial communication with the host application.
 */

void loop() {

  encoder.tick();

  bool currentState = digitalRead(SW) == LOW;
  
  if (currentState && !buttonPressed) {

    // Button press debounce.
    
    delay(30);

    if (digitalRead(SW) != LOW)
        return;


    buttonPressed = true;
    longPressSent = false;
    pressStart = millis();
  }

  // Generate a long-press event after 700 ms.

  if (currentState && !longPressSent && millis() - pressStart >= 700) {

    Serial.println("master");
    mode = MODE_VOLUME;

    longPressSent = true;
  }


  if (!currentState && buttonPressed) {

    // Button press debounce.
    
    delay(30);

    if (digitalRead(SW) == LOW)
        return;
    


    buttonPressed = false;

    // Short click detected.

    if (!longPressSent) {
      Serial.println("click");
      if(mode == MODE_VOLUME){
        Serial.println("update");
        mode = MODE_SELECT;
      } else if (mode == MODE_SELECT){
        mode = MODE_VOLUME;
        Serial.println("vol");
      }
    }
  }

  // Previous encoder position used to detect rotation direction.

  static int pos = 0;

  // Current encoder position.

  int newPos = encoder.getPosition();

  if (pos < newPos && mode == MODE_VOLUME) {
    Serial.println("volDWN");
    pos = newPos;
  } else if (pos > newPos && mode == MODE_VOLUME){
    Serial.println("volUP");
    pos = newPos;
  } else if (pos < newPos && mode == MODE_SELECT){
    Serial.println("appDWN");
    pos = newPos;
  } else if (pos > newPos && mode == MODE_SELECT){
    Serial.println("appUP");
    pos = newPos;
  }
}