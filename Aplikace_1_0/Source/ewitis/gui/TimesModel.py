# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui, Qt
from libs.myqt import gui
import ewitis.gui.myModel as myModel
import ewitis.gui.UsersModel as UsersModel
import libs.db_csv.db_csv as Db_csv
import ewitis.gui.TimesUtils as TimesUtils
import ewitis.gui.DEF_COLUMN as DEF_COLUMN
from ewitis.data.DEF_DATA import *
import ewitis.gui.TimesSlots as Slots
import libs.utils.utils as utils
import time

'''
F5 - refresh
F6 - export table
F7 - export WWW
F11 - export categories 
F12 - direct WWW export
'''
class TimesParameters(myModel.myParameters):
    
    def __init__(self, source):
                
        #table and db table name
        self.name = "Times"         
        
        #TABLE
        self.tabUser = source.U        
        self.tabCategories = source.C
        self.tabCGroups = source.CG 
                
        
        #=======================================================================
        # KEYS
        #=======================================================================        
        self.DB_COLLUMN_DEF = DEF_COLUMN.TIMES['database']

        
        #toDo: rozlisit podle mode z datastore
        #self.TABLE_COLLUMN_DEF = DEF_COLUMN.TIMES['table_training']                                               
        self.TABLE_COLLUMN_DEF  = DEF_COLUMN.TIMES['table_race']
        
        self.EXPORT_COLLUMN_DEF  = DEF_COLUMN.TIMES['table_race']        
        
        #create MODEL and his structure
        myModel.myParameters.__init__(self, source)  
                      
                                
        #=======================================================================
        # GUI
        #=======================================================================
        self.gui = {} 
        #VIEW
        self.gui['view'] = source.ui.TimesProxyView
        
        #FILTER
        self.gui['filter'] = source.ui.TimesFilterLineEdit
        self.gui['filterclear'] = source.ui.TimesFilterClear
        
        #GROUPBOX
        self.gui['add'] = source.ui.TimesAdd
        self.gui['remove'] =  source.ui.TimesRemove
        self.gui['export'] = source.ui.TimesExport
        self.gui['export_www'] = source.ui.TimesWwwExport
        self.gui['import'] = None 
        self.gui['recalculate'] = source.ui.TimesRecalculate
        self.gui['delete'] = source.ui.TimesDelete
        self.gui['aDirectWwwExport'] = source.ui.aDirectWwwExport
        self.gui['aDirectExportCategories'] = source.ui.aDirectExportCategories 
        self.gui['aDirectExportLaptimes'] = source.ui.aDirectExportLaptimes 
        
        #SPECIAL
        #self.gui['show_all'] = source.ui.TimesShowAll
        #self.gui['show_zero'] = source.ui.timesShowZero
        #self.gui['show_additional_info'] = source.ui.timesAdditionalInfo
        
        #COUNTER
        self.gui['counter'] = source.ui.timesCounter
        
        #self.gui['add'].setEnabled = False
        
        #=======================================================================
        # classes
        #=======================================================================        
        self.classModel = TimesModel                              
        self.classProxyModel = TimesProxyModel
        
        
        
class TimesModel(myModel.myModel):
    def __init__(self, params):                        
                
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)
                    
        #add utils function
        #self.utils = TimesUtils.TimesUtils()
        
        #
        self.starts = TimesUtils.TimesStarts(self.params.db)
        self.order = TimesUtils.TimesOrder(self.params.db, self.params.datastore)
        self.lap = TimesUtils.TimesLap(self.params.db, self.params.datastore)
        self.laptime = TimesUtils.TimesLaptime(self.params.db, self.params.datastore)
                                                           
        #update with first run        
        first_run = self.params.db.getFirst("runs")
        if(first_run != None):
            self.run_id = first_run['id']
        else:
            self.run_id = 0 #no times for run_id = 0 
                                
                   
    #setting flags for this model
    #first collumn is NOT editable
    def flags(self, index): 
        
        #id, name, category, addres NOT editable

        if ((index.column() == 4) or (index.column() == 5) or (index.column() == 6)):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

        return myModel.myModel.flags(self, index)
    
    def getDefaultTableRow(self): 
        row = myModel.myModel.getDefaultTableRow(self)
        row['cell'] = 1                  
        row['nr'] = 0 #musi byt cislo!                    
        row['time_raw'] = 0
        row['start_nr'] = 1               
        return row                 

    
    def db2tableRow(self, dbTime):
        """    
        ["id", "nr", "cell", "time", "name", "category", "address"]
        """
        
        #ztimeT = time.clock()
        #print "TIME", dbTime['id']                                
        
        if(self.params.datastore.Get('show')['times_with_order'] == 2):
            if(self.order.IsToShow(dbTime) == False):
                return None
                                             
        '''hide all zero time?'''                    
        if(self.params.datastore.Get('show')['starttimes'] == False):                            
            if (dbTime["cell"] == 1):                
                return None                      
        
        ''' 1to1 KEYS '''           
        tabTime = myModel.myModel.db2tableRow(self, dbTime)
         
        ''' get USER
            - user_id je id v tabulce Users(bunky) nebo tag_id(rfid) '''
        '''Test: vzal jsem rovnou tabusera, zda se to ze to chodi'''                                            
        tabUser =  self.params.tabUser.getTabUserParIdOrTagId(dbTime["user_id"])         
        #dbUser =  self.params.tabUser.getDbUserParIdOrTagId(dbTime["user_id"])        
       
        
        ''' get CATEGORY'''            
        tabCategory =  self.params.tabCategories.getTabRow(tabUser['category_id'])                                
        #tabCategory =  None                                
                                        
        ''' OTHER KEYS ''' 
        
        '''NR'''                   
        tabTime['nr'] = tabUser['nr']
                                    
        '''START NR'''
        if(tabTime['cell'] == 1) or (tabTime['nr']==0) or tabCategory==None: #start time?                           
            tabTime['start_nr'] = 1 #decrement 1.starttime
        else:                                
            tabTime['start_nr'] = tabCategory['start_nr']        
        
        '''TIME
            dbtime 2 tabletime'''                                               
        
        '''raw time'''        
        tabTime['timeraw'] = TimesUtils.TimesUtils.time2timestring(dbTime['time_raw'])
        
        '''time'''
        if(dbTime['time'] == None):
            '''cas by mel existovat'''
            print "E: neexistuje cas!!!", dbTime                            
            #self.calc_update_time(dbTime, tabTime['start_nr'])
        else:                        
            tabTime['time'] = TimesUtils.TimesUtils.time2timestring(dbTime['time'])            
                
        '''NAME'''        
        if(dbTime['cell'] == 1):
            tabTime['name'] = ''
        elif(dbTime["user_id"] == 0):
            tabTime['name'] = 'undefined'
        else:                       
            tabTime['name'] = tabUser['name'].upper() +' '+tabUser['first_name']        
        
        '''CATEGORY'''                                                                                
        tabTime['category'] = tabUser['category']                                                                                                                              

             
        tabTime['lap'] = None
        tabTime['order'] = None
        tabTime['order_cat'] = None       
        
        '''LAP'''
        #z1 = time.clock()
        #@workaround: potrebuju lap pro poradi => lap.Get() nerezohlednuje ("additional_info")['lap']                
        aux_lap = self.lap.Get(dbTime)          
        if  self.params.datastore.Get("additional_info")['lap']:           
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
        tabTime['order_cat'] = self.order.Get(dbTime, aux_lap, category_id = tabUser['category_id'])
        #print "- order in category takes: ",(time.clock() - z1)    
                                                                                          
        #print "TIME take: ",(time.clock() - ztimeT)
        return tabTime
                                                                                   
    def sModelChanged(self, item):
                
        if(self.params.datastore.Get("user_actions") == 0):                              
        
            #print "radek",item.row()
            tabRow = self.row_dict(item.row())
                    
            if(item.column() == self.params.TABLE_COLLUMN_DEF['nr']['index']):
               
                '''ZMĚNA ČÍSLA'''
                '''přiřazení uživatele nelze u času                
                   - startovací buňky
                   - nulového času'''                                  
                
                if(int(tabRow['cell']) == 1):                            
                    self.params.showmessage(self.params.name+" Update error", "Cannot assign user to start time!")
                    self.update()       
                    return 
#                elif(tabRow['time'] == '00:00:00,00'):
#                   self.params.showmessage(self.params.name+" Update error", "Cannot assign user to zero time!")
#                   self.update()
#                   return
                                                   
                
        
        myModel.myModel.sModelChanged(self, item)
  

                
    def table2dbRow(self, tabTime, item = None): 
                                            
        #get selected id
        #try:                     
        #    rows = self.params.gui['view'].selectionModel().selectedRows()                        
        #    id = self.proxy_model.data(rows[0]).toString()
        #except:
        #    self.params.showmessage(self.params.name+" Delete error", "Cant be deleted")
            
        #1to1 keys, just copy        
        dbTime = myModel.myModel.table2dbRow(self, tabTime, item)
                
        '''RUN_ID'''
        #if(self.showall):
        if(self.params.datastore.Get('show')['alltimes'] == 2):
            '''get time['run_id'] from DB, , in showall-mode i dont know what run is it'''            
            aux_dbtime = self.params.db.getParId("times",tabTime['id'])            
            dbTime['run_id'] = aux_dbtime['run_id']            
        else:
            dbTime['run_id'] = self.run_id
                        
        '''first start time? => cant be updated
            toDo:asi by za určitých okolností měl jít'''       
#        if(int(tabTime['id']) == (self.utils.getFirstStartTime(dbTime['run_id'])['id'])):
#            self.params.showmessage(self.params.name+" Update error", "First start time cant be updated!")
#            return None        
        
        '''USER NR => USER ID'''                        
        if(int(tabTime['nr']) == 0):
            dbTime['user_id'] = 0                     
        else:                                                
            ''' get DB-USER'''
            dbUser = self.params.tabUser.getDbUserParNr(tabTime['nr'])                                                      
            if(dbUser == None):
                self.params.showmessage(self.params.name+" Update error", "Cant find user with nr. "+ tabTime['nr'])                
                return None
                                      
            '''get DB-CATEGORY'''             
            dbCategory = self.params.tabCategories.getDbRow(dbUser['category_id'])
            if(dbCategory == None):
                self.params.showmessage(self.params.name+" Update error", "Cant find category for this user.")                
                return None
            
            '''při změně čísla nejsou v tabTime správné user údaje'''
            '''toDo:sloučit name a first name'''
            #tabTime['category'] = dbCategory['name']
            #tabTime['name'] = dbUser['name'] +' ' + dbUser['first_name']                        
            
            '''TEST if is here enought START-TIMES'''                        
            nr_start = dbCategory['start_nr']            
            try:                                
                aux_start_time = self.starts.Get(dbTime['run_id'], nr_start)
            except IndexError:                        
                self.params.showmessage(self.params.name+": Update error", str(nr_start)+".th start-time is necessary for users from this category!")
                return None
            except:
                self.params.showmessage(self.params.name+": Update error", "Cant find start time for this category.")
                return None
                
            ''' get user id'''
            dbTime['user_id'] = self.params.tabUser.getIdOrTagIdParNr(tabTime['nr'])            
                        
            if(dbTime['user_id'] == None):
                '''user not found => nothing to save'''
                self.params.showmessage(self.params.name+": Update error", "No user or tag with number "+str(tabTime['nr'])+"!")
                return None
            
            #in onelap race user can have ONLY 1 TIME
            if(self.params.datastore.Get('onelap_race') == True):
                if(self.lap.GetLaps(dbTime) != 0):
                    self.params.showmessage(self.params.name+": Update error", "This user has already time!")
                    return None 
                            
        ''' TIME '''                                                            
        #try:                                                         
        #dbTime['time_raw'] = self.utils.tabtime2dbtime(dbTime['run_id'], tabTime)                        
               
        '''get start-time'''        
        if(tabTime['cell'] == 1):                            
            #toDo: je tohle nutné? start_time se nikde nepoužije
            try:                                         
                start_time = self.starts.GetFirst(dbTime['run_id'])
            except (TypeError,KeyError):            
                start_time = self.starts.GetDefault()                
        else:
            '''čas může být v tabulce None, třeba pokud nemá všechny startovací běhy k dispozici
                   potom se čas naupdatuje, nechává se současný v databázi'''
            '''toDo: nevracet string ale pravou hodnotu z getTableRow'''
            if(tabTime['time'] != None) and (tabTime['time'] != u''):
                
                ''' z categories vezmu start_nr a pak jdu do start-times pro start-time'''                
                tabUser = self.params.tabUser.getTabUserParNr(tabTime['nr'])                            
                category = self.params.tabCategories.getDbCategoryParName(tabUser['category'])                
                try:                                        
                    start_time = self.starts.Get(dbTime['run_id'], category['start_nr'])                    
                except TypeError:
                    '''žádný startovací čas => vezmi default (1.čas vůbec)'''                    
                    start_time = self.starts.GetFirst(dbTime['run_id']) 
                                
                '''table-time => db-time'''
                try:
                                        
                    if(item.column() == self.params.TABLE_COLLUMN_DEF['time']['index']):
                        '''změna času=>změna času v db'''             
                        dbTime['time_raw'] = TimesUtils.TimesUtils.timestring2time(tabTime['time']) + start_time['time_raw']
                    
                    '''počítaný čas se vždy maže a spočte se při updatu znova'''    
                    dbTime['time'] = None
                    
                except TimesUtils.TimeFormat_Error:
                    self.params.showmessage(self.params.name+" Update error", "Wrong Time format!")                
                
            
        
        '''nelze přiřadit číslo nulovému/zápornému času'''
        #&if(dbTime['time_raw'] == 0)                                                                                          
                                            
        #except TimesUtils.TimeFormat_Error:
        #    self.params.showmessage(self.params.name+" Update error", "Time wrong format!")             
        

                                                                                                                                                                                                                                                                                                                             
        return dbTime    
        

    def update_laptime(self, dbTime):
        
        if(dbTime['laptime'] == None):            
                                    
            '''vypocet spravneho casu a ulozeni do databaze pro pristi pouziti'''                                                           
            laptime = self.laptime.Get(dbTime)                                            
             
            if laptime != None:                                                        
                '''ulozeni do db'''
                #print "Times: update laptime, id:", dbTime['id'],"time:",laptime            
                dbTime['laptime'] = laptime                                                       
                self.params.db.update_from_dict(self.params.name, dbTime) #commit v update()
    def update_laptimes(self):
        """
        u časů kde 'time'=None, do počítá time z time_raw a startovacího časů pomocí funkce calc_update_time()
        
        *Ret:*
            pole čísel závodníků u kterých se nepodařilo časy updatovat   
        """
        ret_ko_times = []
        
        dbTimes = self.params.db.getAll(self.params.name)
        dbTimes = self.params.db.cursor2dicts(dbTimes)
        
        for dbTime in dbTimes:
            
            '''time'''
            if(dbTime['laptime'] == None):                                                                        
                '''vypocet spravneho casu a ulozeni do databaze pro pristi pouziti'''
                
                try:                                    
                    self.update_laptime(dbTime)
                except:                    
                    ret_ko_times.append(dbTime['id'])
                           
        return ret_ko_times
                                                       
    def calc_update_time(self, dbTime, start_nr = None):
        
        if(dbTime['time'] == None):            
                                    
            '''vypocet spravneho casu a ulozeni do databaze pro pristi pouziti'''
            try:
                '''toDo: misto try catch, Get bude vracet None'''                                   
                start_time = self.starts.Get(dbTime['run_id'], start_nr)                                
            except:                         
                print "E: Times: no startime nr.",start_nr,", for time", dbTime 
                aux_rawtime = None
                start_time = None
                                                    
            '''odecteni startovaciho casu a ulozeni do db'''
            #print dbTime['time_raw']
            dbTime['time'] = dbTime['time_raw'] - start_time['time_raw']                                                       
            self.params.db.update_from_dict(self.params.name, dbTime) #commit v update()                                           
            
                
    def calc_update_times(self):
        """
        u časů kde 'time'=None, do počítá time z time_raw a startovacího časů pomocí funkce calc_update_time()
        
        *Ret:*
            pole časů u kterých se nepodařilo časy updatovat   
        """
        ret_ko_times = []
        
        dbTimes = self.params.db.getAll(self.params.name)
        dbTimes = self.params.db.cursor2dicts(dbTimes)
        
        for dbTime in dbTimes:
            
            '''time'''
            if(dbTime['time'] == None):
            
                ''' get USER'''            
                tabUser =  self.params.tabUser.getTabUserParIdOrTagId(dbTime["user_id"])
                ''' get CATEGORY'''            
                tabCategory =  self.params.tabCategories.getTabRow(tabUser['category_id'])                                
                                            
                '''START NR'''
                if(dbTime['cell'] == 1) or (tabUser['nr']==0): #start time?                           
                    start_nr = 1 #decrement 1.starttime
                else:                                
                    start_nr = tabCategory['start_nr']        
                                                        
                '''vypocet spravneho casu a ulozeni do databaze pro pristi pouziti'''
                try:                
                    self.calc_update_time(dbTime, start_nr)
                except:
                    ret_ko_times.append(dbTime['id'])
                           
        return ret_ko_times
    
    #UPDATE TABLE        
    def update(self, run_id = None):                  
        
        #print self.params.name+": model update (t)"
        
        if(run_id != None):                    
            self.run_id = run_id #update run_id
            
        #update start times        
        self.starts.Update()        
        
        ko_nrs = self.calc_update_times()
        if(ko_nrs != []):
            print "E:",self.params.name+" Update error", "Some times have no start times, ids: "+str(ko_nrs)
            
        ko_nrs = self.update_laptimes()        
        if(ko_nrs != []):
            print "E:",self.params.name+" Update error", "Some laptimes can not be updated"+str(ko_nrs)
            
        self.params.db.commit()
            
        
        
        #update times        
        if self.params.datastore.Get('show')['alltimes'] == 2:                        
            #get run ids
            conditions = []
            ids = self.params.tabRuns.proxy_model.ids()
                                            
            #create list of lists, [["id",2],["id",6],..]
            for id in ids:
                conditions.append(['run_id', id])                                                      
                                         
            #update all times             
            myModel.myModel.update(self, conditions = conditions, operation = 'OR')            
        else:            
            #update for selected run        
            #myModel.myModel.update(self, "run_id", self.run_id)            
            myModel.myModel.update(self, "run_id", self.run_id)
        #self.params.db.commit()            
                                                                                       

class TimesProxyModel(myModel.myProxyModel):
    def __init__(self, params):                        
        
        #create PROXYMODEL
        myModel.myProxyModel.__init__(self, params)
        
    def IsColumnAutoEditable(self, column):
        if column == 1:
            '''změna čísla'''    
            return True
        return False
           
                  
   
# view <- proxymodel <- model 
class Times(myModel.myTable):    
    def  __init__(self, params):        
        
        #create table instance (slots, etc.)
        myModel.myTable.__init__(self, params)                
                
        #special slots
        #self.slots = Slots.TimesSlots(self)                                       
       
        #TIMERs
        #self.timer1s = QtCore.QTimer(); 
        #self.timer1s.start(1000);
        
        #MODE EDIT/REFRESH        
        self.system = 0
        
        self.winner = {}
        
    def createSlots(self):
        
        #standart slots
        myModel.myTable.createSlots(self)
        
        
        #button Recalculate
        QtCore.QObject.connect(self.params.gui['recalculate'], QtCore.SIGNAL("clicked()"), lambda:self.sRecalculate(self.model.run_id))
         
        #export direct www
        QtCore.QObject.connect(self.params.gui['aDirectWwwExport'], QtCore.SIGNAL("triggered()"), self.sExport_directWWW)
        
        #export direct categories        
        if (self.params.gui['aDirectExportCategories'] != None):                                   
            QtCore.QObject.connect(self.params.gui['aDirectExportCategories'], QtCore.SIGNAL("triggered()"), lambda:self.sExportCategoriesDirect('col_nr_export'))
                               
        QtCore.QObject.connect(self.params.gui['aDirectExportLaptimes'], QtCore.SIGNAL("triggered()"), self.sExportLaptimesDirect)
        
                                
   
    def sRecalculate(self, run_id):
        print "A: Times: Recalculating.. run id:", run_id
        query = \
                " UPDATE times" +\
                    " SET time = Null, laptime = Null" +\
                    " WHERE (times.cell != 1 ) AND (times.time != 0) AND (times.run_id = \""+str(run_id)+"\")"
                        
        res = self.params.db.query(query)
                        
        self.params.db.commit()
        print "A: Times: Recalculating.. press F5 to finish"
        return res
                 
    ''''''                   
    def tabRow2exportRow(self, tabRow, mode):                        
                                                           
        exportRow = []
        exportHeader = []
        
        #save the winner
        #print "1:",tabRow
        if 'order' in tabRow:
            if(tabRow['order'] != ''):
                if ((mode == Times.eTOTAL) and (int(tabRow['order']) == 1)) or \
                    ((mode == Times.eCATEGORY) and (int(tabRow['order_cat']) == 1)):
                    self.winner = tabRow                    
            
        #print "tabRow: ", tabRow['id'], ":", tabRow['order']
        '''get user'''
        if(mode == Times.eTOTAL) or (mode == Times.eGROUP) or (mode == Times.eCATEGORY):
            tabHeader = self.params.tabUser.proxy_model.header()                                                  
            tabUser = self.params.tabUser.getTabUserParNr(tabRow['nr'])
        
        if(mode == Times.eTOTAL) or (mode == Times.eGROUP):
            exportHeader = [u"Pořadí", u"Číslo", u"Kategorie", u"Jméno", u"Ročník", u"Klub"]                        
            #exportHeader = [u"Pořadí", u"Číslo", u"Kategorie", u"Jméno", u"Klub"]                        
            exportRow.append(tabRow['order']+".")
            exportRow.append(tabRow['nr'])
            exportRow.append(tabRow['order_cat']+"./"+tabRow['category'])            
            exportRow.append(tabRow['name'])
            exportRow.append(tabUser['birthday'])                                       
            exportRow.append(tabUser['club'])            
        elif(mode == Times.eCATEGORY):                                       
            exportHeader = [u"Pořadí", u"Číslo", u"Jméno", u"Ročník", u"Klub"]
            #exportHeader = [u"Pořadí", u"Číslo",  u"Jméno", u"Klub"]
            exportRow.append(tabRow['order_cat']+".")
            exportRow.append(tabRow['nr'])
            exportRow.append(tabRow['name'])
            exportRow.append(tabUser['birthday'])                                       
            exportRow.append(tabUser['club'])            
        elif(mode == Times.eLAPS):                                                      
            #header                                       
            exportHeader = [u"Číslo", u"Jméno", u"1.Kolo", u"2.Kolo", u"3.Kolo",u"4.Kolo", u"5.Kolo", u"6.Kolo",u"7.Kolo", u"8.Kolo", u"9.Kolo", u"10.Kolo", u"11.Kolo", u"12.Kolo", u"13.Kolo", u"14.Kolo", u"15.Kolo",u"16.Kolo", u"17.Kolo", u"18.Kolo",u"19.Kolo", u"20.Kolo", u"21.Kolo", u"22.Kolo", u"23.Kolo", u"24.Kolo"]            
            #row            
            exportRow.append(tabRow[0]['nr'])
            exportRow.append(tabRow[0]['name'])            
            for t in tabRow:
                #exportRow.append(t['time'])   # mezičasy - 2:03, 4:07, 6:09, ...        
                exportRow.append(t['laptime']) # časy kol - 2:03, 2:04, 2:02, ... 
                            
            #row a header musí mít stejnou délku     
            for i in range(len(exportHeader) - len(tabRow) - 2):
                exportRow.append("")                                                                       
        
            
        if(mode == Times.eTOTAL) or (mode == Times.eGROUP) or (mode == Times.eCATEGORY):
            # user_field_1             
            if self.params.datastore.GetItem("export", ["option_1"]) == 2:
                exportHeader.append(self.params.datastore.GetItem("export", ["option_1_name"]))
                exportRow.append(tabUser['o1'])
            # user_field_2             
            if self.params.datastore.GetItem("export", ["option_2"]) == 2:
                exportHeader.append(self.params.datastore.GetItem("export", ["option_2_name"]))
                exportRow.append(tabUser['o2'])
            # user_field_3             
            if self.params.datastore.GetItem("export", ["option_3"]) == 2:
                exportHeader.append(self.params.datastore.GetItem("export", ["option_3_name"]))
                exportRow.append(tabUser['o3'])
            # user_field_4             
            if self.params.datastore.GetItem("export", ["option_4"]) == 2:
                exportHeader.append(self.params.datastore.GetItem("export", ["option_4_name"]))
                exportRow.append(tabUser['o4'])
            # laps             
            if self.params.datastore.GetItem("export", ["laps"]) == 2:
                exportHeader.append(u"Okruhy")
                exportRow.append(tabRow['lap'])
            # best laptime             
            if self.params.datastore.GetItem("export", ["best_laptime"]) == 2:
                exportHeader.append(u"Top okruh")
                exportRow.append(tabRow['best_laptime'])
            
            #time
            exportHeader.append(u"Čas")    
            exportRow.append(tabRow['time'])
            
#            #ztráta
#            exportHeader.append(u"Ztráta")
#            ztrata = ""            
#            if(self.winner != {} and tabRow['time']!=0 and tabRow['time']!=None):
#                if self.winner['lap'] == tabRow['lap']:                
#                    ztrata = TimesUtils.TimesUtils.times_difference(tabRow['time'], self.winner['time'])
#                elif tabRow['lap']!='' and tabRow['lap']!=None:
#                    ztrata = int(self.winner['lap']) - int(tabRow['lap'])                     
#                    if ztrata == 1:
#                        ztrata = str(ztrata) + " kolo"
#                    elif ztrata < 5:
#                        ztrata = str(ztrata) + " kola"
#                    else:
#                        ztrata = str(ztrata) + " kol"     
#            exportRow.append(ztrata)
            
            
#                        t['ztráta'] =  self.timeutils.times_difference(t['time'], exportRows[0]['time'])
#                        print "čas", t['ztráta']
#                    else:
#                        t['ztráta'] = t['time'] - exportRows[0]['lap']
#                        print "lap", t['ztráta']          
                            
            #body
            #exportHeader.append(u"Body")    
            #exportRow.append("")                
                
        
        '''vracim dve pole, tim si drzim poradi(oproti slovniku)'''
        #print "exportRow: ", exportRow
        #print "2:",exportRow                         
        return (exportHeader, exportRow)

                    
    #=======================================================================
    # SLOTS
    #=======================================================================
    def sExportCategoriesDirect(self, col_nr_export):                       
        #title
        title = "Table '"+self.params.name + "' CSV Export Categories" 
        
        #get filename, gui dialog 
        #dirname = QtGui.QFileDialog.getExistingDirectory(self.params.gui['view'], title)
        dirname = self.params.myQFileDialog.getExistingDirectory(self.params.gui['view'], title)                 
        if(dirname == ""):
            return              

        exportRows = []
        self.winner = {}        

        '''EXPORT TOTAL'''                                       
        for tabRow in self.proxy_model.dicts():
            dbTime = self.getDbRow(tabRow['id'])
            #d print "id:", tabRow['id'],
            
            if(dbTime['user_id'] == 0) or (dbTime['cell'] <= 1):
                continue
                        
            #if(self.model.order.IsLastUsertime(dbTime)):
            if(self.params.datastore.Get('order_evaluation') == OrderEvaluation.RACE and self.model.order.IsLastUsertime(dbTime)) or \
                    (self.params.datastore.Get('order_evaluation') == OrderEvaluation.SLALOM and self.model.order.IsBestUsertime(dbTime)):
                #d print ": yes"                                    
                exportRow = self.tabRow2exportRow(tabRow, Times.eTOTAL)                                                                                                                                       
                exportRows.append(exportRow[1])
                exportHeader = exportRow[0]
            #else:
                #d print ": no" 
                    
            
        '''natvrdo pred girem'''        
        #exportHeader = ["Pořadí", "Pořadí K", "Kategorie" , "Číslo", "Jméno", "Ročník", "Klub", "Čas"]  
            
        '''write to csv file'''
        if(exportRows != []):
            print "export total, ", len(exportRows),"times"                        
            exportRows.insert(0, [self.params.datastore.Get('race_name'),] + (len(exportHeader)-1) * ["",])
            exportRows.insert(1, len(exportHeader)*["",])
            exportRows.insert(2, exportHeader)
            filename = utils.get_filename("_"+self.params.datastore.Get('race_name')+".csv")            
            aux_csv = Db_csv.Db_csv(dirname+"/"+filename) #create csv class
            try:
                aux_csv.save(exportRows)
            except IOError:
                self.params.showmessage(self.params.name+" Export warning", "File "+self.params.datastore.Get('race_name')+".csv"+"\nPermission denied!")
                                             
        '''EXPORT CATEGORIES'''                        
        dbCategories = self.params.tabCategories.getDbRows()                      
        for dbCategory in dbCategories:
            exportRows = []
            self.winner = {}                                     
            for tabRow in self.proxy_model.dicts():
                dbTime = self.getDbRow(tabRow['id'])
                
                if(dbTime['user_id'] == 0) or (dbTime['cell'] <= 1):
                    continue
                                            
                if(self.params.datastore.Get('order_evaluation') == OrderEvaluation.RACE and self.model.order.IsLastUsertime(dbTime)) or \
                    (self.params.datastore.Get('order_evaluation') == OrderEvaluation.SLALOM and self.model.order.IsBestUsertime(dbTime)):  
                    if (tabRow['category'] == dbCategory['name']):
                        exportRow = self.tabRow2exportRow(tabRow, Times.eCATEGORY)                                                                                                                                       
                        exportRows.append(exportRow[1])
                        exportHeader = exportRow[0]                                                                                                                                                                                           
                        
            
            '''write to csv file'''
            if(exportRows != []):
                print "export category", dbCategory['name'], ":",len(exportRows),"times"                                                     
                exportRows.insert(0, ["Kategorie: "+dbCategory['name'],] + ["",]*(len(exportHeader)-2) + [dbCategory['description'],])
                exportRows.insert(1, [self.params.datastore.Get('race_name'),] + (len(exportHeader)-1) * ["",])
                exportRows.insert(2, exportHeader)
                filename = utils.get_filename("c_"+dbCategory['name']+".csv")
                aux_csv = Db_csv.Db_csv(dirname+"/"+filename) #create csv class                
                try:                                                                                             
                    aux_csv.save(exportRows)
                except IOError:
                    self.params.showmessage(self.params.name+" Export warning", "File "+filename+"\nPermission denied!")                                  
                                   
                    
        '''EXPORT GROUPS'''
        dbCGroups = self.params.tabCGroups.getDbRows()
                              
        index_category = self.params.TABLE_COLLUMN_DEF["category"]["index"]                
        dbCategories = self.params.tabCategories.getDbRows()
        for dbCGroup in dbCGroups:                                              
            exportRows = []
            self.winner = {}                        
            for tabRow in self.proxy_model.dicts():
                dbTime = self.getDbRow(tabRow['id'])
                
                if(dbTime['user_id'] == 0) or (dbTime['cell'] <= 1):
                    continue
                            
                if(self.params.datastore.Get('order_evaluation') == OrderEvaluation.RACE and self.model.order.IsLastUsertime(dbTime)) or \
                    (self.params.datastore.Get('order_evaluation') == OrderEvaluation.SLALOM and self.model.order.IsBestUsertime(dbTime)):                    
                     
                    tabCategory = self.params.tabCategories.getTabCategoryParName(tabRow['category'])                 
                    if (tabCategory[dbCGroup['label']] == 1):
                        exportRow = self.tabRow2exportRow(tabRow, Times.eGROUP)                                                                                                                                       
                        exportRows.append(exportRow[1])
                        exportHeader = exportRow[0]                                                                                                                  

            
                    
            '''write to csv file'''
            if(exportRows != []):
                print "export cgroups", dbCGroup['label'], ":",len(exportRows),"times"                
                #exportRows.insert(0, [self.params.datastore.Get('race_name'),time.strftime("%d.%m.%Y", time.localtime()), time.strftime("%H:%M:%S", time.localtime())])
                
                exportRows.insert(0, ["Skupina: "+dbCGroup['name'],] + ["",]*(len(exportHeader)-2) + [dbCGroup['description'],])
                exportRows.insert(1, [self.params.datastore.Get('race_name'),] + (len(exportHeader)-1) * ["",])
                exportRows.insert(2, exportHeader)                                                
                filename = utils.get_filename(dbCGroup['label']+"_"+dbCGroup['name']+".csv")
                aux_csv = Db_csv.Db_csv(dirname+"/"+filename) #create csv class                
                try:                                                                                             
                    aux_csv.save(exportRows)
                except IOError:
                    self.params.showmessage(self.params.name+" Export warning", "File "+filename+"\nPermission denied!")
                                        
        return         
                                                                                                                 
                
    def sExportLaptimesDirect(self):
                
        #title        
        title = "Table '"+self.params.name + "' CSV Export Laptimes" 
        
        #get filename, gui dialog 
        #dirname = QtGui.QFileDialog.getExistingDirectory(self.params.gui['view'], title)
        dirname = self.params.myQFileDialog.getExistingDirectory(self.params.gui['view'], title)                 
        if(dirname == ""):
            return                      
        
        '''LAPS PAR CATEGORY'''                        
        dbCategories = self.params.tabCategories.getDbRows()  
        tableRows = self.proxy_model.dicts()                            
        for dbCategory in dbCategories:
            """ 
            - přes všechny kategorie
                - přes každé čísla #loop A
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
                    exportRow = self.tabRow2exportRow(exportRow, Times.eLAPS)                    
                    exportRows.append(exportRow[1])
                    exportHeader = exportRow[0]
                    
            if(exportRows != []):
                print "Export: laps par category:", dbCategory['name'], ":", len(exportRows),"times"
                
                #srovnat podle čísla                
                from operator import itemgetter
                exportRows = sorted(exportRows, key = itemgetter(0))
                
                #save to csv file                
                exportRows.insert(0, ["Kategorie: "+dbCategory['name'],] + ["",]*(len(exportHeader)-2) + [dbCategory['description'],])
                exportRows.insert(1, [self.params.datastore.Get('race_name'),] + (len(exportHeader)-1) * ["",])
                exportRows.insert(2, exportHeader)    
                filename = utils.get_filename("c_l_"+dbCategory['name']+".csv")
                aux_csv = Db_csv.Db_csv(dirname+"/"+filename) #create csv class                
                try:                                                                                             
                    aux_csv.save(exportRows)
                except IOError:
                    self.params.showmessage(self.params.name+" Export warning", "File "+filename+"\nPermission denied!")
                                                         
        return  
        
        
        
        
    def sExport(self):                      
        import os        
        
        col_nr_export = 'col_nr_export_raw'
        
        '''get filename, gui dialog, save path to datastore'''        
        filename =  self.params.myQFileDialog.getSaveFileName(self.params.gui['view'],"Export table "+self.params.name+" to CSV","dir_export_csv","Csv Files (*.csv)", self.params.name+".csv") 
                                 
        if(filename == ""):
            return                            

        title = "Table '"+self.params.name + "' CSV Export Categories" 
        exportRows = []        

        '''EXPORT ALL TIMES'''                                                        
        for tabRow in self.proxy_model.dicts():
            exportRow = self.tabRow2exportRow(tabRow, Times.eTOTAL)[1]                                    
            if exportRow != []:                            
                exportRows.append(exportRow)
            exportHeader = self.tabRow2exportRow(tabRow, Times.eTOTAL)[0]                                        
             
        '''write to csv file'''
        if(exportRows != []):
            print "export race", self.params.datastore.Get('race_name'), ":",len(exportRows),"times"
            first_header = [self.params.datastore.Get('race_name'), time.strftime("%d.%m.%Y", time.localtime()), time.strftime("%H:%M:%S", time.localtime())]
            exportRows.insert(0, exportHeader)
            aux_csv = Db_csv.Db_csv(filename) #create csv class
            try:                                     
                aux_csv.save(exportRows)
            except IOError:
                self.params.showmessage(self.params.name+" Export warning", "Permission denied!")
                               
                    
    #toDo: sloucit s myModel konstruktorem        
    def update(self, run_id = None):
        ztime = time.clock()                      
        self.model.update(run_id = run_id)                        
        print "I: Times: update:",time.clock() - ztime,"s"
        #myModel.myTable.update(self)
        self.setColumnWidth()
        self.updateTabCounter()
        self.updateDbCounter()
            

    # REMOVE ROW      
    # first starttime cant be deleted          
    def sDelete(self):        
        
        #get selected id
        try:                     
            rows = self.params.gui['view'].selectionModel().selectedRows()                        
            id = self.proxy_model.data(rows[0]).toString()
        except:
            self.params.showmessage(self.params.name+" Delete error", "Cant be deleted")
            return
            
        #first start time? => cant be updated               
        #if(int(id) == (self.model.utils.getFirstStartTime(self.model.run_id)['id'])):
        if(int(id) == (self.model.starts.GetFirst(self.model.run_id)['id'])):
            self.params.showmessage(self.params.name+" Delete warning", "First start time cant be deleted!")
            return  
        
        #delete run with additional message
        myModel.myTable.sDelete(self)                                                         
        
                                    
                                                                                            
    

            
            

        
        
    