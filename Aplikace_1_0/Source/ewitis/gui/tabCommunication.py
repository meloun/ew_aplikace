# -*- coding: utf-8 -*-
'''
Created on 14.12.2013

@author: Meloun
'''

from PyQt4 import QtCore, QtGui
from ewitis.gui.aTab import MyTab, UPDATE_MODE
from ewitis.data.dstore import dstore
from ewitis.gui.Ui import Ui
from ewitis.gui.UiAccesories import uiAccesories
import ewitis.comm.DEF_COMMANDS as DEF_COMMANDS



class TabCommunication(MyTab):
    
    def __init__(self):
        '''
        Constructor
        '''        
        print "tabCommunication: constructor"
        
    def Init(self):        
        '''init combobox command'''
        aux_commands = []        
        for key, value in DEF_COMMANDS.GetSorted():
            #prepare item name
            aux_cmd_key = "%02X" % value['cmd']            
            aux_cmd = "x"+aux_cmd_key+" "+key.lower() + " " + str(value['length'])+"b"            
            if(value['terminal']):
                aux_cmd += " B"              
            if(value['terminal']):
                aux_cmd += " T"
            #add item                        
            aux_commands.append(aux_cmd)
        #set item from a list        
        Ui().comboCommCommand.addItems(aux_commands)
        #update lineedit length
        self.sComboCommand(0)
        #clear log        
        self.sCommClearLog()
        
        self.CreateSlots()
    
    def Update(self, mode = UPDATE_MODE.all):
        aux_diagnostic = dstore.Get("diagnostic")
        #set checkbox
        Ui().checkCommLogCyclic.setCheckState(aux_diagnostic['log_cyclic'])            
        #log request?            
        if aux_diagnostic["communication"] != "":                                        
            if len(Ui().textCommLog.toPlainText()) > 90000:                    
                self.sCommClearLog()
            Ui().textCommLog.insertHtml(aux_diagnostic["communication"])
            Ui().textCommLog.moveCursor(QtGui.QTextCursor.End)
            dstore.SetItem("diagnostic", ["communication"], "")                         
            #vsb = Ui().textCommLog.verticalScrollBar()
            #vsb.setValue(vsb.maximum())            
            #Ui().textCommLog.ensureCursorVisible()            
        Ui().labelCommResponse.setText(aux_diagnostic["sendresponse"])

        
    def CreateSlots(self):
        QtCore.QObject.connect(Ui().comboCommCommand, QtCore.SIGNAL("activated(int)"), self.sComboCommand)
        QtCore.QObject.connect(Ui().pushCommSend, QtCore.SIGNAL("clicked()"), self.sSendCommand)
        QtCore.QObject.connect(Ui().checkCommLogCyclic, QtCore.SIGNAL("stateChanged(int)"), lambda state: self.sGuiSetItem("diagnostic", ["log_cyclic"], state, self.Update()))
        QtCore.QObject.connect(Ui().pushCommClearLog, QtCore.SIGNAL("clicked()"), self.sCommClearLog)                 
            
          
    """                 """
    """ COMMUNICATION   """
    """                 """
    def sComboCommand(self, index):        
        cmd = DEF_COMMANDS.GetSorted()[index]
        cmd_length = cmd[1]['length']
        
        #update senddata lenfth        
        Ui().lineCommData.setInputMask((cmd_length * "HH ")+";0")             
            
    def sSendCommand(self):
        
        cmd_index = Ui().comboCommCommand.currentIndex()
        cmd_key = DEF_COMMANDS.GetSorted()[cmd_index][0]
        data = str(Ui().lineCommData.displayText ().replace(" ", ""))
        
        #set to datastore
        uiAccesories.sGuiSetItem("diagnostic", ["sendcommandkey"], cmd_key)                        
        uiAccesories.sGuiSetItem("diagnostic", ["senddata"], data)
        
        #print "send command:", cmd_key, data
        
                                
    def sCommClearLog(self):
        Ui().textCommLog.clear()
        dstore.InitDiagnostic()
        

        
tabCommunication = TabCommunication()         