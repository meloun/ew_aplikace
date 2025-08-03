# -*- coding: utf-8 -*-
import sys
import pandas as pd
import requests
import json
import time
starttime =  time.time()

'''
PARAMETRY
filename - jmeno tohoto souboru 
utDf - user time dataframe (ale predává se jako string)
u'category', u'cell', u'club', u'email', u'first_name', u'id', u'lap1',
u'lap2', u'lap3', u'lap4', u'name', u'nr', u'o1', u'o2', u'o3', u'o4',
u'order1', u'order2', u'order3', u'points1', u'points2', u'points3',
u'points4', u'points5', u'sex', u'start_nr', u'state', u'status',
u'time1', u'time2', u'time3', u'time4', u'timeraw', u'un1', u'un2',
u'un3', u'us1', u'year'
'''


''' CONFIGURATION '''
conf = { "race": None, "range": None, "delete_all": False, "delete": False, "debug": False }


'''race'''
#conf["race"] = "acceleration-dv"
#conf["race"] = "skidpad-dv"
#conf["race"] = "autocross-dv"
#conf["race"] = "trackdrive"

conf["race"] = "acceleration"
#conf["race"] = "skidpad"
#conf["race"] = "autocross"
#conf["race"] = "endurance"

#conf["race"] = "test_ptsv3"

'''range''' 
conf["range"] = "all"
#conf["range"] = "top5"
#conf["range"] = "empty"

'''PRIO OPERATINs'''
'''normalne vse zakomentovane'''
'''odkomentuj jen jednorazove pri pouziti'''
#1-DELETE ALL - maže všechny záznamy na webu
#conf["delete_all"] = {"category":conf["race"]}
#2-DELETE - maže jeden záznam na webu
#ew_id: id záznamu
#conf["delete"] = {"ew_id": 0, "category":conf["race"]}


'''debug - zapíná výpisy'''
#conf["debug"] = True

''' end of KONFIGURACE '''

if conf["delete_all"] != False:           
    url = "https://portal.fsczech.cz/api/timing-data/delete-all"
elif conf["delete"] != False:
    url = "https://portal.fsczech.cz/api/timing-data/delete"
elif conf["race"] == "acceleration-dv":
    url = "https://portal.fsczech.cz/api/timing-data/acceleration-dv"
elif conf["race"] == "skidpad-dv": 
    url = "https://portal.fsczech.cz/api/timing-data/skidpad-dv"
elif conf["race"] == "autocross-dv":
    url = "https://portal.fsczech.cz/api/timing-data/autocross-dv"
elif conf["race"] == "acceleration":
    url = "https://portal.fsczech.cz/api/timing-data/acceleration"
elif conf["race"] == "skidpad": 
    url = "https://portal.fsczech.cz/api/timing-data/skidpad"
elif conf["race"] == "autocross":
    url = "https://portal.fsczech.cz/api/timing-data/autocross"
elif conf["race"] == "endurance":
    url = "https://portal.fsczech.cz/api/timing-data/endurance"
elif conf["race"] == "trackdrive":
    url = "https://portal.fsczech.cz/api/timing-data/trackdrive"
elif conf["race"] == "test_ptsv3":
    url = "https://ptsv3.com/t/123246549879/"
else:
    print "E: invalid race configuration"
    sys.exit()
    
    
#print "I: Script: " + filename + " -> START"
#print utDf

 # string json to df
exportDf = pd.read_json(utDf)
exportJSON = {"times": [] }

# filter collumns
exportDf["number"] = exportDf.o4
exportDf["driver_id"] = exportDf.o3
exportDf["season_id"] = 5

if conf["race"] in ("acceleration-dv", "acceleration", "autocross-dv", "autocross"):
    exportDf = exportDf[exportDf["time1"].notnull()]
    exportDf =  exportDf[ ["id", "number", "time1","season_id", "timeraw", "driver_id"] ]     
elif conf["race"] in ("skidpad-dv", "skidpad"): 
    exportDf["time1"] = exportDf.time2
    exportDf["time2"] = exportDf.time3
    exportDf = exportDf[exportDf["time2"].notnull()]
    exportDf =  exportDf[ ["id", "number", "time1", "time2", "season_id", "timeraw", "driver_id"] ]     
elif conf["race"] in ("endurance", "trackdrive", "test_ptsv3"):
    exportDf = exportDf[exportDf["lap1"].notnull()]
    exportDf["lap"] = exportDf.lap1.astype(int).astype(str)
    exportDf =  exportDf[ ["id", "number", "time1", "lap","season_id", "timeraw", "driver_id"] ]   
else:
    print "E: invalid race configuration"
    sys.exit()
    

# sort and pick only last times
if conf["range"] == "all":
    pass
elif conf["range"] == "top5":
  exportDf = exportDf.sort_values("timeraw", ascending = False).head(5)
else:
    print "E: invalid range configuration"
    sys.exit()   

times_string = exportDf.to_json(orient="records")
timesJSON = json.loads(times_string)   
exportJSON["times"] =  timesJSON

#print exportJSON, type(exportJSON)  

auth_token='1|71j4X5ae7j9kfLkfhJaxMc9neKsgDpw0jVIuYN7Qa689166f'
headers = {'Authorization': 'Bearer '+auth_token}

if(conf["delete_all"] != False): 
    response = requests.delete(url, json=conf["delete_all"], headers=headers)
elif(conf["delete"] != False): 
    response = requests.delete(url, json=conf["delete"], headers=headers)
else:
    response = requests.post(url, json=exportJSON, headers=headers)

#response code
if response.status_code == 200:
    print "I: " + filename + ": OK -> " + "%.2f s" % (time.time() - starttime)
else:
    print "E: " + filename + ": Failed with status code: " + str(response.status_code)
    
    
    #print("Script export: Response content:", response.text)
#print(response.ok)

