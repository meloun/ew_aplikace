'''
Created on 23. 3. 2018

@author: Meloun
'''

from PyQt4 import QtCore
from ewitis.data.DEF_DATA import NUMBER_OF, Assigments2Dict
from ewitis.data.DEF_ENUM_STRINGS import *
from ewitis.gui.tabExportSettings import tabExportSettings
from ewitis.gui.UiAccesories import uiAccesories

from ewitis.gui.Ui import Ui
from ewitis.data.dstore import dstore
import libs.utils.utils as utils
from ewitis.data.DEF_ENUM_STRINGS import COLORS
from libs.myqt.mygroups import FilterGroup
import simplejson as json
import codecs 
   
class TimesGroup(FilterGroup):    
    def __init__(self,  nr):
        self.rule = getattr(Ui(), "lineAInfoTimeRule_" + str(nr))
        self.minute_timeformat = getattr(Ui(), "checkExportMinuteTimeformat_" + str(nr)) 
        FilterGroup.__init__(self, nr, "Time")

    def CreateSlots(self):
        QtCore.QObject.connect(self.rule, QtCore.SIGNAL("textEdited(const QString&)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["time", self.nr-1, "rule"], utils.toUnicode(x)))
        QtCore.QObject.connect(self.minute_timeformat, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["time", self.nr-1, "minute_timeformat"], state, self.Update))            
        FilterGroup.CreateSlots(self)                                                                                    
     
    def setEnabled(self, enabled):
        self.rule.setEnabled(enabled)        
        self.minute_timeformat.setEnabled(enabled)
        FilterGroup.setEnabled(self, enabled)
    
    def Update(self):        
        # set values from datastore              
        info = self.GetInfo()                                                                            
        uiAccesories.UpdateText(self.rule, info["rule"])        
        self.minute_timeformat.setCheckState(info["minute_timeformat"]) 
        FilterGroup.Update(self)

class LapGroup(FilterGroup):    
    def __init__(self,  nr):                
        self.fromlaststart = getattr(Ui(), "checkAI_FromLastStart_Lap_" + str(nr)) 
        FilterGroup.__init__(self, nr, "Lap")

    def CreateSlots(self):        
        QtCore.QObject.connect(self.fromlaststart, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["lap", self.nr-1, "fromlaststart"], state, self.Update))            
        FilterGroup.CreateSlots(self)                                                                                    
     
    def setEnabled(self, enabled):                
        self.fromlaststart.setEnabled(enabled)
        FilterGroup.setEnabled(self, enabled)
    
    def Update(self):        
        # set values from datastore              
        info = self.GetInfo()                
        self.fromlaststart.setCheckState(info["fromlaststart"]) 
        FilterGroup.Update(self)        
                  
                
class PointGroup():    
    def __init__(self,  nr):
        '''
        Constructor
        group items as class members        
        '''
        ui = Ui()
        
        self.nr = nr
            
        self.checked = getattr(ui, "checkAInfoPoints_" + str(nr))        
        self.rule = getattr(ui, "lineAInfoPointRule_" + str(nr))     
        self.minimum = getattr(ui, "spinAInfoPointMinimum_" + str(nr))
        self.maximum = getattr(ui, "spinAInfoPointMaximum_" + str(nr))                                                                                         

    def CreateSlots(self):
                                             
        QtCore.QObject.connect(self.checked, QtCore.SIGNAL("stateChanged(int)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["points", self.nr-1, "checked"], x, self.Update))                          
        QtCore.QObject.connect(self.rule, QtCore.SIGNAL("textEdited(const QString&)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["points", self.nr-1, "rule"], utils.toUnicode(x)))            
        QtCore.QObject.connect(self.minimum, QtCore.SIGNAL("valueChanged(int)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["points", self.nr-1, "minimum"], x, self.Update))
        QtCore.QObject.connect(self.maximum, QtCore.SIGNAL("valueChanged(int)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["points", self.nr-1, "maximum"], x, self.Update))

    def GetInfo(self):
        return dstore.GetItem("additional_info", [ "points", self.nr-1])
     
    def setEnabled(self, enabled):
        self.rule.setEnabled(enabled)        
        self.minimum.setEnabled(enabled)          
        self.maximum.setEnabled(enabled)       
    
    def Update(self):                                    
        # set values from datastore
        info = self.GetInfo()  
                            
        self.checked.setChecked(info["checked"])
        self.minimum.setValue(info["minimum"])
        self.maximum.setValue(info["maximum"])
        uiAccesories.UpdateText(self.rule, info["rule"])
        
        self.setEnabled(info["checked"]) 
                              
                                                  
class OrderGroup():    
    def __init__(self,  nr):
        '''
        Constructor
        group items as class members        
        '''
        ui = Ui()        
        self.nr = nr
        
        self.checked = getattr(ui, "checkAInfoOrder_" + str(nr))
        self.type = getattr(ui, "comboOrderType_" + str(nr))        
        self.row = getattr(ui,    "comboOrderRow_" + str(nr))
        self.column1 = getattr(ui, "comboOrderColumn_" + str(nr) + "_1")                                
        self.order1 = getattr(ui,  "comboOrderOrder_" + str(nr) + "_1")
        self.column2 = getattr(ui, "comboOrderColumn_" + str(nr) + "_2")                             
        self.order2 = getattr(ui,  "comboOrderOrder_" + str(nr) + "_2")                                              

    def CreateSlots(self):
        
        QtCore.QObject.connect(self.checked, QtCore.SIGNAL("stateChanged(int)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["order", self.nr-1, "checked"], x, self.Update))
        
        QtCore.QObject.connect(self.type, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["order", self.nr-1, "type"], utils.toUnicode(x)))
        
        QtCore.QObject.connect(self.row, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["order", self.nr-1, "row"], utils.toUnicode(x)))
                      
        QtCore.QObject.connect(self.column1, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["order", self.nr-1, "column1"], utils.toUnicode(x)))                          
        QtCore.QObject.connect(self.order1, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["order", self.nr-1, "order1"], utils.toUnicode(x)))
        
        QtCore.QObject.connect(self.column2, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["order", self.nr-1, "column2"], utils.toUnicode(x)))                                      
        QtCore.QObject.connect(self.order2, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["order", self.nr-1, "order2"], utils.toUnicode(x)))             
            
    def GetInfo(self):
        return dstore.GetItem("additional_info", [ "order", self.nr-1])
     
    def setEnabled(self, enabled):
        self.type.setEnabled(enabled)   
        self.column1.setEnabled(enabled)        
        self.row1.setEnabled(enabled)
        self.order1.setEnabled(enabled)
        self.column2.setEnabled(enabled)        
        self.row2.setEnabled(enabled)
        self.order2.setEnabled(enabled)
    
    def Update(self):                
        # set values from datastore              
        info = self.GetInfo()                                
                                            
        self.checked.setChecked(info["checked"]) 
        uiAccesories.SetCurrentIndex(self.type, info["type"])
        uiAccesories.SetCurrentIndex(self.row, info["row"])
         
        uiAccesories.SetCurrentIndex(self.column1, info["column1"])
        uiAccesories.SetCurrentIndex(self.order1, info["order1"])
        
        uiAccesories.SetCurrentIndex(self.column2, info["column2"])        
        uiAccesories.SetCurrentIndex(self.order2, info["order2"])    



class TabColumnsSettings():   
    def __init__(self):
        '''
        Constructor
        '''                
        print "I: CREATE: tabColumnsSettings"
        self.init = False
        
    def Init(self):
        self.pointgroups = [None] * NUMBER_OF.POINTSCOLUMNS
        self.timesgroups = [None] * NUMBER_OF.TIMESCOLUMNS
        self.lapgroups = [None] * NUMBER_OF.TIMESCOLUMNS
        self.ordergroups = [None] * NUMBER_OF.THREECOLUMNS
        self.un = [None] * NUMBER_OF.THREECOLUMNS
        self.us = [None] * 1
        
        
        for i in range(0, NUMBER_OF.TIMESCOLUMNS):
            self.timesgroups[i] = TimesGroup(i+1)
            #self.lapgroups[i] = FilterGroup(i+1, "Lap") 
            self.lapgroups[i] = LapGroup(i+1)
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            self.ordergroups[i] =  OrderGroup(i+1)
            self.un[i] = getattr(Ui(), "checkAInfoUserNumber_" + str(i+1))
        self.us[0] = getattr(Ui(), "checkAInfoUserString_" + str(1))
        self.status = getattr(Ui(), "checkAInfoStatus")
                                      
        for i in range(0, NUMBER_OF.POINTSCOLUMNS): 
            self.pointgroups[i] = PointGroup(i+1)
        
        #add slots to gui elements
        self.addSlots()
        
    def addSlots(self):
                
        print "I: SLOTS: tabColumnsSettings"                                                         
        
        #ADDTITIONAL INFO                                                                              
        QtCore.QObject.connect(self.status, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["status", "checked"], state, self.Update))
        for i in range(0, NUMBER_OF.TIMESCOLUMNS):                                                                     
            self.timesgroups[i].CreateSlots()                  
            self.lapgroups[i].CreateSlots()
        for i in range(0, NUMBER_OF.THREECOLUMNS):                                                                     
            QtCore.QObject.connect(self.un[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, index = i: uiAccesories.sGuiSetItem("additional_info", ["un", index, "checked"], state, self.Update))            
            self.ordergroups[i].CreateSlots()                              
        i=0
        QtCore.QObject.connect(self.us[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, index = i: uiAccesories.sGuiSetItem("additional_info", ["us", index, "checked"], state, self.Update))
        
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):                                                                                    
            self.pointgroups[i].CreateSlots()
            
    def Update(self, mode = UPDATE_MODE.all):
        #print "tabColumnsSettings Update()"
        #aditional info
        for i in range(0, NUMBER_OF.TIMESCOLUMNS):
            self.timesgroups[i].Update()
            self.lapgroups[i].Update()          
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            self.un[i].setChecked(dstore.GetItem("additional_info", ['un', i, "checked"]))                                                                                                                                      
            self.ordergroups[i].Update()
        i=0
        self.us[i].setChecked(dstore.GetItem("additional_info", ['us', i, "checked"]))                                                                                                                                      
        self.status.setChecked(dstore.GetItem("additional_info", ['status',"checked"]))                                                                                                                                      
                            
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            self.pointgroups[i].Update()  
            
            
        #disable columns for export also
        tabExportSettings.Update()
        
        self.init = True
        return True
tabColumnsSettings = TabColumnsSettings()     