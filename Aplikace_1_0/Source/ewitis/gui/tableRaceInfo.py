# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from ewitis.gui.aTab import MyTab
from ewitis.gui.aTableModel import myModel, myProxyModel 
from ewitis.gui.aTable import myTable
from ewitis.gui.dfTableUsers import tableUsers
from ewitis.gui.dfTableCategories import tableCategories
from ewitis.gui.dfTableRuns import tableRuns
from ewitis.data.dstore import dstore
            
class RaceInfoModel(myModel):
    """
    RaceInfo table
    
    states:
        - race (default)    
        - dns (manually set)
        - dq (manually set)
        - dnf (manually set)
        - finished (time received)
    
    NOT finally results:
        - only finished
    
    Finally results:
        - finished = with time
        - race + dnf = DNF
        - dns = DNS
        - dq = DQ                
    """
    def __init__(self, table):                
        myModel.__init__(self, table)        
                            

                
    def getDefaultTableRow(self): 
        category = myModel.getDefaultTableRow(self)                
        category['name'] = "unknown"        
        return category 
        
    def Update(self, parameter=None, value=None):
        """
        Update model z databaze
          
        Update() => update cele tabulky
        Update(parameter, value) => vsechny radky s parametrem = value
        Update(conditions, operation) => condition[0][0]=condition[0][1] OPERATION condition[1][0]=condition[1][1]                 
        """                                

        #disable user actions        
        dstore.Set("user_actions", dstore.Get("user_actions")+1)          
                      
        #smazat vsechny radky
        self.removeRows(0, self.rowCount())                                                                                                                                              
        
        row_id = 1
                        
        #row_table = self.db2tableRow(row)
        row_table = {}
        row_table["id"] = row_id
        row_table["name"] = "Run id:"#+ str(run_id)
        row_table["startlist"] = 0 #tableUsers.getCount()  
        row_table["dns"] = 0#tableUsers.getCount("dns")          
        row_table["finished"] = 0#tableUsers.getCount("finished")
        row_table["dq"] = 0#tableUsers.getCount("dq")  
        row_table["dnf"] = 0#tableUsers.getCount("dnf")
        row_table["race"] = 0#tableUsers.getCount("race")              
                                            
        if row_table["startlist"] ==  row_table["dns"] + row_table["finished"] + row_table["dq"] + row_table["dnf"] + row_table["race"]:
            row_table["check"] = "ok"
        else:
            row_table["check"] = "ko"        
            
        self.addRow(row_table)
        row_id =  row_id + 1
        
        #categories
        dbCategories = tableCategories.getDbRows()                      
        for dbCategory in dbCategories:                                                                                            
            
            #row_table = self.db2tableRow(row)
            row_table = {}
            row_table["id"] = row_id
            row_table["name"] = dbCategory["name"]                        
            row_table["startlist"] = 0# tableUsers.getCount(dbCategory = dbCategory)  
            row_table["dns"] = 0# tableUsers.getCount("dns", dbCategory)              
            row_table["finished"] = 0# tableUsers.getCount("finish", dbCategory)
            row_table["dq"] = 0# tableUsers.getCount("dq", dbCategory)  
            row_table["dnf"] = 0# tableUsers.getCount("dnf", dbCategory)              
            row_table["race"] = 0# tableUsers.getCount("race", dbCategory)
            
            if row_table["startlist"] ==  row_table["dns"] + row_table["finished"] + row_table["dq"] + row_table["dnf"] + row_table["race"]:
                row_table["check"] = "ok"
            else:
                row_table["check"] = "ko"                          
                  
            self.addRow(row_table)
            row_id =  row_id + 1                     
        
        #enable user actions                                                                                                                                                                                                           
        dstore.Set("user_actions", dstore.Get("user_actions")-1)
        
        
                    
class RaceInfoProxyModel(myProxyModel):
    def __init__(self, params):                                        
        myProxyModel.__init__(self, params)  
        

# view <- proxymodel <- model 
class RaceInfo(myTable):
    def  __init__(self):                                                              
        myTable.__init__(self, "RaceInfo")
    def Init(self):        
        myTable.Init(self)
        self.gui['view'].sortByColumn(0, QtCore.Qt.AscendingOrder)
        
    #v modelu tahle funkce šahá do db, raceinfo nema tabulku v db        
    def updateDbCounter(self):
        pass
    
tableRaceInfo = RaceInfo()
tabRaceInfo = MyTab(tables = [tableRaceInfo,])         
                            


        
       


        
        
            
            

        
        
    