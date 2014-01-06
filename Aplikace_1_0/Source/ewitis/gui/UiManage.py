# -*- coding: utf-8 -*-
'''
Created on 2.1.2014

@author: Meloun
'''


import sys
from PyQt4 import QtGui, QtCore

from ewitis.gui.Ui import Ui
from ewitis.gui.Ui import appWindow    
from ewitis.gui.UiAccesories import uiAccesories

#tabs
from ewitis.gui.aTab import MyTab, UPDATE_MODE
from ewitis.gui.tableAlltags import tabAlltags
from ewitis.gui.tableTags import tabTags
from ewitis.gui.tablePoints import tabPoints
from ewitis.gui.tableCGroups import tabCGroups
from ewitis.gui.tableRaceInfo import tabRaceInfo
from ewitis.gui.tableCategories import tabCategories
from ewitis.gui.tableUsers import tabUsers
from ewitis.gui.tableRuns import tabRunTimes

from ewitis.gui.tabRaceSettings import tabRaceSettings
from ewitis.gui.tabActions import tabActions
from ewitis.gui.tabDevice import tabDevice
from ewitis.gui.tabDiagnostic import tabDiagnostic

from ewitis.gui.MenusBars import bars

#'''čísla záložek v TAB widgetu'''
class TAB:
    nr_tabs = 16
    runs_times, users, categories, cgroups, tags, alltags, points, race_info, race_settings, actions,\
    device, diagnostic, cells, communication, manual, about = range(0, nr_tabs)
    NAME =  {runs_times:"RunTimes", users:"Users", categories:"Categories", cgroups:"CGroups", \
              tags:"Tags", alltags:"Alltags", points:"Points", race_info:"RaceInfo", \
              race_settings:"RaceSettings", actions:"Actions", device:"Device", diagnostic: "Diagnostic" \
            }


    
    
def Init():                            
    
    #create app window with all gui items
    appWindow.Init()

    #init gui dialogs
    uiAccesories.Init()
    
    #init tabs
    InitTabs()
    
    #update tabs
    UpdateTabs()
    
    #create slots
    CreateSlots()
    
def InitTabs():
    tabAlltags.Init()
    tabTags.Init()
    tabCGroups.Init()
    tabPoints.Init()
    tabRaceInfo.Init()
    tabCategories.Init()
    tabUsers.Init()
    tabRunTimes.Init()    
    bars.Init()    
    
def UpdateTabs():
    tabAlltags.Update()
    tabTags.Update()
    tabCGroups.Update()
    tabPoints.Update()
    tabRaceInfo.Update()
    tabCategories.Update()
    tabUsers.Update()
    tabRunTimes.Update()
    
def GetCurrentTab():
    tabIndex = Ui().tabWidget.currentIndex()
    tabName = TAB.NAME[tabIndex]
    tab = getattr(sys.modules[__name__], "tab"+tabName)
    return tab
            
def UpdateTab(mode = UPDATE_MODE.all):
    GetCurrentTab().Update(mode)        
    
def CreateSlots():
    
    #timer 500ms
    timer1 = QtCore.QTimer(); 
    timer1.start(500); #500ms
    QtCore.QObject.connect(timer1, QtCore.SIGNAL("timeout()"), sTimer)
    
    #tab changed
    QtCore.QObject.connect(Ui().tabWidget, QtCore.SIGNAL("currentChanged (int)"), sTabChanged) 
    
def sTimer():             
    #update current tab                  
    GetCurrentTab().Update(UPDATE_MODE.gui)
    
def sTabChanged(nr):
                    
    #update current tab
    #print "tab changed", nr                  
    GetCurrentTab().Update(UPDATE_MODE.all)
    
    
    #update common gui 
    #self.updateTab(None, UPDATE_MODE.gui)                                                                         


         
if __name__ == "__main__":
    
    import sys
    from PyQt4 import QtGui    

    
    app = QtGui.QApplication(sys.argv)
       
    #init all tabs
    Init()
            
    #show app        
    appWindow.show()    
    sys.exit(app.exec_())






