# -*- coding: utf-8 -*-
'''
Created on 14.12.2013

@author: Meloun
'''
from PyQt4 import QtCore
from ewitis.data.dstore import dstore
from ewitis.gui.UiAccesories import uiAccesories, MSGTYPE
from ewitis.gui.Ui import Ui
from ewitis.data.DEF_ENUM_STRINGS import *



class TabActions():
    
    def __init__(self):
        '''
        Constructor
        '''        
        print "tabActions: constructor"

        
    def addSlots(self):
        #actions
        QtCore.QObject.connect(Ui().pushEnableStartcell, QtCore.SIGNAL("clicked()"), self.sEnableStartcell)
        QtCore.QObject.connect(Ui().pushEnableFinishcell, QtCore.SIGNAL("clicked()"), self.sEnableFinishcell)
        QtCore.QObject.connect(Ui().pushGenerateStarttime, QtCore.SIGNAL("clicked()"), self.sGenerateStarttime)
        QtCore.QObject.connect(Ui().pushGenerateStoptime, QtCore.SIGNAL("clicked()"), self.sGenerateFinishtime)
        QtCore.QObject.connect(Ui().pushQuitTiming, QtCore.SIGNAL("clicked()"), self.sQuitTiming)
        QtCore.QObject.connect(Ui().pushClearDatabase, QtCore.SIGNAL("clicked()"), self.sClearDatabase)
        QtCore.QObject.connect(Ui().pushEnableScanTags, QtCore.SIGNAL("clicked()"), self.sEnableScanTags)
        QtCore.QObject.connect(Ui().pushDisableScanTags, QtCore.SIGNAL("clicked()"), self.sDisableScanTags)
        #QtCore.QObject.connect(Ui().pushSetTimingSettings, QtCore.SIGNAL("clicked()"), lambda: self.sSetTimingSettings(self.GetGuiTimingSettings()))
        
    """                 """
    """ ACTIONS         """
    """                 """
    def sEnableActions(self, state):
        print "A: enable actions: ", state
        self.updateToolbarActions(state)                                                              
    def sEnableStartcell(self):                                                             
        print "A: Enable start cell"                                                                                                                            
        dstore.Set("enable_startcell", 0x01, "SET")                    
    def sEnableFinishcell(self):                                                                    
        print "A: Enable finish cell"                                                                                                                            
        dstore.Set("enable_finishcell", 0x01, "SET")                                                               
    def sGenerateStarttime(self):
        print "A: Generate starttime"                                                                                                                            
        dstore.Set("generate_starttime", 0x01, "SET")                                    
    def sGenerateFinishtime(self):                                                        
        print "A: Generate finishtime"                                                                                                                            
        dstore.Set("generate_finishtime", 0x00, "SET")
    def sGenerateUserFinishtime(self):
        
        #dialog - get user nr
        user_nr = self.showMessage("Generate Finish Time","User Nr: ", msgtype="input_integer", value = 0)                
        if user_nr == None:
            return
        #get user par nr
        tabUser = self.source.tableTags.getTabTagParUserNr(user_nr)
               
        print "A: Generate finishtime from user ", user_nr, tabUser                                                                                                                            
        dstore.Set("generate_finishtime", tabUser['tag_id'], "SET")
                                   
    def sQuitTiming(self):
        if (self.showMessage("Quit Timing", "Are you sure you want to quit timing? \n ", msgtype = MSGTYPE.warning_dialog) != True):            
            return
        print "A: Generate quit time"                                                                                                                                                                                            
        dstore.Set("quit_timing", 0x00, "SET")                   
    def sClearDatabase(self):
        if (self.showMessage("Clear Database", "Are you sure you want to clear all database? \n ", msgtype = MSGTYPE.warning_dialog) != True):            
            return
        print "A: Clear Database"                                                                                                                                                                                            
        dstore.Set("clear_database", 0x00, "SET")
    def sEnableScanTags(self):
        print "A: Enable Scan Tags"                                                                                                                                                                                            
        dstore.Set("tags_reading", 0x01, "SET")
    def sDisableScanTags(self):
        print "A: Disable Scan Tags"                                                                                                                                                                                            
        dstore.Set("tags_reading", 0x00, "SET")
        
    def Update(self, mode = UPDATE_MODE.all):
        """ TIMING SETTINGS"""
        timing_settings_get = dstore.Get("timing_settings", "GET")
        
        #rfid => no enabel start and finish
        if(dstore.Get("rfid") == 0):                
            Ui().pushEnableStartcell.setEnabled(True)
            Ui().pushEnableFinishcell.setEnabled(True)
        elif(dstore.Get("rfid") == 2):
            Ui().pushEnableStartcell.setEnabled(False)
            Ui().pushEnableFinishcell.setEnabled(False)
            
            
        #enable/disable tags reading
        if(timing_settings_get['tags_reading_enable'] == True):
            Ui().pushEnableScanTags.setEnabled(False)
            Ui().pushDisableScanTags.setEnabled(True)
        elif(timing_settings_get['tags_reading_enable'] == False):
            Ui().pushEnableScanTags.setEnabled(True)
            Ui().pushDisableScanTags.setEnabled(False)
        else:
            Ui().pushEnableScanTags.setEnabled(False)
            Ui().pushDisableScanTags.setEnabled(False)
            


        
        
tabActions = TabActions()  
