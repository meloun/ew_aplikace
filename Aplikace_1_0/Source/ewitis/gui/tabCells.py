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
        self.lineCellCounter1 = getattr(ui, "lineCellCounter1_"+str(nr))
        self.lineCellCounter2 = getattr(ui, "lineCellCounter2_"+str(nr))
        self.lineCellCounter3 = getattr(ui, "lineCellCounter3_"+str(nr))
        self.pushCellClearCounters = getattr(ui, "pushCellClearCounters_"+str(nr))
        self.pushCellPing = getattr(ui, "pushCellPing_"+str(nr))
    
    def Init(self):        
        self.createSlots()
        
    def CreateSlots(self):                
        QtCore.QObject.connect(self.checkbox, QtCore.SIGNAL("stateChanged(int)"), self.sCheckbox)
        QtCore.QObject.connect(self.comboCellTask, QtCore.SIGNAL("activated(int)"), self.sSlot)
        QtCore.QObject.connect(self.pushCellClearCounters, QtCore.SIGNAL("clicked()"), self.sSlot)
        QtCore.QObject.connect(self.pushCellPing, QtCore.SIGNAL("clicked()"), self.sSlot)

    '''Slots'''        
    def sSlot(self, state=None):
        print "cellgroup" +str(self.nr)+": something happend - ", state
        
        
    def sCheckbox(self, state):
        
        #enable/disable all widgets                
        self.lineCellTask.setEnabled(state)
        self.comboCellTask.setEnabled(state)
        self.lineCellBattery.setEnabled(state)
        self.lineCellIrSinal.setEnabled(state)
        self.lineCellActive.setEnabled(state)
        self.lineCellSynchronizedOnce.setEnabled(state)
        self.lineCellSynchronized.setEnabled(state)
        self.lineCellCounter1.setEnabled(state)
        self.lineCellCounter2.setEnabled(state)
        self.lineCellCounter3.setEnabled(state)
        self.pushCellClearCounters.setEnabled(state)
        self.pushCellPing.setEnabled(state)
    
    def Update(self):
        
        #get data from datastore        
        cell_info = dstore.Get("cells_info", "GET")[self.nr-1]

        #task
        if(cell_info['task'] != None):
            self.lineCellTask.setText(cell_info["task"])
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
        
        #diagnostic 1
        if(cell_info['diagnostic1'] != None):                                    
            self.lineCellCounter1.setText(str(cell_info['diagnostic1']))
        else:
            self.lineCellCounter1.setText("- -")
                                          
        #diagnostic 2
        if(cell_info['diagnostic2'] != None):                                    
            self.lineCellCounter2.setText(str(cell_info['diagnostic2']))
        else:
            self.lineCellCounter2.setText("- -")
            
        #diagnostic %
        if(cell_info['diagnostic1'] != None) and (cell_info['diagnostic2'] != None):                                    
            self.lineCellCounter3.setText(str(cell_info['diagnostic1']/cell_info['diagnostic2']))
        else:
            self.lineCellCounter3.setText("- -")

class TabCells(MyTab):
    
    def __init__(self):
        '''
        Constructor
        '''        
        print "tabCells: constructor"
        
    def Init(self):
        '''tab Cells'''        
        self.cellgroups = [None]*2
        for i in range(0,2):            
            self.cellgroups[i] = CellGroup(i+1)
            self.cellgroups[i].CreateSlots()                            
        
    def Update(self, mode = UPDATE_MODE.all):
        for i in range(0,2):
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


        