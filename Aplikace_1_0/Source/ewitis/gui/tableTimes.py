# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import time
import datetime
import os
from PyQt4 import QtCore, QtGui, Qt
from ewitis.gui.Ui import Ui
from ewitis.gui.UiAccesories import MSGTYPE, uiAccesories

from ewitis.gui.aTableModel import myModel, myProxyModel 
from ewitis.gui.aTable import myTable
from ewitis.gui.tableAlltags import tableAlltags
from ewitis.gui.tableTags import tableTags
from ewitis.gui.tablePoints import tablePoints
from ewitis.gui.tableCGroups import tableCGroups
from ewitis.gui.tableCategories import tableCategories
from ewitis.gui.tableUsers import tableUsers
from ewitis.gui.tabExportSettings import tabExportSettings


from ewitis.data.db import db
from ewitis.data.dstore import dstore

import libs.db_csv.db_csv as Db_csv
import ewitis.gui.TimesUtils as TimesUtils
import ewitis.gui.DEF_COLUMN as DEF_COLUMN
from ewitis.data.DEF_DATA import *
import libs.utils.utils as utils
import libs.timeutils.timeutils as timeutils
#import ewitis.gui.TimesStartTimes as TimesStarts
from ewitis.gui.TimesStore import TimesStore, timesstore

import pandas as pd 
from ewitis.data.DEF_ENUM_STRINGS import *


'''
F5 - refresh
F6 - export table
F7 - export WWW
F11 - export categories 
F12 - direct WWW export
'''        
class TimesModel(myModel):
    def __init__(self, table):                        
        myModel.__init__(self, table)                
        
        #
        #self.starts = TimesUtils.TimesStarts()
        #self.starts2 = TimesStarts.TimesStarts()
        #self.starts2 = TimesStore.TimesStore()
        
        self.order = TimesUtils.TimesOrder()
        #self.lap = TimesUtils.TimesLap()
        #self.laptime = TimesLaptimes.TimesLaptime()
                                                           
        #update with first run        
        first_run = db.getFirst("runs")
        if(first_run != None):
            self.run_id = first_run['id']
        else:
            self.run_id = 0 #no times for run_id = 0 
                                
                   

    
  
    def getDefaultDbRow(self): 
        row = myModel.getDefaultDbRow(self)
        row['run_id'] = self.run_id                                                                                                                     
        return row                 

    
                                                                                 

    
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
            dbUser = tableUsers.getDbUserParNr(tabRow['nr'])
            if dbUser == None:
                uiAccesories.showMessage(self.table.name+" Update error", "Cant find user with nr. "+ tabRow['nr'])
                return None
            #category exist?                                                                                              
            dbCategory = tableCategories.getDbRow(dbUser['category_id'])
            if dbCategory == None:
                uiAccesories.showMessage(self.table.name+" Update error", "Cant find category for this user.")
                return None 
            #user id exist?                                                                                                                                                         
            user_id = tableUsers.getIdOrTagIdParNr(tabRow['nr'])
            if user_id == None:
                uiAccesories.showMessage(self.table.name+": Update error", "No user or tag with number "+str(tabRow['nr'])+"!")                                                                         
                return None                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                    
        return user_id

    def sModelChanged(self, item):
                                
        if(dstore.Get("user_actions") == 0):                       
            
            ''' user has changed something '''
            
            #handle common columns
            ret = myModel.sModelChanged(self, item)
        
            if(ret == False):
                
                #get changed row, dict{}
                tabRow = self.row_dict(item.row())                
                
                # NR column
                if(item.column() == self.table.TABLE_COLLUMN_DEF['nr']['index']):                        
                    user_id = self.checkChangedNumber(tabRow)
                    if(user_id != None):
                        #write new number                
                        #print "update", {'id':tabRow['id'], 'user_id': tableUsers.getIdOrTagIdParNr(tabRow['nr'])}                    
                        db.update_from_dict(self.table.name, {'id':tabRow['id'], 'user_id': user_id})
                        self.table.ResetNrOfLaps()
                          
                 
                # STATUS column
                elif(item.column() == self.table.TABLE_COLLUMN_DEF['status']['index']):                    
                    if tableUsers.model.checkChangedStatus(tabRow) == True:
                        dbUser = tableUsers.getDbUserParNr(tabRow['nr'])                
                        #print "update",  {'id':dbUser['id'], 'status': tabRow['status']}
                        db.update_from_dict(tableUsers.name, {'id':dbUser['id'], 'status': tabRow['status']})  
                
                # TIMERAW column
                elif(item.column() == self.table.TABLE_COLLUMN_DEF['timeraw']['index']):                    
                    try:
                        dbTimeraw = TimesUtils.TimesUtils.timestring2time(tabRow['timeraw'])                    
                        #print "update", {'id': tabRow['id'], 'time_raw': dbTimeraw}
                        db.update_from_dict(self.table.name, {'id': tabRow['id'], 'time_raw': dbTimeraw})
                        self.table.ResetNrOfLaps()
                    except TimesUtils.TimeFormat_Error:
                        uiAccesories.showMessage(self.table.name+" Update error", "Wrong Time format!")
                        
                #reset all calculated values for this row
                self.table.ResetCalculatedValues(tabRow['id'])
                
                #update whole model
                self.Update()                
                            
                    
                
#                 if check == True:
#                     #update changed collumn                                  
#                     for key in self.table.DB_COLLUMN_DEF:
#                         if(item.column() == self.table.DB_COLLUMN_DEF[key]['index']):
#                             try: 
#                                 db.update_from_dict(self.table.name, {'id':tabRow['id'], key: tabRow[key]})                      
#                                 return True
#                             except:
#                                 uiAccesories.showMessage(self.table.name+" Update", "Error!")

#                 #update status
#                 dbRow = self.table.getDbRow(tabRow['id'])
                    #                 print "EQ",dbRow
                    
#                 if self.IsFinishTime(self.table.getDbRow(tabRow['id'])) == True:
#                                                                                                                                                                                      
#                     #convert sqlite row to dict
#                     dbUser = tableUsers.getDbUserParNr(tabRow['nr'])                    
#                      
#                     #update status                
#                     #print "finishtime", dbUser
#                     if dbUser != None: 
#                         db.update_from_dict(tableUsers.name, {'id': dbUser['id'], 'status': 'finished'})
                     
                
        
         
        return
        
        #end of test
        
    def db2tableRow(self, dbTime):
        """
        db    ["state", "id", "run_id", "user_id", "cell", "timeraw", "timeX", "lapX"]
        ==>    
        table ["id", "nr", "cell", "status", "timeX", "lapX", "name", "category", "orderX", "start_nr", "pointsX", "timeraw"]
        """
        
        #ztimeT = time.clock()
        #print "TIME", dbTime['id']                                
        
        if(dstore.Get('show')['times_with_order'] == 2):
            if(self.order.IsResultTime(dbTime) == False):                
                return None
                                                                  
        
        ''' 1to1 KEYS
        - ID, CELL 
        '''                   
        tabTime = myModel.db2tableRow(self, dbTime)        
         
        ''' get USER
            - user_id je id v tabulce Users(bunky) nebo tag_id(rfid) '''
        '''join user, hodnoty z table i db'''                                            
        joinUser =  tableUsers.getJoinUserParIdOrTagId(dbTime["user_id"])
        
        ''' get CATEGORY'''                    
        tabCategory =  tableCategories.getTabRow(joinUser['category_id'])        
                                        
        ''' OTHER KEYS ''' 
        
        '''NR'''                   
        tabTime['nr'] = joinUser['nr']
        
        '''NAME'''                       
        tabTime['name'] = joinUser['name'].upper() +' '+joinUser['first_name']        
        
        '''CATEGORY'''        
        tabTime['category'] = joinUser['category']  
                                    
        '''START NR'''
        if(tabTime['cell'] == 1) or (tabTime['nr'] == 0) or tabCategory==None: #start time?                           
            tabTime['start_nr'] = 1
        else:                                
            tabTime['start_nr'] = tabCategory['start_nr']
                    
        '''STATUS'''        
        if (dbTime['cell'] == 1) or (dbTime["user_id"] == 0):
            tabTime['status'] = ''        
        else:                       
            tabTime['status'] = joinUser['status']
            
        '''TIME
            dbtime 2 tabletime'''                                               
        
        '''TIMERAW'''        
        tabTime['timeraw'] = TimesUtils.TimesUtils.time2timestring(dbTime['time_raw'], True)                                                                                                                        
        
        additional_info = dstore.Get("additional_info")        
        
        '''TIME 1-3'''
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            
            #TIME 1-3
            if additional_info['time'][i]:                
                timeX = 'time'+str(i+1)
                if(dbTime[timeX] == None):                    
                    tabTime[timeX] = None #cas neexistuje
                else:                    
                    tabTime[timeX] = TimesUtils.TimesUtils.time2timestring(dbTime[timeX])  
            else: 
                tabTime[timeX] = None
                
        '''LAP 1-3'''
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            #LAP 1-3
            if additional_info['lap'][i]:                
                lapX = 'lap'+str(i+1)
                if(dbTime[lapX] == None):                    
                    tabTime[lapX] = None                    
                else:                                      
                    tabTime[lapX] = dbTime[lapX]  
            else: 
                tabTime[lapX] = None
                                 
        
        '''ORDER 1-3'''
        for i in range(0, NUMBER_OF.THREECOLUMNS):        
            if additional_info['order'][i]:      
                #ztime = time.clock()  
                #print self.dbDf                                      
                #tabTime['order' + str(i+1)] = self.CalcOrder(self.dbDf, dbTime, i) 
                #print "I: 1:",time.clock() - ztime,"s"          
                #print type(self.orderDf[i])
                #ztime = time.clock()
                #print self.orderDf[i]
                dbTime["category"] = tabTime["category"]                
                tabTime['order' + str(i+1)] = timesstore.CalcOrder(dbTime, i)                                
                #print "I: 2:",time.clock() - ztime,"s"
                #print dbTime['id'], 'order', str(i+1), tabTime['order' + str(i+1)] 
            else:                                                         
                tabTime['order' + str(i+1)] = None
                                        
        '''POINTS 1-3'''
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            if  additional_info['points'][i]:        
                #tabTime['points'+str(i+1)] = tablePoints.getPoints(tabTime, dbTime, i)
                tabTime['points'+str(i+1)] = timesstore.CalcPoints(dbTime, i)
            else:
                tabTime['points'+str(i+1)] = None
                                                                        
        return tabTime            
    
    '''
    dict => dict, vykopírují se hodnoty obsažené v keys (z time nebo user)   
    '''                       
    def tabRow2exportRow(self, tabRow, keys):                        
        exportRow = {}
        
        # time values
        exportRowTimes = myModel.tabRow2exportRow(self, tabRow, keys)
        
        # user values
        tabUserRow = tableUsers.getTabUserParNr(tabRow['nr'])
        exportRowUsers = tableUsers.model.tabRow2exportRow(tabUserRow, keys)
        
        #sloučení time a user
        exportRow = dict(exportRowUsers.items() + exportRowTimes.items())                              
        
        # special values
        if u'order_cat_cat' in keys:
            exportRow['order_cat_cat'] = tabRow['order_cat']+"./"+tabRow['category']
                                                
        return exportRow              
        

    
    def importRow2dbRow(self, importRow, mode = myModel.eTABLE):        
        try:
            importRow['id'] = int(importRow['id']) + 10000
        except:
            pass
        importRow['run_id'] = self.run_id            
        return importRow
        
    def IsFinishTime(self, dbTime):
        '''
        splňuje závodník podmínky pro "finished"?
            - (počet kol větší než X) nebo (čas větší než Y)
        '''
        if cLaptime.GetNrOfLap(dbTime, cLaptime.OF_LAST_TIME) >= dstore.Get('race_info')['limit_laps']:
            return True
        return False                                          
            
                
    def UpdateTimesLaps(self, joinDf):
        """
        u časů kde 'time'=None, do počítá time z time_raw a startovacího časů pomocí funkce calc_update_time()
        
        *Ret:*
            pole časů u kterých se nepodařilo časy updatovat   
        """
        ret_ko_times = []        
                
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            
             '''calc times'''
             time_group = dstore.GetItem('additional_info', ['time', i])
             if(time_group['checked'] != 0):
                lap_group = dstore.GetItem('additional_info', ['lap', i])         
            
                #calc times
                for index, dbTime in timesstore.timesDf[i].iterrows():
                
                    #df to dict
                    dbTime = dbTime.to_dict()
                                                                                                
                    '''calc time and lap'''
                    timeX = "time"+str(i+1)
                    lapX = "lap"+str(i+1)
                    value = None                     
                    if(dbTime[timeX] == None):                                                                                    
                        '''calc time'''                                                                                                                                                                                                                                                          
                        value = timesstore.CalcTime(dbTime, i)  
                        key = timeX                                                                         
                    elif (dbTime[lapX] == None) and (lap_group['checked'] != 0) and (dbTime['id'] in timesstore.lapDf[i].id.values):
                        '''calc lap'''                                                                                     
                        value = timesstore.CalcLap(dbTime, i)
                        key = lapX                                                                                                          
                                
                    #update db
                    if value != None:
                        try:                                                                                
                            db.update_from_dict(self.table.name, {'id':dbTime['id'], key:value}) #commit v update()
                        except IndexError: #potreba startime, ale nenalezen 
                            ret_ko_times.append(dbTime['id'])             
                              
        return ret_ko_times
    
    #UPDATE TABLE        
    def Update(self, run_id = None):        
        
        ret = True
        
        if(run_id != None):                    
            self.run_id = run_id #update run_id
        
        #table df    
        tabDf = self.df()
        
        #TIME 1-3                                      
        joinDf = timesstore.Update(self.run_id, tabDf)            
                      
        #self.tabDf = self.df()                                                                                                     
        #mydf2 = pd.concat([left, right], axis = 1)
        #columns =  self.tabDf.columns - self.dbDf.columns                              
        #joinDf = self.dbDf.join(self.tabDf[columns])
#         #print mydf       
#         
#         '''POINTS DFs'''
#         self.orderDf = [None, None, None]
#         for i in range(0, NUMBER_OF.POINTSCOLUMNS):
#               
#             #get order group
#             group = dstore.GetItem('additional_info', ['order', i])                 
#             column1 = group['column1'].lower()  
#             
#             #filter joindf
#             aux_df = joinDf[(joinDf[column1].notnull()) &  (joinDf['user_id']!=0)]
# 
#             #sort
#             aux_df.sort(column1)
#             
#             #last time from each user        
#             aux_df = aux_df.sort(column1).groupby("user_id", as_index = False).last() 
#             aux_df.set_index('id',  drop=False, inplace = True)
#             
#             self.orderDf[i] = aux_df               
                                                      
        ko_nrs = self.UpdateTimesLaps(joinDf)                        
        if(ko_nrs != []):            
            uiAccesories.showMessage(self.table.name+" Update error", "Some times have no start times, ids: "+str(ko_nrs), msgtype = MSGTYPE.statusbar)
            ret = False                                                                                                            
            
        db.commit()
                          
        #timesstore.Update(self.run_id)            
        myModel.Update(self, "run_id", self.run_id)
        #db.commit()        
        return ret            
                                                                                       

class TimesProxyModel(myProxyModel):
    def __init__(self, table):                                        
        myProxyModel.__init__(self, table)
        
    def IsColumnAutoEditable(self, column):
        if column == 1:
            '''změna čísla'''    
            return True
        return False
           
                  
   
# view <- proxymodel <- model 
class Times(myTable):   
    
    (eRESULT_TIMES, eALL_TIMES, eLAP_TIMES) = range(0,3)
      
    def  __init__(self):                
        
        #create table instance (slots, etc.)
        myTable.__init__(self, "Times")     
        
         
                
        #special slots
        #self.slots = Slots.TimesSlots(self)                                       
       
        #TIMERs
        #self.timer1s = QtCore.QTimer(); 
        #self.timer1s.start(1000);
                
        self.system = 0
                
        
    def InitGui(self):
        myTable.InitGui(self)        
        self.gui['export_www'] = Ui().TimesWwwExport         
        self.gui['recalculate'] = Ui().TimesRecalculate        
        self.gui['aDirectWwwExport'] = Ui().aDirectWwwExport
        self.gui['aExportResults'] = Ui().aExportResults
        self.gui['aExportAllTimes'] = Ui().aExportAllTimes 
        self.gui['aExportLaptimes'] = Ui().aExportLaptimes 
        self.gui['times_db_export'] = Ui().TimesDbExport 
        self.gui['times_db_import'] = Ui().TimesDbImport 
        self.gui['filter_column'] = Ui().TimesFilterColumn
        self.gui['filter_starts'] = Ui().TimesFilterStarts
        self.gui['filter_finishes'] = Ui().TimesFilterFinishes        
        
        
    def createSlots(self):
        
        #standart slots
        myTable.createSlots(self)        
                
        #filter starts/finishes
        QtCore.QObject.connect(self.gui['filter_starts'], QtCore.SIGNAL("clicked()"), self.sFilterStarts) 
        QtCore.QObject.connect(self.gui['filter_finishes'], QtCore.SIGNAL("clicked()"), self.sFilterFinishes)
        
        #import table (db format)
        QtCore.QObject.connect(self.gui['times_db_import'], QtCore.SIGNAL("clicked()"), lambda:myTable.sImport(self))
        
        #export table (db format)
        QtCore.QObject.connect(self.gui['times_db_export'], QtCore.SIGNAL("clicked()"), lambda:myTable.sExport(self, myModel.eDB, True))
        
        #button Recalculate
        QtCore.QObject.connect(self.gui['recalculate'], QtCore.SIGNAL("clicked()"), lambda:self.sRecalculate(self.model.run_id))
        
         
        #export direct www
        QtCore.QObject.connect(self.gui['aDirectWwwExport'], QtCore.SIGNAL("triggered()"), lambda:myTable.sExport(self, myModel.eWWW, False))
        
        #export result times        
        #if (self.gui['aDirectExportCategories'] != None):                                   
        QtCore.QObject.connect(self.gui['aExportResults'], QtCore.SIGNAL("triggered()"), lambda: self.sExportDirect(self.eRESULT_TIMES))
                                       
        #export  all times        
        QtCore.QObject.connect(self.gui['aExportAllTimes'], QtCore.SIGNAL("triggered()"), lambda: self.sExportDirect(self.eALL_TIMES))
        
        #export  laptimes        
        QtCore.QObject.connect(self.gui['aExportLaptimes'], QtCore.SIGNAL("triggered()"), lambda: self.sExportDirect(self.eLAP_TIMES))
        
        
           
    def sFilterStarts(self):
        self.gui['filter_column'].setValue(2)
        self.gui['filter'].setText("1")        
    def sFilterFinishes(self):
        self.gui['filter_column'].setValue(2)
        self.gui['filter'].setText("250")            
   
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
        
    
    def sRecalculate(self, run_id):
        if (uiAccesories.showMessage("Recalculate", "Are you sure you want to recalculate times and laptimes? \n (only for the current run) ", MSGTYPE.warning_dialog) != True):            
            return
        print "A: Times: Recalculating.. run id:", run_id
        query = \
                " UPDATE times" +\
                    " SET time1 = Null, lap1 = Null, time2 = Null, lap2 = Null, time3 = Null, lap3 = Null" +\
                    " WHERE (times.run_id = \""+str(run_id)+"\")"
                        
        res = db.query(query)
                        
        db.commit()
        print "A: Times: Recalculating.. press F5 to finish"
        return res
                 
    


            
    def GetExportKeys(self, mode):            
            
        #"order", "nr", "order_cat", "name"
        keys = []
        if(mode == myModel.eTOTAL) or (mode == myModel.eGROUP):
            keys = ["order", "nr", "order_cat_cat", "name"]                                                                      
        elif(mode == myModel.eCATEGORY):                                       
            keys = ["order_cat", "nr", "name"]                     
        
        # + "club", "sex", "lap", "time"
        if(mode == myModel.eTOTAL) or (mode == myModel.eGROUP) or (mode == myModel.eCATEGORY):
            if dstore.GetItem("export", ["year"]) == 2:                    
                keys.append("birthday")
            if dstore.GetItem("export", ["sex"]) == 2:                    
                keys.append("sex")
            if dstore.GetItem("export", ["club"]) == 2:                                       
                keys.append("club")
            # user_field_1             
            if dstore.GetItem("export", ["option_1"]) == 2:                    
                keys.append("o1")                    
            # user_field_2             
            if dstore.GetItem("export", ["option_2"]) == 2:
                keys.append("o2")                                        
            # user_field_3             
            if dstore.GetItem("export", ["option_3"]) == 2:
                keys.append("o3")                                                            
            # user_field_4             
            if dstore.GetItem("export", ["option_4"]) == 2:
                keys.append("o4")                                                                                
            # laps             
            if dstore.GetItem("export", ["laps"]) == 2:
                keys.append("lap")                                        
            # laptime             
            if dstore.GetItem("export", ["laptime"]) == 2:
                keys.append("laptime")                                                            
            # best laptime             
            if dstore.GetItem("export", ["best_laptime"]) == 2:
                keys.append("best_laptime")                                                            
            
            #time
            keys.append("time")                                           
                            
            #body - total, categories, groups
            if(dstore.GetItem("export", ["points1"]) == 2):                                                    
                keys.append('points1')                
            elif(dstore.GetItem("export", ["points2"]) == 2):                                                    
                keys.append('points2')                 
            elif(dstore.GetItem("export", ["points3"]) == 2):                                                    
                keys.append('points3')                                                                                                
        return keys

        
    '''
    export výsledků: F11 - result times, F10 - all times    
    - tabRow2exportRow vrací slovník s požadovanými hodnotami
    - jeden čas = jeden řádek     
    '''
    def ExportToDf(self, proxymodelDf = None, category = None, group = None, export_type = eRESULT_TIMES):                
        
        winner = None
        
        '''get keys (and winner)'''
        if category != None:
            #get winner
            if(export_type == self.eRESULT_TIMES):                
                winner = self.GetWinner(proxymodelDf, category['name'])                       
            keys = self.GetExportKeys(myModel.eCATEGORY)                          
        elif group != None:
            keys = self.GetExportKeys(myModel.eGROUP)            
        else:
            #get winner
            if(export_type == self.eRESULT_TIMES):                
                winner = self.GetWinner(proxymodelDf)  
            keys = self.GetExportKeys(myModel.eTOTAL)   
            
        #filter: no starttime
        proxymodelDf = proxymodelDf[proxymodelDf['cell'] != '1']
         
        #filter: category
        if category != None:
            proxymodelDf = proxymodelDf[proxymodelDf['category'] == category['name']]
            
        #filter: group
        if group != None:            
            cat_names = tableCategories.getCategoryNamesParGroupLabel(group['label'])
            proxymodelDf = proxymodelDf[proxymodelDf['category'].isin(cat_names)]                
                           
            
        '''fill the list (with matching rows/dicts)'''
        listRows = [] 
        for index, tabRow in proxymodelDf.iterrows():                 
            
            #vrací slovník s požadovanými hodnotami                       
            exportRow = self.model.tabRow2exportRow(tabRow, keys)                        
            
            #add gap (according to winner)
            if (dstore.GetItem("export", ["gap"]) == 2) and (winner != None):                
                if ('lap1' in tabRow) and ('time1' in tabRow):                                           
                    exportRow['gap'] = self.model.order.GetGap(tabRow['lap1'], tabRow['time1'], winner['lap1'], winner['time1']) 
                    if ('gap' in keys) == False:
                        keys.append('gap')                                
            
            # no values, take next
            if exportRow == None:
                continue
            
            # append to the list                 
            dbTime = self.getDbRow(tabRow['id'])
            if (export_type == self.eALL_TIMES) or (self.model.order.IsResultTime(dbTime) == True):                                                                   
                listRows.append(exportRow)
                                  
        if listRows != []:
            print "===="
            if category:
                print "category: ", category['name']
            if group:
                print "group: ", group['label'], group['name']            
            print "===="
            
            #get dataframe (from dicts, keys určují pořadí)
            return pd.DataFrame(listRows, columns = keys)
                
        return pd.DataFrame({}, columns = keys)
    
    '''
    export časů okruhu (F9)
    - group by nr
    - všechny časy na jeden řádek     
    '''
    def ExportToDf_laps(self, proxymodelDf, category, group):              
                        
        #filter: no startimes, only with laptime!
        proxymodelDf = proxymodelDf[proxymodelDf['cell'] != '1']        
        proxymodelDf = proxymodelDf[proxymodelDf['laptime'] != '']           
        
        #filter: category
        if category != None:
            proxymodelDf = proxymodelDf[proxymodelDf['category'] == category['name']]
            
        #filter: group 
        if group != None:            
            cat_names = tableCategories.getCategoryNamesParGroupLabel(group['label'])
            proxymodelDf = proxymodelDf[proxymodelDf['category'].isin(cat_names)]
                    
        '''group by number'''                
        times_groups = proxymodelDf.groupby('nr', sort = False)                                                 
        
        '''fill the list (with matching rows/series)'''
        listRows = []
        keys = [u"Číslo", u"Jméno", u"1.Kolo", u"2.Kolo", u"3.Kolo",u"4.Kolo", u"5.Kolo", u"6.Kolo",u"7.Kolo", u"8.Kolo", u"9.Kolo", u"10.Kolo", u"11.Kolo", u"12.Kolo", u"13.Kolo", u"14.Kolo", u"15.Kolo",u"16.Kolo", u"17.Kolo", u"18.Kolo",u"19.Kolo", u"20.Kolo", u"21.Kolo", u"22.Kolo", u"23.Kolo", u"24.Kolo"]
        for k, dfTimes in times_groups:                        
                        
            #series with times            
            if dstore.Get("export")['lapsformat'] == ExportLapsFormat.FORMAT_TIMES:                                        
                sTimes = dfTimes.sort(['timeraw']).time
            elif dstore.Get("export")['lapsformat'] == ExportLapsFormat.FORMAT_LAPTIMES:                                        
                sTimes = dfTimes.sort(['timeraw']).laptime
            elif dstore.Get("export")['lapsformat'] == ExportLapsFormat.FORMAT_POINTS_1:                                        
                sTimes = dfTimes.sort(['timeraw']).points1
            elif dstore.Get("export")['lapsformat'] == ExportLapsFormat.FORMAT_POINTS_2:                                        
                sTimes = dfTimes.sort(['timeraw']).points2
            elif dstore.Get("export")['lapsformat'] == ExportLapsFormat.FORMAT_POINTS_3:                                        
                sTimes = dfTimes.sort(['timeraw']).points3
            else:                                                       
                print "ExportToDf_laps: Fatal error"
        
            #merge two series             
            sLaps = pd.concat([dfTimes[['nr','name']].iloc[0], sTimes]) 
            sLaps.index = keys[0:len(sLaps)]                        
            
            #append new row/series            
            listRows.append(sLaps)                                                                        
                    
        if listRows != []:
            df = pd.DataFrame(listRows, columns = keys)            
            return df
                
        return pd.DataFrame({}, columns = keys)                                                                                                         
    
    '''
    export jednoho souboru s výsledky
    '''    
    def ExportToCsvFile(self, filename, proxymodelDf = None, category = None, group = None, export_type = eRESULT_TIMES):

        '''get the keys and strings'''                
        if category != None:                                 
            header_strings = ["Kategorie: " + category['name'], category['description']] #second line, first and last item              
        elif group != None:            
            header_strings = ["Skupina: " + group['name'], group['description']] #second line, first and last item
        else:            
            header_strings = ["", ""] #second line, first and last item              
         
        '''create export dataframe'''        
        if (export_type == self.eRESULT_TIMES) or (export_type == self.eALL_TIMES):
            exportDf = self.ExportToDf(proxymodelDf, category, group, export_type = export_type)                  
        elif(export_type == self.eLAP_TIMES):
            exportDf = self.ExportToDf_laps(proxymodelDf, category, group)            
        else:
            print "FATAL ERROR"        
        
        
        '''add & convert header, write to csv file'''
        if len(exportDf != 0):                         
            #export header
            header_length = len(exportDf.columns)
            header_racename = [dstore.GetItem("racesettings-app", ['race_name']),] + (header_length-1) * ['']
            header_param = [header_strings[0],]+ ((header_length-2) * ['',]) + [header_strings[1],]
            
            #convert header EN => CZ                        
            exportDf.rename(columns = STRINGS.EN2CZ, inplace = True)               
            exportDf.rename(columns ={'o1': dstore.GetItem("export",['optionname', 1]), 'o2': dstore.GetItem("export", ['optionname', 2]), 'o3': dstore.GetItem("export", ['optionname', 3]), 'o4': dstore.GetItem("export", ['optionname', 4])}, inplace = True)                           
            
            #export times (with collumn's names)            
            try:              
                pd.DataFrame([header_racename, header_param]).to_csv(filename, ";", index = False, header = None, encoding = "utf8")               
                exportDf.to_csv(filename, ";", mode="a", index = False, encoding = "utf8")
            except IOError:
                uiAccesories.showMessage(self.name+" Export warning", "File "+filename+"\nPermission denied!")
                           
        return exportDf
    
    def GetWinner(self, dfTimes, categoryname = None):
        winner = None
        
        try:
            if categoryname != None:
                winner = dict( dfTimes[(dfTimes['order_cat'] == u'1') & (dfTimes['category'] == categoryname)].iloc[0])
            else:
                winner = dict(dfTimes[dfTimes['order'] == u'1'].iloc[0])
        except IndexError:
            winner = None
             
        return winner
    #=======================================================================
    # SLOTS
    #=======================================================================    
        
    '''
     F11 - konečné výsledky, 1 čas na řádek
    '''
    def sExportDirectOld(self, export_type = eRESULT_TIMES):        
        suffix = ""
        if(export_type == self.eALL_TIMES):
            suffix = "_at"
        elif(export_type == self.eLAP_TIMES):
            suffix = "_laps"
        
        
        #ret = uiAccesories.showMessage("Results Export", "Choose format of results", MSGTYPE.question_dialog, "NOT finally results", "Finally results")                        
        #if ret == False: #cancel button
        #    return         
        
        #get filename, gui dialog        
        dirname = utils.get_filename("export/"+timeutils.getUnderlinedDatetime()+"_"+dstore.GetItem("racesettings-app", ['race_name'])+suffix+"/")
        try:
            os.makedirs(dirname)
        except OSError:
            dirname = "export/"
                                         
        if(dirname == ""):
            return
                            
        exported = {}        
        proxymodelDf = self.proxy_model.df()
                   
                        
        '''1. TOTAL'''
        #get name
        name = utils.get_filename("_"+dstore.GetItem("racesettings-app", ['race_name']))                
        
        #write to csv
        df = self.ExportToCsvFile(dirname+name+".csv", proxymodelDf = proxymodelDf, export_type = export_type)
        if(len(df) != 0):
            exported["total"] = len(df)
            
        '''2. CATEGORIES'''
        dbCategories = tableCategories.getDbRows()                      
        for dbCategory in dbCategories:
            
            #get name
            name = utils.get_filename("c_"+dbCategory['name'])                                              
                     
            #write to csv            
            df = self.ExportToCsvFile(dirname+name+".csv", proxymodelDf = proxymodelDf, category = dbCategory,  export_type = export_type)             
            if(len(df) != 0):
                exported[name] = len(df) 
            
        '''3. GROUPS'''                   
        dbCGroups = tableCGroups.getDbRows()                                                            
        for dbCGroup in dbCGroups:
               
            #get name
            name = utils.get_filename("g_"+dbCGroup['label'])
             
            #write to csv
            df = self.ExportToCsvFile(dirname+name+".csv", proxymodelDf = proxymodelDf, group = dbCGroup, export_type= export_type)
            if(len(df) != 0):
                exported[name] = len(df) 
            
        
        exported_string = ""
        for key in sorted(exported.keys()):
            exported_string += key + " : " + str(exported[key])+" times\n"        
        uiAccesories.showMessage(self.name+" Exported", exported_string, MSGTYPE.info)
                                    
    def sExportDirect(self, export_type = eRESULT_TIMES):        
        suffix = ""
        if(export_type == self.eALL_TIMES):
            suffix = "_at"
        elif(export_type == self.eLAP_TIMES):
            suffix = "_laps"
        
        
        #ret = uiAccesories.showMessage("Results Export", "Choose format of results", MSGTYPE.question_dialog, "NOT finally results", "Finally results")                        
        #if ret == False: #cancel button
        #    return         
        
        #get filename, gui dialog        
        dirname = utils.get_filename("export/"+timeutils.getUnderlinedDatetime()+"_"+dstore.GetItem("racesettings-app", ['race_name'])+suffix+"/")
        try:
            os.makedirs(dirname)
        except OSError:
            dirname = "export/"
                                         
        if(dirname == ""):
            return
                            
        exported = {}
        timesstore.UpdateExportDf()        
        aux_df =  timesstore.exportDf[0]
        mylist = tabExportSettings.exportgroups[0].GetAsList()
        mylist.remove("enabled")
        keys = dstore.Get("export_sortkeys")        
        sortkeys =  sorted(mylist, key=lambda k: keys.index(k))        
        #print "export df A:", aux_df
        print "export df B:", aux_df[sortkeys] 
        return
                   
                        
        '''1. TOTAL'''
        #get name
        name = utils.get_filename("_"+dstore.GetItem("racesettings-app", ['race_name']))                
        
        #write to csv
        df = self.ExportToCsvFile(dirname+name+".csv", proxymodelDf = proxymodelDf, export_type = export_type)
        if(len(df) != 0):
            exported["total"] = len(df)
            
        '''2. CATEGORIES'''
        dbCategories = tableCategories.getDbRows()                      
        for dbCategory in dbCategories:
            
            #get name
            name = utils.get_filename("c_"+dbCategory['name'])                                              
                     
            #write to csv            
            df = self.ExportToCsvFile(dirname+name+".csv", proxymodelDf = proxymodelDf, category = dbCategory,  export_type = export_type)             
            if(len(df) != 0):
                exported[name] = len(df) 
            
        '''3. GROUPS'''                   
        dbCGroups = tableCGroups.getDbRows()                                                            
        for dbCGroup in dbCGroups:
               
            #get name
            name = utils.get_filename("g_"+dbCGroup['label'])
             
            #write to csv
            df = self.ExportToCsvFile(dirname+name+".csv", proxymodelDf = proxymodelDf, group = dbCGroup, export_type= export_type)
            if(len(df) != 0):
                exported[name] = len(df) 
            
        
        exported_string = ""
        for key in sorted(exported.keys()):
            exported_string += key + " : " + str(exported[key])+" times\n"        
        uiAccesories.showMessage(self.name+" Exported", exported_string, MSGTYPE.info)                            
                               
                    
    #toDo: sloucit s myModel konstruktorem        
    def Update(self, run_id = None):            
        
        ai = dstore.Get("additional_info")
          
        #show additional info, checkbox                      

        
        #update
        ztime = time.clock()
        ret = self.model.Update(run_id = run_id)                                
        print "I: Times: update:",time.clock() - ztime,"s"
        
        #myModel.myTable.Update(self)        
        self.setColumnWidth()        
        
        #create list of columns to hide
        #print ai.items()
        columns = []
        for k,v in ai.items():            
            c = 0
            for item in v:
                c = c+1                
                if(item['checked'] == 0):                    
                    columns.append(k+""+str(c))
                    
        self.hiddenCollumns =  columns                                                       
        #self.hiddenCollumns = [k for k,v in ai.items() if v==0]
                
        self.updateHideColumns()
        
        #update couterns
        self.updateTabCounter()
        self.updateDbCounter()
        return ret
            

    # REMOVE ROW      
    # first starttime cant be deleted          
    def sDelete(self):        
        
        #get selected id
        try:                     
            rows = self.gui['view'].selectionModel().selectedRows()                        
            id = self.proxy_model.data(rows[0]).toString()
        except:
            uiAccesories.showMessage(self.name+" Delete error", "Cant be deleted")
            return
            
        #first start time? => cant be updated               
        #if(int(id) == (self.model.utils.getFirstStartTime(self.model.run_id)['id'])):
        #if(int(id) == (self.model.starts.GetFirst(self.model.run_id)['id'])):
        #if(int(id) == (self.model.starts2.GetFirst()['id'])):
        #    uiAccesories.showMessage(self.name+" Delete warning", "First start time cant be deleted!")
        #    return  
        
        #delete run with additional message
        myTable.sDelete(self)
                                                                                                                                  
    #
    def getCount(self, run_id, dbCategory = None, minimal_laps = None):
        run_id_esc = str(run_id)                                       
        
        query = "SELECT COUNT(*) FROM(\
                    SELECT COUNT(times.id) from times"
        
        if(dstore.Get("racesettings-app", ['rfid']) == 2):
            query = query + \
                    " INNER JOIN tags ON times.user_id = tags.tag_id"+\
                    " INNER JOIN users ON tags.user_nr = users.nr "
        else:
            query = query + \
                    " INNER JOIN users ON times.user_id = users.id"
            
        query = query + \
                    " WHERE (times.run_id = "+run_id_esc+")"\
                        " AND (users.state != \"dns\")"\
                        " AND (users.state != \"dnf\")"\
                        " AND (users.state != \"dnq\")"
        if dbCategory:
            category_id_esc = str(dbCategory["id"])                        
            query = query + \
                        " AND (users.category_id = "+category_id_esc+")"
        query = query + \
                    " GROUP by times.user_id"
                    
        if minimal_laps:
            query = query + \
                    " HAVING count(*) >= " + str(minimal_laps)
                    
        query = query + ")"     
        
        #print query
        res = db.query(query)
        return res.fetchone()[0]                                                            
        
                                    
                                                                                            
    
tableTimes = Times()   
            
            

        
        
    