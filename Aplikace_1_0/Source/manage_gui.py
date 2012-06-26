# -*- coding: utf-8 -*-

#
#
#

import sys
import time
import manage_comm
import PyQt4
from PyQt4 import QtCore
from PyQt4 import QtGui
import ewitis.gui.Ui_App as Ui_App
import ewitis.gui.myModel as myModel
import ewitis.gui.RunsModel as RunsModel
import ewitis.gui.TimesModel as TimesModel
import ewitis.gui.UsersModel as UsersModel
import ewitis.gui.CategoriesModel as CategoriesModel
import ewitis.gui.CGroupsModel as CGroupsModel
import ewitis.gui.TagsModel as TagsModel
import libs.sqlite.sqlite as sqlite
import ewitis.data.DEF_DATA as DEF_DATA
import libs.datastore.datastore as datastore
import ewitis.gui.UiAccesories as UiAccesories
from ewitis.data.DEF_ENUM_STRINGS import *
import libs.utils.utils as utils 
from libs.myqt import gui
  
class wrapper_gui_ewitis(QtGui.QMainWindow):
    #def __init__(self, parent=None, ShaMem_comm = manage_comm.DEFAULT_COMM_SHARED_MEMORY):    
    def __init__(self, parent=None):
        import libs.comm.serial_utils as serial_utils                                         
        
        """ GUI """
        QtGui.QWidget.__init__(self, parent)        
        self.ui = Ui_App.Ui_MainWindow()
        self.ui.setupUi(self)            
        
        #=======================================================================
        # DATASTORE
        #=======================================================================                
        self.datastore = datastore.Datastore(DEF_DATA.DEF_DATA)
        
        #slots, update etc.                                                                                                                     
        self.UiAccesories = UiAccesories.UiAccesories(self)                    
        
                                                           
        #=======================================================================
        # DATABASE
        #=======================================================================
        try:           
            self.db = sqlite.sqlite_db("db/test_db.sqlite")                
            self.db.connect()
        except:
            print "E: GUI: Database"
        
        #=======================================================================
        # GUI
        #=======================================================================
        self.myQFileDialog = gui.myDialog(self.datastore)                 
        
        
        #self.GuiData = GuiData.GuiData()
        
        
        #UI RESTRICT
        #=======================================================================
        self.uiRestrict()
        
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(10);        
        
        #=======================================================================
        # TABLES
        #=======================================================================
        
        self.tableTags = TagsModel.Tags(TagsModel.TagsParameters(self))
        self.C = CategoriesModel.Categories(CategoriesModel.CategoriesParameters(self))
        self.CG = CGroupsModel.CGroups(CGroupsModel.CGroupsParameters(self))
        self.U = UsersModel.Users( UsersModel.UsersParameters(self))                               
        self.T = TimesModel.Times( TimesModel.TimesParameters(self))
        self.R = RunsModel.Runs( RunsModel.RunsParameters(self))
        
        
        
        
        #doplneni 
        self.T.params.tabRuns = self.R        
        
        '''Update'''
        self.R.update()
        #self.updateTables()                        
        
        #nastaveni prvniho dostupneho portu
        try:
            self.datastore.Set("port_name", "GET_SET", serial_utils.enumerate_serial_ports().next())        
        except:            
            self.datastore.Set("port_name", "GET_SET", "---")
        #print self.datastore.data
        
        self.UiAccesories.updateGui()                                        
        
        '''status bar'''                       
        logic_mode = LOGIC_MODES.STRINGS[self.datastore.Get("timing_settings", "GET")['logic_mode']]
                   
        self.showMessage("mode", logic_mode + " ["+self.datastore.Get("race_name")+"]", dialog=False)

        
        #=======================================================================
        # SIGNALS
        #=======================================================================
        
        QtCore.QObject.connect(self.timer1s, QtCore.SIGNAL("timeout()"), self.sTimer)
         
        QtCore.QObject.connect(self.ui.RunsProxyView.selectionModel(), QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), self.sRunsProxyView_SelectionChanged)
        QtCore.QObject.connect(self.ui.aSetPort, QtCore.SIGNAL("triggered()"), self.sPortSet)
        QtCore.QObject.connect(self.ui.aRefresh, QtCore.SIGNAL("triggered()"), self.sRefresh)
        QtCore.QObject.connect(self.ui.aConnectPort, QtCore.SIGNAL("triggered()"), self.sPortConnect)
        
        QtCore.QObject.connect(self.ui.aShortcuts, QtCore.SIGNAL("triggered()"), self.sShortcuts)        
        
        QtCore.QObject.connect(self.ui.actionAbout, QtCore.SIGNAL("triggered()"), self.sAbout)
        
        QtCore.QObject.connect(self.ui.aRefresh, QtCore.SIGNAL("activated()"), self.sRefresh)   
        
        #self.ui.aRefresh.connect(QtCore.QObject, QtCore.SIGNAL("activated()"), self.sRefresh)
        
        QtCore.QObject.connect(self.ui.aRefreshMode, QtCore.SIGNAL("triggered()"), self.sRefreshMode)      
        QtCore.QObject.connect(self.ui.aLockMode, QtCore.SIGNAL("triggered()"), self.sLockMode)
        QtCore.QObject.connect(self.ui.aEditMode, QtCore.SIGNAL("triggered()"), self.sEditMode)
        QtCore.QObject.connect(self.ui.tabWidget, QtCore.SIGNAL("currentChanged (int)"), self.sTabChanged)
        #QtCore.QObject.connect(self.ui.TimesShowAll, QtCore.SIGNAL("stateChanged (int)"), self.sTimesShowAllChanged)
        #QtCore.QObject.connect(self.ui.timesShowZero, QtCore.SIGNAL("stateChanged (int)"), self.sTimesShowZeroChanged)              
                        
        self.UiAccesories.createSlots()
        
        
        #=======================================================================
        # COMM
        #=======================================================================                                           
        #self.myManageComm = manage_comm.ManageComm(self.datastore) #COMM instance
        #self.myManageComm.start() #start thread, 'run' flag should be 0, so this thread ends immediatelly
        
        #print self.ui.aRefresh.
             
    def __del__(self):
        print "GUI: mazu instanci.."                                                              

    
    #=======================================================================
    # SHOW MESSAGE -     
    #=======================================================================
    # dialog, status bar
    # warning(OK), info(OK), warning_dialog(Yes, Cancel), input_integer(integer, OK)      
    def showMessage(self, title, message, msgtype='warning', dialog=True, statusbar=True, value=0):        
        
        #DIALOG
        if(dialog):                                
            if(msgtype=='warning'):
                QtGui.QMessageBox.warning(self, title, message)            
            elif(msgtype=='info'):
                QtGui.QMessageBox.information(self, title, message)
            elif(msgtype=='warning_dialog'):
                ret = QtGui.QMessageBox.warning(self, title, message, QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Yes)                
                if (ret != QtGui.QMessageBox.Yes):
                    return False
                message = "succesfully"
            elif(msgtype=='input_integer'):
                i, ok = QtGui.QInputDialog.getInteger(self, title, message, value=value)
                if ok:
                    return i
                return None
            
        #STATUSBAR        
        if(statusbar):
            print title, message            
            self.ui.statusbar.showMessage( (title+" : " + message))
        
        return True
        
         
    def start(self):
        self.app = QtGui.QApplication(sys.argv)
        self.myapp = wrapper_gui_ewitis()
        self.myapp.show()    
        sys.exit(self.app.exec_())
                
        
        
    
    def updateTables(self, nr):        
        if(nr==0):
            self.R.update()
            #self.R.updateTimes()  #update TIMES table
            self.T.update()
        elif(nr==1):            
            self.U.update()
        elif(nr==2):            
            self.C.update()
        elif(nr==3):            
            self.CG.update()                     
        elif(nr==4):            
            self.tableTags.update()

    def uiRestrict(self):
        pass
        #toDo: rozlisit podle modu z datastore
#        if(self.GuiData.measure_mode == GuiData.MODE_TRAINING_BASIC):
#            #TABLE RUNS
#            #add
#            self.ui.RunsAdd.setEnabled(False)
#            
#            #TABLE TIMES                
#            #add
#            self.ui.TimesAdd.setEnabled(False)
#            
#            #TOOLBAR MODES
#            self.ui.toolBar_Modes.setEnabled(False)        
#            self.ui.toolBar_Modes.setVisible(False)
#            
#            #MENU
#            self.ui.menubar.setHidden(True)                                                                                              
#            self.ui.TimesWwwExport.addAction(self.ui.aDirectWwwExport)            
         
    #=======================================================================
    ### SLOTS ###
    #=======================================================================  
    # 23 06 04 00 00 0000 00      
    def sTimer(self):
        self.UiAccesories.updateTab(self.ui.tabWidget.currentIndex ())        
        
    def sTabChanged(self, nr):
                
        self.datastore.Set("active_tab", nr)
        
        self.updateTables(nr)        
                

            
        
    def sRunsProxyView_SelectionChanged(self, selected, deselected):               
        if(selected):            
            self.R.updateTimes()  #update TIMES table                                                                               
                      
        
    #===========================================================================
    ### PORT TOOLBAR ### 
    #=========================================================================== 
    def sPortSet(self):
        import libs.comm.serial_utils as serial_utils         
        
        #dostupne porty

        ports = []
        
        title = "Port Set"
        
        try:
            for p in serial_utils.enumerate_serial_ports():            
                ports.append(p)
        except:
            self.showMessage(title, "No serial port available.")
            return   
    
        if (ports==[]):
            self.showMessage(title, "No serial port available.")
            return    
            
            
        ports = sorted(ports)                    

        item, ok = QtGui.QInputDialog.getItem(self, "Serial Port",
                "Serial Port:", ports, 0, False)
        
        
        if (ok and item):                                  
            self.datastore.Set("port_name", str(item))
            self.showMessage(title, str(item), dialog = False)
             
        self.UiAccesories.updateGui()               
        
                           
    #=======================================================================
    # sPortConnect() -> create/kill communication thread 
    #=======================================================================        
    def sPortConnect(self):

        title = "Port connect"
                                            
        #comm runs?        
        if(self.datastore.Get("port_enable") == True):                           
            
            # KILL COMMUNICATION - thread, etc..
            self.datastore.Set("port_enable", False)                    
            self.showMessage(title, self.datastore.Get("port_name")+" disconnected", dialog = False)                       
        else:            
            self.showMessage(title, self.datastore.Get("port_name")+" connected", dialog = False)                                 
                        
            # CREATE COMMUNICATION - thread, etc..                                    
                                 
            self.myManageComm = manage_comm.ManageComm(self.datastore)
            self.myManageComm.start()
            
            # wait to stable shared memory 
            time.sleep(0.2)            
            
            #already connected?                                
            #flag down => cant connect
            if(self.datastore.Get("port_enable") == False):             
                title = "Port connect"                                
                self.showMessage(title, self.datastore.Get("port_name")+" cant connect")                
                                
        self.UiAccesories.updateGui()                     
        
    #===========================================================================
    ### ACTION TOOLBAR ### 
    #=========================================================================== 
    def sRefresh(self):        
        
        nr_tab = self.datastore.Get("active_tab")
        self.updateTables(nr_tab)               
        
        title = "Manual Refresh"
        self.showMessage(title, time.strftime("%H:%M:%S", time.localtime()), dialog = False)   
        
    #===========================================================================
    #### MODE TOOLBAR => EDIT, LOCK, REFRESH ### 
    #===========================================================================         
    def sEditMode(self):
        
        self.ui.aEditMode.setChecked(True) 
        self.ui.aLockMode.setChecked(False) 
        self.ui.aRefreshMode.setChecked(False)
        
        self.GuiData.table_mode = GuiData.MODE_EDIT
          
        self.T.model.table_mode = myModel.MODE_EDIT           
        self.R.model.table_mode = myModel.MODE_EDIT
        self.U.model.table_mode = myModel.MODE_EDIT
        
        self.showMessage("Mode", "EDIT", dialog = False)
          
    def sRefreshMode(self):
        
        self.ui.aRefreshMode.setChecked(True)
        self.ui.aLockMode.setChecked(False) 
        self.ui.aEditMode.setChecked(False)  
        
        self.GuiData.table_mode = GuiData.MODE_REFRESH     
                  
        self.R.model.table_mode = myModel.MODE_REFRESH
        self.T.model.table_mode = myModel.MODE_REFRESH
        self.U.model.table_mode = myModel.MODE_REFRESH  
        
        self.showMessage("Mode", "REFRESH", dialog = False)      
        
    def sLockMode(self):
        
        self.ui.aLockMode.setChecked(True)
        self.ui.aRefreshMode.setChecked(False) 
        self.ui.aEditMode.setChecked(False)
          
        self.GuiData.table_mode = GuiData.MODE_LOCK     
                
        self.R.model.table_mode = myModel.MODE_LOCK
        self.T.model.table_mode = myModel.MODE_LOCK
        self.U.model.table_mode = myModel.MODE_LOCK
        
        self.showMessage("Mode", "LOCK", dialog = False)                                                                                                                                                                                 
    def sShortcuts(self):                           
        QtGui.QMessageBox.information(self, "Shortcuts", "F5 - manual refresh\nF12 - direct www export")
    def sAbout(self):                           
        QtGui.QMessageBox.information(self, "About", "Ewitis  - Electronic wireless timing \n\ninfo@ewitis.cz\nwww.ewitis.cz\n\n v0.2\n\n (c) 2011")                                                

class manage_gui():
    def __init__(self):
        #self.app = QtGui.QApplication(sys.argv)
        self.myapp = wrapper_gui_ewitis()
    def start(self):                    
        self.myapp.show()    
        sys.exit(self.app.exec_())            
    
if __name__ == "__main__":    
    import threading
    #myManageGui = manage_gui()
    #myManageGui.start()
    
    def gui_start():        
        app = QtGui.QApplication(sys.argv)        
        myapp = wrapper_gui_ewitis()           
        myapp.show()
        sys.exit(app.exec_())
    
    gui_start()
        
    print "MANAGE GUI"
    #thread_gui = threading.Thread(target = gui_start)
    #thread_gui.start()
    
    