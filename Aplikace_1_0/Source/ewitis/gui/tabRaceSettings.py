# -*- coding: utf-8 -*-
'''
Created on 8.12.2013

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
                     
        
        
        
class TabRaceSettings():    
      
    def __init__(self):
        '''
        Constructor
        '''        
        print "tabRaceSettings: constructor"
        self.init = False
                         
        
    def Init(self):
        
        self.pointgroups = [None] * NUMBER_OF.POINTSCOLUMNS
        self.timesgroups = [None] * NUMBER_OF.THREECOLUMNS
        self.ordergroups = [None] * NUMBER_OF.THREECOLUMNS
        self.lapgroups = [None] * NUMBER_OF.THREECOLUMNS
        self.un = [None] * NUMBER_OF.THREECOLUMNS
        self.us = [None] * 1
        
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            self.timesgroups[i] = TimesGroup(i+1)
            self.lapgroups[i] = FilterGroup(i+1, "Lap") 
            self.ordergroups[i] =  OrderGroup(i+1)
            self.un[i] = getattr(Ui(), "checkAInfoUserNumber_" + str(i+1))
        self.us[0] = getattr(Ui(), "checkAInfoUserString_" + str(1))
        self.status = getattr(Ui(), "checkAInfoStatus")
                                      
        for i in range(0, NUMBER_OF.POINTSCOLUMNS): 
            self.pointgroups[i] = PointGroup(i+1)
        
        self.addSlots()
        
    def addSlots(self):
        
        print "tabRaceSettings: adding slots"               
              
        #left group
        QtCore.QObject.connect(Ui().comboTimingMode, QtCore.SIGNAL("activated(int)"), self.sComboTimingMode) 
        QtCore.QObject.connect(Ui().spinTagtime, QtCore.SIGNAL("valueChanged(int)"), self.sFilterTagtime)
        QtCore.QObject.connect(Ui().spinMinlaptime, QtCore.SIGNAL("valueChanged(int)"), self.sFilterMinlaptime)
        QtCore.QObject.connect(Ui().spinMaxlapnumber, QtCore.SIGNAL("valueChanged(int)"), self.sFilterMaxlapnumber)
                
        #middle group 
        QtCore.QObject.connect(Ui().pushLoadProfile, QtCore.SIGNAL('clicked()'), self.sLoadProfile)
        QtCore.QObject.connect(Ui().pushSaveProfile, QtCore.SIGNAL('clicked()'), self.sSaveProfile)                    
        QtCore.QObject.connect(Ui().lineRaceName, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSetItem("racesettings-app", ["race_name"], utils.toUnicode(name), self.Update))                    
        QtCore.QObject.connect(Ui().textProfileDesc, QtCore.SIGNAL("textChanged()"), self.sTextChanged)        
        QtCore.QObject.connect(Ui().checkRemoteRace, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("racesettings-app", ["remote"], state, self.Update, True))        
        QtCore.QObject.connect(Ui().checkRfidRace, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("racesettings-app", ["rfid"], state, self.Update, True))        
        QtCore.QObject.connect(Ui().checkTagFilter, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("racesettings-app",["tag_filter"], state, self.Update))                                                                               
        QtCore.QObject.connect(Ui().comboStarttimeEvaluation, QtCore.SIGNAL("activated(int)"), lambda state: uiAccesories.sGuiSetItem("evaluation", ["starttime"], state, self.Update))
        QtCore.QObject.connect(Ui().spinFinishLaps, QtCore.SIGNAL("valueChanged(int)"), lambda state: uiAccesories.sGuiSetItem("evaluation", ["finishtime", "laps"], state, self.Update))                                                                                                                                                                   
        QtCore.QObject.connect(Ui().lineFinishTime, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSetItem("evaluation", ["finishtime", "time"], utils.toUnicode(name), self.Update))                    
        
        #ADDTITIONAL INFO                                                                              
        QtCore.QObject.connect(self.status, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["status", "checked"], state, self.Update))
        for i in range(0, NUMBER_OF.THREECOLUMNS):                                                                     
            QtCore.QObject.connect(self.un[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, index = i: uiAccesories.sGuiSetItem("additional_info", ["un", index, "checked"], state, self.Update))            
            self.timesgroups[i].CreateSlots()                  
            self.lapgroups[i].CreateSlots()
            self.ordergroups[i].CreateSlots()                              
        i=0
        QtCore.QObject.connect(self.us[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, index = i: uiAccesories.sGuiSetItem("additional_info", ["us", index, "checked"], state, self.Update))
        
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):                                                                                    
            self.pointgroups[i].CreateSlots()                           
                
        
    """                 """
    """ EXPLICIT SLOTS  """
    """                 """
    def sTextChanged(self):        
        uiAccesories.sGuiSetItem("racesettings-app", ["profile_desc"], utils.toUnicode( Ui().textProfileDesc.toHtml()), self.Update)
        
    def sLoadProfile(self):
        
        #gui dialog                        
        filename = uiAccesories.getOpenFileName("Load profile","profiles_directory","Profile Files (*.json)", "profile.json")                
        if(filename == ""):                        
            return  
        profile = json.load(codecs.open(filename, 'r', 'utf-8'))
        
        #reset some values
        #get cell task None         
        for idx in range(0, len(profile["cells_info"]['GET']['value'])):
            profile["cells_info"]['GET']['value'][idx]["task"] = 0
            profile["cells_info"]['SET']['value'][idx]["task"] = 0
            profile["cells_info"]['GET']['value'][idx]["trigger"] = 0
            profile["cells_info"]['SET']['value'][idx]["trigger"] = 0
        profile["timing_settings"]['GET']['value']["logic_mode"] = 1
        profile["timing_settings"]['SET']['value']["logic_mode"] = 1
            
        dstore.Update(profile)
        uiAccesories.sGuiSetItem("racesettings-app", ["profile"], utils.toUnicode(filename))
        
        #send update settings to blackblox
        #dstore.SetChangedFlag("cells_info", range(NUMBER_OF.CELLS))
        #dstore.SetChangedFlag("timing_settings", True)
        
        
        
        
    def sSaveProfile(self):
        #gui dialog                        
        filename = uiAccesories.getSaveFileName("Save Profile","profiles", "Profile Files (*.json)", "neni treba")               
        if(filename == ""):                        
            return  
        
        permanentdata = dstore.GetAllPermanents()
        
        json.dump(permanentdata, codecs.open(filename, 'w', 'utf-8'), ensure_ascii = False, indent = 4)
        uiAccesories.sGuiSetItem("racesettings-app", ["profile"], utils.toUnicode(filename))
        
    def sCheckbox(self, state):
        print "check: ", state
        uiAccesories.sGuiSetItem("additional_info", ["points", 0], state)
        print "dstore: ", dstore.GetItem("additional_info", ["points", 0])
          
    def radio1(self, a):
        print "radio state: ",a           
          
    def sComboTimingMode(self, index):
        #print "sComboTimingMode", index                
        '''získání a nastavení nové SET hodnoty'''
        aux_timing_settings = dstore.Get("timing_settings", "GET").copy()
        aux_timing_settings["logic_mode"] = index + 1                               
        dstore.Set("timing_settings", aux_timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        dstore.ResetValue("timing_settings", ["logic_mode"])                                                                
        self.Update(UPDATE_MODE.gui)
    
    
    def sFilterTagtime(self, value):
        print "sFilterTagTime", value
        '''získání a nastavení nové SET hodnoty'''
        timing_settings = dstore.Get("timing_settings", "GET").copy()
        timing_settings["filter_tagtime"]  = value                                      
        dstore.Set("timing_settings", timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        dstore.ResetValue("timing_settings", ['filter_tagtime'])                                                                
        self.Update(UPDATE_MODE.gui)
    
    def sFilterMinlaptime(self, value):
        print "sFilterMinlaptime", value
        '''získání a nastavení nové SET hodnoty'''
        timing_settings = dstore.Get("timing_settings", "GET").copy()
        timing_settings["filter_minlaptime"]  = value                                      
        dstore.Set("timing_settings", timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        dstore.ResetValue("timing_settings", ['filter_minlaptime'])                                                                
        self.Update(UPDATE_MODE.gui)
        
    def sFilterMaxlapnumber(self, value):
        print "sFilterMaxlapnumber", value
        '''získání a nastavení nové SET hodnoty'''
        timing_settings = dstore.Get("timing_settings", "GET").copy()
        timing_settings["filter_maxlapnumber"]  = value                                      
        dstore.Set("timing_settings", timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        dstore.ResetValue("timing_settings", ['filter_maxlapnumber'])                                                                
        self.Update(UPDATE_MODE.gui)
       
        
    def Update(self, mode = UPDATE_MODE.all):                
                
        """ TIMING SETTINGS"""
        #print dstore.GetItem("racesettings-app", ["race_name"])
        
        timing_settings_get = dstore.Get("timing_settings", "GET")
        timing_settings_set = dstore.Get("timing_settings", "SET")
        
        """ logic mode """  
        if(timing_settings_get['logic_mode'] != None):
            Ui().comboTimingMode.setCurrentIndex(timing_settings_get['logic_mode']-1)            
            Ui().lineTimingMode.setText(str(Ui().comboTimingMode.currentText()+" mode").upper())                    
        else:
            Ui().comboTimingMode.setCurrentIndex(0)
            Ui().lineTimingMode.setText("- - -")
            
                        
        """ Filter Tagtime """
        if(timing_settings_get['filter_tagtime'] != None):                                    
            Ui().lineFilterTagtime.setText(str(timing_settings_get['filter_tagtime']))                 
        else:            
            Ui().lineFilterTagtime.setText("- -")
        """ Filter Minlaptime """                
        if(timing_settings_get['filter_minlaptime'] != None):                                    
            Ui().lineFilterMinlaptime.setText(str(timing_settings_get['filter_minlaptime']))                    
        else:            
            Ui().lineFilterMinlaptime.setText("- -")
        
        """ Filter Maxlapnumber """                
        if(timing_settings_get['filter_maxlapnumber'] != None):                                    
            Ui().lineMaxlapnumber.setText(str(timing_settings_get['filter_maxlapnumber']))                    
        else:            
            Ui().lineMaxlapnumber.setText("- -")
                             
        """ Tags Readidg Enable """
        if(timing_settings_get['tags_reading_enable'] == True):
            Ui().lineTagsReadingEn.setText("ON")
        elif(timing_settings_get['tags_reading_enable'] == False):
            Ui().lineTagsReadingEn.setText("OFF")
        else:
            Ui().lineTagsReadingEn.setText("- -")
             
                                                    
        """ Measurement State"""
        Ui().labelMeasurementState.setText(STRINGS.MEASUREMENT_STATE[timing_settings_get['measurement_state']])                                                                    
            
        #APPLICATION
        #if(dstore.IsChanged("racesettings-app") or (self.init == False)):
        #cursor_position = Ui().lineRaceName.cursorPosition()
        #Ui().lineRaceName.setText(dstore.GetItem("racesettings-app", ["race_name"]))
        #Ui().lineRaceName.setCursorPosition(cursor_position)
        
        uiAccesories.UpdateText(Ui().lineProfileName, dstore.GetItem("racesettings-app", ["profile"]))
        uiAccesories.UpdateText(Ui().textProfileDesc, dstore.GetItem("racesettings-app", ["profile_desc"]))
        uiAccesories.UpdateText(Ui().lineRaceName, dstore.GetItem("racesettings-app", ["race_name"]))
        
                    
        #dstore.ResetChangedFlag("racesettings-app")        
        Ui().checkRemoteRace.setChecked(dstore.GetItem("racesettings-app", ["remote"]))                                  
        Ui().checkRfidRace.setChecked(dstore.GetItem("racesettings-app", ["rfid"]))                                  
        Ui().checkTagFilter.setChecked(dstore.GetItem("racesettings-app", ["tag_filter"]))                                                                                                                                                                                                             
            
        #evaluations        
        Ui().comboStarttimeEvaluation.setCurrentIndex(dstore.Get("evaluation")['starttime'])                                                      
        Ui().spinFinishLaps.setValue(dstore.GetItem("evaluation", ['finishtime', "laps"]))                                                      
        uiAccesories.UpdateText(Ui().lineFinishTime, dstore.GetItem("evaluation", ["finishtime", "time"]))
        
        #aditional info
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            self.un[i].setChecked(dstore.GetItem("additional_info", ['un', i, "checked"]))                                                                                                                                      
            self.timesgroups[i].Update()
            self.lapgroups[i].Update()          
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
    
tabRaceSettings = TabRaceSettings() 