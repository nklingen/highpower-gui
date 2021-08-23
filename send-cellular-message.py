from Hologram.HologramCloud import HologramCloud
import time

import csv
import json
import psutil
import os, signal
from subprocess import check_output


def run_network_disconnect():
    print("hello")
    print('Checking for existing PPP sessions')
    for proc in psutil.process_iter():

        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except:
            print("failed")
    
        print(proc.cmdline())
        if 'send-cellular-message.py' in proc.cmdline() or "ppd" in proc.name():

            print('Found existing PPP session on pid: %s' % proc.pid)
            

            
            #this_process = os.getpgid(0)
            #process.kill()
            print(str(os.getpid()) + " "+ str(proc.pid))
            if ((int(proc.pid)-int(os.getpid())) != 0):
                print('Killing pid %s now' % proc.pid)
                process = psutil.Process(int(proc.pid))
                process.kill()
                #os.system('sudo kill -9 {pid}'.format(pid=proc.pid))


# ----------- Connect to network -------------
hologram = HologramCloud(dict(), network='cellular') #Create hologram object

print("try connection")
run_network_disconnect() #Make sure there are no other network connections in process
result = hologram.network.connect()

#hologram.network.disconnect()


if result == False:
    print (' Failed to connect to cell network')

# ---------------------------------------------


while(True):
    print("In while true")
    
    data = {} #Initalize variables to send


    # ----------- Read from file -------------
    with open('values.csv', newline='') as File:  
        reader = csv.reader(File)
        for row in reader:
            listdata=row
        
        for x,element in enumerate(listdata):
            data["group"+str(x+1)] = element

    # ---------- Send data package -----------
    try:
        print(data)
        response_code = hologram.sendMessage(str(data))
        print (hologram.getResultString(response_code)) # Prints 'Message sent successfully'.

    except:
        #Re-establish connection
        run_network_disconnect()
        hologram = HologramCloud(dict(), network='cellular') #Create hologram object
        result = hologram.network.connect() #Connect to network

        #Try and send data once again
        print(data)
        response_code = hologram.sendMessage(str(data))
        print (hologram.getResultString(response_code)) # Prints 'Message sent successfully'.


    time.sleep(3600) #Sleep for an hour
    #time.sleep(20)



