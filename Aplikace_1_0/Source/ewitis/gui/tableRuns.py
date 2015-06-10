# -*- coding: utf-8 -*-

import time
from PyQt4 import QtCore, QtGui
from ewitis.gui.aTab import MyTab 
from ewitis.gui.aTableModel import myModel, myProxyModel 
from ewitis.gui.aTable import myTable
from ewitis.gui.tableTimes import tableTimes
from ewitis.data.db import db
from ewitis.data.dstore import dstore
import ewitis.gui.DEF_COLUMN as DEF_COLUMN
from manage_calc import manage_calc, myevent 

class RunsModel(myModel):
    def __init__(self, table):                                        
        myModel.__init__(self, table)
                 
                
    #setting flags for this model        
    #first collumn is NOT editable
    def flags(self, index):
        aux_flags = 0
                
        #id, name, category, addres NOT editable
#        if ((index.column() == 2) and (self.params.guidata.table_mode !=  GuiData.MODE_REFRESH)):
#            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
        return myModel.flags(self, index)
    
                
    def db2tableRow(self, run):                        
        
        #get USER
        user = db.getParX("users", "id", run["name_id"]).fetchone()
        
        #exist user?
        if user == None:
            run['name']='unknown'
        #exist => restrict username                
        else:
            if(user['name']==''):
                run['name'] = 'nobody'
            run['name'] = user['name']
                                
        return run
    
        

class RunsProxyModel(myProxyModel):
    def __init__(self, table):                
        myProxyModel.__init__(self, table)        
    
# view <- proxymodel <- model 
class Runs(myTable):
    def  __init__(self):                        
                                      
        myTable.__init__(self, "Runs")        
                       
    def  Init(self):
                                
        myTable.Init(self)
                
        #set default sorting
        self.gui['view'].sortByColumn(0, QtCore.Qt.DescendingOrder)
            
        #MODE EDIT/REFRESH        
        self.system = 0
        
        first_run = db.getFirst("runs")
        if(first_run != None):
            self.run_id = first_run['id']
        else:
            self.run_id = 0 #no times for run_id = 0
        dstore.Set("current_run", self.run_id)
        #self.run_id = 0                       
                               
        #set selection to first row
        self.gui['view'].selectionModel().setCurrentIndex(self.model.index(0,0), QtGui.QItemSelectionModel.Rows | QtGui.QItemSelectionModel.SelectCurrent)                
            
        #update table times (use selection to define run_id)                
        #self.updateTimes()
        
    
    #=======================================================================
    # SLOTS
    #=======================================================================        
    def sSelectionChanged(self, selected, deselected):    
        #print "Runs: selection changed", dstore.Get("user_actions"), selected            
        if(selected) and (dstore.Get("user_actions") == 0):                            
                self.updateTimes()  #update TIMES table
                   
    # CLEAR FILTER BUTTON -> CLEAR FILTER        
    def sFilterClear(self): 
        myTable.sFilterClear(self)
        tableTimes.Update()   
        
                        
    # FILTER CHANGE -> CHANGE TABLE
    def sFilterRegExp(self):    
        myTable.sFilterRegExp(self)
        #for tests, self.params.tabTimes.update()
        
        
    #=======================================================================
    # UPDATE TIMES
    #=======================================================================    
    # function for update table TIMES according to selection in RUNS
    def updateTimes(self):                 
                                 
        #get index of selected ID (from tableRuns)         
        rows = self.gui['view'].selectionModel().selectedRows() #default collumn = 0        
                                                              
        #update table times with run_id
        try:             
            #ziskani id z vybraneho radku                                         
            self.run_id = (self.proxy_model.data(rows[0]).toInt()[0])                 
                                     
            #update table times
            dstore.Set("current_run", self.run_id)
            myevent.set()              
            time.sleep(0.4)                                     
            tableTimes.Update()                                                                          
        except:
            print "I: Times: nelze aktualizovat! id:", self.run_id                    
        
    # REMOVE ROW               
    def sDelete(self):
        
        #delete run with additional message
        myTable.sDelete(self, "and ALL TIMES belonging to him")
        
        #delete times
        db.deleteParX("times", "run_id", self.run_id)
        myevent.set()
        time.sleep(0.4)               
        tableTimes.Update()
        
    def deleteAll(self):        
        myTable.deleteAll(self)
        tableTimes.deleteAll()
        myevent.set()
        time.sleep(0.4)               
        tableTimes.Update()
        
        
tableRuns = Runs()
          
        
                                   
         
                               
