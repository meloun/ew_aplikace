#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import ewitis.gui.TimesUtils as TimesUtils
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
    (eTOTAL, eCATEGORY, eGROUP) = range(0,3)
    def  __init__(self, params):                                             
         
        #default table constructor
        myModel.myTable.__init__(self, params)
    
    def evaluate(self, rule, order, timestring, minimum = 0, maximum = 9999):
        points = 0

        #rule
        rule = rule.lower()
        
        time = TimesUtils.TimesUtils.timestring2time(timestring)
        
        aux_split = rule.split('%')
        ruletime_string =  aux_split[1] if (len(aux_split) == 3) else None
        ruletime = TimesUtils.TimesUtils.timestring2time(ruletime_string)        
        
        #make expression
        if ruletime:            
            rule = aux_split[0]+str(ruletime)+aux_split[2]            
        expression_string = rule.replace("order", str(order))
        expression_string = expression_string.replace("time", str(time))       
        
        #evaluate
        try:
            #print expression_string
            points = eval(expression_string)        
        except SyntaxError:
            print "E: invalid string for evaluation", expression_string
        
        #restrict               
        if points < minimum:
            points = minimum
        if points > maximum:
            points = maximum                     
        
        #print "points", points
        return points

    
    def getDbPointParOrder(self, order):
        
        if (order == 0) or (order == ""):
            return None
                         
        dbPoint = self.params.db.getParX("Points", "order", order, limit = 1).fetchone()                                
        return dbPoint
    
    def getTabPointParOrder(self, order):                                           
        dbPoint = self.getDbPointParOrder(order)                             
        tabPoint = self.model.db2tableRow(dbPoint)                                   
        return tabPoint
    
    def getPoints(self, tabTime, mode):
        if(mode == self.eTOTAL):
            order = tabTime['order']
        elif(mode == self.eCATEGORY):
            order = tabTime['order_cat']
        elif(mode == self.eGROUP):
            order = tabTime['order']
            
        points = self.params.datastore.Get("points")
        tabPoint = {}
        if(points["table"] == 2):
            tabPoint = self.getTabPointParOrder(order)
        else:                        
            tabPoint['points'] = self.evaluate(points['rule'], order, tabTime['time'], points['minimum'], points['maximum'])
        
        return tabPoint       
                        

                            


        
       


        
        
            
            

        
        
    