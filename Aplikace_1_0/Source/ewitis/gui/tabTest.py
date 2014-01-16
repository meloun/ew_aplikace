# -*- coding: utf-8 -*-
#!/usr/bin/env python

from ewitis.gui.UiAccesories import uiAccesories
from ewitis.gui.tableAlltags import tabAlltags
from ewitis.gui.tableTags import tabTags
from ewitis.gui.tablePoints import tabPoints
from ewitis.gui.tableCGroups import tabCGroups
from ewitis.gui.tableRaceInfo import tabRaceInfo
from ewitis.gui.tableCategories import tabCategories
from ewitis.gui.tableUsers import tabUsers
from ewitis.gui.tabRunsTimes import tabRunsTimes

  

if __name__ == "__main__":
    import sys
    from PyQt4 import QtGui    
    from ewitis.gui.Ui import appWindow
    app = QtGui.QApplication(sys.argv)
    appWindow.Init()
    uiAccesories.Init()
    
        
    tabAlltags.Init()
    tabTags.Init()
    tabCGroups.Init()
    tabPoints.Init()
    tabRaceInfo.Init()
    tabCategories.Init()
    tabUsers.Init()
    tabRunsTimes.Init()    
    
    tabAlltags.Update()
    tabTags.Update()
    tabCGroups.Update()
    tabPoints.Update()
    tabRaceInfo.Update()
    tabCategories.Update()
    tabUsers.Update()
    tabRunsTimes.Update()    
        
    appWindow.show()    
    sys.exit(app.exec_())
