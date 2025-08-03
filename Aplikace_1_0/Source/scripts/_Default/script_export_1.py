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


print "I: Script 1: START"

# Retrieve arguments passed from the calling script
#print utDf

 # string json to df
exportDf = pd.read_json(utDf)
exportJSON = {"times": [] }

# filter
exportDf["number"] = exportDf.o4
exportDf["season_id"] = 4
exportDf = exportDf[exportDf["lap1"].notnull()]
exportDf["lap"] = exportDf.lap1.astype(int).astype(str)
exportDf =  exportDf[ ["id", "number", "time1", "lap","season_id"] ]     


times_string = exportDf.to_json(orient="records")
timesJSON = json.loads(times_string)
#print timesJSON, type(timesJSON)      
exportJSON["times"] =  timesJSON 

#=======================================================================
# RESET: PRO SMAZANI VSECH ZAZNAMU NA WEBU SMAZAT ZNAK # NA NASLEDUJICI RADCE
#======================================================================= 
#exportJSON["times"] = [{}] 
                

print "I: Script 1: END"        
