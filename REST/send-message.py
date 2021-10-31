from Hologram.HologramCloud import HologramCloud
import time
import sys 
import csv
import json
import psutil
import os, signal
from subprocess import check_output
from datetime import datetime

def run_network_disconnect():
    print("hello")
    print('Checking for existing PPP sessions')
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except:
            print("failed")
    
        print(proc.cmdline())
        if 'send-message.py' in proc.cmdline() or "ppd" in proc.name():

            print('Found existing PPP session on pid: %s' % proc.pid)
            print(str(os.getpid()) + " "+ str(proc.pid))
            if ((int(proc.pid)-int(os.getpid())) != 0):
                print('Killing pid %s now' % proc.pid)
                process = psutil.Process(int(proc.pid))
                process.kill()

def send_message(data):
    try:
        # ----------- Connect to network -------------
        hologram = HologramCloud(dict(), network='cellular') #Create hologram object

        print("try connection")
        run_network_disconnect() #Make sure there are no other network connections in process
        print("connect")
        result = hologram.network.connect()


        if result == False:
            print (' Failed to connect to cell network ')


        # ---------- Send data package -----------

        print(data)
        response_code = hologram.sendMessage(str(data))
        print (hologram.getResultString(response_code)) # Prints 'Message sent successfully'.

        hologram.network.disconnect()

        return "OK"
    except:
        return ""

if __name__ == '__main__':
    response_code = ""
    data = json.loads(sys.argv[1])
    
    while response_code!="OK":
        print("test")
        response_code = send_message(data)
        time.sleep(30)






