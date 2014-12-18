#!/usr/bin/env python

from ewitis.gui.aTab import MyTab
from ewitis.gui.aTableModel import myModel, myProxyModel 
from ewitis.gui.aTable import myTable

from ewitis.data.db import db
from ewitis.data.dstore import dstore
import ewitis.gui.TimesUtils as TimesUtils
from ewitis.gui.TimesLaptimes import cLaptime
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
        points = None
                
        rule = formula['formula']
        minimum = formula['minimum']
        maximum = formula['maximum']
        
        #rule
        rule = rule.lower()
            
        #check if data exist
        if ("time" in rule) and (dbTime['time'] == None):
            return None
        if ("laptime" in rule) and (dbTime['laptime'] == None):
            return None
        
        
        '''REPLACE keywords'''
        
        # replace keyword: %00:00:01,66% to number(166)
        aux_split = rule.split('%')
        if(len(aux_split) == 3): # 3 parts => ruletime exist, on 2.position                
            try:
                ruletime = TimesUtils.TimesUtils.timestring2time(aux_split[1], including_days = False) #timestring=>time        
            except TimesUtils.TimeFormat_Error:
                return None                                    
            rule = aux_split[0] + str(ruletime) + aux_split[2] #glue expression again

        # replace keywords: order, order_cat
        expression_string = rule.replace("order_cat", str(tabTime['order_cat']))                            
        expression_string = expression_string.replace("order", str(tabTime['order']))

        # replace keywords: laptime1, laptime2, .., laptime24
        for i in range(1,24):
            laptimeX = "laptime" + str(i)
            if (laptimeX in rule):
                try:                                                
                    expression_string = expression_string.replace(laptimeX, str(cLaptime.Get(dbTime, i)))                
                except TypeError:                
                    return None
                                           
        # replace keywords: laptime, time        
        expression_string = expression_string.replace("laptime", str(dbTime['laptime']))                                                  
        expression_string = expression_string.replace("time", str(dbTime['time']))       
                
        ''' evaluate expresion '''
        try:            
            points = eval(expression_string)        
        except (SyntaxError, TypeError, NameError):
            print "I: invalid string for evaluation", expression_string            
            return None        
        
        #restrict final value               
        if points < minimum:
            points = minimum
        if points > maximum:
            points = maximum                     
                
        return points

    
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
        if(tabTime['time'] == None):            
            return None        
                       
            
        points_evaluation = dstore.Get("evaluation")["points"]
        tabPoint = {}
        if(points_evaluation == PointsEvaluation.FROM_TABLE):                                  
            tabPoint = self.getTabPointParOrder(tabTime['order'])
        else:                      
            points_formula = dstore.Get("evaluation")["points_formula"][index]                                                                        
            tabPoint['points'] = self.evaluate(points_formula, tabTime, dbTime)                                                    
        
        if isinstance(tabPoint['points'], float):
            tabPoint['points'] = "{0:.2f}".format(tabPoint['points'])         
        return tabPoint['points']       
                        

tablePoints = Points()
tabPoints = MyTab(tables = [tablePoints,])                          


        
       


        
        
            
            

        
        
    