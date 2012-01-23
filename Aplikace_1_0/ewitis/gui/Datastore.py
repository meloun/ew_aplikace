# -*- coding: utf-8 -*-
'''
Created on 29.12.2011

@author: Meloun
'''

#"""
#DATA
# - přenos dat mezi gui a kommunikací
# - sekce:
#     TERMINAL_GET: data se pravidelně se obnovují z terminálu 
#     TERMINAL_SET: při změně se data nastavují do termiinálu
#     GET_SET: žádná akce mimo základní metody Datastore
#"""
#DATA = {        
#        """ LOKÁLNÍ DATA (neposílájí se do terminálu) """
#        "port_enable"        : {"name"    : "Port enable",
#                               "GET_SET" : {"value": False}
#                               }
#        "port_name"          : {"name"    : "Port name",
#                               "GET_SET" : {"value": "COM5"}
#                               }
#        "port_baudrate"      : {"name"    : "Port baudrate",
#                               "GET_SET" : {"value": 38400}
#                               }        
#
#        """ TERMINAL DATA """
#        "backlight"          : {"name"    : "backlight", 
#                                "SET"     : {"value": False, "request": False},
#                                "GET"     : {"value": False},
#                               },
#        "time"               : {"name"    : "time",
#                                "SET"     : {"value": False, "request": False},
#                                "GET"     : {"value": False},
#                               },                                        
#        "language"           : {"name"    : "language",
#                                "GET"     : {"value": "čeština"},
#                               },                                               
#        "terminal_battery"   : {"name"     : "battery",
#                                "GET"      : {"value": 0},
#                               },                                               
#        "cell0_battery"      : {"name"     : "battery",
#                                "GET"      : {"value": 0},
#                               },
#        "cell1_battery"      : {"name"     : "battery",
#                                "GET"      : {"value": 0},
#                               },
#        "cell2_battery"      : {"name"     : "battery",
#                                "GET"      : {"value": 0},
#                               }, 
#        "cell3_battery"      : {"name"     : "battery",
#                                "GET"      : {"value": 0},
#                               },                                                                 
#        }
class Datastore():
    """
     
    |======|   |======|  =>    |==========|
    | GUI  |   | COMM |  RS232 | TERMINAL |
    |======|   |======|  <=    |==========|
       |           |
     \SET/       /GET\
       |           |
    |==================|
    |     DATASTORE    |
    |==================|
    
          
    """
    def __init__(self, data):
        '''
        Constructor
        '''
        self.data = data

    
    """
    SET DATA
    
    - metoda Set() nastaví hodnotu a případně také request na obsloužení
    - metodou isRequested() lze otestovat, zda je požadováno obsloužení(např. vyslání do terminálu)
    - metodou Get() se získají data pro obsluhu
    - metodou resetRequest() se request smaže, volá se po obsloužení    
    """    
    def Set(self, name, section, value, requests = []):
        '''
        Nastaví proměnnou typu "SET" a flag "changed" 
        '''
        
        if(name in self.data) and (section in self.data[name]): #data exist? section exist? (GET, SET, ..)
                        
            #set data            
            self.data[name][section]["value"] = value            
            
            #set requests
            for request in requests:              
                if(self.data[name][section][request]): #exist request for this section?
                    self.data[name][section][request] = True
            
        return None
        
    def ResetRequest(self, name, section, request):
        """
        Vynuluje request
        volá se po provedení reakce na změnu, typicky poslání do terminálu  
        """
        
        if(name in self.data) and (section in self.data[name]) and (request in self.data[name][section]):
            self.data[name][section][request] = False
    
    def isRequested(self, name, section, request):
        """
        Vrací zvolený request        
        slouží ke zjištění zda nastala nějáká událost, typický změna request "changed"  
        """
        
        if(name in self.data) and (section in self.data[name]) and (request in self.data[name][section]):
            return self.data[name][section][request]
            
        return False
            
    
    """
    GET DATA
    - zapis je nutný pomocí metody SET()
    - GET vrací data zapsaná v dané sekci    
    """    
    def Get(self, name, section):
        '''
        Vrací data
        '''
        if(name in self.data) and (section in self.data[name]):                
                return self.data[name][section]["value"]
        return None
        
#    def GetCounter(self, name):
#        '''
#        Vrací čítač pro danou proměnnou
#        '''
#        section = "GET"
#        
#        if(name in self.get_data) and (section in self.data[name]):
#            return self.get_data[name][section]["counter"]
#        return None
#    
#    def SetCounter(self, name):
#        '''
#        Nastaví čítač na maximum pro danou proměnnou
#        '''        
#        section = "SET"
#        
#        if(name in self.get_data) and (section in self.data[name]):
#            self.get_data[name][section]["counter"] = self.get_data[name][section]["period"]
                
    
if __name__ == "__main__":
    DATA = {
        """
        definice DAT pro DATASTORE
         - přenos dat mezi gui a kommunikací
         - sekce:
             TERMINAL_GET: data se pravidelně se obnovují z terminálu
             TERMINAL_SET: při změně se data nastavují do terminálu
             GET_SET: žádná akce mimo základní metody Datastore
        """
                
        #LOKÁLNÍ DATA (neposílájí se do terminálu)
        "port_enable"        : {"name"    : "Port enable",
                                "GET_SET"  : {"value": False}
                               },                                       

        #TERMINAL DATA
        "backlight"          : {"name"    : "backlight",                                 
                                "GET"     : {"value": False},
                                "SET"     : {"value": False, "changed": False},
                               }                                                                
        }
    datastore = Datastore(DATA)
    print "Data1: ",datastore.data
    print datastore.Get("backlight")
    
    print "t1",datastore.Get("time")
    datastore.Set("time", 56)    
    print "t2",datastore.Get("time")

        