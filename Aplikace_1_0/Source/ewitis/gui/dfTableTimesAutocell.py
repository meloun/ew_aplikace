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
    gui['auto_cell_address'].setCurrentIndex(times["auto_cell_address"])
    for nr in range(NUMBER_OF.AUTO_NUMBER):                      
        gui['auto_cell_'+str(nr+1)].setValue(times["auto_cell"][nr])
        

def Update(df, new_time):
        
    pass

    
        
