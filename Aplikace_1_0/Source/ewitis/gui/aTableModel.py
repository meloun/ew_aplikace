# -*- coding: utf-8 -*-
'''
Created on 28.12.2013

@author: Meloun
'''
from PyQt4 import Qt, QtCore, QtGui
from ewitis.gui.Ui import Ui
from ewitis.gui.UiAccesories import uiAccesories
import ewitis.gui.DEF_COLUMN as DEF_COLUMN
import libs.utils.utils as utils
from ewitis.data.dstore import dstore
from ewitis.data.db import db
import pandas as pd

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
            column = str(self.headerData(c, QtCore.Qt.Horizontal).toString())
            value = self.data(index ).toString()       
            
#             if(column == "id") or (column == "points2"): #need integer type for id
#                 print "yeah1", column, type(value)
#                 value = int(value)
#             else:                                    
#                 value = utils.toUnicode(value)
                
            if (column in self.table.TABLE_COLLUMN_DEF) and ("type" in  self.table.TABLE_COLLUMN_DEF[column]) and (self.table.TABLE_COLLUMN_DEF[column]["type"] == "number"):
                try:
                    value = int(value)
                except ValueError:
                    value = None                    
            else:                                    
                value = utils.toUnicode(value)
            row.append(value)                            
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

    def df(self):
        """
        vrací tabulku(hodnoty buněk) jako dataframe
        """
        df = pd.DataFrame(columns = self.header())                
        for i in range(self.rowCount()):                    
            df.loc[i] = self.row(i)
        df.set_index('id',  drop=False, inplace = True)
        
        
        #replace nan with None                
        df = df.where(pd.notnull(df), None)
        #print df.columns        
        return df


class myModel(QtGui.QStandardItemModel, myAbstractModel):
    """    
    odděděná od QStandardItemModel,
    základní model    
        
    *Args:* 
        table: pro přístup ke gui a name
    """
    (eTABLE, eDB, eWWW, eTOTAL, eGROUP, eCATEGORY, eLAPS) = range(0,7) 
    def __init__(self, table):                    
                
        self.table = table
        
        #model
        QtGui.QStandardItemModel.__init__(self, 0, len(self.table.TABLE_COLLUMN_DEF))                
        
        #nastaveni hlavicky   
        for key in self.table.TABLE_COLLUMN_DEF:
            
            #nastaveni jmena sloupce a jeho pozicovani            
            index = self.table.TABLE_COLLUMN_DEF[key]["index"]                          
            self.setHeaderData(index, QtCore.Qt.Horizontal, self.table.TABLE_COLLUMN_DEF[key]["name"]) 
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
                        
            #get changed row, dict{}
            tabRow = self.row_dict(item.row())            
                                                                                                                                      
            #update changed collumn                                  
            for key in self.table.TABLE_COLLUMN_DEF:                             
                if(item.column() == self.table.TABLE_COLLUMN_DEF[key]['index']):
                    if key in self.table.DB_COLLUMN_DEF:
                        try:                         
                            tabKey = self.table.TABLE_COLLUMN_DEF[key]['name']
                            db.update_from_dict(self.table.name, {'id':tabRow['id'], key: tabRow[tabKey]})                      
                            #db.update_from_dict(self.table.name, {'id':tabRow['id'], key: tabRow[key]})                      
                            return True
                        except KeyError:
                            uiAccesories.showMessage(self.table.name+" Update", "Error!")        
        return False
                                                                                           
                
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
        definice vlastností - enabled, selectable, editable;        
        první políčko je standartně needitovatelné => id
        """
        
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled        
        
        #set the item editable or not editable
        for key, value in self.table.TABLE_COLLUMN_DEF.items():
            #print "kv:",key, value
            if value['index'] == index.column():
                if value['write'] == False:                
                    return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
                else:
                    return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
        print self.table.name,">", key, value, index.data().toInt()[0] 
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
        for key in self.table.DB_COLLUMN_DEF:
            #kopie 1to1
            try:
                tabRow[key] = dbRow[key]
            except:
                pass #tento sloupec v tabulce neexistuje

        return tabRow     
            
    '''
    tabRow2exportRow()     
    '''
    def tabRow2exportRow(self, tabRow, keys, mode):                                    
        exportRow = {}        
                          
        if mode == myModel.eDB:
            exportRow = self.table.getDbRow(tabRow['id'])
        else:
            for key in keys:
                if key in tabRow:            
                    exportRow[key] = tabRow[key]                              
                                                              
        return dict(exportRow)
    
    
    def importRow2dbRow(self, importRow, mode = eTABLE):            
        return importRow
                          
        
    def getDefaultTableRow(self):
        """
        vraci radek naplneny zakladnimi daty
        """                
           
        #prazdne znaky do vsech sloupcu
        row = {}     
        for key, value in self.table.TABLE_COLLUMN_DEF.items():            
            row[key] = value["default"]            
        
        # id = maximal id + 1        
        try:
            row['id'] = db.getMax(self.table.name, 'id') + 1
        except:
            row['id'] = 0                                
        return row  
          
    def getDefaultDbRow(self):
        """
        vraci radek naplneny zakladnimi daty
        """                
           
        #prazdne znaky do vsech sloupcu
        row = {}     
        for key, value in self.table.DB_COLLUMN_DEF.items():            
            row[key] = value["default"]                    
        
        # id = maximal id + 1   
        try:
            row['id'] = db.getMax(self.table.name, 'id') + 1
        except:
            pass
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
        for key in self.table.TABLE_COLLUMN_DEF.keys():                                      
                                                     
            #existuje tento sloupec v pridavanem radku?                                               
            if (key in row.keys()):                                                                      
                
                #nastavit hodnotu policka                                                
                self.setData(self.index(0,self.table.TABLE_COLLUMN_DEF[key]["index"]), row[key])                                
                                
                nr_column += 1
            else:
                pass                                                              
    
    def Update(self, parameter=None, value=None, conditions=None, operation=None):
        """
        Update modelu z databaze
          
        Update() => update cele tabulky
        Update(parameter, value) => vsechny radky s parametrem = value
        Update(conditions, operation) => condition[0][0]=condition[0][1] OPERATION condition[1][0]=condition[1][1] 
        """        
        #print self.table.name+": model update (s)"
       
        #disable user actions        
        dstore.Set("user_actions", dstore.Get("user_actions")+1)          
                      
        #smazat vsechny radky
        self.removeRows(0, self.rowCount())          
        
        #ziskat radky z databaze DB
        if ((parameter == None) and (conditions == None)):                
            rows = db.getAll(self.table.name)
        elif (conditions == None):
            rows = db.getParX(self.table.name, parameter, value) #, dstore.Get("times_view_limit"))
            #rows = db.getParX(self.params.name, parameter, value)
        #elif (conditions!=[]):
        #    rows = db.getParXX(self.table.name, conditions, operation, dstore.Get("times_view_limit"))
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
    def __init__(self, table):        
        QtGui.QSortFilterProxyModel.__init__(self)
        self.table = table             
        
        #This property holds whether the proxy model is dynamically sorted and filtered whenever the contents of the source model change.       
        self.setDynamicSortFilter(True)

        #This property holds the column where the key used to filter the contents of the source model is read from.
        #The default value is 0. If the value is -1, the keys will be read from all columns.                
        self.setFilterKeyColumn(-1)
        
        QtCore.QObject.connect(self, QtCore.SIGNAL("dataChanged(const QModelIndex&,const QModelIndex&)"), self.sModelChanged)
            
    #def flags(self, index):        
    #    return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable        
                        
    def IsColumnAutoEditable(self, column):
        '''pokud true, po uživatelské editaci focus na další řádek''' 
        return False
    
    def sModelChanged(self,  topLeft, bottomRight):
        if(dstore.Get("user_actions") == 0):                  
            if(topLeft == bottomRight):                
            
                '''změna jednoho prvku'''
                
                if(self.IsColumnAutoEditable(topLeft.column())):                                                        

                    '''editovat sloupec nad aktivním řádkem'''
                    
                    '''uložit aktivní řádek do datastore'''
                    dstore.SetItem("gui", ["active_row"], topLeft.row())
                    #print "aktivni radek je ted: ", topLeft.row(), dstore.Get("active_row")                    

                    '''editovat sloupec nad aktivním řádkem'''                         
                    myindex = self.index(dstore.GetItem("gui", ["active_row"])-1, topLeft.column())                    
                    if(myindex.isValid() == True):                        
                        self.table.gui['view'].edit(myindex)

    #get ids
    def ids(self):
        ids = []
        for i in range(self.rowCount()):
            row = []
            index = self.index(i,0)                              
            ids.append(str(self.data(index).toString()))
        return ids