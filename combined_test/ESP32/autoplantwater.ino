unsigned long ledTimer = 0;
unsigned long overrideBlink = 0;
bool overrideLedState = false;
bool ledState = false;
bool ledcd = false;
bool manualOverride = false;

//määritetään pinnit
const int waterPin = 5; 
const int pumpPin = 21; 
const int tankLed = 4; 
const int moistPin = 2;
const int testPin = 39;

//asetetaan pinneille arvot, joiden alittaessa toiminta muuttuu.
const int moistLimit = 500;
const int waterLevel = 500;

void setup(){
//115200Baudrate ESP32:lle
    Serial.begin(115200);
//12 bitin resoluutio
    analogReadResolution(12);

// asetetaan pinnit output muotoon
    pinMode(pumpPin, OUTPUT);
    pinMode(tankLed, OUTPUT);
    pinMode(testPin, OUTPUT);
// asetetaan pinnit pois päältä uudelleen käynnistyessä.
    digitalWrite(pumpPin, LOW);
    digitalWrite(tankLed, LOW);
    digitalWrite(testPin, LOW);

    Serial.setTimeout(50);

}

void loop(){
    int waterValue = analogRead(waterPin);
    int moistValue = analogRead(moistPin);

    bool tankIsFull = waterValue > waterLevel;
    

    unsigned long stopwatch = millis();
    //manuaalimoodin määritys
    if (manualOverride){
        if(millis()-overrideBlink >= 500){
            overrideBlink = millis();
            overrideLedState = !overrideLedState;
            digitalWrite(tankLed, overrideLedState ? HIGH : LOW);
        }
    } else {
            digitalWrite(tankLed, tankIsFull ? LOW : HIGH);
    }
    if(!manualOverride){
        if(ledState && stopwatch - ledTimer >= 3000){
            digitalWrite(pumpPin, LOW);
            digitalWrite(testPin, LOW);
            ledState = false;
            ledcd = true;
            ledTimer = stopwatch; // aloittaa ajastimen
            Serial.println("AUTO PUMP OFF");
        }
        // ajastimen tarkoitus on lopettaa pumpun toiminta 
        //ettei pumppu vahingossa ylikastele kasvia
        if(ledcd && stopwatch - ledTimer >= 6000){
            ledcd = false;
            Serial.println("Cooldown complete");  
        }

        if (tankIsFull && !ledState && !ledcd && moistValue < moistLimit) {
            digitalWrite(pumpPin, HIGH);
            digitalWrite(testPin, HIGH);
            ledState = true;
            ledTimer = stopwatch;
            Serial.println("AUTO PUMP ON");
        }
        Serial.printf("Moist ADC = %d | Tank level ADC = %d | Tank is %s\n", moistValue, waterValue, tankIsFull ? "FULL" : "EMPTY");
    }
    //manuaalisen moodin koodit
    if (Serial.available()){
        String command = Serial.readStringUntil('\n');
        command.trim();

        if (command.equalsIgnoreCase("on")){
            Serial.println("Manual override: PUMP FORCED ON");
            digitalWrite(pumpPin, HIGH);
            digitalWrite(testPin, HIGH);
            ledState = true;
            ledcd = false;
        } else if (command.equalsIgnoreCase("off")){
            Serial.println("Manual override: PUMP LOCKED OFF");
            manualOverride = true;
            digitalWrite(pumpPin, LOW);
            digitalWrite(testPin, LOW);
            ledState = false;
            ledcd = false;
        }else if (command.equalsIgnoreCase("active")){
            Serial.println("Resuming automated action");
            manualOverride = false;
            ledState = false;
            ledcd = false;
            }
        }
    

    delay(500);

}
