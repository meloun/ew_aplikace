#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import ewitis.gui.GuiData as GuiData
import libs.db_csv.db_csv as Db_csv



        
class UsersParameters(myModel.myParameters):
       
    def __init__(self, source):
                                
        #table and db table name
        self.name = "Users"  
        
        #=======================================================================
        # KEYS DEFINITION
        #======================================================================= 
        self.DB_COLLUMN_DEF = { "id"            :     {"index": 0,      "name": "id",               "col_nr_export": None},
                                "nr"            :     {"index": 1,      "name": "nr",               "col_nr_export": None},
                                "name"          :     {"index": 2,      "name": "name",             "col_nr_export": None},
                                "first_name"    :     {"index": 3,      "name": "first_name",       "col_nr_export": None},
                                "category"      :     {"index": 4,      "name": "category",         "col_nr_export": None},
                                "club"          :     {"index": 5,      "name": "club",             "col_nr_export": 3},
                                "birthday"      :     {"index": 6,      "name": "birthday",         "col_nr_export": 4},
                                "sex"           :     {"index": 7,      "name": "sex",              "col_nr_export": None},
                                "email"         :     {"index": 8,      "name": "email",            "col_nr_export": None},
                                "symbol"        :     {"index": 9,      "name": "symbol",           "col_nr_export": None},
                                "paid"          :     {"index": 10,     "name": "paid",             "col_nr_export": None},
                                "note"          :     {"index": 11,     "name": "note",             "col_nr_export": None},
                                "user_field_1"  :     {"index": 12,     "name": "user_field_1",     "col_nr_export": None},
                                "user_field_2"  :     {"index": 13,     "name": "user_field_2",     "col_nr_export": None},
                                "user_field_3"  :     {"index": 14,     "name": "user_field_3",     "col_nr_export": None},    
                                "user_field_4"  :     {"index": 15,     "name": "user_field_4",     "col_nr_export": None},                                                                    
                              }
        self.TABLE_COLLUMN_DEF = { "id"            :     {"index": 0,   "name": "id"},
                                   "nr"            :     {"index": 1,   "name": "nr"},
                                   "name"          :     {"index": 2,   "name": "name"},
                                   "first_name"    :     {"index": 3,   "name": "first_name"},
                                   "category"      :     {"index": 4,   "name": "category"},
                                   "club"          :     {"index": 5,   "name": "club"},
                                   "birthday"      :     {"index": 6,   "name": "birthday"},
                                   "sex"           :     {"index": 7,   "name": "sex"},
                                   "email"         :     {"index": 8,   "name": "email"},
                                   "symbol"        :     {"index": 9,   "name": "symbol"},
                                   "paid"          :     {"index": 10,   "name": "paid"},
                                   "note"          :     {"index": 11,  "name": "note"},
                                   "user_field_1"  :     {"index": 12,  "name": "user_field_1"},
                                   "user_field_2"  :     {"index": 13,  "name": "user_field_2"},
                                   "user_field_3"  :     {"index": 14,  "name": "user_field_3"},    
                                   "user_field_4"  :     {"index": 15,  "name": "user_field_4"},                                                                    
                              }                                

                
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
        self.gui['counter'] = source.ui.usersCounter
                

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
    def db2tableRow(self, dbUser):                                        
        
        #1to1 keys just copy
        tabUser = myModel.myModel.db2tableRow(self, dbUser) 
        
        if(tabUser['name']==''):
                tabUser['name'] = 'nobody'                              
                                
        return tabUser
    
    #===============================================================
    # GUI => DB                            
    #===============================================================
    #GUI: "id", "nr", "name", "first_name", "category", "address"   
    #DB:  "id", "nr", "name", "first_name", "category", "address"    
    def table2dbRow(self, tabUser):                              
            
        #1to1 keys just copy
        dbUser = myModel.myModel.table2dbRow(self, tabUser)
                                                                                          
        return dbUser 
     
    def slot_ModelChanged(self, item):
        
        #EXIST USER WITH THIS NR??
        if((self.params.guidata.table_mode == GuiData.MODE_EDIT) and (self.params.guidata.user_actions == GuiData.ACTIONS_ENABLE)):
            if(item.column() == 1):                                
                nr = item.data(0).toString() #get row
                user = self.params.db.getParX("users", "nr", nr).fetchone()
                if(user != None):
                    self.params.showmessage(self.params.name+" Update error", "User with number "+nr+" already exist!")
                    self.update()
                    return None
        myModel.myModel.slot_ModelChanged(self, item)
                 
class UsersProxyModel(myModel.myProxyModel):
    def __init__(self):                        
        
        #create PROXYMODEL
        myModel.myProxyModel.__init__(self)  
        


# view <- proxymodel <- model 
class Users(myModel.myTable):
    def  __init__(self, params):                
                
        #create MODEL
        self.model = UsersModel(params)        
        
        #create PROXY MODEL
        self.proxy_model = UsersProxyModel() 
        
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
        self.params.gui['view'].setColumnWidth(3,100)
        self.params.gui['view'].setColumnWidth(4,100)        
        self.params.gui['view'].setColumnWidth(5,250)
        
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
        
       


        
        
            
            

        
        
    