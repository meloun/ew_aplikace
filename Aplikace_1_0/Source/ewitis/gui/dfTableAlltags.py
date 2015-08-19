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
from ewitis.data.dstore import dstore
from ewitis.gui.Ui import Ui


'''
Model
'''
class DfModelAlltags(DataframeTableModel):
    def __init__(self, table):
        super(DfModelAlltags, self).__init__(table)
                      
    #jen prozatim
    def db2tableRow(self, dbRow):
        return dbRow
   
    def GetDataframe(self): 
        df = psql.read_sql(\
            "SELECT * FROM " + str(self.name )
            , db.getDb())
        return df
    
    def setDataFromDict(self, mydict):
        print "setDataFromDict()", mydict, self.name
        db.update_from_dict(self.name, mydict)
        
    def getDefaultRow(self):
        """
        vraci radek naplneny zakladnimi daty
        """ 
        row = DataframeTableModel.getDefaultRow(self)
        return row

    
    
'''
Proxy Model
'''    
class DfProxymodelAlltags(QtGui.QSortFilterProxyModel, ModelUtils):
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
class DfTableAlltags(DfTable):
    def  __init__(self):        
        DfTable.__init__(self, "Alltags")
        
    def InitGui(self):
        DfTable.InitGui(self)        
     
    def createSlots(self):
        DfTable.createSlots(self)        
                
    def Update(self):                                                                                  
        return DfTable.Update(self)
        


tableAlltags = DfTableAlltags()
tabAlltags = MyTab(tables = [tableAlltags,])          
                
        
 