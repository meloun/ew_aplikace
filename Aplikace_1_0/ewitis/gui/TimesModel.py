# -*- coding: utf-8 -*-s
#!/usr/bin/env python

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import ewitis.gui.UsersModel as UsersModel
import ewitis.gui.GuiData as GuiData
import libs.db_csv.db_csv as Db_csv
import ewitis.gui.TimesUtils as Utils
import ewitis.gui.TimesSlots as Slots
import libs.utils.utils as utils



class TimesParameters(myModel.myParameters):
    def __init__(self, source):
                
        #table and db table name
        self.name = "Times" 
        
        #TABLE
        self.tabUser = source.U 
        
        #guidata
        self.guidata = source.GuiData          
        
        #=======================================================================
        # KEYS
        #=======================================================================
        self.DB_COLLUMN_DEF = { "state"     :     {"index": 0, "name": "state"},
                                "id"        :     {"index": 1, "name": "id"},
                                "run_id"    :     {"index": 2, "name": "run_id"},
                                "user_id"   :     {"index": 3, "name": "user_id"},
                                "cell"      :     {"index": 4, "name": "cell"},
                                "time_raw"  :     {"index": 5, "name": "time_raw"},
                                "time"      :     {"index": 6, "name": "time"},                                
                              }
        if(self.guidata.measure_mode == GuiData.MODE_TRAINING_BASIC) or (self.guidata.measure_mode == GuiData.MODE_TRAINING):
            self.TABLE_COLLUMN_DEF = { "id"         : {"index": 0,  "name": "id",        "width":35,    "write":1},
                                       "nr"         : {"index": 1,  "name": "nr",        "width":50,    "write":1},
                                       "cell"       : {"index": 2,  "name": "cell",      "width":50,    "write":1},
                                       "time"       : {"index": 3,  "name": "time",      "width":50,    "write":1},
                                       "name"       : {"index": 4,  "name": "name",      "width":50,    "write":1},
                                       "category"   : {"index": 5,  "name": "category",  "width":150,   "write":1},                                       
                                     }                             
      
        elif(self.guidata.measure_mode == GuiData.MODE_RACE):
            self.TABLE_COLLUMN_DEF = { "id"         : {"index": 0,  "name": "id",        "width":35,    "col_nr_export": None,    "write":1},
                                       "nr"         : {"index": 1,  "name": "nr",        "width":50,    "col_nr_export": 1,       "write":1},
                                       "cell"       : {"index": 2,  "name": "cell",      "width":50,    "col_nr_export": None,    "write":1},
                                       "time"       : {"index": 3,  "name": "time",      "width":100,   "col_nr_export": 5,       "write":1},
                                       "name"       : {"index": 4,  "name": "name",      "width":150,   "col_nr_export": 2,       "write":1},
                                       "category"   : {"index": 5,  "name": "category",  "width":100,   "col_nr_export": None,    "write":1},
                                       "order"      : {"index": 6,  "name": "order",     "width":50,    "col_nr_export": None,    "write":1},      
                                       "order_kat"  : {"index": 7,  "name": "order_kat", "width":50,    "col_nr_export": 0,       "write":1},      
                                       "start_nr"   : {"index": 8,  "name": "start_nr",  "width":50,    "col_nr_export": None,    "write":1},
                                       "lap"        : {"index": 9,  "name": "lap",       "width":50,    "col_nr_export": None,    "write":1},                                               
                                     }  
        self.EXPORT_COLLUMN_DEF = { "nr   "     :     {"index": 0, "name": "nr"},
                                    "time"      :     {"index": 1, "name": "time"},
                                    "name"      :     {"index": 2, "name": "name"},
                                    "category"  :     {"index": 3, "name": "category"}                                                                                                                                            
                                  }
        
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
        
        
class TimesModel(myModel.myModel):
    def __init__(self, params):                        
                
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)
        
        #width define - toDo for all tables, move to myModel
        #self.TABLE_DEF = params.TABLE_DEF
        
        #for row in params.TABLE_DEF:
        #    print "row:", row
            
            
        
        
        
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
        if (self.params.guidata.table_mode !=  GuiData.MODE_REFRESH):
            if ((index.column() == 4) or (index.column() == 5) or (index.column() == 6)):
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

        return myModel.myModel.flags(self, index)
    
    def getDefaultTableRow(self): 
        row = myModel.myModel.getDefaultTableRow(self)
        row['cell'] = 0                  
        row['nr'] = 0 #musi byt cislo!        
        row['time'] = "00:00:00,00"     
        row['start_nr'] = 1               
        return row                 

    
    #["id", "nr", "cell", "time", "name", "category", "address"]
    def db2tableRow(self, dbTime):
        
        
        #hide all zero time?
        if(self.showzero == False):
            if (dbTime["time"]=="00:00:00,00"):  
                return {}                        
        
        ''' USER '''         
        user =  self.params.tabUser.get_tab_user(dbTime["user_id"]) 
        
                        
        ''' 1to1 KEYS '''
        tabTime = myModel.myModel.db2tableRow(self, dbTime) 
        
        ''' OTHER KEYS '''                    
        tabTime['nr'] = user['nr']        
        if(dbTime['cell'] == 1):
            tabTime['name'] = ''
        else:            
            tabTime['name'] = user['name'] +' '+user['first_name']
        tabTime['category'] = user['category']        
        tabTime['cell'] = dbTime['cell']       
                                    
        ''' TIME '''
        #get starttime number
        if(tabTime['cell'] == 1): #start time?                           
            tabTime['start_nr'] = 1 #decrement 1.starttime
        else:
            tabTime['start_nr'] = self.params.guidata.getStartNr(tabTime['category']) #get starttime number
            
        #print tabTime['start_nr']
                                      
        tabTime['time'] = self.utils.dbtime2tabtime( dbTime['run_id'],dbTime, tabTime['start_nr']) #dbtime -> tabtime
        
        #lap
        try:
            tabTime['lap'] = self.utils.getLap(dbTime)
        except Utils.ZeroRawTime_Error, Utils.NoneRawTime_Error:
            tabTime['lap'] = 0
        
        
      
        #tabTime['address'] = user['address']            
        
        
        #RACE MODE?
        if(self.params.guidata.measure_mode == GuiData.MODE_RACE):
            
            dbTime["category"] = tabTime['category']
            
            #GET ORDER
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
                    
            #GET ORDER IN CATEGEORY
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
            
        return tabTime
                                                                                   
    
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
        
        #user nr => user id
        if(tabTime['nr'] == "0"):
            dbTime['user_id'] = 0            
        else:
                                                
            ''' USER '''                     
            user =  self.params.tabUser.get_db_user_par_nr(tabTime['nr'])                                           
            #user not found => nothing to save
            if(user == None):
                self.params.showmessage(self.params.name+" Update error", "No user with number "+str(tabTime['nr'])+"!")
                return None
            
            #TEST if is here enought START-TIMES
            nr_start = self.params.guidata.getStartNr(user['category'])            
            try:
                aux_start_time = self.utils.getStartTime(self.run_id, nr_start)
            except IndexError:                        
                self.params.showmessage(self.params.name+" Update error", str(nr_start)+".th start-time is necessary for users from this category!")
                return None
            except:
                self.params.showmessage(self.params.name+" Update error", "Cant find start time for this category.")
                return None
                
            
            
            #add user_id                     
            dbTime['user_id'] = user['id']    
        
        ''' TIME '''                         
        #try:
            #get TIME in absolut format
        

        try:                       
            dbTime['time_raw'] = self.utils.tabtime2dbtime(run_id, tabTime)
        except Utils.TimeFormat_Error:
            self.params.showmessage(self.params.name+" Update error", "Time wrong format!")                     
        
        
        dbTime['run_id'] = run_id
                    
        #except:
        #    self.params.showmessage(self.params.name+" Update error", "Wrong time format.!")
        #    return None                                
                  
                     
                                                                                                                                         
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
                
            #print conditions                            
                                         
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
        
        self.params = params               
                                                    
        #create MODEL
        self.model = TimesModel(params)  
        
         
        
        #create PROXY MODEL
        self.proxy_model = TimesProxyModel() 
        
        #create table instance (slots, etc.)
        myModel.myTable.__init__(self, params)                
        
        
        #special slots
        self.slots = Slots.TimesSlots(self)                     
        
        #assign MODEL to PROXY MODEL
        #self.proxy_model.setSourceModel(self.model)
        
        #assign PROXY MODEL to VIEW        
        self.params.gui['view'].setModel(self.proxy_model)
        self.params.gui['view'].setRootIsDecorated(False)
        self.params.gui['view'].setAlternatingRowColors(True)        
        self.params.gui['view'].setSortingEnabled(True)       
        
        #width
        for collumn in self.params.TABLE_COLLUMN_DEF.values():       
            self.params.gui['view'].setColumnWidth(collumn["index"], collumn["width"])
            
       
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
            print "export categories"
            QtCore.QObject.connect(self.params.gui['aDirectExportCategories'], QtCore.SIGNAL("triggered()"), self.sExportCategoriesDirect)
            #QtCore.QObject.connect(self.params.gui['aDirectExportCategories'], QtCore.SIGNAL("clicked()"), self.sExportCategoriesDirect)
            
    #=======================================================================
    # SLOTS
    #=======================================================================
    # EXPORT CATEGORIES
    def tabRow2exportRow(self, tabRow):        
               
        #export                    
        exportRow = []
        exportHeader = []
        
        index_user_nr = self.params.TABLE_COLLUMN_DEF["nr"]["index"]        
                            
        #table times part
        tabHeader = self.proxy_model.header()
        for collumn in self.params.TABLE_COLLUMN_DEF.values():
            if(collumn['col_nr_export'] is not None):
                
                #extend export if necessary                            
                if((len(exportRow))<=collumn['col_nr_export']):
                    exportRow = exportRow + ([''] * (collumn['col_nr_export'] - len(exportRow)+1))
                    exportHeader = exportHeader + ([''] * (collumn['col_nr_export'] - len(exportHeader)+1))                                
                    
                #add collumn to export
                exportRow[collumn['col_nr_export']] = tabRow[collumn['index']]
                exportHeader[collumn['col_nr_export']] = tabHeader[collumn['index']]
                
        #db user part
        tabHeader = self.params.tabUser.proxy_model.header()                    
        user = self.params.tabUser.get_db_user_par_nr(tabRow[index_user_nr])        
        for collumn in self.params.tabUser.params.DB_COLLUMN_DEF.values():
            if(collumn['col_nr_export'] is not None):
                
                #extend export if necessary
                if((len(exportRow))<=collumn['col_nr_export']):
                    exportRow = exportRow + ([''] * (collumn['col_nr_export'] - len(exportRow)+1))
                    exportHeader = exportHeader + ([''] * (collumn['col_nr_export'] - len(exportHeader)+1))
                    
                #add collumn to export
                if(user is not None):  
                    exportRow[collumn['col_nr_export']] = user[collumn['index']]
                else:
                    exportRow = []
                exportHeader[collumn['col_nr_export']] = tabHeader[collumn['index']]
        #print user
        exportHeader.append("gap")                
        return (exportHeader, exportRow) 
                    
    def sExportCategoriesDirect(self):        
        
        #title
        title = "Table '"+self.params.name + "' CSV Export Categories" 
        
        #get filename, gui dialog 
        dirname = QtGui.QFileDialog.getExistingDirectory(self.params.gui['view'], title)                
        if(dirname == ""):
            return              

        exportRows = []        

#        #EXPORT ALL TIMES                                    
        for tabRow in self.proxy_model.lists():
            exportRow = self.tabRow2exportRow(tabRow)[1]
            if exportRow != []:                            
                exportRows.append(exportRow)
            exportHeader = self.tabRow2exportRow(tabRow)[0]
            
        #write to csv file
        if(exportRows != []):
            print "export race", self.params.guidata.measure_setting["name"], ":",len(exportRows),"times"
            first_header = [self.params.guidata.measure_setting["name"], time.strftime("%d.%m.%Y", time.localtime()), time.strftime("%H:%M:%S", time.localtime())]
            exportRows.insert(0, exportHeader)
            aux_csv = Db_csv.Db_csv(dirname+"/"+self.params.guidata.measure_setting["name"]+".csv") #create csv class
            aux_csv.save(exportRows, keys = first_header)

        
                
         
        
        categories = [start['category'] for start in self.params.guidata.measure_setting["starts"]]
        index_category = self.params.TABLE_COLLUMN_DEF["category"]["index"]             
         
        for category in categories:
            exportRows = []                              
            for tabRow in self.proxy_model.lists():
                if (tabRow[index_category] == category):                
                    
                    #print "O,",exportRow                    
                    exportRows.append(self.tabRow2exportRow(tabRow)[1])
                    #exportHeader = self.tabRow2exportRow(tabRow)[0]                                             
            
            #export to csv file
            if(exportRows != []):
                print "export category", category, ":",len(exportRows),"times"
                first_header = [self.params.guidata.measure_setting["name"], category, time.strftime("%d.%m.%Y", time.localtime()), time.strftime("%H:%M:%S", time.localtime())]
                exportRows.insert(0, exportHeader)
                aux_csv = Db_csv.Db_csv(dirname+"/"+category+".csv") #create csv class
                aux_csv.save(exportRows, keys = first_header)
        #print first_header
        #print exportHeader
        
        
        
        
                    
                                         
        return 
    
    
    
    
    
    

                
                
        #for all ca
        for start in self.params.guidata.measure_setting["starts"]:
            exportRows = []
            print start["category"]
            for tabRow in self.proxy_model.lists():
                if (tabRow[category_index] == start["category"]):                    
                    exportRow = ['']*10
                    for collumn in self.params.TABLE_COLLUMN_DEF.values():
                        if(collumn['col_nr_export'] is not None):
                            exportRow[collumn['index']] = 6
                    
                    
                    for key in keys:
                        exportRow.append(tabRow[key]) 
                    print "export row",exportRow
                    exportRows.append(exportRow)

            header = self.proxy_model.header()
            exportHeader = []
            for key in keys:
                exportHeader.append(header[key])
            
            print "exportHeader", exportHeader
            print "exportRows", exportRows                                                                                         
                

                
                    
            
    def update(self, run_id = None):                      
        self.model.update(run_id = run_id)                
        #myModel.myTable.update(self)
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
        
                                    
                                                                                            
    

            
            

        
        
    