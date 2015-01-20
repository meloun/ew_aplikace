# -*- coding: utf-8 -*-
'''
Created on 8.12.2013

@author: Meloun
'''

from PyQt4 import QtCore
from ewitis.data.DEF_DATA import NUMBER_OF
from ewitis.data.DEF_ENUM_STRINGS import *
from ewitis.gui.UiAccesories import uiAccesories
from ewitis.gui.Ui import Ui
from ewitis.data.dstore import dstore
import libs.utils.utils as utils


class PointFormulaGroup():    
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
        QtCore.QObject.connect(self.rule, QtCore.SIGNAL("textEdited(const QString&)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["points", self.nr-1, "formula"], utils.toUnicode(x)))            
        QtCore.QObject.connect(self.minimum, QtCore.SIGNAL("valueChanged(int)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["points", self.nr-1, "minimum"], x, self.Update))
        QtCore.QObject.connect(self.maximum, QtCore.SIGNAL("valueChanged(int)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["points", self.nr-1, "minimum"], x, self.Update))

    def GetInfo(self):
        return dstore.GetItem("additional_info", [ "points", self.nr-1])
     
    def setEnabled(self, enabled):
        self.rule.setEnabled(enabled)        
        self.minimum.setEnabled(enabled)          
        self.maximum.setEnabled(enabled)       
    
    def Update(self):                                    
        # set values from datastore
        formula_info = self.GetInfo()  
        print dstore.Get("additional_info")   
        print formula_info                              
        self.checked.setChecked(formula_info["checked"])
        self.minimum.setValue(formula_info["minimum"])
        self.maximum.setValue(formula_info["maximum"])
        self.rule.setText(formula_info["rule"])
                              
class TimesFormulaGroup():    
    def __init__(self,  nr):
        '''
        Constructor
        group items as class members        
        '''
        ui = Ui()        
        self.nr = nr
        
        self.checked = getattr(ui, "checkAInfoTime_" + str(nr))        
        self.rule = getattr(ui, "lineAInfoTimeRule_" + str(nr))                             
        self.filter = getattr(ui, "lineAInfoTimeFilter_" + str(nr))                                              

    def CreateSlots(self):
        QtCore.QObject.connect(self.checked, QtCore.SIGNAL("stateChanged(int)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["times", self.nr-1, "checked"], x, self.Update))                          
        QtCore.QObject.connect(self.rule, QtCore.SIGNAL("textEdited(const QString&)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["times", self.nr-1, "formula"], utils.toUnicode(x)))            
        QtCore.QObject.connect(self.filter, QtCore.SIGNAL("textEdited(const QString&)"), lambda x: uiAccesories.sGuiSetItem("additional_info", ["times", self.nr-1, "filter"], utils.toUnicode(x)))            
        
    def GetInfo(self):
        return dstore.GetItem("additional_info", [ "times", self.nr-1])
     
    def setEnabled(self, enabled):
        self.rule.setEnabled(enabled)        
        self.filter.setEnabled(enabled)
    
    def Update(self):        
        # set values from datastore              
        formula_info = self.GetInfo()                                                                    
        self.checked.setChecked(formula_info["checked"])                      
        self.rule.setText(formula_info["formula"])                      
        self.filter.setText(formula_info["filter"])                      
        

class TabRaceSettings():    
      
    def __init__(self):
        '''
        Constructor
        '''        
        print "tabRaceSettings: constructor"
        self.init = False
        
        #define gui widgets
#         self.pointformulagroups = [None] * NUMBER_OF.POINTSCOLUMNS
#         self.timesformulagroups = [None] * NUMBER_OF.POINTSCOLUMNS
#         self.order = [None] * NUMBER_OF.POINTSCOLUMNS
#         self.lap = [None] * NUMBER_OF.POINTSCOLUMNS
#         for i in range(0, NUMBER_OF.POINTSCOLUMNS):
#             self.order[i] = getattr(Ui(), "checkAInfoOrder_" + str(nr)) 
#             self.lap[i] = getattr(Ui(), "checkAInfoLap_" + str(nr)) 
#             self.timesformulagroups[i] = TimesFormulaGroup(i+1)
#             self.pointformulagroups[i] = PointFormulaGroup(i+1)                    
        
    def Init(self):
        self.pointformulagroups = [None] * NUMBER_OF.POINTSCOLUMNS
        self.timesformulagroups = [None] * NUMBER_OF.POINTSCOLUMNS
        self.order = [None] * NUMBER_OF.POINTSCOLUMNS
        self.lap = [None] * NUMBER_OF.POINTSCOLUMNS
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            self.order[i] = getattr(Ui(), "checkAInfoOrder_" + str(i+1)) 
            self.lap[i] = getattr(Ui(), "checkAInfoLap_" + str(i+1)) 
            self.timesformulagroups[i] = TimesFormulaGroup(i+1)
            self.pointformulagroups[i] = PointFormulaGroup(i+1)                       
        self.addSlots()
        
    def addSlots(self):
        
        print "tabRaceSettings: adding slots"               
              
        #left group
        QtCore.QObject.connect(Ui().comboTimingMode, QtCore.SIGNAL("activated(int)"), self.sComboTimingMode) 
        QtCore.QObject.connect(Ui().spinTagtime, QtCore.SIGNAL("valueChanged(int)"), self.sFilterTagtime)
        QtCore.QObject.connect(Ui().spinMinlaptime, QtCore.SIGNAL("valueChanged(int)"), self.sFilterMinlaptime)
        QtCore.QObject.connect(Ui().spinMaxlapnumber, QtCore.SIGNAL("valueChanged(int)"), self.sFilterMaxlapnumber)
                
        #middle group             
        QtCore.QObject.connect(Ui().lineRaceName, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSet("race_name", utils.toUnicode(name), self.Update))        
        QtCore.QObject.connect(Ui().checkRemoteRace, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("racesettings-app", ["remote"], state, self.Update, True))        
        QtCore.QObject.connect(Ui().checkRfidRace, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("racesettings-app", ["rfid"], state, self.Update, True))        
        QtCore.QObject.connect(Ui().checkTagFilter, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("racesettings-app",["tag_filter"], state, self.Update))                                 
        
        #start download from last time and run 
        QtCore.QObject.connect(Ui().checkDownloadFromLast, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSet("download_from_last", state, self.Update))

        QtCore.QObject.connect(Ui().spinTimesViewLimit, QtCore.SIGNAL("valueChanged(int)"),  lambda state: self.sGuiSet("times_view_limit", state, self.Update))
        #table TIMES
        #order evaluation
        #QtCore.QObject.connect(Ui().comboOrderEvaluation, QtCore.SIGNAL("activated(int)"), self.sComboOrderEvaluation)
        QtCore.QObject.connect(Ui().comboOrderEvaluation, QtCore.SIGNAL("activated(int)"), lambda index: uiAccesories.sGuiSetItem("evaluation", ["order"], index, self.Update))                
        QtCore.QObject.connect(Ui().comboStarttimeEvaluation, QtCore.SIGNAL("activated(int)"), lambda index: uiAccesories.sGuiSetItem("evaluation", ["starttime"], index, self.Update))
          
        QtCore.QObject.connect(Ui().radioLaptimeFinishStart,      QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("evaluation", ["laptime"], 0, self.Update) if index else None)
        QtCore.QObject.connect(Ui().radioLaptimeCurrentPrevious,  QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("evaluation", ["laptime"], 1, self.Update) if index else None)        
                                                
        QtCore.QObject.connect(Ui().radioPointsFromTable,      QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("evaluation", ["points"], 0, self.Update) if index else None)
        QtCore.QObject.connect(Ui().radioPointsFromFormula,    QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("evaluation", ["points"], 1, self.Update) if index else None)
                
          
                                                
        #show
        QtCore.QObject.connect(Ui().checkShowOnlyTimesWithOrder, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("show",["times_with_order"], state, self.Update))                
        
        #ADDTITIONAL INFO
        QtCore.QObject.connect(Ui().checkAInfoEnabled, QtCore.SIGNAL("stateChanged(int)"),  lambda state: uiAccesories.sGuiSetItem("additional_info", ["enabled"], state, self.Update))                                                                      
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):                         
            QtCore.QObject.connect(self.order[i], QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["order", i], state, self.Update))        
            QtCore.QObject.connect(self.lap[i], QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["lap", i], state, self.Update))            
            self.pointformulagroups[i].CreateSlots()                            
            self.timesformulagroups[i].CreateSlots()                  
                
        
    """                 """
    """ EXPLICIT SLOTS  """
    """                 """
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
        dstore.ResetValue("timing_settings", 'logic_mode')                                                                
        self.Update(UPDATE_MODE.gui)
    
    
    def sFilterTagtime(self, value):
        print "sFilterTagTime", value
        '''získání a nastavení nové SET hodnoty'''
        timing_settings = dstore.Get("timing_settings", "GET").copy()
        timing_settings["filter_tagtime"]  = value                                      
        dstore.Set("timing_settings", timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        dstore.ResetValue("timing_settings", 'filter_tagtime')                                                                
        self.Update(UPDATE_MODE.gui)
    
    def sFilterMinlaptime(self, value):
        print "sFilterMinlaptime", value
        '''získání a nastavení nové SET hodnoty'''
        timing_settings = dstore.Get("timing_settings", "GET").copy()
        timing_settings["filter_minlaptime"]  = value                                      
        dstore.Set("timing_settings", timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        dstore.ResetValue("timing_settings", 'filter_minlaptime')                                                                
        self.Update(UPDATE_MODE.gui)
        
    def sFilterMaxlapnumber(self, value):
        print "sFilterMaxlapnumber", value
        '''získání a nastavení nové SET hodnoty'''
        timing_settings = dstore.Get("timing_settings", "GET").copy()
        timing_settings["filter_maxlapnumber"]  = value                                      
        dstore.Set("timing_settings", timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        dstore.ResetValue("timing_settings", 'filter_maxlapnumber')                                                                
        self.Update(UPDATE_MODE.gui)
        from ewitis.data.presets import presets
        print presets.GetPreset("blizak")
        dstore.Update(presets.GetPreset("blizak"))

#     def sComboOrderEvaluation(self, index):
#         #print "sComboOrderEvaluation", index                                                               
#         print "test"        
#         dstore.SetItem("evaluation",['order'], index)                                                                                                    
#         self.Update(UPDATE_MODE.gui)

        
        
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
            #Ui().spinTagtime.setText(str(timing_settings_get['filter_tagtime']))                    
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
        if(dstore.IsChanged("racesettings-app") or (self.init == False)):
            print "RACE CHANGED"
            Ui().lineRaceName.setText(dstore.GetItem("racesettings-app", ["race_name"]))
            dstore.ResetChangedFlag("racesettings-app")        
        Ui().checkRemoteRace.setCheckState(dstore.GetItem("racesettings-app", ["remote"]))                                  
        Ui().checkRfidRace.setCheckState(dstore.GetItem("racesettings-app", ["rfid"]))                                  
        Ui().checkTagFilter.setCheckState(dstore.GetItem("racesettings-app", ["tag_filter"]))                                                          
        
                        
        
#         #points
#         
#points: set checked from radio button
        points = dstore.Get("evaluation")["points"]
        Ui().radioPointsFromTable.setChecked(not(points))            
        Ui().radioPointsFromFormula.setChecked(points)        
        #pointsgroups
        for i in range(0, NUMBER_OF.POINTSCOLUMNS): 
            self.pointformulagroups[i].setEnabled(points)
            self.pointformulagroups[i].Update()                                                                                    
            
            
        ##TIMES##
        #evaluations
        #print dstore.Get("evaluation")
        Ui().comboOrderEvaluation.setCurrentIndex(dstore.Get('evaluation')['order'])                            
        Ui().comboStarttimeEvaluation.setCurrentIndex(dstore.Get("evaluation")['starttime'])
                
        if dstore.Get("evaluation")["laptime"] == LaptimeEvaluation.ONLY_FINISHTIME:
            Ui().radioLaptimeFinishStart.setChecked(True)            
            Ui().radioLaptimeCurrentPrevious.setChecked(False)
        else:            
            Ui().radioLaptimeFinishStart.setChecked(False)            
            Ui().radioLaptimeCurrentPrevious.setChecked(True)
                        
         
        
        #show
        Ui().checkShowOnlyTimesWithOrder.setCheckState(dstore.Get("show")["times_with_order"])        
        #Ui().checkShowTimesFromAllRuns.setCheckState(dstore.Get("show")["alltimes"])                   
        
        #aditional info        
        Ui().checkAInfoEnabled.setCheckState(dstore.Get("additional_info")['enabled'])
        Ui().checkAInfoOrder.setCheckState(dstore.Get("additional_info")['order'])
        Ui().checkAInfoOrderInCategory.setCheckState(dstore.Get("additional_info")['order_cat'])
        Ui().checkAInfoLaps.setCheckState(dstore.Get("additional_info")['lap'])
        Ui().checkAInfoLaptime.setCheckState(dstore.Get("additional_info")['laptime'])
        Ui().checkAInfoBestLaptime.setCheckState(dstore.Get("additional_info")['best_laptime'])        
        for i in range(0, NUMBER_OF.POINTS):    
            checkAIPoints = getattr(Ui(), "checkAInfoPoints_" + str(i+1))
            checkAIPoints.setCheckState(dstore.Get("additional_info")['points'][i])                             
        
        #view limit
        Ui().spinTimesViewLimit.setValue(dstore.Get("times_view_limit"))
        
        self.init = True
        return True
    
tabRaceSettings = TabRaceSettings() 