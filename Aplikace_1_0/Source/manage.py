# -*- coding: utf-8 -*-
'''
Created on 2.1.2014

@author: Meloun
'''


import threading
import sys, time
from PyQt4 import QtGui, QtCore

from ewitis.gui.Ui import Ui
from ewitis.gui.Ui import appWindow    
from ewitis.gui.UiAccesories import uiAccesories
from ewitis.data.dstore import dstore
from ewitis.gui.UiAccesories import MSGTYPE
 
#tabs
from ewitis.gui.aTab import MyTab, UPDATE_MODE
from ewitis.gui.dfTableAlltags import tabAlltags
from ewitis.gui.dfTableTags import tabTags
from ewitis.gui.dfTableCGroups import tabCGroups
from ewitis.gui.tableRaceInfo import tabRaceInfo
from ewitis.gui.dfTableCategories import tabCategories
from ewitis.gui.dfTableUsers import tabUsers
from ewitis.gui.tabRunsTimes import tabRunsTimes

from ewitis.gui.tabRaceSettings import tabRaceSettings
from ewitis.gui.tabExportSettings import tabExportSettings
from ewitis.gui.tabDevice import tabDevice
from ewitis.gui.tabCells import tabCells
from ewitis.gui.tabCommunication import tabCommunication
from ewitis.gui.tabDiagnostic import tabDiagnostic
from ewitis.gui.tabManual import tabManual
from ewitis.gui.tabAbout import tabAbout

from ewitis.gui.MenusBars import bars
from ewitis.data.DEF_DATA import TAB


    
timer1 = QtCore.QTimer();
timer1_1s_cnt = 0
       
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
    
def UpdateTabs():
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
    bars.Update()    
    
def GetCurrentTab():
    tabIndex = Ui().tabWidget.currentIndex()
    tabName = TAB.NAME[tabIndex]    
    tab = getattr(sys.modules[__name__], "tab"+tabName)
    return tab
            
def UpdateTab(mode = UPDATE_MODE.all):    
    GetCurrentTab().Update(mode)        
    
def CreateSlots():
    
    #timer 500ms
    global  timer1    
    timer1.start(500); #500ms
    QtCore.QObject.connect(timer1, QtCore.SIGNAL("timeout()"), sTimer)    
    
    #refresh
    QtCore.QObject.connect(Ui().aRefresh, QtCore.SIGNAL("triggered()"), sRefresh)
    
    #tab changed
    QtCore.QObject.connect(Ui().tabWidget, QtCore.SIGNAL("currentChanged (int)"), sTabChanged) 
    
def sTimer():  
    global timer1_1s_cnt  
             
    #update current tab           
    GetCurrentTab().Update(UPDATE_MODE.gui)
    
    #toolbars, statusbars
    bars.Update()
    
    if(timer1_1s_cnt == 0):
        timer1_1s_cnt = 1
    else:
        #timer auto-updates
        tabRunsTimes.tables[1].AutoUpdate() #table times
        timer1_1s_cnt = 0
    
    
def sTabChanged(nr):
                    
    #update current tab
    tabIndex = Ui().tabWidget.currentIndex()
    #tabName = TAB.NAME[tabIndex]
    #print "new tab", tabName, tabIndex
    
    dstore.SetItem("gui", ["active_tab"], tabIndex)
    GetCurrentTab().Update(UPDATE_MODE.gui)
                                                             
      
def sRefresh():
    title = "Manual Refresh"
    myevent2.clear()
    
    #disable user actions
    ztime = time.clock()        
    dstore.Set("user_actions", dstore.Get("user_actions")+1)
                                     
    ret = GetCurrentTab().Update(UPDATE_MODE.all)        
    if(ret == True):
        localtime = time.strftime("%H:%M:%S", time.localtime())
        updatetime = str(time.clock() - ztime)[0:5]+"s"
        calctime = str(manage_calc.LastCalcTime())[0:5]+"s"                              
        uiAccesories.showMessage(title, localtime + " :: update: "+updatetime +" / calc: "+ str(calctime), MSGTYPE.statusbar)        
    
    myevent2.set()   
    #enable user actions        
    dstore.Set("user_actions", dstore.Get("user_actions")-1)    
        
if __name__ == "__main__":
    
    import sys, time
    from PyQt4 import QtGui
    from manage_calc import manage_calc
    from ewitis.gui.events import myevent, myevent2
        

    
    app = QtGui.QApplication(sys.argv)
       
    #init all tabs
    Init()
    
    
    manage_calc.start()
    time.sleep(1.0)
    tabRunsTimes.Update()    
    #print "tv", 5, manage_calc.my_manage_calc.tv, type(manage_calc.my_manage_calc.tv)    
        
            
    #show app        
    #appWindow.show()
    appWindow.showMaximized()    
    sys.exit(app.exec_())    

