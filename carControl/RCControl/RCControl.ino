#include <Servo.h> 

int helm=15;
int motor = 14;
//
//int helm=2;
//int motor = 3;

Servo motor_left;
Servo helm_servo;

int helm_center=90;
//int helm_angle_pin = 8;
//int mot_pin_left = 9;

int helm_angle_pin = 16;
int mot_pin_left = 17;

int helm_angle_rc;
int motor_speed_rc;

int motor_speed,helm_angle;
int start = 1;

void setup()
{
    Serial.begin(115200);    //Start serial at baud rate 9600
    pinMode(motor, INPUT);  //Define motor and helm as input
    pinMode(helm,INPUT);
     
    motor_left.attach(mot_pin_left);    //Инициальзация левого мотора (порт, начальная позиция, максимальная позиция)       !!!
    helm_servo.attach(helm_angle_pin);

}
void loop()
{
  
  if(start == 1) {
    motor_left.write(1500);
    delay(700);
    start = 0;
  }

  
  motor_speed = pulseIn(motor, HIGH);            //Read the pulse and store it as val
  helm_angle = pulseIn(helm,HIGH);                   //Print val to serial monitor

  

  motor_speed_rc = map(motor_speed, 900, 1900,800, 1900);
  
  helm_angle_rc = map(helm_angle, 970, 2070, 45, -45);
  
  Serial.println("\t");
  Serial.println("\t");
  Serial.print(motor_speed_rc);
  Serial.print("\t");
  Serial.print(helm_angle_rc);


  if ((motor_speed_rc<1550) and (motor_speed_rc>1450)){
      motor_speed_rc=1500;
    }
    
  if ((helm_angle<1550) and (helm_angle_rc>1450)){
      motor_speed_rc=0;
    }
    
  motor_left.write(motor_speed_rc);
  helm_servo.write(helm_center+helm_angle_rc);
  
  
delay(50);

}
