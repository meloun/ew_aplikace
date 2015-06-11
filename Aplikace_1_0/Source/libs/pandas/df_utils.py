'''
Created on 29.05.2015
@author: z002ys1y
'''

def Filter(df, filter):
    '''
    filter dataframe according to pattern        
    '''                                              
    if filter != None:        
        for k,v in filter.iteritems():                
            try:
                #replace
                v = str(v)
                
                if(k == "cell") and (v == "2"):
                    v="2$"                
                v = v.replace("2|", "2$|") #cell=2|250
                v = v.replace(" ", "") #mezery pryc
                
                # filter frame
                df = df[df[k].notnull()]                                                                                                                                                                                                                                                                  
                df = df[df[k].astype(int).astype(str).str.match(str(v))] #convert to int because of float type (3.0)
                       
            except (KeyError):
                print "error: race settings: filter", k, v, filter
                continue
    return df
    
'''
 
'''
def Get(df, nr, filter = None):
    row = {}
    
    #filter
    df = Filter(df, filter)                      

    #find x-th row           
    try:    
        row = df.iloc[nr-1]
        row = dict(row)                        
    except IndexError:
        row = None                        
    return row
 
def GetFirst(filter = None):                    

    return Get(1, filter)       