import RPi.GPIO as GPIO
import time, random
from pixel import Pixel

DATA = 7
CLOCK = 11
BRIGHTNESS = 90

def sendBit(val):
    GPIO.output(DATA,val)
    GPIO.output(CLOCK,True)
    GPIO.output(CLOCK,False)

def sendByte(val):
    #testByte(val)
    for pos in range(7,-1,-1):
        mask = 2**pos
        bit = (val&mask>0)
        sendBit(bit)

def testByte(val):
    byteString = ""
    for pos in range(7,-1,-1):
        mask = 2**pos
        bit = (val&mask>0)
        if bit == True:
            byteString = byteString + "1"
        else:
            byteString = byteString + "0"
    print(str(val)+" = "+byteString)

def sendZeros():
    for x in range(0,8):
        sendBit(False)

def sendOnes():
    for x in range(0,8):
        sendBit(True)

def start():
    sendZeros()
    sendZeros()
    sendZeros()
    sendZeros()

def end():
    sendOnes()
    sendOnes()
    sendOnes()
    sendOnes()

def off():
    sendByte(BRIGHTNESS)
    sendZeros()
    sendZeros()
    sendZeros()

def allOff():
    start()
    for x in range(0,61):
        off()
    end()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(DATA, GPIO.OUT)
GPIO.setup(CLOCK, GPIO.OUT)


# OFF
allOff()

GPIO.cleanup()

print("Done")
