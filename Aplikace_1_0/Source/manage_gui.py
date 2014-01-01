# -*- coding: utf-8 -*-

#
#
#


from PyQt4 import QtGui
from ewitis.data.dstore import dstore
from ewitis.gui.Ui import appWindow
import libs.test.codepage as codepage  
from ewitis.gui.UiAccesories import uiAccesories
from ewitis.gui.tabRaceSettings import tabRaceSettings
from ewitis.gui.tabActions import tabActions
from ewitis.gui.tabDevice import tabDevice
from ewitis.gui.tabCells import tabCells
from ewitis.gui.tabCommunication import tabCommunication
from ewitis.gui.tabDiagnostic import tabDiagnostic
from ewitis.gui.tabManual import tabManual
from ewitis.gui.tabAbout import tabAbout

import ewitis.gui.tabPoints as tabPoints
import ewitis.gui.tabAlltags as tabAlltags
import ewitis.gui.tabTags as tabTags
import ewitis.gui.tabCategories as tabCategories
import ewitis.gui.tabCGroups as tabCGroups
import ewitis.gui.tabUsers as tabUsers
  
  
class Init():        
    def __init__(self):
                                            
        #=======================================================================
        # FIRST CONSOLE OUTPUT
        #=======================================================================
        print "*****************************************"
        print "* Ewitis application, ", dstore.Get("versions")["app"], "rfid" if dstore.Get("rfid") else "ir"
        print "*****************************************" 
        codepage.codepage()
                                                                                                                                                                                                                                                       
  
if __name__ == "__main__":    
    import sys
    
    #create app
    app = QtGui.QApplication(sys.argv)
    
    #window with widgets
    appWindow.Init()
    
    #gui datastore methods (with dialogs)
    uiAccesories.Init()
    
    #gui datastore methods (with dialogs)
    
    #tabs: init
    tabCells.init()
    
    #tables
    tablePoints = tabPoints.Points(tabPoints.PointsParameters())
    tableAlltags = tabAlltags.Alltags(tabAlltags.AlltagsParameters())
    tableTags = tabTags.Tags(tabTags.TagsParameters())
    tableCategories = tabCategories.Categories(tabCategories.CategoriesParameters())
    tableCategoryGroups = tabCGroups.CGroups(tabCGroups.CGroupsParameters())
    #tableUsers = tabUsers.Users(tabUsers.UsersParameters())
    

    
    #tabs: add slots
    tabRaceSettings.addSlots()
    tabActions.addSlots()
    tabDevice.addSlots()
    tabCells.addSlots()
    tabCommunication.addSlots()
    tabManual.addSlots()
    tabAbout.addSlots()
    tabDiagnostic.addSlots()
    
    #tabs: update test
    tabRaceSettings.update()
    tabDevice.update()
    tabCommunication.update()
    tabActions.update()
    
    #tables update test
    tablePoints.update()
    tableAlltags.update()
    tableTags.update()
    tableCategories.update()
    tableCategoryGroups.update()
    

       
    Init()
    
    #show window
    appWindow.show()
    
    #end of app    
    sys.exit(app.exec_())
    
    #should never happend        
    print "FATAL ERROR: end of gui"    
    
    
#     import sys
#     from ewitis.gui.Ui_App import Ui_MainWindow
#     app = QtGui.QApplication(sys.argv)
#     MainWindow = QtGui.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     Gui()
#     MainWindow.show()
#     sys.exit(app.exec_())        

    
    