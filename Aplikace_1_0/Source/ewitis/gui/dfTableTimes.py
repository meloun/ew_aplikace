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
from ewitis.data.DEF_ENUM_STRINGS import COLORS, STATUS
import ewitis.gui.TimesUtils as TimesUtils
import libs.pandas.df_utils as df_utils



from ewitis.data.DEF_DATA import *
from ewitis.gui.dfTableUsers import tableUsers
from ewitis.gui.dfTableCategories import tableCategories
from ewitis.gui.dfTableCGroups import tableCGroups
import ewitis.gui.dfTableTimesExport as ttExport
import ewitis.gui.dfTableTimesAutonumbers as ttAutonumbers
import ewitis.gui.dfTableTimesAutocell as ttAutocell
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
        self.mynr = 0 
                
        
    def flags(self, index):                 
                
        column_name =  self.df.columns[index.column()]
        editable_columns = self.conf.Get("name", ("editable", True))
                
        if(column_name in editable_columns):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable              
        
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if (role == QtCore.Qt.BackgroundRole):
            if dstore.Get("times")["highlight_enable"]:
                try:
                    row = self.df.iloc[index.row()]
                    #no number and no user string
                    if row['nr']== 0 and row['us1'] == '':
                        return QtGui.QColor(COLORS.peachorange)
                    #changed rawtime -> yellow
                    elif row['state'][0]== 'C':
                        return QtGui.QColor(COLORS.yellow)
                    #time on request -> lila
                    elif row['state'][1] == 'R':
                        return QtGui.QColor(COLORS.lila)
                    #manual time -> green
                    elif row['state'][2]== 'M':
                        return QtGui.QColor(COLORS.light_green)
                except:
                    pass
            return
        return DataframeTableModel.data(self, index, role)
    
    def IsColumnAutoEditable(self, column):
        '''pokud true, po uživatelské editaci focus na další řádek'''
        
        #number and cell
        if(column == 1) or (column == 2):
            return True
        
        return False
    
    def getDefaultRow(self):
        row = DataframeTableModel.getDefaultRow(self)
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

        #ToDo: remove
        #mynr = len(df.index)
        #print "mynr:", mynr
        #if(mynr > self.mynr):
        #    print "TT: new record", time.clock()
        #self.mynr = mynr
                         
        return df
    
       
    def setDataFromDict(self, mydict):
        
        #mydict: {'nr': 62, 'id': 57} 
        
        #print "setDataFromDict()", mydict, self.name
              
        #take row before change (from global df)
        dfChangedRow = self.df.loc[[mydict['id']]]
        
        #take user before change                                                        
        userBeforeChange = tableUsers.model.getUserParNr(int(dfChangedRow['nr']))
               
        #update row  with change
        dfChangedRow.update(pd.DataFrame([mydict], index = [mydict['id']]))
        srsChangedRow = dfChangedRow.iloc[0].copy()
        
        #get the time_raw
        try:
            dbTimeraw = TimesUtils.TimesUtils.timestring2time(srsChangedRow['timeraw'])
        except TimesUtils.TimeFormat_Error:
            uiAccesories.showMessage(self.name+" Update error", "Wrong Time format!")
            return False
        
        
        '''MODIFY THE CHANGED mydict FOR WRITNG TO DB'''               
        #nr changed          
        if "nr" in mydict:
            
            #check changed number                                                              
            user_id = self.checkChangedNumber(srsChangedRow)                                                                                   
            if user_id == None: #dialog inside checkChangedNumber()
                return False
            
            #add 'user_id', remove 'nr'
            mydict["user_id"] = user_id
            if mydict["nr"] < 0:                       
                mydict["us1"] = "Civil #"+str(abs(mydict["nr"]))
            del mydict["nr"]                            
        
        #cell changed                                 
        elif "cell" in mydict:                                                                      
            pass
                      
        #timeraw changed
        elif "timeraw" in mydict:
            
            #adjust dict for writing to db
            mydict["time_raw"] = dbTimeraw
            del mydict["timeraw"]            

            #change the state (C -> manually Changed)            
            state = str(srsChangedRow['state'])         
            mydict["state"] = "C" + state[1:]            
            
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
            return False                                                                                         
                                    
        # add changed row to "changed_rows"        
        if not (("us1" in mydict) or ("un1" in mydict) or ("un2" in mydict) or ("un3" in mydict)):
            srsChangedRow = self.ClearCalculated(srsChangedRow)
        #print "BEFORE: ", self.changed_rows                                                                         
        self.changed_rows = self.changed_rows.append(srsChangedRow)
        #print "AFTER: ", self.changed_rows 
        
        try:
            self.changed_rows["nr"] = int(self.changed_rows["nr"])                           
            self.changed_rows["cell"] = int(self.changed_rows["cell"])                           
        except:
            pass        
        eventCalcReady.clear() #s                                 
                                                                                            
        #update db from mydict            
        db.update_from_dict(self.name, mydict)
        
        '''RESET CALCULATED VALUES'''
        #user changed => reset older times for user before and after change
        if mydict and ("user_id" in mydict):                     
            #reset older times for user after change            
            self.ResetOlderCalculatedValuesForUser(mydict["user_id"], dbTimeraw)
            #reset older times foŕ user before change
            if userBeforeChange and ("id" in userBeforeChange):
                self.ResetOlderCalculatedValuesForUser(userBeforeChange["id"], dbTimeraw)

        #us1, un1-un3 changed => no action
        elif mydict and (("us1" in mydict) or ("un1" in mydict) or ("un2" in mydict) or ("un3" in mydict)):                        
            pass
        
        #us1 changed => no action
        elif mydict and ("us1" in mydict):                        
            pass
            
        #any other change(cell, rawtime) => reset the time only
        elif mydict and ("id" in mydict):                     
            self.ResetAllCalculatedValuesForUser(userBeforeChange["id"])
                
        #self.ResetNrOfLaps()  
        eventCalcNow.set()
        return True
            
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
        #print "checkChangedNumber", tabRow, type(tabRow["nr"])
                                                                                                                                                                                                                                                   
        if(tabRow["nr"] == 0):
            user_id = 0
        else:
                        
            #rigthts to change start cell?
            if(tabRow['cell'] == 1) and (dstore.GetItem("racesettings-app" ,["evaluation", "starttime"]) == StarttimeEvaluation.VIA_CATEGORY):                                                              
                uiAccesories.showMessage(self.name+" Update error", "Cannot assign user to start time!")
                return None
                                        
            #user exist?            
            user = tableUsers.model.getUserParNr(int(tabRow['nr']))                                                          
            if user == None:
                uiAccesories.showMessage(self.name+" Update error", "User nr. "+ str(tabRow['nr'])+" not found !")                
                QtCore.QTimer.singleShot(100, lambda: self.table.Edit())
                return None
            
            #category exist?                                                                                              
            category = tableCategories.model.getCategoryParName(user['category'])                        
            if category.empty:                
                uiAccesories.showMessage(self.name+" Update error", "Category not found " + str(user['category']))
                return None 
            
            #user id exist?                                        
            user_id = tableUsers.model.getIdOrTagIdParNr(user['nr'])                                                                                                                 
            if user_id == None:
                uiAccesories.showMessage(self.name+": Update error", "No user or tag with number "+str(tabRow['nr'])+"!")                                                                         
                return None                                                                                                                                                                                                                                             

                                                                                                                                                                                                                                    
        return user_id
    
    def ResetCalculatedValuesForThisTime(self, timeid):
        query = \
                " UPDATE times" +\
                    " SET time1 = Null, lap1 = Null, time2 = Null, lap2 = Null, time3 = Null, lap3 = Null, time4 = Null, lap4 = Null" +\
                    " WHERE (times.id = \""+str(timeid)+"\")"                                
        res = db.query(query) 
        db.commit()                                                              
        return res
    
    def ResetOlderCalculatedValuesForUser(self, user_id, time_raw):
        query = \
                " UPDATE times" +\
                    " SET time1 = Null, lap1 = Null, time2 = Null, lap2 = Null, time3 = Null, lap3 = Null, time4 = Null, lap4 = Null" +\
                    " WHERE (times.user_id = \""+str(user_id)+"\") AND (times.time_raw >= " + str(time_raw) + ")"
        #print query
        res = db.query(query) 
        db.commit()
        return res
    
    def ResetAllCalculatedValuesForUser(self, user_id):
        query = \
                " UPDATE times" +\
                    " SET time1 = Null, lap1 = Null, time2 = Null, lap2 = Null, time3 = Null, lap3 = Null, time4 = Null, lap4 = Null" +\
                    " WHERE (times.user_id = \""+str(user_id)+"\")"
        #print query
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
    
    def  __init__(self):     
        self.init = False   
        DfTable.__init__(self, "Times")                
        
    def InitGui(self):
        DfTable.InitGui(self)          
                        
        self.gui['civils_to_zeroes'] = Ui().TimesCivilsToZeroes        
        self.gui['recalculate'] = Ui().TimesRecalculate        
        self.gui['aWwwExportDirect'] = Ui().aWwwExportDirect
        self.gui['aWwwExportLogo'] = Ui().aWwwExportLogo
        self.gui['aExportResults'] = Ui().aExportResults
        self.gui['aExportResultsDNF'] = Ui().aExportResultsDNF
        self.gui['aExportDbResults'] = Ui().aExportDbResults
        self.gui['aExportDbResultsDNF'] = Ui().aExportDbResultsDNF
        self.gui['aExportAllTimes'] = Ui().aExportAllTimes 
        self.gui['aExportLaptimes'] = Ui().aExportLaptimes
        try: 
            self.gui['times_db_export'] = Ui().TimesDbExport
            self.gui['times_db_import'] = Ui().TimesDbImport 
        except AttributeError:
            pass
             
        self.gui['filter_column'] = Ui().TimesFilterColumn
        self.gui['filter_starts'] = Ui().TimesFilterStarts
        self.gui['filter_finishes'] = Ui().TimesFilterFinishes
        self.gui['auto_refresh'] = Ui().TimesAutoRefresh
        ttAutonumbers.InitGui()
        ttAutocell.InitGui()
        self.gui['auto_refresh_clear'] = Ui().TimesAutoRefreshClear
        self.gui['auto_www_refresh'] = Ui().TimesAutoWWWRefresh
        self.gui['auto_www_refresh_clear'] = Ui().TimesAutoWWWRefreshClear
        self.gui['highlight_enable'] = Ui().TimesHighlightEnable
        self.gui['auto_timer_set'] = Ui().TimerSet
        self.gui['auto_timer_get'] = Ui().TimerGet
        self.gui['auto_timer_icon'] = Ui().TimerIcon
        
        self.auto_timer_cnt = 0
        self.auto_timer_green_cnt = 5
        self.timericon_grey = QtGui.QIcon("gui/icons/Circle_Grey_34212.png")
        self.timericon_green = QtGui.QIcon("gui/icons/Circle_Green_34211.png")
        self.timericon_yellow = QtGui.QIcon("gui/icons/Circle_Yellow_34215.png")
        self.timericon_orange = QtGui.QIcon("gui/icons/Circle_Orange_34213.png")
        self.timericon_red = QtGui.QIcon("gui/icons/Circle_Red_34214.png")
        
        
    def Init(self):
        
        DfTable.Init(self)
        
        #set sort rules
        self.gui['view'].sortByColumn(28, QtCore.Qt.DescendingOrder)

        self.UpdateGui()
        
        self.dfActiveNrs = pd.DataFrame()
        self.init = True 
        
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
        
        #autonumbers
        ttAutonumbers.createSlots()
        
        #autocell
        ttAutocell.createSlots()
        
        #
        QtCore.QObject.connect(self.gui['auto_refresh'], QtCore.SIGNAL("valueChanged(int)"), lambda state: (uiAccesories.sGuiSetItem("times", ["auto_refresh"], state, self.UpdateGui), setattr(self, "auto_refresh_cnt", state)))
        QtCore.QObject.connect(self.gui['auto_www_refresh'], QtCore.SIGNAL("valueChanged(int)"), lambda state: (uiAccesories.sGuiSetItem("times", ["auto_www_refresh"], state, self.UpdateGui), setattr(self, "auto_www_refresh_cnt", state)))
        QtCore.QObject.connect(self.gui['auto_refresh_clear'], QtCore.SIGNAL("clicked()"), lambda: uiAccesories.sGuiSetItem("times", ["auto_refresh"], 0, self.UpdateGui))
        QtCore.QObject.connect(self.gui['auto_www_refresh_clear'], QtCore.SIGNAL("clicked()"), lambda: uiAccesories.sGuiSetItem("times", ["auto_www_refresh"], 0, self.UpdateGui))
        QtCore.QObject.connect(self.gui['highlight_enable'], QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("times", ["highlight_enable"], state, self.UpdateGui))
        QtCore.QObject.connect(self.gui['auto_timer_set'], QtCore.SIGNAL("valueChanged(int)"), lambda state: (uiAccesories.sGuiSetItem("times", ["auto_timer"], state, self.UpdateGui), setattr(self, "auto_timer_cnt", state)))
               
        #button Recalculate
        QtCore.QObject.connect(self.gui['civils_to_zeroes'], QtCore.SIGNAL("clicked()"), lambda:self.sCivilsToZeroes())
        QtCore.QObject.connect(self.gui['recalculate'], QtCore.SIGNAL("clicked()"), lambda:self.sRecalculate())        
         
        #exports
        QtCore.QObject.connect(self.gui['aWwwExportDirect'], QtCore.SIGNAL("triggered()"), lambda: self.sExportDirect(ttExport.eHTM_EXPORT))
        QtCore.QObject.connect(self.gui['aWwwExportLogo'], QtCore.SIGNAL("triggered()"), lambda: self.sExportDirect(ttExport.eHTM_EXPORT_LOGO))                                                    
        QtCore.QObject.connect(self.gui['aExportResults'], QtCore.SIGNAL("triggered()"), lambda: self.sExportDirect(ttExport.eCSV_EXPORT))
        QtCore.QObject.connect(self.gui['aExportResultsDNF'], QtCore.SIGNAL("triggered()"), lambda: self.sExportDirect(ttExport.eCSV_EXPORT_DNS))
        QtCore.QObject.connect(self.gui['aExportDbResults'], QtCore.SIGNAL("triggered()"), lambda: self.sExportDirect(ttExport.eCSV_EXPORT_DB))
        QtCore.QObject.connect(self.gui['aExportDbResultsDNF'], QtCore.SIGNAL("triggered()"), lambda: self.sExportDirect(ttExport.eCSV_EXPORT_DNS_DB))
         
    def sSlot(self, state = False):
        print "sSlot", state
        
    def EditingFinished(self, x):
        print "self.EditingFinished", x
        
    def sCivilsToZeroes(self):
        if (uiAccesories.showMessage("Civils to zeroes", "Are you sure you want to set civils numbers to zeroes?", MSGTYPE.warning_dialog) != True):            
            return
        print "A: Times: Civils to zeroes.. "
        query = \
                " UPDATE times" +\
                    " SET user_id=0, time1 = Null, lap1 = Null, time2 = Null, lap2 = Null, time3 = Null, lap3 = Null,  time4 = Null, lap4 = Null" +\
                    " WHERE (times.user_id > 100000)"                    
        res = db.query(query)                        
                        
        db.commit()
        eventCalcNow.set()
        print "A: Times: Civils to zeroes.. press F5 to finish"
        return res
    
    def sRecalculate(self):
        if (uiAccesories.showMessage("Recalculate", "Are you sure you want to recalculate times and laptimes?", MSGTYPE.warning_dialog) != True):            
            return

        query = \
                " UPDATE times" +\
                    " SET time1 = Null, lap1 = Null, time2 = Null, lap2 = Null, time3 = Null, lap3 = Null,  time4 = Null, lap4 = Null"

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
    def sExportDirect(self, export_type = ttExport.eCSV_EXPORT):             
        
        #ret = uiAccesories.showMessage("Results Export", "Choose format of results", MSGTYPE.question_dialog, "NOT finally results", "Finally results")                        
        #if ret == False: #cancel button
        #    return 
        
        # 3DFs for 3 exports
        exportDf = [pd.DataFrame()] * NUMBER_OF.EXPORTS        
        exported = {}
        ttDf = self.model.GetDataframe() #self.model.df      
        utDf = pd.DataFrame()
        
        #merge table users and times
        if len(ttDf) != 0:                       
            cols_to_use = tableUsers.model.df.columns.difference(self.model.df.columns)        
            cols_to_use = list(cols_to_use) + ["nr"]     
            utDf = pd.merge(ttDf, tableUsers.model.df[cols_to_use], how = "left", on="nr")                    
        
        #call export function
        if (len(ttDf) != 0) or (export_type == ttExport.eHTM_EXPORT_LOGO):   
            try:            
                exported = ttExport.Export(utDf, export_type)
            except IOError:                            
                uiAccesories.showMessage("Export", time.strftime("%H:%M:%S", time.localtime())+" :: NOT succesfully, cannot write into the file.", MSGTYPE.statusbar)
                return
            
        #dialog message
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
            else:
                print "AutoUpdate: KO"

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
            ret = self.sExportDirect(ttExport.eHTM_EXPORT)
                       
        #decrement the timer
        if(self.auto_timer_cnt > 0):
            self.auto_timer_cnt = self.auto_timer_cnt - 1
            self.auto_timer_green_cnt = 5
            
        #update the get value
        self.gui['auto_timer_get'].setText(str(self.auto_timer_cnt)+" s")            
                    
        #update the icon
        autorefresh_set = dstore.GetItem("times", ["auto_timer"]) 
        if(autorefresh_set == 0):
            self.gui['auto_timer_icon'].setIcon(self.timericon_grey)
        elif(self.auto_timer_cnt == 0):
            #after 5s the green is blinking
            if self.auto_timer_green_cnt == 0:                                        
                self.gui['auto_timer_icon'].setIcon(self.timericon_grey)  
                self.auto_timer_green_cnt = 1          
            else:
                self.gui['auto_timer_icon'].setIcon(self.timericon_green)
                self.auto_timer_green_cnt = self.auto_timer_green_cnt - 1
                
        elif(self.auto_timer_cnt <= 5):            
            self.gui['auto_timer_icon'].setIcon(self.timericon_yellow)                            
        elif((self.auto_timer_cnt-1) != 0):
            self.gui['auto_timer_icon'].setIcon(self.timericon_red)                                      
        else:            
            self.auto_timer_cnt = autorefresh_set
                    

    #called periodically, timer 1,5s            
    def Update_AutoNumbers(self, new_time):  
        ret = False
        
        #auto timer
        if new_time["cell"] == 1:
            self.auto_timer_cnt = dstore.GetItem("times", ["auto_timer"])
        
        #auto numbers
        #ds_times = dstore.Get("times")
        an_mode = dstore.Get("racesettings-app")["autonumbers"] ["mode"]        
        if(an_mode == AutonumbersMode.SIMPLE) or (an_mode == AutonumbersMode.LOGIC):
            updates = ttAutonumbers.Update(self.model.GetDataframe(), new_time)
            #print "00: Update_AutoNumbers: ", updates, time.clock()                
            #self.model.Update()
            for update in updates:
                user = tableUsers.model.getUserParNr(int(update['nr']))                                                                                   
                if user != None:
                                        
                    #update user id in db
                    if user["nr"] < 0:
                        #for civils also write name to user string
                        db.update_from_dict(self.model.name, {"id":update["id"], "user_id":user["id"], "us1":user["name"]})
                    else:    
                        db.update_from_dict(self.model.name, {"id":update["id"], "user_id":user["id"]})
                    print "I: auto number: update:", update['nr'], "id:", update["id"]
                    ret = True #only one number at once
            if ret == True:
                eventCalcNow.set()                  
        return ret


    def Get_ActiveNumbers(self):
        ret_list = []
        if 'nr' in self.dfActiveNrs:
            return self.dfActiveNrs["nr"].tolist()
        return ret_list        
        
    def Update_ActiveNumbers(self):
        ttDf = self.model.GetDataframe()        
        if 'nr' in ttDf.columns:
            ttDf = ttDf.groupby("nr", as_index = False).last()
            ttDf = ttDf.sort_values(by="timeraw")
            self.dfActiveNrs = ttDf[(ttDf.cell!=250) & (ttDf.status.str.match('race'))]                        
        
                          
    def UpdateGui(self): 
        
        DfTable.UpdateGui(self)
        
        times = dstore.Get("times")
        

        self.gui['highlight_enable'].setCheckState(times["highlight_enable"])        
        
        #autonumbers        
        ttAutonumbers.UpdateGui()
        
        #autocell        
        ttAutocell.UpdateGui()
             
        self.gui['auto_refresh'].setValue(times["auto_refresh"])
        self.gui['auto_www_refresh'].setValue(times["auto_www_refresh"])
        
        #stylesheets
        if(times["auto_refresh"] == 0):
            self.gui['auto_refresh'].setStyleSheet("")
        else:
            self.gui['auto_refresh'].setStyleSheet("background:"+COLORS.green)
            
        return 
       
    def Update(self):                                                           
                                                                                        
        # stop dynamic filtering if no children
        # because of filter issue and "has stopped working" error            
        #self.proxy_model.setDynamicSortFilter(self.proxy_model.hasChildren())
        #print "U1"                    
        ret = DfTable.Update(self)
        #print "U2"      
                
        #update gui            
        self.UpdateGui()
        
        #update active numbers
        self.Update_ActiveNumbers()
                
#         # po F5 edituje číslo u prvniho radku
#         myindex = self.proxy_model.index(0,1)
#         print myindex, type(myindex), myindex.column(), myindex.row()
#         if(myindex.isValid() == True):            
#             self.gui['view'].edit(myindex)                 
                                              
        return ret
                  
    #edit previous cell
    def AutoEdit_MOVEDTO_dfTABLE(self, myindex):              
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


        
 
    