# -*- coding: utf-8 -*-


if __name__ == "__main__":
    from ewitis.data.db import db
    import pandas as pd
    import pandas.io.sql as psql    
    from pysqlite2 import dbapi2 as sqlite

    # Create your connection.    
    cnx = sqlite.connect("db/test_db.sqlite", 5)  
    df1 = psql.read_frame('select * from times', cnx)
    print df1, type(df1)
    
    #exiting connection
    df2 = psql.read_frame('select * from times', db.getDb())
    print df2, type(df2)
                     
    #max
    print "max", df1["time"].max()
    print "max", df2["time"].max()
    
    #sorting
    Sorted = df1.sort(['time'], ascending = False)
    print Sorted, type(Sorted)
    #print Sorted.head(3) #first X rows
    Sorted = df2.sort(['time'], ascending = False)
    #print Sorted, type(Sorted)
    print Sorted.head(3) #first X rows
    
    idx = df1[df1['user_id']==1]['id'].argmax()
    print  df1[df1['user_id']==1]['id']
    print "idx", idx
    
    #cyklus
    #for index, row in df1.iterrows():
    #    print row, "tyoee",type(row)
    
    #podle indexu
    #print df1.loc[1], "tyoee2", type(df1.loc[1])
    
    #graf
    #print df1['time'].plot(kind='bar')
    
    print df1
    print "groupby", df1.groupby('run_id')
    
    df1.groupby('run_id')[run_id=6]
    
    for item in df1.groupby('run_id'):
        print "user"
        print item
    
    #df = pd.DataFrame(data=list(result), columns=result.keys())
    #print df
#    import numpy as numpy
#    df = pd.DataFrame(numpy.random.randn(5,2),index=range(0,10,2),columns=list('AB'))
#    print df
#    print "max"
#    print df['A'].argmax()
#    print "loc"
#    print df.loc[df['A'].argmax()]
#    
