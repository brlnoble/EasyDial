import RPi.GPIO as GPIO #For GPIO input
#import os               # Was used for sudo commands, NOT used anymore
from time import sleep  #Only need sleep function
import socket

GPIO.setmode(GPIO.BCM)  #Using BCM layout

Caller1 = 16            #Initializing these pins for each caller
Caller2 = 21
Caller3 = 20
Caller4 = 26
HangUp = 19

GPIO.setup([21,20,16], GPIO.IN) #Set input pins

UDP_IP = '192.168.42.1' #This is the IP address of the server
UDP_PORT = 50007        #Port being used by the server and client
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Initiate socket

while True:
    if GPIO.input(Caller1) == True: #If caller1 is called
        MESSAGE = 'Caller1'         #This string is sent to the server
        sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT)) #Encodes and sends message
        print("Caller1")
        sleep(1)

    elif GPIO.input(Caller2) == True: #If caller2 is called
        MESSAGE = 'Caller2'
        sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))
        print("Caller2")
        sleep(1)
        
    elif GPIO.input(Caller3) == True: #If caller3 is called
        MESSAGE = 'Caller3'
        sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))
        print("Caller3")
        sleep(1)
        
    elif GPIO.input(Caller4) == True: #If caller4 is called
        MESSAGE = 'Caller4'
        sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))
        print("Caller4")
        sleep(1)
        
    elif GPIO.input(HangUp) == True: #If hang up button is pressed
        MESSAGE = 'Hang Up'
        sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))
        print("Hang Up")
        sleep(1)


#This is the client program; when a button is pressed it recognizes who the desired
    #caller is and creates a string to the corresponding person. This string is then
    #encoded and sent over to server.
