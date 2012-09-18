# -*- coding: utf-8 -*-
#!/usr/bin/env python
# 
#
#
#

import sys
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import ewitis.gui.DEF_COLUMN as DEF_COLUMN


class RunsParameters(myModel.myParameters):
    def __init__(self, source):                
                        
        #table and db table name
        self.name = "Runs" 
        
        #TABLE TIMES
        self.tabTimes = source.T 
        
        #=======================================================================
        # KEYS
        #=======================================================================
        self.DB_COLLUMN_DEF = DEF_COLUMN.RUNS['database'] 
        self.TABLE_COLLUMN_DEF = DEF_COLUMN.RUNS['table']
        
        #create MODEL and his structure
        myModel.myParameters.__init__(self, source)
                                  
        #=======================================================================
        # GUI
        #=======================================================================
        self.gui = {} 
        #VIEW
        self.gui['view'] = source.ui.RunsProxyView
        
        #FILTER
        self.gui['filter'] = source.ui.RunsFilterLineEdit
        self.gui['filterclear'] = source.ui.RunsFilterClear
        
        #GROUPBOX
        self.gui['add'] = source.ui.RunsAdd
        self.gui['remove'] =  source.ui.RunsRemove
        self.gui['export'] = source.ui.RunsExport
        self.gui['export_www'] = None
        self.gui['import'] = None 
        self.gui['delete'] = source.ui.RunsDelete
        
        #COUNTER
        self.gui['counter'] = source.ui.runsCounter
        
        #=======================================================================
        # classes
        #=======================================================================        
        self.classModel = RunsModel                              
        self.classProxyModel = RunsProxyModel
                 
        

class RunsModel(myModel.myModel):
    def __init__(self, params):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)
                 
                
    #setting flags for this model        
    #first collumn is NOT editable
    def flags(self, index):
        aux_flags = 0
                
        #id, name, category, addres NOT editable
#        if ((index.column() == 2) and (self.params.guidata.table_mode !=  GuiData.MODE_REFRESH)):
#            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
        return myModel.myModel.flags(self, index)
    
                
    def db2tableRow(self, run):                        
        
        #get USER
        user = self.params.db.getParX("users", "id", run["name_id"]).fetchone()
        
        #exist user?
        if user == None:
            run['name']='unknown'
        #exist => restrict username                
        else:
            if(user['name']==''):
                run['name'] = 'nobody'
            run['name'] = user['name']
                                
        return run
    
    def table2dbRow(self, run_table, item = None): 
        run_db = {"id" : run_table['id'], "date" : run_table['date'], "description" :  run_table['description']}                                                                       
        return run_db
    
    
        

class RunsProxyModel(myModel.myProxyModel):
    def __init__(self, params):                        
        
        #create PROXYMODEL
        myModel.myProxyModel.__init__(self, params)        
        
              
        
    
# view <- proxymodel <- model 
class Runs(myModel.myTable):
    def  __init__(self, params):                        
                                      
        myModel.myTable.__init__(self, params)        
                       
        #set default sorting
        self.params.gui['view'].sortByColumn(0, QtCore.Qt.DescendingOrder)
    
        
        #MODE EDIT/REFRESH        
        self.system = 0                       
                               
        #set selection to first row
        self.params.gui['view'].selectionModel().setCurrentIndex(self.model.index(0,0), QtGui.QItemSelectionModel.Rows | QtGui.QItemSelectionModel.SelectCurrent)                
            
        #update table times (use selection to define run_id)                
        #self.updateTimes()
        
    
    #=======================================================================
    # SLOTS
    #=======================================================================        
    def sSelectionChanged(self, selected, deselected):    
        #print "Runs: selection changed", self.params.datastore.Get("user_actions"), selected            
        if(selected) and (self.params.datastore.Get("user_actions") == 0):                            
                self.updateTimes()  #update TIMES table
                   
    # CLEAR FILTER BUTTON -> CLEAR FILTER        
    def sFilterClear(self): 
        myModel.myTable.sFilterClear(self)
        self.params.tabTimes.update()   
        
                        
    # FILTER CHANGE -> CHANGE TABLE
    def sFilterRegExp(self):    
        myModel.myTable.sFilterRegExp(self)
        self.params.tabTimes.update()
        
        
    #=======================================================================
    # UPDATE TIMES
    #=======================================================================    
    # function for update table TIMES according to selection in RUNS
    def updateTimes(self):         
                         
        #get index of selected ID (from tableRuns)         
        rows = self.params.gui['view'].selectionModel().selectedRows() #default collumn = 0
                                      
        #update table times with run_id
        try:             
            #ziskani id z vybraneho radku                                         
            self.run_id = (self.proxy_model.data(rows[0]).toInt()[0])                 
                                     
            #get TIMES from database & add them to the table              
            self.params.tabTimes.update(run_id = self.run_id)                                     
        except:
            print "I: Times: nelze aktualizovat!"        
        
    # REMOVE ROW               
    def sDelete(self):
        
        #delete run with additional message
        myModel.myTable.sDelete(self, "and ALL TIMES belonging to him")
        
        #delete times
        self.params.tabTimes.params.db.deleteParX("times", "run_id", self.run_id)               
        self.params.tabTimes.update()
        
    def deleteAll(self):        
        myModel.myTable.deleteAll(self)
        self.params.tabTimes.deleteAll()
        
        
         
        
                                   
         
                               
