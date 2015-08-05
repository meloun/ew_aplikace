'''
Created on 05.08.2015

@author: z002ys1y
'''
import multiprocessing
import time

def worker(d, key, value):    
    d[key] = value
    print d

if __name__ == '__main__':
    mydict = {}
    
    mgr = multiprocessing.Manager()
    d = mgr.dict(mydict)
    
    mydict["keyA"] = 55
    d = mgr.dict(mydict)
    
#     #multiprocessing-dict read
#     ztime = time.clock()
#     for i in range(0,100000):
#         a = d[i%3]
#     print "multiprocessing: read:", time.clock() - ztime,"s"
#     
#     
#     #buildin-dict read
#     ztime = time.clock()
#     for i in range(0,100000):
#         a = mydict[i%3]
#     print "buildin: read:", time.clock() - ztime,"s"
#         
# 
#     
#     
#     #multiprocessing-dict read
#     ztime = time.clock()
#     for i in range(0,100000):
#         d[i%3] = i%3
#     print "multiprocessing: write:", time.clock() - ztime,"s"
#         
#     #buildin-dict read
#     ztime = time.clock()
#     for i in range(0,100000):
#         mydict[i%3] = i%3 
#     print "buildin: write:", time.clock() - ztime,"s"
        

        
    
#     
    jobs = [ multiprocessing.Process(target=worker, args=(d, i, i*2))
             for i in range(10) 
             ]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    print 'Results:', d
    print 'source', mydict