#include <Servo.h>

Servo myservo;
int16_t data;

void setup(void)
{
	myservo.attach(3);
	Serial.begin(115200);
}

void loop(void)
{
	if(Serial.available())
	{
		data = Serial.read();
		Serial.print("data arrived:");
		Serial.println(data);
	}

	if(data == 49)//open(ascii "1")の時
	{
		//open
		Serial.println("open START");
		myservo.writeMicroseconds(1);
		delay(1000);
		myservo.writeMicroseconds(1300);
		//delay(50);
		Serial.println("open OK");
	}
	else if(data == 50)//close(ascii "2")の時
	{
		//close
		Serial.println("close START");
		myservo.writeMicroseconds(2600);
		delay(1000);
		myservo.writeMicroseconds(1300);
		//delay(50);
		Serial.println("close OK");
	}
	else;
}
