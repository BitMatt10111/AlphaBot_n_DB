import socket as sck
import threading as thr 
import logging
import time
import RPi.GPIO as GPIO #libreria per alphabot
import sqlite3 #libreria per sqlite

class AlphaBot(object): #classe per gestire il moviemento dell'AlphaBot
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 25
        self.PB  = 25
        
        #setup iniziale del bot
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def right(self, sec): #funzione che ruota sul posto verso destra il bot per "sec" secondi
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(sec) #continua a muoversi per la durata del moviemento indicata come parametro
        self.stop() #dopo aver concluso il movimento si ferma

    def stop(self): #funzione che ferma il bot
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def left(self, sec): #funzione che ruota sul posto verso sinistra il bot per "sec" secondi
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        time.sleep(sec) #continua a muoversi per la durata del moviemento indicata come parametro
        self.stop() #dopo aver concluso il movimento si ferma

    def forward(self, sec, speed=30): #funzione che muove avanti il bot per "sec" secondi
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(sec) #continua a muoversi per la durata del moviemento indicata come parametro
        self.stop() #dopo aver concluso il movimento si ferma


    def backward(self, sec, speed=30): #funzione che muove indietro il bot per "sec" secondi
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        time.sleep(sec) #continua a muoversi per la durata del moviemento indicata come parametro
        self.stop() #dopo aver concluso il movimento si ferma
        
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

class Client_Manager(thr.Thread):
    def __init__(self,connection,address):
        thr.Thread.__init__(self) #super di Java
        self.connection=connection
        self.address=address
        self.alpha=AlphaBot()
        self.running=True
    
    def run(self):
        while self.running:
            msg=self.connection.recv(4096).decode() #aspetta di ricevere un messaggio (nome del comando) dal client
            conn = sqlite3.connect("movements.db") #crea una "connessione" col database
            cur = conn.cursor()
            cur.execute(f"SELECT sequenza FROM movements WHERE nome = '{msg}'") #esegue la query indicata per trovare la sequenza giusta tramite il nome
            comandi = cur.fetchall()[0][0]
            l_comandi=comandi.split(":") #divide la sequenza in singoli comendi [movimento:tempo]
            for comando in l_comandi:
                c=comando[0] #preleva dalla stringa il movimento
                if c!="S":
                    sec=float(comando[1:]) #preleva dalla stringa i secondi e li mette float
                    #print(sec)
                if c[0] == "F": #se il comando è F -> va avanti
                    self.alpha.forward(sec)
                elif c[0] == "S": #se il comando è S -> si ferma
                    self.alpha.stop()
                elif c[0] == "B": #se il comando è B -> va indietro
                    self.alpha.backward(sec)
                elif c[0] == "R": #se il comando è R -> gira a destra
                    self.alpha.right(sec)
                elif c[0] == "L":  #se il comando è L -> gira a sinistra
                    self.alpha.left(sec)
                else:
                    logging.debug("Errore di sintassi")

def main():
    
    s=sck.socket(sck.AF_INET,sck.SOCK_STREAM) #crea il socket per la trasmissione tcp 
    s.bind(("192.168.0.131",5000))
    s.listen() #si mette in ascolto per un client che si connette

    while True:
        
        connection, address=s.accept() #accetta la connessione
        client=Client_Manager(connection,address) #crea il thread per gestire il client
        print(address)
        client.start() #avvia il thread client

if __name__=="__main__":
    main()
