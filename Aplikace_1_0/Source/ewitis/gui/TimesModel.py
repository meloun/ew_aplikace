# -*- coding: utf-8 -*-s
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
        self.gui['delete'] = source.ui.TimesDelete
        self.gui['aDirectWwwExport'] = source.ui.aDirectWwwExport
        self.gui['aDirectExportCategories'] = source.ui.aDirectExportCategories 
        
        #SPECIAL
        self.gui['show_all'] = source.ui.TimesShowAll
        self.gui['show_zero'] = source.ui.timesShowZero
        self.gui['show_additional_info'] = source.ui.timesAdditionalInfo
        
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
        
                        
        self.showall = False
        self.showzero = True
                                        
        
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

        #ztime = time.clock()
        #print "Z:", ztime                                     
        '''hide all zero time?'''
        if(self.showzero == False):
            if (int(dbTime["cell"])==1):                
                return None                      
        
        ''' 1to1 KEYS '''           
        tabTime = myModel.myModel.db2tableRow(self, dbTime)
         
        ''' get USER
            - user_id je id v tabulce Users(bunky) nebo tag_id(rfid) '''
        '''Test: vzal jsem rovnou tabusera, zda se to ze to chodi'''                                            
        tabUser =  self.params.tabUser.getTabUserParIdOrTagId(dbTime["user_id"])
        #print "M1:", (time.clock()-ztime)*1000         
        #dbUser =  self.params.tabUser.getDbUserParIdOrTagId(dbTime["user_id"])
        #print "K:", (time.clock()-ztime) * 1000        
       
        
        ''' get CATEGORY'''            
        tabCategory =  self.params.tabCategories.getTabRow(tabUser['category_id'])                                
                                        
        ''' OTHER KEYS ''' 
        
        '''NR'''                   
        tabTime['nr'] = tabUser['nr']
                                    
        '''START NR'''
        if(tabTime['cell'] == 1) or (tabTime['nr']==0): #start time?                           
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

        '''LAP'''        
        tabTime['lap'] = self.lap.Get(dbTime)
        
        '''ORDER'''                        
        lasttime = self.order.IsLastUsertime(dbTime, tabTime['lap'])        
        #print "last: ", lasttime, tabTime['lap'], dbTime
        
        if(lasttime == True):                                
            tabTime['order']  = self.order.Get(dbTime, tabTime['lap'])
        else:
            tabTime['order']  = ""            
                
        '''ORDER IN CATEGORY'''
        if(lasttime == True):                        
            #z1 = time.clock()                       
            tabTime['order_cat'] = self.order.Get(dbTime, tabTime['lap'], category_id = tabUser['category_id'])
            #print (time.clock() - z1)
        else:
            tabTime['order_cat']  = ""
        
        '''GAP'''
        tabTime['gap'] = ""
        #print start_time
        #try:         
        #dbRow = self.params.db.getParId("Times", start_time['id']+1)
        #print dbRow
            #tabTime['gap'] = aux_rawtime - dbRow['time']
        #except TypeError:
        #    pass
            
        
        #'''ORDER'''        
        #tabTime['order']  = self.order.Get2(tabTime, tabTime['lap'])                                         
                    
        return tabTime
                                                                                   
    def slot_ModelChanged(self, item):
                
        if(self.params.datastore.Get("user_actions")):                              
        
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
                                                   
                
        
        myModel.myModel.slot_ModelChanged(self, item)
  

                
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
        if(self.showall):
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
#                if(self.utils.start_times==None):
#                    start_time = {id:0, 'time_raw':0}
#                elif not(dbTime['run_id'] in self.utils.start_times):
#                    start_time = {id:0, 'time_raw':0}
#                else:
#                    #start_time = self.utils.start_times[dbTime['run_id']][0]
#                    start_time = self.starts.GetFirst(dbTime['run_id'])
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
        

    def calc_update_time(self, dbTime, start_nr = None):
        
        if(dbTime['time'] == None):            
                                    
            '''vypocet spravneho casu a ulozeni do databaze pro pristi pouziti'''
            try:
                '''toDo: misto try catch, Get bude vracet None'''                                   
                start_time = self.starts.Get(dbTime['run_id'], start_nr)                                
            except:                         
                print "E:neexistuje startime"
                aux_rawtime = None
                start_time = None
                                                    
            '''odecteni startovaciho casu a ulozeni do db'''
            #print dbTime['time_raw']
            dbTime['time'] = dbTime['time_raw'] - start_time['time_raw']                                                       
            self.params.db.update_from_dict(self.params.name, dbTime) #commit v update()                                           
            
                
    def calc_update_times(self):
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
                self.calc_update_time(dbTime, start_nr)
            
               
             
    #UPDATE TABLE        
    def update(self, run_id = None):                  
        
        if(run_id != None):                    
            self.run_id = run_id #update run_id
            
        #update start times        
        self.starts.Update()        
        
        self.calc_update_times()
        
        #update times
        if(self.showall):
            
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
        self.params.db.commit()            
                                                                                       

class TimesProxyModel(myModel.myProxyModel):
    def __init__(self, params):                        
        
        #create PROXYMODEL
        myModel.myProxyModel.__init__(self, params)
        QtCore.QObject.connect(self, QtCore.SIGNAL("dataChanged(const QModelIndex&,const QModelIndex&)"), self.slot_ModelChanged)   
        
    #setting flags for this model
    #first collumn is NOT editable
    def flags(self, index):             

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable        
        
                
    def slot_ModelChanged(self,  topLeft, bottomRight):
        if(self.params.datastore.Get("user_actions")):                  
            if(topLeft == bottomRight):
            
                '''změna jednoho prvku'''
                
                if(topLeft.column() == 1):                    
                
                    '''ZMĚNA ČÍSLA'''

                    '''editovat číslo o jeden řádek výše'''                        
                    myindex = self.index(topLeft.row()-1,1)                    
                    if(myindex.isValid()==True):                        
                        self.params.gui['view'].edit(myindex)                    
   
# view <- proxymodel <- model 
class Times(myModel.myTable):    
    def  __init__(self, params):        
        
        #create table instance (slots, etc.)
        myModel.myTable.__init__(self, params)                
                
        #special slots
        self.slots = Slots.TimesSlots(self)                                       
       
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(1000);
        
        #MODE EDIT/REFRESH        
        self.system = 0
        
    def createSlots(self):
        
        #standart slots
        myModel.myTable.createSlots(self)
        
        # EXPORT WWW BUTTON        
        if (self.params.gui['aDirectExportCategories'] != None):            
            QtCore.QObject.connect(self.params.gui['aDirectExportCategories'], QtCore.SIGNAL("triggered()"), lambda:self.sExportCategoriesDirect('col_nr_export'))                   

            
    ''''''
    def tabRow2exportRow(self, tabRow, mode):        
                                                           
        exportRow = []
        exportHeader = []
        
        '''get user'''
        tabHeader = self.params.tabUser.proxy_model.header()                                                  
        tabUser = self.params.tabUser.getTabUserParNr(tabRow['nr']) 
        
        if(mode == Times.eTOTAL) or (mode == Times.eGROUP):
            exportHeader = [u"Pořadí", u"Číslo", u"Kategorie", u"Jméno", u"Ročník", u"Klub", u"Čas"]
            exportRow.append(tabRow['order']+".")
            exportRow.append(tabRow['nr'])
            exportRow.append(tabRow['order_cat']+"./"+tabRow['category'])            
            exportRow.append(tabRow['name'])
            exportRow.append(tabUser['birthday'])                                       
            exportRow.append(tabUser['club'])
            exportRow.append(tabRow['time'])
        elif(mode == Times.eCATEGORY):                                       
            exportHeader = [u"Pořadí", u"Číslo", u"Jméno", u"Ročník", u"Klub", u"Čas"]
            exportRow.append(tabRow['order_cat']+".")
            exportRow.append(tabRow['nr'])
            exportRow.append(tabRow['name'])
            exportRow.append(tabUser['birthday'])                                       
            exportRow.append(tabUser['club'])
            exportRow.append(tabRow['time'])
                        
        exportHeader.append(u"Okruhy")
        exportRow.append(tabRow['lap'])
        
        '''vracim dve pole, tim si drzim poradi(oproti slovniku)'''                         
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

        '''EXPORT TOTAL'''                                       
        for tabRow in self.proxy_model.dicts():
            dbTime = self.getDbRow(tabRow['id'])            
            if(self.model.order.IsLastUsertime(dbTime, tabRow['lap'])):                                   
                exportRow = self.tabRow2exportRow(tabRow, Times.eTOTAL)                                                                                                                                       
                exportRows.append(exportRow[1])
                exportHeader = exportRow[0] 
                    
            
        '''natvrdo pred girem'''        
        #exportHeader = ["Pořadí", "Pořadí K", "Kategorie" , "Číslo", "Jméno", "Ročník", "Klub", "Čas"]  
            
        '''write to csv file'''
        if(exportRows != []):                        
            exportRows.insert(0, [self.params.datastore.Get('race_name'),"","","","","","",""])
            exportRows.insert(1, ["","","","","","","",""])
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
            for tabRow in self.proxy_model.dicts():
                dbTime = self.getDbRow(tabRow['id'])            
                if(self.model.order.IsLastUsertime(dbTime, tabRow['lap'])): 
                    if (tabRow['category'] == dbCategory['name']):
                        exportRow = self.tabRow2exportRow(tabRow, Times.eCATEGORY)                                                                                                                                       
                        exportRows.append(exportRow[1])
                        exportHeader = exportRow[0]                                                                             
                        
            
            '''write to csv file'''
            if(exportRows != []):
                print "export category", dbCategory['name'], ":",len(exportRows),"times"
                first_header = ["Kategorie: "+dbCategory['name'],"","","","","",dbCategory['description']]                
                exportRows.insert(0, [self.params.datastore.Get('race_name'),"","","","","",""])
                exportRows.insert(1, first_header)
                exportRows.insert(2, exportHeader)
                filename = utils.get_filename("c_"+dbCategory['name']+".csv")
                aux_csv = Db_csv.Db_csv(dirname+"/"+filename) #create csv class                
                try:                                                                                             
                    aux_csv.save(exportRows)
                except IOError:
                    self.params.showmessage(self.params.name+" Export warning", "File "+dbCategory['name']+".csv"+"\nPermission denied!")
                    
        '''EXPORT GROUPS'''
        dbCGroups = self.params.tabCGroups.getDbRows()
                              
        index_category = self.params.TABLE_COLLUMN_DEF["category"]["index"]                
        dbCategories = self.params.tabCategories.getDbRows()                      
        for dbCGroup in dbCGroups:            
            exportRows = []                        
            for tabRow in self.proxy_model.dicts():
                dbTime = self.getDbRow(tabRow['id'])            
                if(self.model.order.IsLastUsertime(dbTime, tabRow['lap'])): 
                    tabCategory = self.params.tabCategories.getTabCategoryParName(tabRow['category'])                 
                    if (tabCategory[dbCGroup['label']] == 1):
                        exportRow = self.tabRow2exportRow(tabRow, Times.eGROUP)                                                                                                                                       
                        exportRows.append(exportRow[1])
                        exportHeader = exportRow[0]                                                                                                                  

            
                    
            '''write to csv file'''
            if(exportRows != []):
                print "export cgroups", dbCGroup['label'], ":",len(exportRows),"times"
                first_header = ["Skupina: "+dbCGroup['label'],"","","","",dbCGroup['description']]
                #exportRows.insert(0, [self.params.datastore.Get('race_name'),time.strftime("%d.%m.%Y", time.localtime()), time.strftime("%H:%M:%S", time.localtime())])
                exportRows.insert(0, [self.params.datastore.Get('race_name'),"","","","",""])
                exportRows.insert(1, first_header)
                exportRows.insert(2, exportHeader)                                                
                filename = utils.get_filename(dbCGroup['label']+"_"+dbCGroup['name']+".csv")
                aux_csv = Db_csv.Db_csv(dirname+"/"+filename) #create csv class                
                try:                                                                                             
                    aux_csv.save(exportRows)
                except IOError:
                    self.params.showmessage(self.params.name+" Export warning", "File "+dbCGroup['label']+"_"+dbCGroup['name']+".csv"+"\nPermission denied!")  
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
        #myModel.myTable.update(self)
        self.setColumnWidth()
        self.update_counter()
        print "Times: update",time.clock() - ztime
            

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
        
                                    
                                                                                            
    

            
            

        
        
    