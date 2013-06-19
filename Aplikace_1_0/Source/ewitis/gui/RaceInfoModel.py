#-*- coding: utf-8 -*-  

import sys
import time
from PyQt4 import QtCore, QtGui
import ewitis.gui.myModel as myModel
import libs.db_csv.db_csv as Db_csv
import ewitis.gui.DEF_COLUMN as DEF_COLUMN

      
class RaceInfoParameters(myModel.myParameters):
       
    def __init__(self, source):
                                
        #table and db table name
        self.name = "RaceInfo"
        
        #tables
        self.tabUser = source.U  
        self.tabTimes = source.T  
        self.tabCategories = source.C  
        
        #=======================================================================
        # KEYS DEFINITION
        #======================================================================= 
        self.DB_COLLUMN_DEF = DEF_COLUMN.RACE_INFO['database']
        self.TABLE_COLLUMN_DEF = DEF_COLUMN.RACE_INFO['table']
                
        #create MODEL and his structure
        myModel.myParameters.__init__(self, source)                                                                                            
        
        #=======================================================================
        # GUI
        #=======================================================================
        #VIEW   
        self.gui = {}     
        self.gui['view'] = source.ui.RaceInfoProxyView        
        
        #FILTER
        self.gui['filter'] = source.ui.RaceInfoFilterLineEdit
        self.gui['filterclear'] = source.ui.RaceInfoFilterClear
        
        #GROUPBOX #todo move to model
        self.gui['add'] = None
        self.gui['remove'] =  None
        self.gui['export'] = source.ui.RaceInfoExport
        self.gui['export_www'] = None
        self.gui['import'] = None 
        self.gui['delete'] = None
        
        #COUNTER
        self.gui['counter'] = source.ui.RaceInfoCounter
        
        #=======================================================================
        # classes
        #=======================================================================        
        self.classModel = RaceInfoModel                              
        self.classProxyModel = RaceInfoProxyModel
                

class RaceInfoModel(myModel.myModel):
    def __init__(self, params):                        
        
        #create MODEL and his structure
        myModel.myModel.__init__(self, params)        
                            

                
    def getDefaultTableRow(self): 
        category = myModel.myModel.getDefaultTableRow(self)                
        category['name'] = "unknown"        
        return category 
    
    def update(self, parameter=None, value=None, conditions=None, operation=None):
        """
        update model z databaze
          
        update() => update cele tabulky
        update(parameter, value) => vsechny radky s parametrem = value
        update(conditions, operation) => condition[0][0]=condition[0][1] OPERATION condition[1][0]=condition[1][1] 
        """
        
        #run_id                
        run_id = self.params.tabTimes.model.run_id
        
        #disable user actions        
        self.params.datastore.Set("user_actions", self.params.datastore.Get("user_actions")+1)          
                      
        #smazat vsechny radky
        self.removeRows(0, self.rowCount())                                                                                                                                              
        
        row_id = 1
        
        #race        
        row = {}
        row["id"] = row_id
        row["name"] = "Run id:"+ str(run_id)
        row["start_list"] = self.params.tabUser.getCount()  
        row["ok"] = self.params.tabUser.getCount("ok")  
        row["dns"] = self.params.tabUser.getCount("dns")  
        row["dnq"] = self.params.tabUser.getCount("dnq")  
        row["dnf"] = self.params.tabUser.getCount("dnf")              
        row["finished"] = self.params.tabTimes.getCount(run_id)
        row["awaited"] = row["start_list"] - row["dns"] - row["dnq"] - row["dnf"] - row["finished"]            
        row_table = self.db2tableRow(row)
        self.addRow(row_table)
        row_id =  row_id + 1
        
        #categories
        dbCategories = self.params.tabCategories.getDbRows()                      
        for dbCategory in dbCategories:                                                                                            
            
            row = {}
            row["id"] = row_id
            row["name"] = dbCategory["name"]
            row["start_list"] = self.params.tabUser.getCount(dbCategory = dbCategory)  
            row["ok"] = self.params.tabUser.getCount("ok", dbCategory)  
            row["dns"] = self.params.tabUser.getCount("dns", dbCategory)  
            row["dnq"] = self.params.tabUser.getCount("dnq", dbCategory)  
            row["dnf"] = self.params.tabUser.getCount("dnf", dbCategory)              
            row["finished"] = self.params.tabTimes.getCount(run_id, dbCategory)
            row["awaited"] = row["start_list"] - row["dns"] - row["dnq"] - row["dnf"] - row["finished"]            
            row_table = self.db2tableRow(row)
            self.addRow(row_table)
            row_id =  row_id + 1
            #print row_table           

        
#        for row_dict in row_dicts:            
#            #call table-specific function, return "table-row"                                           
#            row_table = self.db2tableRow(row_dict)                                                                                                                                                     
#            #add row to the table             
#            self.addRow(row_table)

        #enable user actions                                                                                                                                                                                                           
        self.params.datastore.Set("user_actions", self.params.datastore.Get("user_actions")-1)
        
        
                    
class RaceInfoProxyModel(myModel.myProxyModel):
    def __init__(self, params):                        
        
        #default proxy-model constructor
        myModel.myProxyModel.__init__(self, params)  
        

# view <- proxymodel <- model 
class RaceInfo(myModel.myTable):
    def  __init__(self, params):                                             
         
        #default table constructor
        myModel.myTable.__init__(self, params)
        
        self.params.gui['view'].sortByColumn(0, QtCore.Qt.AscendingOrder)
        
    #v modelu tahle funkce šahá do db, raceinfo nema tabulku v db        
    def updateDbCounter(self):
        pass
        
                            


        
       


        
        
            
            

        
        
    