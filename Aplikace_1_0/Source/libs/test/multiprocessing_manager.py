'''
Created on 04.08.2015

@author: z002ys1y
'''
import multiprocessing, time, sys
import pandas as pd

NR_ROWS = 10000
i = 0
def getDf():
    global i, NR_ROWS
    myheader = ["name", "test2", "test3"]                
    myrow1 =   [ i,  i+400, i+250]
    df = pd.DataFrame([myrow1]*NR_ROWS, columns = myheader)    
    i = i+1
    return df 

def put_process(mydict):
    print "put_process"
    while(1): 
        data = getDf()                
        mydict["df"] = data
        print "P:", mydict["df"]["name"].iloc[0]              
        sys.stdout.flush()                    
        time.sleep(2)
        
   
    

if __name__ == "__main__":
    mgr = multiprocessing.Manager()
    mgr.daemon = True
    mydict = mgr.dict({"df":pd.DataFrame()})
    
    p = multiprocessing.Process(target=put_process, args=(mydict,))
    
    p.start()
    while(1):
        time.sleep(0.1)
        df = mydict["df"]
        if not df.empty:
            print "T:", df["name"].iloc[0], len(df.index)        

            
    p.join() 