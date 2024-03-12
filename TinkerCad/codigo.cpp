// C++ code
//

//Link do projeto no tinkercad: https://www.tinkercad.com/things/0Vfoc4IxsZ0-missao-arduino

#define PIN_LED 9
#define LIGHT_BRIGHT_ON 255
#define LIGHT_BRIGHT_OFF 0

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
  lightStateIntensity(PIN_LED,LIGHT_BRIGHT_ON);
  delay(500); // Periodo de 0.5 segundos
  lightStateIntensity(PIN_LED,LIGHT_BRIGHT_OFF);
  delay(500); 
}

void lightStateIntensity(uint8_t pin, uint8_t intensity){
  analogWrite(pin,intensity);
}
