#!/usr/bin/env python

from ewitis.data.db import db
from ewitis.data.dstore import dstore
import ewitis.gui.TimesUtils as TimesUtils
from ewitis.gui.TimesLaptimes import cLaptime
from ewitis.data.DEF_DATA import *
from ewitis.gui.TimesStore import timesstore
from ewitis.gui.tableCategories import tableCategories
from ewitis.gui.tableUsers import tableUsers


def Evaluate(rule, tabTime, dbTime):
    points = None
            
    rule = rule['rule']
    
    minimum =  rule['minimum'] if ('minimum' in rule) else None
    maximum = rule['maximum'] if ('maximum' in rule) else None
    
    #rule
    rule = rule.lower()
        
    #check if data exist
    if ("time1" in rule) and (dbTime['time1'] == None):    
        return None
    if ("time2" in rule) and (dbTime['time2'] == None):        
        return None
    if ("time3" in rule) and (dbTime['time3'] == None):        
        return None

    
    
    '''REPLACE keywords'''
    
    # TIME CONSTANT: %00:00:01,66% => number(166)
    aux_split = rule.split('%')
    if(len(aux_split) == 3): # 3 parts => ruletime exist, on 2.position                
        try:
            ruletime = TimesUtils.TimesUtils.timestring2time(aux_split[1], including_days = False) #timestring=>time        
        except TimesUtils.TimeFormat_Error:            
            return None                                    
        rule = aux_split[0] + str(ruletime) + aux_split[2] #glue expression again

    # ORDER1-ORDER3
    expression_string = rule 
       
    try:
        if ("order1" in rule):                                
            expression_string = expression_string.replace("order1", str(tabTime['order1']))
        if ("order2" in rule):                                
            expression_string = expression_string.replace("order2", str(tabTime['order2']))
        if ("order3" in rule):                                
            expression_string = expression_string.replace("order3", str(tabTime['order3']))
    except KeyError:        
        return None
           
    # CELLTIME2 - CELLTIME250
    for i in range(2,25):
        
        #replace index for finishtime
        if i == 25:
            i = 250
        
        celltimeX = "celltime" + str(i)
        if (celltimeX in rule):
            try:                                                
                expression_string = expression_string.replace(celltimeX, str(timesstore.GetPrevious(dbTime, [i,])['time1']))                
            except TypeError:       
                print "type error"         
                return None
            
    # STARTTIME    
    #user without number => no time
    if ("starttime" in rule):
        starttime = None          
        tabUser =  tableUsers.getTabUserParIdOrTagId(dbTime["user_id"])          
        if(tabUser['nr'] == 0):
            return None        
    
        if(dstore.Get('evaluation')['starttime'] == StarttimeEvaluation.VIA_CATEGORY):
            #VIA CATEGORY => Xth starttime                                                                                                                              
            start_nr = tableCategories.getTabRow(tabUser['category_id'])['start_nr'] #get category starttime                
            starttime = timesstore.Get(start_nr, cells = [1,])                                    
        elif(dstore.Get('evaluation')['starttime'] == StarttimeEvaluation.VIA_USER):
            #VIA USER => previous startime from the same user                                        
            starttime = timesstore.GetPrevious(dbTime, cells = [1,])
        
        if starttime != None:
            expression_string = rule.replace("starttime", str(starttime['time_raw']))
                    
                                       
           
    # TIME1-TIME3                                                        
    expression_string = expression_string.replace("time1", str(dbTime['time1']))       
    expression_string = expression_string.replace("time2", str(dbTime['time2']))       
    expression_string = expression_string.replace("time3", str(dbTime['time3']))
           
    # TIME
    expression_string = expression_string.replace("time", str(dbTime['time_raw']))
            
    ''' evaluate expresion '''
    try:            
        points = eval(expression_string)        
    except (SyntaxError, TypeError, NameError):
        print "I: invalid string for evaluation", expression_string            
        return None        
    
    #restrict final value               
    if minimum and (points < minimum):
        points = minimum
    if maximum and (points > maximum):
        points = maximum                     
            
    return points