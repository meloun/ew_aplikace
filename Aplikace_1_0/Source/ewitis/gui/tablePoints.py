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
    
    def evaluate(self, formula, time):
        points = None
                
        rule = formula['formula']
        minimum = formula['minimum']
        maximum = formula['maximum']

        
        #check if data exist
        if ("time" in rule) and (time['time'] == None):
            return None
        if ("laptime" in rule) and (time['laptime'] == None):
            return None
        
        #rule
        rule = rule.lower()    
        
        #convert %rule-timestring% to ruletime(number)
        aux_split = rule.split('%')
        if(len(aux_split) == 3): #3 parts => ruletime exist, on 2.position                
            try:
                ruletime = TimesUtils.TimesUtils.timestring2time(aux_split[1], including_days = False) #timestring=>time        
            except TimesUtils.TimeFormat_Error:
                return None                    
            #glue expression again                        
            rule = aux_split[0]+str(ruletime)+aux_split[2]

        #replace keywords with time values
        expression_string = rule.replace("order_cat", str(time['order_cat']))                            
        expression_string = expression_string.replace("order", str(time['order']))
        #if ("laptime" in rule):
        #    expression_string = expression_string.replace("laptime", str(TimesUtils.TimesUtils.timestring2time(time['laptime'] , including_days = False)))
        if ("laptime1" in rule):
            try:
                print "p:", cLaptime.Get(time, 1)
                print "a",expression_string
                expression_string = expression_string.replace("laptime1", cLaptime.Get(time, 1))
                print "b",expression_string
            except:
                return None  
            print "es: ", expression_string           
        if ("time" in rule):                    
            expression_string = expression_string.replace("time", str(TimesUtils.TimesUtils.timestring2time(time['time'] , including_days = False)))       
                
        #evaluate
        try:            
            points = eval(expression_string)        
        except (SyntaxError,TypeError,NameError):
            print "I: invalid string for evaluation", expression_string
            points = expression_string
            #return None        
        
        #restrict               
#        if points < minimum:
#            points = minimum
#        if points > maximum:
#            points = maximum                     
        
        #print "points", points
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
    
    def getPoints(self, tabTime, key = "points_formula1"):
        
        if(tabTime['cell'] == 1):           
            return None
        if(tabTime['time'] == None):            
            return None        
                       
            
        points_evaluation = dstore.Get("evaluation")["points"]
        tabPoint = {}
        if(points_evaluation == PointsEvaluation.FROM_TABLE):            
            tabPoint = self.getTabPointParOrder(order)
        else:
            points_formula = dstore.Get("evaluation")[key]                                                                        
            #tabPoint['points'] = self.evaluate(points_formula['formula'], order, order_cat, tabTime['time'], tabTime['laptime'], points_formula['minimum'], points_formula['maximum'])                    
            tabPoint['points'] = self.evaluate(points_formula, tabTime)                    
        
        if isinstance(tabPoint['points'], float):
            tabPoint['points'] = "{0:.2f}".format(tabPoint['points'])         
        return tabPoint['points']       
                        

tablePoints = Points()
tabPoints = MyTab(tables = [tablePoints,])                          


        
       


        
        
            
            

        
        
    