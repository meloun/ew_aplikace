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
        pass
    
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
            
            # add slots                    
            QtCore.QObject.connect(cell_actions['ping_cell'], QtCore.SIGNAL("triggered()"), lambda task=i : self.sPing(task))
            QtCore.QObject.connect(cell_actions['enable_cell'], QtCore.SIGNAL("triggered()"), lambda task=i: self.sEnable(task))        
            QtCore.QObject.connect(cell_actions['generate_celltime'], QtCore.SIGNAL("triggered()"), lambda task=i: self.sGenerateCelltime(task))        
            QtCore.QObject.connect(cell_actions['disable_cell'], QtCore.SIGNAL("triggered()"), lambda task=i: self.sDisable(task))
            
        QtCore.QObject.connect(Ui().aQuitTiming, QtCore.SIGNAL("triggered()"), self.sQuitTiming)
        QtCore.QObject.connect(Ui().aClearDatabase, QtCore.SIGNAL("triggered()"), self.sClearDatabase)
             
    def sPing(self, task):
        print "sPing", task
        
                
    def sEnable(self, task):
        print "sEnable", task
        dstore.Set("enable_cell", {'task':task}, "SET")                    
                
    def sDisable(self, task):
        print "sDisable", task
        dstore.Set("disable_cell", {'task':task}, "SET")
                                                                                                                                                                                                                                 
    def sGenerateCelltime(self, task, nr = 0):
        print "sGenerateCelltime", task, nr
        dstore.Set("generate_celltime", {'task':task, 'user_id':nr}, "SET")                                                               
                
                   
        
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

        
    def Update(self):  
        #self.lineCellSynchronizedOnce.setStyleSheet("background:"+COLORS.green)      
        
        #enable/disable items in cell toolbar                    
        for i, cell_actions in enumerate(self.cells_actions):
            #print cell_actions
            cell = tabCells.GetCellParTask(self.Collumn2TaskNr(i))            
            if cell != None:
                if cell.GetInfo()['active']:
                    font = cell_actions['ping_cell'].font()
                    font.setBold(True)
                    font.setUnderline(True)
                    cell_actions['ping_cell'].setFont(font)
                else:
                    font = cell_actions['ping_cell'].font()
                    font.setBold(False)
                    font.setUnderline(False)
                    cell_actions['ping_cell'].setFont(font)
                    
                for key, action in cell_actions.items():                                            
                    action.setEnabled(True)                    
            else:
                for key, action in cell_actions.items(): 
                    action.setEnabled(False)                                             
            
barCellActions = BarCellActions()