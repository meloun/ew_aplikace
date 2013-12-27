# -*- coding: utf-8 -*-

#
#
#


from PyQt4 import QtGui
from ewitis.data.dstore import dstore
from ewitis.gui.Ui import appWindow
import libs.test.codepage as codepage  
from ewitis.gui.UiAccesories2 import uiAccesories
from ewitis.gui.tabRaceSettings import tabRaceSettings
from ewitis.gui.tabActions import tabActions
from ewitis.gui.tabDevice import tabDevice
from ewitis.gui.tabCells import tabCells
from ewitis.gui.tabCommunication import tabCommunication
from ewitis.gui.tabDiagnostic import tabDiagnostic
from ewitis.gui.tabManual import tabManual
from ewitis.gui.tabAbout import tabAbout

import ewitis.gui.PointsModel as PointsModel
import ewitis.gui.AlltagsModel as AlltagsModel
import ewitis.gui.TagsModel as TagsModel
import ewitis.gui.CategoriesModel as CategoriesModel
import ewitis.gui.CGroupsModel as CGroupsModel
  
  
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
    tablePoints = PointsModel.Points(PointsModel.PointsParameters())
    tableAlltags = AlltagsModel.Alltags(AlltagsModel.AlltagsParameters())
    tableTags = TagsModel.Tags(TagsModel.TagsParameters())
    tableCategories = CategoriesModel.Categories(CategoriesModel.CategoriesParameters())
    tableCategoryGroups = CGroupsModel.CGroups(CGroupsModel.CGroupsParameters())
    

    
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

    
    