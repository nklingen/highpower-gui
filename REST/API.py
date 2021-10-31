import flask #To create API
from flask import request, jsonify, make_response,json #To format requests from API
import numpy as np
import json
import time
import operator
import os
from subprocess import Popen
import csv
from smbus2 import SMBus
from mysql.connector import MySQLConnection,Error
import psutil

 
app = flask.Flask(__name__)
app.config["DEBUG"] = True #To make debugging easier
p = ""
c = ""
addr = 0x8
directory = os.getcwd()

#Test page
@app.route('/', methods=['GET'])
def home():
    
    return make_response("<h1>Internal API</h1><p>:)</p>",200)

#Api to start Python code that controls cabinet:
@app.route('/StartPython', methods=['POST'])
def StartPython():
    global p
    try:
        with SMBus(1) as bus:
            bus.write_i2c_block_data(addr,204,[]) #Write data to arduino
        
        p.terminate()
        return make_response("killed")

    except:
        print("nothing to kill")
        
    '''
    To simulate a post request with JSON to the server:
    curl --header "Content-Type: application/json"  --url 0.0.0.0:5001/StartPython --request POST -d '{"gruppe1":"1","gruppe2":"2","gruppe3":"3","gruppe4":"4","anlagsnummer":"1234"}'

    '''
    #Reformatting the json file to fit the ML-model.
    reformat_json = []
    json_data = request.json

    print(json_data)


    g1 = json_data['gruppe1']
    g2 = json_data['gruppe2']
    g3 = json_data['gruppe3']
    g4 = json_data['gruppe4']
    g5 = json_data['anlagsnummer']
    print(g1,g2,g3,g4)

    p = Popen(['sudo','python3', directory+'/master.py',g1,g2,g3,g4,g5]) # something long running
 


    return make_response(jsonify(json_data))

#Kills python code that controls cabinet:
@app.route('/StopPython', methods=['POST'])
def StopPython():
    '''
    To simulate a post request with JSON to the server:
    curl --header "Content-Type: application/json"  --url 0.0.0.0:5001/StartPython --request POST -d '{"gruppe1":"1","gruppe2":"2","gruppe3":"3","gruppe4":"4"}'

    '''
    #Reformatting the json file to fit the ML-model.
    

    try:
        with SMBus(1) as bus:
            bus.write_i2c_block_data(addr,204,[]) #Write data to arduino
        
        p.terminate()
        return make_response("killed")

    except:
        return make_response("nothing to kill")

#Kills python code that controls cabinet:
@app.route('/SendData', methods=['POST'])
def SendData():
    global c

    json_data = request.json

    print(json_data)
    '''
    To simulate a post request with JSON to the server:
    curl --header "Content-Type: application/json"  --url 0.0.0.0:5001/StartPython --request POST 
    '''
    try:
        c.terminate()

    except:
        print("No other threads running")

    c = Popen(['sudo','python3', directory+'/send-message.py',str(json_data)]) # run send message
    
    try:
        c.wait(timeout=300) #timeout after 5 minutes = 300 seconds
        response ="OK"
        
        
    except:
        c.kill()
        response = "Error"

    
    return make_response(response)


    

# Return the values from the values file
@app.route('/RequestValues', methods=['GET'])
def RequestValues():

    '''
    # To simulate the GET request: http://0.0.0.0:5001/RequestValues
    '''
    

    cnx = MySQLConnection(user='Guldager', password='GuldagerPassword',
                            host='localhost',
                            database='userValues')

    cursor = cnx.cursor()
    query = "SELECT * FROM RefValues;"
    cursor.execute(query)
    records = str((cursor.fetchall())[0])
    records = records.replace('(','')
    records = records.replace(')','')
    records = records.replace("'",'')
    records = records.replace(" ",'')


    cursor.close()
    cnx.close()
    


    return make_response(records,200)

@app.route('/WriteToDb', methods=['POST'])
def WriteToDb():
    #Retreive data
    json_data = request.json

    g0 = json_data['anlægsnummer']
    g1 = json_data['gruppe1']
    g2 = json_data['gruppe2']
    g3 = json_data['gruppe3']
    g4 = json_data['gruppe4']
    g5 = json_data['reboot_status']



    query = "UPDATE RefInput SET anlægsnummer = %s, ref1 = %s,ref2 = %s,ref3 =%s,ref4 =%s,status=%s; "
    args = (g0,g1,g2,g3,g4,g5)


    cnx = MySQLConnection(user='Guldager', password='GuldagerPassword',
                            host='localhost',
                            database='userValues')
    cursor = cnx.cursor()
    cursor.execute(query,args)

    cnx.commit()


    cursor.close()
    cnx.close()
    return make_response("Updated DB")

@app.route('/GetFromDb', methods=['GET'])
def GetFromDb():  

    cnx = MySQLConnection(user='Guldager', password='GuldagerPassword',
                            host='localhost',
                            database='userValues')

    cursor = cnx.cursor()
    query = "SELECT * FROM RefInput;"
    cursor.execute(query)
    records = str((cursor.fetchall())[0])
    records = records.replace('(','')
    records = records.replace(')','')
    records = records.replace("'",'')
    records = records.replace(" ",'')

    print(records)

    cursor.close()
    cnx.close()
    #records = "ANLÆG123456,-1200,-1000,-700,0,index"

    
    return records


@app.errorhandler(404)
def page_not_found(e):
    return make_response("<h1>404</h1><p>The resource could not be found.</p>", 404)


#Choose port where the API will run. 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

app.run()