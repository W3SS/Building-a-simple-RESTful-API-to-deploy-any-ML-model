

import cherrypy
from engine import predict_1,PreTreatment 
import pandas as pd
from datetime import datetime;
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from flask import Flask, request, jsonify
import h2o
import subprocess 

app = Flask(__name__)

@app.route("/Insurer_ML_Model", methods=["POST"])
def Insurer_ML_Model_Json():
    start = datetime.now()
    entry = request.get_json()
    print(entry)
    newObservation,qte_third,qte_third_etd,qte_all_risk = PreTreatment(entry,carDetails,cities)
    endPreTreatment = datetime.now()
    
    #print(h2o.cluster_info())
    #h2o.cluster_info()
    #delaisPreTreatment = endPreTreatment - start
    
    newObservation=h2o.H2OFrame(newObservation)
    newObservation.col_names = ['YearlyKilometers','ProductLevel','SeniorityAsInsured','Age','LicenseSeniority','Brand',
								'Fuel','Tenant','Price','Horsepower','MaritalStatus','CityPopulation',<...>]  
	
    try : 
        output = rf_Insurer_ML_Model.predict(newObservation[range(0,3),:])
        output1 = str(h2o.as_list(output).values[0])
        output2 = str(h2o.as_list(output).values[1])
        output3 = str(h2o.as_list(output).values[2])
        
    except : output = str(0)
    
    res1 = round(float(output1.replace('[ ','').replace(']','')),2)
    res2 = round(float(output2.replace('[ ','').replace(']','')),2)
    res3 = round(float(output3.replace('[ ','').replace(']','')),2)

    lossratio_third = res1*qte_third
    lossratio_third_etd = res2*qte_third_etd
    lossratio_all_risk = res3*qte_all_risk
    
    print(lossratio_third)
    print(lossratio_third_etd)
    print(lossratio_all_risk)
    
    end = datetime.now()
    delay = fin - deb
    print(delay.microseconds)
    
    output = {"third" : lossratio_third,"third_etendu" : lossratio_third_etd,"all_risk" :lossratio_all_risk}
    
    return(jsonify(third=lossratio_third,third_etendu=lossratio_third_etd,all_risk=lossratio_all_risk))


#Test function to check whether the API is able to respond or not    
@app.route("/predict_1/<int:user_id>", methods=["GET"])
def predict1(user_id):
    start = datetime.now()
    logger.debug("User %s ", user_id)
    res = predict_1(user_id)
    
    end = datetime.now()
    delay = end - start
    return (str(res) + "   execution time (microseconds) :" + str(delay.microseconds))
  
    
@app.route("/exit", methods=["GET"])
def exit():
    cherrypy.engine.exit()
    h2o.shutdown()
    return ("Quit")


def create_app():
    print('App start')
    
    subprocess.Popen("java -jar h2o.jar",shell=True,cwd="/api/lossratio")

    try : 
        (h2o.init());
    except: 
        print('ko')

    global rf_Insurer_ML_Model,carDetails,cities
 
	# loading the random forest, built uphill from the app 
    rf_Insurer_ML_Model = h2o.load_model("/api/lossratio/rf_Insurer_ML_Model")

	# loading opendata
    carDetails = pd.read_csv(filepath_or_buffer="carDetails.csv")
    cities = pd.read_csv(filepath_or_buffer="cities.csv")
	
    print('App ready to respond')    
    
    return app

