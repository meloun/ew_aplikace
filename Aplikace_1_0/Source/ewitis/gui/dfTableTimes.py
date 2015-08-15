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

from ewitis.data.DEF_DATA import *
from ewitis.gui.dfTableUsers import tableUsers
from ewitis.gui.dfTableCategories import tableCategories
from ewitis.data.db import db
from ewitis.gui.dfTable import DfTable
from ewitis.data.dstore import dstore
from ewitis.gui.Ui import Ui
from ewitis.gui.multiprocessingManager import mgr, eventCalcNow, eventCalcReady
from ewitis.gui.UiAccesories import uiAccesories, MSGTYPE
from ewitis.gui.tabExportSettings import tabExportSettings



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
        {'name': 'timeraw',  'length':0,   'default': True,   "editable": False },
]


 
'''
Model
'''
class DfModelTimes(DataframeTableModel):
    def __init__(self, name, parent = None):
        super(DfModelTimes, self).__init__(name)
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
    
    def getDefaultRow(self):
        row = DataframeTableModel.getDefaultRow(self)
        row["run_id"] = dstore.Get("current_run")        
        return row
               
                
        
    def sModelChanged(self, index1, index2):                
        DataframeTableModel.Update(self)
        
    def GetDataframe(self):
        df = mgr.GetDfs()["table"]
                
        if eventCalcReady.is_set() == False:
            #print self.changed_rows
            for index, row in self.changed_rows.iterrows():
                if index in df.index:
                    df.loc[index] = row             
        else:            
            self.changed_rows = pd.DataFrame()
                         
        return df
    
       
    def setDataFromDict(self, mydict):
        print "setDataFromDict()", mydict, self.name        
                
        tableRow =  self.df.loc[mydict["id"]].to_dict()
        tableRow.update(mydict)
        #print "row, ", mydict, tableRow
        
        update_flag = True
        
        #category changed
        if "nr" in mydict:
            update_flag = False                                    
            user_id = self.checkChangedNumber(tableRow)                                                 
            if user_id != None:
                mydict["user_id"] = user_id
                del mydict["nr"]
                update_flag = True
                 
                 
                #print "not cleared", tableRow
                cleared = self.ClearCalculated(tableRow)
                #print "CLEARED: ", cleared, type(cleared)                
                self.changed_rows = self.changed_rows.append(cleared, ignore_index = True)
                self.changed_rows["id"] = self.changed_rows["id"].astype(int)
                self.changed_rows.set_index('id',  drop=False, inplace = True)                                                              

                self.ResetNrOfLaps()
                eventCalcReady.clear()
                                         
        elif "cell" in mydict:                                                                      

            cleared = self.ClearCalculated(tableRow)
            #print "CLEARED: ", cleared, type(cleared)                
            self.changed_rows = self.changed_rows.append(cleared, ignore_index = True)
            self.changed_rows["id"] = self.changed_rows["id"].astype(int)
            self.changed_rows.set_index('id',  drop=False, inplace = True)                                                              
            #print "CHANGED:", self.changed_rows
                    
            self.ResetNrOfLaps()  
            eventCalcReady.clear()                       
            
        
        #update db from mydict
        if update_flag:        
            db.update_from_dict(self.name, mydict)
            self.ResetCalculatedValues(mydict["id"])        
            eventCalcNow.set()
            
    def ClearCalculated(self, tabRow):
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            tabRow["time"+str(i+1)] = None
            tabRow["lap"+str(i+1)] = None
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
        if(int(tabRow['nr']) == 0):
            user_id = 0
        else:
                        
            #rigthts to change start cell?
            if(int(tabRow['cell']) == 1) and (dstore.Get("evaluation")['starttime'] == StarttimeEvaluation.VIA_CATEGORY):                                                              
                uiAccesories.showMessage(self.table.name+" Update error", "Cannot assign user to start time!")
                return None
                                        
            #user exist?                    
            user = tableUsers.model.getUserParNr(tabRow['nr'])                                    
            if user == None:
                uiAccesories.showMessage(self.name+" Update error", "Cant find user with nr. "+ str(tabRow['nr']))
                return None
            
            #category exist?                                                                                              
            category = tableCategories.model.getCategoryParName(user['category'])                        
            if category.empty:
                uiAccesories.showMessage(self.name+" Update error", "Cant find category for this user: " + user['category'])
                return None 
            
#@             #user id exist?                                                                                                                                                         
#             user_id = tableUsers.getUserParIdOrTagId(user['user_id'])
#             if user_id == None:
#                 uiAccesories.showMessage(self.table.name+": Update error", "No user or tag with number "+str(tabRow['nr'])+"!")                                                                         
#                 return None                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                    
        return user['id']
    
    def ResetCalculatedValues(self, timeid):
        query = \
                " UPDATE times" +\
                    " SET time1 = Null, lap1 = Null, time2 = Null, lap2 = Null, time3 = Null, lap3 = Null" +\
                    " WHERE (times.id = \""+str(timeid)+"\")"                                
        res = db.query(query) 
        db.commit()                                                              
        return res
    
    def ResetNrOfLaps(self):
        query = \
                " UPDATE times" +\
                    " SET lap1 = Null, lap2 = Null, lap3 = Null"                                                    
        res = db.query(query)                        
        db.commit()        
        return res
        
             
    
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
    
    (eCSV_EXPORT, eHTM_EXPORT, eHTM_EXPORT_LOGO) = range(0,3)
    
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
    - pro sloupce kde se vyskytuje i něco jiného než číslo jsou reprezentovány jako object
    - to_csv() čísla exportuje jako float ve formátu 2.00
    - přetypuju je na float a formátem %g nastavím že nuly se přidávají jen když je třeba
    '''
    def ConvertToInt(self, df):  
        df["nr"]  = df["nr"].astype(float)
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            if "lap"+str(i+1) in df:
                df["lap"+str(i+1)]  = df["lap"+str(i+1)].astype(float)
            if "order"+str(i+1) in df:
                df["order"+str(i+1)]  = df["order"+str(i+1)].astype(float)
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            if "points"+str(i+1) in df:
                df["points"+str(i+1)]  = df["points"+str(i+1)].astype(float)                
        return df
                                       
    '''
     F11 - konečné výsledky, 1 čas na řádek
    '''  
    def sExportDirect(self, export_type = eCSV_EXPORT):
        #print tableUsers.model.df.columns
        #print self.model.df.columns
        cols_to_use = tableUsers.model.df.columns.difference(self.model.df.columns)
        cols_to_use = list(cols_to_use)
        cols_to_use = cols_to_use + ["nr"]
        aux_df2 = pd.merge(self.model.df, tableUsers.model.df[cols_to_use], how = "inner", on="nr")


        aux_df2["nr"]  = aux_df2["nr"].astype(float)
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            aux_df2["lap"+str(i+1)]  = aux_df2["lap"+str(i+1)].astype(float)
            aux_df2["order"+str(i+1)]  = aux_df2["order"+str(i+1)].astype(float)
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            aux_df2["points"+str(i+1)]  = aux_df2["points"+str(i+1)].astype(float)
        
        #update export df
        self.exportDf = [pd.DataFrame()] * NUMBER_OF.EXPORTS        
        for i in range(0, NUMBER_OF.EXPORTS):
                          
            aux_df = aux_df2.copy()
            #print "E: ",i,  aux_df.head(5)
            
            if (tabExportSettings.IsEnabled(i) == False):
                continue            
            
            #get export group            
            checked_info = dstore.GetItem('export', ["checked", i])
            
            #get export filtersort
            filtersort = dstore.GetItem('export_filtersort', [i])
                                      
            filter = filtersort['filter']
            sort1 = filtersort['sort1'].lower()  
            sort2 = filtersort['sort2'].lower()
            sortorder1 = True if(filtersort['sortorder1'].lower() == "asc") else False
            sortorder2 = True if(filtersort['sortorder2'].lower() == "asc") else False
            
            #filter 
            filter_split_keys = filter.split(" ")
            filter_keys = []
            for key in filter_split_keys:
                if(key in aux_df.columns):
                    filter_keys.append(key)
                
            #print filter_keys, len(filter_keys)
            
            if(len(filter_keys) == 1):
                #print "====", filter_keys
                aux_df =  aux_df[aux_df[filter_keys[0]] != ""]
                aux_df =  aux_df[aux_df[filter_keys[0]].notnull()]
                #print aux_df[filter_keys[0]]
                
            elif(len(filter_keys) == 2):
                aux_df =  aux_df[(aux_df[filter_keys[0]] != "") | (aux_df[filter_keys[1]] != "")]
                aux_df =  aux_df[(aux_df[filter_keys[0]] != None) | (aux_df[filter_keys[1]] != None)]
            
            #aux_df = self.joinedDf[(aux_df[column1].notnull()) & (self.joinedDf['user_id']!=0)]
            
                        
            #last time from each user                    
            aux_df = aux_df.sort("timeraw")                        
            if("last" in filter):                                                                
                aux_df = aux_df.groupby("nr", as_index = False).last()
            aux_df = aux_df.where(pd.notnull(aux_df), None)
            aux_df.set_index('id',  drop=False, inplace = True)
            
            #sort again
            if(sort2 in aux_df.columns):
                #print "nested sorting", sort1, sort2, sortorder1, sortorder2
                #print aux_df
                aux_df = aux_df.sort([sort1, sort2], ascending = [sortorder1, sortorder2])
            else:
                #print "basic sorting"
                aux_df = aux_df.sort(sort1, ascending = sortorder1)
                        
            #filter to checked columns
            columns = tabExportSettings.exportgroups[i].GetCheckedColumns()            
            
            for oc in range(0, NUMBER_OF.EXPORTS):
                ordercatX = 'ordercat'+str(oc+1)
                orderX = 'order'+str(oc+1)                
                aux_df[ordercatX] = aux_df[orderX].astype(str)+"./"+aux_df.category                        
                                                           
            
            self.ConvertToInt(aux_df)
            self.exportDf[i] = aux_df[columns]
        
        #print "sExport: start"
        #print self.exportDf[0] 
        exported = self.sExportCsv()
        print "sExport: done", exported
        return #self.joinedDf             
        
        
    def sExportCsv(self):               
        
        #ret = uiAccesories.showMessage("Results Export", "Choose format of results", MSGTYPE.question_dialog, "NOT finally results", "Finally results")                        
        #if ret == False: #cancel button
        #    return         
        
        #get filename  
        racename = dstore.GetItem("racesettings-app", ['race_name'])      
        dirname = utils.get_filename("export/"+timeutils.getUnderlinedDatetime()+"_"+racename+"/")
        try:
            os.makedirs(dirname)
        except OSError:
            dirname = "export/"
                                         
        if(dirname == ""):
            return        
                            
        exported = {}
                
        for i in range(0, NUMBER_OF.EXPORTS): 
            
            if (tabExportSettings.IsEnabled(i, "csv") == False):
                continue
            
            df =  self.exportDf[i]
            #df = mgr.GetDfs()["table"]
            
#             if(dstore.GetItem("racesettings-app", ['rfid']) == 0):
#                 if "time1" in df:
#                     if(dstore.GetItem("additional_info", ["time", 0, "minute_timeformat"])):
#                         df.time1[df.time1>"30:00,00"] = "DNF"
#                     else:
#                         df.time1[df.time1>"00:30:00,00"] = "DNF" 
#                             
#                 if "time2" in df:
#                     if(dstore.GetItem("additional_info", ["time", 1, "minute_timeformat"])):
#                         df.time2[df.time2>"30:00,00"] = "DNF"
#                     else:
#                         df.time2[df.time2>"00:30:00,00"] = "DNF" 
#                             
#                 if "time3" in df:
#                     if(dstore.GetItem("additional_info", ["time", 2, "minute_timeformat"])):
#                         df.time3[df.time3>"30:00,00"] = "DNF"
#                     else:
#                         df.time3[df.time3>"00:30:00,00"] = "DNF"             
        
            #get racename
            header = dstore.GetItem("export_header", [i])             
            racename =  header["racename"].replace("%race%", dstore.GetItem("racesettings-app", ['race_name']))            
                        
            #complete export
            if(len(df) != 0):
                filename = utils.get_filename("e"+str(i+1)+"_t_"+racename)
                self.ExportToCsvFile(dirname+filename+".csv", racename, df)            
                exported["total"] = len(df)
            
            
            #category export                
            c_df = self.exportDf[i]           
            c_df = c_df.set_index("category")
            category_groupby = c_df.groupby(c_df.index)
            for c_name, c_df in category_groupby:                
                if(len(c_df) != 0):
                    category = tableCategories.model.getCategoryParName(c_name)
                    category = category.to_dict()
                     
                    #add prefix and suffix for category name and desription
                    c_name =  header["categoryname"].replace("%category%", c_name)
                    category["name"] = c_name                    
                    category["description"]  =  header["description"].replace("%description%", category["description"])
                    
                    filename = utils.get_filename("e"+str(i+1)+"_c_"+c_name)  
               
                    self.ExportToCsvFile(dirname+filename+".csv", racename, c_df, category = category)
                    exported[filename] = len(c_df) 
#                     
#             #group export
#             groups = {}
#             g_df = manage_calc.exportDf[i]
#             for x in range(1,11):                
#                 g_label = "g"+str(x)
#                 values = tableCategories.getCategoryNamesParGroupLabel(g_label)   
#                 #print "VALUES", values
#                 categories = values 
#                 #print type(categories[0])#[str(v) for v in values]             
#                 aux_df = g_df[g_df["category"].isin(categories)]                                               
#                 if(len(aux_df) != 0):
#                     group = tableCGroups.getTabCGrouptParLabel(g_label)
#                     filename = utils.get_filename("e"+str(i+1)+"_"+g_label+"__"+group["name"])                                
#                     self.ExportToCsvFile(dirname+filename+".csv", racename, aux_df, group = group)                                       
#                     exported[filename] = len(aux_df)
                

                         
        return exported    

    
    def ExportToCsvFile(self, filename, racename, df, category = None, group = None):

        '''get the keys and strings'''
                      
        if category != None:                                 
            header_strings = ["Kategorie: " + category['name'], category['description']] #second line, first and last item              
        elif group != None:            
            header_strings = ["Skupina: " + group['name'], group['description']] #second line, first and last item
        else:            
            header_strings = ["", ""] #second line, first and last item                     
        
        
        '''add & convert header, write to csv file'''        
        aux_df = df
        if len(aux_df != 0):  
            #export header
            header_length = len(aux_df.columns)
            header_racename = [racename,] + (header_length-1) * ['']
            header_param = [header_strings[0],]+ ((header_length-2) * ['',]) + [header_strings[1],]
                           
            #convert header EN => CZ
            tocz_dict = dstore.GetItem("export", ["names"])                                                 
            aux_df = aux_df.rename(columns = tocz_dict)                                                              
            #aux_df = aux_df.rename(columns ={'o1': dstore.GetItem("export",['optionname', 1]), 'o2': dstore.GetItem("export", ['optionname', 2]), 'o3': dstore.GetItem("export", ['optionname', 3]), 'o4': dstore.GetItem("export", ['optionname', 4])})                           
            
            
            #export times (with collumn's names)            
            try:              
                pd.DataFrame([header_racename, header_param]).to_csv(filename, ";", index = False, header = None, encoding = "utf8")
                aux_df.to_csv(filename, ";", mode="a", index = False, encoding = "utf8", float_format = "%g")                
            except IOError:
                uiAccesories.showMessage(self.name+" Export warning", "File "+filename+"\nPermission denied!")
                           
        return aux_df                           

        
        
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
    
    
tableTimes = DfTableTimes()         


        
 
    