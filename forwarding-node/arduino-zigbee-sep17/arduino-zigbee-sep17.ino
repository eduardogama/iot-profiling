#include <Arduino.h>
#include <DHT.h>
#include <Adafruit_Sensor.h>
#include <SoftwareSerial.h>

SoftwareSerial xbee_s(2, 3);

// Pino conectado ao pino de dados do sensor
#define DHTPIN 7

#define DHTTYPE DHT22   // Sensor DHT 22  (AM2302)

// Definicoes do sensor : pino, tipo
DHT dht(DHTPIN, DHTTYPE);

//Definicao pinos sensor
int pino_analogico = A5;
int pino_digital = 5;


int valor_A0 = 0;
int valor_D = 0;

String ATCMD;
// Array simbolo grau
byte grau[8] ={ B00001100,
                B00010010,
                B00010010,
                B00001100,
                B00000000,
                B00000000,
                B00000000,
                B00000000,};  

void setup()
{
  xbee_s.begin(9600);
  Serial.begin(9600);

  xbee_s.print("+++"); 
  delay(1000);
 
  if(xbee_s.available()){
    ATCMD = xbee_s.readString();
    Serial.println(ATCMD);
  }

  xbee_s.print("ATID\r");  //ask PAN ID
 
  delay(1000);
  
  if(xbee_s.available()){
    ATCMD = xbee_s.readString();  // answer PAN ID
    Serial.println(ATCMD);
  }
  xbee_s.print("ATSH\r");  // ask higher serial address
 
  delay(1000);
  if(xbee_s.available()){
    ATCMD = xbee_s.readString();  // answer higher serial address
    Serial.println(ATCMD);
  }
  
  xbee_s.print("ATSL\r");  // ask lower serial address
 
  delay(1000);
 
  if(xbee_s.available()){
    ATCMD = xbee_s.readString();  // answer lower serial address
    Serial.println(ATCMD);
  }
  xbee_s.print("ATCN\r");  // ask lower serial address
 
  delay(1000);
 
  if(xbee_s.available()){
    ATCMD = xbee_s.readString();
    Serial.println(ATCMD);
  }

  Serial.println("Aguardando dados...");
  //Iniclaiza o sensor DHT
  //Define pinos sensor como entrada
  pinMode(pino_analogico, INPUT);
  pinMode(pino_digital, INPUT);

  dht.begin();
}

String probe;

void loop()
{
  delay(1000);
  String msg;
  probe = "\0";
  int aux=0;

  Serial.println("entrou loop()");
  if(xbee_s.available()){
    probe = xbee_s.readString();
    aux=1;
    Serial.println(probe);
    xbee_s.print("Starting PL\n");
  }

  if(aux != 0){

    xbee_s.print("+++");
    delay(3000);

    if(xbee_s.available()){
      ATCMD = xbee_s.readString();
      Serial.println(ATCMD);
    }
 
    if(probe == "1"){
        xbee_s.print("ATPL 1\r"); //4,3,2,1
    }else if(probe == "2"){
        xbee_s.print("ATPL 2\r"); //4,3,2,1
    }else if(probe == "3"){
        xbee_s.print("ATPL 3\r"); //4,3,2,1
    }else if(probe == "4"){
        xbee_s.print("ATPL 4\r"); //4,3,2,1
    }
    
    delay(1000);
    if(xbee_s.available()){
      ATCMD = xbee_s.readString();
      Serial.println(ATCMD);
    }

    delay(1000);
    xbee_s.print("ATPL\r");
    
    if(xbee_s.available()){
      ATCMD = xbee_s.readString();
      Serial.println(ATCMD);
    }

    delay(10000);
    
    Serial.print("Iniciando teste ...\n");
    xbee_s.print("Starting test\n");
    
    int d = 40;//probe.toInt(); //Delay between packets in ms
    
    int count = 10; //msg
    
    // Leitura da umidade
    float hmd = dht.readHumidity();
    // Leitura da temperatura (Celsius)
    float tmp = dht.readTemperature(); 
    // Verifica se o sensor esta respondendo
    if (isnan(hmd) || isnan(tmp)){
        Serial.println("Falha ao ler dados do sensor DHT !!!");
        return;
    }
    int i,j; 
    msg += "Temperatura: ";
    msg += tmp;
    msg += "*C Humidade: ";
    msg += hmd;
    msg += "%\n";

    while(count--){
      xbee_s.print(msg); 
      delay(d);
    }

    delay(1000);

    xbee_s.print("+++");
    delay(3000);

    if(xbee_s.available()){
      ATCMD = xbee_s.readString();
      Serial.println(ATCMD);
    }

    xbee_s.print("ATPL 4\r");

    delay(1000);
    if(xbee_s.available()){
      ATCMD = xbee_s.readString();
      Serial.println(ATCMD);
    }

    delay(10000);

    xbee_s.print("[FIN]\n");
    Serial.print("[FIN]\n");
  }
}
