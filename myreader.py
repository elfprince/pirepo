#!/usr/bin/env python
# -*- coding: utf8 -*-
#


import RPi.GPIO as GPIO
import MFRC522
import signal
from time import sleep
import subprocess
from picamera import PiCamera


def captureImage(): 
    camera = PiCamera() 
    camera.capture('/home/pi/repo/mypiproject/captured/image.jpg')
    print ('Captured')
    camera.close()

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
MIFAREReader = MFRC522.MFRC522()

def readCard():
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        hexUid = ""
        for val in uid[0:4]:
            hexUid = hexUid + "{:02x}".format(val)
        return str(hexUid)
    else:
      return ""
    


# Welcome message
print ("Welcome to the MFRC522 data read example")
print ("Press Ctrl-C to stop.")

continue_reading = True
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    serialNumber = readCard()
    sleep(1)
    if serialNumber != "":
        print ("Serial number: %s" % serialNumber)
        captureImage()
        