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
        
    def Init(self):                     
        self.addSlots()
        
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
        QtCore.QObject.connect(Ui().lineRaceName, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSet("race_name", utils.toUnicode(name), self.Update))        
        QtCore.QObject.connect(Ui().checkRemoteRace, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSet("remote", state, self.Update, True))        
        QtCore.QObject.connect(Ui().checkRfidRace, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSet("rfid", state, self.Update, True))        
        QtCore.QObject.connect(Ui().checkTagFilter, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSet("tag_filter", state, self.Update))
        
     
        
             

        
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
        QtCore.QObject.connect(Ui().linePointsRule_1, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSetItem("evaluation", ["points_formula1","formula"], utils.toUnicode(name)))
        QtCore.QObject.connect(Ui().spinPointsMinimum_1, QtCore.SIGNAL("valueChanged(int)"), lambda x: uiAccesories.sGuiSetItem("evaluation", ["points_formula1","minimum"], x, self.Update))
        QtCore.QObject.connect(Ui().spinPointsMaximum_1, QtCore.SIGNAL("valueChanged(int)"), lambda x: uiAccesories.sGuiSetItem("evaluation", ["points_formula1","maximum"], x, self.Update))        
        QtCore.QObject.connect(Ui().linePointsRule_2, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSetItem("evaluation", ["points_formula2","formula"], utils.toUnicode(name)))
        QtCore.QObject.connect(Ui().spinPointsMinimum_2, QtCore.SIGNAL("valueChanged(int)"), lambda x: uiAccesories.sGuiSetItem("evaluation", ["points_formula2","minimum"], x, self.Update))
        QtCore.QObject.connect(Ui().spinPointsMaximum_2, QtCore.SIGNAL("valueChanged(int)"), lambda x: uiAccesories.sGuiSetItem("evaluation", ["points_formula2","maximum"], x, self.Update))
        QtCore.QObject.connect(Ui().linePointsRule_3, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSetItem("evaluation", ["points_formula3","formula"], utils.toUnicode(name)))
        QtCore.QObject.connect(Ui().spinPointsMinimum_3, QtCore.SIGNAL("valueChanged(int)"), lambda x: uiAccesories.sGuiSetItem("evaluation", ["points_formula3","minimum"], x, self.Update))
        QtCore.QObject.connect(Ui().spinPointsMaximum_3, QtCore.SIGNAL("valueChanged(int)"), lambda x: uiAccesories.sGuiSetItem("evaluation", ["points_formula3","maximum"], x, self.Update))
                
                                                
        #show
        QtCore.QObject.connect(Ui().checkShowOnlyTimesWithOrder, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("show",["times_with_order"], state, self.Update))                
        
        #additional info
        QtCore.QObject.connect(Ui().checkAInfoEnabled, QtCore.SIGNAL("stateChanged(int)"),  lambda state: uiAccesories.sGuiSetItem("additional_info", ["enabled"], state, self.Update))
        QtCore.QObject.connect(Ui().checkAInfoOrder, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["order"], state, self.Update))
        QtCore.QObject.connect(Ui().checkAInfoOrderInCategory, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["order_cat"], state, self.Update))
        QtCore.QObject.connect(Ui().checkAInfoLaps, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["lap"], state, self.Update))
        QtCore.QObject.connect(Ui().checkAInfoLaptime, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["laptime"], state, self.Update))
        QtCore.QObject.connect(Ui().checkAInfoBestLaptime, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["best_laptime"], state, self.Update))
        QtCore.QObject.connect(Ui().checkAInfoPoints_1, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["points1"], state, self.Update))
        QtCore.QObject.connect(Ui().checkAInfoPoints_2, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["points2"], state, self.Update))
        QtCore.QObject.connect(Ui().checkAInfoPoints_3, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["points3"], state, self.Update))
        
        #export
        QtCore.QObject.connect(Ui().checkExportYear, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["year"], state, self.Update))                                
        QtCore.QObject.connect(Ui().checkExportSex, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["sex"], state, self.Update))                                
        QtCore.QObject.connect(Ui().checkExportClub, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["club"], state, self.Update))                                
        QtCore.QObject.connect(Ui().checkExportLaps, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["laps"], state, self.Update))                                
        QtCore.QObject.connect(Ui().checkExportLaptime, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["laptime"], state, self.Update))
        QtCore.QObject.connect(Ui().checkExportBestLaptime, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["best_laptime"], state, self.Update))
        QtCore.QObject.connect(Ui().checkExportOption_1, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["option_1"], state, self.Update))
        QtCore.QObject.connect(Ui().checkExportOption_2, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["option_2"], state, self.Update))
        QtCore.QObject.connect(Ui().checkExportOption_3, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["option_3"], state, self.Update))
        QtCore.QObject.connect(Ui().checkExportOption_4, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["option_4"], state, self.Update))
        QtCore.QObject.connect(Ui().lineOption1Name, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSetItem("export", ["option_1_name"], utils.toUnicode(name), self.Update))
        QtCore.QObject.connect(Ui().lineOption2Name, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSetItem("export", ["option_2_name"], utils.toUnicode(name), self.Update))
        QtCore.QObject.connect(Ui().lineOption3Name, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSetItem("export", ["option_3_name"], utils.toUnicode(name), self.Update))
        QtCore.QObject.connect(Ui().lineOption4Name, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSetItem("export", ["option_4_name"], utils.toUnicode(name), self.Update))
        QtCore.QObject.connect(Ui().checkExportGap, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["gap"], state, self.Update))
        QtCore.QObject.connect(Ui().checkExportPointsRace, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["points_race"], state, self.Update))
        QtCore.QObject.connect(Ui().checkExportPointsCategories, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["points_categories"], state, self.Update))
        QtCore.QObject.connect(Ui().checkExportPointsGroups, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["points_groups"], state, self.Update))
        QtCore.QObject.connect(Ui().radioExportLapsTimes,      QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("export", ["lapsformat"], 0, self.Update) if index else None)
        QtCore.QObject.connect(Ui().radioExportLapsLaptimes,  QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("export", ["lapsformat"], 1, self.Update) if index else None) 
        QtCore.QObject.connect(Ui().radioExportLapsPoints_1,  QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("export", ["lapsformat"], 2, self.Update) if index else None) 
        QtCore.QObject.connect(Ui().radioExportLapsPoints_2,  QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("export", ["lapsformat"], 3, self.Update) if index else None) 
        QtCore.QObject.connect(Ui().radioExportLapsPoints_3,  QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("export", ["lapsformat"], 4, self.Update) if index else None) 
                

        
    """                 """
    """ EXPLICIT SLOTS  """
    """                 """
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

    def sComboOrderEvaluation(self, index):
        #print "sComboOrderEvaluation", index                                                               
        dstore.SetItem("evaluation",['order'], index)                                                                                                    
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
            Ui().lineTagsReadingEn.setText("- -")
             
                                                    
        """ Measurement State"""                       
        Ui().labelMeasurementState.setText(STRINGS.MEASUREMENT_STATE[timing_settings_get['measurement_state']])                                                                    
            
        #APPLICATION
        if(dstore.IsChanged("race_name") or (self.init == False)):
            print "RACE CHANGED"
            Ui().lineRaceName.setText(dstore.Get("race_name"))
            dstore.ResetChangedFlag("race_name")
        Ui().checkRemoteRace.setCheckState(dstore.Get("remote"))                                  
        Ui().checkRfidRace.setCheckState(dstore.Get("rfid"))                                  
        Ui().checkTagFilter.setCheckState(dstore.Get("tag_filter"))                                  
        #export
        Ui().checkExportYear.setCheckState(dstore.Get("export")["year"])                                
        Ui().checkExportSex.setCheckState(dstore.Get("export")["sex"])                                
        Ui().checkExportClub.setCheckState(dstore.Get("export")["club"])                                
        Ui().checkExportLaps.setCheckState(dstore.Get("export")["laps"])                                
        Ui().checkExportLaptime.setCheckState(dstore.Get("export")["laptime"])
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
            
            if dstore.Get("export")["lapsformat"] == ExportLapsFormat.FORMAT_TIMES:
                Ui().radioExportLapsTimes.setChecked(True)            
                Ui().radioExportLapsLaptimes.setChecked(False)
                Ui().radioExportLapsPoints_1.setChecked(False)
                Ui().radioExportLapsPoints_2.setChecked(False)
                Ui().radioExportLapsPoints_3.setChecked(False)
            elif dstore.Get("export")["lapsformat"] == ExportLapsFormat.FORMAT_LAPTIMES:            
                Ui().radioExportLapsTimes.setChecked(False)            
                Ui().radioExportLapsLaptimes.setChecked(True)
                Ui().radioExportLapsPoints_1.setChecked(False)
                Ui().radioExportLapsPoints_2.setChecked(False)
                Ui().radioExportLapsPoints_3.setChecked(False)
            elif dstore.Get("export")["lapsformat"] == ExportLapsFormat.FORMAT_POINTS_1:            
                Ui().radioExportLapsTimes.setChecked(False)            
                Ui().radioExportLapsLaptimes.setChecked(False)
                Ui().radioExportLapsPoints_1.setChecked(True)                                
                Ui().radioExportLapsPoints_2.setChecked(False)
                Ui().radioExportLapsPoints_3.setChecked(False)
            elif dstore.Get("export")["lapsformat"] == ExportLapsFormat.FORMAT_POINTS_2:            
                Ui().radioExportLapsTimes.setChecked(False)            
                Ui().radioExportLapsLaptimes.setChecked(False)
                Ui().radioExportLapsPoints_1.setChecked(False)                                
                Ui().radioExportLapsPoints_2.setChecked(True)
                Ui().radioExportLapsPoints_3.setChecked(False)
            elif dstore.Get("export")["lapsformat"] == ExportLapsFormat.FORMAT_POINTS_3:            
                Ui().radioExportLapsTimes.setChecked(False)            
                Ui().radioExportLapsLaptimes.setChecked(False)
                Ui().radioExportLapsPoints_1.setChecked(False)                                
                Ui().radioExportLapsPoints_2.setChecked(False)
                Ui().radioExportLapsPoints_3.setChecked(True)
            else:
                print "error: export laptimes"
                
            dstore.ResetChangedFlag("export")
        
        #points
        
        #points: set checked from radio button
        points = dstore.Get("evaluation")["points"]
        Ui().radioPointsFromTable.setChecked(not(points))            
        Ui().radioPointsFromFormula.setChecked(points)
        #points: set enabled rule, min, max
        Ui().linePointsRule_1.setEnabled(points)
        Ui().linePointsRule_2.setEnabled(points)
        Ui().linePointsRule_3.setEnabled(points)
        Ui().spinPointsMinimum_1.setEnabled(points) 
        Ui().spinPointsMinimum_2.setEnabled(points) 
        Ui().spinPointsMinimum_3.setEnabled(points) 
        Ui().spinPointsMaximum_1.setEnabled(points)
        Ui().spinPointsMaximum_2.setEnabled(points)
        Ui().spinPointsMaximum_3.setEnabled(points)
        
        
        points_formula1 = dstore.Get("evaluation")["points_formula1"]        
        points_formula2 = dstore.Get("evaluation")["points_formula2"]        
        points_formula3 = dstore.Get("evaluation")["points_formula3"]        
                        
        #points: set formula text
        if(self.init == False):            
            Ui().linePointsRule_1.setText(points_formula1["formula"])
            Ui().linePointsRule_2.setText(points_formula2["formula"])
            Ui().linePointsRule_3.setText(points_formula3["formula"])
            #uiAccesories.showMessage("Poinst formula changed:", (dstore.Get("points_formula")["formula"]).toString(), MSGTYPE.statusbar)                       
            #dstore.ResetChangedFlag("points")
                            
        #points: set min and max
        Ui().spinPointsMinimum_1.setValue(points_formula1["minimum"])
        Ui().spinPointsMaximum_1.setValue(points_formula1["maximum"])
        Ui().spinPointsMinimum_2.setValue(points_formula2["minimum"])
        Ui().spinPointsMaximum_2.setValue(points_formula2["maximum"])
        Ui().spinPointsMinimum_3.setValue(points_formula3["minimum"])
        Ui().spinPointsMaximum_3.setValue(points_formula3["maximum"])                                                                                      
            
            
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
        Ui().checkAInfoPoints_1.setCheckState(dstore.Get("additional_info")['points1'])        
        Ui().checkAInfoPoints_2.setCheckState(dstore.Get("additional_info")['points2'])        
        Ui().checkAInfoPoints_3.setCheckState(dstore.Get("additional_info")['points3'])        
        
        #view limit
        Ui().spinTimesViewLimit.setValue(dstore.Get("times_view_limit"))
        
        self.init = True
        return True
    
tabRaceSettings = TabRaceSettings() 