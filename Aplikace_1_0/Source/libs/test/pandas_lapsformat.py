'''
Created on 12.08.2015

@author: z002ys1y
'''
import pandas as pd 

df2 = pd.DataFrame({'id1': [1, 1, 5, 6],'id2': [2, 3, 5, 5], 'lap': [1, 2, 1, 2], 'nr': [2, 2, 3, 3], 'time': [10, 100, 20, 200]})
print df2

df2['colnum'] = df2.groupby('nr').cumcount()+1
df = df2[['lap','nr','time','colnum']]
df = df.pivot(index='nr', columns='colnum')
df.columns = ['{}{}'.format(col, num) for col,num in df.columns]
df = df.reset_index()
print pd.merge(df, df2.drop_duplicates(subset = "nr", take_last = True), on="nr")


    
# mygroupby = df.groupby("nr")
# 
# print "============"
# #print mygroupby.mean()
# 
# for name, group in mygroupby:    
#     #print(name)
#     print group, type(group)    
#     print "============"
#     x =  group[["lap", "time"]].stack()
#     print x, type(x)
#     #print x.reset_index()
#     mydf =  pd.concat([group.iloc[-1][["nr"]], x])
#     #print mydf
#     mydf = mydf.reset_index()
#     #print mydf
#     
#     
#     #print "header", group.iloc[-1], type(group.iloc[-1])
#         
#     #mydf =  pd.concat([group.iloc[-1][["nr"]], group["time"]])
#     #print mydf    
    
    
    


# aux_df = df[df["nr"]==2]
# print "============"
# print aux_df
# aux_df = aux_df["time1"]
# print "============"
# df["time"] = aux_df
# print df
# #print df["time1"].transpose()


