import sys
import psutil
import os


for proc in psutil.process_iter():
    #print (proc.cmdline())
 
    if '/home/pi/REST/master.py' in proc.cmdline() or "master.py" in proc.name():

         print(str(os.getpid()) + " "+ str(proc.pid))
         if ((int(proc.pid)-int(os.getpid())) != 0):
             print('Killing pid %s now' % proc.pid)
             process = psutil.Process(int(proc.pid))
             process.kill()
        

