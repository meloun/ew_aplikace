import sys
import pandas as pd
import requests
import json

'''
u'category', u'cell', u'club', u'email', u'first_name', u'id', u'lap1',
u'lap2', u'lap3', u'lap4', u'name', u'nr', u'o1', u'o2', u'o3', u'o4',
u'order1', u'order2', u'order3', u'points1', u'points2', u'points3',
u'points4', u'points5', u'sex', u'start_nr', u'state', u'status',
u'time1', u'time2', u'time3', u'time4', u'timeraw', u'un1', u'un2',
u'un3', u'us1', u'year'
'''


#url = "https://portal.fsczech.cz/api/acceleration"
#url = "https://portal.fsczech.cz/api/skidpad"
url = "https://portal.fsczech.cz/api/autocross"
#url = "https://portal.fsczech.cz/api/endurance"
#url = "https://portal.fsczech.cz/api/trackdrive"

print "I: Script: START - "

# Retrieve arguments passed from the calling script
#print utDf

 # string json to df
exportDf = pd.read_json(utDf)
exportJSON = {"times": [] }

# filter
exportDf["number"] = exportDf.o4
exportDf["season_id"] = 4
exportDf =  exportDf[ ["id", "number", "time1","season_id"] ]     
exportDf = exportDf[exportDf["time1"].notnull()]

times_string = exportDf.to_json(orient="records")
timesJSON = json.loads(times_string)
#print times_json, type(times_json)      
exportJSON["times"] =  timesJSON                    
#print "USEREXPORT: now", export
auth_token='1|71j4X5ae7j9kfLkfhJaxMc9neKsgDpw0jVIuYN7Qa689166f'
headers = {'Authorization': 'Bearer '+auth_token}
#print headers
response = requests.post(url, json=exportJSON, headers=headers)
if response.status_code == 200:
    print("I: Script: Request successful -> " + url)
else:
    print("I: Script: Failed with status code:", response.status_code)
    #print("Script export: Response content:", response.text)
#print(response.ok)
print "I: Script: END"        
