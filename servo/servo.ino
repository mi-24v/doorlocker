#include <Servo.h>

Servo myservo;
String data;

void setup(void)
{
	myservo.attach(3);
	Serial.begin(115200);
}

void loop(void)
{
	data = "";
	if(Serial.available())
	{
		data = Serial.readString();
		Serial.print("data arrived:");
		Serial.println(data);
	}

	if(data.startsWith("open"))//"open*"の時
	{
		//open
		Serial.println("open START");
		myservo.writeMicroseconds(1);
		delay(1000);
		myservo.writeMicroseconds(1300);
		//delay(50);
		Serial.println("open OK");
	}
	else if(data.startsWith("close"))//"close*"の時
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
