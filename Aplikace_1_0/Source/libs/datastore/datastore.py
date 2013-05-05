# -*- coding: utf-8 -*-
'''
Created on 29.12.2011

@author: Meloun
'''
from threading import RLock

"""
definice DAT pro DATASTORE
 - přenos dat mezi gui a kommunikací
 - sekce:
     GET: data se pravidelně se obnovují z terminálu
          očekávané hodnoty:
              - refresh_countdown - za jak dlouho se data obnoví z terminálu 
     SET: při změně se data nastavují do terminálu
          očekávané hodnoty:
              - changed - hodnoty se změnili a čekají na odeslání do terminálu
     GET_SET: žádná akce mimo základní metody Datastore
         
    zmáčknutí tlačítka =>
        GUI PART
        - nastaví se nová SET hodnota(a flag changed) a GET na NULL
        - GET hodnota se ale nějákou dobu nesmí aktualizovat, musí držet NULL a čekat na zapsání SET
        - jinak by se přepsal GET starou hodnotou, proto 'refresh_countdown '
        COMMUNICATION PART
        - při poslání do terminálu se maže flag 'changed'
        - při každém cyklu se decrementuje 'refresh_countdown' u dané GET proměnné
          pokud je nulový vyčítá se z terminálu hodnota, ukládá se  
     
"""
DEF_DATA = {
               
        # GET_SET, LOKÁLNÍ DATA (neposílájí se do terminálu)
        "port_enable"        : {"name"   : "Port enable",
                                "GET_SET"  : {"value": False}
                               },
        # SET - flag 'changed' nutný!
        "backlight"          : {"name"    : "backlight",                                                                 
                                "SET"     : {"value": 0x01, 
                                             "changed": True,                                             
                                             },
                               },
        # GET - 'refresh_coutndown' nutný!
        "terminal_info"      : {"name"    : "terminal info",
                                "GET"     : {"value": {"number_of_cells": None,
                                                       "battery": None,
                                                       "backlight":  None,
                                                       "speaker": {"keys": None, "timing": None, "system":None},
                                                       "language": None,
                                                       "datetime": {"year":1999, "month":8, "day":13, "hour":15, "minutes":5, "seconds":7, "dayweek":5}
                                                       },
                                             "refresh_coutndown": 0                                              
                                             },
                                },
            }
        
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
        
        self.datalock = RLock(False)
        
        self.REFRESH_COUNTDOWN = 0x01
    
    def ResetValue(self, name, key1 = None, key2 = None):
        '''
        only for GET section
        set value to None
        set refresh countdown => GET hodnota se neobnoví hned, ale až po odpočítání countdown 
        '''
        if(key1 and key2):
            self.data[name]['GET']['value'][key1][key2] = None
        elif(key1):
            self.data[name]['GET']['value'][key1] = None
        else:
            self.data[name]['GET']['value'] = None
            
        self.data[name]['GET']['refresh_countdown'] = self.REFRESH_COUNTDOWN                                
    
    def IsReadyForRefresh(self, name):
        """
        jen pro GET section
        """
        if(self.data[name]['GET']['refresh_countdown'] == 0x00):
            return True
        
        self.data[name]['GET']['refresh_countdown'] = self.data[name]['GET']['refresh_countdown'] - 1            
        return False

    
    """
    SET DATA
    
    - metoda Set() nastaví hodnotu a případně také flag na obsloužení
    - metodou isflaged() lze otestovat, zda je požadováno obsloužení(např. vyslání do terminálu)
    - metodou Get() se získají data pro obsluhu
    - metodou resetFlags() se flag smaže, volá se po obsloužení    
    """    
    def Set(self, name, value, section = "GET_SET"):
        '''
        Nastaví proměnnou typu "section" a flagy "flags" 
        '''
        
        if(name in self.data) and (section in self.data[name]):
             
            #data exist, section exist (GET, SET, ..)
                        
            self.datalock.acquire()   
                     
            #set data            
            self.data[name][section]["value"] = value            
            
            '''set flag "changed" for section SET'''
            if (section == "SET"):
                self.data[name][section]['changed'] = True
            
            self.datalock.release() 
            
        return None
    
    """
    SET ITEM
    
    - metoda Set() nastaví hodnotu a případně také flag na obsloužení
    - metodou isflaged() lze otestovat, zda je požadováno obsloužení(např. vyslání do terminálu)
    - metodou Get() se získají data pro obsluhu
    - metodou resetFlags() se flag smaže, volá se po obsloužení    
    """    
    def SetItem(self, name, keys, value, section = "GET_SET"):
        '''
        Nastaví proměnnou typu "section" a flagy "flags"             
        '''
                       
        item = self.data[name][section]["value"]
    
        for key in keys[:-1]:          
            if key in item:                
                item = item[key]                

        self.datalock.acquire() 
        
        #set data          
        item[keys[-1]] = value        
        
        #set flag "changed" for section SET
        if (section == "SET"):
            self.data[name][section]['changed'] = True
        if (section == "GET_SET"):
            if 'changed' in self.data[name][section]:
                self.data[name][section]['changed'] = True
            
        self.datalock.release() 
    
        return None
        
    
    def ResetChangedFlag(self, name):
        """
        Jen pro SET section
        Vynuluje flag 'changed'
        volá se po provedení reakce na změnu, typicky poslání do terminálu  
        """
        if 'GET_SET' in self.data[name]:
            self.data[name]['GET_SET']['changed'] = False
        else:
            self.data[name]['SET']['changed'] = False
        
    def IsChanged(self, name):
        """
        Jen pro SET section                
        slouží ke zjištění zda nastala změna, flag "changed" == True  
        """
        if 'GET_SET' in self.data[name]:
            return self.data[name]['GET_SET']['changed']           
        return self.data[name]['SET']['changed']          
               
    
    """
    GET DATA
    - zapis je nutný pomocí metody SET()
    - GET vrací data zapsaná v dané sekci    
    """    
    def Get(self, name, section = "GET_SET"):
        '''
        Vrací data
        '''            
        if(name in self.data) and (section in self.data[name]):
            #reset flags                                
            return self.data[name][section]["value"]
        return None
    """
    GET DATA
    - zapis je nutný pomocí metody SET()
    - GET vrací data zapsaná v dané sekci    
    """    
    def GetItem(self, name, keys, section = "GET_SET"):
        '''
        Vrací data
        '''            
        #print name, section
        item = self.data[name][section]["value"]
    
        for key in keys:          
            if key not in item:
                return None
            item = item[key]                

        return item
    
    """
    GET DATA
    - zapis je nutný pomocí metody SET()
    - GET vrací data zapsaná v dané sekci    
    """    
    def GetName(self, name):
        '''
        Vrací data
        '''            
        if(name in self.data):
                #reset flags                                
                return self.data[name]["name"]
        return None
                      
    
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

        