# -*- coding: utf-8 -*-

## @package gui
#  Dokumentace pro model Gui
#
#  bla blar

import time
from PyQt4 import Qt, QtCore, QtGui
from ewitis.gui.UiAccesories2 import uiAccesories

from ewitis.data.db import db
from ewitis.data.dstore import dstore
from ewitis.gui.UiAccesories import MSGTYPE 

import libs.db_csv.db_csv as Db_csv
import ewitis.exports.ewitis_html as ew_html
import libs.utils.utils as utils 



TABLE_RUNS, TABLE_TIMES, TABLE_USERS = range(3)
MODE_EDIT, MODE_LOCK, MODE_REFRESH = range(3)
SYSTEM_SLEEP, SYSTEM_WORKING = range(2)   
    
class myParameters():
    """
    parametr pro třídu myTable (resp. odděděné TimesParameters, RunsParameters, UserParameters)
    
    *Args:*
        Source(QMainWindow): postupuje gui, database, table a další   
    """
    def __init__(self, source):                
        
        #ui accesories
        self.uia = source.UiAccesories        
    
class myAbstractModel():
    def __init__(self): 
        pass 
    
    def row(self, r):
        """
        vrací řádek jako list[] unicode stringů
        """                
        row = []
        for c in range(self.columnCount()):
            index = self.index(r, c)
            value = self.data(index ).toString()
            row.append(utils.toUnicode(value))        
        return row
    
    
    def header(self):
        """
        vrací hlavičku tabulky jako list[]
        """
        
        header = []
        for i in range(self.columnCount()):
            value = self.headerData(i, QtCore.Qt.Horizontal).toString()
            header.append(utils.toUnicode(value))
        return header
    
    def row_dict(self, r):
        """
        vraci radek jako slovnik (podle cisla radku)
        """                    
        row = self.row(r)                                   
        header = self.header()                                                                                                                                                                          
        return dict(zip(header, row)) 
    
    def lists(self):
        """
        vrací tabulku(hodnoty buněk) v listu[]
        """        
        rows = []
        for r in range(self.rowCount()):                              
            rows.append(self.row(r))
        return rows
            
    def dicts(self):
        """
        vrací tabulku(hodnoty buněk) jako list of dict{}
        """ 
        dicts = []
        
        header = self.header()
        
        for i in range(self.rowCount()):
            row = self.row(i)            
            aux_dict = dict(zip(header, row))
            dicts.append(aux_dict)
        
        return dicts
           
class myModel(QtGui.QStandardItemModel, myAbstractModel):
    """    
    #odděděná od QStandardItemModel,
    základní model    
        
    *Args:* 
        params: třída obdahující parametry
    """
    def __init__(self, params):                    
                        
        #parametry
        self.params = params
        
        #model
        QtGui.QStandardItemModel.__init__(self, 0, len(self.params.TABLE_COLLUMN_DEF))                
        
        #
        self.table_mode = MODE_EDIT
        
        #nastaveni hlavicky   
        for key in self.params.TABLE_COLLUMN_DEF:
            
            #nastaveni jmena sloupce a jeho pozicovani            
            index = self.params.TABLE_COLLUMN_DEF[key]["index"]                          
            self.setHeaderData(index, QtCore.Qt.Horizontal, self.params.TABLE_COLLUMN_DEF[key]["name"]) 
            self.setHeaderData(index, QtCore.Qt.Horizontal, QtCore.QVariant(QtCore.Qt.AlignHCenter), QtCore.Qt.TextAlignmentRole)         
        
                                    
        #SLOTY
        
        #slot na zmenu policka, modelu
        QtCore.QObject.connect(self, QtCore.SIGNAL("itemChanged(QStandardItem *)"), self.sModelChanged)                                                    
             
    def sModelChanged(self, item):
        """
        SLOT, model se zmenil => ulozeni do DB
        """                                  
        
        #user change, no auto update        
        if(dstore.Get("user_actions") == 0):                                                                                                
                        
            #ziskat zmeneny radek, slovnik{}
            tabRow = self.row_dict(item.row())#self.getTableRow(item.row())                                                                                                  
            
            #prevest na databazovy radek, dbRow <- tableRow
            dbRow = self.table2dbRow(tabRow, item)                                            
                                        
            #exist row? 
            if (dbRow != None):                                                                                         
                #update DB
                try:                                                        
                    db.update_from_dict(self.params.name, dbRow)                
                except:                
                    uiAccesories.showMessage(self.params.name+" Update", "Error!")                
                
            #update model
            #time.sleep(2)
#            z1 = time.clock()
#            print "1: update"
#            time.sleep(1)                                                                        
            #self.update()
#            time.sleep(1)
#            print "2: update", (time.clock() - z1)                                                                        
    
    def flags(self, index):
        """
        definovice vlastností - enabled, selectable, editable;        
        první políčko je standartně needitovatelné => id
        """
        
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled        
        
        #NOT editable items
        if (index.column() == 0):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable 

    def db2tableRow(self, dbRow):
        """
        konverze DATABASE radku na TABLE radek
        pokud existuje sloupec z database i v tabulce, zkopiruje se 
        """        
        tabRow = {}
        
        #exist?
        if dbRow == None:
            tabRow = self.getDefaultTableRow()
        
        #kopie všeho z db do tab    
        for key in self.params.DB_COLLUMN_DEF:
            #kopie 1to1
            try:
                tabRow[key] = dbRow[key]
            except:
                pass #tento sloupec v tabulce neexistuje

        return tabRow     
   
    def table2dbRow(self, tabRow, item = None):
        """
        konverze TABLE radku do DATABASE radku       
        pokud existuje sloupec z tabulky i v databazi, zkopiruje se  
        """
        
        dbRow = {}
                       
        for key in self.params.DB_COLLUMN_DEF:                                 
            #kopie 1to1
            try:
                dbRow[ key] = tabRow[key]
            except:
                pass #tento sloupec v tabulce neexistuje                             
        return dbRow
    
    def import2dbRow(self, importRow):
        return importRow
    
    def table2exportRow(self, tableRow):
        exportRow = []
        return exportRow                        
        
    def getDefaultTableRow(self):
        """
        vraci radek naplneny zakladnimi daty
        """                
        row = {}     
           
        #prazdne znaky do vsech sloupcu
        for key in self.params.TABLE_COLLUMN_DEF:            
            row[key] = ""            
        
        #pokud existuje sloupec id, naplnit ho nejvyssim id
        if row.has_key('id'):
            try:
                row['id'] = db.getMax(self.params.name, 'id') + 1
            except:
                row['id'] = 0                        
        return row        
                
    def addRow(self, row):
        """
        prida radek do modelu,
        
        prochazi vsechny definovane sloupce tabulky
        pokud radek{} obsahuje sloupec(klic) z definice 
        prida se toto policko na prislusne misto    
        """
        
        nr_column = 0                        

        if (row == None):            
            return
            
        #novy radek
        self.insertRow(0)                
                        
        #pres definovane sloupce
        for key in self.params.TABLE_COLLUMN_DEF.keys():                                      
                                                     
            #existuje tento sloupec v pridavanem radku?                                               
            if (key in row.keys()):                                                                      
                
                #nastavit hodnotu policka                                                
                self.setData(self.index(0,self.params.TABLE_COLLUMN_DEF[key]["index"]), row[key])                                
                                
                nr_column += 1
            else:
                pass                                                              
    
    def update(self, parameter=None, value=None, conditions=None, operation=None):
        """
        update modelu z databaze
          
        update() => update cele tabulky
        update(parameter, value) => vsechny radky s parametrem = value
        update(conditions, operation) => condition[0][0]=condition[0][1] OPERATION condition[1][0]=condition[1][1] 
        """        
        #print self.params.name+": model update (s)"
       
        #disable user actions        
        dstore.Set("user_actions", dstore.Get("user_actions")+1)          
                      
        #smazat vsechny radky
        self.removeRows(0, self.rowCount())          
        
        #ziskat radky z databaze DB
        if ((parameter == None) and (conditions == None)):                
            rows = db.getAll(self.params.name)
        elif (conditions == None):
            rows = db.getParX(self.params.name, parameter, value, dstore.Get("times_view_limit"))
            #rows = db.getParX(self.params.name, parameter, value)
        elif (conditions!=[]):
            rows = db.getParXX(self.params.name, conditions, operation, dstore.Get("times_view_limit"))
        else:
            rows = []
                                   
                                                                 
        #pridat radky do modelu/tabulky
        row_dicts = []         
#        for row in rows:
#                        
#            #convert "db-row" to dict (in dict can be added record)
#            row_dicts.append(db.dict_factory(rows, row))
        row_dicts = db.cursor2dicts(rows)                                                
            
                            
        for row_dict in row_dicts:            
            #call table-specific function, return "table-row"                                           
            row_table = self.db2tableRow(row_dict)                                                                                                                                                     
            #add row to the table             
            self.addRow(row_table)

        #enable user actions                                                                                                                                                                                                   
        dstore.Set("user_actions", dstore.Get("user_actions")-1)                                                                          
            

class myProxyModel(QtGui.QSortFilterProxyModel, myAbstractModel):
    """
    """
    def __init__(self, params):
        #model
        QtGui.QSortFilterProxyModel.__init__(self)
        self.setDynamicSortFilter(True)        
        self.setFilterKeyColumn(-1)
        self.params = params                    
        
        QtCore.QObject.connect(self, QtCore.SIGNAL("dataChanged(const QModelIndex&,const QModelIndex&)"), self.sModelChanged)
            
    #setting flags for this model
    #first collumn is NOT editable
    def flags(self, index):             

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable        
        
                
    def IsColumnAutoEditable(self, column):
        return False
    def sModelChanged(self,  topLeft, bottomRight):
        if(dstore.Get("user_actions") == 0):                  
            if(topLeft == bottomRight):                
            
                '''změna jednoho prvku'''
                
                if(self.IsColumnAutoEditable(topLeft.column())):                                                        

                    '''editovat sloupec nad aktivním řádkem'''
                    
                    '''uložit aktivní řádek do datastore'''
                    dstore.Set("active_row", topLeft.row())
                    #print "aktivni radek je ted: ", topLeft.row(), dstore.Get("active_row")
                    
                    '''update model'''                                                                 
                    self.model.update()

                    '''editovat sloupec nad aktivním řádkem'''                         
                    myindex = self.index(dstore.Get("active_row")-1, topLeft.column())                    
                    if(myindex.isValid() == True):                        
                        self.params.gui['view'].edit(myindex)

    #get ids
    def ids(self):
        ids = []
        for i in range(self.rowCount()):
            row = []
            index = self.index(i,0)                              
            ids.append(str(self.data(index).toString()))
        return ids

class myTable():
    """
    
    """
    (eTOTAL, eCATEGORY, eGROUP, eLAPS) = range(0,4) 
    def  __init__(self, params):                                                
        
        #name
        self.params = params        
        
        #create PROXY MODEL
        print params.name, ": vytvarim proxy model"        
        self.proxy_model = self.params.classProxyModel(params)
        
        #create MODEL
        print params.name, ": vytvarim model"
        self.model = self.params.classModel(params)                
        
        
        #vazba na proxy model kvuli focusu / edit
        self.proxy_model.model = self.model
        
        #assign MODEL to PROXY MODEL
        self.proxy_model.setSourceModel(self.model)   
        
        #nastaveni proxy modelu
        self.params.gui['view'].setModel(self.proxy_model)
        
        #set default sorting
        self.params.gui['view'].sortByColumn(0, QtCore.Qt.DescendingOrder)
        
        
        #parametry        
        self.params.gui['view'].setRootIsDecorated(False)
        self.params.gui['view'].setAlternatingRowColors(True)        
        self.params.gui['view'].setSortingEnabled(True)
                
        #setColumnWidth()
        #self.update()
        
        QtCore.QObject.connect(self.params.gui['view'].selectionModel(), QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), self.sSelectionChanged)
                         
        #TIMERs
        #self.timer1s = QtCore.QTimer(); 
        #self.timer1s.start(1000);
        
        #MODE EDIT/REFRESH        
        self.table_mode = MODE_EDIT                     
                
        self.createSlots()
        
        #update "Counter"
        self.sFilterRegExp()        
        
    def sSelectionChanged(self, selected, deselected):
        #if selected:
        #print "selection changed"
        pass               
                        
        
        
    def setColumnWidth(self):
        
        for col in range(self.proxy_model.columnCount()):
            self.params.gui['view'].resizeColumnToContents(col)
              
        #nastaveni sirky sloupcu        
        for key in self.params.TABLE_COLLUMN_DEF:
            index = self.params.TABLE_COLLUMN_DEF[key]["index"]
            width = self.params.TABLE_COLLUMN_DEF[key]["width"]
            if(width):            
                self.params.gui['view'].setColumnWidth(index,width)
                #print index, key, width                        
        
    def createSlots(self):
        print "I: ",self.params.name," vytvarim sloty.."
        
        #TIMEOUT
        #QtCore.QObject.connect(self.timer1s, QtCore.SIGNAL("timeout()"), self.slot_Timer1s)
        
        # CLEAR FILTER BUTTON -> CLEAR FILTER
        QtCore.QObject.connect(self.params.gui['filterclear'], QtCore.SIGNAL("clicked()"), self.sFilterClear)
        
        # FILTER CHANGE -> CHANGE TABLE
        QtCore.QObject.connect(self.params.gui['filter'], QtCore.SIGNAL("textChanged (const QString & )"), self.sFilterRegExp)
        
        # ADD ROW BUTTON
        if (self.params.gui['add'] != None):
            QtCore.QObject.connect(self.params.gui['add'], QtCore.SIGNAL("clicked()"), self.sAdd)
        
        # REMOVE ROW BUTTON
        if (self.params.gui['remove'] != None):
            QtCore.QObject.connect(self.params.gui['remove'], QtCore.SIGNAL("clicked()"), self.sDelete)
        
        # IMPORT BUTTON -> CHANGE TABLE
        if (self.params.gui['import'] != None):
            QtCore.QObject.connect(self.params.gui['import'], QtCore.SIGNAL("clicked()"), self.sImport)   
            
        # EXPORT BUTTON
        if (self.params.gui['export'] != None):
            QtCore.QObject.connect(self.params.gui['export'], QtCore.SIGNAL("clicked()"), self.sExport)        
        
        # EXPORT WWW BUTTON
        #if(self.params.guidata.measure_mode != GuiData.MODE_TRAINING_BASIC):
        if (self.params.gui['export_www'] != None):
            QtCore.QObject.connect(self.params.gui['export_www'], QtCore.SIGNAL("clicked()"), self.sExport_www)
        
        # DELETE BUTTON -> EMPTY TABLE
        if (self.params.gui['delete'] != None):
            QtCore.QObject.connect(self.params.gui['delete'], QtCore.SIGNAL("clicked()"), self.sDeleteAll)
        
        #self.sFilterRegExp(filter, table, label_counter)        
                             
    #=======================================================================
    # SLOTS
    #=======================================================================
        
    #UPDATE TIMER    
    def slot_Timer1s(self):                 
        pass 
        #self.update()    #update table            
    
           
                 
    # CLEAR FILTER BUTTON -> CLEAR FILTER        
    def sFilterClear(self):    
        self.params.gui['filter'].setText("")
                        
    # FILTER CHANGE -> CHANGE TABLE
    def sFilterRegExp(self):    
        regExp = QtCore.QRegExp(self.params.gui['filter'].text(), QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
        self.proxy_model.setFilterRegExp(regExp)
        self.updateTabCounter()
        #self.params['counter'].setText(str(self.proxy_model.rowCount())+"/"+str(self.model.rowCount()))
              
                 
    # ADD ROW               
    def sAdd(self):
        title = "Table "+self.params.name+" Add"                
        
        #get ID for default record
        row = self.model.getDefaultTableRow()        
        #print row                        
        my_id = uiAccesories.showMessage(title,"ID: ", MSGTYPE.get_integer, row['id'])                
        if my_id == None:
            return

        #this ID exist?                
        res = db.getParId(self.params.name, my_id)            
        if(res):
            uiAccesories.showMessage(title,"Record with this ID already exist!")
            return
     
        row['id'] = my_id        
                    
        #dstore.Set("user_actions", False)  
                              
        dbRow = self.model.table2dbRow(row)        
        if(dbRow != None):        
            db.insert_from_dict(self.params.name, dbRow)            
            uiAccesories.showMessage(title,"succesfully (id="+str(my_id)+")", MSGTYPE.statusbar)

        self.update()                    
        #dstore.Set("user_actions", True)  
        
    # REMOVE ROW               
    def sDelete(self, label=""):                
        
        #title
        title = "Table '"+self.params.name + "' Delete"
                        
        #get selected id
        try:                     
            rows = self.params.gui['view'].selectionModel().selectedRows()                        
            id = self.proxy_model.data(rows[0]).toString()
        except:
            uiAccesories.showMessage(title, "Nelze smazat")
            return
            
        #confirm dialog and delete
        if (label != ""):
            label="\n\n("+label+")"        
        if (uiAccesories.showMessage(title, "Are you sure you want to delete 1 record from table '"+self.params.name+"' ? \n (id="+str(id)+")"+label, MSGTYPE.warning_dialog)):                        
            self.delete(id)
            uiAccesories.showMessage(title, "succesfully (id="+str(id)+")", MSGTYPE.statusbar)                                                                                            
                            
    def sImport(self):
        """import"""                                   
                                           
        #gui dialog        
        #filename = self.params.myQFileDialog.getOpenFileName(self.params.gui['view'],"Import CSV to table "+self.params.name,"dir_import_csv","Csv Files (*.csv)", self.params.name+".csv")                
        filename = uiAccesories.myQFileDialog.getOpenFileName("Import CSV to table "+self.params.name,"dir_import_csv","Csv Files (*.csv)", self.params.name+".csv")                
        
        #cancel or close window
        if(filename == ""):                 
            return        
                  
        #IMPORT CSV TO DATABASE
        #try:            
            
        #get sorted keys
        keys = []
        for list in sorted(self.params.DB_COLLUMN_DEF.items(), key = lambda (k,v): (v["index"])):
            keys.append(list[0])
            
        #create csv        
        aux_csv = Db_csv.Db_csv(filename)
        rows =  aux_csv.load()
                    
        #check csv file format - emty file
        if(rows==[]):                
            uiAccesories.showMessage(self.params.name+" CSV Import", "NOT Succesfully imported\n wrong file format")
            return
        
        #check csv file format - wrong format                                
        header = rows.pop(0)
        for i in range(3): 
            if not(header[i] in keys):
                uiAccesories.showMessage(self.params.name+" CSV Import", "NOT Succesfully imported\n wrong file format")
                return

        #counters
        state = {'ko':0, 'ok':0}
        
        #adding records to DB                        
        for row in rows:                                                                                                                                    
            #try:
                #add 1 record
            importRow = dict(zip(keys, row)) 
            dbRow = self.model.import2dbRow(importRow)                     
            if( db.insert_from_dict(self.params.name, dbRow, commit = False) == True):                                      
                state['ok'] += 1
            else:            
                state['ko'] += 1 #increment errors for error message
            #except:
            #    state['ko'] += 1 #increment errors for error message

        db.commit()                        
        self.model.update()
        self.sImportDialog(state)
        #except:
        #    uiAccesories.showMessage(self.params.name+" CSV Import", "Error")
                                                    
                
                                
    def sImportDialog(self, state):                            
        #title
        title = "Table '"+self.params.name + "' CSV Import"
        
        if(state['ko'] != 0) :
            uiAccesories.showMessage(title, "NOT Succesfully"+"\n\n" +str(state['ok'])+" record(s) imported.\n"+str(state['ko'])+" record(s) NOT imported.\n\n Probably already exist.")                                                            
        else:
            uiAccesories.showMessage(title,"Succesfully"+"\n\n" +str(state['ok'])+" record(s) imported.", MSGTYPE.info)                                               
        
    # EXPORT
    # WEB (or DB) => CSV FILE
    # what you see, is exported    
    #def sExport(self, source='table'):                        
    def sExport(self, source='table'):
        
        print "I: ", self.params.name, ": export"

                
        #get filename, gui dialog         
        #filename = self.params.myQFileDialog.getSaveFileName(self.params.gui['view'],"Export table "+self.params.name+" to CSV","dir_export_csv","Csv Files (*.csv)", self.params.name+".csv")                
        filename = uiAccesories.myQFileDialog.getSaveFileName("Export table "+self.params.name+" to CSV","dir_export_csv","Csv Files (*.csv)", self.params.name+".csv")                
        if(filename == ""):
            return              
        
        #title
        title = "Table '"+self.params.name + "' CSV Export"                
         
        #export to csv file
        #try:                        
        self.export_csv(filename, source)                                
        uiAccesories.showMessage(title, "Succesfully")            
        #except:            
        #    uiAccesories.showMessage(title, "NOT succesfully \n\nCannot write into the file")
                   
             
    # EXPORT WWW    
    # what you see, is exported    
    def sExport_www(self): 
        
        #get filename, gui dialog         
        filename = uiAccesories.myQFileDialog.getSaveFileName(self.params.gui['view'],"Export table "+self.params.name+" to HTML","dir_export_www","HTML Files (*.htm; *.html)", self.params.name+".htm")                
        if(filename == ""):
            return                
         
        #export to HTML file        
        self.sExport_directWWW(filename)
                                                                        
    
    #default WWW export - without dialog to specific directory        
    def sExport_directWWW(self, filename = None):

        if filename == None:
            filename = utils.get_filename("export/www/"+self.params.name+"_"+dstore.Get('race_name')+".htm")
            
        exportRows = []
        for tabRow in self.proxy_model.dicts():
            #dbRow = self.getDbRow(tabRow['id'])            
            #if(self.model.order.IsLastUsertime(dbRow, tabRow['lap'])):
            exportRow = self.tabRow2exportRow(tabRow, myTable.eTOTAL)
            
            #workaround FORMULE
            #exportRow[1].append(tabRow['laptime']) 
            #exportRow[0].append(u'Čas kola')
            
            exportRows.append(exportRow[1])
            exportHeader = exportRow[0]              
        
        #title
        title = "Table '"+self.params.name + "' HTML Export"
         
        #export to HTML file
        try:                                                
            html_page = ew_html.Page_table(filename, title = dstore.Get('race_name'), styles= ["css/results.css",], lists = exportRows, keys = exportHeader)
            html_page.save()                             
            uiAccesories.showMessage(title, "Succesfully ("+filename+")", dialog=False)            
        except IOError:            
           uiAccesories.showMessage(title, "NOT succesfully \n\nCannot write into the file ("+filename+")")
                                         
                        
    # DELETE BUTTON          
    def sDeleteAll(self):
        
        #title
        title = "Table '"+self.params.name + "' Delete"
        
        #confirm dialog and delete
        if (uiAccesories.showMessage(title, "Are you sure you want to delete table '"+self.params.name+"' ?", msgtype = MSGTYPE.warning_dialog)):
            self.deleteAll()                                            
    
                  
        
    def export_csv(self, filename, source='table'):      
                
        aux_csv = Db_csv.Db_csv(filename) #create csv class        
        
        #FROM TABLE 
        if(source == 'table'):                        
            
            #get table as lists; save into file in csv format
            #print self.proxy_model.header()                 
            aux_csv.save(self.proxy_model.lists(), keys = self.proxy_model.header()) 
        
        #FROM DB
        elif(source == 'db'):
            ids = self.proxy_model.ids()
    
            conditions = []
            for id in ids:
                conditions.append(['id', id])
                            
            #get db as tuples; save into file in csv format
            rows = db.getParXX(self.params.name, conditions, 'OR')
            print "dicts", dict(zip(self.proxy_model.header(),self.proxy_model.lists()))
            aux_csv.save(rows)
            
        #FROM DB
        elif(source == 'raw'):
            self.export_csv_raw(filename)
            return
            
            #final lists for CSV export
            raw = []
            
            #get list from table Times
            tabLists = self.proxy_model.lists()                    
            
            #get indexes
            user_id_index = self.params.DB_COLLUMN_DEF['user_id']['index']
            id_index = self.params.TABLE_COLLUMN_DEF['id']['index']                                
            name_index = self.params.TABLE_COLLUMN_DEF['name']['index']
            category_index = self.params.TABLE_COLLUMN_DEF['category']['index']
            
            
            #            
            for list in tabLists:
                userlist = []             
                
                #get time per id
                time = db.getParId("times", list[id_index])                                
                                
                #get user per user_id                                                
                #user = db.getParId("users", time[user_id_index])
                user = db.getParId("users", time[user_id_index])
                               
                
                if user != None:
                                    
                    #convert sqlite3.row to list                
                    for item in user:
                        userlist.append(item)                        
                                        
                    #pop name, category
                    list.pop(category_index)
                    list.pop(name_index)                                                            
                                                        
                    #get final row for export
                    raw_row =  list + userlist

                    #append row to final lists                                          
                    raw.append(raw_row)
                else:
                    print "neco spatne",list       
                    
                #save to CSV
                header = self.proxy_model.header()                
                header.pop(category_index)
                header.pop(name_index)    
                
                header2 = self.params.tabUser.proxy_model.header()
                header2[0] = "user_id"                                                                     

                aux_csv.save(raw, keys = (header + header2))
                                                             
            
            
    def update(self, parameter=None, value=None, selectionback=True):                        
                                    
        #get row-selection
        if(selectionback==True):
            try:
                rows = self.params.gui['view'].selectionModel().selectedRows()         
                model_index = rows[0] #selected row index #row = rows[0].row() if rows else 0         
            except:
                pass 
        
        #update model
        self.model.update(parameter=parameter, value=value)
        
        
        #resize collumns to contents        
        #for col in range(self.proxy_model.columnCount()):
        #    self.params.gui['view'].resizeColumnToContents(col)        
        self.setColumnWidth()        

            
        #row-selection back
        if(selectionback==True):                           
            try:                
                self.params.gui['view'].selectionModel().setCurrentIndex(model_index, QtGui.QItemSelectionModel.Rows | QtGui.QItemSelectionModel.SelectCurrent)            
            except:
                pass            
        
        #update gui counter
        self.updateTabCounter()
       
        #
        #update db couner
        self.updateDbCounter()
        #print "db counter:",self.params.name, dstore.Get("count")
                
        
    def updateTabCounter(self):        
        self.params.gui['counter'].setText(str(self.proxy_model.rowCount())+"/"+str(self.model.rowCount()))
        
    def updateDbCounter(self):        
        dstore.SetItem("count", [self.params.name,], self.getDbCount())
            
                         
    def getDbRow(self, id):
                 
        dbRow = db.getParX(self.params.name, "id", id).fetchone()                            
        return dbRow
    
    def getTabRow(self, id):
                             
        #get db row
        dbRow = self.getDbRow(id)
        
        tabRow = self.model.db2tableRow(dbRow)  
            
        return tabRow
    
    def getDbRows(self):                                 
        dbRows = db.getAll(self.params.name)                      
        return dbRows
            
    def getDbCount(self):                                 
        count = db.getCount(self.params.name)                              
        return count        
    
    def delete(self, id):
        db.delete(self.params.name, id)                          
        self.model.update()
        
    def deleteAll(self):
        #print "table deleteall"
        db.deleteAll(self.params.name)
        self.model.update()
        
                                        
        
        
        
                        
                
        
        
        
        


              
