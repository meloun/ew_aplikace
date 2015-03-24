#!/usr/bin/env python

from ewitis.gui.aTab import MyTab
from ewitis.gui.aTableModel import myModel, myProxyModel 
from ewitis.gui.aTable import myTable

from ewitis.data.db import db
from ewitis.data.dstore import dstore
import ewitis.gui.TimesUtils as TimesUtils
from ewitis.gui.TimesStore import TimesStore, timesstore
from ewitis.data.DEF_DATA import *
     
             
class PointsModel(myModel):
    def __init__(self, table):                                     
        myModel.__init__(self, table)
          
    def getDefaultTableRow(self): 
        tabRow = myModel.getDefaultTableRow(self)        
        tabRow['points'] = None                                  
        return tabRow                
                    
class PointsProxyModel(myProxyModel):    
    def __init__(self, table):                        
        myProxyModel.__init__(self, table)  
        

# view <- proxymodel <- model 
class Points(myTable):
    (ePOINTS1, ePOINTS2, ePOINTS3) = range(0,3)
    def  __init__(self):                                                     
        myTable.__init__(self, "Points")
    
    #def evaluate(self, formula, tabTime, dbTime):        
    #    return timesstore.Evaluate(None, formula, tabTime, dbTime)        

    
    def getDbPointParOrder(self, order):
        
        if (order == 0) or (order == ""):
            return None
                         
        dbPoint = db.getParX("Points", "order_", order, limit = 1).fetchone()                                
        return dbPoint
    
    def getTabPointParOrder(self, order):                                           
        dbPoint = self.getDbPointParOrder(order)                                     
        tabPoint = self.model.db2tableRow(dbPoint)        
        return tabPoint
    
    def getPoints(self, tabTime, dbTime, index):
        
        if(tabTime['cell'] == 1):                       
            return None
        if(tabTime['time1'] == None):            
            return None
                                        
        tabPoint = self.getTabPointParOrder(tabTime['order'])
                                                     
        
        if isinstance(tabPoint['points'], float):
            tabPoint['points'] = "{0:.2f}".format(tabPoint['points'])         
        return tabPoint['points']       
                        

tablePoints = Points()
tabPoints = MyTab(tables = [tablePoints,])                          


        
       


        
        
            
            

        
        
    