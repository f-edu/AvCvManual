#include <Servo.h> 

Servo motor_left;
Servo helm_servo;

int helm_angle_pin = 8;
int mot_pin_left = 9;
int helm_center=90;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);   
  motor_left.attach(mot_pin_left);
  helm_servo.attach(helm_angle_pin);
  helm_servo.write(helm_center);
  delay(500);
  motor_left.write(1500);
  delay(500);
 
}


int helm_test(int helm_angle_max){
   helm_servo.write(helm_center+helm_angle_max);
   delay(2000);
   helm_servo.write(helm_center-helm_angle_max);
   delay(2000);
}

int motor_test(int forward_motor_speed){
  
   motor_left.write(1580);
   delay(2000);
   
   motor_left.write(800);
   delay(100);
   
   motor_left.write(1500);
   delay(100);


   motor_left.write(1380);
   delay(2000);
  
   motor_left.write(1500);
   delay(200);
}


 

void loop() {

  //1. Tesing helm servo. 
  //Max angle 35 deg.
  
  //helm_test(30);

  
  //1. Tesing motor. 
  //Min forward speed = 1580.
  //Max forward speed = 2300.
  

  motor_test(30);

  


}
