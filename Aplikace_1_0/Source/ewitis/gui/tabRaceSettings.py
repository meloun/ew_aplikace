# -*- coding: utf-8 -*-
'''
Created on 8.12.2013

@author: Meloun
'''

from PyQt4 import QtCore
from ewitis.data.DEF_ENUM_STRINGS import *
from ewitis.gui.UiAccesories import uiAccesories
from ewitis.gui.Ui import Ui
from ewitis.data.dstore import dstore
import libs.utils.utils as utils



class TabRaceSettings():
    
    def __init__(self):
        '''
        Constructor
        '''        
        print "tabRaceSettings: constructor"
        self.init = False                     
        #self.addSlots()
        
    def addSlots(self):
        ##tab RACE SETTINGS##
        
        #race settings          
        print "tabRaceSettings: addind slots"
        #left group
        QtCore.QObject.connect(Ui().comboTimingMode, QtCore.SIGNAL("activated(int)"), self.sComboTimingMode) 
        QtCore.QObject.connect(Ui().spinTagtime, QtCore.SIGNAL("valueChanged(int)"), self.sFilterTagtime)
        QtCore.QObject.connect(Ui().spinMinlaptime, QtCore.SIGNAL("valueChanged(int)"), self.sFilterMinlaptime)
        QtCore.QObject.connect(Ui().spinMaxlapnumber, QtCore.SIGNAL("valueChanged(int)"), self.sFilterMaxlapnumber)
                
        #middle group             
        QtCore.QObject.connect(Ui().lineRaceName, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSet("race_name", utils.toUnicode(name), TAB.race_settings))        
        QtCore.QObject.connect(Ui().checkRfidRace, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSet("rfid", state, TAB.race_settings, True))        
        QtCore.QObject.connect(Ui().checkTagFilter, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSet("tag_filter", state, TAB.race_settings))
        
        
        #export
        QtCore.QObject.connect(Ui().checkExportYear, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["year"], state, TAB.race_settings))                                
        QtCore.QObject.connect(Ui().checkExportClub, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["club"], state, TAB.race_settings))                                
        QtCore.QObject.connect(Ui().checkExportLaps, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["laps"], state, TAB.race_settings))                                
        QtCore.QObject.connect(Ui().checkExportLaptime, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["laptime"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().checkExportBestLaptime, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["best_laptime"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().checkExportOption_1, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["option_1"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().checkExportOption_2, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["option_2"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().checkExportOption_3, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["option_3"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().checkExportOption_4, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["option_4"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().lineOption1Name, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSetItem("export", ["option_1_name"], utils.toUnicode(name), TAB.race_settings))
        QtCore.QObject.connect(Ui().lineOption2Name, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSetItem("export", ["option_2_name"], utils.toUnicode(name), TAB.race_settings))
        QtCore.QObject.connect(Ui().lineOption3Name, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSetItem("export", ["option_3_name"], utils.toUnicode(name), TAB.race_settings))
        QtCore.QObject.connect(Ui().lineOption4Name, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSetItem("export", ["option_4_name"], utils.toUnicode(name), TAB.race_settings))
        QtCore.QObject.connect(Ui().checkExportGap, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["gap"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().checkExportPointsRace, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["points_race"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().checkExportPointsCategories, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["points_categories"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().checkExportPointsGroups, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["points_groups"], state, TAB.race_settings))
        
        #points
        QtCore.QObject.connect(Ui().checkPoinstsFromTable, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("points", ["table"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().linePointsRule, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSetItem("points", ["rule"], utils.toUnicode(name), TAB.race_settings))
        #QtCore.QObject.connect(Ui.lineRaceName, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: self.sGuiSet("race_name", utils.toUnicode(name), TAB.race_settings))
        QtCore.QObject.connect(Ui().spinPointsMinimum, QtCore.SIGNAL("valueChanged(int)"), lambda laps: uiAccesories.sGuiSetItem("points", ["minimum"], laps, TAB.race_settings))
        QtCore.QObject.connect(Ui().spinPointsMaximum, QtCore.SIGNAL("valueChanged(int)"), lambda laps: uiAccesories.sGuiSetItem("points", ["maximum"], laps, TAB.race_settings))
        

        
        #start download from last time and run 
        QtCore.QObject.connect(Ui().checkDownloadFromLast, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSet("download_from_last", state, TAB.race_settings))

        QtCore.QObject.connect(Ui().spinTimesViewLimit, QtCore.SIGNAL("valueChanged(int)"),  lambda state: self.sGuiSet("times_view_limit", state, TAB.race_settings))
        #table TIMES
        #order_evaluation
        QtCore.QObject.connect(Ui().comboOrderEvaluation, QtCore.SIGNAL("activated(int)"), self.sComboOrderEvaluation)
                                                
        #show
        QtCore.QObject.connect(Ui().checkShowOnlyTimesWithOrder, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("show",["times_with_order"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().checkShowStartTimes, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("show",["starttimes"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().checkShowTimesFromAllRuns, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("show",["alltimes"], state, TAB.race_settings))
        
        #additional info
        QtCore.QObject.connect(Ui().checkAInfoEnabled, QtCore.SIGNAL("stateChanged(int)"),  lambda state: uiAccesories.sGuiSetItem("additional_info", ["enabled"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().checkAInfoOrder, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["order"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().checkAInfoOrderInCategory, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["order_in_cat"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().checkAInfoLaps, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["lap"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().checkAInfoLaptime, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["laptime"], state, TAB.race_settings))
        QtCore.QObject.connect(Ui().checkAInfoBestLaptime, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["best_laptime"], state, TAB.race_settings))
                

        
    """                 """
    """ EXPLICIT SLOTS  """
    """                 """            
    def sComboTimingMode(self, index):
        print "sComboTimingMode", index                
        '''získání a nastavení nové SET hodnoty'''
        aux_timing_settings = dstore.Get("timing_settings", "GET").copy()
        aux_timing_settings["logic_mode"] = index + 1                               
        dstore.Set("timing_settings", aux_timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        dstore.ResetValue("timing_settings", 'logic_mode')                                                                
        self.Update(TAB.device, UPDATE_MODE.gui)
    
    
    def sFilterTagtime(self, value):
        print "sFilterTagTime", value
        '''získání a nastavení nové SET hodnoty'''
        timing_settings = dstore.Get("timing_settings", "GET").copy()
        timing_settings["filter_tagtime"]  = value                                      
        dstore.Set("timing_settings", timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        dstore.ResetValue("timing_settings", 'filter_tagtime')                                                                
        self.Update(TAB.device, UPDATE_MODE.gui)
    
    def sFilterMinlaptime(self, value):
        print "sFilterMinlaptime", value
        '''získání a nastavení nové SET hodnoty'''
        timing_settings = dstore.Get("timing_settings", "GET").copy()
        timing_settings["filter_minlaptime"]  = value                                      
        dstore.Set("timing_settings", timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        dstore.ResetValue("timing_settings", 'filter_minlaptime')                                                                
        self.Update(TAB.device, UPDATE_MODE.gui)
        
    def sFilterMaxlapnumber(self, value):
        print "sFilterMaxlapnumber", value
        '''získání a nastavení nové SET hodnoty'''
        timing_settings = dstore.Get("timing_settings", "GET").copy()
        timing_settings["filter_maxlapnumber"]  = value                                      
        dstore.Set("timing_settings", timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        dstore.ResetValue("timing_settings", 'filter_maxlapnumber')                                                                
        self.Update(TAB.device, UPDATE_MODE.gui)

    def sComboOrderEvaluation(self, index):
        #print "sComboOrderEvaluation", index                                                               
        dstore.Set("order_evaluation", index)                                                                                                    
        self.Update(UPDATE_MODE.gui)        

        
        
    def Update(self, mode = UPDATE_MODE.all):
                
        """ TIMING SETTINGS"""
        
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
            Ui().lineBacklight.setText("- -")
             
                                                    
        """ Measurement State"""                       
        Ui().labelMeasurementState.setText(STRINGS.MEASUREMENT_STATE[timing_settings_get['measurement_state']])                                                                    
            
        #APPLICATION
        if(dstore.IsChanged("race_name") or (self.init == False)):
            print "RACE CHANGED"
            Ui().lineRaceName.setText(dstore.Get("race_name"))
            dstore.ResetChangedFlag("race_name")
        Ui().checkRfidRace.setCheckState(dstore.Get("rfid"))                                  
        Ui().checkTagFilter.setCheckState(dstore.Get("tag_filter"))                                  
        #export
        Ui().checkExportYear.setCheckState(dstore.Get("export")["year"])                                
        Ui().checkExportClub.setCheckState(dstore.Get("export")["club"])                                
        Ui().checkExportLaps.setCheckState(dstore.Get("export")["laps"])                                
        Ui().checkExportBestLaptime.setCheckState(dstore.Get("export")["best_laptime"])
        #export - options
        if(dstore.IsChanged("export") or (self.init == False)):
            Ui().checkExportOption_1.setCheckState(dstore.Get("export")["option_1"])
            Ui().checkExportOption_2.setCheckState(dstore.Get("export")["option_2"])
            Ui().checkExportOption_3.setCheckState(dstore.Get("export")["option_3"])
            Ui().checkExportOption_4.setCheckState(dstore.Get("export")["option_4"])
            Ui().checkExportGap.setCheckState(dstore.Get("export")["gap"])
            Ui().lineOption1Name.setText(dstore.Get("export")["option_1_name"])
            Ui().lineOption2Name.setText(dstore.Get("export")["option_2_name"])
            Ui().lineOption3Name.setText(dstore.Get("export")["option_3_name"])
            Ui().lineOption4Name.setText(dstore.Get("export")["option_4_name"])                
            Ui().checkExportPointsRace.setCheckState(dstore.Get("export")["points_race"])
            Ui().checkExportPointsCategories.setCheckState(dstore.Get("export")["points_categories"])
            Ui().checkExportPointsGroups.setCheckState(dstore.Get("export")["points_groups"])
            dstore.ResetChangedFlag("export")
        
        #points
        points = dstore.Get("points")
        Ui().checkPoinstsFromTable.setCheckState(points["table"])
        
        if(dstore.IsChanged("points") or (self.init == False)):
            #print "RULE CHANGED"                
            Ui().linePointsRule.setText(points["rule"])
            dstore.ResetChangedFlag("points")
        
        #Ui().linePointsRule.setText(points["rule"])            
        Ui().spinPointsMinimum.setValue(points["minimum"])
        Ui().spinPointsMaximum.setValue(points["maximum"])            
        Ui().linePointsRule.setEnabled(not(points['table']))
        Ui().spinPointsMinimum.setEnabled(not(points['table'])) 
        Ui().spinPointsMaximum.setEnabled(not(points['table']))                                   
            
            
        ##TIMES##
        #order evaluation
        Ui().comboOrderEvaluation.setCurrentIndex(dstore.Get("order_evaluation"))            
        
        #show
        Ui().checkShowOnlyTimesWithOrder.setCheckState(dstore.Get("show")["times_with_order"])
        Ui().checkShowStartTimes.setCheckState(dstore.Get("show")["starttimes"])
        Ui().checkShowTimesFromAllRuns.setCheckState(dstore.Get("show")["alltimes"])                   
        
        #aditional info
        Ui().checkAInfoEnabled.setCheckState(dstore.Get("additional_info")['enabled'])
        Ui().checkAInfoOrder.setCheckState(dstore.Get("additional_info")['order'])
        Ui().checkAInfoOrderInCategory.setCheckState(dstore.Get("additional_info")['order_in_cat'])
        Ui().checkAInfoLaps.setCheckState(dstore.Get("additional_info")['lap'])
        Ui().checkAInfoLaptime.setCheckState(dstore.Get("additional_info")['laptime'])
        
        #view limit
        Ui().spinTimesViewLimit.setValue(dstore.Get("times_view_limit"))
        
        self.init = True
    
tabRaceSettings = TabRaceSettings() 