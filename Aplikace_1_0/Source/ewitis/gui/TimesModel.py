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
        self.utils = TimesUtils.TimesUtils(self)
        
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
                                
                
    def ssTimesShowAllChanged(self, state):
        print "wrong"
        
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
        
        #print "TIME DB2TABLEROW START", time.time()            
        '''hide all zero time?'''
        if(self.showzero == False):
            if (int(dbTime["cell"])==1):                
                return None                      
        
        ''' 1to1 KEYS '''           
        tabTime = myModel.myModel.db2tableRow(self, dbTime)
         
        ''' get USER
            - user_id je id v tabulce Users(bunky) nebo tag_id(rfid) '''
        '''toDo: proč neberu tabUSera rovnou?'''                                            
        dbUser =  self.params.tabUser.getDbUserParIdOrTagId(dbTime["user_id"])        
        if(dbUser == None):
            dbUser = {}
            dbUser['id'] = 0
            dbUser['category_id'] = 0        
        tabUser = self.params.tabUser.getTabRow(dbUser["id"])
        #print "..2", time.time()
        
        ''' get CATEGORY'''               
        tabCategory =  self.params.tabCategories.getTabRow(dbUser['category_id'])                                
                                        
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
        aux_rawtime = dbTime['time_raw']

        '''get start-time for this run'''        
        try:
            '''toDo: misto try catch, Get bude vracet None'''                                   
            start_time = self.starts.Get(dbTime['run_id'], tabTime['start_nr'])
        except:                         
            print "E:neexistuje startime"
            aux_rawtime = None
            start_time = None                
                        
        '''time = time_raw - starttime'''        
        if tabTime['start_nr'] and start_time:
            tabTime['time'] = self.utils.timeraw2timestring(aux_rawtime, start_time['time_raw'])
        else:
            print "e: dbtime2tabtime"
            tabTime['time'] = None
            aux_rawtime = None           
                
        '''NAME'''        
        if(dbTime['cell'] == 1):
            tabTime['name'] = ''
        elif(dbTime["user_id"] == 0):
            tabTime['name'] = 'undefined'
        else:           
            tabTime['name'] = tabUser['name'] +' '+tabUser['first_name']        
        
        '''CATEGORY'''                                                                                
        tabTime['category'] = tabUser['category']                                                              
                        
        '''ORDER'''        
        tabTime['order']  = self.order.Get(tabTime)
                
        '''ORDER IN CATEGORY'''        
        #tabTime['order_kat'] = self.order.Get(dbTime, category=tabTime['category'])        
        tabTime['order_kat'] = self.order.Get(dbTime, category=dbUser['category_id'])

        '''LAP'''        
        tabTime['lap'] = self.lap.Get(dbTime)
        
        '''GAP'''
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
        
            tabRow = self.getTableRow(item.row())
                    
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

                
    def table2dbRow(self, tabTime): 
                                            
        #get selected id
        #try:                     
        #    rows = self.params.gui['view'].selectionModel().selectedRows()                        
        #    id = self.proxy_model.data(rows[0]).toString()
        #except:
        #    self.params.showmessage(self.params.name+" Delete error", "Cant be deleted")
            
        #1to1 keys, just copy        
        dbTime = myModel.myModel.table2dbRow(self, tabTime)
                
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
                self.params.showmessage(self.params.name+" Update error", str(nr_start)+".th start-time is necessary for users from this category!")
                return None
            except:
                self.params.showmessage(self.params.name+" Update error", "Cant find start time for this category.")
                return None
                
            ''' get user id'''
            dbTime['user_id'] = self.params.tabUser.getIdOrTagIdParNr(tabTime['nr'])            
                        
            if(dbTime['user_id'] == None):
                '''user not found => nothing to save'''
                self.params.showmessage(self.params.name+" Update error", "No user or tag with number "+str(tabTime['nr'])+"!")
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
                
                ''' z categories vezmu start_nr a pak do start-times pro start-time
                    při změně čísla se počítá se starou kategorii a časem, ale nevadí to'''                            
                category = self.params.tabCategories.getDbCategoryParName(tabTime['category'])                
                try:                    
                    start_time = self.starts.Get(dbTime['run_id'], category['start_nr']) 
                except TypeError:
                    '''žádný startovací čas => vezmi default (1.čas vůbec)'''                    
                    start_time = self.starts.GetFirst(dbTime['run_id']) 
                                
                '''table-time => db-time'''
                try:
                    dbTime['time_raw'] = self.utils.timestring2timeraw(tabTime['time'], start_time['time_raw'])
                except TimesUtils.TimeFormat_Error:
                    self.params.showmessage(self.params.name+" Update error", "Wrong Time format!")                
                
            
        
        '''nelze přiřadit číslo nulovému/zápornému času'''
        #&if(dbTime['time_raw'] == 0)                                                                                          
                                            
        #except TimesUtils.TimeFormat_Error:
        #    self.params.showmessage(self.params.name+" Update error", "Time wrong format!")             
                                                                                                                                                                                                                                                                                                                             
        return dbTime    
        
    
    #UPDATE TABLE        
    def update(self, run_id = None):                
        
        if(run_id != None):                    
            self.run_id = run_id #update run_id
            
        #update start times
        #self.utils.updateStartTimes()
        self.starts.Update()        
        
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
            myModel.myModel.update(self, "run_id", self.run_id)            
                                                                                       

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
#    def  __init__(self, view, db, guidata):  
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
    def tabRow2exportRow(self, tabRow, col_nr_export):        
                                                           
        exportRow = []
        exportHeader = []                                       
                            
        '''TIME part'''
        tabHeader = self.proxy_model.header()
        for collumn_key in self.params.TABLE_COLLUMN_DEF.keys():
            collumn = self.params.TABLE_COLLUMN_DEF[collumn_key]
            if(collumn[col_nr_export] is not None):                                
                
                '''pokud mezera, vložit prozatím prázdné prvky'''                            
                if((len(exportRow))<=collumn[col_nr_export]):
                    exportRow = exportRow + ([''] * (collumn[col_nr_export] - len(exportRow)+1))
                    exportHeader = exportHeader + ([''] * (collumn[col_nr_export] - len(exportHeader)+1))                                

                '''restrict'''
                if(collumn_key == 'order_kat'):
                    tabRow[collumn_key] = tabRow[collumn_key]+'.'
                                        
                '''add collumn to export'''                
                exportRow[collumn[col_nr_export]] = tabRow[collumn_key]
                exportHeader[collumn[col_nr_export]] = tabHeader[collumn['index']]
                #print exportRow[collumn[col_nr_export]], type(exportRow[collumn[col_nr_export]])                               
                
        #print "time part",exportRow
                 
        '''USER part'''
        tabHeader = self.params.tabUser.proxy_model.header()                                                  
        tabUser = self.params.tabUser.getTabUserParNr(tabRow['nr'])        
        for collumn_key in self.params.tabUser.params.TABLE_COLLUMN_DEF.keys():            
            collumn = self.params.tabUser.params.TABLE_COLLUMN_DEF[collumn_key]
            if(collumn[col_nr_export] is not None):                                
                
                '''pokud mezera, vložit prozatím prázdné prvky''' 
                if((len(exportRow))<=collumn[col_nr_export]):
                    exportRow = exportRow + ([''] * (collumn[col_nr_export] - len(exportRow)+1))
                    exportHeader = exportHeader + ([''] * (collumn[col_nr_export] - len(exportHeader)+1))
                    
                #add collumn to export
                if(tabUser is not None):                    
                    exportRow[collumn[col_nr_export]] = tabUser[collumn_key]
                
                exportHeader[collumn[col_nr_export]] = tabHeader[collumn['index']]
                if(exportHeader[collumn[col_nr_export]] == 'id'):
                    exportHeader[collumn[col_nr_export]] = 'user_id'
                         
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

        '''export all'''                                       
        for tabRow in self.proxy_model.dicts():
            exportRow = self.tabRow2exportRow(tabRow, col_nr_export)[1]
            if exportRow != []:                            
                exportRows.append(exportRow)
            #exportHeader = self.tabRow2exportRow(tabRow, col_nr_export)[0]
            #print "exportHeader",exportHeader
            
        '''natvrdo pred girem'''
        exportHeader = ["pořadí", "číslo", "jméno", "klub", "ročník", "čas"]  
            
        '''write to csv file'''
        if(exportRows != []):
            #print "export race", self.params.datastore.Get('race_name'), ":",len(exportRows),"times"
            first_header = [self.params.datastore.Get('race_name'), time.strftime("%d.%m.%Y", time.localtime()), time.strftime("%H:%M:%S", time.localtime())]
            exportRows.insert(0, exportHeader)
            aux_csv = Db_csv.Db_csv(dirname+"/"+self.params.datastore.Get('race_name')+".csv") #create csv class
            aux_csv.save(exportRows, keys = first_header)
                                             
        '''export categories'''
        index_category = self.params.TABLE_COLLUMN_DEF["category"]["index"]                
        dbCategories = self.params.tabCategories.getDbRows()                      
        for dbCategory in dbCategories:
            exportRows = []                        
            for tabRow in self.proxy_model.dicts():
                if (tabRow['category'] == dbCategory['name']):                                                                                               
                    exportRows.append(self.tabRow2exportRow(tabRow, col_nr_export)[1])                    
                    #exportHeader = self.tabRow2exportRow(tabRow)[0]                                             
            
            '''natvrdo pred girem'''
            #exportHeader = ["Pořadí", "Číslo", "Jméno", "Ročník", "Klub", "Čas", "Ztráta"]    
            exportHeader = ["Pořadí", "Číslo", "Jméno", "Ročník", "Klub", "Čas"]    
            
            '''write to csv file'''
            if(exportRows != []):
                print "export category", dbCategory['name'], ":",len(exportRows),"times"
                first_header = ["Kategorie:"+dbCategory['name'],"","","","",dbCategory['description']]
                #exportRows.insert(0, [self.params.datastore.Get('race_name'),time.strftime("%d.%m.%Y", time.localtime()), time.strftime("%H:%M:%S", time.localtime())])
                exportRows.insert(0, [self.params.datastore.Get('race_name'),])
                exportRows.insert(1, first_header)
                exportRows.insert(2, exportHeader)
                aux_csv = Db_csv.Db_csv(dirname+"/"+dbCategory['name']+".csv") #create csv class
                #aux_csv.save(exportRows, keys = first_header)
                try:                                                                                             
                    aux_csv.save(exportRows)
                except IOError:
                    self.params.showmessage(self.params.name+" Export warning", "File "+dbCategory['name']+".csv"+"\nPermission denied!")
                                                                                                                 
        return                                                                                                                   
                

    def sExport(self):                      
        import os        
        
        col_nr_export = 'col_nr_export_raw'
        
        #get filename, gui dialog        
        #filename = QtGui.QFileDialog.getSaveFileName(self.params.gui['view'],"Export table "+self.params.name+" to CSV",self.params.datastore.Get("dir_export_csv")+"/"+self.params.name+".csv","Csv Files (*.csv)")
        #filename =  self.params.myQFileDialog.getSaveFileName(self.params.gui['view'],"Export table "+self.params.name+" to CSV",self.params.datastore.Get("dir_export_csv")+"/"+self.params.name+".csv","Csv Files (*.csv)")
        filename = self.params.myQFileDialog.getSaveFileName(self.params.gui['view'],"Export table "+self.params.name+" to CSV","dir_export_csv","Csv Files (*.csv)", self.params.name+".csv") 
                         
        #print "FF1",filename
        if(filename == ""):
            return
        #CurrentDir = QtCore.QDir()
        #self.params.datastore.Set("dir_export_csv", os.path.dirname(str(CurrentDir.absoluteFilePath(filename))))
        #print "FF2",filename

                       

        title = "Table '"+self.params.name + "' CSV Export Categories" 
        exportRows = []        

        #EXPORT ALL TIMES                                            
        for tabRow in self.proxy_model.dicts():
            exportRow = self.tabRow2exportRow(tabRow, col_nr_export)[1]
            #print "tabRow ",tabRow
            #print "exportRow ",exportRow            
            if exportRow != []:                            
                exportRows.append(exportRow)
            exportHeader = self.tabRow2exportRow(tabRow, col_nr_export)[0]
            
        #print exportRows
             
        #write to csv file
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
        self.model.update(run_id = run_id)                        
        #myModel.myTable.update(self)
        self.setColumnWidth()
        self.update_counter()
            

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
        
                                    
                                                                                            
    

            
            

        
        
    