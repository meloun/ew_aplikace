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
import ewitis.gui.GuiData as GuiData
import ewitis.gui.RunsModel as RunsModel
import ewitis.gui.TimesModel as TimesModel
import ewitis.gui.UsersModel as UsersModel
import libs.sqlite.sqlite as sqlite
  
class wrapper_gui_ewitis(QtGui.QMainWindow):
    def __init__(self, parent=None, ShaMem_comm = manage_comm.DEFAULT_COMM_SHARED_MEMORY):    
        import libs.comm.serial_utils as serial_utils 
        
        #GUI
        QtGui.QWidget.__init__(self, parent)        
        self.ui = Ui_App.Ui_MainWindow()
        self.ui.setupUi(self)                                                                                                                          

                       
        #nastaveni prvniho dostupneho portu
        try:
            self.ui.aSetPort.setText(serial_utils.enumerate_serial_ports().next())        
        except:            
            self.ui.aSetPort.setText("COM1")
        
                                                           
        #=======================================================================
        # DATABASE
        #=======================================================================
        try:           
            self.db = sqlite.sqlite_db("db/test_db.sqlite")                
            self.db.connect()
        except:
            print "E: GUI: Database"                 
        
        
        self.GuiData = GuiData.GuiData()
        
        
        #UI RESTRICT
        #=======================================================================
        self.uiRestrict()        
        
        #=======================================================================
        # TABLES
        #=======================================================================
        
        self.U = UsersModel.Users( UsersModel.UsersParameters(self))                       
        self.T = TimesModel.Times( TimesModel.TimesParameters(self))        
        self.R = RunsModel.Runs( RunsModel.RunsParameters(self))
        
        #doplneni 
        self.T.params.tabRuns = self.R        
        
        self.U.update()
        self.T.update()
        self.R.update()
        
        '''status bar'''                
        self.showMessage("mode", self.GuiData.getMesureModeString() + " ["+self.GuiData.getRaceName()+"]", dialog=False)
        
        #=======================================================================
        # SIGNALS
        #=======================================================================  
        QtCore.QObject.connect(self.ui.RunsProxyView.selectionModel(), QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), self.sRunsProxyView_SelectionChanged)
        QtCore.QObject.connect(self.ui.aSetPort, QtCore.SIGNAL("triggered()"), self.sPortSet)
        QtCore.QObject.connect(self.ui.aRefresh, QtCore.SIGNAL("triggered()"), self.sRefresh)
        QtCore.QObject.connect(self.ui.aConnectPort, QtCore.SIGNAL("triggered()"), self.sPortConnect)
        
        QtCore.QObject.connect(self.ui.aShortcuts, QtCore.SIGNAL("triggered()"), self.sShortcuts)        
        
        QtCore.QObject.connect(self.ui.actionAbout, QtCore.SIGNAL("triggered()"), self.sAbout)  
        
        #self.ui.aRefresh.a connect(QtCore.QObject, QtCore.SIGNAL("activated()"), self.sRefresh)
        
        QtCore.QObject.connect(self.ui.aRefreshMode, QtCore.SIGNAL("triggered()"), self.sRefreshMode)      
        QtCore.QObject.connect(self.ui.aLockMode, QtCore.SIGNAL("triggered()"), self.sLockMode)
        QtCore.QObject.connect(self.ui.aEditMode, QtCore.SIGNAL("triggered()"), self.sEditMode)
        QtCore.QObject.connect(self.ui.tabWidget, QtCore.SIGNAL("currentChanged (int)"), self.sTabChanged)
        #QtCore.QObject.connect(self.ui.TimesShowAll, QtCore.SIGNAL("stateChanged (int)"), self.sTimesShowAllChanged)
        #QtCore.QObject.connect(self.ui.timesShowZero, QtCore.SIGNAL("stateChanged (int)"), self.sTimesShowZeroChanged)
                                                                         
        #COMM
        self.ShaMem_comm = ShaMem_comm                       
        self.myManageComm = manage_comm.ManageComm(ShaMem_comm = self.ShaMem_comm) #COMM instance                        
        self.myManageComm.start() #start thread, 'run' flag should be 0, so this thread ends immediatelly
        
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
            self.ui.statusbar.showMessage( unicode(title+" : " + message))
        
        return True
        
         
    def start(self):
        self.app = QtGui.QApplication(sys.argv)
        self.myapp = wrapper_gui_ewitis()
        self.myapp.show()    
        sys.exit(self.app.exec_())
                
    def updateShaMem_comm(self):
        self.ShaMem_comm["port"] = str(self.ui.aSetPort.text()) 

    def uiRestrict(self):
        if(self.GuiData.measure_mode == GuiData.MODE_TRAINING_BASIC):
            #TABLE RUNS
            #add
            self.ui.RunsAdd.setEnabled(False)
            
            #TABLE TIMES                
            #add
            self.ui.TimesAdd.setEnabled(False)
            
            #TOOLBAR MODES
            self.ui.toolBar_Modes.setEnabled(False)        
            self.ui.toolBar_Modes.setVisible(False)
            
            #MENU
            self.ui.menubar.setHidden(True)                                                                                              
            self.ui.TimesWwwExport.addAction(self.ui.aDirectWwwExport)
            
        
        
        

         
    #=======================================================================
    ### SLOTS ###
    #=======================================================================
    def sTabChanged(self, nr):        
        if(nr==0):
            self.R.update()
            self.R.updateTimes()  #update TIMES table
            #self.T.update()
        elif(nr==1):
            self.U.update()
            
    def sTimesShowAllChanged(self, state):        
        if(state == 0):
            self.T.model.showall = False
            self.T.params.gui['add'].setEnabled(True)            
        elif(state == 2):            
            self.T.model.showall = True
            self.T.params.gui['add'].setEnabled(False)            
        self.T.update()
        
    def sTimesShowZeroChanged(self, state):        
        if(state == 0):
            self.T.model.showzero = False
        elif(state == 2):
            self.T.model.showzero = True
        self.T.update()
        
        
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
            self.ui.aSetPort.setText(item)
            self.showMessage(title, str(item), dialog = False)                
        
                           
    #=======================================================================
    # sPortConnect() -> create/kill communication thread 
    #=======================================================================        
    def sPortConnect(self):
        
        #refresh COMM data (gui -> shared memory; port, speed, etc..)
        self.updateShaMem_comm()
        
        title = "Port connect"
        
        if(self.ShaMem_comm["port"] == "---"):
            self.showMessage(title, "no port selected")
            return
                    
        
        #comm runs?
        if(self.ShaMem_comm["enable"] == True):                            
            
            #=======================================================================
            # KILL COMMUNICATION - thread, etc..
            #=======================================================================
            #close current thread            
            self.ShaMem_comm["enable"] = False
            #gui 
            self.ui.aSetPort.setEnabled(True)   
            self.ui.aConnectPort.setText("Connect")
            self.showMessage(title, self.ShaMem_comm["port"]+" disconnected", dialog = False)  
            
            if(self.GuiData.measure_mode == GuiData.MODE_TRAINING_BASIC):
                self.GuiData.table_mode = GuiData.MODE_EDIT       
                print "edit"                       
        else:                                    
            
            #=======================================================================
            # CREATE COMMUNICATION - thread, etc..
            #=======================================================================
            # create thread
            self.ShaMem_comm["enable"] = True
            self.myManageComm = manage_comm.ManageComm(ShaMem_comm = self.ShaMem_comm)           
            self.myManageComm.start()
            
            # wait to stable shared memory 
            time.sleep(0.1)
            #print self.ShaMem_comm
            
            #already connected?
            if(self.ShaMem_comm["enable"] == True):                        
                #gui
                self.ui.aSetPort.setEnabled(False)
                self.ui.aConnectPort.setText("Disconnect")
                self.showMessage(title, self.ShaMem_comm["port"]+" connected", dialog = False)
                
                #auto mode
                if(self.GuiData.measure_mode == GuiData.MODE_TRAINING_BASIC):
                    self.GuiData.table_mode = GuiData.MODE_REFRESH
                    print "refresh"
                     
            #flag down => cant connect
            else:
                self.showMessage(title, self.ShaMem_comm["port"]+" cant connect")                     
        
    #===========================================================================
    ### ACTION TOOLBAR ### 
    #=========================================================================== 
    def sRefresh(self):        
        
        self.R.update()
        self.T.update()
        self.U.update()
        
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
    
    