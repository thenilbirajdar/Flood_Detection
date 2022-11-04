import RPi.GPIO as GPIO
import time, sys
GPIO.setmode(GPIO.BOARD)
inpt=16
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