'''
Created on 17.08.2015

@author: z002ys1y
'''

import pandas as pd
df = pd.DataFrame({'A': {0: 'a', 1: 'b', 2: 'c'},
                   'B': {0: 1, 1: 3, 2: 5},
                   'C': {0: 2, 1: 4, 2: 6}})

print df

print pd.melt(df, id_vars=[('A', 'C')], value_vars=[('B', 'C')])

