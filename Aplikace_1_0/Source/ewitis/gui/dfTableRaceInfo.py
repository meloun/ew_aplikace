# -*- coding: utf-8 -*-
import time
import pandas as pd
import pandas.io.sql as psql 
from PyQt4 import QtCore, QtGui
from ewitis.gui.aTab import MyTab
from libs.myqt.DataframeTableModel import DataframeTableModel, ModelUtils 

from ewitis.gui.dfTable import DfTable
from ewitis.gui.dfTableTimes import tableTimes
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
        row = pd.Series()
        row["id"] = 0
        row["name"] = "NOTDEF"
        row["cell#1"] = "-"
        row["cell#2"] = "-"
        row["cell#3"] = "-"
        row["cell#4"] = "-"
        row["cell#5"] = "-"
        row["cell#250"] = "-"        
        return row    
    
    #virtual function to override
    def GetDataframe(self):
        row_id = 1
        rows = pd.DataFrame()
        
        #check if df is alread available        
        if tableTimes.model.df.empty:
            return pd.DataFrame()  
        
        '''ADD TOTAL'''
        #group by cell and get size
        serTimesByCell_size = tableTimes.model.df.groupby("cell", as_index=False).size()
                 
        #create new row               
        row = self.getDefaultTableRow()
        row["id"] = row_id
        row["name"] = "Total"        
        for (k,v) in serTimesByCell_size.iteritems():
                key = "cell#"+str(k)
                row[key] = v            
        
        #append new row
        rows = rows.append(row, ignore_index=True)
        row_id =  row_id + 1
            
        
        '''ADD CATEGORIES'''
        #group by category and get size
        gbTimesByCategory = tableTimes.model.df.groupby("category")        
        for category, dfTimesInCategory in gbTimesByCategory: 
            serTimesForCategoryByCell_size = dfTimesInCategory.groupby("cell").size()        
                                                                 
            #create new row
            row = self.getDefaultTableRow()
            row["id"] = row_id
            row["name"] = category
            for (k,v) in serTimesForCategoryByCell_size.iteritems():
                key = "cell#"+str(k)
                row[key] = v
                         
            #add new row and increment id   
            rows = rows.append(row, ignore_index=True)
            row_id =  row_id + 1
        
        df = pd.DataFrame(rows, columns=row.keys())
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
