#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import libs.db_csv.db_csv as Db_csv
import ewitis.gui.DEF_COLUMN as DEF_COLUMN

      
class CGroupsParameters(myModel.myParameters):
       
    def __init__(self, source):
                                
        #table and db table name
        self.name = "CGroups"  
        
        #=======================================================================
        # KEYS DEFINITION
        #======================================================================= 
        self.DB_COLLUMN_DEF = DEF_COLUMN.CGROUPS['database']
        self.TABLE_COLLUMN_DEF = DEF_COLUMN.CGROUPS['table']
                
        #create MODEL and his structure
        myModel.myParameters.__init__(self, source)                                                                                            
        
        #=======================================================================
        # GUI
        #=======================================================================
        #VIEW   
        self.gui = {}     
        self.gui['view'] = source.ui.CGroupsProxyView        
        
        #FILTER
        self.gui['filter'] = source.ui.CGroupsFilterLineEdit
        self.gui['filterclear'] = source.ui.CGroupsFilterClear
        
        #GROUPBOX
        self.gui['add'] = source.ui.CGroupsAdd
        self.gui['remove'] =  source.ui.CGroupsRemove
        self.gui['export'] = source.ui.CGroupsExport
        self.gui['export_www'] = None
        self.gui['import'] = source.ui.CGroupsImport 
        self.gui['delete'] = source.ui.CGroupsDelete
        
        #COUNTER
        self.gui['counter'] = source.ui.CGroupsCounter
        
        #=======================================================================
        # classes
        #=======================================================================        
        self.classModel = CGroupsModel                              
        self.classProxyModel = CGroupsProxyModel
                

class CGroupsModel(myModel.myModel):
    def __init__(self, params):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)
                            

                
    def getDefaultTableRow(self): 
        cgroup = myModel.myModel.getDefaultTableRow(self)                
        cgroup['name'] = "unknown"        
        cgroup['label'] = g0
        return cgroup 
                    
class CGroupsProxyModel(myModel.myProxyModel):
    def __init__(self, params):                        
        
        #default proxy-model constructor
        myModel.myProxyModel.__init__(self, params)  
        

# view <- proxymodel <- model 
class CGroups(myModel.myTable):
    def  __init__(self, params):                                             
         
        #default table constructor
        myModel.myTable.__init__(self, params)
        
    def getDbCGroupParLabel(self, label):
                 
        dbCGroup = self.params.db.getParX("CGroups", "label", label).fetchone()        
                        
        return dbCGroup   
        
    def getTabCGrouptParLabel(self, label):
                 
        
        dbCGroup = getDbCGroupParLabel(label)        
                     
        tabCGroup = self.model.db2tableRow(dbCGroup)   
                                
        return tabCGroup       
                        