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


from ewitis.data.db import db
from ewitis.data.dstore import dstore

import libs.db_csv.db_csv as Db_csv
import ewitis.gui.TimesUtils as TimesUtils
import ewitis.gui.DEF_COLUMN as DEF_COLUMN
from ewitis.data.DEF_DATA import *
import libs.utils.utils as utils
import libs.timeutils.timeutils as timeutils
import ewitis.gui.TimesStartTimes as TimesStarts
import ewitis.gui.TimesLaptimes as TimesLaptimes
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
        self.starts2 = TimesStarts.TimesStarts()
        
        self.order = TimesUtils.TimesOrder()
        #self.lap = TimesUtils.TimesLap()
        self.laptime = TimesLaptimes.TimesLaptime()
                                                           
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

    
    def db2tableRow(self, dbTime):
        """    
        ["id", "nr", "cell", "time", "name", "category", "address"]
        """
        
        #ztimeT = time.clock()
        #print "TIME", dbTime['id']                                
        
        if(dstore.Get('show')['times_with_order'] == 2):
            if(self.order.IsResultTime(dbTime) == False):                
                return None
                                                                  
        
        ''' 1to1 KEYS '''           
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
                                    
        '''START NR'''
        if(tabTime['cell'] == 1) or (tabTime['nr']==0) or tabCategory==None: #start time?                           
            tabTime['start_nr'] = 1 #decrement 1.starttime
        else:                                
            tabTime['start_nr'] = tabCategory['start_nr']
                    
        '''STATUS'''        
        if (dbTime['cell'] == 1) or (dbTime["user_id"] == 0):
            tabTime['status'] = ''        
        else:                       
            tabTime['status'] = joinUser['status']
            
        '''TIME
            dbtime 2 tabletime'''                                               
        
        '''raw time'''        
        tabTime['timeraw'] = TimesUtils.TimesUtils.time2timestring(dbTime['time_raw'], True)
        
        '''time'''
        if(dbTime['time'] == None):
            '''cas neexistuje'''
            tabTime['time'] = None
        else:            
            tabTime['time'] = TimesUtils.TimesUtils.time2timestring(dbTime['time'])            
                
        '''NAME'''        
#        if(dbTime['cell'] == 1):
#            tabTime['name'] = ''
        #if(dbTime["user_id"] == 0):
        #    tabTime['name'] = 'undefined'
        #else:                       
        tabTime['name'] = joinUser['name'].upper() +' '+joinUser['first_name']        
        
        '''CATEGORY'''        
        tabTime['category'] = joinUser['category']                                                                                                                              
             
        tabTime['lap'] = None
        tabTime['order'] = None
        tabTime['order_cat'] = None       
        
        '''LAP'''        
        #@workaround: potrebuju lap pro poradi => lap.Get() nerezohlednuje ("additional_info")['lap']                
        aux_lap = self.laptime.GetLap(dbTime)          
        if  dstore.Get("additional_info")['lap']:                
            tabTime['lap'] = aux_lap        
        
        '''LAPTIME'''     
        #počítá se jen pokud neexistuje           
        tabTime['laptime'] = TimesUtils.TimesUtils.time2timestring(self.laptime.Get(dbTime))
        
        '''BEST LAPTIME'''
        #počítá se vždy                        
        tabTime['best_laptime'] = TimesUtils.TimesUtils.time2timestring(self.laptime.GetBest(dbTime))                                           
        
        '''ORDER'''
        #počítá se vždy                                                                                         
        tabTime['order']  = self.order.Get(dbTime, aux_lap)        
                                                        
        '''ORDER IN CATEGORY'''
        #počítá se vždy                                                                       
        tabTime['order_cat'] = self.order.Get(dbTime, aux_lap, category_id = joinUser['category_id'])        
                                                                                                  
        
        '''POINTS'''
        if (dstore.Get("additional_info")["enabled"] == 2):
            try:        
                tabTime['points'] = tablePoints.getPoints(tabTime, tablePoints.eTOTAL)        
                tabTime['points_cat'] = tablePoints.getPoints(tabTime, tablePoints.eCATEGORY)                        
            except:
                print "E: Some points were not succesfully calculated!"
        return tabTime
                                                                                   

    
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
                if self.IsFinishTime(self.table.getDbRow(tabRow['id'])) == True:
                                                                                                                                                                                     
                    #convert sqlite row to dict
                    dbUser = tableUsers.getDbUserParNr(tabRow['nr'])                    
                     
                    #update status                
                    #print "finishtime", dbUser 
                    db.update_from_dict(tableUsers.name, {'id': dbUser['id'], 'status': 'finished'})
                     
                
        
         
        return
        
        #end of test
            
    
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
        if self.laptime.GetLaps(dbTime) >= dstore.Get('race_info')['limit_laps']:
            return True
        return False
        
    def update_laptime(self, dbTime):
        
        if(dbTime['laptime'] == None):            
                                    
            '''vypocet spravneho casu a ulozeni do databaze pro pristi pouziti'''                                                           
            laptime = self.laptime.Get(dbTime)                                            
             
            if laptime != None:                                                        
                '''ulozeni do db'''
                #print "Times: update laptime, id:", dbTime['id'],"time:",laptime            
                dbTime['laptime'] = laptime                                                       
                db.update_from_dict(self.table.name, dbTime) #commit v update()
                
    def update_laptimes(self):
        """
        u časů kde 'time'=None, do počítá time z time_raw a startovacího časů pomocí funkce calc_update_time()
        
        *Ret:*
            pole čísel závodníků u kterých se nepodařilo časy updatovat   
        """
        ret_ko_times = []
        
        dbTimes = db.getAll(self.table.name)
        dbTimes = db.cursor2dicts(dbTimes)
        
        for dbTime in dbTimes:
            
            '''time'''
            if(dbTime['laptime'] == None):                                                                        
                '''vypocet spravneho casu a ulozeni do databaze pro pristi pouziti'''
                
                try:                                    
                    self.update_laptime(dbTime)
                except:                    
                    ret_ko_times.append(dbTime['id'])
                           
        return ret_ko_times
                                                       
    def calc_update_time(self, dbTime):
        
        if(dbTime['time'] == None):
            
            '''no time in some cases'''
            
            #start time => no time
            if(dbTime['cell'] == 1):                
                return None
            
            #user without number => no time          
            tabUser =  tableUsers.getTabUserParIdOrTagId(dbTime["user_id"])          
            if(tabUser['nr'] == 0):
                return None      
                                    
            '''vypocet spravneho casu a ulozeni do databaze pro pristi pouziti'''
                            
   
            
            #try:
            '''toDo: misto try catch, Get bude vracet None'''                
            if dstore.Get('remote') == 2:
                return None             
            elif(dstore.Get('evaluation')['starttime'] == StarttimeEvaluation.VIA_CATEGORY):                                                                                                                              
                start_nr = tableCategories.getTabRow(tabUser['category_id'])['start_nr'] #get category starttime                
                start_time = self.starts2.Get(start_nr)                    
            elif(dstore.Get('evaluation')['starttime'] == StarttimeEvaluation.VIA_USER):
                #print "calc_update_time:", dbTime, start_nr
                start_time = self.starts2.GetLast(dbTime)                    
            else:
                print "E: Fatal Error: Starttime "
                return None
                                                                                                 
            if start_time.empty != True:                                                                                     
                '''odecteni startovaciho casu a ulozeni do db'''
                if(dbTime['time_raw'] < start_time['time_raw']):
                    print "E: Times: startime started later as this time!", dbTime 
                else:                       
                    dbTime['time'] = dbTime['time_raw'] - start_time['time_raw']
                #except:                         
                #    print "E: Times: no starttime nr.",start_nr,", for time", dbTime 
                            
                db.update_from_dict(self.table.name, dbTime) #commit v update()                                           
            
                
    def calc_update_times(self):
        """
        u časů kde 'time'=None, do počítá time z time_raw a startovacího časů pomocí funkce calc_update_time()
        
        *Ret:*
            pole časů u kterých se nepodařilo časy updatovat   
        """
        ret_ko_times = []
        
        dbTimes = db.getAll(self.table.name)
        dbTimes = db.cursor2dicts(dbTimes)
        
        for dbTime in dbTimes:
            
            '''time'''
            if(dbTime['time'] == None):
            
                '''vypocet spravneho casu a ulozeni do databaze pro pristi pouziti'''
                try:                                    
                    self.calc_update_time(dbTime)
                except IndexError: #potreba startime, ale nenalezen 
                    ret_ko_times.append(dbTime['id'])                        
        return ret_ko_times
    
    #UPDATE TABLE        
    def Update(self, run_id = None):        
        
        ret = True
        
        if(run_id != None):                    
            self.run_id = run_id #update run_id
            
        #update start times      
        self.starts2.Update(self.run_id)        
        self.laptime.Update(self.run_id)        
                
        ko_nrs = self.calc_update_times()        
        if(ko_nrs != []):            
            uiAccesories.showMessage(self.table.name+" Update error", "Some times have no start times, ids: "+str(ko_nrs), msgtype = MSGTYPE.statusbar)
            ret = False
            
        ko_nrs = self.update_laptimes()        
        if(ko_nrs != []):
            uiAccesories.showMessage(self.table.name+" Update error", "Some laptimes can not be updated"+str(ko_nrs), msgtype = MSGTYPE.statusbar)            
            ret = False
            
        db.commit()
                          
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
        
        QtCore.QObject.connect(Ui().timesShowAdditionalInfo, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("additional_info", ["enabled"], state, self.Update))
                
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
                    " SET time = Null, laptime = Null" +\
                    " WHERE (times.id = \""+str(timeid)+"\")"                                
        res = db.query(query)                        
        db.commit()        
        return res
        
    
    def sRecalculate(self, run_id):
        if (uiAccesories.showMessage("Recalculate", "Are you sure you want to recalculate times and laptimes? \n (only for the current run) ", MSGTYPE.warning_dialog) != True):            
            return
        print "A: Times: Recalculating.. run id:", run_id
        query = \
                " UPDATE times" +\
                    " SET time = Null, laptime = Null" +\
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
            if(mode == myModel.eTOTAL) and (dstore.GetItem("export", ["points_race"]) == 2):                                                    
                keys.append('points')                
            elif(mode == myModel.eCATEGORY) and (dstore.GetItem("export", ["points_categories"]) == 2):                                                    
                keys.append('points_cat')                 
            elif(mode == myModel.eGROUP) and (dstore.GetItem("export", ["points_groups"]) == 2):                                                    
                keys.append('points')                                                                                                
        return keys

        
    '''
    export jednoho souboru s výsledky
    '''
    def ExportToDf(self, proxymodelDf = None, category = None, group = None, export_type = eRESULT_TIMES):                
        
        winner = None
        
        '''get the keys and strings'''
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
            
        #category check
        if category != None:
            proxymodelDf = proxymodelDf[proxymodelDf['category'] == category['name']]
                           
            
        '''create export dataframe'''
        listRows = []#pd.DataFrame(columns = keys) 
        for index, tabRow in proxymodelDf.iterrows():                                             
            
#             #alternative category check
#             if category != None:                
#                 if tabRow['category'] != category['name']:                    
#                     continue
                 
            #group check
            if group != None:                
                tabCategory = tableCategories.getTabCategoryParName(tabRow['category'])
                if (tabCategory[group['label']] != 1):
                    continue
                            
            dbTime = self.getDbRow(tabRow['id'])                                   
            if(dbTime['user_id'] == 0) or (dbTime['cell'] <= 1):
                continue
            
            #tabRow to exportRow                       
            exportRow = self.model.tabRow2exportRow(tabRow, keys)                        
            
            #add gap    
            if dstore.GetItem("export", ["gap"]) == 2 and winner!=None:                            
                if ('lap' in keys) and ('time' in keys):                                                                                                                                    
                    gap = self.model.order.GetGap(exportRow['lap'], exportRow['time'], winner['lap'], winner['time'])     
                    exportRow['gap'] = gap             
            
            if exportRow == None:
                continue
            
            if (export_type == self.eALL_TIMES) or (self.model.order.IsResultTime(dbTime) == True):                                                                   
                listRows.append(exportRow)
                                  
        if listRows != []:
            return pd.DataFrame(listRows, columns = keys) #exportDf
                
        return pd.DataFrame({}, columns = keys) #exportDf
    
    def ExportToDf_laps(self, proxymodelDf, category, group):              
                        
        #no startimes
        proxymodelDf = proxymodelDf[proxymodelDf['cell'] > 1]
        
        #category selection
        if category != None:
            proxymodelDf = proxymodelDf[proxymodelDf['category'] == category['name']]
            
        #(dbTime['user_id'] == 0) or (dbTime['cell'] <= 1):
        '''1. TOTAL'''        
        #get name
        times_groups = proxymodelDf.groupby('nr', sort = False)
                          
        
               
        
        #group = times_groups.get_group(u'395')
        listRows = []
        for k, dfTimes in times_groups:            
                        
            #series with times                
            sTimes = dfTimes.sort(['time']).time
            sTimes.index = range(1, len(sTimes)+1)                           
        
            #merge two series
            sLaps = pd.concat([dfTimes[['nr','name']] .iloc[0], sTimes])                                    
            listRows.append(sLaps)                                                    
            
        keys = [u"Číslo", u"Jméno", u"1.Kolo", u"2.Kolo", u"3.Kolo",u"4.Kolo", u"5.Kolo", u"6.Kolo",u"7.Kolo", u"8.Kolo", u"9.Kolo", u"10.Kolo", u"11.Kolo", u"12.Kolo", u"13.Kolo", u"14.Kolo", u"15.Kolo",u"16.Kolo", u"17.Kolo", u"18.Kolo",u"19.Kolo", u"20.Kolo", u"21.Kolo", u"22.Kolo", u"23.Kolo", u"24.Kolo"]
        if listRows != []:
            return pd.DataFrame(listRows, columns = keys) #exportDf
                
        return pd.DataFrame({}, columns = keys) #exportDf                                                                                                         
        
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
            header_racename = [dstore.Get('race_name'),] + (header_length-1) * ['']
            header_param = [header_strings[0],]+ ((header_length-2) * ['',]) + [header_strings[1],]
            
            #convert header EN => CZ                        
            exportDf.rename(columns = STRINGS.EN2CZ, inplace = True)               
            exportDf.rename(columns ={'o1': dstore.Get("export")['option_1_name'], 'o2': dstore.Get("export")['option_2_name'], 'o3': dstore.Get("export")['option_3_name'], 'o4': dstore.Get("export")['option_4_name']}, inplace = True)                           
            
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
        dirname = utils.get_filename("export/"+timeutils.getUnderlinedDatetime()+"_"+dstore.Get('race_name')+suffix+"/")
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
        name = utils.get_filename("_"+dstore.Get('race_name'))                
        
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
        
        #show additional info, checkbox                      
        Ui().timesShowAdditionalInfo.setCheckState(dstore.Get("additional_info")['enabled'])
        
        #update
        ztime = time.clock()
        ret = self.model.Update(run_id = run_id)                                
        print "I: Times: update:",time.clock() - ztime,"s"
        
        #myModel.myTable.Update(self)        
        self.setColumnWidth()
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
        if(int(id) == (self.model.starts2.GetFirst()['id'])):
            uiAccesories.showMessage(self.name+" Delete warning", "First start time cant be deleted!")
            return  
        
        #delete run with additional message
        myTable.sDelete(self)
                                                                                                                                  
    #
    def getCount(self, run_id, dbCategory = None, minimal_laps = None):
        run_id_esc = str(run_id)                                       
        
        query = "SELECT COUNT(*) FROM(\
                    SELECT COUNT(times.id) from times"
        
        if(dstore.Get('rfid') == 2):
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
            
            

        
        
    