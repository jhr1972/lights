#!/usr/bin/python3
import asyncio
import RPi.GPIO as GPIO
import sys
import time
import traceback

loop = None

def alter_GPIO(input,led):
    #led = 24
    current_value= GPIO.input(led)
    print ("reading current value of led " + str(led) +": " + str(current_value )+".")
    if ( current_value == GPIO.HIGH ):
        GPIO.output(led, GPIO.LOW)
        print ("GPIO" + str(led) + " now set to ON /LOW (" + str(current_value) + ")" )
    else:
        GPIO.output(led, GPIO.HIGH)
        print ("GPIO" + str(led) + " now set to OFF /HIGH (" + str(current_value) + ")" )
 
    
def callback_GPIO(input, led):
    if loop is None:
        print(":(")
        return       # should not come to this
    # this enqueues a call to message_manager_f() 
    print("GPIO {} pressed".format(input))
    time.sleep(0.1)
    current_button = GPIO.input(input)
    print ("reading current value of input " + str(input) +": " + str(current_button )+".")
    countdown = 3
    em = 0 
    while (countdown):
       if (current_button ==  GPIO.LOW):
           countdown -= 1
           em = 0
           time.sleep(0.1)
           print ("waiting a little more to be sure. Counter: " + str(countdown))

       else:
           print ("disregarding EM effects")
           countdown = 0
           em = 1 

    if ( em == 0 ):
           loop.call_soon_threadsafe(lambda: alter_GPIO(input,led))
    else:
           print ("doing nothing due to detected em effects")

    


# this is the primary thread mentioned in Part 2
if __name__ == '__main__':
    try:
        # setup the GPIO
        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.IN)  #  office
        GPIO.setup(20, GPIO.OUT) #
        GPIO.setup(6, GPIO.IN)   #  guest 
        GPIO.setup(21, GPIO.OUT) # 
        GPIO.setup(13, GPIO.IN)  #  schlafen 
        GPIO.setup(16, GPIO.OUT) # 
        print ("Adding event for GPIO 26 & 6")
        GPIO.add_event_detect(26, GPIO.RISING, callback=lambda x, i=26, l=20: callback_GPIO(i,l), bouncetime=1500)
        GPIO.add_event_detect(6, GPIO.RISING, callback=lambda y, i=6, l=21: callback_GPIO(i,l), bouncetime=1500)
        GPIO.add_event_detect(13, GPIO.RISING, callback=lambda z, i=13, l=16: callback_GPIO(i,l), bouncetime=1500)
        print ("done adding event for GPIO 26 an 6")
        # run the event loop
        loop = asyncio.get_event_loop()
        loop.run_forever()
        loop.close()
    except :
        print("Error:", sys.exc_info()[0])
        traceback.print_exc()
    finally:
    # cleanup
        GPIO.cleanup()
