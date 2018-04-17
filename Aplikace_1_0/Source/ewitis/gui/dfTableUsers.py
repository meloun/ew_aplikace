# -*- coding: utf-8 -*-
'''
Created on 2. 8. 2015

@author: Meloun
'''


import time
import pandas as pd
import pandas.io.sql as psql 
from PyQt4 import QtCore, QtGui
from libs.myqt.DataframeTableModel import DataframeTableModel, ModelUtils
import libs.pandas.df_utils as df_utils

from ewitis.data.db import db
from ewitis.gui.dfTable import DfTable
from ewitis.gui.aTab import MyTab
#from ewitis.gui.dfTableTags import tableTags
from ewitis.gui.dfTableCategories import tableCategories
from ewitis.data.dstore import dstore
from ewitis.gui.Ui import Ui
from ewitis.gui.UiAccesories import uiAccesories


'''
Model
'''
class DfModelUsers(DataframeTableModel):
    def __init__(self, table):
        super(DfModelUsers, self).__init__(table)
        
    def IsColumnAutoEditable(self, column):
        '''pokud true, po uživatelské editaci focus na další řádek'''
        
#         #number
#         if(column == 1):              
#             return True
        
        return False
   
    def GetDataframe(self): 
        uDf = psql.read_sql(\
            "SELECT * FROM " + str(self.name )
            , db.getDb())
                # CATEGORY df
        cDf = psql.read_sql("SELECT id, name FROM categories", db.getDb())
        cDf.columns = ['cdf_id', 'category']                          
        uDf =  pd.merge(uDf,  cDf, left_on='category_id', right_on='cdf_id', how="left")        
        uDf = uDf[["id", "nr", "status", "name",  "first_name", "category", "club", "year", "sex", "email", "o1", "o2", "o3", "o4"]]
           
        return uDf
    
    def setDataFromDict(self, mydict):
        print "setDataFromDict()", mydict, self.name
        
        
        #category changed
        if "category" in mydict:                         
            category = tableCategories.model.getCategoryParName(unicode(mydict["category"]))
            if category.empty:
                uiAccesories.showMessage(self.name+" Update error", "No category with this name "+(mydict['category'])+"!")
                return                
            mydict["category_id"] = category['id']
            del mydict["category"]           
        
        #update db from mydict
        db.update_from_dict(self.name, mydict)
        return True
        
    def getDefaultRow(self):
        """
        vraci radek naplneny zakladnimi daty
        """ 
        row = DataframeTableModel.getDefaultRow(self)
        row["category_id"] = 1        
        return row
    
    def getUserParNr(self, nr):        
        user = df_utils.Get(self.df, 0, {"nr": nr})
        return user
    
    def getUserParTagId(self, tag_id):
        tag = tableTags.getTagParTagid(tag_id)
        user = df_utils.Get(self.df, 0, {"nr":tag['user_nr']})
        return user

    def getUserParIdOrTagId(self, id):
                
        
        if(dstore.GetItem("racesettings-app", ['rfid']) == 2):                                            
            user = self.getUserParTagId(id) #tag id
        else:                            
            user = self.getRow(id) #id
                     
        return user
    
    def getIdOrTagIdParNr(self, nr):                              
        if(dstore.GetItem("racesettings-app", ['rfid']) == 2):    
            '''tag id'''
            try:
                dbTag = tableTags.model.getTagParUserNr(nr)                        
                return dbTag['tag_id']
            except TypeError:
                return None  
        else:       
            '''id'''
            try:
                user = self.getUserParNr(nr)
                return user['id']  
            except TypeError:
                return None 
        
    
'''
Proxy Model
'''    
class DfProxymodelUsers(QtGui.QSortFilterProxyModel, ModelUtils):
    def __init__(self, parent = None):        
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        
        #This property holds whether the proxy model is dynamically sorted and filtered whenever the contents of the source model change.       
        self.setDynamicSortFilter(True)

        #This property holds the column where the key used to filter the contents of the source model is read from.
        #The default value is 0. If the value is -1, the keys will be read from all columns.                
        self.setFilterKeyColumn(-1)

        
'''
Table
'''        
class DfTableUsers(DfTable):
    def  __init__(self):        
        DfTable.__init__(self, "Users")

            
    def InitGui(self):
        DfTable.InitGui(self)        
     
    def createSlots(self):
        DfTable.createSlots(self)        

    def importDf2dbDdf(self, df): 

        if "description" in df.columns:
            #df.drop(df.columns[16], axis=1, inplace=True)
            df.drop(["description", "paid", "symbol"], axis=1, inplace=True)
           
        #df["category_id"] = df.apply(lambda row: tableCategories.model.getCategoryParName(row["category"])['id'], axis = 1)
        #df.drop(["category"], axis=1, inplace=True)        
        return df
    
    def importRow2dbRow(self, row):
        #print "cateogory name:",  row["category"]
        category = tableCategories.model.getCategoryParName(row["category"])
        #print "cateogory:", category, type(category)
        #print "ROW1", row  
        row["category_id"] = category['id']  
        row.drop(["category"], inplace=True) 
                    
    def Update(self):                                                                                  
        return DfTable.Update(self)
        
        
        


tableUsers = DfTableUsers()
tabUsers = MyTab(tables = [tableUsers,])          
                
        
