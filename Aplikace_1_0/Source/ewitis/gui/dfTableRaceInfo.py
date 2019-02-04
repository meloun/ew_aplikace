# -*- coding: utf-8 -*-
import time
import pandas as pd
import pandas.io.sql as psql 
from PyQt4 import QtCore, QtGui
from ewitis.gui.aTab import MyTab
from libs.myqt.DataframeTableModel import DataframeTableModel, ModelUtils 

from ewitis.gui.dfTable import DfTable
from ewitis.gui.dfTableUsers import tableUsers
from ewitis.gui.dfTableCategories import tableCategories
from ewitis.data.dstore import dstore
            
class DfModelRaceInfo(DataframeTableModel):
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
        super(DfModelRaceInfo, self).__init__(table)       
                            

                
    def getDefaultTableRow(self): 
        category = DataframeTableModel.getDefaultTableRow(self)                
        category['name'] = "unknown"        
        return category 
        
    
    
    
    #virtual function to override
    def GetDataframe(self):
        row_id = 1
        rows = []
        
        
        row = {}
        row["id"] = row_id
        row["name"] = "Run id:" #+ str(run_id)
        row["startlist"] = 0 #tableUsers.getCount()  
        row["dns"] = 0#tableUsers.getCount("dns")          
        row["finished"] = 0#tableUsers.getCount("finished")
        row["dq"] = 0#tableUsers.getCount("dq")  
        row["dnf"] = 0#tableUsers.getCount("dnf")
        row["race"] = 0#tableUsers.getCount("race") 
        
        
        if row["startlist"] ==  row["dns"] + row["finished"] + row["dq"] + row["dnf"] + row["race"]:
            row["check"] = "ok"
        else:
            row["check"] = "ko"        
             
        rows.append(row)
        row_id =  row_id + 1        
         
        #categories
        dbCategories = tableCategories.getDbRows()                      
        for dbCategory in dbCategories:                                                                                            
             
            #row = self.db2tableRow(row)
            row = {}
            row["id"] = row_id
            row["name"] = dbCategory["name"]                        
            row["startlist"] = 0# tableUsers.getCount(dbCategory = dbCategory)  
            row["dns"] = 0# tableUsers.getCount("dns", dbCategory)              
            row["finished"] = 0# tableUsers.getCount("finish", dbCategory)
            row["dq"] = 0# tableUsers.getCount("dq", dbCategory)  
            row["dnf"] = 0# tableUsers.getCount("dnf", dbCategory)              
            row["race"] = 0# tableUsers.getCount("race", dbCategory)
             
            if row["startlist"] ==  row["dns"] + row["finished"] + row["dq"] + row["dnf"] + row["race"]:
                row["check"] = "ok"
            else:
                row["check"] = "ko"                          
                   
            rows.append(row)
            row_id =  row_id + 1                     
        
        
        df = pd.DataFrame(rows)        
        return df                    
    
'''
Proxy Model
'''    
class DfProxymodelRaceInfo(QtGui.QSortFilterProxyModel, ModelUtils):
    def __init__(self, parent = None):        
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        
        #This property holds whether the proxy model is dynamically sorted and filtered whenever the contents of the source model change.       
        self.setDynamicSortFilter(True)

        #This property holds the column where the key used to filter the contents of the source model is read from.
        #The default value is 0. If the value is -1, the keys will be read from all columns.                
        self.setFilterKeyColumn(-1) 
        

# view <- proxymodel <- model 
class DfTableRaceInfo(DfTable):
    def  __init__(self):                                                              
        DfTable.__init__(self, "RaceInfo")
    def Init(self):        
        DfTable.Init(self)
        self.gui['view'].sortByColumn(0, QtCore.Qt.AscendingOrder)
        
    #v modelu tahle funkce šahá do db, raceinfo nema tabulku v db        
    def updateDbCounter(self):
        pass
    
tableRaceInfo = DfTableRaceInfo()
tabRaceInfo = MyTab(tables = [tableRaceInfo,])         
                            


        
       


        
        
            
            

        
        
    