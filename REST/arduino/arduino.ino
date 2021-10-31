

#include <EEPROM.h>
#include <Wire.h> 

//////////////////////////////////////////////////////////

#define PWM_0 5  //D5
#define PWM_1 6  //D6
#define PWM_2 9  //D8
#define PWM_3 10 //D9

#define voltage_0 A0 
#define voltage_1 A1 
#define voltage_2 A2 
#define voltage_3 A3  

struct group{
   int target_voltage;
   int duty;
};

group group_0 = {0,0};
group group_1 = {0,0};
group group_2 = {0,0};
group group_3 = {0,0};

int ref_0 = 0;
int ref_1 = 0;
int ref_2 = 0;
int ref_3 = 0;

int message_timer = 0;


int msg;
int c[9] = {0};
bool on = false;
bool firstrun = true;
//////////////////////////////////////////////////////////

void setup() {

  // Give arduino an adress
  Wire.begin(0x8);  
  // register event 
  Wire.onReceive(receiveEvent); 
  Wire.onRequest(requestEvent);

  while (!Serial) { delay(10); }
  
  Serial.begin(9600);
}

void loop() {
  Serial.println("On?");
  Serial.println(on);

  if (on && ((millis() - message_timer) <= 120000)) {
    Serial.println("on");
    firstrun = true;
    runPWM();
  }
  else {
    if (firstrun) {
      Serial.println("off");
      powerOff();
      firstrun = false;
    }
    delay(1000);
  }
  

}

void runPWM() {
  delay(1000);

  Serial.println(group_0.target_voltage);
  Serial.println(group_1.target_voltage);
  Serial.println(group_2.target_voltage);
  Serial.println(group_3.target_voltage);
  Serial.println("");


  
  powerOff();

  group_0.duty = dutyUpdate(ref_0, group_0);
  group_1.duty = dutyUpdate(ref_1, group_1);
  group_2.duty = dutyUpdate(ref_2, group_2);
  group_3.duty = dutyUpdate(ref_3, group_3);

  setDuty();

}


void receiveEvent(int howMany){
  
  //while(Wire.available()){
    int code = Wire.read();
    if (code==204) {
      on = false;
    }
    else if (code==1) {
      //Do nothing
      
    }
    else {
      
      on = true;
      for (int msg = 1; msg<9;msg++){
        c[msg] = Wire.read();
      }
      Serial.println("new taregt value");
      newTargetVoltages();
      }
    
  //}
}

 
// Turn power off for reading off-potential
void powerOff(){
  
  analogWrite(PWM_0,0);
  analogWrite(PWM_1,0);
  analogWrite(PWM_2,0);
  analogWrite(PWM_3,0);
  
  ref_0 = analogRead(voltage_0);
  ref_1 = analogRead(voltage_1);
  ref_2 = analogRead(voltage_2);
  ref_3 = analogRead(voltage_3);
  
}

int dutyUpdate(int ref, group activeGroup){

  int newDuty = 0;
  
  if (ref > activeGroup.target_voltage){
    newDuty = activeGroup.duty + 1;
    
  } else if (ref < activeGroup.target_voltage ){
    newDuty = activeGroup.duty - 1;
    
  }

  if (newDuty > 255){
    newDuty = 255;
  } else if (newDuty < 0){
    newDuty = 0;
  }
  
  return newDuty;
}

void setDuty(){
  analogWrite(PWM_0,group_0.duty);
  analogWrite(PWM_1,group_1.duty);
  analogWrite(PWM_2,group_2.duty);
  analogWrite(PWM_3,group_3.duty);
}

void newTargetVoltages(){

  Serial.println("Setting new values");
  Serial.println(c[1]);
  Serial.println(c[2]);

  group_0.target_voltage = byteDecoder(c[1],c[2]);
  group_1.target_voltage = byteDecoder(c[3],c[4]);
  group_2.target_voltage = byteDecoder(c[5],c[6]);
  group_3.target_voltage = byteDecoder(c[7],c[8]);
  
}

int byteDecoder(int byte_1, int byte_2){
  
  int x = byte_1*255+byte_2;

  return x;
  
}

void requestEvent(){
  Serial.println("request");
  int message_timer = millis();

  Wire.write(ref_0 / 255);
  Wire.write(ref_0 % 255);

 
  Wire.write(ref_1 / 255);
  Wire.write(ref_1 % 255);

  Wire.write(ref_2 / 255);
  Wire.write(ref_2 % 255);

  Wire.write(ref_3 / 255);
  Wire.write(ref_3 % 255);
}
