'''
Created on 20.08.2015

@author: z002ys1y
'''
import pandas as pd
import numpy as np

df1 = pd.DataFrame({'id': [1, 2, 5], 'int2': [1, 2, 5], 'int3': [1, 2, 5], 'float': [np.nan, np.nan, np.nan]})
mydict = {'id': 1, 'int2': 5}

mydf = pd.DataFrame([mydict])

dfRow = df1.loc[mydf.id]

mydf.index = dfRow.index







print mydf
print "---------"
print mydf.dtypes
print "---------"
print type(mydf)
print "---------"

print "---------"
print dfRow
print "---------"
print dfRow.dtypes
print "---------"
print type(dfRow)
print "---------"

dfRow.update(mydf)

print "---------"
print dfRow
print "---------"
print dfRow.dtypes
print "---------"
print type(dfRow)
