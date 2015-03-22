'''
Created on 18.03.2015

@author: z002ys1y
'''
import pandas as pd
import numpy as np
from numpy.random import randn
from ewitis.data.db import db
import pandas.io.sql as psql    
from pysqlite2 import dbapi2 as sqlite


df = pd.DataFrame({'A' : ['one', 'one', 'two', 'three','two', 'two', 'one', 'three'],
                'B' : randn(8)})

d = {'one':'Start', 'two':'Start', 'three':'End'}

grouped2 = df.set_index('A').groupby(d)
for group_name, data in grouped2:
    print group_name
    print '---------'
    print data