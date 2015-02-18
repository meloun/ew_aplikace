# -*- coding: utf-8 -*-
'''
Created on 18.02.2015

@author: lubos.melichar
'''
from PyQt4 import QtCore
from ewitis.data.DEF_DATA import NUMBER_OF, Assigments2Dict
from ewitis.data.DEF_ENUM_STRINGS import *
from ewitis.gui.UiAccesories import uiAccesories
from ewitis.gui.Ui import Ui
from ewitis.data.dstore import dstore
import libs.utils.utils as utils
from ewitis.data.DEF_ENUM_STRINGS import COLORS

class FilterGroup():    
    def __init__(self,  nr, name):
        '''        
        checkbox + filter        
        '''
        ui = Ui()        
        self.nr = nr
        self.name = name.lower()
        
        self.checked = getattr(ui, "checkAInfo"+name+ "_"+str(nr))                                     
        self.filter = getattr(ui, "lineAInfo"+name+"Filter_" + str(nr))                                              

    def CreateSlots(self):
        QtCore.QObject.connect(self.checked, QtCore.SIGNAL("stateChanged(int)"), lambda x: uiAccesories.sGuiSetItem("additional_info", [self.name, self.nr-1, "checked"], x, self.Update))                                          
        QtCore.QObject.connect(self.filter, QtCore.SIGNAL("textEdited(const QString&)"), lambda x: uiAccesories.sGuiSetItem("additional_info", [self.name, self.nr-1, "filter"], utils.toUnicode(x)))            
        
    def GetInfo(self):
        return dstore.GetItem("additional_info", [ self.name, self.nr-1])                 
    
     
    def setEnabled(self, enabled):                
        self.filter.setEnabled(enabled)
    
    def Update(self):        
        # set values from datastore              
        info = self.GetInfo()                                                                    
        self.checked.setChecked(info["checked"])         
        uiAccesories.UpdateText(self.filter, info["filter"])
        
        self.setEnabled(info["checked"])
        
        #filter color
        filter_dict = Assigments2Dict(dstore.GetItem("additional_info", [ self.name, self.nr-1])['filter'])        
        if(dstore.GetItem("additional_info", [ self.name, self.nr-1])['filter'] == ""):
            self.filter.setStyleSheet("background:"+COLORS.GetColor(None))  
        else:                    
            self.filter.setStyleSheet("background:"+COLORS.GetColor(filter_dict != None))