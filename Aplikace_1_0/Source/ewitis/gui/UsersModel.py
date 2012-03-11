#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import ewitis.gui.GuiData as GuiData
import libs.db_csv.db_csv as Db_csv
import ewitis.gui.DEF_COLUMN as DEF_COLUMN
        
class UsersParameters(myModel.myParameters):
       
    def __init__(self, source):
                                
        #table and db table name
        self.name = "Users"  
        
        #=======================================================================
        # KEYS DEFINITION
        #======================================================================= 
        #toDo: predat jen DEF_COLUMN.USERS, zbytek v myModel
        self.DB_COLLUMN_DEF = DEF_COLUMN.USERS['database']
        self.TABLE_COLLUMN_DEF = DEF_COLUMN.USERS['table']
                                  

                
        #create MODEL and his structure
        myModel.myParameters.__init__(self, source)                                                                            
        
        #=======================================================================
        # GUI
        #=======================================================================
        #VIEW   
        self.gui = {}     
        self.gui['view'] = source.ui.UsersProxyView
        
        
        #FILTER
        self.gui['filter'] = source.ui.UsersFilterLineEdit
        self.gui['filterclear'] = source.ui.UsersFilterClear
        
        #GROUPBOX
        self.gui['add'] = source.ui.UsersAdd
        self.gui['remove'] =  source.ui.UsersRemove
        self.gui['export'] = source.ui.UsersExport
        self.gui['export_www'] = None
        self.gui['import'] = source.ui.UsersImport 
        self.gui['delete'] = source.ui.UsersDelete
        
        #COUNTER
        self.gui['counter'] = source.ui.UsersCounter
        
        #=======================================================================
        # classes
        #=======================================================================        
        self.classModel = UsersModel                              
        self.classProxyModel = UsersProxyModel
                

class UsersModel(myModel.myModel):
    def __init__(self, params):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)

        self.update()                    

        
    #first collumn is NOT editable      
    def flags(self, index):
        return myModel.myModel.flags(self, index)
    
        
    def getDefaultTableRow(self): 
        user = myModel.myModel.getDefaultTableRow(self)                
        user['nr'] = 0
        user['name'] = "unknown"        
        return user 
    
    #===============================================================
    # DB => GUI                            
    #===============================================================   
    #DB:  "id", "nr", "name", "first_name", "category", "address"
    #GUI: "id", "nr", "name", "first_name", "category", "address"    
#    def db2tableRow(self, dbUser):                                        
#        
#        #1to1 keys just copy
#        tabUser = myModel.myModel.db2tableRow(self, dbUser) 
#        
#        if(tabUser['name']==''):
#                tabUser['name'] = 'nobody'                              
#                                
#        return tabUser
    
    #===============================================================
    # GUI => DB                            
    #===============================================================
    #GUI: "id", "nr", "name", "first_name", "category", "address"   
    #DB:  "id", "nr", "name", "first_name", "category", "address"    
#    def table2dbRow(self, tabUser):                              
#            
#        #1to1 keys just copy
#        dbUser = myModel.myModel.table2dbRow(self, tabUser)
#                                                                                          
#        return dbUser 
     
#    def slot_ModelChanged(self, item):
#        
#        #EXIST USER WITH THIS NR??
#        if((self.params.guidata.table_mode == GuiData.MODE_EDIT) and (self.params.guidata.user_actions == GuiData.ACTIONS_ENABLE)):
#            if(item.column() == 1):                                
#                nr = item.data(0).toString() #get row
#                user = self.params.db.getParX("users", "nr", nr).fetchone()
#                if(user != None):
#                    self.params.showmessage(self.params.name+" Update error", "User with number "+nr+" already exist!")
#                    self.update()
#                    return None
#        myModel.myModel.slot_ModelChanged(self, item)
                 
class UsersProxyModel(myModel.myProxyModel):
    def __init__(self):                        
        
        #create PROXYMODEL
        myModel.myProxyModel.__init__(self)  
        


# view <- proxymodel <- model 
class Users(myModel.myTable):
    def  __init__(self, params):                
                
        #create MODEL
        #self.model = UsersModel(params)        
        
        #create PROXY MODEL
        #self.proxy_model = UsersProxyModel() 
        
        myModel.myTable.__init__(self, params)
        
        
        #assign MODEL to PROXY MODEL
        #self.proxy_model.setSourceModel(self.model)
        
        #assign PROXY MODEL to VIEW
        #self.view = view 
#        self.params.gui['view'].setModel(self.proxy_model)
#        self.params.gui['view'].setRootIsDecorated(False)
#        self.params.gui['view'].setAlternatingRowColors(True)        
#        self.params.gui['view'].setSortingEnabled(True)
#        self.params.gui['view'].setColumnWidth(0,90)
#        self.params.gui['view'].setColumnWidth(1,230)
#        self.params.gui['view'].setColumnWidth(2,100)
#        self.params.gui['view'].setColumnWidth(3,100)
#        self.params.gui['view'].setColumnWidth(4,100)        
#        self.params.gui['view'].setColumnWidth(5,250)
#        
        
#        print self.params.gui['view'].columnWidth(2)
#        self.params.gui['view'].setColumnWidth(2,640)
#        print self.params.gui['view'].columnWidth(2)
        
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(1000);
        
        #MODE EDIT/REFRESH        
        #self.table_mode = myModel.MODE_REFRESH
               
        #self.db = db
        
        #self.keys = keys
        
        #self.model.update()        
        #self.createSlots()
        
    def get_db_user_par_nr(self, nr):
                 
        db_user = self.params.db.getParX("users", "nr", nr).fetchone()        
                        
        return db_user
    
    def get_db_user(self, id):
                 
        db_user = self.params.db.getParX("users", "id", id).fetchone()        
                        
        return db_user
    
    def get_tab_user(self, id):
                             
        #get db user
        db_user = self.get_db_user(id)
        
        #exist user?
        if db_user == None:
            tab_user = self.model.getDefaultTableRow()
            
        #exist => restrict username                
        else:
            tab_user = self.model.db2tableRow(db_user)  
            
        return tab_user
        
       


        
        
            
            

        
        
    