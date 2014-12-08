# -*- coding: utf-8 -*-
'''
Created on 19.6.2014

@author: Meloun
'''
import pandas as pd

test = pd.Series()
test = dict(test)
print "tz", test, type(test)

df = pd.DataFrame(columns = ["AA", "BB", "CC"])
df.loc[0]= ["a", "b", "c1"]
df.loc[1]= ["a", "b", "c2"]
df.loc[2]= ["a", "b", "c3"]

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

