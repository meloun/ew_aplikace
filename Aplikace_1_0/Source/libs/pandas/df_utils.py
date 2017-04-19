'''
Created on 29.05.2015
@author: z002ys1y
'''
import pandas as pd

def Filter(df, filter):
    '''
    filter dataframe according to pattern {"cell":"2|250";"lap":"2|4"}        
    '''                                                  
    if filter != None:        
        for k,v in filter.iteritems():                
            try:
                
                if(isinstance(v, int)):
                    df = df[df[k].notnull()]                                                                                                                                                                                                                                                                  
                    df = df[df[k] == v]                    
                else:                                    
                    #replace                
                    v = str(v)
                    
                    #if(k == "cell") and (v == "2"):
                    #    v="2$"                
                    v = v.replace("2|", "2$|") #cell=2|250
                    v = v.replace(" ", "") #mezery pryc
                    
                    v = v+"$"
                    #print "kv", k, v
                    
                    # filter frame
                    df = df[df[k].notnull()]                                                                                                                                                                                                                                                                  
                    df = df[df[k].astype(int).astype(str).str.match(v)] #convert to int because of float type (3.0)
                       
            except (KeyError):
                print "error: race settings: filter", k,":",v,"-", filter
                continue
    return df


"""
Filter dataframe
- filter out all rows with empty columns
"""
def FilterEmptyColumns(df, columns):
         
    columns = [x for x in columns if x in df.columns]       
    
    if(len(columns) == 1):                
        df =  df[df[columns[0]] != ""]
        df =  df[df[columns[0]].notnull()]
        
    elif(len(columns) == 2):
        df =  df[(df[columns[0]] != "") | (df[columns[1]] != "")]
        df =  df[(df[columns[0]] != None) | (df[columns[1]] != None)]
        
    return df

"""
ExportToCsvFile
- export dataframe to csv file
"""
def WriteToCsvFile(filename, df, firstline = ['',''], secondline = ['','']):
    length = len(df.columns)
    
    if(length != 0):                   
        
        if (secondline == None):
            if (firstline != None):
                firstline =  [firstline[0],] + ((length-2) * ['',]) + [firstline[1],]                                                                       
                pd.DataFrame([firstline]).to_csv(filename, ";", index = False, header = None, encoding = "utf8")
        else:
            firstline =  [firstline[0],] + ((length-2) * ['',]) + [firstline[1],]
            secondline = [secondline[0],]+ ((length-2) * ['',]) + [secondline[1],]                                                                      
            pd.DataFrame([firstline, secondline]).to_csv(filename, ";", index = False, header = None, encoding = "utf8")
        
        df.to_csv(filename, ";", mode="a", index = False, encoding = "utf8", float_format = "%g", decimal = ',')                
    
    
    
'''
 
'''
def Get(df, nr, filter = None):
    row = {}

    if nr == None:
        return None
    
    #filter
    df = Filter(df, filter)                      

    #find x-th row           
    try:    
        row = df.iloc[nr-1]
        row = dict(row)                        
    except IndexError, TypeError:
        row = None                        
    return row
 
def GetFirst(filter = None):                    

    return Get(1, filter)       