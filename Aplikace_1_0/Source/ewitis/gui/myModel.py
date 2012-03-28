# -*- coding: utf-8 -*-

## @package gui
#  Dokumentace pro model Gui
#
#  bla bla

import time
from PyQt4 import Qt, QtCore, QtGui
import ewitis.gui.GuiData as GuiData
import libs.db_csv.db_csv as Db_csv
import ewitis.exports.ewitis_html as ew_html
import libs.sqlite.sqlite as sqlite

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
        
        #callback METHOD,  for showing dialogs, messages
        self.showmessage = source.showMessage
    
        #db for acces
        self.db = source.db
        
        #guidata
        self.guidata = source.GuiData
           
class myModel(QtGui.QStandardItemModel):
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
        QtCore.QObject.connect(self, QtCore.SIGNAL("itemChanged(QStandardItem *)"), self.slot_ModelChanged)                                            
             
    def slot_ModelChanged(self, item):
        """
        SLOT, model se zmenil => ulozeni do DB
        """                          
        
        #user change, no auto update
        if((self.params.guidata.table_mode == GuiData.MODE_EDIT) and (self.params.guidata.user_actions == GuiData.ACTIONS_ENABLE)):                                                                  
                        
            #ziskat zmeneny radek, slovnik{}
            tabRow = self.getTableRow(item.row())                                                                              
            
            #prevest na databazovy radek, dbRow <- tableRow
            dbRow = self.table2dbRow(tabRow)                    
                                        
            #exist row? 
            if (dbRow != None): 
                                                                                           
                #update DB
                try:                                                        
                    self.params.db.update_from_dict(self.params.name, dbRow)
                except:                
                    self.params.showmessage(self.params.name+" Update", "Error!")                
                
            #update model                                                               
            self.update() 
    
    def flags(self, index):
        """
        definovice vlastností - enabled, selectable, editable;        
        první políčko je standartně needitovatelné => id
        """
        
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled        

        #refresh mode => NOT editable                                    
        if(self.params.guidata.table_mode ==  MODE_REFRESH):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
        #NOT editable items
        if (index.column() == 0):
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
         
    def lists(self):
        """
        vraci tabulku(hodnoty bunek) v listu[]
        """
        
        rows = []
        for i in range(self.rowCount()):
            row = []
            for j in range(self.columnCount()):
                index = self.index(i,j)
                mystr1 = self.data(index).toString()                   
                mystr2 = str(mystr1.toUtf8())                
                row.append(mystr2)            
            rows.append(row)
        return rows
    
    
    


    def db2tableRow(self, dbRow):
        """
        konverze DATABASE radku na TABLE radek
        pokud existuje sloupec z database i v tabulce, zkopiruje se 
        """
        
        tabRow = {}
        
        #exist?
        if dbRow == None:
            tabRow = self.getDefaultTableRow()
     
        for key in self.params.TABLE_COLLUMN_DEF:         
                        
            #kopie 1to1
            try:
                tabRow[key] = dbRow[key]
            except:
                pass #tento sloupec v tabulce neexistuje

        return tabRow
     
   
    def table2dbRow(self, tabRow):
        """
        konverze TABLE ěščřžýáíéradku do DATABASE radku       
        pokud existuje sloupec z tabulky i v databazi, zkopiruje se  
        """
        
        dbRow = {}
                       
        for key in self.params.DB_COLLUMN_DEF:         
                        
            #kopie 1to1
            try:
                dbRow[ key] = tabRow[key]
            except:
                pass #tento sloupec v tabulce neexistuje
                
        #QString to String
        for key in dbRow.keys():
            if type(dbRow[key]) is Qt.QString:
                dbRow[key] = str(dbRow[key].toUtf8())
                
        return dbRow
       
    def table2exportRow(self, tabRow):
        """
        konverze TABLE radku do DATABASE radku       
        pokud existuje sloupec z tabulky i v databazi, zkopiruje se
        """     
        exportRow = {}
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
                row['id'] = self.params.db.getMax(self.params.name, 'id') + 1
            except:
                row['id'] = 0                
        
        return row
    
    def header(self):
        """
        vraci hlavicku tabulky jako list[]
        """
        
        header = []
        for i in range(self.columnCount()):
            header.append(str(self.headerData(i, QtCore.Qt.Horizontal).toString()))
        return header
     
    def getTableRow(self, nr_row):
        """
        vraci radek jako slovnik (podle cisla radku)
        """
                
        nr_column = 0
        row = {}                

        print self.header()                
        for key in self.header():                            
            row[key] = self.item(nr_row, nr_column).text()
            nr_column += 1
        
        return row    
                
    def addRow(self, row):
        """
        prida radek do modelu,
        
        prochazi vsechny definovane sloupce tabulky
        pokud radek{} obsahuje sloupec(klic) z definice 
        prida se toto policko na prislusne misto    
        """
        
        nr_column = 0                        

        if (row == {}):            
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
                
        self.params.guidata.user_actions = GuiData.ACTIONS_DISABLE        
                      
        #smazat vsechny radky
        self.removeRows(0, self.rowCount())  
        
        #ziskat radky z databaze DB
        if ((parameter == None) and (conditions == None)):                
            rows = self.params.db.getAll(self.params.name)
        elif (conditions == None):
            rows = self.params.db.getParX(self.params.name, parameter, value)
        elif (conditions!=[]):
            rows = self.params.db.getParXX(self.params.name, conditions, operation)
        else:
            rows = []        
                                                    
        #pridat radky do modelu/tabulky
        for row in rows:            
            
            #convert "db-row" to dict (in dict can be added record)
            row_dict = self.params.db.dict_factory(rows, row)            
            
            #call table-specific function, return "table-row"                                           
            row_table = self.db2tableRow(row_dict)                                                                                                                        
             
            #add row to the table            
            self.addRow(row_table)                                 
            
        self.params.guidata.user_actions = GuiData.ACTIONS_ENABLE                                                                          
            

class myProxyModel(QtGui.QSortFilterProxyModel):
    """
    """
    def __init__(self):
        #model
        QtGui.QSortFilterProxyModel.__init__(self)
        self.setDynamicSortFilter(True)        
        self.setFilterKeyColumn(-1)                
        
    #get ids
    def ids(self):
        ids = []
        for i in range(self.rowCount()):
            row = []
            index = self.index(i,0)                              
            ids.append(str(self.data(index).toString()))
        return ids
        
    #get headerData
    def header(self):
        header = []
        for i in range(self.columnCount()):
            header.append(str(self.headerData(i, QtCore.Qt.Horizontal).toString()))
        return header
    
    
    def row(self, nr_row):
        row = []
        for j in range(self.columnCount()):
            index = self.index(nr_row, j)
            mystr1 = self.data(index).toString()                   
            mystr2 = str(mystr1.toUtf8())                
            row.append(mystr2)
        return row     
    
    #get current state in lists
    def lists_old(self):
        rows = []
        for i in range(self.rowCount()):
            row = []
            for j in range(self.columnCount()):
                index = self.index(i,j)
                mystr1 = self.data(index).toString()                   
                mystr2 = str(mystr1.toUtf8())                
                row.append(mystr2)            
            rows.append(row)
        return rows
    
    #get current state in lists
    def lists(self):
        rows = []
        for i in range(self.rowCount()):
            row = self.row(i)                       
            rows.append(row)
        return rows
    
    #get current state in dicts
    def dicts(self):
        dicts = []
        
        header = self.header()
        
        for i in range(self.rowCount()):
            row = self.row(i)
            aux_dict = dict(zip(header, row))
            dicts.append(aux_dict)
        
        return dicts


class myTable():
    """
    
    """
    def  __init__(self, params):                
                        
        #
        print "TABLE: ",params.name
        
        #name
        self.params = params        
        
        
        #create MODEL
        self.model = self.params.classModel(params)        
        
        #create PROXY MODEL        
        self.proxy_model = self.params.classProxyModel()
        
        #assign MODEL to PROXY MODEL
        self.proxy_model.setSourceModel(self.model)   
        
        #set default sorting
        self.params.gui['view'].sortByColumn(1, QtCore.Qt.AscendingOrder)
        
        #nastaveni proxy modelu
        self.params.gui['view'].setModel(self.proxy_model)
        
        #parametry        
        self.params.gui['view'].setRootIsDecorated(False)
        self.params.gui['view'].setAlternatingRowColors(True)        
        self.params.gui['view'].setSortingEnabled(True)
        
        self.update()#setColumnWidth()
                    
        
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(1000);
        
        #MODE EDIT/REFRESH        
        self.table_mode = MODE_EDIT                     
                
        self.createSlots()
        
        #update "Counter"
        self.sFilterRegExp()
        
        #TIMERs
        self.timer1s = QtCore.QTimer(); 
        self.timer1s.start(1000);
        
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
        QtCore.QObject.connect(self.timer1s, QtCore.SIGNAL("timeout()"), self.slot_Timer1s)
        
        # CLEAR FILTER BUTTON -> CLEAR FILTER
        QtCore.QObject.connect(self.params.gui['filterclear'], QtCore.SIGNAL("clicked()"), self.sFilterClear)
        
        # FILTER CHANGE -> CHANGE TABLE
        QtCore.QObject.connect(self.params.gui['filter'], QtCore.SIGNAL("textChanged (const QString & )"), self.sFilterRegExp)
        
        # ADD ROW BUTTON
        QtCore.QObject.connect(self.params.gui['add'], QtCore.SIGNAL("clicked()"), self.sAdd)
        
        # REMOVE ROW BUTTON
        QtCore.QObject.connect(self.params.gui['remove'], QtCore.SIGNAL("clicked()"), self.sDelete)
        
        # IMPORT BUTTON -> CHANGE TABLE
        if (self.params.gui['import'] != None):
            QtCore.QObject.connect(self.params.gui['import'], QtCore.SIGNAL("clicked()"), self.sImport)   
            
        # EXPORT BUTTON
        QtCore.QObject.connect(self.params.gui['export'], QtCore.SIGNAL("clicked()"), self.sExport)        
        
        # EXPORT WWW BUTTON
        #if(self.params.guidata.measure_mode != GuiData.MODE_TRAINING_BASIC):
        if (self.params.gui['export_www'] != None):
            QtCore.QObject.connect(self.params.gui['export_www'], QtCore.SIGNAL("clicked()"), self.sExport_www)
        
        # DELETE BUTTON -> EMPTY TABLE
        QtCore.QObject.connect(self.params.gui['delete'], QtCore.SIGNAL("clicked()"), self.sDeleteAll)
        
        #self.sFilterRegExp(filter, table, label_counter)
                             
    #=======================================================================
    # SLOTS
    #=======================================================================
        
    #UPDATE TIMER    
    def slot_Timer1s(self):                 
        if (self.params.guidata.table_mode == GuiData.MODE_REFRESH): 
            self.update()    #update table            
    
        # CLEAR FILTER BUTTON -> CLEAR FILTER        
    def sFilterClear(self):    
        self.params.gui['filter'].setText("")
                        
    # FILTER CHANGE -> CHANGE TABLE
    def sFilterRegExp(self):    
        regExp = QtCore.QRegExp(self.params.gui['filter'].text(), QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
        self.proxy_model.setFilterRegExp(regExp)
        self.update_counter()
        #self.params['counter'].setText(str(self.proxy_model.rowCount())+"/"+str(self.model.rowCount()))
              
                 
    # ADD ROW               
    def sAdd(self):
        title = "Table "+self.params.name+" Add"                
        
        #get ID for default record
        row = self.model.getDefaultTableRow()        
        #print row                
        my_id = self.params.showmessage(title,"ID: ", msgtype="input_integer", value = row['id'])                
        if my_id == None:
            return

        #this ID exist?                
        res = self.params.db.getParId(self.params.name, my_id)            
        if(res):
            self.params.showmessage(title,"Record with this ID already exist!")
            return
     
        #get dict for adding
        #row = {}
        #for key in self.params['keys']:
        #    row[key] = ''
        row['id'] = my_id        
                
        self.model.params.guidata.user_actions = GuiData.ACTIONS_DISABLE
                
        #self.model.addRow(row)
                
        dbRow = self.model.table2dbRow(row)        
        if(dbRow != None):        
            self.params.db.insert_from_dict(self.params.name, dbRow)            
            self.params.showmessage(title,"succesfully (id="+str(my_id)+")", dialog = False)

        self.update()            
        self.model.params.guidata.user_actions = GuiData.ACTIONS_ENABLE
        
    # REMOVE ROW               
    def sDelete(self, label=""):                
        
        #title
        title = "Table '"+self.params.name + "' Delete"
                        
        #get selected id
        try:                     
            rows = self.params.gui['view'].selectionModel().selectedRows()                        
            id = self.proxy_model.data(rows[0]).toString()
        except:
            self.params.showmessage(title, "Nelze smazat")
            
        #confirm dialog and delete
        if (label!=""):
            label="\n\n("+label+")"        
        if (self.params.showmessage(title, "Are you sure you want to delete 1 record from table '"+self.params.name+"' ? \n (id="+str(id)+")"+label, msgtype='warning_dialog')):                        
            self.delete(id)                          
                                                      
        
    # IMPORT
    # CSV FILE => DB               
    def sImport(self): 
                           
                                   
        #gui dialog -> get filename
        filename = QtGui.QFileDialog.getOpenFileName(self.params.gui['view'],"Import CSV to table "+self.params.name,"import/table_"+self.params.name+".csv","Csv Files (*.csv)")                
        
        #cancel or close window
        if(filename == ""):                 
            return        
                  
        #IMPORT CSV TO DATABASE
        try:                          
            
            #get sorted keys
            keys = []
            for list in sorted(self.params.DB_COLLUMN_DEF.items(), key = lambda (k,v): (v["index"])):
                    keys.append(list[0])
                    
            #import CSV to Database
            state = self.params.db.importCsv(self.params.name, filename, keys)
            
            #update gui
            self.model.update()
            self.sImportDialog(state)
        except sqlite.CSV_FILE_Error:
            self.params.showmessage(self.params.name+" CSV Import", "NOT Succesfully imported\n wrong file format")
                                
    def sImportDialog(self, state):                            
        #title
        title = "Table '"+self.params.name + "' CSV Import"
        
        if(state['ko'] != 0) :
            self.params.showmessage(title, "NOT Succesfully"+"\n\n" +str(state['ok'])+" record(s) imported.\n"+str(state['ko'])+" record(s) NOT imported.\n\n Probably already exist.")                                                            
        else:
            self.params.showmessage(title,"Succesfully"+"\n\n" +str(state['ok'])+" record(s) imported.", type='info')                                               
        
    # EXPORT
    # WEB (or DB) => CSV FILE
    # what you see, is exported    
    #def sExport(self, source='table'):                        
    def sExport(self, source='table'):
        
        #hack for table times
        print self.params.name
        if(self.params.name == "Times"):            
            source = 'raw'
        
        #get filename, gui dialog 
        filename = QtGui.QFileDialog.getSaveFileName(self.params.gui['view'],"Export table "+self.params.name+" to CSV","export/csv/table_"+self.params.name+".csv","Csv Files (*.csv)")                
        if(filename == ""):
            return              
        
        #title
        title = "Table '"+self.params.name + "' CSV Export"
        
        #print filename, source
         
        #export to csv file
        #try:                        
        self.export_csv(filename, source)                                
        self.params.showmessage(title, "Succesfully", dialog=False)            
        #except:            
        #    self.params.showmessage(title, "NOT succesfully \n\nCannot write into the file")
                   
             
    # EXPORT WWW    
    # what you see, is exported    
    def sExport_www(self): 
        
        #get filename, gui dialog 
        filename = QtGui.QFileDialog.getSaveFileName(self.params.gui['view'],"Export table "+self.params.name+" to HTML","export/www/table_"+self.params.name+".htm","HTML Files (*.htm; *.html)")                
        if(filename == ""):
            return              
        
        #misto zbytku dole pouzit sExport_directWWW()
        
        #title
        title = "Table '"+self.params.name + "' HTML Export"
         
        #export to HTML file        
        try:                                    
            html_page = ew_html.Page_table(filename, styles= ["css/results.css",], lists = self.proxy_model.lists(), keys = self.params.TABLE_COLLUMN_DEF.keys())
            html_page.save()                             
            self.params.showmessage(title, "Succesfully ("+filename+")", dialog=False)            
        except:            
            self.params.showmessage(title, "NOT succesfully \n\nCannot write into the file ("+filename+")")
    
    
    #default WWW export - without dialog to specific directory        
    def sExport_directWWW(self, filename="export/www/filename.htm"):
        
        #sort model
        self.model.sort(3, order = QtCore.Qt.DescendingOrder)
        
        #title
        title = "Table '"+self.params.name + "' HTML Export"
         
        #export to HTML file
        try:                                                
            html_page = ew_html.Page_table(filename, styles= ["css/results.css",], lists = self.proxy_model.lists(), keys = self.params.TABLE_COLLUMN_DEF.keys())
            html_page.save()                             
            self.params.showmessage(title, "Succesfully ("+filename+")", dialog=False)            
        except:            
            self.params.showmessage(title, "NOT succesfully \n\nCannot write into the file ("+filename+")")
                                         
                        
    # DELETE BUTTON          
    def sDeleteAll(self):
        
        #title
        title = "Table '"+self.params.name + "' Delete"
        
        #confirm dialog and delete
        if (self.params.showmessage(title, "Are you sure you want to delete table '"+self.params.name+"' ?", msgtype='warning_dialog')):
            self.deleteAll()                                            
    
                  
        
    def export_csv(self, filename, source='table'):      
                
        aux_csv = Db_csv.Db_csv(filename) #create csv class        
        
        #FROM TABLE 
        if(source == 'table'):                        
            
            #get table as lists; save into file in csv format                
            aux_csv.save(self.proxy_model.lists(), keys = self.proxy_model.header()) 
        
        #FROM DB
        elif(source == 'db'):
            ids = self.proxy_model.ids()
    
            conditions = []
            for id in ids:
                conditions.append(['id', id])
                            
            #get db as tuples; save into file in csv format
            rows = self.params.db.getParXX(self.params.name, conditions, 'OR')
            print "dicts", dict(zip(self.proxy_model.header(),self.proxy_model.lists()))
            aux_csv.save(rows)
            
        #FROM DB
        elif(source == 'raw'):
            
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
                time = self.params.db.getParId("times", list[id_index])                                
                                
                #get user per user_id                                                
                user = self.params.db.getParId("users", time[user_id_index])
                               
                
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
        
        #update counter
        self.update_counter()
        
    def update_counter(self):        
        self.params.gui['counter'].setText(str(self.proxy_model.rowCount())+"/"+str(self.model.rowCount()))
                         
    def getDbRow(self, id):
                 
        dbRow = self.params.db.getParX(self.params.name, "id", id).fetchone()                            
        return dbRow
    
    def getTabRow(self, id):
                             
        #get db row
        dbRow = self.getDbRow(id)
        
        tabRow = self.model.db2tableRow(dbRow)  
            
        return tabRow
    
    def delete(self, id):

        self.params.db.delete(self.params.name, id)                          
        self.model.update()
        
    def deleteAll(self):
        #print "table deleteall"
        self.params.db.deleteAll(self.params.name)
        self.model.update()
        
                                        
        
        
        
                        
                
        
        
        
        


              
