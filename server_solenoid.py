import RPi.GPIO as GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)          #Using BCM pin layout
GPIO.setwarnings(False)

from time import sleep

import os
os.system("sudo /usr/sbin/hostapd /etc/hostapd/hostapd.conf") #Set up server for client to connect to

#Initialize each solenoid with the corresponding pin

Sol0 = 21
Sol1 = 26
Sol2 = 23
Sol3 = 24
Sol4 = 19
Sol5 = 25
Sol6 = 12
Sol7 = 13
Sol8 = 16
Sol9 = 20
SolOutputs = [21,26,23,24,19,25,12,13,16,20] #List created to call all at once

recCtrl = 6            #Controls the receiver button

callLabib = 27          #Button input to call Labib
callBrandon = 17        #Button input to call Brandon
RESET = 5          #To be used later...
hangUp = 22              #Button input to hang up the phone
InputsList = [27,17,5,22] #List created to call all at once

currentCall = False

GPIO.setup(SolOutputs, GPIO.OUT) #Sets all solenoid pins as outputs
GPIO.output(SolOutputs, GPIO.LOW) #Initially all solenoids are off

GPIO.setup(InputsList, GPIO.IN) #Sets all the inputs as input pins
GPIO.setup(6, GPIO.OUT)        #Sets the receiver control pin as an output
GPIO.output(recCtrl, GPIO.HIGH) #Receiver initially starts on; button is pressed down

Caller1 = [2,8,9,0,0,0,0,0,0,0] #sample phone numbers
Caller2 = [2,8,9,0,0,0,0,0,0,1]
Caller3 = [2,8,9,0,0,0,0,0,0,2]
Caller4 = [2,8,9,0,0,0,0,0,0,3]

t = 0.5         #Time delay variable

def solExtend(num):     #This function receives each digit in the phone number and activates the corresponding solenoid
	if num == 0:
		GPIO.output(Sol0, GPIO.HIGH)    #Activates solenoid
		sleep(t)                   	#Pauses for activation
		GPIO.output(Sol0, GPIO.LOW)     #Solenoid retracts
	elif num == 1:
		GPIO.output(Sol1, GPIO.HIGH)
		sleep(t)
		GPIO.output(Sol1, GPIO.LOW)
	elif num == 2:
		GPIO.output(Sol2, GPIO.HIGH)
		sleep(t)
		GPIO.output(Sol2, GPIO.LOW)
	elif num == 3:
		GPIO.output(Sol3, GPIO.HIGH)
		sleep(t)
		GPIO.output(Sol3, GPIO.LOW)
	elif num == 4:
		GPIO.output(Sol4, GPIO.HIGH)
		sleep(t)
		GPIO.output(Sol4, GPIO.LOW)
	elif num == 5:
		GPIO.output(Sol5, GPIO.HIGH)
		sleep(t)
		GPIO.output(Sol5, GPIO.LOW)
	elif num == 6:
		GPIO.output(Sol6, GPIO.HIGH)
		sleep(t)
		GPIO.output(Sol6, GPIO.LOW)
	elif num == 7:
		GPIO.output(Sol7, GPIO.HIGH)
		sleep(t)
		GPIO.output(Sol7, GPIO.LOW)
	elif num == 8:
		GPIO.output(Sol8, GPIO.HIGH)
		sleep(t)
		GPIO.output(Sol8, GPIO.LOW)
	elif num == 9:
		GPIO.output(Sol9, GPIO.HIGH)
		sleep(t)
		GPIO.output(Sol9, GPIO.LOW)


def solCallControl(caller):     #Function receives the caller
	for i in range(len(caller)): #Executes for length of phone number (10 digits)
		solExtend(caller[i]) #Calls function above, inputting each digit in the list
		print("Digit =", caller[i]) #Prints the digit dialed (for debugging purposes)
		sleep (0.2)     #Pauses



while GPIO.input(RESET) == False: #Constant loop; ends only when the reset button is triggered
        import socket

        UDP_IP = '192.168.42.1' #This is the IP address of the server; this device
        UDP_PORT = 50007        #This is the port being used for communication between the two devices

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))

        while True:
                data, addr = sock.recvfrom(1024) #Receives the message from the client and stores it as 'data'
                print('Message received', data)
            

                if data == 'Caller1': #If caller1 is dialed
                        GPIO.output(recCtrl, GPIO.LOW) #Receiver button is lifted
                        currentCall = True
                        sleep(1)   #Pause for phone to recognize
                        solCallControl(Caller1)   #Call labib using function above
                        sleep(1)
                elif data == 'Caller2':
                        GPIO.output(recCtrl, GPIO.LOW)
                        currentCall = True
                        sleep(1)
                        solCallControl(Caller2)
                elif data == 'Caller3':
                        GPIO.output(recCtrl, GPIO.LOW)
                        currentCall = True
                        sleep(1)
                        solCallControl(Caller3)
                elif data == 'Caller4': #If Brandon is dialed
                        GPIO.output(recCtrl, GPIO.LOW)
                        currentCall = True
                        sleep(1)
                        solCallControl(Caller4)
                elif data == 'Hang Up': #If hang up button is pressed
                        if currentCall == True: #Only runs if there is an active call; this ends the call
                                GPIO.output(recCtrl, GPIO.HIGH) #Receiver button is activated
                                print("HANG UP")        #Prints 'hang up' (for debugging purposes)
                                currentCall = False
                                sleep(1)
                        elif currentCall == False: #Only runs if there is no active call; this answers a call
                                GPIO.output(recCtrl, GPIO.LOW)
                                print("PICK UP") #For debugging
                                currentCall = True
                        sleep(2)
        if RESET == True:               #If the reset button is pressed, end program
                print("RESET")          #For debugging
                GPIO.cleanup()          #Clear GPIO pins for program stability
                os.system("sudo /usr/sbin/hostapd /etc/hostapd/hostapd.conf") #Ends the server
                break                   #Ends the loop
