# -*- coding: utf-8 -*-
'''
Created on 14.12.2013

@author: Meloun
'''

from PyQt4 import QtCore
from ewitis.gui.UiAccesories import uiAccesories
from ewitis.gui.Ui import Ui
from ewitis.data.dstore import dstore
from ewitis.data.DEF_ENUM_STRINGS import *


class TabDevice():
    
    def __init__(self):
        '''
        Constructor
        '''        
        print "tabDevice: constructor"

        
    def addSlots(self):
        QtCore.QObject.connect(Ui().pushBacklight, QtCore.SIGNAL("clicked()"), self.sTerminalBacklight)              
        QtCore.QObject.connect(Ui().pushSpeakerKeys, QtCore.SIGNAL("clicked()"), lambda: self.sTerminalSpeaker("keys"))
        QtCore.QObject.connect(Ui().pushSpeakerSystem, QtCore.SIGNAL("clicked()"), lambda: self.sTerminalSpeaker("system"))
        QtCore.QObject.connect(Ui().pushSpeakerTiming, QtCore.SIGNAL("clicked()"), lambda: self.sTerminalSpeaker("timing"))
        QtCore.QObject.connect(Ui().comboLanguage, QtCore.SIGNAL("activated(int)"), self.sComboLanguage)

        
    def sLimitTime(self):
        hours = Ui().spinLimitTimeHours.value()
        minutes = Ui().spinLimitTimeMinutes.value()
        seconds = Ui().spinLimitTimeSeconds.value()
        miliseconds = Ui().spinLimitTimeMiliseconds.value()*10        
        print hours, minutes, seconds, miliseconds

                             
    def sTerminalBacklight(self):
        
        '''získání a nastavení nové SET hodnoty'''
        aux_terminal_info = dstore.Get("terminal_info", "GET")                        
        dstore.Set("backlight", not(aux_terminal_info["backlight"]), "SET")        
        
        '''reset GET hodnoty'''
        dstore.ResetValue("terminal_info", 'backlight')                                                                
        self.updateTab(TAB.device, UPDATE_MODE.gui)
                                                 
    def sTerminalSpeaker(self, key):
        
        '''získání a nastavení nové SET hodnoty'''
        aux_terminal_info = dstore.Get("terminal_info", "GET")
        aux_speaker = aux_terminal_info['speaker'].copy()       
        aux_speaker[key] = not(aux_speaker[key])                 
        dstore.Set("speaker", aux_speaker, "SET")

        '''reset GET hodnoty'''                
        dstore.ResetValue("terminal_info", 'speaker', key)                                                          
        self.updateTab(TAB.device, UPDATE_MODE.gui)
                             
    def sComboLanguage(self, index):
        print "SLOT", index
        '''získání a nastavení nové SET hodnoty'''                                
        dstore.Set("language", index, "SET")               
        
        '''reset GET hodnoty'''
        dstore.ResetValue("terminal_info", 'language')                                                                
        self.updateTab(TAB.device, UPDATE_MODE.gui)
        
    def sCommCommand(self, index):        
        print DEF_COMMANDS.Get(index)
        '''získání a nastavení nové SET hodnoty'''                                
        #dstore.Set("language", index, "SET")               
        
        '''reset GET hodnoty'''
        #dstore.ResetValue("terminal_info", 'language')                                                                
        #self.updateTab(TAB.device, UPDATE_MODE.gui)

    def Update(self, mode = UPDATE_MODE.all):
        """ HW & FW VERSION """
        aux_versions = dstore.Get("versions")
        
        if(aux_versions['hw'] != None):                                        
            Ui().lineHwVersion.setText(str(aux_versions['hw']))  
        else:
            Ui().lineHwVersion.setText("- -")
             
        if(aux_versions['fw'] != None):                                        
            Ui().lineFwVersion.setText(str(aux_versions['fw']))  
        else:
            Ui().lineFwVersion.setText("- -") 
        
        
        
        """ TERMINAL INFO """
        aux_terminal_info = dstore.Get("terminal_info", "GET")
        
        """ number of cells """
        if(aux_terminal_info['number_of_cells'] != None):
            Ui().lineCells.setText(str(aux_terminal_info['number_of_cells']))                        
        else:
            Ui().lineCells.setText("-") 
            
        
        """ battery """
        if(aux_terminal_info['battery'] != None):
            Ui().lineBattery.setText(str(aux_terminal_info['battery'])+" %")                        
        else:
            Ui().lineBattery.setText("-- %")                                
        
        """ backlight """        
        if(aux_terminal_info['backlight'] == True):
            Ui().lineBacklight.setText("ON")
            Ui().pushBacklight.setText("OFF")
            Ui().pushBacklight.setEnabled(True)
        elif(aux_terminal_info['backlight'] == False):
            Ui().lineBacklight.setText("OFF")
            Ui().pushBacklight.setText("ON")
            Ui().pushBacklight.setEnabled(True)
        else:
            Ui().lineBacklight.setText("- -")
            Ui().pushBacklight.setText("- -")
            Ui().pushBacklight.setEnabled(False)        
        
        """ speaker """        
        if(aux_terminal_info['speaker']['keys'] == True):
            Ui().lineSpeakerKeys.setText("ON")
            Ui().pushSpeakerKeys.setText("OFF")
            Ui().pushSpeakerKeys.setEnabled(True)
            Ui().pushSpeakerSystem.setEnabled(True)
            Ui().pushSpeakerTiming.setEnabled(True)
        elif(aux_terminal_info['speaker']['keys'] == False):
            Ui().lineSpeakerKeys.setText("OFF")
            Ui().pushSpeakerKeys.setText("ON")
            Ui().pushSpeakerKeys.setEnabled(True)
            Ui().pushSpeakerSystem.setEnabled(True)
            Ui().pushSpeakerTiming.setEnabled(True)
        else:
            Ui().lineSpeakerKeys.setText("- -")
            Ui().pushSpeakerKeys.setText("- -")
                    
        if(aux_terminal_info['speaker']['system'] == True):
            Ui().lineSpeakerSystem.setText("ON")
            Ui().pushSpeakerSystem.setText("OFF")
            Ui().pushSpeakerSystem.setEnabled(True)
        elif(aux_terminal_info['speaker']['system'] == False):
            Ui().lineSpeakerSystem.setText("OFF")
            Ui().pushSpeakerSystem.setText("ON")
            Ui().pushSpeakerSystem.setEnabled(True)
        else:
            Ui().lineSpeakerSystem.setText("- -")
            Ui().pushSpeakerSystem.setText("- -")
            Ui().pushSpeakerSystem.setEnabled(False)
            
        if(aux_terminal_info['speaker']['timing'] == True):
            Ui().lineSpeakerTiming.setText("ON")
            Ui().pushSpeakerTiming.setText("OFF")
            Ui().pushSpeakerTiming.setEnabled(True)
        elif(aux_terminal_info['speaker']['timing'] == False):
            Ui().lineSpeakerTiming.setText("OFF")
            Ui().pushSpeakerTiming.setText("ON")
            Ui().pushSpeakerTiming.setEnabled(True)
        else: 
            Ui().lineSpeakerTiming.setText("- -")
            Ui().pushSpeakerTiming.setText("- -")
            Ui().pushSpeakerTiming.setEnabled(False)
        
        if(aux_terminal_info['speaker']['keys'] == None or aux_terminal_info['speaker']['timing']==None or aux_terminal_info['speaker']['system']==None):    
            Ui().pushSpeakerKeys.setEnabled(False)
            Ui().pushSpeakerSystem.setEnabled(False)
            Ui().pushSpeakerTiming.setEnabled(False)
        else:
            Ui().pushSpeakerKeys.setEnabled(True)
            Ui().pushSpeakerSystem.setEnabled(True)
            Ui().pushSpeakerTiming.setEnabled(True)
                
        """ language """          
        if(aux_terminal_info['language'] != None):            
            Ui().comboLanguage.setCurrentIndex(aux_terminal_info['language'])            
            Ui().lineLanguage.setText(Ui().comboLanguage.currentText())                    
        else:            
            Ui().lineLanguage.setText("- -")    
        
tabDevice = TabDevice()  