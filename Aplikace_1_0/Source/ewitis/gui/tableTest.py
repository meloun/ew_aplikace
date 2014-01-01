# -*- coding: utf-8 -*-
#!/usr/bin/env python

from ewitis.gui.UiAccesories import uiAccesories
from ewitis.gui.tableAlltags import tableAlltags
from ewitis.gui.tableTags import tableTags
from ewitis.gui.tablePoints import tablePoints
from ewitis.gui.tableCGroups import tableCGroups
from ewitis.gui.tableRaceInfo import tableRaceInfo
from ewitis.gui.tableCategories import tableCategories
from ewitis.gui.tableUsers import tableUsers
from ewitis.gui.tableTimes import tableTimes
from ewitis.gui.tableRuns import tableRuns
  

if __name__ == "__main__":
    import sys
    from PyQt4 import QtGui    
    from ewitis.gui.Ui import appWindow
    app = QtGui.QApplication(sys.argv)
    appWindow.Init()
    uiAccesories.Init()
    
        
    tableAlltags.Init()
    tableTags.Init()
    tableCGroups.Init()
    tablePoints.Init()
    tableRaceInfo.Init()
    tableCategories.Init()
    tableUsers.Init()
    tableRuns.Init()
    tableTimes.Init()
    
    tableAlltags.Update()
    tableTags.Update()
    tableCGroups.Update()
    tablePoints.Update()
    tableRaceInfo.Update()
    tableCategories.Update()
    tableUsers.Update()
    tableRuns.Update()
    tableTimes.Update()
        
    appWindow.show()    
    sys.exit(app.exec_())
