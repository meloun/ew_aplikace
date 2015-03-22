'''
Created on 14.3.2014

@author: Meloun
'''
import pandas as pd
import numpy as np
from numpy.random import randn
from ewitis.data.db import db
import pandas.io.sql as psql    
from pysqlite2 import dbapi2 as sqlite


df = pd.DataFrame({'A' : ['fodo', 'bsar', 'foo', 'bar',
                       'foo', 'bar', 'foo', 'foo'],
                   'B' : ['1', '2', '3', '4',
                       '5', '6', '7', '8'],
                   })

print df

grouped = df.groupby('A')




for a, group in grouped:
    print group.drop('A', 1)
    
print grouped.get_group('foo')

#print grouped.last()


#print grouped.size()
#print len(grouped)
#print grouped.last()


#print grouped.agg(np.count)

# 
# print grouped.get_group('foo') #.reset_index()
# print grouped.get_group('bar') #.reset_index()
# 
# print type(grouped.get_group('foo'))
# print dict(grouped.get_group('foo').iloc[0])
# print grouped.get_group('foo').iloc[0]
# print dict(grouped.get_group('foo').iloc[1])
# print dict(grouped.get_group('foo').iloc[2])
# print dict(grouped.get_group('foo').iloc[3])
# print dict(grouped.get_group('foo').iloc[4])
# #print grouped
# #for name, group in grouped:
# #    print name
# #    print group
# 
# 
# #groub by v SQL
# #df2a = psql.read_frame('select * from times', db.getDb())
# #df2 = psql.read_frame('select * from times ORDER BY times.time ASC', db.getDb())
# #print "df2a", df2a
# #print "df2", df2


