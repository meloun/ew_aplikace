'''
Created on 10.12.2013

@author: z002ys1y
'''
class Singleton(object):     
    def __new__(cls,*dt,**mp): 
        print "new"       
        if not hasattr(cls,'_inst'):
            cls._inst = super(Singleton, cls).__new__(cls,dt,mp)
        elif(dt!=() or mp!={}):
            print "E: Singleton: Init already done", cls, dt, mp            
            def init_pass(self,*dt,**mp):pass
            cls.__init__ = init_pass
        print "a"    
        return cls._inst.__call__
    
class MyClass(Singleton):    
    def __init__(self, a):
        self.a = a
        print "init", a
        
        
if __name__ == '__main__':
    
    dva = MyClass(2)
    tri = MyClass()
    

