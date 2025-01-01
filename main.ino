#include "Arduino.h"
#include "Buzzer.h"
#include "DHT.h"
#include "LiquidCrystal.h"
#include "LED.h"

#define BUZZER_PIN_SIG	2
#define DHT_PIN_DATA	3
#define LCD_PIN_RS	11
#define LCD_PIN_E	10
#define LCD_PIN_DB4	4
#define LCD_PIN_DB5	7
#define LCD_PIN_DB6	8
#define LCD_PIN_DB7	9
#define LEDG_PIN_VIN	5
#define LEDR_PIN_VIN	6
#define MQ135_5V_PIN_AOUT	A3

#define DHTTYPE DHT11

int t_int;
int h_int;
int c_int;

char clear = "                ";

Buzzer buzzer(BUZZER_PIN_SIG);
LiquidCrystal lcd(LCD_PIN_RS,LCD_PIN_E,LCD_PIN_DB4,LCD_PIN_DB5,LCD_PIN_DB6,LCD_PIN_DB7);
LED ledG(LEDG_PIN_VIN);
LED ledR(LEDR_PIN_VIN);
DHT dht(DHT_PIN_DATA, DHTTYPE, 3);


void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  dht.begin();
};

void loop() {

  get_readings();
  print_to_lcd();


  if (((12 < t_int) && (25 > t_int)) && ((20 < h_int) && (80 > h_int)) && (c_int < 1000)) {

    for(int i=255 ; i> 0 ; i -= 5)
    {
    ledG.dim(i);
    delay(15);
    }
    ledG.off();    
  } else {

    for(int i=255 ; i> 0 ; i -= 5)
    {
    ledR.dim(i);
    delay(15);
    }                                          
    ledR.off();

    buzzer.on();
    delay(500);
    buzzer.off();

    }
  

};

void get_readings() {

  //Read CO2 Level
  float h = dht.readHumidity();
  h_int = (int)h;
  float t = dht.readTemperature();
  t_int = (int)t;
  c_int = analogRead(MQ135_5V_PIN_AOUT);


};

void print_to_lcd() {

  lcd.setCursor(1, 0);
  lcd.print("Humidity - ");
  lcd.print(h_int);
  lcd.print("%");

  lcd.setCursor(3, 1);
  lcd.print("Temp - ");
  lcd.print(t_int);
  lcd.print("C");

  delay(2000);

  lcd.setCursor(0, 0);
  lcd.print("                ");
  lcd.setCursor(0, 1);
  lcd.print("                ");

  delay(500);

  lcd.setCursor(1, 0);
  lcd.print("CO2 - ");
  lcd.print(c_int*35);
  lcd.print(" PPM");

  delay(2000);

  lcd.setCursor(0, 0);
  lcd.print("                ");
  lcd.setCursor(0, 1);
  lcd.print("                ");

  delay(500);

}
