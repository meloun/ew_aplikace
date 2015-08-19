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
#from ewitis.gui.dfTableUsers import tableUsers
from ewitis.gui.aTab import MyTab
from ewitis.data.dstore import dstore
from ewitis.gui.Ui import Ui


'''
Model
'''
class DfModelCategories(DataframeTableModel):
    def __init__(self, table):
        super(DfModelCategories, self).__init__(table)
                      
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
        row["name"] = "undefined"
        return row
    
    def getCategoryParName(self, name):        
        #category = df_utils.Get(self.df, 0, {"name":name})        
        categories = self.df[self.df['name'].str.match(name)]
        try:                  
            category = categories.iloc[0]
        except IndexError:
            return pd.DataFrame()

                  
        return category
    
    def getCategoriesParGroupLabel(self, label):
        categories = df_utils.Filter(self.df, {label: 1})
        print categories
        return categories

    def Update(self):
        ret = DataframeTableModel.Update(self)
        dstore.SetItem("gui", ["update_requests", "tableUsers"], True)
        return ret
        
    
'''
Proxy Model
'''    
class DfProxymodelCategories(QtGui.QSortFilterProxyModel, ModelUtils):
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
class DfTableCategories(DfTable):
    def  __init__(self):        
        DfTable.__init__(self, "Categories")
        
    def InitGui(self):
        DfTable.InitGui(self)        
     
    def createSlots(self):
        DfTable.createSlots(self)           
                
    def Update(self):    
        ret = DfTable.Update(self)                                                                                           
        return ret
        
          
                
        
                                       
    
if __name__ == "__main__":    

    
    import sys
    from PyQt4 import QtGui
    from Ui_App import Ui_MainWindow
    from ewitis.gui.Ui import appWindow
    from ewitis.gui.Ui import Ui
    from ewitis.gui.UiAccesories import uiAccesories
    print "START"
    
    app = QtGui.QApplication(sys.argv)
    appWindow.Init()
    uiAccesories.Init()
    
    dfTableTimes = DfTableCategories()
    dfTableTimes.Init()    
    dfTableTimes.Update()
        
    appWindow.show()    
    sys.exit(app.exec_())
    


tableCategories = DfTableCategories()
tabCategories = MyTab(tables = [tableCategories,])       

       
                        
