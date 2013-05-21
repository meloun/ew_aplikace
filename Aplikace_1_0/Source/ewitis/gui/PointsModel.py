#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import libs.db_csv.db_csv as Db_csv
import ewitis.gui.DEF_COLUMN as DEF_COLUMN

      
class PointsParameters(myModel.myParameters):
       
    def __init__(self, source):
                                
        #table and db table name
        self.name = "Points"  
        
        #=======================================================================
        # KEYS DEFINITION
        #======================================================================= 
        self.DB_COLLUMN_DEF = DEF_COLUMN.POINTS['database']
        self.TABLE_COLLUMN_DEF = DEF_COLUMN.POINTS['table']
                
        #create MODEL and his structure
        myModel.myParameters.__init__(self, source)                                                                                            
        
        #=======================================================================
        # GUI
        #=======================================================================
        #VIEW   
        self.gui = {}     
        self.gui['view'] = source.ui.PointsProxyView        
        
        #FILTER
        self.gui['filter'] = source.ui.PointsFilterLineEdit
        self.gui['filterclear'] = source.ui.PointsFilterClear
        
        #GROUPBOX
        self.gui['add'] = source.ui.PointsAdd
        self.gui['remove'] =  source.ui.PointsRemove
        self.gui['export'] = source.ui.PointsExport
        self.gui['export_www'] = None
        self.gui['import'] = source.ui.PointsImport 
        self.gui['delete'] = source.ui.PointsDelete
        
        #COUNTER
        self.gui['counter'] = source.ui.PointsCounter
        
        #=======================================================================
        # classes
        #=======================================================================        
        self.classModel = PointsModel                              
        self.classProxyModel = PointsProxyModel
                

class PointsModel(myModel.myModel):
    def __init__(self, params):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)
                                            
    def getDefaultTableRow(self): 
        row = myModel.myModel.getDefaultTableRow(self)                                
        return row 
                    
class PointsProxyModel(myModel.myProxyModel):
    def __init__(self, params):                        
        
        #default proxy-model constructor
        myModel.myProxyModel.__init__(self, params)  
        

# view <- proxymodel <- model 
class Points(myModel.myTable):
    def  __init__(self, params):                                             
         
        #default table constructor
        myModel.myTable.__init__(self, params)         
    
    def getDbPointParOrder(self, order):                 
        dbPoint = self.params.db.getParX("Points", "order", order, limit = 1).fetchone()                                
        return dbPoint
    
    def getTabPointParOrder(self, order):                                 
        dbPoint = self.getDbPointParUserNr(order)                             
        tabPoint = self.model.db2tableRow(dbPoint)                                   
        return tabPoint       
                        

                            


        
       


        
        
            
            

        
        
    