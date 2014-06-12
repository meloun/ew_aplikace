# -*- coding: utf-8 -*-
from ewitis.gui.aTab import MyTab
from ewitis.gui.aTableModel import myModel, myProxyModel 
from ewitis.gui.aTable import myTable
from ewitis.data.db import db
from ewitis.data.dstore import dstore
from ewitis.gui.tableCategories import tableCategories
from ewitis.gui.tableTags import tableTags
from ewitis.gui.UiAccesories import uiAccesories
        
               
class UsersModel(myModel):
    def __init__(self, table):                                        
        myModel.__init__(self, table)
                        
    #first collumn is NOT editable      
    def flags(self, index):
        return myModel.flags(self, index)
    
        
    def getDefaultTableRow(self): 
        user = myModel.getDefaultTableRow(self)                        
        user['category'] = tableCategories.getTabCategoryFirst()['name']                          
        return user
    
    def getDefaultDbRow(self, dbTag = None): 
        user = myModel.getDefaultDbRow(self)
        if  dbTag != None:              
            user['id'] = 0
            user['nr'] = dbTag['user_nr']
            user['race'] = "race"
            user['name'] = "USER: "+ str(dbTag['user_nr'])+ ", TAG: "+str(dbTag['printed_nr'])#+" id:"+ str(dbTag['tag_id'])
    #        user['first_name'] = ""
    #        user['first_name'] = ""                
            user['category_id'] = 0
    #        user['club'] = ""
    #        user['birthday'] = ""
    #        user['sex'] = ""
    #        user['email'] = ""
    #        user['symbol'] = ""
    #        user['paid'] = ""
    #        user['note'] = ""
    #        user['o1'] = ""
    #        user['o2'] = ""
    #        user['o3'] = ""
    #        user['o4'] = ""                                          
        return user 
    
    
    #===============================================================
    # DB => GUI                            
    #===============================================================   
    #DB:  "id", "nr", "name", "first_name", "category", "address"
    #GUI: "id", "nr", "name", "first_name", "category", "address"    
    def db2tableRow(self, dbUser):                                        
        
        #1to1 keys just copy
        tabUser = myModel.db2tableRow(self, dbUser) 
        
        '''get category'''
        if dbUser == None:
            tabCategory = tableCategories.model.getDefaultTableRow()
        else:
            tabCategory = tableCategories.getTabRow(dbUser['category_id'])        
        
        tabUser['category'] = tabCategory['name']
                        
                                
        return tabUser
    

   
    def checkChangedStatus(self, tabRow):
        '''ZMĚNA STATUSu'''
        '''- pro nestartovcí časy lze do času zapsat 'dns', 'dnf' nebo 'dnq'            
        '''
        
        #check rights and format
        if(int(tabRow['cell']) == 1):
            uiAccesories.showMessage("Status update error", "Status can NOT be set to starttime")
            return False                
        elif(int(tabRow['nr']) == 0):   
            uiAccesories.showMessage("Status update error", "Status can NOT be set to user with nr. 0")
            return False              
        elif tabRow['status'] != 'finished' and tabRow['status'] != 'race' and tabRow['status'] != 'dns' and tabRow['status'] != 'dnf' and tabRow['status'] != 'dsq':
            uiAccesories.showMessage("Status update error", "Wrong format of status! \n\nPossible only 'race','dns', dnf' or 'dsq'!")
            return False
                                                                                                                                                                                                                                    
        return True 
    
    def sModelChanged(self, item):
                                
        if(dstore.Get("user_actions") == 0):                       
            
            ''' user has changed something '''
            
            #handle common columns
            ret = myModel.sModelChanged(self, item)
        
            if(ret == False):
                
                #get changed row, dict{}
                tabRow = self.row_dict(item.row())                                
                 
                # STATUS column
                if(item.column() == self.table.TABLE_COLLUMN_DEF['status']['index']):                    
                    if self.sStatusChanged_Check(tabRow) == True:
                        dbUser = tableUsers.getDbUserParNr(tabRow['nr'])                
                        #print "update",  {'id':dbUser['id'], 'status': tabRow['status']}
                        db.update_from_dict(tableUsers.name, {'id':dbUser['id'], 'status': tabRow['status']})
                        
                elif(item.column() == self.table.TABLE_COLLUMN_DEF['category']['index']):                    
                
                    '''category_id'''        
                    dbCategory = tableCategories.getDbCategoryParName(tabRow['category']) 
        
                    if(dbCategory == None):
                        '''category not found => nothing to save'''
                        uiAccesories.showMessage(self.table.name+" Update error", "No category with this name "+(tabRow['category'])+"!")
                        return None                    
                    db.update_from_dict(tableUsers.name, {'id':tabRow['id'], 'category_id': dbCategory['id']})
                                        
                #update whole model
                self.Update()                                                                                     
         
        return
    
    def importRow2dbRow(self, importRow):                    
        #if 'category_id' in importRow:
        #    del importRow['category_id']        
        tabCategory = tableCategories.getTabCategoryParName(importRow['category_id'])        
        importRow['category_id'] = tabCategory['id']
        return importRow
        

                 
class UsersProxyModel(myProxyModel):
    def __init__(self, table):                                
        myProxyModel.__init__(self, table)
        
    def IsColumnAutoEditable(self, column):
        if column == 1:
            '''změna čísla'''    
            return True
        return False  
        


# view <- proxymodel <- model 
class Users(myTable):
    def  __init__(self):                                    
        myTable.__init__(self, "Users")
           
        #TIMERs
        #self.timer1s = QtCore.QTimer(); 
        #self.timer1s.start(1000);
            
            
    def getDbUserParNr(self, nr):
                 
        db_user = db.getParX("users", "nr", nr, limit = 1).fetchone()        
                        
        return db_user
    
    def getTabUserParNr(self, nr):
                             
        #get db row
        dbRow = self.getDbUserParNr(nr)        
        
        tabRow = self.model.db2tableRow(dbRow)                
            
        return tabRow
    
    def getDbUserParTagId(self, tag_id):
        
        '''get tag because of number'''
        dbTag = tableTags.getDbTagParTagId(tag_id) 
                 
        if (dbTag == None):
            return None
        
        '''get user par number'''
        db_user = db.getParX("users", "nr", dbTag['user_nr'], limit = 1).fetchone()
        
        if(db_user == None):
            return self.model.getDefaultDbRow(dbTag)        
                        
        return db_user
    
    def getDbUserParIdOrTagId(self, id):        
             
        if(dstore.Get("rfid") == 2):                    
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
    
    def getJoinUserParIdOrTagId(self, user_id):        
        
        dbUser = self.getDbUserParIdOrTagId(user_id)        
        
        if(dbUser == None):
            return dict(self.model.getDefaultDbRow().items()+self.model.getDefaultTableRow().items())
        
        tabUser = self.model.db2tableRow(dbUser)            
        
        return  dict(db.row2dict(dbUser).items()+tabUser.items())
    
    def getIdOrTagIdParNr(self, nr):
        
        if(dstore.Get("rfid") == 2):    
            '''tag id'''
            try:
                dbTag = tableTags.getDbTagParUserNr(nr)                        
                return dbTag['tag_id']
            except TypeError:
                return None  
        else:       
            '''id'''
            dbUser = self.getDbUserParNr(nr)
            return dbUser['id']    
        
                
    #
    def getCount(self, status = None, dbCategory = None):
        
        if status!=None and dbCategory!=None:
            res = db.getParXX("users", [["status", status], ["category_id", str(dbCategory["id"])]], "AND")                                                                                        
        elif status!=None and dbCategory==None:
            res = db.getParX("users", "status", status)
        elif status==None and dbCategory!=None:
            res = db.getParX("users", "category_id", str(dbCategory["id"]))
        else:
            res = self.getDbRows()             
        
        row_dicts = db.cursor2dicts(res)                              
        return len(row_dicts)
        
tableUsers = Users()
tabUsers = MyTab(tables = [tableUsers,])         


        
        
            
            

        
        
    