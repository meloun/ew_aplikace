# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui 
from threading import Thread,RLock
from ewitis.data.DEF_ENUM_STRINGS import * 



class UiAccesories():
    def __init__(self, source):
        
        self.ui = source.ui
        self.datastore = source.datastore
        self.showmessage = source.showMessage
        self.source = source
        
    def createSlots(self): 
                
        """SLOTY"""
        QtCore.QObject.connect(self.ui.checkRfidRace, QtCore.SIGNAL("clicked()"), self.sRfidRace)        
        QtCore.QObject.connect(self.ui.checkOneLapRace, QtCore.SIGNAL("clicked()"), self.sOneLapRace)        
        QtCore.QObject.connect(self.ui.pushBacklight, QtCore.SIGNAL("clicked()"), self.sTerminalBacklight)       
        #QtCore.QObject.connect(self.ui.pushSpeakerKeys, QtCore.SIGNAL("clicked()"), labmda: self.sTerminalSpeakerKeys(1))
        QtCore.QObject.connect(self.ui.pushSpeakerKeys, QtCore.SIGNAL("clicked()"), lambda: self.sTerminalSpeaker("keys"))
        QtCore.QObject.connect(self.ui.pushSpeakerSystem, QtCore.SIGNAL("clicked()"), lambda: self.sTerminalSpeaker("system"))
        QtCore.QObject.connect(self.ui.pushSpeakerTiming, QtCore.SIGNAL("clicked()"), lambda: self.sTerminalSpeaker("timing"))
        QtCore.QObject.connect(self.ui.comboLanguage, QtCore.SIGNAL("activated(int)"), self.sComboLanguage)
        QtCore.QObject.connect(self.ui.comboTimingMode, QtCore.SIGNAL("activated(int)"), self.sComboTimingMode)        
        
        QtCore.QObject.connect(self.ui.spinTagtime, QtCore.SIGNAL("valueChanged(int)"), self.sFilterTagtime)
        QtCore.QObject.connect(self.ui.spinMinlaptime, QtCore.SIGNAL("valueChanged(int)"), self.sFilterMinlaptime)
        QtCore.QObject.connect(self.ui.spinMaxlapnumber, QtCore.SIGNAL("valueChanged(int)"), self.sFilterMaxlapnumber)
        QtCore.QObject.connect(self.ui.pushGenerateStarttime, QtCore.SIGNAL("clicked()"), self.sGenerateStarttime)
        QtCore.QObject.connect(self.ui.pushGenerateStoptime, QtCore.SIGNAL("clicked()"), self.sGenerateStoptime)
        QtCore.QObject.connect(self.ui.pushQuitTiming, QtCore.SIGNAL("clicked()"), self.sQuitTiming)
        #QtCore.QObject.connect(self.ui.pushSetTimingSettings, QtCore.SIGNAL("clicked()"), lambda: self.sSetTimingSettings(self.GetGuiTimingSettings()))

    def updateGui(self):
        self.updateTab(TAB.run_times)
        self.updateTab(TAB.users)
        self.updateTab(TAB.categories)
        self.updateTab(TAB.cgroups)
        self.updateTab(TAB.tags)
        self.updateTab(TAB.device)
        self.updateTab(TAB.timing_settings)
        
    def updateTab(self, tab, mode = UPDATE_MODE.all):
        """ 
        """
        #print "update tab", tab
        if(tab == TAB.run_times):
            
            if(mode == UPDATE_MODE.all) or (mode == UPDATE_MODE.gui):
                """ PORT NAME """
                self.ui.aSetPort.setText(self.datastore.Get("port_name"))                    
                self.ui.aSetPort.setEnabled(not(self.datastore.Get("port_enable")))
                
                """ PORT CONNECT """
                if(self.datastore.Get("port_enable")):
                    self.ui.aConnectPort.setText("Disconnect")
                else:
                    self.ui.aConnectPort.setText("Connect")
                        
                #terminal_info = self.datastore.Get("terminal info", "GET")                                            
                
            if(mode == UPDATE_MODE.all) or (mode == UPDATE_MODE.tables):
                self.source.R.update()
                self.source.T.update()
                
        elif(tab == TAB.users):                                
            if(mode == UPDATE_MODE.all) or (mode == UPDATE_MODE.tables):
                self.source.U.update()
                
        elif(tab == TAB.categories):                                
            if(mode == UPDATE_MODE.all) or (mode == UPDATE_MODE.tables):
                self.source.C.update()
                  
        elif(tab == TAB.cgroups):                                
            if(mode == UPDATE_MODE.all) or (mode == UPDATE_MODE.tables):                
                self.source.CG.update()
                   
        elif(tab == TAB.tags):                                
            if(mode == UPDATE_MODE.all) or (mode == UPDATE_MODE.tables):
                self.source.tableTags.update()                                               
        
        elif(tab == TAB.device):
            
            """ TERMINAL INFO """
            aux_terminal_info = self.datastore.Get("terminal_info", "GET")
            
            """ number of cells """
            if(aux_terminal_info['number_of_cells'] != None):
                self.ui.lineCells.setText(str(aux_terminal_info['number_of_cells']))                        
            else:
                self.ui.lineCells.setText("-") 
                
            
            """ battery """
            if(aux_terminal_info['battery'] != None):
                self.ui.lineBattery.setText(str(aux_terminal_info['battery'])+" %")                        
            else:
                self.ui.lineBacklight.setText("-- %")                                
            
            """ backlight """        
            if(aux_terminal_info['backlight'] == True):
                self.ui.lineBacklight.setText("ON")
                self.ui.pushBacklight.setText("OFF")
                self.ui.pushBacklight.setEnabled(True)
            elif(aux_terminal_info['backlight'] == False):
                self.ui.lineBacklight.setText("OFF")
                self.ui.pushBacklight.setText("ON")
                self.ui.pushBacklight.setEnabled(True)
            else:
                self.ui.lineBacklight.setText("- -")
                self.ui.pushBacklight.setText("- -")
                self.ui.pushBacklight.setEnabled(False)        
            
            """ speaker """        
            if(aux_terminal_info['speaker']['keys'] == True):
                self.ui.lineSpeakerKeys.setText("ON")
                self.ui.pushSpeakerKeys.setText("OFF")
                self.ui.pushSpeakerKeys.setEnabled(True)
                self.ui.pushSpeakerSystem.setEnabled(True)
                self.ui.pushSpeakerTiming.setEnabled(True)
            elif(aux_terminal_info['speaker']['keys'] == False):
                self.ui.lineSpeakerKeys.setText("OFF")
                self.ui.pushSpeakerKeys.setText("ON")
                self.ui.pushSpeakerKeys.setEnabled(True)
                self.ui.pushSpeakerSystem.setEnabled(True)
                self.ui.pushSpeakerTiming.setEnabled(True)
            else:
                self.ui.lineSpeakerKeys.setText("- -")
                self.ui.pushSpeakerKeys.setText("- -")
                        
            if(aux_terminal_info['speaker']['system'] == True):
                self.ui.lineSpeakerSystem.setText("ON")
                self.ui.pushSpeakerSystem.setText("OFF")
                self.ui.pushSpeakerSystem.setEnabled(True)
            elif(aux_terminal_info['speaker']['system'] == False):
                self.ui.lineSpeakerSystem.setText("OFF")
                self.ui.pushSpeakerSystem.setText("ON")
                self.ui.pushSpeakerSystem.setEnabled(True)
            else:
                self.ui.lineSpeakerSystem.setText("- -")
                self.ui.pushSpeakerSystem.setText("- -")
                self.ui.pushSpeakerSystem.setEnabled(False)
                
            if(aux_terminal_info['speaker']['timing'] == True):
                self.ui.lineSpeakerTiming.setText("ON")
                self.ui.pushSpeakerTiming.setText("OFF")
                self.ui.pushSpeakerTiming.setEnabled(True)
            elif(aux_terminal_info['speaker']['timing'] == False):
                self.ui.lineSpeakerTiming.setText("OFF")
                self.ui.pushSpeakerTiming.setText("ON")
                self.ui.pushSpeakerTiming.setEnabled(True)
            else: 
                self.ui.lineSpeakerTiming.setText("- -")
                self.ui.pushSpeakerTiming.setText("- -")
                self.ui.pushSpeakerTiming.setEnabled(False)
            
            if(aux_terminal_info['speaker']['keys'] == None or aux_terminal_info['speaker']['timing']==None or aux_terminal_info['speaker']['system']==None):    
                self.ui.pushSpeakerKeys.setEnabled(False)
                self.ui.pushSpeakerSystem.setEnabled(False)
                self.ui.pushSpeakerTiming.setEnabled(False)
            else:
                self.ui.pushSpeakerKeys.setEnabled(True)
                self.ui.pushSpeakerSystem.setEnabled(True)
                self.ui.pushSpeakerTiming.setEnabled(True)
                    
            """ language """          
            if(aux_terminal_info['language'] != None):            
                self.ui.comboLanguage.setCurrentIndex(aux_terminal_info['language'])            
                self.ui.lineLanguage.setText(self.ui.comboLanguage.currentText())                    
            else:            
                self.ui.lineLanguage.setText("- -")
        
        elif(tab == TAB.timing_settings):    
            """ TIMING SETTINGS"""
            timing_settings_get = self.datastore.Get("timing_settings", "GET")
            timing_settings_set = self.datastore.Get("timing_settings", "SET")
            #print timing_settings_get
            #print aux_timing_settings
            
            if(self.datastore.Get("rfid")):
                self.ui.checkRfidRace.setCheckState(2)
            else:
                self.ui.checkRfidRace.setCheckState(0)
                       
            if(self.datastore.Get("onelap_race")):
                self.ui.checkOneLapRace.setCheckState(2)
            else:
                self.ui.checkOneLapRace.setCheckState(0)
            
            """ logic mode """  
            if(timing_settings_get['logic_mode'] != None):
                self.ui.comboTimingMode.setCurrentIndex(timing_settings_get['logic_mode']-1)            
                self.ui.lineTimingMode.setText(str(self.ui.comboTimingMode.currentText()+" mode").upper())                    
            else:
                self.ui.comboTimingMode.setCurrentIndex(0)
                self.ui.lineTimingMode.setText("- - -")
            """ Measurement State"""
            if(timing_settings_get['measurement_state'] != None):            
                self.ui.labelMeasurementState.setText(MEASUREMENT_STATE.STRINGS[timing_settings_get['measurement_state']])                    
            else:            
                self.ui.labelMeasurementState.setText("- - -")
                            
            """ Filter Tagtime """
            if(timing_settings_get['filter_tagtime'] != None):                                    
                self.ui.lineFilterTagtime.setText(str(timing_settings_get['filter_tagtime']))
                #self.ui.spinTagtime.setText(str(timing_settings_get['filter_tagtime']))                    
            else:            
                self.ui.lineFilterTagtime.setText("- -")
            """ Filter Minlaptime """                
            if(timing_settings_get['filter_minlaptime'] != None):                                    
                self.ui.lineFilterMinlaptime.setText(str(timing_settings_get['filter_minlaptime']))                    
            else:            
                self.ui.lineFilterMinlaptime.setText("- -")
            
            """ Filter Maxlapnumber """                
            if(timing_settings_get['filter_maxlapnumber'] != None):                                    
                self.ui.lineMaxlapnumber.setText(str(timing_settings_get['filter_maxlapnumber']))                    
            else:            
                self.ui.lineMaxlapnumber.setText("- -")
                    
        
    
    def sRfidRace(self):                        
        if (self.showmessage("Rfid race", "Are you sure you want to change \"Rfid Race\"? \n ", msgtype='warning_dialog')):            
            self.datastore.Set("rfid", not(self.datastore.Get("rfid")))
        self.updateTab(TAB.timing_settings)
        
    def sOneLapRace(self):                                
        if (self.showmessage("One Lap Race", "Are you sure you want to change \"One Lap Race\"? \n ", msgtype='warning_dialog')):            
            self.datastore.Set("onelap_race", not(self.datastore.Get("onelap_race")))        
        self.updateTab(TAB.timing_settings)
        
                            
        
    def sTerminalBacklight(self):
        
        '''získání a nastavení nové SET hodnoty'''
        aux_terminal_info = self.datastore.Get("terminal_info", "GET")                        
        self.datastore.Set("backlight", not(aux_terminal_info["backlight"]), "SET")        
        
        '''reset GET hodnoty'''
        self.datastore.ResetValue("terminal_info", 'backlight')                                                                
        self.updateTab(TAB.device, UPDATE_MODE.gui)
                                                 
    def sTerminalSpeaker(self, key):
        
        '''získání a nastavení nové SET hodnoty'''
        aux_terminal_info = self.datastore.Get("terminal_info", "GET")
        aux_speaker = aux_terminal_info['speaker'].copy()       
        aux_speaker[key] = not(aux_speaker[key])                 
        self.datastore.Set("speaker", aux_speaker, "SET")

        '''reset GET hodnoty'''                
        self.datastore.ResetValue("terminal_info", 'speaker', key)                                                          
        self.updateTab(TAB.device, UPDATE_MODE.gui)
                             
    def sComboLanguage(self, index):
        print "SLOT", index
        '''získání a nastavení nové SET hodnoty'''                                
        self.datastore.Set("language", index, "SET")               
        
        '''reset GET hodnoty'''
        self.datastore.ResetValue("terminal_info", 'language')                                                                
        self.updateTab(TAB.device, UPDATE_MODE.gui)
    
    """                 """
    """ TIMING SETTINGS """
    """                 """
    
    def sComboTimingMode(self, index):
        print "sComboTimingMode", index                
        '''získání a nastavení nové SET hodnoty'''
        aux_timing_settings = self.datastore.Get("timing_settings", "GET").copy()
        aux_timing_settings["logic_mode"] = index + 1                               
        self.datastore.Set("timing_settings", aux_timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        self.datastore.ResetValue("timing_settings", 'logic_mode')                                                                
        self.updateTab(TAB.device, UPDATE_MODE.gui)
    
    
    def sFilterTagtime(self, value):
        print "sFilterTagTime", value
        '''získání a nastavení nové SET hodnoty'''
        timing_settings = self.datastore.Get("timing_settings", "GET").copy()
        timing_settings["filter_tagtime"]  = value                                      
        self.datastore.Set("timing_settings", timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        self.datastore.ResetValue("timing_settings", 'filter_tagtime')                                                                
        self.updateTab(TAB.device, UPDATE_MODE.gui)
    
    def sFilterMinlaptime(self, value):
        print "sFilterMinlaptime", value
        '''získání a nastavení nové SET hodnoty'''
        timing_settings = self.datastore.Get("timing_settings", "GET").copy()
        timing_settings["filter_minlaptime"]  = value                                      
        self.datastore.Set("timing_settings", timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        self.datastore.ResetValue("timing_settings", 'filter_minlaptime')                                                                
        self.updateTab(TAB.device, UPDATE_MODE.gui)
        
    def sFilterMaxlapnumber(self, value):
        print "sFilterMaxlapnumber", value
        '''získání a nastavení nové SET hodnoty'''
        timing_settings = self.datastore.Get("timing_settings", "GET").copy()
        timing_settings["filter_maxlapnumber"]  = value                                      
        self.datastore.Set("timing_settings", timing_settings, "SET")            
        
        '''reset GET hodnoty'''
        self.datastore.ResetValue("timing_settings", 'filter_maxlapnumber')                                                                
        self.updateTab(TAB.device, UPDATE_MODE.gui)
        
    def sGenerateStarttime(self):                                                            
        self.datastore.Set("generate_starttime", 0x01, "SET")                    
        
    def sGenerateStoptime(self):                                                        
        self.datastore.Set("generate_finishtime", 0x00, "SET")                   
        
    def sQuitTiming(self):                                                                
        self.datastore.Set("quit_timing", 0x00, "SET")                   
        
           
