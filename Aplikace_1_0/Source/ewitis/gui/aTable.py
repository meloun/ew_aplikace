# -*- coding: utf-8 -*-
'''
Created on 28.12.2013

@author: Meloun
'''
from PyQt4 import Qt, QtCore, QtGui
from ewitis.gui.Ui import Ui
from ewitis.gui.UiAccesories import uiAccesories, MSGTYPE
import ewitis.gui.DEF_COLUMN as DEF_COLUMN
import libs.utils.utils as utils
from ewitis.data.dstore import dstore
from ewitis.data.db import db  
from ewitis.gui.aTableModel import * 

import libs.db_csv.db_csv as Db_csv
import ewitis.exports.ewitis_html as ew_html
import libs.utils.utils as utils 

      
class myTable():
    """
    
    """
    (eTOTAL, eCATEGORY, eGROUP, eLAPS) = range(0,4) 
    def  __init__(self, name):                                                                
        self.name = name
        self.InitCollumns()
        
    def InitCollumns(self):                        
        self.DB_COLLUMN_DEF = getattr(DEF_COLUMN, self.name.upper())['database']
        self.TABLE_COLLUMN_DEF = getattr(DEF_COLUMN,  self.name.upper())['table']  
        self.EXPORT_COLLUMN_DEF  = getattr(DEF_COLUMN,  self.name.upper())['table']       
        
    def InitGui(self, sImport = True):
        
        #============        
        # GUI
        #============
        #VIEW   
        self.gui = {}     
        self.gui['view'] = getattr(Ui(), self.name+"ProxyView") #self.gui['view'] = Ui().PointsProxyView
        
        #FILTER
        self.gui['filter'] = getattr(Ui(), self.name+"FilterLineEdit") #Ui().PointsFilterLineEdit
        self.gui['filterclear'] = getattr(Ui(), self.name+"FilterClear") #Ui().PointsFilterClear
        
        #GROUPBOX
        self.gui['add'] = getattr(Ui(), self.name+"Add") #Ui().PointsAdd
        self.gui['remove'] = getattr(Ui(), self.name+"Remove")# Ui().PointsRemove
        self.gui['export'] = getattr(Ui(), self.name+"Export") #Ui().PointsExport
        self.gui['export_www'] = None        
        try:
            self.gui['import'] = getattr(Ui(), self.name+"Import") #Ui().PointsImport
        except AttributeError:
            self.gui['import'] = None         
        self.gui['delete'] = getattr(Ui(), self.name+"Delete") #Ui().PointsDelete
        
        #COUNTER
        self.gui['counter'] = None #getattr(Ui(), self.name+"Counter") #Ui().PointsCounter
    
    def InitModels(self): 
        print __name__       
        module = __import__("table"+self.name, globals=globals())
        
        #create PROXY MODEL               
        self.proxy_model = getattr(module, self.name+"ProxyModel")(self) #self.params.classProxyModel(self.gui)        
        
        #create MODEL        
        self.model = getattr(module, self.name+"Model")(self) #self.params.classModel(self.gui)                                                        
        
        #vazba na proxy model kvuli focusu / edit
        self.proxy_model.model = self.model
        
        #assign MODEL to PROXY MODEL
        self.proxy_model.setSourceModel(self.model)
           
    def Init(self):              
        
        # init Gui
        self.InitGui()
        
        # init Models                                
        self.InitModels()
        
        #nastaveni proxy modelu
        self.gui['view'].setModel(self.proxy_model)
        
        #set default sorting
        self.gui['view'].sortByColumn(0, QtCore.Qt.DescendingOrder)
        
        
        #parametry        
        self.gui['view'].setRootIsDecorated(False)
        self.gui['view'].setAlternatingRowColors(True)        
        self.gui['view'].setSortingEnabled(True)
                
        #setColumnWidth()
        #self.update()
        
        QtCore.QObject.connect(self.gui['view'].selectionModel(), QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), self.sSelectionChanged)
                         
        #TIMERs
        #self.timer1s = QtCore.QTimer(); 
        #self.timer1s.start(1000);                        
                
        self.createSlots()
        
        #update "Counter"
        self.sFilterRegExp()        
        
    def sSelectionChanged(self, selected, deselected):
        #if selected:
        #print "selection changed"
        pass                                               
        
    def setColumnWidth(self):
        
        for col in range(self.proxy_model.columnCount()):
            self.gui['view'].resizeColumnToContents(col)
              
        #nastaveni sirky sloupcu        
        for key in self.TABLE_COLLUMN_DEF:
            index = self.TABLE_COLLUMN_DEF[key]["index"]
            width = self.TABLE_COLLUMN_DEF[key]["width"]
            if(width):            
                self.gui['view'].setColumnWidth(index,width)
                #print index, key, width                        
        
    def createSlots(self):
        print "I: ",self.name," vytvarim sloty.."
        
        #TIMEOUT
        #QtCore.QObject.connect(self.timer1s, QtCore.SIGNAL("timeout()"), self.slot_Timer1s)
        
        # CLEAR FILTER BUTTON -> CLEAR FILTER
        QtCore.QObject.connect(self.gui['filterclear'], QtCore.SIGNAL("clicked()"), self.sFilterClear)
        
        # FILTER CHANGE -> CHANGE TABLE
        QtCore.QObject.connect(self.gui['filter'], QtCore.SIGNAL("textChanged (const QString & )"), self.sFilterRegExp)
        
        # ADD ROW BUTTON
        if (self.gui['add'] != None):
            QtCore.QObject.connect(self.gui['add'], QtCore.SIGNAL("clicked()"), self.sAdd)
        
        # REMOVE ROW BUTTON
        if (self.gui['remove'] != None):
            QtCore.QObject.connect(self.gui['remove'], QtCore.SIGNAL("clicked()"), self.sDelete)
        
        # IMPORT BUTTON -> CHANGE TABLE
        if (self.gui['import'] != None):
            QtCore.QObject.connect(self.gui['import'], QtCore.SIGNAL("clicked()"), self.sImport)   
            
        # EXPORT BUTTON
        if (self.gui['export'] != None):
            QtCore.QObject.connect(self.gui['export'], QtCore.SIGNAL("clicked()"), self.sExport)        
        
        # EXPORT WWW BUTTON
        #if(self.params.guidata.measure_mode != GuiData.MODE_TRAINING_BASIC):
        if (self.gui['export_www'] != None):
            QtCore.QObject.connect(self.gui['export_www'], QtCore.SIGNAL("clicked()"), self.sExport_www)
        
        # DELETE BUTTON -> EMPTY TABLE
        if (self.gui['delete'] != None):
            QtCore.QObject.connect(self.gui['delete'], QtCore.SIGNAL("clicked()"), self.sDeleteAll)
        
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
        self.gui['filter'].setText("")
                        
    # FILTER CHANGE -> CHANGE TABLE
    def sFilterRegExp(self):    
        regExp = QtCore.QRegExp(self.gui['filter'].text(), QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
        self.proxy_model.setFilterRegExp(regExp)
        self.updateTabCounter()
        #self.params['counter'].setText(str(self.proxy_model.rowCount())+"/"+str(self.model.rowCount()))
              
                 
    # ADD ROW               
    def sAdd(self):
        title = "Table "+self.name+" Add"                
        
        #get ID for default record
        row = self.model.getDefaultTableRow()        
        #print row                        
        my_id = uiAccesories.showMessage(title,"ID: ", MSGTYPE.get_integer, row['id'])                
        if my_id == None:
            return

        #this ID exist?                
        res = db.getParId(self.name, my_id)            
        if(res):
            uiAccesories.showMessage(title,"Record with this ID already exist!")
            return
     
        row['id'] = my_id        
                    
        #dstore.Set("user_actions", False)  
                              
        dbRow = self.model.table2dbRow(row)        
        if(dbRow != None):        
            db.insert_from_dict(self.params.name, dbRow)            
            uiAccesories.showMessage(title,"succesfully (id="+str(my_id)+")", MSGTYPE.statusbar)

        self.Update()                    
        #dstore.Set("user_actions", True)  
        
    # REMOVE ROW               
    def sDelete(self, label=""):                
        
        #title
        title = "Table '"+self.name + "' Delete"
                        
        #get selected id
        try:                     
            rows = self.gui['view'].selectionModel().selectedRows()                        
            id = self.proxy_model.data(rows[0]).toString()
        except:
            uiAccesories.showMessage(title, "Nelze smazat")
            return
            
        #confirm dialog and delete
        if (label != ""):
            label="\n\n("+label+")"        
        if (uiAccesories.showMessage(title, "Are you sure you want to delete 1 record from table '"+self.name+"' ? \n (id="+str(id)+")"+label, MSGTYPE.warning_dialog)):                        
            self.delete(id)
            uiAccesories.showMessage(title, "succesfully (id="+str(id)+")", MSGTYPE.statusbar)                                                                                            
                            
    def sImport(self):
        """import"""                                         
                                           
        #gui dialog        
        #filename = self.params.myQFileDialog.getOpenFileName(self.params.gui['view'],"Import CSV to table "+self.params.name,"dir_import_csv","Csv Files (*.csv)", self.params.name+".csv")                
        filename = uiAccesories.getOpenFileName("Import CSV to table "+self.name,"dir_import_csv","Csv Files (*.csv)", self.name+".csv")                
        
        #cancel or close window
        if(filename == ""):                        
            return        
                  
        #IMPORT CSV TO DATABASE
        #try:            
            
        #get sorted keys
        keys = []
        for list in sorted(self.DB_COLLUMN_DEF.items(), key = lambda (k,v): (v["index"])):
            keys.append(list[0])
            
        #create csv        
        aux_csv = Db_csv.Db_csv(filename)
        rows =  aux_csv.load()
                    
        #check csv file format - emty file
        if(rows==[]):                
            uiAccesories.showMessage(self.name+" CSV Import", "NOT Succesfully imported\n wrong file format")
            return
        
        #check csv file format - wrong format                                
        #header = rows.pop(0)
        header = aux_csv.header()
        for i in range(3): 
            if not(header[i] in keys):
                uiAccesories.showMessage(self.name+" CSV Import", "NOT Succesfully imported\n wrong file format")
                return

        #counters
        state = {'ko':0, 'ok':0}
        
        #adding records to DB                        
        for row in rows:                                                                                                                                    
            #try:
                #add 1 record            
            dbRow = self.model.import2dbRow(row)                     
            if(db.insert_from_dict(self.name, dbRow, commit = False) == True):                                      
                state['ok'] += 1
            else:            
                state['ko'] += 1 #increment errors for error message
            #except:
            #    state['ko'] += 1 #increment errors for error message

        db.commit()                        
        self.model.Update()
        self.sImportDialog(state)
        #except:
        #    uiAccesories.showMessage(self.params.name+" CSV Import", "Error")
                                                    
                
                                
    def sImportDialog(self, state):                            
        #title
        title = "Table '"+self.name + "' CSV Import"
        
        if(state['ko'] != 0) :
            uiAccesories.showMessage(title, "NOT Succesfully"+"\n\n" +str(state['ok'])+" record(s) imported.\n"+str(state['ko'])+" record(s) NOT imported.\n\n Probably already exist.")                                                            
        else:
            uiAccesories.showMessage(title,"Succesfully"+"\n\n" +str(state['ok'])+" record(s) imported.", MSGTYPE.info)                                               
        
    # EXPORT
    # WEB (or DB) => CSV FILE
    # what you see, is exported    
    #def sExport(self, source='table'):                        
    def sExport(self, source='table'):
        
        print "I: ", self.name, ": export"

                
        #get filename, gui dialog         
        #filename = self.params.myQFileDialog.getSaveFileName(self.params.gui['view'],"Export table "+self.params.name+" to CSV","dir_export_csv","Csv Files (*.csv)", self.params.name+".csv")                
        filename = uiAccesories.getSaveFileName("Export table "+self.name+" to CSV","dir_export_csv","Csv Files (*.csv)", self.name+".csv")                
        if(filename == ""):
            return              
        
        #title
        title = "Table '"+self.name + "' CSV Export"                
         
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
        filename = uiAccesories.myQFileDialog.getSaveFileName(self.params.gui['view'],"Export table "+self.name+" to HTML","dir_export_www","HTML Files (*.htm; *.html)", self.params.name+".htm")                
        if(filename == ""):
            return                
         
        #export to HTML file        
        self.sExport_directWWW(filename)
                                                                        
    
    #default WWW export - without dialog to specific directory        
    def sExport_directWWW(self, filename = None):

        if filename == None:
            filename = utils.get_filename("export/www/"+self.name+"_"+dstore.Get('race_name')+".htm")
            
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
        title = "Table '"+self.name + "' HTML Export"
         
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
        title = "Table '"+self.name + "' Delete"
        
        #confirm dialog and delete
        if (uiAccesories.showMessage(title, "Are you sure you want to delete table '"+self.name+"' ?", msgtype = MSGTYPE.warning_dialog)):
            self.deleteAll()                                            
    
                  
        
    def export_csv(self, filename, source='table'):      
                
        aux_csv = Db_csv.Db_csv(filename) #create csv class        
        
        #FROM TABLE 
        if(source == 'table'):                        
            
            #get table as lists; save into file in csv format
            #print self.proxy_model.header()                 
            aux_csv.save(self.proxy_model.lists(), self.proxy_model.header()) 
        
        #FROM DB
        elif(source == 'db'):
            ids = self.proxy_model.ids()
    
            conditions = []
            for id in ids:
                conditions.append(['id', id])
                            
            #get db as tuples; save into file in csv format
            rows = db.getParXX(self.name, conditions, 'OR')
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
            user_id_index = self.DB_COLLUMN_DEF['user_id']['index']
            id_index = self.TABLE_COLLUMN_DEF['id']['index']                                
            name_index = self.TABLE_COLLUMN_DEF['name']['index']
            category_index = self.TABLE_COLLUMN_DEF['category']['index']
            
            
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
                                                             
            
            
    def Update(self, parameter = None, value = None, selectionback = True):                        
        
        print "update table", self.name
                                    
        #get row-selection
        if(selectionback==True):
            try:
                rows = self.gui['view'].selectionModel().selectedRows()         
                model_index = rows[0] #selected row index #row = rows[0].row() if rows else 0         
            except:
                pass 
        
        #update model
        self.model.Update(parameter=parameter, value=value)
        
        
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
        return True
          
                
        
    def updateTabCounter(self):
        if  self.gui['counter'] != None:         
            self.gui['counter'].setText(str(self.proxy_model.rowCount())+"/"+str(self.model.rowCount()))
        
    def updateDbCounter(self):        
        dstore.SetItem("count", [self.name,], self.getDbCount())
            
                         
    def getDbRow(self, id):
                 
        dbRow = db.getParX(self.name, "id", id).fetchone()                            
        return dbRow
    
    def getTabRow(self, id):
                             
        #get db row
        dbRow = self.getDbRow(id)
        
        tabRow = self.model.db2tableRow(dbRow)  
            
        return tabRow
    
    def getDbRows(self):                                 
        dbRows = db.getAll(self.name)                      
        return dbRows
            
    def getDbCount(self):                                 
        count = db.getCount(self.name)                              
        return count        
    
    def delete(self, id):
        db.delete(self.name, id)                          
        self.model.Update()
        
    def deleteAll(self):
        #print "table deleteall"
        db.deleteAll(self.name)
        self.model.Update()        
         

if __name__ == "__main__":
    import sys
    from PyQt4 import QtGui
    from Ui_App import Ui_MainWindow
    from ewitis.gui.Ui import appWindow
    app = QtGui.QApplication(sys.argv)
    appWindow.Init()
    uiAccesories.Init()
    
    tableTest =  myTable("Points")
    tableTest.Init()
        
    appWindow.show()    
    sys.exit(app.exec_())
    
