import os
import time
import RPi.GPIO as GPIO
from socket import *
PIN_AUDIO = 12  #gpio 12
PIN_RELAY = 22  #gpio 22

def setup():
	GPIO.setmode(GPIO.BCM)      
        GPIO.setwarnings(False)
	GPIO.setup(PIN_RELAY, GPIO.OUT)
	GPIO.setup(PIN_AUDIO, GPIO.OUT)


def alarm():

	GPIO.output(PIN_AUDIO, GPIO.LOW)
	GPIO.output(PIN_RELAY, GPIO.LOW)
	time.sleep(2)
	GPIO.output(PIN_RELAY, GPIO.HIGH)
	GPIO.output(PIN_AUDIO, GPIO.HIGH)

		

def createServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.bind(('0.0.0.0',9000))
    serversocket.listen(3)
    while(1):
        (clientsocket, address) = serversocket.accept()
        alarm()
        clientsocket.send("HTTP/1.1 200 OK\n"
         +"Content-Type:application/json\n"
         +"\n" # Important!
         + '{"success":true}'
         +"\n")
        clientsocket.shutdown(SHUT_WR)
        clientsocket.close()

    serversocket.close()



def destroy():
	GPIO.output(PIN_RELAY, GPIO.HIGH)
	GPIO.output(PIN_RELAY, GPIO.HIGH)
	GPIO.cleanup() 

if __name__ == '__main__':   
	setup()
	try:
		createServer()
	except KeyboardInterrupt:  
		destroy()
