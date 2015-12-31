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
    ConvertToInt()
    - pro sloupce kde se vyskytuje i něco jiného než číslo jsou reprezentovány jako object
    - to_csv() čísla exportuje jako float ve formátu 2.00
    - přetypuju je na float a formátem %g nastavím že nuly se přidávají jen když je třeba
    '''
    def ConvertToInt(self, df):
          
        #nr
        df["nr"]  = df["nr"].astype(int)
        
        #format a convert na string (kvůli 3.0 => 3)
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            orderX = "order"+str(i+1)
            #try:
            if orderX in df:
                df[orderX] = df[orderX].astype(float).map('{:,g}'.format)            
            #except:
            #    print "W: not succesfully converted: ", orderX

        #lapX         
        for i in range(0, NUMBER_OF.TIMESCOLUMNS):
            lapX = "lap"+str(i+1)
            if lapX in df:
                df[lapX]  = df[lapX].astype(float).map('{:,g}'.format)
#                 
#         for i in range(0, NUMBER_OF.THREECOLUMNS):
#             if "order"+str(i+1) in df:
#                 df["order"+str(i+1)]  = df["order"+str(i+1)].astype(float)
                
        #pointsX
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            if "points"+str(i+1) in df:
                df["points"+str(i+1)]  = df["points"+str(i+1)].astype(float)
                
                #aux_df["points21"] = aux_df["points21"].astype(float)
                #aux_df["points22"] = aux_df["points22"].astype(float)
                #aux_df["points23"] = aux_df["points23"].astype(float)                
        return df
    
    '''
    '''
    def ToLapsExport(self, df):        
                
        
        # http://stackoverflow.com/questions/32051676/how-to-transpose-dataframe/32052086        
        df['colnum'] = df.groupby('nr').cumcount()+1
        
        columns_to_transpose =  [s for s in df.columns if "time" in s] + [s for s in df.columns if "points" in s]        
                
        aux_df = df[columns_to_transpose + ["nr", "colnum"]]
        aux_df = aux_df.pivot(index='nr', columns='colnum')
        aux_df.columns = ['{}{}'.format(col, num) for col,num in aux_df.columns]
        aux_df = aux_df.reset_index()
        
        cols_to_use = df.columns.difference(aux_df.columns)
        cols_to_use = list(cols_to_use) + ["nr"]  
        
        df = pd.merge(aux_df, df[cols_to_use].drop_duplicates(subset = "nr", take_last = True), on="nr", how = "left")
        
        for c in [s for s in df.columns if "points" in s]:
            if c in df:
                df[c] = df[c].astype(float)                                                
        return df
                                       
    '''
     F11, F12 - konečné výsledky
     - prepare DFs for export (according to filter, sort, etc.)
     - call ExportToXXXFiles with these 3 DFs
    '''  
    def sExportDirect(self, export_type = eCSV_EXPORT):             
        
        #take last calculated data
        self.Update()
        
        # 3DFs for 3 exports
        self.exportDf = [pd.DataFrame()] * NUMBER_OF.EXPORTS
        
        if len(self.model.df) != 0:
                    
            #merge table users and times
            cols_to_use = tableUsers.model.df.columns.difference(self.model.df.columns)        
            cols_to_use = list(cols_to_use) + ["nr"]        
            ut_df = pd.merge(self.model.df, tableUsers.model.df[cols_to_use], how = "left", on="nr")            
            
            #update export df
            for i in range(0, NUMBER_OF.EXPORTS):
                              
                aux_df = ut_df.copy()
                
                if (tabExportSettings.IsEnabled(i) == False):
                    continue
                
                #get export filtersort
                filtersort = dstore.GetItem('export_filtersort', [i])
                                          
                filter = filtersort['filter']
                sort1 = filtersort['sort1'].lower()  
                sort2 = filtersort['sort2'].lower()
                sortorder1 = True if(filtersort['sortorder1'].lower() == "asc") else False
                sortorder2 = True if(filtersort['sortorder2'].lower() == "asc") else False
                
                #filter                 
                aux_df = df_utils.FilterEmptyColumns(aux_df, filter.split(" "))
                                
                #aux_df = self.joinedDf[(aux_df[column1].notnull()) & (self.joinedDf['user_id']!=0)]                
                            
                #last time from each user?                    
                aux_df = aux_df.sort("timeraw")                        
                if("last" in filter):                                                                
                    aux_df = aux_df.groupby("nr", as_index = False).last()
                    
                #beautify
                aux_df = aux_df.where(pd.notnull(aux_df), None)
                aux_df.set_index('id',  drop=False, inplace = True)
                
                #sort again
                if(sort2 in aux_df.columns):
                    aux_df = aux_df.sort([sort1, sort2], ascending = [sortorder1, sortorder2])
                else:
                    aux_df = aux_df.sort(sort1, ascending = sortorder1)
                            
                #add "order in category" -> "3./Kategorie XY"
                for oc in range(0, NUMBER_OF.EXPORTS):
                    ordercatX = 'ordercat'+str(oc+1)
                    orderX = 'order'+str(oc+1)                
                    aux_df[ordercatX] = aux_df[orderX].astype(str)+"./"+aux_df.category                                   
                
                #filter to checked columns
                #columns = tabExportSettings.exportgroups[i].GetCheckedColumns()            
                #aux_df = aux_df[columns]
                
                #lapsexport
                if (dstore.GetItem('export_filtersort', [i, "onerow"]) != 0):
                    #print "ToLapsExport", i, dstore.GetItem('export_filtersort', [i, "onerow"])   
                    aux_df = self.ToLapsExport(aux_df)
                
                #print "PRED",i, aux_df.head(2), aux_df.dtypes
                self.ConvertToInt(aux_df)
                #print "PO",i, aux_df.head(2), aux_df.dtypes                                                
                
                #add missing users with DNF status
                if export_type == self.eCSV_EXPORT_DNF:
                    aux_df = self.AddMissingUsers(aux_df)
                
                self.exportDf[i] = aux_df #[columns]
        
        #export complete/ category and group results from export DFs        
        exported = {}
        if (export_type == self.eCSV_EXPORT) or (export_type == self.eCSV_EXPORT_DNF):
            exported = self.ExportToCsvFiles()            
        elif export_type == self.eHTM_EXPORT:
            exported = self.ExportToHtmFiles(export_type)
        elif export_type == self.eHTM_EXPORT_LOGO:
            exported = self.ExportToHtmFiles(export_type)
        else:
            uiAccesories.showMessage("Export warning", "This export is not defined!", MSGTYPE.warning)
            return
        
        
        exported_string = ""
        for key in sorted(exported.keys()):
            exported_string += key + " : " + str(exported[key])+" times\n"
               
        if export_type == self.eHTM_EXPORT or export_type == self.eHTM_EXPORT_LOGO:                        
            uiAccesories.showMessage("WWW Export", time.strftime("%H:%M:%S", time.localtime())+" :: exported "+exported_string, MSGTYPE.statusbar)
        else:
            uiAccesories.showMessage(self.name+" Exported", exported_string, MSGTYPE.info)
        
        return #self.joinedDf             
    
    """
    Add users to dataframe
    """
    def AddMissingUsers(self, tDf):        
        
        #get missing users
        df_dnf_users =  tableUsers.model.df[~tableUsers.model.df["nr"].isin(tDf["nr"])].copy()    
                            
        # add "DNF" to timeX (and also timeraw)
        for c in [s for s in tDf.columns if "time" in s]:
            df_dnf_users[c] = "DNF"
            
        # order = lastorder + 1 (for all DNF users same order)
        for c in [s for s in tDf.columns if "order" in s]:
            try:
                last_order = tDf.iloc[-1][c]  
                df_dnf_users[c] = int(last_order) + 1
            except (ValueError, IndexError):
                pass                                 
        tDf = tDf.append(df_dnf_users)
        return tDf      

    '''
    ExportToCsvFiles
    - from prepared DFs export complete, category and group export    
    - prepare header and df and call ExportToCsvFile()
    '''
    def ExportToCsvFiles(self):               
        
        #ret = uiAccesories.showMessage("Results Export", "Choose format of results", MSGTYPE.question_dialog, "NOT finally results", "Finally results")                        
        #if ret == False: #cancel button
        #    return         
        
        #return info
        exported = {}
        
        #get dirname
        racename = dstore.GetItem("racesettings-app", ['race_name'])      
        dirname = utils.get_filename("export/"+timeutils.getUnderlinedDatetime()+"_"+racename+"/")
        os.makedirs(dirname)                                                                                       
                
        for i in range(0, NUMBER_OF.EXPORTS): 
            
            if (tabExportSettings.IsEnabled(i, "csv") == False):
                continue
            
            #get df
            df =  self.exportDf[i]                        
            filtersort = dstore.GetItem('export_filtersort', [i])
            
            #get racename
            header = dstore.GetItem("export_header", [i])             
            racename =  header["racename"].replace("%race%", dstore.GetItem("racesettings-app", ['race_name']))              
                        
            #filter to checked columns            
            columns = self.GetExportCollumns(df, i)                                    
            
            #workarround
            #replace time with DNF for long times
            #df = self.DNF_workarround(df)          
                        
            #total export
            if "total" in filtersort["type"]:
                print i, "TOTAL"
                if(len(df) != 0):
                    filename = utils.get_filename("e"+str(i+1)+"_t_"+racename)                                     
                    self.ExportToCsvFile(dirname+filename+".csv", self.Columns2Cz(df[columns]), racename)                                
                    exported[filename] = len(df) 
                        
            #category export    
            elif "categories" in filtersort["type"]:
                print i, "CATEGORIES"            
                c_df = self.exportDf[i]           
                c_df = c_df.set_index("category", drop = False)
                category_groupby = c_df.groupby(c_df.index)
                for c_name, c_df in category_groupby:                
                    if(len(c_df) != 0):
                        category = tableCategories.model.getCategoryParName(c_name)
                        category = category.to_dict()
                         
                        #get secondline (!!c_name used also for filename!!)
                        c_name = header["categoryname"].replace("%category%", c_name)
                        secondline = [c_name, header["description"].replace("%description%", category["description"])]
                        
                        #write to file
                        filename = utils.get_filename("e"+str(i+1)+"_c_"+c_name)
                        self.ExportToCsvFile(dirname+filename+".csv",  self.Columns2Cz(c_df[columns]), racename, secondline)                                                                                                                                                
                        
                        exported[filename] = len(c_df) 
                     
            #group export 
            elif "groups" in filtersort["type"]: 
                print i, "GROUPS"          
                g_df = self.exportDf[i]
                for x in range(1,11):                
                    g_label = "g"+str(x)
                    categories = tableCategories.model.getCategoriesParGroupLabel(g_label)
                                                                     
                    aux_df = g_df[g_df["category"].isin(categories["name"])]                                                                           
                    if(aux_df.empty == False):                                 
                        group = tableCGroups.model.getCGrouptParLabel(g_label)
                        filename = utils.get_filename("e"+str(i+1)+"_"+g_label+"__"+group["name"])                        
                        self.ExportToCsvFile(dirname+filename+".csv", self.Columns2Cz(aux_df[columns]), racename, [group["name"], group["description"]])                                       
                        exported[filename] = len(aux_df)                                        
        return exported
    
    def GetExportCollumns(self, df, i):
        
        
        #filter to checked columns
        columns = tabExportSettings.exportgroups[i].GetCheckedColumns()
                     
        #export filter-sort settings
        filtersort = dstore.GetItem('export_filtersort', [i])
        
        #add onerow-columns to filtered columns            
        if(filtersort["onerow"] != 0):
            for x in range(0, NUMBER_OF.TIMESCOLUMNS):
                timeX = "time"+str(x+1) 
                if timeX in columns:
                    for y in range(0,50):
                        timeXY = timeX+str(y+1)
                        if timeXY in df.columns:                            
                            columns.insert(columns.index(timeX), timeXY)
                    columns.remove(timeX)            
            for x in range(0, NUMBER_OF.POINTSCOLUMNS):
                pointsX = "points"+str(x+1)                                        
                if pointsX in columns:                        
                    for y in range(0,50):
                        pointsXY = pointsX+str(y+1)
                        if pointsXY in df.columns:                           
                            columns.insert(columns.index(pointsX), pointsXY)
                    columns.remove(pointsX)
        return columns 
    
    def DNF_workarround(self, df):
        if(dstore.GetItem("racesettings-app", ['rfid']) == 0):
            if "time1" in df:
                if(dstore.GetItem("additional_info", ["time", 0, "minute_timeformat"])):
                    df.time1[df.time1>"30:00,00"] = "DNF"
                else:
                    df.time1[df.time1>"00:30:00,00"] = "DNF" 
                         
            if "time2" in df:
                if(dstore.GetItem("additional_info", ["time", 1, "minute_timeformat"])):
                    df.time2[df.time2>"30:00,00"] = "DNF"
                else:
                    df.time2[df.time2>"00:30:00,00"] = "DNF" 
                         
            if "time3" in df:
                if(dstore.GetItem("additional_info", ["time", 2, "minute_timeformat"])):
                    df.time3[df.time3>"30:00,00"] = "DNF"
                else:
                    df.time3[df.time3>"00:30:00,00"] = "DNF" 
        return df 
    
    def ExportToHtmFiles(self, type):
        #ret = uiAccesories.showMessage("Results Export", "Choose format of results", MSGTYPE.question_dialog, "NOT finally results", "Finally results")                        
        #if ret == False: #cancel button
        #    return         

        #return info
        exported = {}
                                
        #get filename, gui dialog  
        racename = dstore.GetItem("racesettings-app", ['race_name'])      
        dirname = utils.get_filename("export/www/")
                                               
                            

                
        for i in range(0, NUMBER_OF.EXPORTS): 
            
            if (tabExportSettings.IsEnabled(i, "htm") == False):
                continue
            
            #filter to checked columns
            columns = tabExportSettings.exportgroups[i].GetCheckedColumns() 
            
            df = pd.DataFrame()
            if(type == self.eHTM_EXPORT):            
                df =  self.exportDf[i]
                if(len(df) != 0):
                    df = df[columns]
                css_filename = dstore.GetItem("export_www", [i, "css_filename"])
                title = dstore.GetItem("racesettings-app", ['race_name']) 
            elif(type == self.eHTM_EXPORT_LOGO):
                df =  pd.DataFrame()                      
                css_filename = u"css/logo.css"
                title = "Časomíra Ewitis - <i>Vy závodíte, my měříme..</i>"
            else:
                uiAccesories.showMessage("Export warning", "This export is not defined!", MSGTYPE.warning)
                return
            #complete export            
            #if(len(df) != 0) or (type == self.eHTM_EXPORT_LOGO):
            filename =  utils.get_filename(dirname+"e"+str(i+1)+"_"+racename+".htm")
            self.ExportToHtmFile(filename, df, css_filename, title)            
            exported["total"] = len(df)
             
        return exported 
    
    '''
    export jednoho souboru s výsledky
    '''    
    def ExportToHtmFile(self, filename, df, css_filename = "css/results.css", title = ""):
        title_msg = "Table '"+self.name + "' HTM Export"
        try:
            #convert header EN => CZ            
            tocz_dict = dstore.GetItem("export", ["names"])                                               
            df = df.rename(columns = tocz_dict)
                                                                                                   
            html_page = ew_html.Page_table(filename, title, styles= [css_filename,], lists = df.values, keys = df.columns)                                                                            
            html_page.save()                                                                                                         
            #uiAccesories.showMessage(title_msg, "Succesfully ("+filename+") : "+ time.strftime("%H:%M:%S", time.localtime()), msgtype = MSGTYPE.statusbar)            
        except IOError:            
            uiAccesories.showMessage(title_msg, "NOT succesfully \n\nCannot write into the file ("+filename+")")
               



    """
    ExportToCsvFile
    - export dataframe to csv file
    """
    def ExportToCsvFile(self, filename, df, firstline = '', secondline = ['','']):                                                  
        try:
            df_utils.ExportToCsvFile(filename, df, firstline = '', secondline = ['',''])                                      
        except IOError:
            uiAccesories.showMessage(self.name+" Export warning", "File "+filename+"\nPermission denied!")
            
    def Columns2Cz(self, df):
        #convert header EN => CZ
        tocz_dict = dstore.GetItem("export", ["names"])                                                 
        df = df.rename(columns = tocz_dict)     
        
        #onerow columns to CZ                                        
        for x in range(0, NUMBER_OF.TIMESCOLUMNS):
            timeX = "time"+str(x+1) 
            df.columns = df.columns.str.replace(timeX, tocz_dict[timeX])          
        for x in range(0, NUMBER_OF.POINTSCOLUMNS):
            pointsX = "points"+str(x+1)                                        
            df.columns = df.columns.str.replace(pointsX, tocz_dict[pointsX])  
        return df
                       

        
        
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
                #uiAccesories.showMessage("Auto Refresh", time.strftime("%H:%M:%S", time.localtime())+" ("+str(time.clock() - ztime)[0:5]+"s)", MSGTYPE.statusbar)
            
                
                
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


        
 
    