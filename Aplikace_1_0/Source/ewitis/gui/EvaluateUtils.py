#!/usr/bin/env python

from ewitis.data.db import db
from ewitis.data.dstore import dstore
import ewitis.gui.TimesUtils as TimesUtils
from ewitis.gui.TimesLaptimes import cLaptime
from ewitis.data.DEF_DATA import *
from ewitis.gui.TimesStore import timesstore


def Evaluate(formula, tabTime, dbTime):
    points = None
            
    rule = formula['formula']
    minimum = formula['minimum']
    maximum = formula['maximum']
    
    #rule
    rule = rule.lower()
        
    #check if data exist
    if ("time" in rule) and (dbTime['time1'] == None):
        return None
    if ("laptime" in rule) and (dbTime['laptime'] == None):
        return None
    
    
    '''REPLACE keywords'''
    
    # replace time constants: %00:00:01,66% => number(166)
    aux_split = rule.split('%')
    if(len(aux_split) == 3): # 3 parts => ruletime exist, on 2.position                
        try:
            ruletime = TimesUtils.TimesUtils.timestring2time(aux_split[1], including_days = False) #timestring=>time        
        except TimesUtils.TimeFormat_Error:
            return None                                    
        rule = aux_split[0] + str(ruletime) + aux_split[2] #glue expression again

    # replace keywords: order1-3, order_category1-3
    expression_string = rule.replace("order_category", str(tabTime['order_cat']))                            
    expression_string = expression_string.replace("order", str(tabTime['order']))

    # replace keywords: laptime1, laptime2, .., laptime24
    for i in range(1,24):
        laptimeX = "laptime" + str(i)
        if (laptimeX in rule):
            try:                                                
                expression_string = expression_string.replace(laptimeX, str(cLaptime.Get(dbTime, i)))                
            except TypeError:                
                return None
            
    # replace keywords: celltime2, celltime3, .., celltime250
    #
    for i in range(2,25):
        
        #replace index for finishtime
        if i == 25:
            i = 250
        
        timeX = "celltime" + str(i)
        if (timeX in rule):
            try:                                                
                expression_string = expression_string.replace(timeX, str(timesstore.GetPrevious(dbTime, [i,])['time1']))                
            except TypeError:                
                return None
                                       
    # replace keywords: laptime, time        
    expression_string = expression_string.replace("laptime", str(dbTime['laptime']))                                                  
    expression_string = expression_string.replace("time", str(dbTime['time1']))       
            
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