# -*- coding: utf-8 -*-
'''
Created on 30.07.2015

@author: Meloun
'''

import time, os
import pandas as pd
from PyQt4 import QtCore, QtGui
from libs.myqt.DataframeTableModel import DataframeTableModel
from libs.utils.ListOfDicts import ListOfDicts
import libs.utils.utils as utils
import libs.timeutils.timeutils as timeutils
import ewitis.gui.TimesUtils as TimesUtils
import libs.pandas.df_utils as df_utils

from ewitis.data.DEF_DATA import *
from ewitis.gui.dfTableUsers import tableUsers
from ewitis.gui.dfTableCategories import tableCategories
from ewitis.gui.dfTableCGroups import tableCGroups
import ewitis.gui.dfTableTimesExport as ttExport
from ewitis.data.db import db
from ewitis.gui.dfTable import DfTable
from ewitis.data.dstore import dstore
from ewitis.gui.Ui import Ui
from ewitis.gui.multiprocessingManager import mgr, eventCalcNow, eventCalcReady
from ewitis.gui.UiAccesories import uiAccesories, MSGTYPE
from ewitis.gui.tabExportSettings import tabExportSettings
import ewitis.exports.ewitis_html as ew_html




CONF_TABLE_TIMES = [                                                                
        {'name': 'id',       'length':0,   'default': True,   "editable": False },                                      
        {'name': 'nr',       'length':0,   'default': True,   "editable": True  },
        {'name': 'cell',     'length':0,   'default': True,   "editable": True  },
        {'name': 'status',   'length':0,   'default': True,   "editable": True  },
        {'name': 'time1',    'length':0,   'default': True,   "editable": False },
        {'name': 'lap1',     'length':0,   'default': True,   "editable": False },
        {'name': 'time2',    'length':0,   'default': True,   "editable": False },
        {'name': 'lap2',     'length':0,   'default': True,   "editable": False },
        {'name': 'time3',    'length':0,   'default': True,   "editable": False },
        {'name': 'lap3',     'length':0,   'default': True,   "editable": False },
        {'name': 'time4',    'length':0,   'default': True,   "editable": False },
        {'name': 'lap4',     'length':0,   'default': True,   "editable": False },
        {'name': 'name',     'length':0,   'default': True,   "editable": False },
        {'name': 'category', 'length':0,   'default': True,   "editable": False },
        {'name': 'order1',   'length':0,   'default': True,   "editable": False },
        {'name': 'order2',   'length':0,   'default': True,   "editable": False },
        {'name': 'order3',   'length':0,   'default': True,   "editable": False },
        {'name': 'start',    'length':0,   'default': True,   "editable": False },
        {'name': 'points1',  'length':0,   'default': True,   "editable": False },
        {'name': 'points2',  'length':0,   'default': True,   "editable": False },
        {'name': 'points3',  'length':0,   'default': True,   "editable": False },
        {'name': 'points4',  'length':0,   'default': True,   "editable": False },
        {'name': 'points5',  'length':0,   'default': True,   "editable": False },
        {'name': 'un1',      'length':0,   'default': True,   "editable": True  },
        {'name': 'un2',      'length':0,   'default': True,   "editable": True  },
        {'name': 'un3',      'length':0,   'default': True,   "editable": True  },
        {'name': 'us1',      'length':0,   'default': True,   "editable": True  },
        {'name': 'timeraw',  'length':0,   'default': True,   "editable": True  },
]


 
'''
Model
'''
class DfModelTimes(DataframeTableModel):
    def __init__(self, table):        
        super(DfModelTimes, self).__init__(table)
        self.df = pd.DataFrame()
        self.conf = ListOfDicts(CONF_TABLE_TIMES) 
        self.db_con = db.getDb()
        self.changed_rows = pd.DataFrame()
                
        
    def flags(self, index):                 
                
        column_name =  self.df.columns[index.column()]
        editable_columns = self.conf.Get("name", ("editable", True))
                
        if(column_name in editable_columns):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable              
        
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    
    def IsColumnAutoEditable(self, column):
        '''pokud true, po uživatelské editaci focus na další řádek'''
        
        #number and cell
        if(column == 1) or (column == 2):              
            return True
        
        return False
    
    def getDefaultRow(self):
        row = DataframeTableModel.getDefaultRow(self)
        row["run_id"] = dstore.Get("current_run")        
        row["cell"] = 250
        return row
                     
    def sModelChanged(self, index1, index2):                        
        DataframeTableModel.sModelChanged(self, index1, index2)
        
                                                            
    def GetDataframe(self):
        df = mgr.GetDfs()["table"]        
                
        if eventCalcReady.is_set() == False:        
            for index, row in self.changed_rows.iterrows():
                if index in df.index:
                    df.loc[index] = row             
        else:            
            self.changed_rows = pd.DataFrame()
                         
        return df
    
       
    def setDataFromDict(self, mydict):
        print "setDataFromDict()", mydict, self.name
                        
        #dict => df
        dfChange = pd.DataFrame([mydict])
        dfChange.set_index(dfChange.id, inplace=True)                   
                       
        dfChangedRow = self.df.loc[dfChange.id]  #take row before change (from global df)                                            
        old_user = tableUsers.model.getUserParNr(int(dfChangedRow['nr'])) #take user before change
               
        #update row before change with change                 
        dfChangedRow.update(dfChange)        
        
        
        #category changed        
        if "nr" in mydict:            
                                                                        
            user_id = self.checkChangedNumber(dfChangedRow.iloc[0])                                                                                            
            if user_id == None: #dialog inside checkChangedNumber()
                return
            
            #adjust dict for writing to db
            mydict["user_id"] = user_id
            del mydict["nr"]                            
                                         
        elif "cell" in mydict:                                                                      
            pass
                      
        # TIMERAW column
        elif "timeraw" in mydict:   
                              
            try:
                dbTimeraw = TimesUtils.TimesUtils.timestring2time(mydict['timeraw'])
            except TimesUtils.TimeFormat_Error:
                uiAccesories.showMessage(self.name+" Update error", "Wrong Time format!")
                return
            
            #adjust dict for writing to db
            mydict["time_raw"] = dbTimeraw
            del mydict["timeraw"]            
            

        elif "un1" in mydict:
            pass 
        elif "un2" in mydict:
            pass 
        elif "un3" in mydict:
            pass 
        elif "us1" in mydict:
            pass 
        else:
            uiAccesories.showMessage(self.name+" Update error", "Unexpecting change!")
            return                                                                                          
                                    
        # add changed row to "changed_rows"
        # keep as dataframe otherwise float issues for "nr" and "cell"
        cleared = self.ClearCalculated(dfChangedRow.iloc[0].copy())                                                                                
        self.changed_rows = self.changed_rows.append(cleared)
        try:
            self.changed_rows["nr"] = int(self.changed_rows["nr"])                           
            self.changed_rows["cell"] = int(self.changed_rows["cell"])                           
        except:
            pass        
        eventCalcReady.clear() #s                                 
                                                                                            
        #update db from mydict            
        db.update_from_dict(self.name, mydict)
        
        #user changed => reset all times for new user
        if mydict and ("user_id" in mydict):
            #print "mazu vsechny1", mydict["user_id"]
            self.ResetCalculatedValuesForUser(mydict["user_id"])        

        #reset 1 time
        elif mydict and ("id" in mydict):
            #print "mazu neco", mydict["id"]
            self.ResetCalculatedValues(mydict["id"])
        
        if old_user and ("id" in old_user):
            print "mazu vsechny2", old_user["id"]
            self.ResetCalculatedValuesForUser(old_user["id"])
                
        #self.ResetNrOfLaps()  
        eventCalcNow.set()
            
    def ClearCalculated(self, tabRow):        
        for i in range(0, NUMBER_OF.TIMESCOLUMNS):
            tabRow["time"+str(i+1)] = None
            tabRow["lap"+str(i+1)] = None
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            tabRow["order"+str(i+1)] = None
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            tabRow["points"+str(i+1)] = None
        tabRow["status"] = "wait"
            
        #precalculate name and category
        user = tableUsers.model.getUserParNr(tabRow["nr"])        
        
        if user:
            if(user['name']):
                tabRow['name'] = user['name'].upper()
                user['name'] = user['name'] +' '+user['first_name']                                        
            tabRow['category'] = user['category']            
        return tabRow
        
        
    def checkChangedNumber(self, tabRow):
        '''ZMĚNA ČÍSLA'''
        '''- kontrola uživatele, categorie, tagu                                
           - vrací user_id!!
        '''
        #print "checkChangedNumber", tabRow
                                                                                                                                                                                                                                                   
        if(tabRow["nr"] == 0):
            user_id = 0
        else:
                        
            #rigthts to change start cell?
            if(tabRow['cell'] == 1) and (dstore.Get("evaluation")['starttime'] == StarttimeEvaluation.VIA_CATEGORY):                                                              
                uiAccesories.showMessage(self.name+" Update error", "Cannot assign user to start time!")
                return None
                                        
            #user exist?            
            user = tableUsers.model.getUserParNr(int(tabRow['nr']))            
            #user_id = tableUsers.model.getIdOrTagIdParNr(tabRow['nr'])                                                           
            if user == None:
                uiAccesories.showMessage(self.name+" Update error", "Cant find user with nr. "+ str(tabRow['nr']))
                return None
            
            #category exist?                                                                                              
            category = tableCategories.model.getCategoryParName(user['category'])                        
            if category.empty:
                uiAccesories.showMessage(self.name+" Update error", "Cant find category for this user: " + user['category'])
                return None 
            
            #user id exist?                                        
            user_id = tableUsers.model.getIdOrTagIdParNr(user['nr'])                                                                                                                 
            if user_id == None:
                uiAccesories.showMessage(self.name+": Update error", "No user or tag with number "+str(tabRow['nr'])+"!")                                                                         
                return None                                                                                                                                                                                                                                             

                                                                                                                                                                                                                                    
        return user_id
    
    def ResetCalculatedValues(self, timeid):
        query = \
                " UPDATE times" +\
                    " SET time1 = Null, lap1 = Null, time2 = Null, lap2 = Null, time3 = Null, lap3 = Null, time4 = Null, lap4 = Null" +\
                    " WHERE (times.id = \""+str(timeid)+"\")"                                
        res = db.query(query) 
        db.commit()                                                              
        return res
    
    def ResetCalculatedValuesForUser(self, user_id):
        query = \
                " UPDATE times" +\
                    " SET time1 = Null, lap1 = Null, time2 = Null, lap2 = Null, time3 = Null, lap3 = Null, time4 = Null, lap4 = Null" +\
                    " WHERE (times.run_id = \""+str(dstore.Get("current_run"))+"\") AND (times.user_id = \""+str(user_id)+"\")"                                
        res = db.query(query) 
        db.commit()                                                              
        return res
    
    def ResetNrOfLaps(self):
        query = \
                " UPDATE times" +\
                    " SET lap1 = Null, lap2 = Null, lap3 = Null, lap4 = Null"                                                    
        res = db.query(query)                        
        db.commit()        
        return res
        
             
    
'''
Proxy Model
'''    
class DfProxymodelTimes(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):        
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        
        self.myclass = None 
        
        #This property holds whether the proxy model is dynamically sorted and filtered whenever the contents of the source model change.       
        self.setDynamicSortFilter(True)

        #This property holds the column where the key used to filter the contents of the source model is read from.
        #The default value is 0. If the value is -1, the keys will be read from all columns.                
        self.setFilterKeyColumn(-1)
                
    

                

'''
Table
'''        
class DfTableTimes(DfTable):
    
    (eCSV_EXPORT, eCSV_EXPORT_DNF, eHTM_EXPORT, eHTM_EXPORT_LOGO) = range(0,4)
    
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
        self.gui['aExportResultsDNF'] = Ui().aExportResultsDNF
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
        self.gui['auto_www_refresh'] = Ui().TimesAutoWWWRefresh
        self.gui['auto_www_refresh_clear'] = Ui().TimesAutoWWWRefreshClear
        
    def Init(self):
        DfTable.Init(self) 
        
    def sDeletePreCallback(self, id):        
                       
        dfRow = self.model.df.loc[id] #take row (from global df)                                                            
        user = tableUsers.model.getUserParNr(int(dfRow['nr'])) #take user        
        
        #reset values for all times of this user
        if user != None:
            self.model.ResetCalculatedValuesForUser(user["id"])
        return True               
        
    def createSlots(self):
        
        #standart slots
        DfTable.createSlots(self)        
                
        #filter starts/finishes
        QtCore.QObject.connect(self.gui['filter_starts'], QtCore.SIGNAL("clicked()"), self.sFilterStarts) 
        QtCore.QObject.connect(self.gui['filter_finishes'], QtCore.SIGNAL("clicked()"), self.sFilterFinishes)
        
        #automativally number and refresh
        QtCore.QObject.connect(self.gui['auto_number'],  QtCore.SIGNAL("valueChanged(int)"),  lambda state: uiAccesories.sGuiSetItem("times", ["auto_number"], state, self.UpdateGui))     
        QtCore.QObject.connect(self.gui['auto_refresh'], QtCore.SIGNAL("valueChanged(int)"), lambda state: (uiAccesories.sGuiSetItem("times", ["auto_refresh"], state, self.UpdateGui), setattr(self, "auto_refresh_cnt", state)))
        QtCore.QObject.connect(self.gui['auto_www_refresh'], QtCore.SIGNAL("valueChanged(int)"), lambda state: (uiAccesories.sGuiSetItem("times", ["auto_www_refresh"], state, self.UpdateGui), setattr(self, "auto_www_refresh_cnt", state)))
        QtCore.QObject.connect(self.gui['auto_number_clear'],  QtCore.SIGNAL("clicked()"),  lambda: uiAccesories.sGuiSetItem("times", ["auto_number"], 0, self.UpdateGui))
        QtCore.QObject.connect(self.gui['auto_refresh_clear'], QtCore.SIGNAL("clicked()"), lambda: uiAccesories.sGuiSetItem("times", ["auto_refresh"], 0, self.UpdateGui))
        QtCore.QObject.connect(self.gui['auto_www_refresh_clear'], QtCore.SIGNAL("clicked()"), lambda: uiAccesories.sGuiSetItem("times", ["auto_www_refresh"], 0, self.UpdateGui))
        
        #export/import table (db format)
        QtCore.QObject.connect(self.gui['times_db_import'], QtCore.SIGNAL("clicked()"), lambda:myTable.sImport(self))        
        QtCore.QObject.connect(self.gui['times_db_export'], QtCore.SIGNAL("clicked()"), lambda:myTable.sExport(self, myModel.eDB, True))
        
        #button Recalculate
        QtCore.QObject.connect(self.gui['recalculate'], QtCore.SIGNAL("clicked()"), lambda:self.sRecalculate(dstore.Get("current_run")))
        
         
        #exports
        QtCore.QObject.connect(self.gui['aWwwExportDirect'], QtCore.SIGNAL("triggered()"), lambda: self.sExportDirect(self.eHTM_EXPORT))
        QtCore.QObject.connect(self.gui['aWwwExportLogo'], QtCore.SIGNAL("triggered()"), lambda: self.sExportDirect(self.eHTM_EXPORT_LOGO))                                                    
        QtCore.QObject.connect(self.gui['aExportResults'], QtCore.SIGNAL("triggered()"), lambda: self.sExportDirect(self.eCSV_EXPORT))
        QtCore.QObject.connect(self.gui['aExportResultsDNF'], QtCore.SIGNAL("triggered()"), lambda: self.sExportDirect(self.eCSV_EXPORT_DNF))
         
    
    def sRecalculate(self, run_id):
        if (uiAccesories.showMessage("Recalculate", "Are you sure you want to recalculate times and laptimes? \n (only for the current run) ", MSGTYPE.warning_dialog) != True):            
            return
        print "A: Times: Recalculating.. run id:", run_id
        query = \
                " UPDATE times" +\
                    " SET time1 = Null, lap1 = Null, time2 = Null, lap2 = Null, time3 = Null, lap3 = Null,  time4 = Null, lap4 = Null" +\
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
     F11, F12 - final results
     - prepare DFs for export (according to filter, sort, etc.)
     - call ExportToXXXFiles with these 3 DFs
    '''  
    def sExportDirect(self, export_type = eCSV_EXPORT):             
        
        #ret = uiAccesories.showMessage("Results Export", "Choose format of results", MSGTYPE.question_dialog, "NOT finally results", "Finally results")                        
        #if ret == False: #cancel button
        #    return 
    
        #take last calculated data
        self.Update()
        
        # 3DFs for 3 exports
        exportDf = [pd.DataFrame()] * NUMBER_OF.EXPORTS
        
        exported = {}
        if len(self.model.df) != 0:
                    
            #merge table users and times
            cols_to_use = tableUsers.model.df.columns.difference(self.model.df.columns)        
            cols_to_use = list(cols_to_use) + ["nr"]        
            utDf = pd.merge(self.model.df, tableUsers.model.df[cols_to_use], how = "left", on="nr")            
            
            #call export function
            try:
                exported = ttExport.Export(utDf, export_type)
            except IOError:
                title_msg = "Table Times HTM Export"            
                uiAccesories.showMessage(title_msg, "NOT succesfully \n\nCannot write into the file.")
        
        exported_string = ""        
        for key in sorted(exported.keys()):
            exported_string += key + " : " + str(exported[key])+" times\n"
               
        if export_type == ttExport.eHTM_EXPORT or export_type == ttExport.eHTM_EXPORT_LOGO:                        
            uiAccesories.showMessage("WWW Export", time.strftime("%H:%M:%S", time.localtime())+" :: exported "+exported_string, MSGTYPE.statusbar)
        else:
            uiAccesories.showMessage("Table Times Exported", exported_string, MSGTYPE.info)
                 
        return                      

        
        
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
            #print "auto update", self.auto_refresh_cnt,  autorefresh, "s"
            self.auto_refresh_cnt = autorefresh
            ret = self.Update()
            if(ret == True):
                localtime = time.strftime("%H:%M:%S", time.localtime())
                updatetime = str(time.clock() - ztime)[0:5]+"s"
                calctime = str(mgr.GetInfo()["lastcalctime"])[0:5]+"s"                              
                uiAccesories.showMessage("Auto Refresh", localtime + " :: update: "+updatetime +" / calc: "+ str(calctime), MSGTYPE.statusbar)                        
                #uiAccesories.showMessage("Auto Refresh", time.strftime("%H:%M:%S", time.localtime())+" ("+str(time.clock() - ztime)[0:5]+"s)", MSGTYPE.statusbar)        ztime = time.clock()                   

        autorefresh = dstore.GetItem("times", ["auto_www_refresh"])
        if(autorefresh == 0):
            pass
        elif(self.auto_www_refresh_cnt == 0):
            self.auto_www_refresh_cnt = autorefresh                
        elif((self.auto_www_refresh_cnt-1) != 0):        
            self.auto_www_refresh_cnt = self.auto_www_refresh_cnt - 1                  
        else:
            #print "auto update", self.auto_refresh_cnt,  autorefresh, "s"
            self.auto_www_refresh_cnt = autorefresh
            ret = self.sExportDirect(self.eHTM_EXPORT)

                
                
    def UpdateGui(self): 
        if(dstore.GetItem("racesettings-app", ['rfid']) == 2):
            dstore.SetItem("times",['auto_number'], 0)
            self.gui['auto_number'].setEnabled(False)
        else:
            self.gui['auto_number'].setEnabled(True)                               

              
        times = dstore.Get("times")
            
        self.gui['auto_number'].setValue(times["auto_number"]) 
        self.gui['auto_refresh'].setValue(times["auto_refresh"])
        self.gui['auto_www_refresh'].setValue(times["auto_www_refresh"])
        
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
                
#         # po F5 edituje číslo u prvniho radku
#         myindex = self.proxy_model.index(0,1)
#         print myindex, type(myindex), myindex.column(), myindex.row()
#         if(myindex.isValid() == True):            
#             self.gui['view'].edit(myindex)
                 
   
        #self.UpdateGui()
               
      
        

#                                      
        return ret
    
    #edit back
    def Edit(self, myindex):        
        myindex = self.proxy_model.mapFromSource(myindex)                
        if myindex.row() > 0:             
            myindex = self.proxy_model.index(myindex.row()-1, myindex.column())
            if(myindex.isValid() == True):            
                self.gui['view'].edit(myindex)
    
    #create list of columns to hide
    def CollumnsToHide(self):
    
        ai = dstore.Get("additional_info")       
        columns = []
        for k,v in ai.items():
             
            #dict            
            if ("checked" in v):
                if(v['checked'] == 0):
                    columns.append(k)
                continue
 
            #list of dict                            
            c = 0
            for item in v:
                c = c+1                
                if(item['checked'] == 0):                    
                    columns.append(k+""+str(c))
        return columns                                                             

    
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
    
    
tableTimes = DfTableTimes()         


        
 
    