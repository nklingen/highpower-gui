import flask #To create API
from flask import request, jsonify, make_response,json #To format requests from API
import numpy as np
from icecream import ic #Beautiful print statements
import json
import time
import operator
import os
from subprocess import Popen
import csv


app = flask.Flask(__name__)
app.config["DEBUG"] = True #To make debugging easier
p = ""

#Test page
@app.route('/', methods=['GET'])
def home():
    
    return make_response("<h1>Internal API</h1><p>:)</p>",200)

#Api to start Python code that controls cabinet:
@app.route('/StartPython', methods=['POST'])
def StartPython():
    global p
    '''
    To simulate a post request with JSON to the server:
    curl --header "Content-Type: application/json"  --url 0.0.0.0:5001/StartPython --request POST -d '{"gruppe1":"1","gruppe2":"2","gruppe3":"3","gruppe4":"4"}'

    '''
    #Reformatting the json file to fit the ML-model.
    reformat_json = []
    json_data = request.json


    g1 = json_data['gruppe1']
    g2 = json_data['gruppe2']
    g3 = json_data['gruppe3']
    g4 = json_data['gruppe4']

    print(g1,g2,g3,g4)

    p = Popen(['python3', '/home/pi/REST/4GruppeHP.py',g1,g2,g3,g4]) # something long running


    #os.system("python3 4GruppeHP.py "+g1+" "+g2+" "+g3+" "+g4)

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
        p.terminate()
        #os.system("python3 /home/pi/REST/killPython") #out comment this when running in Linux
        return make_response("killed")
    except:
        return make_response("nothing to kill")


    

# Return the values from the values file
@app.route('/RequestValues', methods=['GET'])
def RequestForecast():

    '''
    # To simulate the GET request: http://0.0.0.0:5001/RequestForecast?monitor_id=5201_283_2267
    '''
    
    with open('/home/pi/REST/values.csv','rt')as f:
        data = csv.reader(f)
        txt = ""
        for row in data:
            for value in row:
                txt+=","+value
        txt =  txt[1:]

    return make_response(txt,200)

 

@app.errorhandler(404)
def page_not_found(e):
    return make_response("<h1>404</h1><p>The resource could not be found.</p>", 404)

#Choose port where the API will run. 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

app.run()