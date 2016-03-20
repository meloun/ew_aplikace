'''
Created on 13. 3. 2016

@author: Meloun
'''
import time
def funcA1():
    print "func A1"
def funcA2():
    print "func A2"
def funcA3():
    print "func A3"
def funcB(nr):
    print "func BB", nr+1    
def funcB1():
    print "func B1"
def funcB2():
    print "func B2"        
def funcB3():
    print "func B3"
def funcC1():
    print "func C1"
def funcC2():
    print "func C2"
def funcC3():
    print "func C3"
    
if __name__ == "__main__":    
    print "slot tasking"
       
    idx = idx_a = idx_b = idx_c = 0         
    SLOT_A = [funcA1, funcA2, funcA3, None]
    SLOT_B = [funcB1, lambda: funcB(idx_b),  None]
    SLOT_C = [funcC1, funcC2, funcC3]
    LeastCommonMultiple = len(SLOT_A) * len(SLOT_B) * len(SLOT_C) 
    print "LCM:", LeastCommonMultiple
    
    for i in range(0,100):
        time.sleep(0.1)        
        
        """calling run functions"""        
        '''slot A'''
        print "-",idx,"-"
        idx_a = idx % len(SLOT_A)                                                
        if idx_a != len(SLOT_A)-1:                        
            SLOT_A[idx_a]()            
        else:
            '''slot B''' 
            idx_b = (idx / len(SLOT_A)) % len(SLOT_B) 
            if idx_b != len(SLOT_B)-1:                                                          
                SLOT_B[idx_b]()
            else:
                '''slot C'''
                idx_c = (idx / len(SLOT_A) / len(SLOT_B)) % len(SLOT_C)                                                   
                SLOT_C[idx_c]()

        idx = idx + 1   
        if(idx == LeastCommonMultiple):
            idx = 0                             
                    