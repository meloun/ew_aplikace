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

def InitGui():
    gui['auto_cell_address'] = Ui().TimesAutoCell_Address
    gui['auto_cell_1'] = Ui().TimesAutoCell1
    gui['auto_cell_2'] = Ui().TimesAutoCell2
    gui['auto_cell_3'] = Ui().TimesAutoCell3
    gui['auto_cell_4'] = Ui().TimesAutoCell4
    gui['auto_cell_clear'] = Ui().TimesAutoCellClear
    
def createSlots():
    QtCore.QObject.connect(gui['auto_cell_1'],  QtCore.SIGNAL("valueChanged(int)"),  lambda state: uiAccesories.sGuiSetItem("times", ["auto_cell", 0], state, UpdateGui))
    QtCore.QObject.connect(gui['auto_cell_2'],  QtCore.SIGNAL("valueChanged(int)"),  lambda state: uiAccesories.sGuiSetItem("times", ["auto_cell", 1], state, UpdateGui))
    QtCore.QObject.connect(gui['auto_cell_3'],  QtCore.SIGNAL("valueChanged(int)"),  lambda state: uiAccesories.sGuiSetItem("times", ["auto_cell", 2], state, UpdateGui))
    QtCore.QObject.connect(gui['auto_cell_4'],  QtCore.SIGNAL("valueChanged(int)"),  lambda state: uiAccesories.sGuiSetItem("times", ["auto_cell", 3], state, UpdateGui))
    QtCore.QObject.connect(gui['auto_cell_clear'],  QtCore.SIGNAL("clicked()"),  lambda: uiAccesories.sGuiSetItem("times", ["auto_cell"], [0]*NUMBER_OF.AUTO_NUMBER, UpdateGui))
    QtCore.QObject.connect(gui['auto_cell_address'], QtCore.SIGNAL("activated(int)"), sComboAutoCellAddress)
    
def sComboAutoCellAddress(index):
    uiAccesories.sGuiSetItem("times", ["auto_cell_address"], index, UpdateGui)

def UpdateGui():
    times = dstore.Get("times")
    racesettings = dstore.Get("racesettings-app")
    gui['auto_cell_address'].setCurrentIndex(times["auto_cell_address"])
    for nr in range(NUMBER_OF.AUTO_CELL):                      
        #value
        gui['auto_cell_'+str(nr+1)].setValue(times["auto_cell"][nr])
        
        #enable/disable
        if (nr < racesettings["autocell"]["nr_cells"]) and (racesettings["autocell"]["nr_cells"] != 0):
            gui['auto_cell_'+str(nr+1)].setEnabled(True)
            gui['auto_cell_address'].setEnabled(True)
        else:
            gui['auto_cell_'+str(nr+1)].setEnabled(False)
            gui['auto_cell_address'].setEnabled(False)
                
        #stylesheets
        if(nr == times["auto_cell_index"]) and (times["auto_cell_address"] != 0) and (racesettings["autocell"]["nr_cells"] != 0):
            gui['auto_cell_'+str(nr+1)].setStyleSheet("background:"+COLORS.green)
        else:
            gui['auto_cell_'+str(nr+1)].setStyleSheet("")
    
    #enable/disable combobox address
    if (racesettings["autocell"]["nr_cells"] != 0):       
        gui['auto_cell_address'].setEnabled(True)
    else:
        
        gui['auto_cell_address'].setEnabled(False)
        
    #check
    #settings change and index is high
    if(times["auto_cell_index"] >= racesettings["autocell"]["nr_cells"]) and (racesettings["autocell"]["nr_cells"] != 0):
        print "W: autocell index changed to zero (probably setting change and index too high)"
        times["auto_cell_index"] = 0;
        
    
        
