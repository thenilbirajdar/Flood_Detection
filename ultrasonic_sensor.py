import RPi.GPIO as GPIO
import time,sys
from gpiozero import Buzzer, InputDevice
#rain detectio 
no_rain = InputDevice(4)
def rain():
    return no_rain.is_active
#def buzz_now(iterations):
    #for x in range(iterations):
        #buzz.on()
        #time.sleep(0.1)
        #buzz.off()
        #time.sleep(0.1)
    
#while True:
    #if not no_rain.is_active:
        #print("Its raining - get the washing in!")
        #buzz_now(5)
    #time.sleep(1)














#flow control sensor
def flow_control():
    
    
    GPIO.setmode(GPIO.BCM)
    inpt=23
    GPIO.setup(inpt,GPIO.IN)
    rate_cnt=0
    tot_cnt=0
    time_zero=0.0
    time_start=0.0
    time_end=0.0
    gpio_last=0
    pulses=0
    constant=1.79
    print('Water Flow - Approximate')
    print('Control C to exit')
 
    time_zero = time.time()
    
    while True:
        rate_cnt = 0
        pulses = 0
        time_start = time.time()
        while pulses <= 5:
            gpio_cur = GPIO.input(inpt)
            if gpio_cur != 0 and gpio_cur != gpio_last:
                pulses += 1
            gpio_last = gpio_cur
            try:
                None
            except KeyboardInterrupt:
                print('\nCTRL C - Exiting nicely')
                GPIO.cleanup()
                print('Done')
                sys.exit()
        rate_cnt += 1
        tot_cnt += 1
        time_end = time.time()
    
        print('\nLiters / min', round((rate_cnt * constant)/(time_end-time_start),2), 'approximate')
        print('Total Liters', round(tot_cnt*constant,1))
        print('Time(min & clock)', round((time.time()-time_zero)/60,2), '\t', time.asctime(time.localtime(time.time())),'\n')
        break


 
#GPIO Mode (BOARD / BCM)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT) 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            print(flow_control())
            if not rain():
                print("raining start")
                
                
                GPIO.output(21,GPIO.HIGH)
                
                time.sleep(1)
                
            
            if int(dist) <10:
                
                print ("BUZZER ON")
#                 print(flow_control())
                GPIO.output(21,GPIO.HIGH)
                
                time.sleep(1)
                
            if int(dist) <10 and not rain():
                print("raining as well as distance reach critical situation")
                
                GPIO.output(21,GPIO.HIGH)
                
                time.sleep(5)
                
                
            print ("BUZZER OFF")
            GPIO.output(21,GPIO.LOW)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()