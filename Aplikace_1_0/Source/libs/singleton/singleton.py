'''
Created on 10.12.2013

@author: z002ys1y
'''
#exceptions
class Not_initiated_singleton(Exception): pass    
class SingletonWithParams(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonWithParams, cls).__call__(*args, **kwargs)
        elif(args!=() or kwargs!={}):
            print "E: Singleton: Init already done", cls, args, kwargs
            raise Not_initiated_singleton(cls, args, kwargs)        
        return cls._instances[cls]

        

if __name__ == '__main__':    
    class Logger():
        __metaclass__ = SingletonWithParams
        def __init__(self, a):
            self.a = a
            
    class Logger2():
        __metaclass__ = SingletonWithParams
        def __init__(self, a):
            self.a = a
    
        
    s1=Logger(1)    
    s2=Logger()
    
    if(id(s1)==id(s2)):
        print "Same"
    else:
        print "Different"
        
    s3=Logger2(2)    
    s4=Logger2()
    
    if(id(s1)==id(s2)):
        print "Same"
    else:
        print "Different"
        
    print s1.a, s2.a, s3.a, s4.a
        