#-*- coding: utf-8 -*-  

import sys
import time
from PyQt4 import QtCore, QtGui
from ewitis.data.dstore import dstore
import ewitis.gui.myModel as myModel
import libs.db_csv.db_csv as Db_csv
import ewitis.gui.DEF_COLUMN as DEF_COLUMN

      
class RaceInfoParameters(myModel.myParameters):
       
    def __init__(self, source):
                                
        #table and db table name
        self.name = "RaceInfo"
        
        #tables
        self.tabUser = source.U  
        self.tabTimes = source.T  
        self.tabCategories = source.C  
        
        #=======================================================================
        # KEYS DEFINITION
        #======================================================================= 
        self.DB_COLLUMN_DEF = DEF_COLUMN.RACE_INFO['database']
        self.TABLE_COLLUMN_DEF = DEF_COLUMN.RACE_INFO['table']
                
        #create MODEL and his structure
        myModel.myParameters.__init__(self, source)                                                                                            
        
        #=======================================================================
        # GUI
        #=======================================================================
        #VIEW   
        self.gui = {}     
        self.gui['view'] = source.ui.RaceInfoProxyView        
        
        #FILTER
        self.gui['filter'] = source.ui.RaceInfoFilterLineEdit
        self.gui['filterclear'] = source.ui.RaceInfoFilterClear
        
        #GROUPBOX #todo move to model
        self.gui['add'] = None
        self.gui['remove'] =  None
        self.gui['export'] = source.ui.RaceInfoExport
        self.gui['export_www'] = None
        self.gui['import'] = None 
        self.gui['delete'] = None
        
        #COUNTER
        self.gui['counter'] = source.ui.RaceInfoCounter
        
        #=======================================================================
        # classes
        #=======================================================================        
        self.classModel = RaceInfoModel                              
        self.classProxyModel = RaceInfoProxyModel
                

class RaceInfoModel(myModel.myModel):
    """
    RaceInfo table
    
    states:
        - race (default)    
        - dns (manually set)
        - dnq (manually set)
        - dnf (manually set)
        - finished (time received)
    
    NOT finally results:
        - only finished
    
    Finally results:
        - finished = with time
        - race + dnf = DNF
        - dns = DNS
        - dnq = DNQ                
    """
    def __init__(self, params):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)        
                            

                
    def getDefaultTableRow(self): 
        category = myModel.myModel.getDefaultTableRow(self)                
        category['name'] = "unknown"        
        return category 
        
    def update(self, parameter=None, value=None, conditions=None, operation=None):
        """
        update model z databaze
          
        update() => update cele tabulky
        update(parameter, value) => vsechny radky s parametrem = value
        update(conditions, operation) => condition[0][0]=condition[0][1] OPERATION condition[1][0]=condition[1][1]                 
        """                
        
        #run_id                
        run_id = self.params.tabTimes.model.run_id
        
        #disable user actions        
        dstore.Set("user_actions", dstore.Get("user_actions")+1)          
                      
        #smazat vsechny radky
        self.removeRows(0, self.rowCount())                                                                                                                                              
        
        row_id = 1
                        
        #row_table = self.db2tableRow(row)
        row_table = {}
        row_table["id"] = row_id
        row_table["name"] = "Run id:"+ str(run_id)
        row_table["startlist"] = self.params.tabUser.getCount()  
        row_table["dns"] = self.params.tabUser.getCount("dns")          
        row_table["finished"] = self.params.tabUser.getCount("finished")
        row_table["dsq"] = self.params.tabUser.getCount("dsq")  
        row_table["dnf"] = self.params.tabUser.getCount("dnf")
        row_table["race"] = self.params.tabUser.getCount("race")              
                                            
        if row_table["startlist"] ==  row_table["dns"] + row_table["finished"] + row_table["dsq"] + row_table["dnf"] + row_table["race"]:
            row_table["check"] = "ok"
        else:
            row_table["check"] = "ko"
            #print row_table["race"], type(row_table["race"])
            
        self.addRow(row_table)
        row_id =  row_id + 1
        
        #categories
        dbCategories = self.params.tabCategories.getDbRows()                      
        for dbCategory in dbCategories:                                                                                            
            
            #row_table = self.db2tableRow(row)
            row_table = {}
            row_table["id"] = row_id
            row_table["name"] = dbCategory["name"]                        
            row_table["startlist"] = self.params.tabUser.getCount(dbCategory = dbCategory)  
            row_table["dns"] = self.params.tabUser.getCount("dns", dbCategory)              
            row_table["finished"] = self.params.tabUser.getCount("finish", dbCategory)
            row_table["dsq"] = self.params.tabUser.getCount("dsq", dbCategory)  
            row_table["dnf"] = self.params.tabUser.getCount("dnf", dbCategory)              
            row_table["race"] = self.params.tabUser.getCount("race", dbCategory)
            
            if row_table["startlist"] ==  row_table["dns"] + row_table["finished"] + row_table["dsq"] + row_table["dnf"] + row_table["race"]:
                row_table["check"] = "ok"
            else:
                row_table["check"] = "ko"                          
                  
            self.addRow(row_table)
            row_id =  row_id + 1                     
        
        #enable user actions                                                                                                                                                                                                           
        dstore.Set("user_actions", dstore.Get("user_actions")-1)
        
        
                    
class RaceInfoProxyModel(myModel.myProxyModel):
    def __init__(self, params):                        
        
        #default proxy-model constructor
        myModel.myProxyModel.__init__(self, params)  
        

# view <- proxymodel <- model 
class RaceInfo(myModel.myTable):
    def  __init__(self, params):                                             
         
        #default table constructor
        myModel.myTable.__init__(self, params)
        
        self.params.gui['view'].sortByColumn(0, QtCore.Qt.AscendingOrder)
        
    #v modelu tahle funkce šahá do db, raceinfo nema tabulku v db        
    def updateDbCounter(self):
        pass
    
        
                            


        
       


        
        
            
            

        
        
    