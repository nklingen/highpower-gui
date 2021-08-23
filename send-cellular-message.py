from Hologram.HologramCloud import HologramCloud
import time

import csv
import json

hologram = HologramCloud(dict(), network='cellular')
result = hologram.network.connect()
if result == False:
    print (' Failed to connect to cell network')
 


i=0
while(True):
    
    i+=1
    data = {}
    with open('values.csv', newline='') as File:  
        reader = csv.reader(File)
        for row in reader:
            listdata=row
        
        for x,element in enumerate(listdata):
            data["group"+str(x+1)] = element

    
    print(data)
    response_code = hologram.sendMessage(str(data))
    print (hologram.getResultString(response_code)) # Prints 'Message sent successfully'.

    
    time.sleep(3600)
