# -*- coding: utf-8 -*-
'''
Created on 10. 4. 2016

@author: Meloun
'''
import time, os
import pandas as pd
import libs.pandas.df_utils as df_utils
from ewitis.data.DEF_DATA import *
from PyQt4 import QtCore, QtGui
from ewitis.gui.Ui import Ui
from ewitis.data.DEF_ENUM_STRINGS import COLORS
from ewitis.data.dstore import dstore
from ewitis.gui.UiAccesories import uiAccesories

gui =  {}
init = False

def InitGui():    
    gui['auto_number_enable'] = Ui().TimesAutoNumberEnable
    gui['auto_number_logic'] = Ui().TimesAutoNumberLogic
    gui['auto_number1'] = Ui().TimesAutoNumber1
    gui['auto_number2'] = Ui().TimesAutoNumber2
    gui['auto_number3'] = Ui().TimesAutoNumber3
    gui['auto_number4'] = Ui().TimesAutoNumber4    
    gui['auto_number_clear'] = Ui().TimesAutoNumberClear
    init = True
    
def createSlots(): 
    QtCore.QObject.connect(gui['auto_number_enable'], QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("times", ["auto_number_enable"], state, UpdateGui))
    QtCore.QObject.connect(gui['auto_number_logic'], QtCore.SIGNAL("toggled(bool)"), lambda state: uiAccesories.sGuiSetItem("times", ["auto_number_logic"], state, UpdateGui))    
    QtCore.QObject.connect(gui['auto_number1'],  QtCore.SIGNAL("valueChanged(int)"),  lambda state: uiAccesories.sGuiSetItem("times", ["auto_number", 0], state, UpdateGui))     
    QtCore.QObject.connect(gui['auto_number2'],  QtCore.SIGNAL("valueChanged(int)"),  lambda state: uiAccesories.sGuiSetItem("times", ["auto_number", 1], state, UpdateGui))
    QtCore.QObject.connect(gui['auto_number3'],  QtCore.SIGNAL("valueChanged(int)"),  lambda state: uiAccesories.sGuiSetItem("times", ["auto_number", 2], state, UpdateGui))
    QtCore.QObject.connect(gui['auto_number4'],  QtCore.SIGNAL("valueChanged(int)"),  lambda state: uiAccesories.sGuiSetItem("times", ["auto_number", 3], state, UpdateGui))        
    QtCore.QObject.connect(gui['auto_number_clear'],  QtCore.SIGNAL("clicked()"),  lambda: uiAccesories.sGuiSetItem("times", ["auto_number"], [0]*NUMBER_OF.AUTO_NUMBER, UpdateGui))
    
def UpdateGui():
    times = dstore.Get("times")
    racesettings = dstore.Get("racesettings-app")
        
    gui['auto_number_enable'].setCheckState(times["auto_number_enable"])
    gui['auto_number_logic'].setChecked(times["auto_number_logic"])
    
    if(times["auto_number_enable"] == 0):
        """ everything off """
        gui['auto_number_logic'].setEnabled(False)
        for i in range(0, NUMBER_OF.AUTO_NUMBER):
            gui['auto_number'+str(i+1)].setEnabled(False)
    else:
        gui['auto_number_logic'].setEnabled(True)
        if(times["auto_number_logic"] == 0):
            """primitive auto number """
            gui['auto_number1'].setEnabled(True)
            for i in range(1, NUMBER_OF.AUTO_NUMBER):
                gui['auto_number'+str(i+1)].setEnabled(False)
        else:
            """auto numbers full logic"""
            for i in range(0, NUMBER_OF.AUTO_NUMBER):     
                if(i < dstore.GetItem("racesettings-app", ["autonumbers", "nr_users"])):
                    gui['auto_number'+str(i+1)].setEnabled(True)
                else:
                    gui['auto_number'+str(i+1)].setEnabled(False)

    #set autonumbers value  
    for i in range(0, NUMBER_OF.AUTO_NUMBER):  
        #if self.gui['auto_number'+str(i+1)].hasFocus() == False:                                                                               
        if gui['auto_number'+str(i+1)].text() != '' and gui['auto_number'+str(i+1)].text() != '-':                                                                               
            gui['auto_number'+str(i+1)].setValue(times["auto_number"][i])

    for nr in range(NUMBER_OF.AUTO_NUMBER):
        if(times["auto_number"][nr] == 0) or (init == False):            
            gui['auto_number'+str(nr+1)].setStyleSheet("")
        else:
            if(tableUsers.model.getUserParNr(times["auto_number"][nr]) != None):
                if(gui['auto_number'+str(nr+1)].styleSheet() != "background:"+COLORS.green):
                    gui['auto_number'+str(nr+1)].setStyleSheet("")
            else:
                if(gui['auto_number'+str(nr+1)].styleSheet() != "background:"+COLORS.red):
                    gui['auto_number'+str(nr+1)].setStyleSheet("background:"+COLORS.red)
                    
def Update(df, new_time):        
    ret = []        
    
    cells = dstore.GetItem("racesettings-app", ["autonumbers", "cells"])
    nr_cells = dstore.GetItem("racesettings-app", ["autonumbers", "nr_cells"])

    """for one new time"""
    for number in dstore.GetItem("times", ["auto_number"]):            
        """test if this user should be taken"""

        #print "number", number
        #if number == 0: #number not set
        #    continue
        
        #get position of new time (first from defined list)
        try:
            cell_position = cells.index(new_time["cell"])
            #print "cp:", cell_position            
        except ValueError:            
            continue
                  
        # get starttime         
        #starttime = GetStartime2(df, number) #bug cell 2,250
        starttime = GetLasttime(df, number, cells[0])        
        
        if starttime != None:                                    
            sequence_times = df[(df.nr==number)  & (df.id >= starttime['id'])]
            sequence_cells = list(sequence_times.cell)
        else:            
            sequence_cells = []         

        if (
                (new_time["cell"]) == 1 and (sequence_cells ==  cells[:nr_cells]) or
                (sequence_cells ==  cells[:cell_position])
            ):
            
            #print "I: auto number: MATCH nr.", number
            ret.append({"id":new_time["id"], "nr": number})                
            if cell_position == (nr_cells - 1):
                #print "I: auto number: run finished - shifting nr.", number
                ShiftNumbers()
            return ret
        else:
            pass
            #print "I: auto number: NO MATCH nr.", number, sequence_cells, cells[:cell_position]
                                                
    return ret
        

def GetStartime(df, nr):
    
    if df.empty:
        return None
    
    try:      
        starttime = df[(df.nr==nr) & (df.cell ==1)].iloc[-1]
        starttime = dict(starttime)
    except IndexError, AttributeError:
        starttime = None
    
    return starttime

def GetLasttime(df, nr, cell):
    
    if df.empty:
        return None
    
    try:              
        starttime = df[(df.nr==nr) & (df.cell == int(cell))].iloc[-1]
        starttime = dict(starttime)
    except IndexError, AttributeError:
        starttime = None
    
    return starttime
    

def ShiftNumbers():        
    nrs = dstore.GetItem("times", ["auto_number"])
    nrs = nrs[1:]+[0]
    dstore.SetItem("times", ["auto_number"], nrs)
    
        
