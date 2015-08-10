# -*- coding: utf-8 -*-
'''
Created on 30.07.2015

@author: Meloun
'''

import time
import pandas as pd
from PyQt4 import QtCore, QtGui
from libs.myqt.DataframeTableModel import DataframeTableModel

from ewitis.data.db import db
from ewitis.gui.dfTable import DfTable
from ewitis.data.dstore import dstore
from ewitis.gui.Ui import Ui
from ewitis.gui.multiprocessingManager import mgr, eventCalcNow
from ewitis.gui.UiAccesories import uiAccesories, MSGTYPE



 
'''
Model
'''
class DfModelTimes(DataframeTableModel):
    def __init__(self, name, parent = None):
        super(DfModelTimes, self).__init__(name)
        self.df = pd.DataFrame()
        self.editable = ["nr", "cell", "status", "timeraw", "un1", "un2", "un3", "us1"]
        
    def flags(self, index):
                
        column_name =  self.df.columns[index.column()]        
        if(column_name in self.editable):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable              
        
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable        
                
        
    def sModelChanged(self, index1, index2):        
        time.sleep(0.8)
        DataframeTableModel.Update(self)
        
    def GetDataframe(self):                    
        return mgr.GetDfs()["table"]
    
       
    def setDataFromDict(self, mydict):
        print "setDataFromDict()", mydict, self.name
        
        #category changed
        if "category" in mydict:                         
            try:
                mydict["category_id"] = tableCategories.model.getCategoryParName(str(mydict["category"]))['id']            
                del mydict["category"]
            except IndexError:            
                uiAccesories.showMessage(self.name+" Update error", "No category with this name "+(mydict['category'])+"!")
                return                
        
        #update db from mydict
        db.update_from_dict(self.name, mydict)        
        eventCalcNow.set()

        
             
    
'''
Proxy Model
'''    
class DfProxymodelTimes(QtGui.QSortFilterProxyModel):
    def __init__(self):        
        QtGui.QSortFilterProxyModel.__init__(self)
        
        #This property holds whether the proxy model is dynamically sorted and filtered whenever the contents of the source model change.       
        self.setDynamicSortFilter(True)

        #This property holds the column where the key used to filter the contents of the source model is read from.
        #The default value is 0. If the value is -1, the keys will be read from all columns.                
        self.setFilterKeyColumn(-1)
        
'''
Table
'''        
class DfTableTimes(DfTable):
    def  __init__(self):        
        DfTable.__init__(self, "Times")
        self.i = 1  
        
    def InitGui(self):
        DfTable.InitGui(self)        
        self.gui['export_www'] = Ui().TimesWwwExport         
        self.gui['recalculate'] = Ui().TimesRecalculate        
        self.gui['aWwwExportDirect'] = Ui().aWwwExportDirect
        self.gui['aWwwExportLogo'] = Ui().aWwwExportLogo
        self.gui['aExportResults'] = Ui().aExportResults
        self.gui['aExportAllTimes'] = Ui().aExportAllTimes 
        self.gui['aExportLaptimes'] = Ui().aExportLaptimes 
        self.gui['times_db_export'] = Ui().TimesDbExport 
        self.gui['times_db_import'] = Ui().TimesDbImport 
        self.gui['filter_column'] = Ui().TimesFilterColumn
        self.gui['filter_starts'] = Ui().TimesFilterStarts
        self.gui['filter_finishes'] = Ui().TimesFilterFinishes        
        self.gui['auto_number'] = Ui().TimesAutoNumber
        self.gui['auto_refresh'] = Ui().TimesAutoRefresh
        self.gui['auto_number_clear'] = Ui().TimesAutoNumberClear
        self.gui['auto_refresh_clear'] = Ui().TimesAutoRefreshClear
        
    def createSlots(self):
        
        #standart slots
        DfTable.createSlots(self)        
                
        #filter starts/finishes
        QtCore.QObject.connect(self.gui['filter_starts'], QtCore.SIGNAL("clicked()"), self.sFilterStarts) 
        QtCore.QObject.connect(self.gui['filter_finishes'], QtCore.SIGNAL("clicked()"), self.sFilterFinishes)
        
        #automativally number and refresh
        QtCore.QObject.connect(self.gui['auto_number'],  QtCore.SIGNAL("valueChanged(int)"),  lambda state: uiAccesories.sGuiSetItem("times", ["auto_number"], state, self.UpdateGui))     
        QtCore.QObject.connect(self.gui['auto_refresh'], QtCore.SIGNAL("valueChanged(int)"), lambda state: (uiAccesories.sGuiSetItem("times", ["auto_refresh"], state, self.UpdateGui), setattr(self, "auto_refresh_cnt", state)))
        QtCore.QObject.connect(self.gui['auto_number_clear'],  QtCore.SIGNAL("clicked()"),  lambda: uiAccesories.sGuiSetItem("times", ["auto_number"], 0, self.UpdateGui))
        QtCore.QObject.connect(self.gui['auto_refresh_clear'], QtCore.SIGNAL("clicked()"), lambda: uiAccesories.sGuiSetItem("times", ["auto_refresh"], 0, self.UpdateGui))
        
        #export/import table (db format)
        QtCore.QObject.connect(self.gui['times_db_import'], QtCore.SIGNAL("clicked()"), lambda:myTable.sImport(self))        
        QtCore.QObject.connect(self.gui['times_db_export'], QtCore.SIGNAL("clicked()"), lambda:myTable.sExport(self, myModel.eDB, True))
        
        #button Recalculate
        QtCore.QObject.connect(self.gui['recalculate'], QtCore.SIGNAL("clicked()"), lambda:self.sRecalculate(dstore.Get("current_run")))
        
         
        #exports
        QtCore.QObject.connect(self.gui['aWwwExportDirect'], QtCore.SIGNAL("triggered()"), lambda: self.sExportDirect(self.eHTM_EXPORT))
        QtCore.QObject.connect(self.gui['aWwwExportLogo'], QtCore.SIGNAL("triggered()"), lambda: self.sExportDirect(self.eHTM_EXPORT_LOGO))                                                    
        QtCore.QObject.connect(self.gui['aExportResults'], QtCore.SIGNAL("triggered()"), lambda: self.sExportDirect(self.eCSV_EXPORT))
         
    def sRecalculate(self, run_id):
        if (uiAccesories.showMessage("Recalculate", "Are you sure you want to recalculate times and laptimes? \n (only for the current run) ", MSGTYPE.warning_dialog) != True):            
            return
        print "A: Times: Recalculating.. run id:", run_id
        query = \
                " UPDATE times" +\
                    " SET time1 = Null, lap1 = Null, time2 = Null, lap2 = Null, time3 = Null, lap3 = Null" +\
                    " WHERE (times.run_id = \""+str(run_id)+"\")"
                        
        res = db.query(query)
                
        #self.ResetStatus() 
                        
        db.commit()
        eventCalcNow.set()
        print "A: Times: Recalculating.. press F5 to finish"
        return res                
    def sFilterStarts(self):
        self.gui['filter_column'].setValue(2)
        self.gui['filter'].setText("1")        
    def sFilterFinishes(self):
        self.gui['filter_column'].setValue(2)
        self.gui['filter'].setText("250")
        
    ''' 
     end of SLOTS
    '''
        
        
        
    def AutoUpdate(self):
        ztime = time.clock()                   
        autorefresh = dstore.GetItem("times", ["auto_refresh"])
        if(autorefresh == 0):
            pass
        elif(self.auto_refresh_cnt == 0):
            self.auto_refresh_cnt = autorefresh                
        elif((self.auto_refresh_cnt-1) != 0):        
            self.auto_refresh_cnt = self.auto_refresh_cnt - 1                  
        else:
            print "auto update", self.auto_refresh_cnt,  autorefresh, "s"
            self.auto_refresh_cnt = autorefresh
            ret = self.Update()
            if(ret == True):                       
                uiAccesories.showMessage("Auto Refresh", time.strftime("%H:%M:%S", time.localtime())+" ("+str(time.clock() - ztime)[0:5]+"s)", MSGTYPE.statusbar)
            
                
                
    def UpdateGui(self): 
        if(dstore.GetItem("racesettings-app", ['rfid']) == 2):
            dstore.SetItem("times",['auto_number'], 0)
            self.gui['auto_number'].setEnabled(False)
        else:
            self.gui['auto_number'].setEnabled(True)                               

              
        times = dstore.Get("times")
            
        self.gui['auto_number'].setValue(times["auto_number"]) 
        self.gui['auto_refresh'].setValue(times["auto_refresh"])
        
        #stylesheets
#         if(times["auto_refresh"] == 0):
#             self.gui['auto_refresh'].setStyleSheet("")
#         else:
#             self.gui['auto_refresh'].setStyleSheet("background:"+COLORS.green)
#             
#             
#         if(times["auto_number"] == 0):            
#             self.gui['auto_number'].setStyleSheet("")
#         else:
#             if(tableUsers.getDbUserParNr(times["auto_number"]) != None):
#                 if(self.gui['auto_number'].styleSheet() != "background:"+COLORS.green):
#                     self.gui['auto_number'].setStyleSheet("")
#             else:
#                 if(self.gui['auto_number'].styleSheet() != "background:"+COLORS.red):
#                     self.gui['auto_number'].setStyleSheet("background:"+COLORS.red)
        return 
       
    def Update(self):                                                    
                                        
        ret = DfTable.Update(self)
        #self.UpdateGui()
               
      
        
         #ai = dstore.Get("additional_info")       
         #create list of columns to hide
#         ztime = time.clock()
#         columns = []
#         for k,v in ai.items():
#             
#             #dict            
#             if ("checked" in v):
#                 if(v['checked'] == 0):
#                     columns.append(k)
#                 continue
# 
#             #list of dict                            
#             c = 0
#             for item in v:
#                 c = c+1                
#                 if(item['checked'] == 0):                    
#                     columns.append(k+""+str(c))
#                     
#         self.hiddenCollumns =  columns                                                             
#         #self.hiddenCollumns = [k for k,v in ai.items() if v==0]
#                                      
        return ret

    
if __name__ == "__main__":    

    
    import sys
    from PyQt4 import QtGui
    from Ui_App import Ui_MainWindow
    from ewitis.gui.Ui import appWindow
    from ewitis.gui.Ui import Ui
    from ewitis.gui.UiAccesories import uiAccesories
    print "START"
    
    app = QtGui.QApplication(sys.argv)
    appWindow.Init()
    uiAccesories.Init()
    
    model = DfModelTimes()
    proxymodel = DfProxymodelTimes()
    
    dfTableTimes = DfTableTimes()
    dfTableTimes.Init()    
    dfTableTimes.Update()
        
    appWindow.show()    
    sys.exit(app.exec_())
    
    
import multiprocessing
tableTimes = DfTableTimes()         
q = multiprocessing.Queue()

        
 
    