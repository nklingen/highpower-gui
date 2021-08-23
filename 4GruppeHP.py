import RPi.GPIO as GPIO
import datetime
import time
import board
import busio
import adafruit_ina260
import pigpio
import sys
import csv
from collections import deque

def water_switch(current_switch, target_val):
    if current_switch == 1:
        target_val = 0
    return target_val
    
def update_duty_cycle(duty_val, current_val, target_val):
    if int(current_val) < int(target_val) :
        duty_val += 0.01
    elif int(current_val) > int(target_val) :
        duty_val -= 0.01

    # Duty max is 100 and min is 0
    if duty_val <= 0  :
        duty_val = 0  
    elif duty_val >= 100 :
        duty_val = 100
    
    # If the target value has been changed to 0  immediately change duty to 0
    if int(target_val) == 0 :
        duty_val = 0
        
    return duty_val

def run(mv1,mv2,mv3,mv4):

    queue1 = deque()
    queue2 = deque()
    queue3 = deque()
    queue4 = deque()
    #test connection with screen
    # f = open("demofile2.txt", "a")
    # f.write(mv1)
    # f.write(mv2)
    # f.write(mv3)
    # f.write(mv4)
    # f.close()

    #_____________________________________________________________________________________________
    # Setup

    # Initialize voltage sensors
    i2c = busio.I2C(board.SCL, board.SDA)
    ina260_1 = adafruit_ina260.INA260(i2c, address = 0x40)
    ina260_2 = adafruit_ina260.INA260(i2c, address = 0x41)
    ina260_3 = adafruit_ina260.INA260(i2c, address = 0x44)
    ina260_4 = adafruit_ina260.INA260(i2c, address = 0x45)

    # Initialize dokument for logbook
    date = datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
    file = open("Watchdog.txt", "w")
    file.write(str("Out of range from " + date))
    file.flush()

    # Tell the library which pin nunbering system you are going to use
    GPIO.setmode(GPIO.BCM)

    # Initialize pwm pins
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    
    # Initialize switch pins
    switch1 = GPIO.setup(17, GPIO.IN)
    switch2 = GPIO.setup(27, GPIO.IN)
    switch3 = GPIO.setup(22, GPIO.IN)
    switch4 = GPIO.setup(10, GPIO.IN)

    # Initialize variables 
    duty1 = 0
    duty2 = 0
    duty3 = 0
    duty4 = 0

    i = 0
    log_state = 1
    prev_log_state = 1

    # Initialize Gruppe 1
    tagtet_voltage1 = (mv1)
    Gruppe1 = GPIO.PWM(12, 1000)
    Gruppe1.start(duty1)

    # Initialize Gruppe 2
    tagtet_voltage2 = (mv2)
    Gruppe2 = GPIO.PWM(13, 1000)
    Gruppe2.start(duty2)

    # Initialize Gruppe 3
    tagtet_voltage3 = (mv3)
    Gruppe3 = GPIO.PWM(19, 1000)
    Gruppe3.start(duty3)

    # Initialize Gruppe 4
    tagtet_voltage4 = (mv4)
    Gruppe4 = GPIO.PWM(16, 1000)
    Gruppe4.start(duty4)

    #_____________________________________________________________________________________________
    # Tanks Are runnng
    while 1:
        
        # Group 1
        tagtet_voltage1 = water_switch(GPIO.input(17), tagtet_voltage1)
        duty1 = update_duty_cycle(duty1, ina260_1.voltage*1000, tagtet_voltage1)
        Gruppe1.ChangeDutyCycle(duty1)
        
        # Group 2
        tagtet_voltage2 = water_switch(GPIO.input(27), tagtet_voltage2)
        duty2 = update_duty_cycle(duty2, ina260_2.voltage*1000, tagtet_voltage2)
        Gruppe2.ChangeDutyCycle(duty2)
        
        # Group 3
        tagtet_voltage3 = water_switch(GPIO.input(22), tagtet_voltage3)
        duty3 = update_duty_cycle(duty3, ina260_3.voltage*1000, tagtet_voltage3)
        Gruppe3.ChangeDutyCycle(duty3)
        
        # Group 4
        tagtet_voltage4 = water_switch(GPIO.input(10), tagtet_voltage4)
        duty4 = update_duty_cycle(duty4, ina260_4.voltage*1000, tagtet_voltage4)
        Gruppe4.ChangeDutyCycle(duty4)

        #______________________________________________________________________________________________
        # Watchdog (Only for gruppe 1)

    
        if ina260_1.voltage*1000 > int(tagtet_voltage1)-100 and ina260_1.voltage*1000 < int(tagtet_voltage1)+100 :
            log_state = 0
        else:
            log_state = 1
            

        if log_state != prev_log_state :
            date = datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
            if log_state == 0 :
                file.write(str(" to " + date) + '\n')
                file.flush()
            elif log_state == 1 :
                file.write(str("Out of range from " + date))
                file.flush()

        prev_log_state = log_state
        #_____________________________________________________________________________________________
        
        # update last 50 values
        queue1.append(int(ina260_1.voltage))
        queue2.append(int(ina260_2.voltage))
        queue3.append(int(ina260_3.voltage))
        queue4.append(int(ina260_4.voltage))

        if len(queue1) > 50:
            queue1.popleft() #O(1) performance
            queue2.popleft() #O(1) performance
            queue3.popleft() #O(1) performance
            queue4.popleft() #O(1) performance


        # After 1000 loops update the csv file
        i = i + 1
        if i == 1000:
            
            avg_1 = sum(queue1)/50
            avg_2 = sum(queue2)/50
            avg_3 = sum(queue3)/50
            avg_4 = sum(queue4)/50


            i = 0  
            # open the file in the write mode
            f = open('values.csv', 'w')
            # create the csv writer
            writer = csv.writer(f)
            # write a row to the csv file
            writer.writerow(avg_1*1000, avg_2*1000,avg_3*1000,avg_4*1000)
            # close the file
            f.close()


if __name__ == '__main__':
    run(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])