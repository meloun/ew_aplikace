#!/usr/bin/env python

from ewitis.gui.aTab import MyTab
from ewitis.gui.aTableModel import myModel, myProxyModel 
from ewitis.gui.aTable import myTable

from ewitis.data.db import db
from ewitis.data.dstore import dstore
import ewitis.gui.TimesUtils as TimesUtils
from ewitis.gui.EvaluateUtils import Evaluate
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
    
    def evaluate(self, formula, tabTime, dbTime):        
        return Evaluate(formula, tabTime, dbTime)        

    
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
                       
            
        #points_evaluation = dstore.Get("evaluation")["points"]
        points_evaluation = PointsEvaluation.FROM_FORMULA
        
        tabPoint = {}
        if(points_evaluation == PointsEvaluation.FROM_TABLE):                                  
            tabPoint = self.getTabPointParOrder(tabTime['order'])
        else:                      
            points_formula = dstore.Get("additional_info")["points"][index]                                                                        
            tabPoint['points'] = self.evaluate(points_formula, tabTime, dbTime)                                                    
        
        if isinstance(tabPoint['points'], float):
            tabPoint['points'] = "{0:.2f}".format(tabPoint['points'])         
        return tabPoint['points']       
                        

tablePoints = Points()
tabPoints = MyTab(tables = [tablePoints,])                          


        
       


        
        
            
            

        
        
    