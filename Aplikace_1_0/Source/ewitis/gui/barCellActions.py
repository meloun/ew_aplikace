# -*- coding: utf-8 -*-
'''
Created on 09.04.2014

@author: Meloun
'''
from PyQt4 import QtCore, QtGui
from ewitis.gui.Ui import appWindow, Ui 
from ewitis.data.dstore import dstore 
from ewitis.gui.UiAccesories import MSGTYPE, uiAccesories
from ewitis.data.DEF_ENUM_STRINGS import * 
from ewitis.gui.tabCells import tabCells

class BarCellActions():
    
    
    
    def __init__(self):
        self.clear_database_changed = False        
    
    def Init(self):
        self.InitGui()        
    
    def InitGui(self):
        ui = Ui()
        self.nr = 6 #dstore.Get("nr_cells")
        
        # list of dict
        # in each dict all gui item
        self.cells_actions = [dict() for _ in range(self.nr)]
        
        #                       
        for i, cell_actions in enumerate(self.cells_actions):                                                                                 
            
            #take care about finish time
            i = self.Collumn2TaskNr(i)            
                             
            # define gui items 
            cell_actions['ping_cell'] = getattr(ui, "aPingCell_"+str(i))
            cell_actions['enable_cell'] = getattr(ui, "aEnableCell_"+str(i))
            cell_actions['generate_celltime'] = getattr(ui, "aGenerateCelltime_"+str(i))
            cell_actions['disable_cell'] = getattr(ui, "aDisableCell_"+str(i))
            
            
            
    def Collumn2TaskNr(self, idx):
        #take care about finish time
        if idx == (self.nr - 1):
            idx = 250 - 1
        return idx+1 
                                
            
    def createSlots(self):
        
        for i, cell_actions in enumerate(self.cells_actions):
            
            #take care about finish time
            i = self.Collumn2TaskNr(i)
            
            if i == 1:
                #add starttime shortcut ("+S")                
                cell_actions['enable_cell'].setShortcuts([cell_actions['enable_cell'].shortcut(), QtGui.QKeySequence("Alt+S")])
                cell_actions['disable_cell'].setShortcuts([cell_actions['disable_cell'].shortcut(), QtGui.QKeySequence("Alt+Ctrl+S")])
                cell_actions['generate_celltime'].setShortcuts([cell_actions['generate_celltime'].shortcut(), QtGui.QKeySequence("Ctrl+S")])
            if i == 250:
                #add finishtime shortcut ("+F")                
                cell_actions['enable_cell'].setShortcuts([cell_actions['enable_cell'].shortcut(), QtGui.QKeySequence("Alt+F")])
                cell_actions['disable_cell'].setShortcuts([cell_actions['disable_cell'].shortcut(), QtGui.QKeySequence("Alt+Ctrl+F")])
                cell_actions['generate_celltime'].setShortcuts([cell_actions['generate_celltime'].shortcut(), QtGui.QKeySequence("Ctrl+F")])
                
            
            # add slots                    
            QtCore.QObject.connect(cell_actions['ping_cell'], QtCore.SIGNAL("triggered()"), lambda task=i : dstore.Set("get_cell_last_times", task, "SET"))
            QtCore.QObject.connect(cell_actions['enable_cell'], QtCore.SIGNAL("triggered()"), lambda task=i: dstore.Set("enable_cell", task, "SET"))        
            QtCore.QObject.connect(cell_actions['generate_celltime'], QtCore.SIGNAL("triggered()"), lambda task=i: dstore.Set("generate_celltime", {'task':task, 'user_id':0}, "SET"))        
            QtCore.QObject.connect(cell_actions['disable_cell'], QtCore.SIGNAL("triggered()"), lambda task=i: dstore.Set("disable_cell", task, "SET"))
        

            
        QtCore.QObject.connect(Ui().aQuitTiming, QtCore.SIGNAL("triggered()"), self.sQuitTiming)
        QtCore.QObject.connect(Ui().aClearDatabase, QtCore.SIGNAL("triggered()"), self.sClearDatabase)
             
#    def sPing(self, task):
#        print "sPing", task
#        
#                
#    def sEnable(self, task):
#        print "sEnable", task
#        dstore.Set("enable_cell", {'task':task}, "SET")                    
#                
#    def sDisable(self, task):
#        print "sDisable", task
#        dstore.Set("disable_cell", {'task':task}, "SET")
#                                                                                                                                                                                                                                 
#    def sGenerateCelltime(self, task, nr = 0):
#        print "sGenerateCelltime", task, nr
#        dstore.Set("generate_celltime", {'task':task, 'user_id':nr}, "SET")                                                               
                
                   
        
    def sQuitTiming(self):
        if (uiAccesories.showMessage("Quit Timing", "Are you sure you want to quit timing? \n ", msgtype = MSGTYPE.warning_dialog) != True):            
            return
        print "A: Generate quit time"                                                                                                                                                                                            
        dstore.Set("quit_timing", 0x00, "SET")
         
    def sClearDatabase(self):
        if (uiAccesories.showMessage("Clear Database", "Are you sure you want to clear all database?\n It will take 20 seconds.\n ", msgtype = MSGTYPE.warning_dialog) != True):            
            return        
        uiAccesories.showMessage("Clear Database", "clearing database, please wait.. it will take 20 seconds.", msgtype = MSGTYPE.statusbar)                                                                                                                                                                                            
        dstore.Set("clear_database", 0x00, "SET")
        self.clear_database_changed = True

        
    def Update(self):  
        #self.lineCellSynchronizedOnce.setStyleSheet("background:"+COLORS.green)      
        
        #enable/disable items in cell toolbar 
        if(dstore.Get('rfid') == 2):
            '''RFID RACE'''
            
            #enable 'generate celltime' for START and FINISH
            for i, cell_actions in enumerate(self.cells_actions):
                for key, action in cell_actions.items():                    
                    if (i==0 or i==5) and (key == 'generate_celltime') and dstore.Get("port")["opened"]:                    
                        action.setEnabled(True)
                    else:
                        action.setEnabled(False)                    
        else:                        
            for i, cell_actions in enumerate(self.cells_actions):
                                            
                cell = tabCells.GetCellParTask(self.Collumn2TaskNr(i))            
                if cell != None and dstore.Get("port")["opened"]:
                                        
                    # PING, set bold if cell activ
                    if cell.GetInfo()['active'] and dstore.Get("port")["opened"]:
                        font = cell_actions['ping_cell'].font()
                        font.setBold(True)
                        font.setUnderline(True)
                        cell_actions['ping_cell'].setFont(font)
                    else:
                        font = cell_actions['ping_cell'].font()
                        font.setBold(False)
                        font.setUnderline(False)
                        cell_actions['ping_cell'].setFont(font)
                        
                    # ENABLE all actions
                    for key, action in cell_actions.items():                                                                
                        action.setEnabled(True)
                        
                else:
                    #DISABLE all actions, cell not configured or no connection with device
                    for key, action in cell_actions.items(): 
                        action.setEnabled(False)
            
        #enabled only when blackbox is connected
        if dstore.Get("port")["opened"]:            
            Ui().aClearDatabase.setEnabled(True)
            Ui().aQuitTiming.setEnabled(True)
        else:
            Ui().aQuitTiming.setEnabled(False)
            Ui().aClearDatabase.setEnabled(False)
            
        #asynchron messages
        if self.clear_database_changed:
            if(dstore.IsChanged("clear_database") == False):
                uiAccesories.showMessage("Clear Database", "Database is empty now", msgtype = MSGTYPE.statusbar)
                self.clear_database_changed = False
                                                          
            
barCellActions = BarCellActions()