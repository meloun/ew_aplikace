# -*- coding: utf-8 -*-

from ewitis.gui.aTableModel import myModel, myProxyModel
from ewitis.gui.aTab import MyTab 
from ewitis.gui.aTable import myTable
from ewitis.data.db import db

class CGroupsModel(myModel):
    def __init__(self, table):                        
        myModel.__init__(self, table)
               
    def getDefaultTableRow(self): 
        cgroup = myModel.getDefaultTableRow(self)                
        cgroup['name'] = "unknown"        
        cgroup['label'] = "gx"
        return cgroup 
                    
class CGroupsProxyModel(myProxyModel):
    def __init__(self, table):                                        
        myProxyModel.__init__(self, table)  
        

# view <- proxymodel <- model 
class CGroups(myTable):
    def  __init__(self):                                             
         
        #default table constructor
        myTable.__init__(self, "CGroups")
        
    def getDbCGroupParLabel(self, label):                 
        dbCGroup = db.getParX("CGroups", "label", label).fetchone()                                
        return dbCGroup   
        
    def getTabCGrouptParLabel(self, label):                         
        dbCGroup = self.getDbCGroupParLabel(label)        
        tabCGroup = self.model.db2tableRow(dbCGroup)                                   
        return tabCGroup

    
tableCGroups = CGroups()
tabCGroups = MyTab(tables = [tableCGroups,])          
                        