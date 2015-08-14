'''
Created on 12.08.2015

@author: z002ys1y
'''
import pandas as pd
import numpy as np 
df = pd.DataFrame({'vals': [1, 2, 3, np.nan], 'ids': ['a', 'b', np.nan, 'n'], 'ids2': ['a', 'n', np.nan, np.nan]})

#print df
df["ids2"] = df.ids2.replace(np.nan, 68)
#print df


df = pd.DataFrame({'A': [1, 2, 3],'B': [np.NaN, np.NaN, np.NaN]})
print df
df.loc[df.B.isnull(), "B"] = 68
print df