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
import ewitis.gui.AlltagsModel as AlltagsModel
import ewitis.gui.PointsModel as PointsModel
import libs.sqlite.sqlite as sqlite
from ewitis.data.DEF_DATA import *
import libs.datastore.datastore as datastore
import ewitis.gui.UiAccesories as UiAccesories
from ewitis.data.DEF_ENUM_STRINGS import *
import libs.utils.utils as utils
import libs.test.codepage as codepage  
from libs.myqt import gui
  
class wrapper_gui_ewitis(QtGui.QMainWindow):        
    def __init__(self, parent = None):
        import libs.comm.serial_utils as serial_utils                                     
        
        """ GUI """
        QtGui.QWidget.__init__(self, parent)        
        self.ui = Ui_App.Ui_MainWindow()
        self.ui.setupUi(self)                    
        
        #=======================================================================
        # DATASTORE
        #=======================================================================                
        self.datastore = datastore.Datastore(DEF_DATA)                
        

        #=======================================================================
        # FIRST CONSOLE OUTPUT
        #=======================================================================
        print "*****************************************"
        print "* Ewitis application, ", self.datastore.Get("app_version"), "rfid" if self.datastore.Get("rfid") else "ir"
        print "*****************************************" 
        codepage.codepage()
                                                           
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
        #slots, update etc.                                                                                                                     
        self.UiAccesories = UiAccesories.UiAccesories(self)                            
        self.UiAccesories.createSlots()                
        self.UiAccesories.configGui()        
        
                     
        #=======================================================================
        # TABLES
        #=======================================================================
        self.tablePoints = PointsModel.Points(PointsModel.PointsParameters(self))
        self.tableAlltags = AlltagsModel.Alltags(AlltagsModel.AlltagsParameters(self))
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
             
    def __del__(self):
        print "GUI: mazu instanci.."                                                                         
         
    def start(self):
        self.app = QtGui.QApplication(sys.argv)
        self.myapp = wrapper_gui_ewitis()
        self.myapp.show()    
        sys.exit(self.app.exec_())            
                                                                                     
class manage_gui():
    def __init__(self):
        #self.app = QtGui.QApplication(sys.argv)
        self.myapp = wrapper_gui_ewitis()
    def start(self):                    
        self.myapp.show()    
        sys.exit(self.app.exec_())            
    
if __name__ == "__main__":    
    import threading
    import sys
    
    #sys.setdefaultencoding('utf-8')
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
    
    