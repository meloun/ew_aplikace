'''
Created on 04.08.2015

@author: z002ys1y
'''
import multiprocessing, time, sys


NR_ROWS = 8000
i = 0
def getList():
    global i, NR_ROWS                
    myrow1 =   [ i,  i+400, i+250]
    mylist = [myrow1]*NR_ROWS    
    i = i+1
    return mylist 


def f_put_once(q):               
     
    data = getList()                
    q.put(data)
    print "P:", data[0][0]         
    sys.stdout.flush()                    
    time.sleep(0.5)
        
def f_put(q):
    print "f_put start"        
    
    while(1): 
        data = getList()                
        q.put(data)
        print "P:", data[0][0]      
        sys.stdout.flush()                    
        time.sleep(0.5)
                     
      
def f_get(q):                
    data = {}
    
  
    while not q.empty():
        data = q.get()
        print "get"
        
    if data != {}:
        print "G:", data[0][0]
    else:
        print "nothing new"
    return data
        
                                  

    
if __name__ == "__main__":
    mgr = multiprocessing.Manager()
        
    q = multiprocessing.Queue()            
    p = multiprocessing.Process(target=f_put, args=(q,))
    
    
    f_put_once(q)
    f_put_once(q)
    f_put_once(q)
    f_get(q)
    
    
    print "AAA"
    
    p.start()
    while(1):        
        f_get(q)                
        f_get(q)
        f_get(q)
        time.sleep(2)
            
    p.join()    
    