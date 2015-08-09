# -*- coding: utf-8 -*-
'''
Created on 2.1.2014

@author: Meloun
'''


import threading
import sys, time
from PyQt4 import QtGui, QtCore

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
from ewitis.gui.dfTableTimes import q, tableTimes

from ewitis.gui.tabRaceSettings import tabRaceSettings
from ewitis.gui.tabExportSettings import tabExportSettings
from ewitis.gui.tabDevice import tabDevice
from ewitis.gui.tabCells import tabCells
from ewitis.gui.tabCommunication import tabCommunication
from ewitis.gui.tabDiagnostic import tabDiagnostic
from ewitis.gui.tabManual import tabManual
from ewitis.gui.tabAbout import tabAbout

from ewitis.gui.MenusBars import bars
from ewitis.gui.tabManager import tabManager
from ewitis.gui.multiprocessingManager import mgr

from ewitis.data.DEF_DATA import TAB

from ewitis.gui.Ui import Ui

    
timer1 = QtCore.QTimer();
timer1_1s_cnt = 0
       
def InitGui():                            
    
    #create app window with all gui items
    appWindow.Init()

    #init gui dialogs
    uiAccesories.Init()
    
    #create slots
    CreateSlots()
    
   
    

      
    
def CreateSlots():
    
    #timer 500ms
    global  timer1    
    timer1.start(6000); #500ms
    QtCore.QObject.connect(timer1, QtCore.SIGNAL("timeout()"), sTimer)    
    
    #refresh
    QtCore.QObject.connect(Ui().aRefresh, QtCore.SIGNAL("triggered()"), sRefresh)
    
    #tab changed
    #QtCore.QObject.connect(Ui().tabWidget, QtCore.SIGNAL("currentChanged (int)"), sTabChanged) 
    
def sTimer():  
    
    tableTimes.model.GetDataframe()
    return
    global timer1_1s_cnt  
             
    #update current tab           
    tabManager.GetCurrentTab().Update(UPDATE_MODE.gui)
    
    #toolbars, statusbars
    bars.Update()
    
    if(timer1_1s_cnt == 0):
        timer1_1s_cnt = 1
    else:
        #timer auto-updates
        tabRunsTimes.tables[1].AutoUpdate() #table times
        timer1_1s_cnt = 0
    
    
def sTabChanged(nr):
    
    print "MAIN AAA", Ui()
                    
    #update current tab
    tabIndex = Ui().tabWidget.currentIndex()
    #tabName = TAB.NAME[tabIndex]
    #print "new tab", tabName, tabIndex
    
    dstore.SetItem("gui", ["active_tab"], tabIndex)
    tabManager.GetCurrentTab().Update(UPDATE_MODE.gui)
                                                             
      
def sRefresh():
    title = "Manual Refresh"
    myevent2.clear()
    
    #disable user actions
    ztime = time.clock()        
    dstore.Set("user_actions", dstore.Get("user_actions")+1)
                                     
    ret = tabManager.GetCurrentTab().Update(UPDATE_MODE.all)        
    if(ret == True):
        localtime = time.strftime("%H:%M:%S", time.localtime())
        updatetime = str(time.clock() - ztime)[0:5]+"s"
        calctime = ""#str(manage_calc.LastCalcTime())[0:5]+"s"                              
        uiAccesories.showMessage(title, localtime + " :: update: "+updatetime +" / calc: "+ str(calctime), MSGTYPE.statusbar)        
    
    myevent2.set()   
    #enable user actions        
    dstore.Set("user_actions", dstore.Get("user_actions")-1)    


if __name__ == "__main__":
    
    import sys, time
    from PyQt4 import QtGui
    from manage_calc_process import manage_calc_process
    from ewitis.gui.events import myevent, myevent2
    import multiprocessing  
    import pandas as pd             

    
    app = QtGui.QApplication(sys.argv)
       
    #gui
    InitGui()    
    

    
        
    print "init dstore for calc-process" 
    mgr.Init({"dstore"   :  {"current_run":None, "racesettings-app":None, "additional_info": None}, 
              "dfTable"  :  pd.DataFrame(),
              "dfExport" :  pd.DataFrame()
            })
    dstore.SetProcessDict(mgr.Get())
    dstore.UpdateProcessDict("current_run")
    
    #tabs
    tabManager.Init()
    tabManager.Update()
    
    p = multiprocessing.Process(target=manage_calc_process.run, args=(mgr.Get(),))    
    p.daemon = True    
    p.start()
       
    time.sleep(1.0)
    tabRunsTimes.Update() 
    
            
    #show app        
    #appWindow.show()
    appWindow.showMaximized()
    app.exec_()
    
    p.terminate()    
    print "I: App was properly teminated"
    sys.exit()     

