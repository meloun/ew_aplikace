# -*- coding: utf-8 -*-
'''
Created on 19.6.2014

@author: Meloun
'''
import pandas as pd





test = pd.Series()
test = dict(test)
#print "tz", test, type(test)

df = pd.DataFrame(columns = ["AA", "BB", "cell"])



df.loc[0]= ["a1", "b", "250"]
df.loc[1]= ["a2", "b", "2"]
df.loc[2]= ["a3", "b", "220"]


print "filter",df[df['cell'].astype(str).str.match('2$')]

df2 = df
print df
df2.loc[0]= ["a1", "b", "251"]
print df2
print df
print "============================================="

# 
# for i in range(0,3):
#     for v,row in df.iterrows():
#         print row
#         
# print "-------------------------------------------------"        
        
        

#print df
#print  df[df['CC'].str.contains("c1|c2")]
#print  df[df['CC'].isin(["c1","c2"])]

from ewitis.gui.TimesStore import TimesStore, timesstore
filter_dict = {'cell':'250'}



               

        
for k,v in filter_dict.iteritems():
    print "kv",k,v, type(k), type(v)        
    aux_df = df[df[k].astype(str).str.contains(v)]
    print aux_df
  

print "!===================================="          
#print df
#
#for s in df.get_values():
#    print s, type(s)
#    
#for index, row in df.iterrows():
#    print index, row, type(row)
#    print row['AA']
    
    
#df = pd.DataFrame([list(s1), list(s2)])
#mycolumns=pd.MultiIndex.from_product([['one','two'], ['first','second']])
#df.columns = mycolumns
print "---"
print df.columns, type(df.columns)
tuples = zip(["AA", "BB", "CC"], ["DD", "EE", "FF"])
#df.columns = pd.MultiIndex.from_tuples(tuples,  names=["a","g"])
df.columns = pd.MultiIndex.from_arrays([["a","g","t"],['ticker','field', "d"]])
print "---"
print df.columns, type(df.columns)
print "---"
df2 = df = pd.DataFrame(df, columns = df.columns)
print df2.columns, type(df.columns)
df2 = df2.reindex()
df2 = df2.reset_index()
print df2.columns, type(df.columns)

print "---"
df.to_csv("testA.csv")

#df = df.append(pd.Series(["a", "b", "c"], index = ["AA", "BB", "CC"]), ignore_index=True)
#df = df.append(["e", "f", "g"])
#df = df.append(["h", "i", "j"])

print df.columns.levels

