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
            QtCore.QObject.connect(cell_actions['ping_cell'], QtCore.SIGNAL("triggered()"), lambda nr=i : self.sPing(nr))
            QtCore.QObject.connect(cell_actions['enable_cell'], QtCore.SIGNAL("triggered()"), lambda nr=i: self.sEnable(nr))        
            QtCore.QObject.connect(cell_actions['generate_celltime'], QtCore.SIGNAL("triggered()"), lambda nr=i: self.sGenerateCelltime(nr))        
            QtCore.QObject.connect(cell_actions['disable_cell'], QtCore.SIGNAL("triggered()"), lambda nr=i: self.sDisable(nr))
             
    def sPing(self, nr):
        print "sPing", nr
                
    def sEnable(self, nr):
        print "sEnable", nr
                
    def sGenerateCelltime(self, nr):
        print "sGenerateCelltime", nr
                
    def sDisable(self, nr):
        print "sDisable", nr        

        
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