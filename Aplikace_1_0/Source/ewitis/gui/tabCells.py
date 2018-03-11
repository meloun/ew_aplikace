# -*- coding: utf-8 -*-
'''
Created on 8.12.2013

@author: Meloun
'''

import sys
from PyQt4 import QtCore, QtGui
from ewitis.gui.aTab import MyTab, UPDATE_MODE
from ewitis.gui.UiAccesories import MSGTYPE, uiAccesories
from ewitis.data.dstore import dstore
from ewitis.gui.Ui import Ui
from ewitis.data.DEF_ENUM_STRINGS import COLORS, STATUS
from ewitis.data.DEF_DATA import *



class CellGroup ():
    
    TIMER_NOCHANGE = 25  
    TIMER_NODIALOG_INIT = 25   

    def __init__(self,  nr):
        '''
        Constructor
        group items as class members
        format groupCell_1, checkCell_1.. groupCell_2, checkCell_2 
        '''
        ui = Ui()
                
        self.nr = nr                        
        self.groupbox = getattr(ui, "groupCell_"+str(nr))        
        self.lineCellTask = getattr(ui, "lineCellTask_"+str(nr))
        self.comboCellTask = getattr(ui, "comboCellTask_"+str(nr))
        self.lineCellTrigger = getattr(ui, "lineCellTrigger_"+str(nr))
        self.comboCellTrigger = getattr(ui, "comboCellTrigger_"+str(nr))
        self.lineCellAutoEnable = getattr(ui, "lineCellAutoEnable_"+str(nr))
        self.comboCellAutoEnable = getattr(ui, "comboCellAutoEnable_"+str(nr))
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
        self.pushCellRunDiagnostic = getattr(ui, "pushCellRunDiagnostic_"+str(nr))
        self.pushCellPing = getattr(ui, "pushCellPing_"+str(nr))
        
        self.timer_nodialog = CellGroup.TIMER_NODIALOG_INIT
        self.timer_nochange = CellGroup.TIMER_NOCHANGE
        self.initialized = False
        
    
    def Init(self):        
        self.createSlots()
        
        
    def CreateSlots(self):                        
        QtCore.QObject.connect(self.comboCellTask, QtCore.SIGNAL("activated(int)"), self.sComboCellTask)
        QtCore.QObject.connect(self.comboCellTrigger, QtCore.SIGNAL("activated(int)"), self.sComboCellTrigger)
        QtCore.QObject.connect(self.comboCellAutoEnable, QtCore.SIGNAL("activated(int)"), self.sComboCellAutoEnable)
        QtCore.QObject.connect(self.pushCellClearCounters, QtCore.SIGNAL("clicked()"), lambda: dstore.SetItem("set_cell_diag_info", ["address"], self.nr, "SET"))
        QtCore.QObject.connect(self.pushCellRunDiagnostic, QtCore.SIGNAL("clicked()"), lambda: dstore.Set("run_cell_diagnostic", self.nr, "SET"))
        QtCore.QObject.connect(self.pushCellPing, QtCore.SIGNAL("clicked()"), lambda: dstore.Set("ping_cell", self.nr, "SET"))

    '''Slots'''        
    def sSlot(self, state=None):
        print "cellgroup" +str(self.nr)+": something happend - ", state 
    
    def sComboCellTask(self, index):                        
        '''získání a nastavení nové SET hodnoty'''
        cells_info = dstore.Get("cells_info", "GET")
        get_cell_info = cells_info[self.nr-1]
        set_cell_info = {}
        task = self.Idx2TaskNr(index)
        set_cell_info["task"] = task
        set_cell_info["trigger"] = get_cell_info["trigger"]
        set_cell_info["auto_enable"] = get_cell_info["auto_enable"]                               
        set_cell_info["address"] = self.nr                               
        set_cell_info["fu1"] = 0x00                               
        set_cell_info["fu2"] = 0x00        
        
        cells_info = dstore.Get("cells_info", "GET")
        
        if task != 0:
            for info in cells_info:
                if info['task'] == task:         
                    self.comboCellTask.setCurrentIndex(self.TaskNr2Idx(get_cell_info["task"]))                                                                                                            
                    uiAccesories.showMessage("Cell Update error", "Cannot assign this task, probably already exist!")
                    return        
                               
        dstore.SetItem("cells_info", [self.nr-1], set_cell_info, "SET", changed = [self.nr-1])                               
        
        '''reset GET hodnoty'''
        dstore.ResetValue("cells_info", [self.nr-1, 'task'])
        #self.timer_nochange = CellGroup.TIMER_NOCHANGE
      
        
    def sComboCellTrigger(self, index):                        
        '''získání a nastavení nové SET hodnoty'''
        cells_info = dstore.Get("cells_info", "GET")
        get_cell_info = cells_info[self.nr-1]
        set_cell_info = {}
        set_cell_info["address"] = self.nr
        set_cell_info["task"] = get_cell_info["task"]                                                                      
        set_cell_info["trigger"] = index
        set_cell_info["auto_enable"] = get_cell_info["auto_enable"]                               
        set_cell_info["fu1"] = 0x00                               
        set_cell_info["fu2"] = 0x00                                      
                               
        dstore.SetItem("cells_info", [self.nr-1], set_cell_info, "SET", changed = [self.nr-1])                               
        
        '''reset GET hodnoty'''
        dstore.ResetValue("cells_info", [self.nr-1, 'trigger'])
        #self.timer_nochange = CellGroup.TIMER_NOCHANGE
        
    def sComboCellAutoEnable(self, index):                        
        '''získání a nastavení nové SET hodnoty'''
        cells_info = dstore.Get("cells_info", "GET")
        get_cell_info = cells_info[self.nr-1]
        set_cell_info = {}
        set_cell_info["address"] = self.nr                               
        set_cell_info["task"] = get_cell_info["task"]                                                                      
        set_cell_info["trigger"] = get_cell_info["trigger"]
        set_cell_info["auto_enable"] = index
        set_cell_info["fu1"] = 0x00                               
        set_cell_info["fu2"] = 0x00            
                               
        dstore.SetItem("cells_info", [self.nr-1], set_cell_info, "SET", changed = [self.nr-1])                               
        
        '''reset GET hodnoty'''
        dstore.ResetValue("cells_info", [self.nr-1, 'auto_enable'])
        #self.timer_nochange = CellGroup.TIMER_NOCHANGE       
        
        
    def SetEnabled(self, state, state2):        
        #enable/disable all widgets            
        self.lineCellTask.setEnabled(state)        
        self.lineCellTrigger.setEnabled(state)        
        self.lineCellAutoEnable.setEnabled(state)
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
        self.pushCellRunDiagnostic.setEnabled(state)
        self.pushCellPing.setEnabled(state)
        
        if state2:        
            self.comboCellTask.setEnabled(True)
        else:
            self.comboCellTask.setEnabled(state)
            
        self.comboCellTrigger.setEnabled(state)
        self.comboCellAutoEnable.setEnabled(state)
    
    def GetInfo(self):
        return dstore.Get("cells_info", "GET")[self.nr-1]
    def SetInfo(self):
        return dstore.Get("cells_info", "SET")[self.nr-1]
    
    def GetTask(self):        
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
        get_info = self.GetInfo()
        set_info = self.SetInfo()
        port_open = dstore.Get("port")["opened"]
        
        #set enabled               
        if(port_open ==False) or (get_info['task'] == None) or (get_info['task'] == 0):
            self.SetEnabled(False, port_open)
        else: 
            self.SetEnabled(True, port_open)                    
        
        #task
        index = self.TaskNr2Idx(get_info["task"])        
        if(get_info['task'] != None):
            self.lineCellTask.setText(self.comboCellTask.itemText(index))
        else:
            self.lineCellTask.setText(" - - - ")                                    
        colors_enabled =  get_info['task']
        #self.lineCellTask.setStyleSheet("background:"+COLORS.GetColor(self.lineCellTask.text(), get_info['task']))                    
            
        #trigger                            
        if(get_info['trigger'] != None):
            self.lineCellTrigger.setText(self.comboCellTrigger.itemText(get_info['trigger']))
        else:
            self.lineCellTrigger.setText(" - - - ")                                                    
        
        #auto enable        
        if(get_info['auto_enable'] != None):
            self.lineCellAutoEnable.setText(self.comboCellAutoEnable.itemText(get_info['auto_enable']))
        else:
            self.lineCellAutoEnable.setText(" - - - ")
        #self.lineCellAutoEnable.setStyleSheet("background:"+COLORS.GetColor(self.lineCellAutoEnable.text(), get_info['auto_enable']))
                 
                               
        #synchronize comboboxes with GET value (after timeout)
        if port_open:            
            if dstore.Get("cells_initiated") == True:
                if(self.initialized == False):                    
                    self.initialized = True
                    
                    task_index = self.TaskNr2Idx(get_info["task"])
                    if task_index:
                        if(task_index != self.comboCellTask.currentIndex()):
                            self.comboCellTask.setCurrentIndex(task_index)
                            dstore.SetItem("cells_info", [self.nr-1, "task"], get_info["task"], "SET", changed = False)
                            #if port_open and (self.timer_nodialog==0):                    
                            #    uiAccesories.showMessage("Cell Update error", "Cannot assign this task!")           
                    else:
                        self.comboCellTask.setCurrentIndex(0) #get value None <= "- - -"
                    
                    if get_info["trigger"] != None:
                        if(get_info["trigger"] != self.comboCellTrigger.currentIndex()):
                            self.comboCellTrigger.setCurrentIndex(get_info["trigger"])
                            dstore.SetItem("cells_info", [self.nr-1, "trigger"], get_info["trigger"], "SET", changed = False)
                            #if port_open and (self.timer_nodialog==0):                 
                            #    uiAccesories.showMessage("Cell Update error", "Cannot assign this trigger!")  
                    else:                
                        self.comboCellTrigger.setCurrentIndex(0)  #get value None <= "- - -"
                    
                    if get_info["auto_enable"] != None:
                        if(get_info["auto_enable"] != self.comboCellAutoEnable.currentIndex()):
                            self.comboCellAutoEnable.setCurrentIndex(get_info["auto_enable"])
                            dstore.SetItem("cells_info", [self.nr-1, "auto_enable"], get_info["auto_enable"], "SET", changed = False)
                            #if port_open and (self.timer_nodialog==0):                 
                            #    uiAccesories.showMessage("Cell Update error", "Cannot assign this settings!")  
                    else:                
                        self.comboCellAutoEnable.setCurrentIndex(0)  #get value None <= "- - -"         
        
        #set match color        
        match = (get_info['task'] == set_info['task'])
        #print "TZZ", self.nr, get_info['task'], set_info['task'] 
        self.lineCellTask.setStyleSheet("background:"+COLORS.GetColor(match, get_info['task']))
        #print get_info['task'], set_info['task']
        match = (get_info['auto_enable'] == set_info['auto_enable'])
        self.lineCellAutoEnable.setStyleSheet("background:"+COLORS.GetColor(match, get_info['task']))
        match = (get_info['trigger'] == set_info['trigger'])
        self.lineCellTrigger.setStyleSheet("background:"+COLORS.GetColor(match, get_info['task']))    
                                    
        
        #battery
        if(get_info['battery'] != None):
            self.lineCellBattery.setText(str(get_info['battery']))                        
        else:
            self.lineCellBattery.setText("0")
        self.lineCellBattery.setStyleSheet("background:"+self.GetColorParBattery(get_info["battery"], colors_enabled))
                                                                                          
        
        #ir signal                
        if get_info["ir_signal"] == True:
            self.lineCellIrSinal.setText("IR SIGNAL")
        elif get_info["ir_signal"] == False:
            self.lineCellIrSinal.setText("NO IR SIGNAL")
        else:
            self.lineCellIrSinal.setText(" - - ")        
        self.lineCellIrSinal.setStyleSheet("background:"+COLORS.GetColor(get_info["ir_signal"], colors_enabled))

        #active/blocked            
        if get_info["active"] == True:
            self.lineCellActive.setText("ACTIVE")
        elif get_info["active"] == False:
            self.lineCellActive.setText("BLOCKED")
        else:
            self.lineCellActive.setText(" - - ")
        self.lineCellActive.setStyleSheet("background:"+COLORS.GetColor(get_info["active"], colors_enabled))
            
        #synchronized once
        if get_info["synchronized_once"] == True:
            self.lineCellSynchronizedOnce.setText("ONCE")
            self.lineCellSynchronizedOnce.setStyleSheet("background:"+COLORS.green)
        elif get_info["synchronized_once"] == False:
            self.lineCellSynchronizedOnce.setText("ONCE")
            self.lineCellSynchronizedOnce.setStyleSheet("background:grey"+COLORS.red)
        else:
            self.lineCellSynchronizedOnce.setText(" - - ")
            self.lineCellSynchronizedOnce.setStyleSheet("")
        self.lineCellSynchronizedOnce.setStyleSheet("background:"+COLORS.GetColor(get_info["synchronized_once"], colors_enabled))
        
        #synchronized 10min
        if get_info["synchronized"] == True:
            self.lineCellSynchronized.setText("10MIN")            
        elif get_info["synchronized"] == False:
            self.lineCellSynchronized.setText("10MIN")            
        else:
            self.lineCellSynchronized.setText(" - - ")                    
        self.lineCellSynchronized.setStyleSheet("background:"+COLORS.GetColor(get_info["synchronized"], colors_enabled))                       
        
        #diagnostic shork ok
        if(get_info['diagnostic_short_ok'] != None):                                    
            self.lineCellDiagShortOk.setText(str(get_info['diagnostic_short_ok']))
        else:
            self.lineCellDiagShortOk.setText("- -")
                                          
        #diagnostic short ko
        if(get_info['diagnostic_short_ko'] != None):                                    
            self.lineCellDiagShortKo.setText(str(get_info['diagnostic_short_ko']))
        else:
            self.lineCellDiagShortKo.setText("- -")            
        #diagnostic %
        sum_ko_ok = get_info['diagnostic_short_ko']+get_info['diagnostic_short_ok']
        if(get_info['diagnostic_short_ok'] != None) and (get_info['diagnostic_short_ko'] != None) and (sum_ko_ok != 0):                                    
            self.lineCellDiagShortRatio.setText(str((100*get_info['diagnostic_short_ok'])/sum_ko_ok))
        else:
            self.lineCellDiagShortRatio.setText("- -")
            
        #diagnostic shork ok
        if(get_info['diagnostic_long_ok'] != None):                                    
            self.lineCellDiagLongOk.setText(str(get_info['diagnostic_long_ok']))
        else:
            self.lineCellDiagLongOk.setText("- -")
                                          
        #diagnostic long ko
        if(get_info['diagnostic_long_ko'] != None):                                    
            self.lineCellDiagLongKo.setText(str(get_info['diagnostic_long_ko']))
        else:
            self.lineCellDiagLongKo.setText("- -")            
        #diagnostic %
        sum_ko_ok = get_info['diagnostic_long_ko']+get_info['diagnostic_long_ok']
        if(get_info['diagnostic_long_ok'] != None) and (get_info['diagnostic_long_ko'] != None) and (sum_ko_ok != 0):                                    
            self.lineCellDiagLongRatio.setText(str((100*get_info['diagnostic_long_ok'])/sum_ko_ok))
        else:
            self.lineCellDiagLongRatio.setText("- -")
            
            
    def GetColorParBattery(self, battery, enabled):    
        if enabled:                                 
            if battery > 25:
                color = COLORS.green
            elif battery < 25:
                color = COLORS.orange
        else:
            color = COLORS.none
        return color
    
    def GetStatus(self):
        status = STATUS.error
        
        get_info = self.GetInfo()               
        
        if get_info["task"] == None or get_info["task"] == 0:            
            status =  STATUS.none
        else:
            if get_info["battery"] >= 25 and get_info["ir_signal"]==True and get_info["synchronized_once"]==True and get_info["synchronized"]==True:
                status =  STATUS.ok
            elif get_info["battery"] < 25 and get_info["ir_signal"]==True and get_info["synchronized_once"]==True and get_info["synchronized"]==True:
                status =  STATUS.warning
            else:                
                status =  STATUS.error
                                
        return status                                            
                                                    
        
            

class TabCells(MyTab):   
    
    def __init__(self):
        '''
        Constructor
        '''        
        print "I: CREATE: tabCells"
        
    def Init(self):
        '''tab Cells'''                    
        self.cellgroups = [None] *  NUMBER_OF.CELLS
        for i in range(0, NUMBER_OF.CELLS):            
            self.cellgroups[i] = CellGroup(i+1)
            self.cellgroups[i].CreateSlots()
            
        self.CreateSlots()
        
    def CreateSlots(self):
        pass
    
    @staticmethod
    def GetActive(from_nr = 0):                    
        ret = None
        
        for i in range(0, NUMBER_OF.CELLS):            
            #get cell info from datastore                                      
            get_info = dstore.Get("cells_info", "GET")[(i+from_nr) % NUMBER_OF.CELLS]
            
            if get_info["task"]: #not None, not 0                
                ret = get_info
                break
        return ret
         
    def GetCellParTask(self, task):        
        for cellgroup in self.cellgroups:            
            if cellgroup.GetTask() == task:                
                return cellgroup
        return None                                                                           
    
        
    def GetStatus(self):
        status = STATUS.ok
        
        for i in range(0, NUMBER_OF.CELLS):
            cell_status = self.cellgroups[i].GetStatus()
            if status < cell_status:                
                status = cell_status                
        return status
    
    def Update(self, mode = UPDATE_MODE.all):
        for i in range(0, NUMBER_OF.CELLS):
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


        