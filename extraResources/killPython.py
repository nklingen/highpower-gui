import psutil
import os, signal
import RPi.GPIO as GPIO

# Initialize pwm pins
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)


# Initialize Gruppe 1
Gruppe1 = GPIO.PWM(12, 1000)
Gruppe1.start(0)
Gruppe1.stop()


# Initialize Gruppe 2
Gruppe2 = GPIO.PWM(13, 1000)
Gruppe2.start(0)
Gruppe2.stop()

# Initialize Gruppe 3
Gruppe3 = GPIO.PWM(19, 1000)
Gruppe3.start(0)
Gruppe3.stop()

# Initialize Gruppe 4
Gruppe4 = GPIO.PWM(16, 1000)
Gruppe4.start(0)
Gruppe4.stop()


for proc in psutil.process_iter():
    print(proc.cmdline())
    if '4GruppeHP.py' in proc.cmdline() or "ppd" in proc.name():

        print('Found existing PPP session on pid: %s' % proc.pid)
   
        print(str(os.getpid()) + " "+ str(proc.pid))
        if ((int(proc.pid)-int(os.getpid())) != 0):
            print('Killing pid %s now' % proc.pid)
            process = psutil.Process(int(proc.pid))
            process.kill()
        
