# -*- coding: utf-8 -*-
'''
Created on 2.1.2014

@author: Meloun
'''


import threading
import sys, time
from libs.logger.logger import Logger

#sys.stdout = Logger('log/'+time.strftime("%Y_%m_%d__%H_%M_", time.localtime())+'00_log.txt') #open('log/log.txt', 'w')

from PyQt4 import QtGui, QtCore

from ewitis.gui.Ui import appWindow    
from ewitis.gui.UiAccesories import uiAccesories
from ewitis.data.dstore import dstore
from ewitis.gui.UiAccesories import MSGTYPE
 
#tabs    
from ewitis.gui.aTab import MyTab, UPDATE_MODE
# from ewitis.gui.dfTableAlltags import tabAlltags
# from ewitis.gui.dfTableTags import tabTags
# from ewitis.gui.dfTableCGroups import tabCGroups
# from ewitis.gui.dfTableRaceInfo import tabRaceInfo
# from ewitis.gui.dfTableCategories import tabCategories
# from ewitis.gui.dfTableUsers import tabUsers
from ewitis.gui.tabRunsTimes import tabRunsTimes
from ewitis.gui.dfTableTimes import tableTimes
import ewitis.gui.dfTableTimesAutonumbers as ttAutonumbers
from ewitis.gui.dfTableUsers import tableUsers
# from ewitis.gui.dfTableTimes import tableTimes
# 
# from ewitis.gui.tabRaceSettings import tabRaceSettings
# from ewitis.gui.tabExportSettings import tabExportSettings
# from ewitis.gui.tabDevice import tabDevice
# from ewitis.gui.tabCells import tabCells
# from ewitis.gui.tabCommunication import tabCommunication
# from ewitis.gui.tabDiagnostic import tabDiagnostic
# from ewitis.gui.tabManual import tabManual
# from ewitis.gui.tabAbout import tabAbout

from ewitis.gui.MenusBars import bars
from ewitis.gui.tabManager import tabManager
from ewitis.gui.tabCells import tabCells
from ewitis.gui.multiprocessingManager import mgr, eventCalcNow, eventCalcReady

from ewitis.data.DEF_DATA import TAB

from ewitis.gui.Ui import Ui

    
timer1 = QtCore.QTimer();
timer1_1s_cnt = 0
timer_autonumbers = 0
focus_state = 0
       
def InitGui():                            
    
    #create app window with all gui items
    appWindow.Init()

    #init gui dialogs
    uiAccesories.Init()
    
    #create slots
    CreateSlots()

      
    
def CreateSlots():
    
    #timer 500ms        
    timer1.start(500); #500ms
    QtCore.QObject.connect(timer1, QtCore.SIGNAL("timeout()"), sTimer)    
    
    #refresh
    QtCore.QObject.connect(Ui().aRefresh, QtCore.SIGNAL("triggered()"), sRefresh)
    
    #focus
    QtCore.QObject.connect(Ui().aFocusTable, QtCore.SIGNAL("triggered()"), sFocusTable)
    QtCore.QObject.connect(Ui().aFocusTable2, QtCore.SIGNAL("triggered()"), sFocusTable2)    
    QtCore.QObject.connect(Ui().aFocusNumber, QtCore.SIGNAL("triggered()"), sFocusNumber)
     
    
def sFocusHandler(old, new):
    global focus_state
    print "new", new, type(new)
    if new != QtGui.QSpinBox:
        focus_state = 0
    #if old == tableTimes.gui['auto_number1']:
    #    focus_state = 0
    
#shortcut home -> focus to first auto number    
def sFocusNumber():
    #print "sFocusNumber"
    tableTimes.CloseEditor()
    ttAutonumbers.Focus()

def sFocusTable():    
    #print "sFocusTable"
    tableTimes.CloseEditor()
    tableTimes.Edit(0,1)        
        
def sFocusTable2():
    #print "sFocusTable2"                         
    tableTimes.CloseEditor(0,1)
    tableTimes.Edit(0,26)        
        
def sTimer():  
    
    global timer1_1s_cnt    
    global timer_autonumbers      
                 
    #update current tab           
    tabManager.GetCurrentTab().Update(UPDATE_MODE.gui)    
    
    #update requests
    requests = dstore.GetItem("gui", ["update_requests"])    
    if(requests["tableUsers"]):        
        tableUsers.Update()
        dstore.SetItem("gui", ["update_requests", "tableUsers"], False) 
    if(requests["tableTimes"]):
        tableTimes.Update()
        dstore.SetItem("gui", ["update_requests", "tableTimes"], False)
         
    #toolbars, statusbars
    bars.Update()
    
    #shift auto numbers
    if timer_autonumbers == 0:
        if(requests["new_times"] != []):
            ret = tableTimes.Update_AutoNumbers(requests["new_times"].pop(0))
            if ret:
                timer_autonumbers = 3
    else:
        timer_autonumbers = timer_autonumbers -1        
        
    
    if(timer1_1s_cnt == 0):
        timer1_1s_cnt = 1        
    else:
        #timer auto-updates
        tabRunsTimes.tables[0].AutoUpdate() #table times
        timer1_1s_cnt = 0
    
    return
    

                                                             
      
def sRefresh():
    title = "Manual Refresh"
    #myevent2.clear()
    
    #disable user actions
    ztime = time.clock()        
                                     
    ret = tabManager.GetCurrentTab().Update(UPDATE_MODE.all)           
    if(ret == True):
        localtime = time.strftime("%H:%M:%S", time.localtime())
        updatetime = str(time.clock() - ztime)[0:5]+"s"
        calctime = str(mgr.GetInfo()["lastcalctime"])[0:5]+"s"                              
        uiAccesories.showMessage(title, localtime + " :: update: "+updatetime +" / calc: "+ str(calctime), MSGTYPE.statusbar)            


if __name__ == "__main__":
    
    import sys, time
    from PyQt4 import QtGui
    from manage_calc import manage_calc    
    import multiprocessing  
    import pandas as pd       
    
    multiprocessing.freeze_support()

        
    #print "pandas: ", pd.__version__
    #print "multiprocessing: ", multiprocessing.__version__
    
    app = QtGui.QApplication(sys.argv)
    
    #app.focusChanged.connect(sFocusHandler) 
       
    #gui
    InitGui()
        
    #init shared-data (and sync with dstore)
    print "I: Init multiprocessing manager"
    mgr.Init( {"racesettings-app":None, "additional_info": None},  #shared-dstore
              {"table"  :  pd.DataFrame()},                        #shared-dfs
              {"wdg_calc":0, "lastcalctime"  :  " - - - "}         #shared-info
            )    
    dstore.SetSharedData(mgr.GetDstore())
    dstore.UpdateSharedData("racesettings-app")  
    print "I: Shared dstore" #, mgr.GetDstore()  
    
    #tabs
    tabManager.Init()
    tabManager.Update()

    #start calc-process (wit access to shared data)
    p = multiprocessing.Process(target=manage_calc.run, args=(mgr.GetDstore(), mgr.GetDfs(), mgr.GetInfo(), eventCalcNow, eventCalcReady))    
    p.daemon = True    
    p.start()
       
    time.sleep(1.0)
    tabRunsTimes.Update()  
            
    #show app        
    #appWindow.show()
    app.installEventFilter(appWindow)
    appWindow.showMaximized()
    app.exec_()
    
    p.terminate()    
    print "I: App was properly teminated"
    sys.exit()     

