import sys
from smbus2 import SMBus
import time
import csv
import json
import mysql.connector
from datetime import datetime
import requests
# defining the api-endpoint 
API_ENDPOINT = "http://0.0.0.0:5001/SendData"

addr = 0x8

def collect_data(cursor,mv):
    try:
        data = {}
        for i in range(4):
            group = {}
            log = []
            query = 'SELECT Date,Ref FROM Log WHERE Gruppe=%s;'
            args = (1,)
            cursor.execute(query,args)
            records = ((cursor.fetchall()))
            for elements in records:
                log_element = {}
                log_element['timestamp'] = elements[0].strftime("%d/%m/%Y %H:%M:%S")
                log_element['potentiale'] = elements[1]
                log.append(log_element)
            group['target'] = mv[i]
            group['log'] = log

            data['group'+str(i+1)] = group
        

        return data
    except:
        return {}

def smbus2(mv1,mv2,mv3,mv4,anlægsnummer):
    mv = [mv1,mv2,mv3,mv4]

    #--------- Write ---------

    quo1 = int(mv1/255)
    rest1 = int(mv1%255)

    quo2 = int(mv2/255)
    rest2 = int(mv2%255)

    quo3 = int(mv3/255)
    rest3 = int(mv3%255)

    quo4 = int(mv4/255)
    rest4 = int(mv4%255)

    try:
        with SMBus(1) as bus:
            bus.write_i2c_block_data(addr,0,[quo1,rest1,quo2,rest2,quo3,rest3,quo4,rest4]) #Write data to arduino
    except:
        print("error with bus")

    #--------- Read ---------

    now = datetime.now()
    lasthour = int(datetime.now().strftime("%H"))#Current hour
    error_happend = False
    send_daily_message = False

    while True:
        time.sleep(30)
        #TODO: add try except
        try:
            with SMBus(1) as bus:

                block = bus.read_i2c_block_data(addr,0,8)
        except:
            print("error with bus")
            block = [-1,-1,-1,-1,-1,-1,-1,-1]
        
        val1 = -(block[0]*255+block[1])
        val2 = -(block[2]*255+block[3])
        val3 = -(block[4]*255+block[5])
        val4 = -(block[6]*255+block[7])


        
        #Write to Database
        query = "UPDATE RefValues SET ref1 = %s,ref2 = %s,ref3 =%s,ref4 =%s; "
        args = (str(val1),str(val2),str(val3),str(val4))

        try:
            cnx = mysql.connector.connect(user='Guldager', password='GuldagerPassword',
                                    host='localhost',
                                    database='userValues')
            cursor = cnx.cursor()
            cursor.execute(query,args)
        except:
            print("database error")
            print(IOError)
      
      
        

        #------------Update the log once every hour-----------
        this_hour = int(datetime.now().strftime("%H"))#Current hour

        if abs(this_hour-lasthour) >= 1: #If the hour changes
            lasthour = this_hour #Update the hourly timer
            hour = int(lasthour.strftime("%H"))
            #Write to the log
            values=[val1,val2,val3,val4]
            date = lasthour.strftime("%Y-%m-%dT%H:%M:%S") #Format date for sql input
            for i in range(4):
                try:
                    query_log = "INSERT INTO Log (Gruppe,Date,Hour,Ref) VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE Date = %s, Ref= %s;"
                    args_log = (i+1,date,hour,values[i],date,values[i])
                    cursor.execute(query_log,args_log)
                except:
                    print("database error")
                    print(IOError)

        #------------Send the log once pr. day-----------
        
        if this_hour == 17 and (not send_daily_message):
    
            #------- Collect Data ------
            data = collect_data(cursor,mv)

            error_message = {}
            error_message['timestamp'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            error_message['code'] = 'HEARTBEAT' #Everything is OK
            error_message['anlage'] = anlægsnummer
            error_message['data'] = data

            try:
                #------- Send message ------
                r = requests.post(url = API_ENDPOINT, json = json.dumps(error_message))
                # extracting response text 
                pastebin_url = r.text
                print(pastebin_url)
                #TODO: #Check if message has been sent, if not try again.
                if (pastebin_url == 'OK') :
                    print("Send daily message")
                    send_daily_message = True #Make sure we dont send the same message mulitple times
                else:
                    print("error")
                    #Try again
            except:
                print("API error")
                print(IOError)

        elif this_hour!=17:
            print("-----reset----")
            send_daily_message = False #reset daily message so that it sends again tomorrow


            
        #-----------Don't reset timer if the ref is outside target-----------

        if ((abs(val1-mv1)>=500) or (abs(val2-mv2)>=500) or (abs(val3-mv3)>=500) or (abs(val4-mv4)>=500)) and not error_happend:
            
            #Then there is a problem after 4 hours of this, seconds = 864000
            if ((datetime.now()-now).total_seconds())>864000:

                #------- Collect Data ------
                data = collect_data(cursor,mv)

                error_message = {}
                error_message['timestamp'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                error_message['code'] = 'ALARM POTENTIALE'
                error_message['anlage'] = anlægsnummer
                error_message['data'] = data
                
                try:
                    #------- Send message ------
                    r = requests.post(url = API_ENDPOINT, json = json.dumps(error_message))
                    # extracting response text 
                    pastebin_url = r.text
                    print(pastebin_url)
                    #TODO: #Check if message has been sent, if not try again.
                    if (pastebin_url == 'OK') :
                        print("JUHU")
                        error_happend = True #Make sure we dont send the same mulitple times
                        now = datetime.now() #Reset timer after error has occured
                    else:
                        print("error")
                        #Try again
                except:
                    print("API error")
                    print(IOError)



    
        #-----------RESET timer if the ref is within target-----------

        else:
            
            now = datetime.now()
            #If I just send an error message, make sure they know everything is running again now

            if error_happend:
                #Send a message that everything is OK

                #------- Collect Data ------
                data = collect_data(cursor,mv)

                error_message = {}
                error_message['timestamp'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                error_message['code'] = 'OK POTENTIALE' #Everything is OK
                error_message['anlage'] = anlægsnummer
                error_message['data'] = data

                try:
                
                    #------- Send message ------
                    r = requests.post(url = API_ENDPOINT, json = json.dumps(error_message))
                    # extracting response text 
                    pastebin_url = r.text
                    print(pastebin_url)
                    #TODO: #Check if message has been sent, if not try again.
                    if (pastebin_url == 'OK') :
                        print("JUHU")
                        error_happend = False #Make sure we dont send the same message mulitple times
                    else:
                        print("error")
                        #Try again
                except:
                    print("API error")
                    print(IOError)

                
        cnx.commit()
        cursor.close()
        cnx.close()

            
            



if __name__ == '__main__':
    smbus2(abs(int(sys.argv[1])), abs(int(sys.argv[2])), abs(int(sys.argv[3])), abs(int(sys.argv[4])), abs(int(sys.argv[5])))
    