#include <OneWire.h>
#include <DallasTemperature.h>
#include <EEPROM.h>
#include <GravityTDS.h>


// set up oneWire for temperature
OneWire oneWire(13);
DallasTemperature tempSensor(&oneWire);

// set up TDS
GravityTDS tds;


// setup code
void setup() {
  // initialize serial
  Serial.begin(9600);

  // initialize temperature sensor
  tempSensor.begin();

  // initialize turbidity sensor
  tds.setPin(A2);
  tds.setAref(5.0);
  tds.setAdcRange(1024);
  tds.begin();

  // configure temperature power pin
  pinMode(12, OUTPUT);
}


// method to get pH
float getpH() {
  // get 10 analog readings
  int buf[10];
  for(int i = 0; i < 10; i++) {
    buf[i] = analogRead(A0); 
    delay(10);
  }

  // sort analog readings least to greatest
  for(int i = 0; i < 9; i++) {
    for(int j = i + 1; j < 10; j++) {
      if(buf[i] > buf[j]) {
        int temp = buf[i];
        buf[i] = buf[j];
        buf[j] = temp;
      }
    }
  }


  // find average analog reading
  float avgValue = 0;
  for(int i = 2; i < 8; i++) {
    avgValue += buf[i];
  }

  float millivolts = avgValue * 5.0 / 1024 / 6;

  float offset = 0;
  float pH = 3.5 * millivolts + offset;
  return pH;
}


// method to get total dissolved solids
float getTDS() {
  tds.setTemperature(getTemperature());
  tds.update();
  return tds.getTdsValue();
}


// method to get turbidity reading
int getTurbidity() {
  // get analog reading
  int sensorValue = analogRead(A1);

  // convert analog value to voltage
  float voltage = sensorValue * (5.0 / 1024.0);

  int turbidity = (int) (-1120.4 * square(voltage) + 5742.3 * voltage - 4353.8);

  return turbidity;
}


// method to get temperature reading
float getTemperature() {
  digitalWrite(12, HIGH);

  // command to get temperatures
  tempSensor.requestTemperatures();

  // read temperature in Celsius
  float tempCelsius = tempSensor.getTempCByIndex(0);

  // convert Celsius to Fahrenheit
  float tempFahrenheit = tempCelsius * 9 / 5 + 32;
  
  digitalWrite(12, LOW);

  return tempFahrenheit;
}


// main code
void loop() {
  Serial.println(
    String(getpH()) + ", " +
    String(getTDS()) + ", " +
    String(getTurbidity()) + ", " +
    String(getTemperature())
  );

  delay(500);
}



