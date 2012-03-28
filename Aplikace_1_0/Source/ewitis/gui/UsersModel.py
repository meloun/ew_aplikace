#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import ewitis.gui.GuiData as GuiData
import libs.db_csv.db_csv as Db_csv
import ewitis.gui.DEF_COLUMN as DEF_COLUMN
import libs.datastore.datastore as datastore
        
class UsersParameters(myModel.myParameters):
       
    def __init__(self, source):
                                
        #table and db table name
        self.name = "Users"  
        
        self.tableTags = source.tableTags
        
        self.datastore = source.datastore
        
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
    def db2tableRow(self, dbUser):                                        
        
        #1to1 keys just copy
        tabUser = myModel.myModel.db2tableRow(self, dbUser) 
        
#        if(tabUser['name']==''):
#                tabUser['name'] = 'nobody'

        if dbUser:            
            #tabUser['user_id'] = dbUser['id']
            dbTag = self.params.tableTags.getTabTagParUserNr(dbUser['nr'])            
            tabUser['user_id'] = dbTag['tag_id']
        else:
            tabUser['user_id'] = 0                              
                                
        return tabUser
    
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
        
        myModel.myTable.__init__(self, params)
        
           
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(1000);        
            
    def getDbUserParNr(self, nr):
                 
        db_user = self.params.db.getParX("users", "nr", nr).fetchone()        
                        
        return db_user
    
    def getTabUserParNr(self, id):
                             
        #get db row
        dbRow = self.getDbUserParNr(id)
        
        tabRow = self.model.db2tableRow(dbRow)  
            
        return tabRow
    
    def getDbUserParTagId(self, tag_id):
        
        '''get tag because of number'''
        dbTag = self.params.tableTags.getDbTagParTagId(tag_id) 
                 
        if (dbTag == None):
            return None
        
        '''get user par number'''
        db_user = self.params.db.getParX("users", "nr", dbTag['user_nr']).fetchone()        
                        
        return db_user
    
    
    def getTabUserParIdOrTagId(self, id):
        
        if(self.params.datastore.Get("rfid") == True):        
            '''tag id'''
            dbUser = self.getDbUserParTagId(id)
        else:        
            '''id'''
            dbUser = self.getDbRow(id)
        
        tabUser = self.model.db2tableRow(dbUser)
        return tabUser
    
    def getIdOrTagIdParNr(self, nr):
        
        if(self.params.datastore.Get("rfid") == True):    
            '''tag id'''
            dbTag = self.params.tableTags.getDbTagParUserNr(nr)                        
            return dbTag['tag_id']
        else:       
            '''id'''
            dbUser = self.getDbUserParNr(nr)
            return dbUser['id']
        
       


        
        
            
            

        
        
    