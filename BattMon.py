import time
import string
import RPi.GPIO as GPIO
#from time import gmtime, strftime

GPIO.setmode(GPIO.BCM)         # Pins numbered by GPIO numbering

SPICLK = 8                     # clock GPIO8, pin 24
SPIMISO = 23                   # data in GPIO23, pin 16
SPIMOSI = 24                   # data out GPIO24, pin 18
SPICS = 25                     # chip select GPIO25, pin 22

# Set up GPIO pin directions
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

#####################################################################
# Function to read MCP3002 ADC chip.
# adcnum refers to CH0 or CH1
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 1) or (adcnum < 0)):
        return -1
    if (adcnum == 0):
        commandout = 0x6
    else:
        commandout = 0x7

    GPIO.output(cspin, True)      # set CS high
    GPIO.output(clockpin, False)  # start clock low
    GPIO.output(cspin, False)     # bring CS low

    commandout <<= 5    # we only need to send 3 bits here
    for i in range(3):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:   
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        if (GPIO.input(misopin)):
            adcout |= 0x1

    GPIO.output(cspin, True)

    adcout /= 2       # first bit is 'null' so drop it
    return adcout
####################################################################
# Function to get battery voltage.
def getVolts(ch):
    if(ch == 0):
        adcs = [0] # 0 battery voltage divider
        vflat = 4.0
        dv = 5.0 - vflat
    else:
        adcs = [1]
        vflat = 9.0
        dv = 11.1 - vflat

    reps = 10  # how many times to take each measurement for averaging

#    initspi()  # initialise GPIO pins for SPI comms
    for ch in adcs:
        # read the analog pin
        adctot = 0
        for i in range(reps):
            read_adc = readadc(ch, SPICLK, SPIMOSI, SPIMISO, SPICS)
            adctot += read_adc
            time.sleep(0.05)
        read_adc = adctot / reps / 1.0
#        print(read_adc)

        # convert analog reading to Volts = ADC * ( 3.33 / 1024 )
        # 3.33 tweak according to the 3v3 measurement on the Pi
        if(ch == 0):
            volts = read_adc * (3.33 / 1024.0) * 2.37
            if(volts - vflat <= 0):
                perCent = 0
            else:
                perCent = 100 * (volts - vflat)/dv
        else:
            volts = read_adc * (11.1 / 1024) * 0.45
            if(volts - vflat <= 0):
                perCent = 0
            else:
                perCent = 100 * (volts - vflat) / dv

    if(perCent > 100):
        perCent = 100

#####################################################################

# BattMon.py
# Script to monitor battery voltages via MCP3002 ADC using SPI
# getVolts(0) returns voltage on CH0 - Raspberry Pi battery
# getVolts(1) returns voltage on CH1 - Motor battery

# Example
 Rpibat = getVolts(0)
 voltstring = str(Rpibat)[0:5]
 print("Pi Battery Voltage: %.2f" % Rpibat)
 Motbat = getVolts(2)
 voltstring = str(Motbat)[0:5]
 print("Motor Battery Voltage: %.2f" % Motbat)






