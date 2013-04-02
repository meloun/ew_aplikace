# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui 
from threading import Thread,RLock
from ewitis.data.DEF_ENUM_STRINGS import * 
import libs.utils.utils as utils 
import manage_comm


class UiAccesories():
    def __init__(self, source):
        
        self.ui = source.ui
        self.datastore = source.datastore
        #self.showmessage = source.UishowMessage
        self.source = source        
        
    def createSlots(self): 
                
        """SLOTY"""
        #common
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(500); #500ms
        QtCore.QObject.connect(self.timer1s, QtCore.SIGNAL("timeout()"), self.sTimer)
        QtCore.QObject.connect(self.ui.aSetPort, QtCore.SIGNAL("triggered()"), self.sPortSet)
        QtCore.QObject.connect(self.ui.tabWidget, QtCore.SIGNAL("currentChanged (int)"), self.sTabChanged)
        QtCore.QObject.connect(self.ui.aRefresh, QtCore.SIGNAL("triggered()"), self.sRefresh)
        QtCore.QObject.connect(self.ui.aConnectPort, QtCore.SIGNAL("triggered()"), self.sPortConnect)        
        QtCore.QObject.connect(self.ui.aShortcuts, QtCore.SIGNAL("triggered()"), self.sShortcuts)                
        QtCore.QObject.connect(self.ui.actionAbout, QtCore.SIGNAL("triggered()"), self.sAbout)
        
        #actions toolbar
        QtCore.QObject.connect(self.ui.aActionsEnable, QtCore.SIGNAL("triggered(bool)"), self.sEnableActions)
        QtCore.QObject.connect(self.ui.aEnableStart, QtCore.SIGNAL("triggered()"), self.sEnableStartcell)
        QtCore.QObject.connect(self.ui.aGenerateStarttime, QtCore.SIGNAL("triggered()"), self.sGenerateStarttime)
        QtCore.QObject.connect(self.ui.aGenerateFinishtime, QtCore.SIGNAL("triggered()"), self.sGenerateFinishtime)        
        QtCore.QObject.connect(self.ui.aEnableFinish, QtCore.SIGNAL("triggered()"), self.sEnableFinishcell)
        QtCore.QObject.connect(self.ui.aQuitTiming, QtCore.SIGNAL("triggered()"), self.sQuitTiming)
        QtCore.QObject.connect(self.ui.aEnableTagsReading, QtCore.SIGNAL("triggered()"), self.sEnableScanTags)
        QtCore.QObject.connect(self.ui.aDisableTagsReading, QtCore.SIGNAL("triggered()"), self.sDisableScanTags)
        QtCore.QObject.connect(self.ui.aClearDatabase, QtCore.SIGNAL("triggered()"), self.sClearDatabase)                   
        
        #tab RUN-TIMES#
        
        #times
        QtCore.QObject.connect(self.ui.timesShowStartTimes, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSetItem("show", ["starttimes"], state, TAB.run_times))
        QtCore.QObject.connect(self.ui.timesShowAllTimes, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSetItem("show", ["alltimes"], state, TAB.run_times))
        QtCore.QObject.connect(self.ui.timesShowAdditionalInfo, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSetItem("additional_info", ["enabled"], state, TAB.run_times))

        #tab RACE SETTINGS#
        
        #race settings                        
        QtCore.QObject.connect(self.ui.lineRaceName, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: self.sGuiSet("race_name", utils.toUnicode(name), TAB.race_settings))        
        QtCore.QObject.connect(self.ui.checkRfidRace, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSet("rfid", state, TAB.race_settings, True))        
        QtCore.QObject.connect(self.ui.checkOneLapRace, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSet("onelap_race", state, TAB.race_settings, True))
        
        #export
        QtCore.QObject.connect(self.ui.checkExportLaps, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSetItem("export", ["laps"], state, TAB.race_settings))                                
        QtCore.QObject.connect(self.ui.checkExportBestLaptime, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSetItem("export", ["best_laptime"], state, TAB.race_settings))
        
        #start download from last time and run 
        QtCore.QObject.connect(self.ui.checkDownloadFromLast, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSet("download_from_last", state, TAB.race_settings))

        #table TIMES
        #order_evaluation
        QtCore.QObject.connect(self.ui.comboOrderEvaluation, QtCore.SIGNAL("activated(int)"), self.sComboOrderEvaluation)
                                                
        #show
        QtCore.QObject.connect(self.ui.checkShowOnlyTimesWithOrder, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSetItem("show",["times_with_order"], state, TAB.race_settings))
        QtCore.QObject.connect(self.ui.checkShowStartTimes, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSetItem("show",["starttimes"], state, TAB.race_settings))
        QtCore.QObject.connect(self.ui.checkShowTimesFromAllRuns, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSetItem("show",["alltimes"], state, TAB.race_settings))
        
        #additional info
        QtCore.QObject.connect(self.ui.checkAInfoEnabled, QtCore.SIGNAL("stateChanged(int)"),  lambda state: self.sGuiSetItem("additional_info", ["enabled"], state, TAB.race_settings))
        QtCore.QObject.connect(self.ui.checkAInfoOrder, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSetItem("additional_info", ["order"], state, TAB.race_settings))
        QtCore.QObject.connect(self.ui.checkAInfoOrderInCategory, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSetItem("additional_info", ["order_in_cat"], state, TAB.race_settings))
        QtCore.QObject.connect(self.ui.checkAInfoLaps, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSetItem("additional_info", ["lap"], state, TAB.race_settings))
        QtCore.QObject.connect(self.ui.checkAInfoLaptime, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSetItem("additional_info", ["laptime"], state, TAB.race_settings))
        QtCore.QObject.connect(self.ui.checkAInfoBestLaptime, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSetItem("additional_info", ["best_laptime"], state, TAB.race_settings))
        
        #view limit
        QtCore.QObject.connect(self.ui.spinTimesViewLimit, QtCore.SIGNAL("valueChanged(int)"),  lambda state: self.sGuiSet("times_view_limit", state, TAB.race_settings))        
                                        

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
        
        #actions
        QtCore.QObject.connect(self.ui.pushEnableStartcell, QtCore.SIGNAL("clicked()"), self.sEnableStartcell)
        QtCore.QObject.connect(self.ui.pushEnableFinishcell, QtCore.SIGNAL("clicked()"), self.sEnableFinishcell)
        QtCore.QObject.connect(self.ui.pushGenerateStarttime, QtCore.SIGNAL("clicked()"), self.sGenerateStarttime)
        QtCore.QObject.connect(self.ui.pushGenerateStoptime, QtCore.SIGNAL("clicked()"), self.sGenerateFinishtime)
        QtCore.QObject.connect(self.ui.pushQuitTiming, QtCore.SIGNAL("clicked()"), self.sQuitTiming)
        QtCore.QObject.connect(self.ui.pushClearDatabase, QtCore.SIGNAL("clicked()"), self.sClearDatabase)
        QtCore.QObject.connect(self.ui.pushEnableScanTags, QtCore.SIGNAL("clicked()"), self.sEnableScanTags)
        QtCore.QObject.connect(self.ui.pushDisableScanTags, QtCore.SIGNAL("clicked()"), self.sDisableScanTags)
        #QtCore.QObject.connect(self.ui.pushSetTimingSettings, QtCore.SIGNAL("clicked()"), lambda: self.sSetTimingSettings(self.GetGuiTimingSettings()))
        
    def configGui(self):
        self.ui.statusbar_msg = QtGui.QLabel("configuring..")        
        self.ui.statusbar.addPermanentWidget(self.ui.statusbar_msg)    
        self.showMessage("Race", self.datastore.Get("race_name"), False)            
    
    def sRaceNameChanged(self, s):
        print "1:Race changed", s
    def updateGui(self):
        self.updateTab()
        self.updateTab(TAB.run_times)
        self.updateTab(TAB.users)
        self.updateTab(TAB.categories)
        self.updateTab(TAB.cgroups)
        self.updateTab(TAB.tags)
        self.updateTab(TAB.device)
        self.updateTab(TAB.race_settings)
        
    def updateTab(self, tab = None, mode = UPDATE_MODE.all):
        """ 
        """
        if(tab == None):
            #common for all tabs
            if(mode == UPDATE_MODE.all) or (mode == UPDATE_MODE.gui):
                
                """ port name """
                self.ui.aSetPort.setText(self.datastore.Get("port_name"))                    
                self.ui.aSetPort.setEnabled(not(self.datastore.Get("port_enable")))
                
                """ port conect """                            
                self.ui.aConnectPort.setText(STRINGS.PORT_CONNECT[not self.datastore.Get("port_enable")])                                                                                                                    
                self.ui.timesShowStartTimes.setCheckState(self.datastore.Get("show")['starttimes'])
                self.ui.timesShowAllTimes.setCheckState(self.datastore.Get("show")['alltimes'])
                self.ui.timesShowAdditionalInfo.setCheckState(self.datastore.Get("additional_info")['enabled'])
                
                #enable/disable tags reading
                self.updateToolbarActions()                    
                
                """ right status bar """
                self.showMessage('','', 'right_statusbar', statusbar = False)        
            
        #print "update tab", tab
        if(tab == TAB.run_times):
            
                
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
                
        elif(tab == TAB.race_settings):    
            """ TIMING SETTINGS"""
            timing_settings_get = self.datastore.Get("timing_settings", "GET")
            timing_settings_set = self.datastore.Get("timing_settings", "SET")
            
            """ logic mode """  
            if(timing_settings_get['logic_mode'] != None):
                self.ui.comboTimingMode.setCurrentIndex(timing_settings_get['logic_mode']-1)            
                self.ui.lineTimingMode.setText(str(self.ui.comboTimingMode.currentText()+" mode").upper())                    
            else:
                self.ui.comboTimingMode.setCurrentIndex(0)
                self.ui.lineTimingMode.setText("- - -")
                
                            
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
                                 
            """ Tags Readidg Enable """
            if(timing_settings_get['tags_reading_enable'] == True):
                self.ui.lineTagsReadingEn.setText("ON")
            elif(timing_settings_get['tags_reading_enable'] == False):
                self.ui.lineTagsReadingEn.setText("OFF")
            else:
                self.ui.lineBacklight.setText("- -")
                 
                                                        
            """ Measurement State"""                       
            self.ui.labelMeasurementState.setText(STRINGS.MEASUREMENT_STATE[timing_settings_get['measurement_state']])                                                                    
                
            #APPLICATION
            self.ui.lineRaceName.setText(self.datastore.Get("race_name"))
            self.ui.checkRfidRace.setCheckState(self.datastore.Get("rfid"))                                  
            self.ui.checkOneLapRace.setCheckState(self.datastore.Get("onelap_race"))
            #export
            self.ui.checkExportLaps.setCheckState(self.datastore.Get("export")["laps"])                                
            self.ui.checkExportBestLaptime.setCheckState(self.datastore.Get("export")["best_laptime"])
            
            #order evaluation
            self.ui.comboOrderEvaluation.setCurrentIndex(self.datastore.Get("order_evaluation"))
            #print "G",self.datastore.Get("order_evaluation")
            
            #show
            self.ui.checkShowOnlyTimesWithOrder.setCheckState(self.datastore.Get("show")["times_with_order"])
            self.ui.checkShowStartTimes.setCheckState(self.datastore.Get("show")["starttimes"])
            self.ui.checkShowTimesFromAllRuns.setCheckState(self.datastore.Get("show")["alltimes"])                   
            
            #aditional info
            self.ui.checkAInfoEnabled.setCheckState(self.datastore.Get("additional_info")['enabled'])
            self.ui.checkAInfoOrder.setCheckState(self.datastore.Get("additional_info")['order'])
            self.ui.checkAInfoOrderInCategory.setCheckState(self.datastore.Get("additional_info")['order_in_cat'])
            self.ui.checkAInfoLaps.setCheckState(self.datastore.Get("additional_info")['lap'])
            self.ui.checkAInfoLaptime.setCheckState(self.datastore.Get("additional_info")['laptime'])
            
            #view limit
            self.ui.spinTimesViewLimit.setValue(self.datastore.Get("times_view_limit"))
            
                                              
        elif(tab == TAB.actions):
            """ TIMING SETTINGS"""
            timing_settings_get = self.datastore.Get("timing_settings", "GET")
            
            #rfid => no enabel start and finish
            if(self.datastore.Get("rfid") == 0):                
                self.ui.pushEnableStartcell.setEnabled(True)
                self.ui.pushEnableFinishcell.setEnabled(True)
            elif(self.datastore.Get("rfid") == 2):
                self.ui.pushEnableStartcell.setEnabled(False)
                self.ui.pushEnableFinishcell.setEnabled(False)
                
                
            #enable/disable tags reading
            if(timing_settings_get['tags_reading_enable'] == True):
                self.ui.pushEnableScanTags.setEnabled(False)
                self.ui.pushDisableScanTags.setEnabled(True)
            elif(timing_settings_get['tags_reading_enable'] == False):
                self.ui.pushEnableScanTags.setEnabled(True)
                self.ui.pushDisableScanTags.setEnabled(False)
            else:
                self.ui.pushEnableScanTags.setEnabled(False)
                self.ui.pushDisableScanTags.setEnabled(False)
                
            
            
            
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
                self.ui.lineBattery.setText("-- %")                                
            
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
                

    def updateToolbarActions(self, state = None):
                
        if(state == None):            
            state = self.ui.aActionsEnable.isChecked()       
       
        #enable start, enable finish cell
        if(state == False):
            self.ui.aEnableStart.setEnabled(False)
            self.ui.aEnableFinish.setEnabled(False)
        elif(self.datastore.Get("rfid") == 0):        
            self.ui.aEnableStart.setEnabled(state)
            self.ui.aEnableFinish.setEnabled(state)
        else:#if(self.datastore.Get("rfid") == 2):
            self.ui.aEnableStart.setEnabled(False)
            self.ui.aEnableFinish.setEnabled(False)
       
        #Enable and Disable Tags Reading     
        timing_settings_get = self.datastore.Get("timing_settings", "GET")
        if(state == False):
            self.ui.aEnableTagsReading.setEnabled(False)
            self.ui.aDisableTagsReading.setEnabled(False)                            
        elif(timing_settings_get['tags_reading_enable'] == True):
            self.ui.aEnableTagsReading.setEnabled(False)
            self.ui.aDisableTagsReading.setEnabled(True)
        elif(timing_settings_get['tags_reading_enable'] == False):
            self.ui.aEnableTagsReading.setEnabled(True)
            self.ui.aDisableTagsReading.setEnabled(False)
        else:
            self.ui.aEnableTagsReading.setEnabled(False)
            self.ui.aDisableTagsReading.setEnabled(False)

        #generate start and finish time        
        self.ui.aGenerateStarttime.setEnabled(state)
        self.ui.aGenerateFinishtime.setEnabled(state)
        
        #quit timinq
        self.ui.aQuitTiming.setEnabled(state)
        
        #clear database
        self.ui.aClearDatabase.setEnabled(state)
                    
                         
    def showMessage(self, title, message, msgtype='warning', dialog=True, statusbar=True, value=0):
        """
        zobrazuje dialogy a updatuje status bary
        
        *Dialogy:*
            warning(OK), info(OK), warning_dialog(Yes, Cancel), input_integer(integer, OK)
            
        *Status bary:*
            statusbar - zarovnaný vlevo, zobrazí hlášku z parametru
            statusbar_msg - zarovnaný vpravo, zobrazuje stav závodu - not active, running, ...
                
        """        
        
        #DIALOG
        if(dialog):                                
            if(msgtype=='warning'):
                QtGui.QMessageBox.warning(self.source, title, message)            
            elif(msgtype=='info'):
                QtGui.QMessageBox.information(self.source, title, message)
            elif(msgtype=='warning_dialog'):
                ret = QtGui.QMessageBox.warning(self.source, title, message, QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Yes)                
                if (ret != QtGui.QMessageBox.Yes):
                    return False
                message = "succesfully"
            elif(msgtype=='input_integer'):
                i, ok = QtGui.QInputDialog.getInteger(self.source, title, message, value=value)
                if ok:
                    return i
                return None
            elif(msgtype=='right_statusbar'):
                #all time update                 
                timing_settings_get = self.datastore.Get("timing_settings", "GET")
                self.ui.statusbar_msg.setText(STRINGS.MEASUREMENT_STATE[timing_settings_get['measurement_state']])
            
        #STATUSBAR        
        if(statusbar):
            print title, message
            timing_settings_get = self.datastore.Get("timing_settings", "GET")                       
            self.ui.statusbar_msg.setText(STRINGS.MEASUREMENT_STATE[timing_settings_get['measurement_state']])                                                                                                                             
            self.ui.statusbar.showMessage(title+" : " + message)
        
                                                                                                                             
        return True
        
    def sGuiSet(self, name, value, tab, dialog = False):
        if value == self.datastore.Get(name):
            return
                
        if(dialog == True):            
            name_string = self.datastore.GetName(name)            
            if (self.showMessage(name_string, "Are you sure you want to change \""+name_string+"\"? \n ", msgtype='warning_dialog') != True):            
                return
                
        self.datastore.Set(name, value)
        self.updateTab(tab)
        
        
    def sGuiSetItem(self, name, keys, value, tab, dialog = False):
        #print name, keys, value
        if value == self.datastore.GetItem(name, keys):
            return
                
        if(dialog == True):            
            name_string = self.datastore.GetName(name)            
            if (self.showmessage(name_string, "Are you sure you want to change \""+name_string+"\"? \n ", msgtype='warning_dialog') != True):            
                return
                
        self.datastore.SetItem(name, keys, value)        
        self.updateTab(tab)
        
         
    def sTimer(self):               
        self.updateTab(self.ui.tabWidget.currentIndex(), UPDATE_MODE.gui) 
        self.updateTab(None, UPDATE_MODE.gui)       
           
    def sTabChanged(self, nr):                
        self.datastore.Set("active_tab", nr)        
        self.updateTab(nr, UPDATE_MODE.all)
                                     
    # sPortSet() -> set the port 
    def sPortSet(self):
        import libs.comm.serial_utils as serial_utils         
        
        #dostupne porty
        ports = []        
        title = "Port Set"
        
        try:
            for p in serial_utils.enumerate_serial_ports():            
                ports.append(p)
        except:
            self.showMessage(title, "No serial port available.")
            return   
    
        if (ports==[]):
            self.showMessage(title, "No serial port available.")
            return    
            
            
        ports = sorted(ports)                    

        item, ok = QtGui.QInputDialog.getItem(self.source, "Serial Port",
                "Serial Port:", ports, 0, False)
        
        
        if (ok and item):                                  
            self.datastore.Set("port_name", str(item))
            self.showMessage(title, str(item), dialog = False)
        
        self.updateTab()
        
    """                 """
    """ PORT SETTINGS   """
    """                 """    
    # sPortConnect() -> create/kill communication thread             
    def sPortConnect(self):
        '''ddd'''

        title = "Port connect"
                                            
        #comm runs?        
        if(self.datastore.Get("port_enable") == True):                           
            
            # KILL COMMUNICATION - thread, etc..
            self.datastore.Set("port_enable", False)                    
            self.showMessage(title, self.datastore.Get("port_name")+" disconnected", dialog = False)                       
        else:            
            self.showMessage(title, self.datastore.Get("port_name")+" connected", dialog = False)                                 
                        
            # CREATE COMMUNICATION - thread, etc..                                    
                                 
            self.myManageComm = manage_comm.ManageComm(self.datastore)
            self.myManageComm.start()
            
            # wait to stable shared memory 
            time.sleep(0.2)            
            
            #already connected?                                
            #flag down => cant connect
            if(self.datastore.Get("port_enable") == False):             
                title = "Port connect"                                
                self.showMessage(title, self.datastore.Get("port_name")+" cant connect")                
                                
        self.updateGui()                     
        
    
    #sRefresh      
    def sRefresh(self):
        title = "Manual Refresh"
        
        #disable user actions        
        self.datastore.Set("user_actions", self.datastore.Get("user_actions")+1)
                         
        nr_tab = self.datastore.Get("active_tab")        
        self.updateTab(nr_tab)                       
        self.showMessage(title, time.strftime("%H:%M:%S", time.localtime()), dialog = False)
        
        #enable user actions        
        self.datastore.Set("user_actions", self.datastore.Get("user_actions")-1)
        
    def sShortcuts(self):                           
        QtGui.QMessageBox.information(self.source, "Shortcuts", "F5 - manual refresh\nF12 - direct www export")
        
    def sAbout(self):                           
        QtGui.QMessageBox.information(self.source, "About", "Ewitis  - Electronic wireless timing \n\ninfo@ewitis.cz\nwww.ewitis.cz\n\n v0.2\n\n (c) 2011")                                                
                     
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
    """ RACE SETTINGS """
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

    def sComboOrderEvaluation(self, index):
        #print "sComboOrderEvaluation", index                                                               
        self.datastore.Set("order_evaluation", index)                                                                                                    
        self.updateTab(TAB.race_settings, UPDATE_MODE.gui)
        
    """                 """
    """ ACTIONS         """
    """                 """
    
    def sEnableActions(self, state):
        print "A: enable actions: ", state
        self.updateToolbarActions(state)
                          
    def sEnableStartcell(self):                                                             
        print "A: Enable start cell"                                                                                                                            
        self.datastore.Set("enable_startcell", 0x01, "SET")                    
    def sEnableFinishcell(self):                                                                    
        print "A: Enable finish cell"                                                                                                                            
        self.datastore.Set("enable_finishcell", 0x01, "SET")                                                               
    def sGenerateStarttime(self):
        print "A: Generate starttime"                                                                                                                            
        self.datastore.Set("generate_starttime", 0x01, "SET")                            
    def sGenerateFinishtime(self):                                                        
        print "A: generate finishtime"                                                                                                                            
        self.datastore.Set("generate_finishtime", 0x00, "SET")                           
    def sQuitTiming(self):
        print "A: Generate quit time"                                                                                                                                                                                            
        self.datastore.Set("quit_timing", 0x00, "SET")                   
    def sClearDatabase(self):
        if (self.showMessage("Clear Database", "Are you sure you want to clear all database? \n ", msgtype='warning_dialog') != True):            
            return
        print "A: Clear Database"                                                                                                                                                                                            
        self.datastore.Set("clear_database", 0x00, "SET")
    def sEnableScanTags(self):
        print "A: Enable Scan Tags"                                                                                                                                                                                            
        self.datastore.Set("tags_reading", 0x01, "SET")
    def sDisableScanTags(self):
        print "A: Disable Scan Tags"                                                                                                                                                                                            
        self.datastore.Set("tags_reading", 0x00, "SET")
        
                           
        
           
