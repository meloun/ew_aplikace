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
        user['nr'] = 0
        user['status'] = "race"
        user['name'] = "unknown"
        user['category'] = tableCategories.getTabCategoryFirst()['name']
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
        tabUser = myModel.db2tableRow(self, dbUser) 
        
        '''get category'''
        if dbUser == None:
            tabCategory = tableCategories.model.getDefaultTableRow()
        else:
            tabCategory = tableCategories.getTabRow(dbUser['category_id'])        
        
        tabUser['category'] = tabCategory['name']
                        
                                
        return tabUser
    

    
    #===============================================================
    # GUI => DB                            
    #===============================================================
    #GUI: "id", "nr", "name", "first_name", "category", "address"   
    #DB:  "id", "nr", "name", "first_name", "category", "address"    
    def table2dbRow(self, tabUser, item = None):        
        
        if tabUser['status'] != 'finished' and tabUser['status'] != 'race' and tabUser['status'] != 'dns' and tabUser['status'] != 'dnf' and tabUser['status'] != 'dsq':
            uiAccesories.showMessage("Status update error", "Wrong format of status! \n\nPossible only 'race','dns', dnf' or 'dsq'!")                        
            return None                
            
        #1to1 keys just copy        
        dbUser = myModel.table2dbRow(self, tabUser, item)
                
        '''category_id'''        
        dbCategory = tableCategories.getDbCategoryParName(tabUser['category']) 
        
        if(dbCategory == None):
            '''category not found => nothing to save'''
            uiAccesories.showMessage(self.table.name+" Update error", "No category with this name "+(tabUser['category'])+"!")
            return None
        dbUser['category_id'] = dbCategory['id']
                                                                                          
        return dbUser 
    
    def importRow2dbRow(self, importRow):                    
        #if 'category_id' in importRow:
        #    del importRow['category_id']        
        tabCategory = tableCategories.getTabCategoryParName(importRow['category_id'])        
        importRow['category_id'] = tabCategory['id']
        return importRow
        
#     
#    def sModelChanged(self, item):
#        
#        #EXIST USER WITH THIS NR??
#        if((self.params.guidata.table_mode == GuiData.MODE_EDIT) and (self.params.guidata.user_actions == GuiData.ACTIONS_ENABLE)):
#            if(item.column() == 1):                                
#                nr = item.data(0).toString() #get row
#                user = db.getParX("users", "nr", nr).fetchone()
#                if(user != None):
#                    self.params.showmessage(self.params.name+" Update error", "User with number "+nr+" already exist!")
#                    self.Update()
#                    return None
#        myModel.myModel.sModelChanged(self, item)
                 
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
    
    def getIdOrTagIdParNr(self, nr):
        
        if(dstore.Get("rfid") == 2):    
            '''tag id'''
            dbTag = tableTags.getDbTagParUserNr(nr)                        
            return dbTag['tag_id']
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


        
        
            
            

        
        
    