# -*- coding: utf-8 -*-s
#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import ewitis.gui.UsersModel as UsersModel
import libs.db_csv.db_csv as Db_csv
import ewitis.gui.TimesUtils as Utils
import ewitis.gui.DEF_COLUMN as DEF_COLUMN
import ewitis.gui.TimesSlots as Slots
import libs.utils.utils as utils



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
        self.utils = Utils.TimesUtils(self)
                        
        self.showall = False
        self.showzero = True                               
        
        #update with first run        
        first_run = self.params.db.getFirst("runs")
        if(first_run != None):
            self.run_id = first_run['id']
        else:
            self.run_id = 0 #no times for run_id = 0 
                
        self.update()        
                
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
        row['cell'] = 250                  
        row['nr'] = 0 #musi byt cislo!        
        row['time'] = "00:00:00,00"     
        row['start_nr'] = 1               
        return row                 

    
    def db2tableRow(self, dbTime):
        """    
        ["id", "nr", "cell", "time", "name", "category", "address"]
        """             
        #hide all zero time?
        if(self.showzero == False):
            if (int(dbTime["cell"])==1):                
                return {}                        
        
        ''' 1to1 KEYS '''           
        tabTime = myModel.myModel.db2tableRow(self, dbTime)
         
        ''' get USER
            - user_id je id v tabulce Users(bunky) nebo tag_id(rfid) '''                                     
        dbUser =  self.params.tabUser.getDbUserParIdOrTagId(dbTime["user_id"])
        if(dbUser == None):
            dbUser = {}
            dbUser['id'] = 0
            dbUser['category_id'] = 0        
        tabUser = self.params.tabUser.getTabRow(dbUser["id"])                
        tabCategory =  self.params.tabCategories.getTabRow(dbUser['category_id'])                        
                                
        ''' OTHER KEYS '''                    
        tabTime['nr'] = tabUser['nr']        
        if(dbTime['cell'] == 1):
            tabTime['name'] = ''
        elif(dbTime["user_id"] == 0):
            tabTime['name'] = 'undefined'
        else:           
            tabTime['name'] = tabUser['name'] +' '+tabUser['first_name']
            
        '''category'''            
        tabTime['category'] = tabUser['category']
        
                
        tabTime['cell'] = dbTime['cell']              
                                    
        """ TIME """
                
        '''get starttime number'''
        if(tabTime['cell'] == 1) or (tabTime['nr']==0): #start time?                           
            tabTime['start_nr'] = 1 #decrement 1.starttime
        else:                                
            tabTime['start_nr'] = tabCategory['start_nr']
        
        '''time'''                               
        tabTime['time'] = self.utils.dbtime2tabtime( dbTime['run_id'],dbTime, tabTime['start_nr']) #dbtime -> tabtime
        
        '''lap'''
        try:
            tabTime['lap'] = self.utils.getLap(dbTime)
        except Utils.ZeroRawTime_Error, Utils.NoneRawTime_Error:
            tabTime['lap'] = 0                                              
        
        #RACE MODE?
        #if(self.params.guidata.measure_mode == GuiData.MODE_RACE):
        #toDo: rozlisit podle mode z datastore
            
        dbTime["category"] = tabTime['category']
                        
        '''order'''
        try:
            order = self.utils.getOrder(dbTime)
            if(order["start"] >= order["end"]):                    
                tabTime['order'] = '%03d' % order["start"]
                #tabTime['order'] = str(order["start"])
            else:
                tabTime['order'] = '%03d - %03d ' % (order["start"], order["end"])
                #tabTime['order'] = str(order["start"])+" - "+str(order["end"])                
        except Utils.ZeroRawTime_Error, Utils.NoneRawTime_Error:            
            tabTime['order'] = None
        except Utils.WrongCell_Error:
            tabTime['order'] = None
                
        '''order in category'''
        try:
            order_incategory = self.utils.getOrder(dbTime, incategory=True)                                                           
            if(order_incategory["start"] >= order_incategory["end"]):  
                #tabTime['order in cat.'] = order_incategory["start"]                  
                tabTime['order_kat'] = '%03d' % order_incategory["start"]
                #tabTime['order in cat.'] = str(order_incategory["start"])           
            else:
                #tabTime['order in cat.'] = order_incategory["start"]
                tabTime['order_kat'] = '%03d - %03d ' % (order_incategory["start"], order_incategory["end"])
                #tabTime['order in cat.'] = str(order_incategory["start"])+" - "+str(order_incategory["end"])
        except Utils.ZeroRawTime_Error:                                 
            tabTime['order_kat'] = None
        except Utils.WrongCell_Error:
            tabTime['order'] = None                              
            
        return tabTime
                                                                                   
    def slot_ModelChanged(self, item):
        
                
        if(self.params.datastore.Get("user_actions")):  
        
            tabRow = self.getTableRow(item.row())
                    
            if(item.column() == self.params.TABLE_COLLUMN_DEF['nr']['index']):
               
                '''změna čísla/přiřazení uživatele nelze u času                
                   - startovací buňky
                   - nulového času'''
                
                if(int(tabRow['cell']) == 1):                            
                    self.params.showmessage(self.params.name+" Update error", "Cannot assign user to start time!")
                    self.update()
                    return 
                elif(tabRow['time'] == '00:00:00,00'):
                   self.params.showmessage(self.params.name+" Update error", "Cannot assign user to zero time!")
                   self.update()
                   return                                               
                
        
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
        
        #get run_id
        if(self.showall):
            #get time['run_id'] from DB, , in showall-mode i dont know what run is it            
            dbtime = self.params.db.getParId("times",tabTime['id'])
            run_id = dbtime['run_id']            
        else:
            run_id = self.run_id
                
        
        #first start time? => cant be updated       
        if(int(tabTime['id']) == (self.utils.getFirstStartTime(run_id)['id'])):
            self.params.showmessage(self.params.name+" Update error", "First start time cant be updated!")
            return None        
        
        '''USER NR => USER ID'''        
        
        if(int(tabTime['nr']) == 0):
            dbTime['user_id'] = 0            
        else:                                                
            ''' get DB-USER for save'''                                          
            dbUser =  self.params.tabUser.getDbUserParNr(tabTime['nr'])
            if(dbUser == None):
                self.params.showmessage(self.params.name+" Update error", "Cant find user with nr. "+ tabTime['nr'])                
                return None
                        
              
            '''get DB-CATEGORY'''             
            dbCategory = self.params.tabCategories.getDbRow(dbUser['category_id'])
            if(dbCategory == None):
                self.params.showmessage(self.params.name+" Update error", "Cant find category for this user.")                
                return None
            
            '''při změně čísla nejsou v tabTime správné user údaje'''
            tabTime['category'] = dbCategory['name']
            
            '''TEST if is here enought START-TIMES'''                        
            nr_start = dbCategory['start_nr']
            try:
                aux_start_time = self.utils.getStartTime(self.run_id, nr_start)
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
                     
        #get TIME in absolut format        
        try:                                               
            dbTime['time_raw'] = self.utils.tabtime2dbtime(run_id, tabTime)            
        except Utils.TimeFormat_Error:
            self.params.showmessage(self.params.name+" Update error", "Time wrong format!")                                 
                
        dbTime['run_id'] = run_id
        
        print "dbTime", dbTime                
                                                                                                                                                                                                                                                                                     
        return dbTime    
        
    
    #UPDATE TABLE        
    def update(self, run_id = None):
        
        if(run_id != None):                    
            self.run_id = run_id #update run_id
            
        #update start times
        self.utils.updateStartTimes()
        
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
    def __init__(self):                        
        
        #create PROXYMODEL
        myModel.myProxyModel.__init__(self)      
   
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
                    
                #add collumn to export                
                exportRow[collumn[col_nr_export]] = tabRow[collumn_key]
                exportHeader[collumn[col_nr_export]] = tabHeader[collumn['index']]                                
                
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
        dirname = QtGui.QFileDialog.getExistingDirectory(self.params.gui['view'], title)                
        if(dirname == ""):
            return              

        exportRows = []        

        '''export all'''                                       
        for tabRow in self.proxy_model.dicts():
            exportRow = self.tabRow2exportRow(tabRow, col_nr_export)[1]
            if exportRow != []:                            
                exportRows.append(exportRow)
            exportHeader = self.tabRow2exportRow(tabRow, col_nr_export)[0]
            
        '''write to csv file'''
        if(exportRows != []):
            print "export race", self.params.datastore.Get('race_name'), ":",len(exportRows),"times"
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
            
            '''write to csv file'''
            if(exportRows != []):
                print "export category", dbCategory['name'], ":",len(exportRows),"times"
                first_header = [self.params.datastore.Get('race_name'), dbCategory['name'], time.strftime("%d.%m.%Y", time.localtime()), time.strftime("%H:%M:%S", time.localtime())]
                exportRows.insert(0, exportHeader)
                aux_csv = Db_csv.Db_csv(dirname+"/"+dbCategory['name']+".csv") #create csv class
                aux_csv.save(exportRows, keys = first_header)                                                                                             
        return                                                                                                                   
                

    def sExport(self):
        
        col_nr_export = 'col_nr_export_raw'
        
        #get filename, gui dialog 
        filename = QtGui.QFileDialog.getSaveFileName(self.params.gui['view'],"Export table "+self.params.name+" to CSV","export/csv/table_"+self.params.name+".csv","Csv Files (*.csv)")                
        if(filename == ""):
            return               

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
            aux_csv.save(exportRows)               
                    
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
            
        #first start time? => cant be updated               
        if(int(id) == (self.model.utils.getFirstStartTime(self.model.run_id)['id'])):
            self.params.showmessage(self.params.name+" Delete warning", "First start time cant be deleted!")
            return None  
        
        #delete run with additional message
        myModel.myTable.sDelete(self)                                                         
        
                                    
                                                                                            
    

            
            

        
        
    