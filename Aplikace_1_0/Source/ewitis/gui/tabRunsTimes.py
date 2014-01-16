# -*- coding: utf-8 -*-
'''
Created on 6.1.2014

@author: Meloun
'''
from PyQt4 import QtCore
from ewitis.gui.aTab import MyTab
from ewitis.gui.UiAccesories import uiAccesories, MSGTYPE
from ewitis.gui.tableTimes import tableTimes
from ewitis.gui.tableRuns import tableRuns
from ewitis.gui.tableTags import tableTags
from ewitis.gui.Ui import Ui 
from ewitis.data.db import db
from ewitis.data.dstore import dstore

      
class ActionToolbar():
    def __init__(self):
        pass
    def Init(self):
        self.createSlots()
    def createSlots(self):
        #actions toolbar
        QtCore.QObject.connect(Ui().aActionsEnable, QtCore.SIGNAL("triggered(bool)"), self.sEnableActions)
        QtCore.QObject.connect(Ui().aEnableStart, QtCore.SIGNAL("triggered()"), self.sEnableStartcell)
        QtCore.QObject.connect(Ui().aGenerateStarttime, QtCore.SIGNAL("triggered()"), self.sGenerateStarttime)
        QtCore.QObject.connect(Ui().aGenerateFinishtime, QtCore.SIGNAL("triggered()"), self.sGenerateFinishtime)        
        QtCore.QObject.connect(Ui().aEnableFinish, QtCore.SIGNAL("triggered()"), self.sEnableFinishcell)
        QtCore.QObject.connect(Ui().aQuitTiming, QtCore.SIGNAL("triggered()"), self.sQuitTiming)
        QtCore.QObject.connect(Ui().aEnableTagsReading, QtCore.SIGNAL("triggered()"), self.sEnableScanTags)
        QtCore.QObject.connect(Ui().aDisableTagsReading, QtCore.SIGNAL("triggered()"), self.sDisableScanTags)
        QtCore.QObject.connect(Ui().aClearDatabase, QtCore.SIGNAL("triggered()"), self.sClearDatabase)
        
    def Update(self, state = None):                
                
        if(state == None):            
            state = Ui().aActionsEnable.isChecked()       
       
        #enable start, enable finish cell
        if(state == False):
            Ui().aEnableStart.setEnabled(False)
            Ui().aEnableFinish.setEnabled(False)
        elif(dstore.Get("rfid") == 0):        
            Ui().aEnableStart.setEnabled(state)
            Ui().aEnableFinish.setEnabled(state)
        else:#if(dstore.Get("rfid") == 2):
            Ui().aEnableStart.setEnabled(False)
            Ui().aEnableFinish.setEnabled(False)
       
        #Enable and Disable Tags Reading     
        timing_settings_get = dstore.Get("timing_settings", "GET")
        if(state == False):
            Ui().aEnableTagsReading.setEnabled(False)
            Ui().aDisableTagsReading.setEnabled(False)                            
        elif(timing_settings_get['tags_reading_enable'] == True):
            Ui().aEnableTagsReading.setEnabled(False)
            Ui().aDisableTagsReading.setEnabled(True)
        elif(timing_settings_get['tags_reading_enable'] == False):
            Ui().aEnableTagsReading.setEnabled(True)
            Ui().aDisableTagsReading.setEnabled(False)
        else:
            Ui().aEnableTagsReading.setEnabled(False)
            Ui().aDisableTagsReading.setEnabled(False)

        #generate start and finish time        
        Ui().aGenerateStarttime.setEnabled(state)
        Ui().aGenerateFinishtime.setEnabled(state)
        
        #quit timinq
        Ui().aQuitTiming.setEnabled(state)
        
        #clear database
        Ui().aClearDatabase.setEnabled(state)
    
    """        """
    """ SLOTS  """
    """        """
    def sEnableActions(self, state):
        print "A: enable actions: ", state
        self.Update(state)                                                              
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
        tabUser = tableTags.getTabTagParUserNr(user_nr)
               
        print "A: Generate finishtime from user ", user_nr, tabUser                                                                                                                            
        dstore.Set("generate_finishtime", tabUser['tag_id'], "SET")
                                   
    def sQuitTiming(self):
        if (uiAccesories.showMessage("Quit Timing", "Are you sure you want to quit timing? \n ", msgtype = MSGTYPE.warning_dialog) != True):            
            return
        print "A: Generate quit time"                                                                                                                                                                                            
        dstore.Set("quit_timing", 0x00, "SET")                   
    def sClearDatabase(self):
        if (uiAccesories.showMessage("Clear Database", "Are you sure you want to clear all database? \n ", msgtype = MSGTYPE.warning_dialog) != True):            
            return
        print "A: Clear Database"                                                                                                                                                                                            
        dstore.Set("clear_database", 0x00, "SET")
    def sEnableScanTags(self):
        print "A: Enable Scan Tags"                                                                                                                                                                                            
        dstore.Set("tags_reading", 0x01, "SET")
    def sDisableScanTags(self):
        print "A: Disable Scan Tags"                                                                                                                                                                                            
        dstore.Set("tags_reading", 0x00, "SET")
    
actionToolbar = ActionToolbar()
tabRunsTimes = MyTab(tables = [tableRuns, tableTimes], items = [actionToolbar,])  