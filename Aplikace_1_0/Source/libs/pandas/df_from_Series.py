'''
Created on 3.8.2014

@author: Meloun
'''
import pandas as pd
mydict1 = {"a":"a1","b":"b1"}
mydict2 = {"a":"a2","b":"b2"}
myseries1 = pd.Series( mydict1 )
myseries2 = pd.Series( mydict2)
myseries1.index = ["sl1", "sl2"]


print myseries1
print myseries2

mydf = pd.DataFrame([myseries1, myseries2], columns = ["sl1", "sl2", "sl3"])
print mydf
