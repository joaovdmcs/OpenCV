// C++ code
//

//Link do projeto no tinkercad: https://www.tinkercad.com/things/0Vfoc4IxsZ0-missao-arduino
//Link do repositorio: https://github.com/joaovdmcs/IEEE1


//O Programa utiliza de entradas e saídas via serial para realizar suas operações e demonstrar o estado atual do LED.
// Os periodos  do LED NÃO mudam de forma ciclica (ie. se o periodo acabar acima de 1000ms, voltar para 250ms).
int currState = 1000;
int comando = 0;

#define PIN_LED 9
#define LIGHT_BRIGHT_ON 255
#define LIGHT_BRIGHT_OFF 0

void setup(){
  Serial.begin(115200);
  Serial.println("Digite + ou - para alterar o periodo do LED");
  Serial.println("Periodo atual: 1000ms");
  
}

void loop(){
  
	if(Serial.available()>0){
		comando = Serial.read();
    	if(comando == '+') currState = currState + 375;
      	else if (comando == '-') currState = currState - 375;
        
        if(currState > 1000) currState = 1000;
        else if (currState < 250) currState = 250;
        Serial.print("Periodo atual: ");
        Serial.print(currState);  
      	Serial.println("ms");
    }
	
  	analogWrite(PIN_LED, LIGHT_BRIGHT_ON);
  	delay(currState);
  	analogWrite(PIN_LED,LIGHT_BRIGHT_OFF);
  	delay(currState);
	
}

