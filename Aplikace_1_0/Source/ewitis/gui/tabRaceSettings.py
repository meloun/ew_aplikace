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
import simplejson as json
import codecs 
   
      
        
        
class TabRaceSettings():    
      
    def __init__(self):
        '''
        Constructor
        '''                
        print "I: CREATE: tabRaceSettings"
        self.init = False
                         
        
    def Init(self):
                        
        self.autonumbers_cell = [None] * len(dstore.GetItem("racesettings-app", ["autonumbers", "cells"]))

        
        
        for i in range(0, len(self.autonumbers_cell)):            
            self.autonumbers_cell[i] = getattr(Ui(), "spinAutonumbersCell" + str(i+1))
            
        #add slots to gui elements
        self.addSlots()
        
    def addSlots(self):                
        print "I: SLOTS: tabRaceSettings"               
              
        #left group
        QtCore.QObject.connect(Ui().comboTimingMode, QtCore.SIGNAL("activated(int)"), self.sComboTimingMode) 
        QtCore.QObject.connect(Ui().comboTimesDownloadMode, QtCore.SIGNAL("activated(int)"), self.sComboTimesDownloadMode)
        QtCore.QObject.connect(Ui().spinAutoenableCell, QtCore.SIGNAL("valueChanged(int)"), self.sAutoenableCell)
        QtCore.QObject.connect(Ui().spinAutoenableBB, QtCore.SIGNAL("valueChanged(int)"), self.sAutoenableBB)
        QtCore.QObject.connect(Ui().spinAutorequestMissingtimes, QtCore.SIGNAL("valueChanged(int)"), self.sAutorequestMissingtimes)
                
        #middle group 
        QtCore.QObject.connect(Ui().pushLoadProfile, QtCore.SIGNAL('clicked()'), self.sLoadProfile)
        QtCore.QObject.connect(Ui().pushSaveProfile, QtCore.SIGNAL('clicked()'), self.sSaveProfile)                    
        QtCore.QObject.connect(Ui().lineRaceName, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSetItem("racesettings-app", ["race_name"], utils.toUnicode(name), self.Update))                    
        QtCore.QObject.connect(Ui().lineTestName, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: uiAccesories.sGuiSetItem("racesettings-app", ["test_name"], utils.toUnicode(name), self.Update))                    
        QtCore.QObject.connect(Ui().textProfileDesc, QtCore.SIGNAL("textChanged()"), self.sTextChanged)        
        QtCore.QObject.connect(Ui().checkRemoteRace, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("racesettings-app", ["remote"], state, self.Update, True))                                                                                       
        QtCore.QObject.connect(Ui().comboStarttimeEvaluation, QtCore.SIGNAL("activated(int)"), lambda state: uiAccesories.sGuiSetItem("racesettings-app", ["evaluation", "starttime"], state, self.Update))                                                                                                                                                                                        
        #middle group: auto-numbers
        QtCore.QObject.connect(Ui().comboAutonumbersMode, QtCore.SIGNAL("activated(int)"),        lambda state: uiAccesories.sGuiSetItem("racesettings-app", ["autonumbers", "mode"], state, self.Update))
        QtCore.QObject.connect(Ui().spinAutonumbersNrOfUsers, QtCore.SIGNAL("valueChanged(int)"), lambda state: uiAccesories.sGuiSetItem("racesettings-app", ["autonumbers", "nr_users"], state, self.Update))
        QtCore.QObject.connect(Ui().spinAutonumbersNrOfCells, QtCore.SIGNAL("valueChanged(int)"), lambda state: uiAccesories.sGuiSetItem("racesettings-app", ["autonumbers", "nr_cells"], state, self.Update))
        for i in range(0, len(self.autonumbers_cell)):                                                                     
            QtCore.QObject.connect(self.autonumbers_cell[i], QtCore.SIGNAL("valueChanged(int)"), lambda state, index = i: uiAccesories.sGuiSetItem("racesettings-app", ["autonumbers", "cells", index], state, self.Update))                       
        QtCore.QObject.connect(Ui().spinAutocellNrOfCells, QtCore.SIGNAL("valueChanged(int)"), lambda state: uiAccesories.sGuiSetItem("racesettings-app", ["autocell", "nr_cells"], state, self.Update))
                
        
    """                 """
    """ EXPLICIT SLOTS  """
    """                 """
    def sTextChanged(self):                
        uiAccesories.sGuiSetItem("racesettings-app", ["profile_desc"], utils.toUnicode( Ui().textProfileDesc.toPlainText()), self.Update)
        
    def sLoadProfile(self, suffix="json"):
        
        #gui dialog                        
        filename = uiAccesories.getOpenFileName("Load profile","profiles_directory","Profile Files (*."+suffix+")", "profile.json")                
        if(filename == ""):                        
            return  
        profile = json.load(codecs.open(filename, 'r', 'utf-8'))
        
        #reset some values
        #profile["timing_settings"]['GET']['value']["logic_mode"] = 1
        #profile["timing_settings"]['SET']['value']["logic_mode"] = 1
        dstore.Set("com_init", 2) 
            
        dstore.Update(profile)
        uiAccesories.sGuiSetItem("racesettings-app", ["profile"], utils.toUnicode(filename))
        
        #send update settings to blackblox
        #dstore.SetChangedFlag("cells_info", range(NUMBER_OF.CELLS))
        #dstore.SetChangedFlag("timing_settings", True)
        
        
        
        
    def sSaveProfile(self, suffix="json"):
        #gui dialog                        
        filename = uiAccesories.getSaveFileName("Save Profile","profiles", "Profile Files (*."+suffix+")", "neni treba")               
        if(filename == ""):                        
            return  
        
        permanentdata = dstore.GetAllPermanents()
        print permanentdata
        
        json.dump(permanentdata, codecs.open(filename, 'w', 'utf-8'), ensure_ascii = False, indent = 4)
        uiAccesories.sGuiSetItem("racesettings-app", ["profile"], utils.toUnicode(filename))
        
    #def sCheckbox(self, state):
    #    print "check: ", state
    #    uiAccesories.sGuiSetItem("additional_info", ["points", 0], state)
    #    print "dstore: ", dstore.GetItem("additional_info", ["points", 0])
          
    #def radio1(self, a):
    #    print "radio state: ",a           
          
    def sComboTimingMode(self, index):
        #print "sComboTimingMode", index                
        '''získání a nastavení nové SET hodnoty'''
        aux_timing_settings = dstore.Get("timing_settings", "GET").copy()
        aux_timing_settings["logic_mode"] = index + 1                               
        dstore.Set("timing_settings", aux_timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        dstore.ResetValue("timing_settings", ["logic_mode"])                                                                
        self.Update(UPDATE_MODE.gui)
          
    def sComboTimesDownloadMode(self, index):
        #print "sComboTimesDownloadMode", index                
        '''získání a nastavení nové SET hodnoty'''
        aux_timing_settings = dstore.Get("timing_settings", "GET").copy()
        aux_timing_settings["times_download_mode"] = index                               
        dstore.Set("timing_settings", aux_timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        dstore.ResetValue("timing_settings", ["times_download_mode"])                                                                
        self.Update(UPDATE_MODE.gui)
    
    
    def sAutoenableCell(self, value):        
        '''získání a nastavení nové SET hodnoty'''
        timing_settings = dstore.Get("timing_settings", "GET").copy()
        timing_settings["autoenable_cell"]  = value                                      
        dstore.Set("timing_settings", timing_settings, "SET")                   
        
        '''reset GET hodnoty'''
        dstore.ResetValue("timing_settings", ['autoenable_cell'])                                                                
        self.Update(UPDATE_MODE.gui)
    
    def sAutoenableBB(self, value):
        print "sAutoenableBb", value
        '''získání a nastavení nové SET hodnoty'''
        timing_settings = dstore.Get("timing_settings", "GET").copy()
        timing_settings["autoenable_bb"]  = value                                      
        dstore.Set("timing_settings", timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        dstore.ResetValue("timing_settings", ['autoenable_bb'])                                                                
        self.Update(UPDATE_MODE.gui)
        
    def sAutorequestMissingtimes(self, value):
        #print "sAutorequestMissingtimes", value
        '''získání a nastavení nové SET hodnoty'''
        timing_settings = dstore.Get("timing_settings", "GET").copy()
        timing_settings["autorequest_missingtimes"]  = value                                      
        dstore.Set("timing_settings", timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        dstore.ResetValue("timing_settings", ['autorequest_missingtimes'])                                                                
        self.Update(UPDATE_MODE.gui)
       
        
    def Update(self, mode = UPDATE_MODE.all):                
                
        """ TIMING SETTINGS"""
        #print dstore.GetItem("racesettings-app", ["race_name"])
        
        timing_settings_get = dstore.Get("timing_settings", "GET")
        timing_settings_set = dstore.Get("timing_settings", "SET")
        
        """ logic mode """  
        #print "lm", timing_settings_get['logic_mode']
        if(timing_settings_get['logic_mode'] != None):
            Ui().comboTimingMode.setCurrentIndex(timing_settings_get['logic_mode']-1)            
            Ui().lineTimingMode.setText(str(Ui().comboTimingMode.currentText()).upper())                    
        else:
            Ui().comboTimingMode.setCurrentIndex(0)
            Ui().lineTimingMode.setText("- - -")
            
        """ times download mode """ 
        #print "tdm",timing_settings_get['times_download_mode']
        if(timing_settings_get['times_download_mode'] != None):
            Ui().comboTimesDownloadMode.setCurrentIndex(timing_settings_get['times_download_mode'])            
            Ui().lineTimesDownloadMode.setText(str(Ui().comboTimesDownloadMode.currentText()).upper())                    
        else:
            Ui().comboTimesDownloadMode.setCurrentIndex(0)
            Ui().lineTimesDownloadMode.setText("- - -")
            
                        
        """ AutoEnable by cell """
        if(timing_settings_get['autoenable_cell'] != None):                                    
            Ui().lineAutoenableCell.setText(str(timing_settings_get['autoenable_cell']))
            #init set value from get value (typically after app starts)
            Ui().spinAutoenableCell.blockSignals(True)
            Ui().spinAutoenableCell.setValue(timing_settings_get['autoenable_cell'])
            Ui().spinAutoenableCell.blockSignals(False)                 
        else:            
            Ui().lineAutoenableCell.setText("- -")
            
        """ AutoEnable by BB """                
        if(timing_settings_get['autoenable_bb'] != None):
            #print "AE:", timing_settings_get['autoenable_bb'], type(timing_settings_get['autoenable_bb'])                                    
            Ui().lineAutoenableBB.setText(str(timing_settings_get['autoenable_bb']))
            #init set value from get value (typically after app starts)
            Ui().spinAutoenableBB.blockSignals(True)
            Ui().spinAutoenableBB.setValue(timing_settings_get['autoenable_bb'])
            Ui().spinAutoenableBB.blockSignals(False)                    
        else:            
            Ui().lineAutoenableBB.setText("- -")
        
        """ Auto request for missing times """
        if(timing_settings_get['autorequest_missingtimes'] != None):                                    
            Ui().lineAutorequestMissingtimes.setText(str(timing_settings_get['autorequest_missingtimes']))
            #init set value from get value (typically after app starts)
            Ui().spinAutorequestMissingtimes.blockSignals(True)
            Ui().spinAutorequestMissingtimes.setValue(timing_settings_get['autorequest_missingtimes'])
            Ui().spinAutorequestMissingtimes.blockSignals(False)                 
        else:            
            Ui().lineAutorequestMissingtimes.setText("- -")
                             
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
        uiAccesories.UpdateText(Ui().lineTestName, dstore.GetItem("racesettings-app", ["test_name"]))
        
                    
        #dstore.ResetChangedFlag("racesettings-app")        
        Ui().checkRemoteRace.setChecked(dstore.GetItem("racesettings-app", ["remote"]))                                                                                                                                                                                                                                               
            
        #evaluations        
        Ui().comboStarttimeEvaluation.setCurrentIndex(dstore.GetItem("racesettings-app", ["evaluation", "starttime"]))                                                             
        
        #autonumbers
        Ui().comboAutonumbersMode.setCurrentIndex(dstore.GetItem("racesettings-app", ["autonumbers", "mode"]))
        Ui().spinAutonumbersNrOfUsers.setValue(dstore.GetItem("racesettings-app", ["autonumbers", "nr_users"]))
        Ui().spinAutonumbersNrOfCells.setValue(dstore.GetItem("racesettings-app", ["autonumbers", "nr_cells"]))    
        for i in range(0, len(self.autonumbers_cell)):                                                        
            self.autonumbers_cell[i].setValue(dstore.GetItem("racesettings-app", ["autonumbers", "cells", i]))
            if(i < dstore.GetItem("racesettings-app", ["autonumbers", "nr_cells"])):            
                self.autonumbers_cell[i].setEnabled(True)
            else:
                self.autonumbers_cell[i].setEnabled(False)
        #autocell
        Ui().spinAutocellNrOfCells.setValue(dstore.GetItem("racesettings-app", ["autocell", "nr_cells"]))        
        #print "TT", dstore.GetItem("racesettings-app", ["autocell", "nr_cells"])
                                
        self.init = True
        return True
    
tabRaceSettings = TabRaceSettings() 