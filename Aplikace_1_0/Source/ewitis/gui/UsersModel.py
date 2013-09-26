# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import libs.db_csv.db_csv as Db_csv
import ewitis.gui.DEF_COLUMN as DEF_COLUMN
#import libs.datastore.datastore as datastore
        
class UsersParameters(myModel.myParameters):
       
    def __init__(self, source):
                                
        #table and db table name
        self.name = "Users"  
        
        self.tableTags = source.tableTags
        self.tabCategories = source.C
        
        #self.datastore = source.datastore
        
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
                    

        
    #first collumn is NOT editable      
    def flags(self, index):
        return myModel.myModel.flags(self, index)
    
        
    def getDefaultTableRow(self): 
        user = myModel.myModel.getDefaultTableRow(self)                
        user['nr'] = 0
        user['status'] = "race"
        user['name'] = "unknown"
        user['category'] = self.params.tabCategories.getTabCategoryFirst()['name']
        user['category_id'] = 0
        user['id'] = 0                  
        return user
     
    def getDefaultDbRow(self, dbTag): 
        user = {}                
        user['id'] = 0
        user['nr'] = dbTag['user_nr']
        user['race'] = "race"
        user['name'] = "USER: "+ str(dbTag['user_nr'])+ ", TAG: "+str(dbTag['printed_nr'])#+" id:"+ str(dbTag['tag_id'])
        user['first_name'] = ""
        user['first_name'] = ""                
        user['category_id'] = 0
        user['club'] = ""
        user['birthday'] = ""
        user['sex'] = ""
        user['email'] = ""
        user['symbol'] = ""
        user['paid'] = ""
        user['note'] = ""
        user['o1'] = ""
        user['o2'] = ""
        user['o3'] = ""
        user['o4'] = ""                                          
        return user 
    
    #===============================================================
    # DB => GUI                            
    #===============================================================   
    #DB:  "id", "nr", "name", "first_name", "category", "address"
    #GUI: "id", "nr", "name", "first_name", "category", "address"    
    def db2tableRow(self, dbUser):                                        
        
        #1to1 keys just copy
        tabUser = myModel.myModel.db2tableRow(self, dbUser) 
        
        '''get category'''
        if dbUser == None:
            tabCategory = self.params.tabCategories.model.getDefaultTableRow()
        else:
            tabCategory = self.params.tabCategories.getTabRow(dbUser['category_id'])        
        
        tabUser['category'] = tabCategory['name']
                        
                                
        return tabUser
    

    
    #===============================================================
    # GUI => DB                            
    #===============================================================
    #GUI: "id", "nr", "name", "first_name", "category", "address"   
    #DB:  "id", "nr", "name", "first_name", "category", "address"    
    def table2dbRow(self, tabUser, item = None):                              

        if tabUser['status'] != 'finished' and tabUser['status'] != 'race' and tabUser['status'] != 'dns' and tabUser['status'] != 'dnf' and tabUser['status'] != 'dsq':
            self.params.uia.showMessage("Status update error", "Wrong format of status! \n\nPossible only 'race','dns', dnf' or 'dsq'!")                        
            return None                
            
        #1to1 keys just copy        
        dbUser = myModel.myModel.table2dbRow(self, tabUser, item)
                
        '''category_id'''        
        dbCategory = self.params.tabCategories.getDbCategoryParName(tabUser['category']) 
        
        if(dbCategory == None):
            '''category not found => nothing to save'''
            self.params.uia.showMessage(self.params.name+" Update error", "No category with this name "+(tabUser['category'])+"!")
            return None
        dbUser['category_id'] = dbCategory['id']
                                                                                          
        return dbUser 
    
    def import2dbRow(self, importRow):                    
        #if 'category_id' in importRow:
        #    del importRow['category_id']
        tabCategory = self.params.tabCategories.getTabCategoryParName(importRow['category_id'])
        #print tabCategory
        importRow['category_id'] = tabCategory['id']
        return importRow
        
#     
#    def sModelChanged(self, item):
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
#        myModel.myModel.sModelChanged(self, item)
                 
class UsersProxyModel(myModel.myProxyModel):
    def __init__(self, params):                        
        
        #create PROXYMODEL
        myModel.myProxyModel.__init__(self, params)
        
    def IsColumnAutoEditable(self, column):
        if column == 1:
            '''změna čísla'''    
            return True
        return False  
        


# view <- proxymodel <- model 
class Users(myModel.myTable):
    def  __init__(self, params):                            
        
        myModel.myTable.__init__(self, params)
        
           
        #TIMERs
        #self.timer1s = QtCore.QTimer(); 
        #self.timer1s.start(1000);
            
            
    def getDbUserParNr(self, nr):
                 
        db_user = self.params.db.getParX("users", "nr", nr, limit = 1).fetchone()        
                        
        return db_user
    
    def getTabUserParNr(self, nr):
                             
        #get db row
        dbRow = self.getDbUserParNr(nr)        
        
        tabRow = self.model.db2tableRow(dbRow)                
            
        return tabRow
    
    def getDbUserParTagId(self, tag_id):
        
        '''get tag because of number'''
        dbTag = self.params.tableTags.getDbTagParTagId(tag_id) 
                 
        if (dbTag == None):
            return None
        
        '''get user par number'''
        db_user = self.params.db.getParX("users", "nr", dbTag['user_nr'], limit = 1).fetchone()
        
        if(db_user == None):
            return self.model.getDefaultDbRow(dbTag)        
                        
        return db_user
    
    def getDbUserParIdOrTagId(self, id):        
             
        if(self.params.datastore.Get("rfid") == 2):                    
            '''tag id'''            
            dbUser = self.getDbUserParTagId(id)
        else:                
            '''id'''            
            dbUser = self.getDbRow(id)
                     
        return dbUser
    
    def getTabUserParIdOrTagId(self, id):
        
        
        dbUser = self.getDbUserParIdOrTagId(id)                 
        
        
        tabUser = self.model.db2tableRow(dbUser)
        return tabUser
    
    def getIdOrTagIdParNr(self, nr):
        
        if(self.params.datastore.Get("rfid") == 2):    
            '''tag id'''
            dbTag = self.params.tableTags.getDbTagParUserNr(nr)                        
            return dbTag['tag_id']
        else:       
            '''id'''
            dbUser = self.getDbUserParNr(nr)
            return dbUser['id']    
        
                
    #
    def getCount(self, status = None, dbCategory = None):
        
        if status!=None and dbCategory!=None:
            res = self.params.db.getParXX("users", [["status", status], ["category_id", str(dbCategory["id"])]], "AND")                                                                                        
        elif status!=None and dbCategory==None:
            res = self.params.db.getParX("users", "status", status)
        elif status==None and dbCategory!=None:
            res = self.params.db.getParX("users", "category_id", str(dbCategory["id"]))
        else:
            res = self.getDbRows()             
        
        row_dicts = self.params.db.cursor2dicts(res)                              
        return len(row_dicts)
        
       


        
        
            
            

        
        
    