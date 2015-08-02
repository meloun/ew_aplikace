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

from ewitis.data.db import db
from ewitis.gui.dfTable import DfTable
from ewitis.gui.aTab import MyTab
from ewitis.gui.dfTableTags import tableTags
from ewitis.data.dstore import dstore
from ewitis.gui.Ui import Ui


'''
Model
'''
class DfModelUsers(DataframeTableModel):
    def __init__(self, name, parent = None):
        super(DfModelUsers, self).__init__(name)
                      
    #jen prozatim
    def db2tableRow(self, dbRow):
        return dbRow
   
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
        db.update_from_dict(self.name, mydict)
        
    def getDefaultRow(self):
        """
        vraci radek naplneny zakladnimi daty
        """ 
        row = DataframeTableModel.getDefaultRow(self)
        row["category_id"] = 1
        return row
    
    def getUserParNr(self, nr):
        user = df_utils.Get(self.df, 0, {"nr":nr})
        return user
    
    def getUserParTagId(self, tag_id):
        tag = tableTags.getTagParTagid(tag_id)
        user = df_utils.Get(self.df, 0, {"nr":tag['user_nr']})
        return user

    def getDbUserParIdOrTagId(self, id):
        user = self.getDbUserParTagId(id)
        return user
        
    
'''
Proxy Model
'''    
class DfProxymodelUsers(QtGui.QSortFilterProxyModel, ModelUtils):
    def __init__(self):        
        QtGui.QSortFilterProxyModel.__init__(self)
        
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
                
    def Update(self):                                                                                  
        DfTable.Update(self)
        
        
        


tableUsers = DfTableUsers()
tabUsers = MyTab(tables = [tableUsers,])          
                
        
 