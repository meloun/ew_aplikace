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
from ewitis.gui.dfTableTimes import tableTimes
from ewitis.gui.aTab import MyTab
from ewitis.data.dstore import dstore
from ewitis.gui.Ui import Ui
from manage_calc import manage_calc
from ewitis.gui.events import myevent, myevent2 


'''
Model
'''
class DfModelRuns(DataframeTableModel):
    def __init__(self, name, parent = None):
        super(DfModelRuns, self).__init__(name)        
                      
    #jen prozatim
    def db2tableRow(self, dbRow):
        return dbRow
   
    def GetDataframe(self): 
        df = psql.read_sql(\
            "SELECT id FROM " + str(self.name )
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
    
    def getCategoryParName(self, name):        
        #category = df_utils.Get(self.df, 0, {"name":name})
        categories = self.df[self.df['name'].str.match(name)]          
        category = categories.iloc[0]

                  
        return category
    
    def getCategoriesParGroupLabel(self, label):
        categories = df_utils.Filter(self.df, {label: 1})
        print categories
        return categories

    
    
'''
Proxy Model
'''    
class DfProxymodelRuns(QtGui.QSortFilterProxyModel, ModelUtils):
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
class DfTableRuns(DfTable):
    def  __init__(self):        
        DfTable.__init__(self, "Runs")
        
    def Init(self):
        DfTable.Init(self)
        self.model.Update()
        self.run_id = self.model.df.iloc[-1]['id']        
        dstore.Set("current_run", self.run_id)
        #set selection to first row
        self.gui['view'].selectionModel().setCurrentIndex(self.model.index(0,0), QtGui.QItemSelectionModel.Rows | QtGui.QItemSelectionModel.SelectCurrent)
        
    def InitGui(self):
        DfTable.InitGui(self)        
     
    def createSlots(self):
        DfTable.createSlots(self)           
                
    def Update(self):                                                                                  
        return DfTable.Update(self)
    
    #=======================================================================
    # SLOTS
    #=======================================================================        
    def sSelectionChanged(self, selected, deselected):    
        
           
        idx = selected.indexes()[0]        
        if(self.run_id != self.proxy_model.data(idx).toInt()[0]):             
            self.run_id = self.proxy_model.data(idx).toInt()[0] 
            dstore.Set("current_run", self.run_id)
            myevent.set()              
            time.sleep(0.9)           
            tableTimes.Update()
        
                                       
    
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
    


tableRuns = DfTableRuns()
       

       
                        
