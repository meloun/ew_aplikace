# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import time
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
import pandas as pd 


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
        self.lap = TimesUtils.TimesLap()
        self.laptime = TimesUtils.TimesLaptime()
                                                           
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
            if(self.order.IsToShow(dbTime) == False):
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
            '''cas by mel existovat'''
            #if dstore.Get('timing_settings', "SET")["logic_mode"] != LOGIC_MODES.remote_manual:
            #    print "E: neexistuje cas!!! time id:", dbTime['start_nr'], ", Try refresh again."                            
            #self.calc_update_time(dbTime, tabTime['start_nr'])
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
        #z1 = time.clock()
        #@workaround: potrebuju lap pro poradi => lap.Get() nerezohlednuje ("additional_info")['lap']                
        aux_lap = self.lap.Get(dbTime)          
        if  dstore.Get("additional_info")['lap']:           
            tabTime['lap'] = aux_lap
        #print "- Lap takes: ",(time.clock() - z1)
        
        '''LAPTIMEs'''        
        tabTime['laptime'] = TimesUtils.TimesUtils.time2timestring(self.laptime.Get(dbTime))                
        tabTime['best_laptime'] = TimesUtils.TimesUtils.time2timestring(self.laptime.GetBest(dbTime))                                            
        
        '''ORDER'''                
        #z1 = time.clock()                                                        
        tabTime['order']  = self.order.Get(dbTime, aux_lap)        
        #print "- order takes: ",(time.clock() - z1)                                
                
        '''ORDER IN CATEGORY'''                                    
        #z1 = time.clock()                                
        tabTime['order_cat'] = self.order.Get(dbTime, aux_lap, category_id = joinUser['category_id'])
        #print "- order in category takes: ",(time.clock() - z1)    
                                                                                          
        #print "TIME take: ",(time.clock() - ztimeT)
        
        '''POINTS'''
        if (dstore.Get("additional_info")["enabled"] == 2):
            try:        
                tabTime['points'] = tablePoints.getPoints(tabTime, tablePoints.eTOTAL)        
                tabTime['points_cat'] = tablePoints.getPoints(tabTime, tablePoints.eCATEGORY)
            except:
                print "E: Points were not succesfully calculated for all times! Try refresh again."
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
                    print "rt", dbUser
                     
                    #update status                
                    #print "finishtime", dbUser 
                    db.update_from_dict(tableUsers.name, {'id': dbUser['id'], 'status': 'finished'})
                     
                
        
         
        return
        
        #end of test
            
    
    '''
    vrací dict, do kterého se pro keys vykopírují hodnoty (z time nebo user)   
    '''                       
    def tabRow2exportRow(self, tabRow, keys):                        
        exportRow = {}
        exportRowTimes = myModel.tabRow2exportRow(self, tabRow, keys)
        
        tabUserRow = tableUsers.getTabUserParNr(tabRow['nr'])
        exportRowUsers = tableUsers.model.tabRow2exportRow(tabUserRow, keys)
        
        #sloučení time a user
        exportRow = dict(exportRowUsers.items() + exportRowTimes.items())
        
        #print "exportRowTimes", exportRowTimes                        
        #print "exportRowUsers", exportRowUsers                        
            
        if u'order_cat_cat' in keys:
            exportRow['order_cat_cat'] = tabRow['order_cat']+"./"+tabRow['category']
        
        '''vracim dve pole, tim si drzim poradi(oproti slovniku)'''                        
        return exportRow             

#        if(mode == myModel.eTOTAL) or (mode == myModel.eGROUP):
#            exportHeader = [u"Pořadí", u"Číslo", u"Pořadí/Kategorie", u"Jméno"]                                                            
#            exportRow.append(tabRow['order']+".")
#            exportRow.append(tabRow['nr'])
#            exportRow.append(tabRow['order_cat']+"./"+tabRow['category'])            
#            exportRow.append(tabRow['name'])           
#        elif(mode == myModel.eCATEGORY):                                       
#            exportHeader = [u"Pořadí", u"Číslo", u"Jméno"]            
#            exportRow.append(tabRow['order_cat']+".")
#            exportRow.append(tabRow['nr'])
#            exportRow.append(tabRow['name'])           
#        elif(mode == myModel.eLAPS):                                                      
#            #header                                       
#            exportHeader = [u"Číslo", u"Jméno", u"1.Kolo", u"2.Kolo", u"3.Kolo",u"4.Kolo", u"5.Kolo", u"6.Kolo",u"7.Kolo", u"8.Kolo", u"9.Kolo", u"10.Kolo", u"11.Kolo", u"12.Kolo", u"13.Kolo", u"14.Kolo", u"15.Kolo",u"16.Kolo", u"17.Kolo", u"18.Kolo",u"19.Kolo", u"20.Kolo", u"21.Kolo", u"22.Kolo", u"23.Kolo", u"24.Kolo"]            
#            #row            
#            exportRow.append(tabRow[0]['nr'])
#            exportRow.append(tabRow[0]['name'])            
#            for t in tabRow:
#                #exportRow.append(t['time'])   # mezičasy - 2:03, 4:07, 6:09, ...        
#                exportRow.append(t['laptime']) # časy kol - 2:03, 2:04, 2:02, ... 
                            
#            #row a header musí mít stejnou délku     
#            for i in range(len(exportHeader) - len(tabRow) - 2):
#                exportRow.append("")                                                                       
             
                  
            
#        if(mode == myModel.eTOTAL) or (mode == myModel.eGROUP) or (mode == myModel.eCATEGORY):
#            if dstore.GetItem("export", ["year"]) == 2:
#                exportHeader.append(u"Ročník")
#                exportRow.append(tabUser['birthday'])
#            if dstore.GetItem("export", ["club"]) == 2:                                       
#                exportHeader.append(u"Klub")
#                exportRow.append(tabUser['club']) 
#            # user_field_1             
#            if dstore.GetItem("export", ["option_1"]) == 2:
#                exportHeader.append(dstore.GetItem("export", ["option_1_name"]))
#                exportRow.append(tabUser['o1'])
#            # user_field_2             
#            if dstore.GetItem("export", ["option_2"]) == 2:
#                exportHeader.append(dstore.GetItem("export", ["option_2_name"]))
#                exportRow.append(tabUser['o2'])
#            # user_field_3             
#            if dstore.GetItem("export", ["option_3"]) == 2:
#                exportHeader.append(dstore.GetItem("export", ["option_3_name"]))
#                exportRow.append(tabUser['o3'])
#            # user_field_4             
#            if dstore.GetItem("export", ["option_4"]) == 2:
#                exportHeader.append(dstore.GetItem("export", ["option_4_name"]))
#                exportRow.append(tabUser['o4'])
#            # laps             
#            if dstore.GetItem("export", ["laps"]) == 2:
#                exportHeader.append(u"Okruhy")
#                exportRow.append(tabRow['lap'])
#            # laptime             
#            if dstore.GetItem("export", ["laptime"]) == 2:
#                exportHeader.append(u'Čas kola')
#                exportRow.append(tabRow['laptime'])
#            # best laptime             
#            if dstore.GetItem("export", ["best_laptime"]) == 2:
#                exportHeader.append(u"Top okruh")
#                exportRow.append(tabRow['best_laptime'])
#            
#            #time
#            exportHeader.append(u"Čas")    
#            exportRow.append(tabRow['time'])
#            
#                                
#                            
#            #body - total, categories, groups
#            if(mode == myModel.eTOTAL) and (dstore.GetItem("export", ["points_race"]) == 2):
#                exportHeader.append(u"Body")                                    
#                exportRow.append(str(tabRow['points']))                
#            elif(mode == myModel.eCATEGORY) and (dstore.GetItem("export", ["points_categories"]) == 2):
#                exportHeader.append(u"Body")                                    
#                exportRow.append(str(tabRow['points_cat']))                 
#            elif(mode == myModel.eGROUP) and (dstore.GetItem("export", ["points_groups"]) == 2):
#                exportHeader.append(u"Body")                                    
#                exportRow.append(str(tabRow['points']))
#                
#        if exportRow == []:            
#            (exportHeader, exportRow) = myModel.tabRow2exportRow(self,tabRow, mode)                
        

    
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
        if self.lap.GetLaps(dbTime) >= dstore.Get('race_info')['limit_laps']:
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
    def  __init__(self):        
        
        #create table instance (slots, etc.)
        myTable.__init__(self, "Times")                
                
        #special slots
        #self.slots = Slots.TimesSlots(self)                                       
       
        #TIMERs
        #self.timer1s = QtCore.QTimer(); 
        #self.timer1s.start(1000);
        
        #MODE EDIT/REFRESH        
        self.system = 0
                
        
    def InitGui(self):
        myTable.InitGui(self)
        self.gui['export_www'] = Ui().TimesWwwExport         
        self.gui['recalculate'] = Ui().TimesRecalculate        
        self.gui['aDirectWwwExport'] = Ui().aDirectWwwExport
        self.gui['aDirectExportCategories'] = Ui().aDirectExportCategories 
        self.gui['aDirectExportLaptimes'] = Ui().aDirectExportLaptimes 
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
        
        #export direct categories        
        if (self.gui['aDirectExportCategories'] != None):                                   
            QtCore.QObject.connect(self.gui['aDirectExportCategories'], QtCore.SIGNAL("triggered()"), self.sExportResultsDirect)
                               
        QtCore.QObject.connect(self.gui['aDirectExportLaptimes'], QtCore.SIGNAL("triggered()"), self.sExportLaptimesDirect)
        
           
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
                 
    


                    
    
    def ExportMerge(self, rows, header, headerdata = ["",""]):
            aux_rows = rows[:]
            #aux_rows.insert(0, [dstore.Get('race_name'),] + (len(header)-1) * ["",])
            #aux_rows.insert(1, len(header)*["",])
            #aux_rows.insert(2, header)            
            aux_rows.insert(0, [headerdata[0],] + ["",]*(len(header)-2) + [headerdata[1],])
            aux_rows.insert(1, [dstore.Get('race_name'),] + (len(header)-1) * ["",])    
            aux_rows.insert(2, header)            
            return aux_rows
    def GetExportKeys(self, mode):            
            
        #"order", "nr", "order_cat", "name"
        keys = []
        if(mode == myModel.eTOTAL) or (mode == myModel.eGROUP):
            keys = ["order", "nr", "order_cat_cat", "name"]                                                                      
        elif(mode == myModel.eCATEGORY):                                       
            keys = ["order_cat", "nr", "name"]         
#        elif(mode == myModel.eLAPS):                                                      
#            #header                                       
#            exportHeader = [u"Číslo", u"Jméno", u"1.Kolo", u"2.Kolo", u"3.Kolo",u"4.Kolo", u"5.Kolo", u"6.Kolo",u"7.Kolo", u"8.Kolo", u"9.Kolo", u"10.Kolo", u"11.Kolo", u"12.Kolo", u"13.Kolo", u"14.Kolo", u"15.Kolo",u"16.Kolo", u"17.Kolo", u"18.Kolo",u"19.Kolo", u"20.Kolo", u"21.Kolo", u"22.Kolo", u"23.Kolo", u"24.Kolo"]            
#            #row            
#            exportRow.append(tabRow[0]['nr'])
#            exportRow.append(tabRow[0]['name'])            
#            for t in tabRow:
#                #exportRow.append(t['time'])   # mezičasy - 2:03, 4:07, 6:09, ...        
#                exportRow.append(t['laptime']) # časy kol - 2:03, 2:04, 2:02, ...
        
        # + "club", "sex", "lap", "time"
        if(mode == myModel.eTOTAL) or (mode == myModel.eGROUP) or (mode == myModel.eCATEGORY):
            if dstore.GetItem("export", ["year"]) == 2:                    
                keys.append("birthday")
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
            
#            #ztráta
#            if dstore.GetItem("export", ["gap"]) == 2:
#                exportHeader.append(u"Ztráta")
#                ztrata = ""            
#                if(self.winner != {} and tabRow['time']!=0 and tabRow['time']!=None):
#                    if self.winner['lap'] == tabRow['lap']:                
#                        ztrata = TimesUtils.TimesUtils.times_difference(tabRow['time'], self.winner['time'])
#                    elif tabRow['lap']!='' and tabRow['lap']!=None:
#                        ztrata = int(self.winner['lap']) - int(tabRow['lap'])                     
#                        if ztrata == 1:
#                            ztrata = str(ztrata) + " kolo"
#                        elif ztrata < 5:
#                            ztrata = str(ztrata) + " kola"
#                        else:
#                            ztrata = str(ztrata) + " kol"     
#                exportRow.append(ztrata)                                 
                            
            #body - total, categories, groups
            if(mode == myModel.eTOTAL) and (dstore.GetItem("export", ["points_race"]) == 2):                                                    
                keys.append('points')                
            elif(mode == myModel.eCATEGORY) and (dstore.GetItem("export", ["points_categories"]) == 2):                                                    
                keys.append('points_cat')                 
            elif(mode == myModel.eGROUP) and (dstore.GetItem("export", ["points_groups"]) == 2):                                                    
                keys.append('points')                                                                                                
        return keys
    #=======================================================================
    # SLOTS
    #=======================================================================
    
    # F11 - konečné výsledky, 1 čas na řádek
    def ExportToCsvFile(self, filename, category = None, group = None):

        if category != None:                     
            keys = self.GetExportKeys(myModel.eCATEGORY)
            header_strings = ["Kategorie: " + category['name'], category['description']] #second line, first and last item
        elif group != None:
            keys = self.GetExportKeys(myModel.eGROUP)
            header_strings = ["Skupina: " + group['name'], group['description']] #second line, first and last item
        else:
            keys = self.GetExportKeys(myModel.eTOTAL)
            header_strings = ["", ""] #second line, first and last item
        
        
        exportDf = pd.DataFrame(columns = keys) 
        for index, tabRow in self.proxy_model.df().iterrows():
            
            #print index, tabRow, type(tabRow)
            
            #category check
            if category != None:                
                if tabRow['category'] != category['name']:                    
                    continue
                
            #group check
            
                            
            dbTime = self.getDbRow(tabRow['id'])            
            if(dbTime['user_id'] == 0) or (dbTime['cell'] <= 1):
                continue
            
            #tabRow to exportRow           
            exportRow = self.model.tabRow2exportRow(tabRow, keys)
            
            if exportRow == None:
                continue
            
            exportDf = exportDf.append(exportRow, ignore_index = True)                                    

        #export header
        header_length = len(exportDf.columns)
        header_racename = [dstore.Get('race_name'),] + (header_length-1) * ['']
        header_param = [header_strings[0],]+ ((header_length-2) * ['',]) + [header_strings[1],]
        pd.DataFrame([header_racename, header_param]).to_csv("test.csv", ";", index = False, header = None)                
        
        #convert header EN => CZ
        exportDf.columns = ["a",] * header_length
        
        #export times (with collumn's names)
        exportDf.to_csv(filename, ";", mode="a", index = False)
        
        
    def sExportResultsDirect(self):
        
        ret = uiAccesories.showMessage("Results Export", "Choose format of results", MSGTYPE.question_dialog, "NOT finally results", "Finally results")        
                
        if ret == False: #cancel button
            return
                               
        #title
        #title = "Table '"+self.name + "' CSV Export Categories" 
        
        #get filename, gui dialog        
        dirname = utils.get_filename("export/"+timeutils.getUnderlinedDatetime()+"_"+dstore.Get('race_name')+"/")
        try:
            os.makedirs(dirname)
        except OSError:
            dirname = "export/"
                                         
        if(dirname == ""):
            return
        
        '''EXPORT TOTAL NEW'''
                
        winner = None
                
        #all times
        self.ExportToCsvFile("test.csv")
        
        #categories
        dbCategories = tableCategories.getDbRows()                      
        for dbCategory in dbCategories:
            self.ExportToCsvFile("test_"+dbCategory['name']+".csv", category = dbCategory)
 
        return 
                
        
        '''EXPORT TOTAL OLD'''        
        winner = None
        keys = self.GetExportKeys(myModel.eTOTAL)        
        for tabRow in self.proxy_model.dicts():                                               
        
            dbTime = self.getDbRow(tabRow['id'])            
            if(dbTime['user_id'] == 0) or (dbTime['cell'] <= 1):
                continue
            
            #tabRow to exportRow           
            exportRow = self.model.tabRow2exportRow(tabRow, keys)            
            exportRowList = [(exportRow[key]) for key in keys] #list, držím pořadí podle keys
            
            if exportRowList == None:
                continue
            
            #all times export - add all
            exportRows_Alltimes.append(exportRowList)             
            
            #times export - add last/best (race/slalom)                                                                                                                                       
            if self.model.order.IsToShow(dbTime) == True:                                                    
                exportRows.append(exportRowList)
            if tabRow['order'] == u'1':
                winner = tabRow                                        

        #add gap    
        if dstore.GetItem("export", ["gap"]) == 2:                       
            if ('lap' in keys) and ('time' in keys):                       
                for exportRow in exportRows:                    
                    time = exportRow[keys.index('time')] 
                    lap = exportRow[keys.index('lap')]            
                    gap = self.model.order.GetGap(lap, time, winner['lap'], winner['time'])     
                    exportRow.append(gap) 

                        
        '''write to csv file'''
        if(exportRows != []):
            #print "export total, ", len(exportRows),"times"
            exported["total"] =  len(exportRows)
            
            #header z property tabulky            
            headerT = [self.GetTableProperty(key, 'name_cz') for key in keys]
            headerU = [tableUsers.GetTableProperty(key, 'name_cz') for key in keys]
            header = [(a if a!=None else b) for a, b in zip(headerT, headerU)] #slouční headerů z times a users
            
            if 'order_cat_cat' in keys:
                header[keys.index('order_cat_cat')] = u"Pořadí/Kategorie"  
            
            #add gap to header
            if dstore.GetItem("export", ["gap"]) == 2:
                header.append(u"Ztráta")
                
            exportRows =  self.ExportMerge(exportRows, header)            
            filename = utils.get_filename("_"+dstore.Get('race_name')+".csv")            
            aux_csv = Db_csv.Db_csv(dirname+"/"+filename) #create csv class
            try:                
                aux_csv.save(exportRows)
            except IOError:
                uiAccesories.showMessage(self.name+" Export warning", "File "+dstore.Get('race_name')+".csv"+"\nPermission denied!")
                        
        '''Alltimes - write to csv file'''
        if(exportRows_Alltimes != []):
            #print "export total alltimes, ", len(exportRows_Alltimes),"times"
            exported["(at) total"] =  len(exportRows_Alltimes)                       
            exportRows_Alltimes =  self.ExportMerge(exportRows_Alltimes, keys)
            filename = utils.get_filename("at_"+dstore.Get('race_name')+".csv")            
            aux_csv = Db_csv.Db_csv(dirname+"/"+filename) #create csv class
            try:                
                aux_csv.save(exportRows_Alltimes)
            except IOError:
                uiAccesories.showMessage(self.name+" Export warning", "File "+dstore.Get('race_name')+".csv"+"\nPermission denied!")
                         
                                             
        '''EXPORT CATEGORIES'''
        winner = None
        keys = self.GetExportKeys(myModel.eCATEGORY)                        
        dbCategories = tableCategories.getDbRows()                      
        for dbCategory in dbCategories:
            exportRows = []             
            exportRows_Alltimes = []                                                 
            for tabRow in self.proxy_model.dicts():
                dbTime = self.getDbRow(tabRow['id'])
                
                if(dbTime['user_id'] == 0) or (dbTime['cell'] <= 1):
                    continue
                                            
                if (tabRow['category'] != dbCategory['name']):
                    continue
                                
                #
                exportRow = self.model.tabRow2exportRow(tabRow, keys)            
                exportRowList = [(exportRow[key]) for key in keys]
                if exportRowList == None:
                    continue
                
                #all times export - add all                
                exportRows_Alltimes.append(exportRowList)
            
                if self.model.order.IsToShow(dbTime) == True:                                                                                                                                                                                    
                    exportRows.append(exportRowList)
                if tabRow['order_cat'] == u'1':
                    winner = tabRow                                                                                                                                                                                                                    
            
            #add gap    
            if dstore.GetItem("export", ["gap"]) == 2:            
                if ('lap' in keys) and ('time' in keys):                                
                    for exportRow in exportRows:                    
                        time = exportRow[keys.index('time')] 
                        lap = exportRow[keys.index('lap')]            
                        gap = self.model.order.GetGap(lap, time, winner['lap'], winner['time'])     
                        exportRow.append(gap)             
            
            '''write to csv file'''
            if(exportRows != []):            
            
                exported["(c_) " + dbCategory['name']] = len(exportRows)                                                                     
                
                #header z property tabulky            
                headerT = [self.GetTableProperty(key, 'name_cz') for key in keys]
                headerU = [tableUsers.GetTableProperty(key, 'name_cz') for key in keys]
                header = [(a if a!=None else b) for a, b in zip(headerT, headerU)] #slouční headerů z times a users
                
                #add gap to header
                if dstore.GetItem("export", ["gap"]) == 2:
                    header.append(u"Ztráta") 
                                   
                exportRows =  self.ExportMerge(exportRows, header, ["Kategorie: "+dbCategory['name'], dbCategory['description']])                
                
                filename = utils.get_filename("c_"+dbCategory['name']+".csv")
                aux_csv = Db_csv.Db_csv(dirname+"/"+filename) #create csv class                
                try:                                                                                             
                    aux_csv.save(exportRows)
                except IOError:
                    uiAccesories.showMessage(self.name+" Export warning", "File "+filename+"\nPermission denied!")
                                                      
            '''Alltimes - write to csv file'''
            if(exportRows_Alltimes != []):                
                exported["(c_at_) " + dbCategory['name']] = len(exportRows_Alltimes)                                                     
                exportRows_Alltimes =  self.ExportMerge(exportRows_Alltimes, keys, ["Kategorie: "+dbCategory['name'], dbCategory['description']])               
                                
                filename = utils.get_filename("c_at_"+dbCategory['name']+".csv")
                aux_csv = Db_csv.Db_csv(dirname+"/"+filename) #create csv class                
                try:                                                                                             
                    aux_csv.save(exportRows_Alltimes)
                except IOError:
                    uiAccesories.showMessage(self.name+" Export warning", "File "+filename+"\nPermission denied!")                                  
                                   
                    
        '''EXPORT GROUPS'''
        winner = None
        keys = self.GetExportKeys(myModel.eCATEGORY)   
        dbCGroups = tableCGroups.getDbRows()
        dbCategories = tableCategories.getDbRows()                              
        #index_category = self.TABLE_COLLUMN_DEF["category"]["index"]                
        for dbCGroup in dbCGroups:                                              
            exportRows = []
            exportRows_Alltimes = []                                    
            for tabRow in self.proxy_model.dicts():
                dbTime = self.getDbRow(tabRow['id'])
                
                if(dbTime['user_id'] == 0) or (dbTime['cell'] <= 1):
                    continue

                tabCategory = tableCategories.getTabCategoryParName(tabRow['category'])
                if (tabCategory[dbCGroup['label']] != 1):
                    continue
                                            
                #all times export - add all
                exportRow = self.model.tabRow2exportRow(tabRow, keys)
                exportRowList = [(exportRow[key]) for key in keys]
                if exportRow == None:
                    continue
                
                #all times export - add all
                exportRows_Alltimes.append(exportRowList)             
                
                if(dstore.Get('evaluation')['order'] == OrderEvaluation.RACE and self.model.order.IsLastUsertime(dbTime)) or \
                    (dstore.Get('evaluation')['order'] == OrderEvaluation.SLALOM and self.model.order.IsBestUsertime(dbTime)):                    
                     
                    tabCategory = tableCategories.getTabCategoryParName(tabRow['category'])                 
                    if (tabCategory[dbCGroup['label']] == 1):                                                                                                                                                               
                        exportRows.append(exportRowList)
                                                                                                                                          

            
                    
            '''write to csv file'''
            if(exportRows != []):                
                exported["(g_) "+dbCGroup['label']] = len(exportRows)                
                
                #header z property tabulky
                #exportRows.insert(0, [dstore.Get('race_name'),time.strftime("%d.%m.%Y", time.localtime()), time.strftime("%H:%M:%S", time.localtime())])
                headerT = [self.GetTableProperty(key, 'name_cz') for key in keys]
                headerU = [tableUsers.GetTableProperty(key, 'name_cz') for key in keys]
                header = [(a if a!=None else b) for a, b in zip(headerT, headerU)] #slouční headerů z times a users
                
                                
                exportRows =  self.ExportMerge(exportRows, header, ["Skupina: "+dbCGroup['name'], dbCGroup['description']])                                                
                filename = utils.get_filename(dbCGroup['label']+"_"+dbCGroup['name']+".csv")
                aux_csv = Db_csv.Db_csv(dirname+"/"+filename) #create csv class                
                try:                                                                                             
                    aux_csv.save(exportRows)
                except IOError:
                    uiAccesories.showMessage(self.name+" Export warning", "File "+filename+"\nPermission denied!")
                    
            '''Alltimes - write to csv file'''
            if(exportRows_Alltimes != []):                
                exported["(g_at_) "+dbCGroup['label']] = len(exportRows_Alltimes)                                                
                exportRows_Alltimes =  self.ExportMerge(exportRows_Alltimes, header, ["Skupina: "+dbCGroup['name'], dbCGroup['description']])                                                
                filename = utils.get_filename(dbCGroup['label']+"_at_"+dbCGroup['name']+".csv")
                aux_csv = Db_csv.Db_csv(dirname+"/"+filename) #create csv class                
                try:                                                                                             
                    aux_csv.save(exportRows_Alltimes)
                except IOError:
                    uiAccesories.showMessage(self.name+" Export warning", "File "+filename+"\nPermission denied!")

        
        exported_string = ""
        for key in sorted(exported.keys()):
            exported_string += key + " : " + str(exported[key])+" times\n"        
        uiAccesories.showMessage(self.name+" Exported", exported_string, MSGTYPE.info)                                        
        return         

                
    def sExportLaptimesDirect(self):
        #get filename, gui dialog
        #title = "Table '"+self.params.name + "' CSV Export Laptimes"                 
        #dirname = self.params.myQFileDialog.getExistingDirectory(self.params.gui['view'], title)
        dirname = utils.get_filename("export/"+timeutils.getUnderlinedDatetime()+"_"+dstore.Get('race_name')+"_laptimes/")
        try:
            os.makedirs(dirname)
        except OSError:
            dirname = "export/"
                             
        if(dirname == ""):
            return  
        
        self.sExportLaptimesCategories(dirname)
        self.sExportLaptimesGroups(dirname)
        
    def sExportLaptimesCategories(self, dirname):            
                                  
        if(dirname == ""):
            return                
        
        '''LAPS PAR CATEGORY'''                        
        dbCategories = tableCategories.getDbRows()  
        tableRows = self.proxy_model.dicts()                            
        for dbCategory in dbCategories:
            """ 
            - přes všechny kategorie
                - přes každé číslo #loop A
                    - vyberu číslo/závodníka, jehož časy budou na novém řádku    #loop A1
                    - přes všechny časy, ukládám časy s tímto číslem (exportRow) #loop A2                    
                - všechny uložené časy transponuju do řádku (exportRow)
                - transponovaný řádek ukládám (exportRows)
            - řádky uložím do csv a jdu na další kategorii                                 
            """
            
            #rows for csv export 
            exportRows = []
            self.winner = {}
                                                                                                                                   
            for nr in range(len(tableRows)): #loop A                                                              
                '''pro každou kategorii přes všechny zbylé časy'''
                if(len(tableRows) == 0):                    
                    break                
                    
                exportRow = []
                
                #první číslo
                nr_user = None
                for t in tableRows: #loop A1
                    if (t['nr'] != None) and (int(t['nr']) != 0) and (t['category'] == dbCategory['name']):                 
                        nr_user = t['nr']                        
                        break #mam číslo
                                        
                if(nr_user == None):
                    break #no user for this category
                                
                
                '''mám číslo, hledám jeho další časy'''                    
                for i in range(len(tableRows)): #A2                                                                                 
                    if (tableRows[i]['category'] == dbCategory['name']) and (tableRows[i]['nr'] == nr_user):
                        exportRow.append(tableRows[i])                        
                                                
                '''pokud jsem našel exportuji a mažu z tabulky'''                
                if(exportRow != []):                    
                    for t in exportRow:
                        tableRows.remove(t)                         
                    exportRow = self.model.tabRow2exportRow(exportRow, Times.eLAPS)                    
                    exportRows.append(exportRow[1])
                    exportHeader = exportRow[0]
                    
            if(exportRows != []):
                print "Export: laps par category:", dbCategory['name'], ":", len(exportRows),"times"
                
                #srovnat podle čísla                
                from operator import itemgetter
                exportRows = sorted(exportRows, key = itemgetter(0))
                
                #save to csv file                
                exportRows.insert(0, ["Kategorie: "+dbCategory['name'],] + ["",]*(len(exportHeader)-2) + [dbCategory['description'],])
                exportRows.insert(1, [dstore.Get('race_name'),] + (len(exportHeader)-1) * ["",])
                exportRows.insert(2, exportHeader)    
                filename = utils.get_filename("c_laps_"+dbCategory['name']+".csv")
                aux_csv = Db_csv.Db_csv(dirname+"/"+filename) #create csv class                
                try:                                                                                             
                    aux_csv.save(exportRows)
                except IOError:
                    uiAccesories.showMessage(self.name+" Export warning", "File "+filename+"\nPermission denied!")
                                                         
        return  
    
    #GROUPS
    def sExportLaptimesGroups(self, dirname):
                             
        if(dirname == ""):
            return                      
        
        '''LAPS PAR GROUPS'''                        
        dbGroups = tableCGroups.getDbRows()  
        tableRows = self.proxy_model.dicts()                            
        for dbGroup in dbGroups:            
            """ 
            - přes všechny kategorie
                - přes každé číslo #loop A
                    - vyberu číslo/závodníka, jehož časy budou na novém řádku    #loop A1
                    - přes všechny časy, ukládám časy s tímto číslem (exportRow) #loop A2                    
                - všechny uložené časy transponuju do řádku (exportRow)
                - transponovaný řádek ukládám (exportRows)
            - řádky uložím do csv a jdu na další kategorii                                 
            """
            
            #rows for csv export 
            exportRows = []
            self.winner = {}
                                                                                                                                   
            for nr in range(len(tableRows)): #loop A                                                              
                '''pro každou kategorii přes všechny zbylé časy'''
                if(len(tableRows) == 0):                    
                    break                
                    
                exportRow = []
                              
                #první číslo
                nr_user = None
                for t in tableRows: #loop A1
                    
                    dbTime = self.getDbRow(t['id'])
                    if(dbTime['user_id'] == 0) or (dbTime['cell'] <= 1):                        
                        continue
                    
                    if (t['nr'] == None) or (int(t['nr']) == 0):                        
                        continue
                    
                    tabCategory = tableCategories.getTabCategoryParName(t['category'])
                    if (tabCategory[dbGroup['label']] != 1):                        
                        continue
                    
                    #mam číslo                                  
                    nr_user = t['nr']                                                                
                    break 
                                        
                if(nr_user == None):                    
                    break #no user for this group
                                
                
                '''mám číslo, hledám jeho další časy'''
                for tabRow in tableRows: #A2
                    tabCategory = tableCategories.getTabCategoryParName(tabRow['category'])
                    if (tabCategory[dbGroup['label']] != 1):                        
                        continue
                                                                                                     
                    if(tabRow['nr'] != nr_user):                        
                        continue
                   
                    #add row
                    exportRow.append(tabRow) 
                        
                                            
                #for i in range(len(tableRows)): #A2                                                                                 
                #    if (tableRows[i]['category'] == dbGroup['name']) and (tableRows[i]['nr'] == nr_user):
                #        exportRow.append(tableRows[i])                        
                                                
                '''pokud jsem našel exportuji a mažu z tabulky'''                
                if(exportRow != []):                    
                    for t in exportRow:
                        tableRows.remove(t)                         
                    exportRow = self.model.tabRow2exportRow(exportRow, Times.eLAPS)                    
                    exportRows.append(exportRow[1])
                    exportHeader = exportRow[0]
                    
            if(exportRows != []):
                print "Export: laps par group:", dbGroup['name'], ":", len(exportRows),"times"
                
                #srovnat podle čísla                
                #from operator import itemgetter
                #exportRows = sorted(exportRows, key = itemgetter(0))
                
                #save to csv file                
                exportRows.insert(0, ["Skupina: "+dbGroup['name'],] + ["",]*(len(exportHeader)-2) + [dbGroup['description'],])
                exportRows.insert(1, [dstore.Get('race_name'),] + (len(exportHeader)-1) * ["",])
                exportRows.insert(2, exportHeader)    
                filename = utils.get_filename("g_laps_"+dbGroup['name']+".csv")
                aux_csv = Db_csv.Db_csv(dirname+"/"+filename) #create csv class                
                try:                                                                                             
                    aux_csv.save(exportRows)
                except IOError:
                    uiAccesories.showMessage(self.name+" Export warning", "File "+filename+"\nPermission denied!")
                                                         
        return  
        
        
        
        

                               
                    
    #toDo: sloucit s myModel konstruktorem        
    def Update(self, run_id = None):
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
            
            

        
        
    