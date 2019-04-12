#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11);

int m1 = 2;
int m2 = 3;
int m3 = 4;
int vD = 0;
double vA = 0.0;
int c = 1;

float gFinal;
float gFinal2;


void setup()
{
	Serial.begin(115200);
	mySerial.begin(38400);
	pinMode(A0, INPUT);
	pinMode(A1, INPUT);
	pinMode(A2, INPUT);
	pinMode(A3, INPUT);
}

void loop()
{

	//BATERIAS

	vD = analogRead(A0);
	vA = (double(vD)/1023.00)*5.00;
	vA = vA*(25.2/3.96);
	Serial.print("C");
	Serial.println(vA);

	vD = analogRead(A1);
	vA = (double(vD)/1023.00)*5.00;
	vA = vA*(25.2/3.98);
	Serial.print("D");
	Serial.println(vA);

	vD = analogRead(A2);
	vA = (double(vD)/1023.00)*5.00;
	vA = vA*(25.2/4.05);
	Serial.print("E");
	Serial.println(vA);

	vD = analogRead(A3);
	vA = (double(vD)/1023.00)*5.00;
	vA = vA*(50.4/4.81);
	Serial.print("F");
	Serial.println(vA);



	//GPS


	if (mySerial.available() > 0) 
	{

		String all = mySerial.readStringUntil('\n');
		String head = all.substring(0, all.indexOf(","));                
		
		int i1 = all.indexOf(",")+1; 


		if(head.equals("$GPRMC")){

			int i2;

			i2 = all.indexOf(",", i1);
			String stime = all.substring(i1, i2);

			i1 = i2 + 1;
			i2 = all.indexOf(",", i1);
			String valid = all.substring(i1, i2);

			i1 = i2 + 1;
			i2 = all.indexOf(",", i1);
			String latitude = all.substring(i1, i2);

			i1 = i2 + 1;
			i2 = all.indexOf(",", i1);
			String N_S = all.substring(i1, i2);

			i1 = i2 + 1;
			i2 = all.indexOf(",", i1);
			String longitude = all.substring(i1, i2);

			i1 = i2 + 1;
			i2 = all.indexOf(",", i1);
			String E_W = all.substring(i1, i2);

			if(valid.equals("A"))
			{
				if(!latitude.equals("") && !longitude.equals(""))
				{
					int punto=latitude.indexOf(".");
					String grados=latitude.substring(0,punto-2);
					float gradosFinal=grados.toFloat();
					String minutos=latitude.substring(punto-2);
					float minFinal=minutos.toFloat();
					float minAGrados=minFinal/60.0;
					gFinal=gradosFinal+minAGrados;



					int punto2=longitude.indexOf(".");
					String grados2=longitude.substring(0,punto2-2);
					float gradosFinal2=grados2.toFloat();
					String minutos2=longitude.substring(punto2-2);
					float minFinal2=minutos2.toFloat();

					float minAGrados2=minFinal2/60.0;
					gFinal2=-(gradosFinal2+minAGrados2);

					Serial.print("A");
					Serial.println(gFinal, 7);
					Serial.print("B");
					Serial.println(gFinal2, 7);

				}
			}

		}
	}



}
