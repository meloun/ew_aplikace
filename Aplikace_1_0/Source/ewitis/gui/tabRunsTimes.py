# -*- coding: utf-8 -*-
'''
Created on 6.1.2014

@author: Meloun
'''
from PyQt4 import QtCore
from ewitis.gui.aTab import MyTab
from ewitis.gui.UiAccesories import uiAccesories, MSGTYPE
#from ewitis.gui.tableTimes import tableTimes
from ewitis.gui.dfTableRuns import tableRuns
from ewitis.gui.dfTableTags import tableTags
from ewitis.gui.Ui import Ui 
from ewitis.data.db import db
from ewitis.data.dstore import dstore

from ewitis.gui.dfTableTimes import tableTimes

      
class ActionToolbar():
    def __init__(self):
        pass
    def Init(self):
        self.createSlots()
    def createSlots(self):
        #actions toolbar


        QtCore.QObject.connect(Ui().aEnableTagsReading, QtCore.SIGNAL("triggered()"), self.sEnableScanTags)
        QtCore.QObject.connect(Ui().aDisableTagsReading, QtCore.SIGNAL("triggered()"), self.sDisableScanTags)                                
        
    def sGenerateUserFinishtime(self):
        
        #dialog - get user nr
        user_nr = self.showMessage("Generate Finish Time","User Nr: ", msgtype="input_integer", value = 0)                
        if user_nr == None:
            return
        #get user par nr
        tabUser = tableTags.getTabTagParUserNr(user_nr)
               
        print "A: Generate finishtime from user ", user_nr, tabUser                                                                                                                            
        dstore.Set("generate_finishtime", tabUser['tag_id'], "SET")
        
    def Update(self, state = None):                
                
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

        return True
    
    """        """
    """ SLOTS  """
    """        """                                                  
    def sEnableScanTags(self):
        print "A: Enable Scan Tags"                                                                                                                                                                                            
        dstore.Set("tags_reading", 0x01, "SET")
    def sDisableScanTags(self):
        print "A: Disable Scan Tags"                                                                                                                                                                                            
        dstore.Set("tags_reading", 0x00, "SET")
    
actionToolbar = ActionToolbar()
tabRunsTimes = MyTab(tables = [tableRuns, tableTimes], items = [actionToolbar,])  