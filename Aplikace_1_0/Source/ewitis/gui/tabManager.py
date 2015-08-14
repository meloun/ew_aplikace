'''
Created on 06.08.2015

@author: Meloun
'''


import sys, time
from ewitis.gui.Ui import Ui
from ewitis.data.DEF_DATA import TAB
from PyQt4 import QtCore
from ewitis.data.dstore import dstore
from ewitis.gui.Ui import appWindow 


#table imports
# from ewitis.gui.dfTableRuns import DfTableRuns
# from ewitis.gui.dfTableTimes import DfTableTimes
# from ewitis.gui.dfTableCategories import DfTableCategories
# from ewitis.gui.dfTableUsers import DfTableUsers
# from ewitis.gui.dfTableCGroups import DfTableCGroups
# from ewitis.gui.dfTableTags import DfTableTags
# from ewitis.gui.dfTableAlltags import DfTableAlltags
# from ewitis.gui.tableRaceInfo import RaceInfo

from ewitis.gui.dfTableRuns import tableRuns
from ewitis.gui.dfTableTimes import tableTimes
from ewitis.gui.dfTableCategories import tableCategories
from ewitis.gui.dfTableUsers import tableUsers
from ewitis.gui.dfTableCGroups import tableCGroups
from ewitis.gui.dfTableTags import tableTags
from ewitis.gui.dfTableAlltags import tableAlltags
from ewitis.gui.dfTableRaceInfo import tableRaceInfo

from ewitis.gui.MenusBars import Bars
 
#tab imports
# from ewitis.gui.aTab import MyTab, UPDATE_MODE
# from ewitis.gui.tabRunsTimes import ActionToolbar 
# from ewitis.gui.tabCells import TabCells 
# from ewitis.gui.tabDevice import TabDevice
# from ewitis.gui.tabExportSettings import TabExportSettings
# from ewitis.gui.tabCommunication import TabCommunication
# from ewitis.gui.tabRaceSettings import TabRaceSettings
# from ewitis.gui.tableRaceInfo import tabRaceInfo

from ewitis.gui.aTab import MyTab, UPDATE_MODE
from ewitis.gui.tabRunsTimes import actionToolbar
from ewitis.gui.dfTableAlltags import tabAlltags 
from ewitis.gui.dfTableTags import tabTags
from ewitis.gui.dfTableCGroups import tabCGroups
from ewitis.gui.dfTableCategories import tabCategories
from ewitis.gui.dfTableUsers import tabUsers
from ewitis.gui.dfTableRaceInfo import tabRaceInfo
from ewitis.gui.tabRunsTimes import tabRunsTimes
from ewitis.gui.tabCells import tabCells 
from ewitis.gui.tabDevice import tabDevice
from ewitis.gui.tabExportSettings import tabExportSettings
from ewitis.gui.tabCommunication import tabCommunication
from ewitis.gui.tabRaceSettings import tabRaceSettings
from ewitis.gui.tabDiagnostic import tabDiagnostic
from ewitis.gui.tabManual import tabManual
from ewitis.gui.tabAbout import tabAbout
from ewitis.gui.MenusBars import bars


# #tables
# tableRuns = DfTableRuns()
# tableTimes = DfTableTimes()
# tableUsers = DfTableUsers()
# tableCategories = DfTableCategories()
# tableCGroups = DfTableCGroups()
# tableTags = DfTableTags()
# tableAlltags = DfTableAlltags()
# tableRaceInfo = RaceInfo()
# 
# actionToolbar = ActionToolbar() 
# 
# tabAlltags = MyTab(tables = [tableAlltags,]) 
# tabTags = MyTab(tables = [tableTags,]) 
# tabCGroups = MyTab(tables = [tableCGroups,]) 
# tabRaceInfo = MyTab(tables = [tableRaceInfo,])   
# tabRaceSettings = TabRaceSettings()
# tabExportSettings = TabExportSettings()
# tabCategories = MyTab(tables = [DfTableCategories(),]) 
# tabUsers = MyTab(tables = [tableUsers,])
# tabRunsTimes = MyTab(tables = [tableRuns, tableTimes], items = [actionToolbar,])   
# tabCells = TabCells()
# tabDevice = TabDevice()        
# tabCommunication = TabCommunication()
# tabManual =  MyTab()    
# bars = Bars()
        
class TabManager():
    def __init__(self, mgr):
        self.mgr = mgr        
        

        
 

    @staticmethod    
    def GetCurrentTab():      
        tabIndex = Ui().tabWidget.currentIndex()
        tabName = TAB.NAME[tabIndex]    
        tab = getattr(sys.modules[__name__], "tab"+tabName)
        return tab     
    
    def CreateSlots(self):
                
        #tab changed
        QtCore.QObject.connect(Ui().tabWidget, QtCore.SIGNAL("currentChanged (int)"), self.sTabChanged) 
 
    def sTabChanged(self, nr):
                    
        #update current tab        
        dstore.SetItem("gui", ["active_tab"], nr)
        self.GetCurrentTab().Update(UPDATE_MODE.gui)

    
    def Init(self):
        tabAlltags.Init()
        tabTags.Init()
        tabCGroups.Init()
        tabRaceInfo.Init()
        tabRaceSettings.Init()
        tabExportSettings.Init()
        tabCategories.Init()
        tabUsers.Init()
        tabRunsTimes.Init()  
        tabCells.Init()
        tabDevice.Init()        
        tabCommunication.Init()
        tabManual.Init()    
        bars.Init() 
        
        self.CreateSlots() 
        
    @staticmethod
    def UpdateTab(self, mode = UPDATE_MODE.all):    
        GetCurrentTab().Update(mode)   
    
    def Update(self, ):
        
        #update all tabs
        tabAlltags.Update()
        tabTags.Update()
        tabCGroups.Update()
        tabRaceInfo.Update()
        tabRaceSettings.Update()
        tabExportSettings.Update()
        tabCategories.Update()
        tabUsers.Update()
        tabRunsTimes.Update()  
        tabCells.Update()
        tabDevice.Update()        
        tabCommunication.Update()
        tabManual.Update() 
        tabAbout.Update()  
        
        #update bars
        bars.Update()          
       




tabManager = TabManager(2)
        
if __name__ == "__main__":
    print "start"
    import multiprocessing, sys
    mgr = 4 #multiprocessing.Manager()  
    tabs = TabManager(mgr)
    sys.stdout.flush()
    print "konec"
