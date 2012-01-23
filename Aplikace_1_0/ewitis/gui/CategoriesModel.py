#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import ewitis.gui.GuiData as GuiData
import libs.db_csv.db_csv as Db_csv

      
class CategoriesParameters(myModel.myParameters):
       
    def __init__(self, source):
                                
        #table and db table name
        self.name = "Categories"  
        
        #=======================================================================
        # KEYS DEFINITION
        #======================================================================= 
        self.DB_COLLUMN_DEF = { "id"            :     {"index": 0,      "name": "id",               "col_nr_export": None},
                                "name"          :     {"index": 1,      "name": "name",             "col_nr_export": None},                                                                 
                                "starttime"     :     {"index": 2,      "name": "starttime",               "col_nr_export": None},
                              }
        self.TABLE_COLLUMN_DEF = { "id"            :     {"index": 0,   "name": "id"},
                                   "name"          :     {"index": 1,   "name": "name"},                                                                
                                   "starttime"     :     {"index": 2,   "name": "starttime"},
                              }                                

                
        #create MODEL and his structure
        myModel.myParameters.__init__(self, source)                                                                            
        
        #=======================================================================
        # GUI
        #=======================================================================
        #VIEW   
        self.gui = {}     
        self.gui['view'] = source.ui.CategoriesProxyView
        
        #FILTER
        self.gui['filter'] = source.ui.CategoriesFilterLineEdit
        self.gui['filterclear'] = source.ui.CategoriesFilterClear
        
        #GROUPBOX
        self.gui['add'] = source.ui.CategoriesAdd
        self.gui['remove'] =  source.ui.CategoriesRemove
        self.gui['export'] = source.ui.CategoriesExport
        self.gui['export_www'] = None
        self.gui['import'] = source.ui.CategoriesImport 
        self.gui['delete'] = source.ui.CategoriesDelete
        
        #COUNTER
        self.gui['counter'] = source.ui.CategoriesCounter
                

class CategoriesModel(myModel.myModel):
    def __init__(self, params):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)

        self.update()                    

        
    #first collumn is NOT editable      
    def flags(self, index):
        return myModel.myModel.flags(self, index)
    
        
    def getDefaultTableRow(self): 
        user = myModel.myModel.getDefaultTableRow(self)                
        user['name'] = "unknown"        
        user['starttime'] = 0
        return user 
    
    #===============================================================
    # DB => GUI                            
    #===============================================================       
    def db2tableRow(self, dbUser):                                        
        
        #1to1 keys just copy
        tabCategory = myModel.myModel.db2tableRow(self, dbUser)                                 
                                
        return tabCategory
    
    #===============================================================
    # GUI => DB                            
    #===============================================================
    #GUI: "id", "nr", "name", "first_name", "category", "address"   
    #DB:  "id", "nr", "name", "first_name", "category", "address"    
    def table2dbRow(self, tabUser):                              
            
        #1to1 keys just copy
        dbCategory = myModel.myModel.table2dbRow(self, tabUser)
                                                                                          
        return dbCategory 
     
#    def slot_ModelChanged(self, item):
#        
#        #EXIST USER WITH THIS NR??
#        if((self.params.guidata.table_mode == GuiData.MODE_EDIT) and (self.params.guidata.user_actions == GuiData.ACTIONS_ENABLE)):
#            if(item.column() == 1):                                
#                nr = item.data(0).toString() #get row
#                user = self.params.db.getParX("Categories", "nr", nr).fetchone()
#                if(user != None):
#                    self.params.showmessage(self.params.name+" Update error", "User with number "+nr+" already exist!")
#                    self.update()
#                    return None
#        myModel.myModel.slot_ModelChanged(self, item)
                 
class CategoriesProxyModel(myModel.myProxyModel):
    def __init__(self):                        
        
        #create PROXYMODEL
        myModel.myProxyModel.__init__(self)  
        


# view <- proxymodel <- model 
class Categories(myModel.myTable):
    def  __init__(self, params):                
                
        #create MODEL
        self.model = CategoriesModel(params)        
        
        #create PROXY MODEL
        self.proxy_model = CategoriesProxyModel() 
        
        myModel.myTable.__init__(self, params)
        
        
        #assign MODEL to PROXY MODEL
        #self.proxy_model.setSourceModel(self.model)
        
        #assign PROXY MODEL to VIEW
        #self.view = view 
        self.params.gui['view'].setModel(self.proxy_model)
        self.params.gui['view'].setRootIsDecorated(False)
        self.params.gui['view'].setAlternatingRowColors(True)        
        self.params.gui['view'].setSortingEnabled(True)
        self.params.gui['view'].setColumnWidth(0,40)
        self.params.gui['view'].setColumnWidth(1,30)
        self.params.gui['view'].setColumnWidth(2,100)
        
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(1000);
                
        
#    def get_db_user_par_nr(self, nr):
#                 
#        db_user = self.params.db.getParX("Categories", "nr", nr).fetchone()        
#                        
#        return db_user
#    
    def getDbCategory(self, id):
                 
        dbCategory = self.params.db.getParX("Categories", "id", id).fetchone()        
                        
        return dbCategory
    
    def getTabCategory(self, id):
                             
        #get db user
        dbCategory = self.getDbCategory(id)
        
        #exist user?
        if dbCategory == None:
            tabCategory = self.model.getDefaultTableRow()
            
        #exist => restrict username                
        else:
            tabCategory = self.model.db2tableRow(dbCategory)  
            
        return tabCategory
        
       


        
        
            
            

        
        
    