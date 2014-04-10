# -*- coding: utf-8 -*-
'''
Created on 8.12.2013

@author: Meloun
'''

import sys
from PyQt4 import QtCore, QtGui
from ewitis.gui.aTab import MyTab, UPDATE_MODE
from ewitis.data.dstore import dstore
from ewitis.gui.Ui import Ui
from ewitis.data.DEF_ENUM_STRINGS import COLORS



class CellGroup ():

    def __init__(self,  nr):
        '''
        Constructor
        group items as class members
        format groupCell_1, checkCell_1.. groupCell_2, checkCell_2 
        '''
        ui = Ui()
                
        self.nr = nr                        
        self.groupbox = getattr(ui, "groupCell_"+str(nr))
        self.checkbox = getattr(ui, "checkCell_"+str(nr))
        self.lineCellTask = getattr(ui, "lineCellTask_"+str(nr))
        self.comboCellTask = getattr(ui, "comboCellTask_"+str(nr))
        self.lineCellBattery = getattr(ui, "lineCellBattery_"+str(nr))
        self.lineCellIrSinal = getattr(ui, "lineCellIrSinal_"+str(nr))
        self.lineCellActive = getattr(ui, "lineCellActive_"+str(nr))
        self.lineCellSynchronizedOnce = getattr(ui, "lineCellSynchronizedOnce_"+str(nr))
        self.lineCellSynchronized = getattr(ui, "lineCellSynchronized_"+str(nr))
        self.lineCellDiagLongOk = getattr(ui, "lineCellDiagLongOk_"+str(nr))
        self.lineCellDiagLongKo = getattr(ui, "lineCellDiagLongKo_"+str(nr))
        self.lineCellDiagLongRatio = getattr(ui, "lineCellDiagLongRatio_"+str(nr))
        self.lineCellDiagShortOk = getattr(ui, "lineCellDiagShortOk_"+str(nr))
        self.lineCellDiagShortKo = getattr(ui, "lineCellDiagShortKo_"+str(nr))
        self.lineCellDiagShortRatio = getattr(ui, "lineCellDiagShortRatio_"+str(nr))
        self.pushCellClearCounters = getattr(ui, "pushCellClearCounters_"+str(nr))
        self.pushCellPing = getattr(ui, "pushCellPing_"+str(nr))
    
    def Init(self):        
        self.createSlots()
        
    def CreateSlots(self):                
        QtCore.QObject.connect(self.checkbox, QtCore.SIGNAL("stateChanged(int)"), self.sCheckbox)
        QtCore.QObject.connect(self.comboCellTask, QtCore.SIGNAL("activated(int)"), self.sComboCellTask)
        QtCore.QObject.connect(self.pushCellClearCounters, QtCore.SIGNAL("clicked()"), self.sSlot)
        QtCore.QObject.connect(self.pushCellPing, QtCore.SIGNAL("clicked()"), self.sSlot)

    '''Slots'''        
    def sSlot(self, state=None):
        print "cellgroup" +str(self.nr)+": something happend - ", state
    
    def sComboCellTask(self, index):                        
        '''získání a nastavení nové SET hodnoty'''
        cell_info = {}
        if index == 6:
            index = 250
        cell_info["task"] = index                               
        cell_info["address"] = self.nr                               
        cell_info["fu1"] = 0x00                               
        cell_info["fu2"] = 0x00                               
        cell_info["fu3"] = 0x00                               
        cell_info["fu4"] = 0x00                        
        dstore.SetItem("cells_info", [self.nr-1], cell_info, "SET", changed = self.nr)                               
        
        '''reset GET hodnoty'''
        dstore.ResetValue("cells_info", self.nr-1, 'task')                                                                
        self.Update()
        
        
    def sCheckbox(self, state):
        
        #enable/disable all widgets
        self.checkbox.setChecked(state)                
        self.lineCellTask.setEnabled(state)
        self.comboCellTask.setEnabled(state)
        self.lineCellBattery.setEnabled(state)
        self.lineCellIrSinal.setEnabled(state)
        self.lineCellActive.setEnabled(state)
        self.lineCellSynchronizedOnce.setEnabled(state)
        self.lineCellSynchronized.setEnabled(state)
        self.lineCellDiagShortOk.setEnabled(state)
        self.lineCellDiagShortKo.setEnabled(state)
        self.lineCellDiagShortRatio.setEnabled(state)
        self.lineCellDiagLongOk.setEnabled(state)
        self.lineCellDiagLongKo.setEnabled(state)
        self.lineCellDiagLongRatio.setEnabled(state)
        self.pushCellClearCounters.setEnabled(state)
        self.pushCellPing.setEnabled(state)
    
    def GetInfo(self):
        return dstore.Get("cells_info", "GET")[self.nr-1]
    def GetTask(self):        
        #print "d1",self.__dict__
        return dstore.Get("cells_info", "GET")[self.nr-1]['task']
    def TaskNr2Idx(self, task):
        #take care about finish time
        if task == 250:
            task = 6
        return task
    def Idx2TaskNr(self, idx):
        #take care about finish time
        if idx == 6:
            idx = 250
        return idx  

    def Update(self):
        
        #get cell info from datastore                                      
        cell_info = self.GetInfo()

        #task
        if(cell_info['task'] != None):
            self.lineCellTask.setText(self.comboCellTask.itemText(cell_info["task"]))
        else:
            self.lineCellTask.setText(" - - - ")
        
        #battery
        if(cell_info['battery'] != None):
            self.lineCellBattery.setText(str(cell_info['battery'])+" %")                        
        else:
            self.lineCellBattery.setText(" - - %")                                                                                  
        
        #ir signal                
        if cell_info["ir_signal"] == True:
            self.lineCellIrSinal.setText("IR SIGNAL")
        elif cell_info["ir_signal"] == False:
            self.lineCellIrSinal.setText("NO IR SIGNAL")
        else:
            self.lineCellIrSinal.setText(" - - ")

        #active            
        if cell_info["active"] == True:
            self.lineCellActive.setText("ACTIVE")
        elif cell_info["active"] == False:
            self.lineCellActive.setText("BLOCKED")
        else:
            self.lineCellActive.setText(" - - ")
            
        #synchronized once
        if cell_info["synchronized_once"] == True:
            self.lineCellSynchronizedOnce.setText("ONCE")
            self.lineCellSynchronizedOnce.setStyleSheet("background:"+COLORS.green)
        elif cell_info["synchronized_once"] == False:
            self.lineCellSynchronizedOnce.setText("ONCE")
            self.lineCellSynchronizedOnce.setStyleSheet("background:grey"+COLORS.red)
        else:
            self.lineCellSynchronizedOnce.setText(" - - ")
            self.lineCellSynchronizedOnce.setStyleSheet("")
        
        #synchronized
        if cell_info["synchronized"] == True:
            self.lineCellSynchronized.setText("10MIN")
            self.lineCellSynchronized.setStyleSheet("background:"+COLORS.green)
        elif cell_info["synchronized"] == False:
            self.lineCellSynchronized.setText("10MIN")
            self.lineCellSynchronized.setStyleSheet("background:"+COLORS.red)
        else:
            self.lineCellSynchronized.setText(" - - ")
            self.lineCellSynchronized.setStyleSheet("")                        
        
        #diagnostic shork ok
        if(cell_info['diagnostic_short_ok'] != None):                                    
            self.lineCellDiagShortOk.setText(str(cell_info['diagnostic_short_ok']))
        else:
            self.lineCellDiagShortOk.setText("- -")
                                          
        #diagnostic short ko
        if(cell_info['diagnostic_short_ko'] != None):                                    
            self.lineCellDiagShortKo.setText(str(cell_info['diagnostic_short_ko']))
        else:
            self.lineCellDiagShortKo.setText("- -")            
        #diagnostic %
        if(cell_info['diagnostic_short_ok'] != None) and (cell_info['diagnostic_short_ko'] != None) and (cell_info['diagnostic_short_ko'] != 0):                                    
            self.lineCellDiagShortRatio.setText(str(cell_info['diagnostic_short_ok']/cell_info['diagnostic_short_ko']))
        else:
            self.lineCellDiagShortRatio.setText("- -")
            
        #diagnostic shork ok
        if(cell_info['diagnostic_long_ok'] != None):                                    
            self.lineCellDiagLongOk.setText(str(cell_info['diagnostic_long_ok']))
        else:
            self.lineCellDiagLongOk.setText("- -")
                                          
        #diagnostic long ko
        if(cell_info['diagnostic_long_ko'] != None):                                    
            self.lineCellDiagLongKo.setText(str(cell_info['diagnostic_long_ko']))
        else:
            self.lineCellDiagLongKo.setText("- -")            
        #diagnostic %
        if(cell_info['diagnostic_long_ok'] != None) and (cell_info['diagnostic_long_ko'] != None) and (cell_info['diagnostic_long_ko'] != 0):                                    
            self.lineCellDiagLongRatio.setText(str(cell_info['diagnostic_long_ok']/cell_info['diagnostic_long_ko']))
        else:
            self.lineCellDiagLongRatio.setText("- -")

class TabCells(MyTab):
    
    def __init__(self):
        '''
        Constructor
        '''        
        print "tabCells: constructor"
        
    def Init(self):
        '''tab Cells'''        
        self.nr  = dstore.Get("nr_cells")                      
        self.cellgroups = [None]*self.nr
        for i in range(0,self.nr):            
            self.cellgroups[i] = CellGroup(i+1)
            self.cellgroups[i].CreateSlots()
            
        self.CreateSlots()
        
    def CreateSlots(self):                        
        QtCore.QObject.connect(Ui().pushCellAllReadOnly, QtCore.SIGNAL("clicked()"), lambda:self.sEnableAll(False))
        QtCore.QObject.connect(Ui().pushCellAllEdit, QtCore.SIGNAL("clicked()"), lambda:self.sEnableAll(True))
    def sEnableAll(self, state):        
        for i in range(0,self.nr):
            self.cellgroups[i].sCheckbox(state)
            
    def GetCellParTask(self, task):        
        for cellgroup in self.cellgroups:            
            if cellgroup.GetTask() == task:                
                return cellgroup
        return None                                                                           
    
        
    def Update(self, mode = UPDATE_MODE.all):
        for i in range(0,self.nr):
            self.cellgroups[i].Update()
        return True        
    
         
tabCells = TabCells()
        

if __name__ == "__main__":         
    import ewitis.gui.Ui_App as Ui_App  
        
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_App.Ui_MainWindow()
    ui.setupUi(MainWindow)     

    GroupWithCheckbox_1 = CellGroup(ui,1)
    print "title: ", GroupWithCheckbox_1.groupbox.title()
    print "title: ", GroupWithCheckbox_1.lineCellIrSinal.text()


        