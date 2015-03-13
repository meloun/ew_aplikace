# -*- coding: utf-8 -*-
'''
Created on 19.6.2014

@author: Meloun
'''
import pandas as pd





test = pd.Series()
test = dict(test)
#print "tz", test, type(test)

df = pd.DataFrame(columns = ["id", "AA", "BB", "cell"])



df.loc[0]= [1, "a1", "b", 250]
df.loc[1]= [2, "a2", "b", 2]
df.loc[2]= [3, "a3", "b", 220]

df2 = pd.DataFrame(columns = ["id", "CC", "BB", "cell"])

df2.loc[0]= [1, "cc1", "b", 250]
df2.loc[1]= [2, "cc2", "b", 2]
df2.loc[2]= [3, "cc3", "b", 220]

left = pd.DataFrame ({'id1': [1, 2, 3], 'key2': ['one', 'two', 'three'], 'lval': [1, 2, 3]})
right = pd.DataFrame({'id2': [3, 2, 1], 'key2': ['one', 'three', 'two'], 'rval': [4, 5, 6]})




#print "filter",df[df['cell'].astype(str).str.match('2$')]

# df2 = df
# print df
# df2.loc[0]= ["a1", "b", "251"]
# print df2

#print left
#print right
#c = right.set_index('id')
print "1============================================="
print pd.merge(left,right, left_on='id1', right_on="id2", how="outer")
#print left.update(right)

#print right[['id', 'rval']]

#df0 = pd.concat([left, right[['id', 'rval']]], ignore_index=True)
#df1 = pd.merge(left, right[['id', 'rval']])
#df2 = left.join(right[['id', 'rval']], on=['id'])
#print df0
#print df1
#df_sorted =  df1.sort(["key2","rval"], ascending = [1,0])
#print df_sorted

#import numpy as np
#print (np.where(df.index==2)[0])
#print df_sorted.loc[:2] 




#print df2

#print df[df['cell']<250]
#print df[df['cell'] == 250]

print "2============================================="

# 
# for i in range(0,3):
#     for v,row in df.iterrows():
#         print row
#         
# print "-------------------------------------------------"        
        
#         
# 
# #print df
# #print  df[df['CC'].str.contains("c1|c2")]
# #print  df[df['CC'].isin(["c1","c2"])]
# 
# from ewitis.gui.TimesStore import TimesStore, timesstore
# filter_dict = {'cell':'250'}
# 
# 
# 
#                
# 
#         
# for k,v in filter_dict.iteritems():
#     print "kv",k,v, type(k), type(v)        
#     aux_df = df[df[k].astype(str).str.contains(v)]
#     print aux_df
#   
# 
# print "!===================================="          
# #print df
# #
# #for s in df.get_values():
# #    print s, type(s)
# #    
# #for index, row in df.iterrows():
# #    print index, row, type(row)
# #    print row['AA']
#     
#     
# #df = pd.DataFrame([list(s1), list(s2)])
# #mycolumns=pd.MultiIndex.from_product([['one','two'], ['first','second']])
# #df.columns = mycolumns
# print "---"
# print df.columns, type(df.columns)
# tuples = zip(["AA", "BB", "CC"], ["DD", "EE", "FF"])
# #df.columns = pd.MultiIndex.from_tuples(tuples,  names=["a","g"])
# df.columns = pd.MultiIndex.from_arrays([["a","g","t"],['ticker','field', "d"]])
# print "---"
# print df.columns, type(df.columns)
# print "---"
# df2 = df = pd.DataFrame(df, columns = df.columns)
# print df2.columns, type(df.columns)
# df2 = df2.reindex()
# df2 = df2.reset_index()
# print df2.columns, type(df.columns)
# 
# print "---"
# df.to_csv("testA.csv")
# 
# #df = df.append(pd.Series(["a", "b", "c"], index = ["AA", "BB", "CC"]), ignore_index=True)
# #df = df.append(["e", "f", "g"])
# #df = df.append(["h", "i", "j"])
# 
# print df.columns.levels

