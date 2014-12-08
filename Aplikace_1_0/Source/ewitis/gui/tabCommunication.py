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
            if(value['Blackbox-RFID']):
                aux_cmd += " RFID"              
            elif(value['Blackbox-IR']):
                aux_cmd += " IR"
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
        return True
        
    def CreateSlots(self):
        QtCore.QObject.connect(Ui().comboCommCommand, QtCore.SIGNAL("activated(int)"), self.sComboCommand)
        QtCore.QObject.connect(Ui().spinCommDatalength, QtCore.SIGNAL("valueChanged(int)"), self.sSpinDatalength)               
        QtCore.QObject.connect(Ui().pushCommSend, QtCore.SIGNAL("clicked()"), self.sSendCommand)
        QtCore.QObject.connect(Ui().checkCommLogCyclic, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("diagnostic", ["log_cyclic"], state))
        QtCore.QObject.connect(Ui().pushCommClearLog, QtCore.SIGNAL("clicked()"), self.sCommClearLog)
            
          
    """                 """
    """ COMMUNICATION   """
    """                 """
    def sComboCommand(self, index):
        DEF_COMMANDS.SetDiagnosticCommand(cmd = 0xFF) #because of sorting        
        cmd = DEF_COMMANDS.GetSorted()[index]
        cmd_cmd = cmd[1]['cmd']
        cmd_datalength = cmd[1]['length']
        
        #copy cmd and length to 2 spinboxes
        cmd_cmd = "%x" % cmd_cmd # number to 'AA'
        Ui().lineCommCommand.setText(cmd_cmd)
        Ui().spinCommDatalength.setValue(cmd_datalength)                
        
        #enable/disable spinboxes
        print cmd[0]
        if cmd[0] == "DIAGNOSTIC_COMMAND":
            Ui().lineCommCommand.setEnabled(True)
            Ui().spinCommDatalength.setEnabled(True)
        else: 
            Ui().lineCommCommand.setEnabled(False)
            Ui().spinCommDatalength.setEnabled(False)                           
        
        #update senddata lenfth        
        Ui().lineCommData.setInputMask((cmd_datalength * "HH ")+";0")
        
    def sSpinDatalength(self):
        #update senddata lenfth        
        Ui().lineCommData.setInputMask((Ui().spinCommDatalength.value() * "HH ")+";0")             
            
    def sSendCommand(self):         
        
        cmd_index = Ui().comboCommCommand.currentIndex()
        DEF_COMMANDS.SetDiagnosticCommand(cmd = 0xFF) #because of sorting
        cmd_key = DEF_COMMANDS.GetSorted()[cmd_index][0]
        
        #prepare command anda datalength, if diagnostic
        if cmd_key == "DIAGNOSTIC_COMMAND":
            DEF_COMMANDS.SetDiagnosticCommand(cmd = int(str(Ui().lineCommCommand.text()), 16))
            DEF_COMMANDS.SetDiagnosticCommand(length = Ui().spinCommDatalength.value())
            
        #prepare data data
        data = str(Ui().lineCommData.displayText().replace(" ", ""))
        
        #set to datastore
        uiAccesories.sGuiSetItem("diagnostic", ["sendcommandkey"], cmd_key)                        
        uiAccesories.sGuiSetItem("diagnostic", ["senddata"], data)
        
        #print "send command:", cmd_key, data
        
                                
    def sCommClearLog(self):
        Ui().textCommLog.clear()
        dstore.InitDiagnostic()
        

        
tabCommunication = TabCommunication()         