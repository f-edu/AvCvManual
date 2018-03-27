#include <Servo.h> 
#include <Ultrasonic.h>

Servo motor_left;
Servo helm_servo;

Ultrasonic ultrasonic_middle(22, 24);
Ultrasonic ultrasonic_left(26, 28);
Ultrasonic ultrasonic_right(30, 32);


int helm_angle_pin = 16;
int mot_pin_left = 17;
int helm_center=90;

int js_position = 1500;  //Начальная позиция, всегда 1.5 мс для регуляторов бесколлекторных двигателей
int max_position = 2300; //Максимальное значение ШИМ 2.3 мс
int min_position = 800;  //Минимальное значени ШИМ 0.8 мс

int start=1;

int us_middle_distance;
int us_left_distance;
int us_right_distance;

int run_count;

float corridor_coef;
float corridor_angle;

int right_line_sensor;
int left_line_sensor;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);   
  motor_left.attach(mot_pin_left, js_position, max_position);
  motor_left.write(1500);
  delay(1000);
  
  helm_servo.attach(helm_angle_pin);
  helm_servo.write(helm_center);
  delay(700);
}


int helm_test(int helm_angle_max){
   helm_servo.write(helm_center+helm_angle_max);
   delay(2000);
   helm_servo.write(helm_center-helm_angle_max);
   delay(2000);
}

int motor_test(){

   motor_left.write(1600);
   delay(2000);
   
   motor_left.write(800);
   delay(100);
   
   motor_left.write(1500);
   delay(1000);


   motor_left.write(1350);
   delay(2000);
  
   motor_left.write(1500);
   delay(1000);
}

int move_to_barrier(int distance){
  
   us_middle_distance=ultrasonic_middle.distanceRead();
   Serial.println(us_middle_distance);
   
   if ((us_middle_distance==0) or (us_middle_distance>distance)){
//      motor_left.write(1500);
//      delay(200);
      motor_left.write(1590);
      run_count=1;
    } else {
        if (run_count==1){
//          motor_left.write(800);
//          delay(20);
          motor_left.write(1500);
          run_count=0;
        }  
    }   
  }
  
int corridor(){
     us_left_distance=ultrasonic_left.distanceRead();
     us_right_distance=ultrasonic_right.distanceRead();

     Serial.println(us_left_distance);
     Serial.println(us_right_distance);

     if (us_left_distance<us_right_distance){
          helm_servo.write(helm_center-20);
          delay(200);
          motor_left.write(1600);
     } else if (us_left_distance>us_right_distance){
          helm_servo.write(helm_center+20);
          delay(200);
          motor_left.write(1600);
          
     } else {
      motor_left.write(1600);
      }
     
        
}

int corridor_corners(){


     us_left_distance=ultrasonic_left.distanceRead();
     us_right_distance=ultrasonic_right.distanceRead();


    
     if (us_left_distance<us_right_distance){
      
          if (float(us_right_distance)/float(us_left_distance)>2){
            corridor_angle=30;
          } else {
            corridor_coef=(float(us_right_distance)/float(us_left_distance))-1;
            corridor_angle=corridor_coef*30;
          }                
          helm_servo.write(helm_center-corridor_angle);
          delay(100);
          motor_left.write(1600);
          
     } else if (us_left_distance>us_right_distance){

          if (float(us_left_distance)/float(us_right_distance)>2){
            corridor_angle=30;
          } else {
            corridor_coef=(float(us_left_distance)/float(us_right_distance))-1;
            corridor_angle=corridor_coef*30;

          }     
      
          helm_servo.write(helm_center+corridor_angle);
          delay(100);
          motor_left.write(1600);
          
     } else {
      motor_left.write(1600);
      }
     
        
}

int white_line_sensor(int middle){
  
  right_line_sensor=analogRead(A0);
  left_line_sensor=analogRead(A1);

  motor_left.write(1600);

  if (left_line_sensor>middle){
    helm_servo.write(helm_center+30);
    delay(100);
    }

      if (right_line_sensor>middle){
    helm_servo.write(helm_center-30);
    delay(100);
    }
//    if ((left_line_sensor>middle) and (right_line_sensor>middle)){
//         helm_servo.write(helm_center);
//    delay(200); 
//    }
  
  Serial.print(right_line_sensor);
   Serial.print("           ");
    Serial.println(left_line_sensor);


     
}

int line_sensor(){
  //http://www.prorobot.ru/lego/line-following-2-sensors.php
}
     

     



 

void loop() {

  //1a. Tesing helm servo. 
  //Max angle 35 deg.
  
  //helm_test(30);

  
  //1b. Tesing motor. 
  
  //Min forward speed = 1580.
  //Max forward speed = 2300.
  //Min backward speed = 1380.
  //Max backward speed = 800.

  //800 - stop. If you want to turn back you must make 800 for sop and netral-1500 (see function "motor_test) 
//Test Example:
//  motor_test();

//  // Using example:
//   motor_left.writeMicroseconds(1500);
//   delay(20);
//
//      motor_left.writeMicroseconds(1600);
//   delay(2000);
//
//      motor_left.writeMicroseconds(800);
//   delay(20);
//         motor_left.writeMicroseconds(1500);
//   delay(200);
//         motor_left.writeMicroseconds(1300);
//   delay(2000);

// 2a. Move to barrier
//  min distance = 10 cm, max distance = 200 cm

//  move_to_barrier(30);

// 2.b Move into corridor

//  corridor();

// 2.c Move corridor r-angle

 // 2.d Move corridor s-angle
// corridor_corners();

 //3. a,b lineSensor
// white_line_sensor(300);
}
