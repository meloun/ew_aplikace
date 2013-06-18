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
       
        #disable user actions        
        self.params.datastore.Set("user_actions", self.params.datastore.Get("user_actions")+1)          
                      
        #smazat vsechny radky
        self.removeRows(0, self.rowCount())          
        
        #ziskat radky z databaze DB                                                
        #rows = self.params.db.getAll(self.params.name)        
        #row_dicts = self.params.db.cursor2dicts(rows)                                                
                                                                                                    
        #pridat radky do modelu/tabulky
        row_dicts = [
            {"id":1,"name":"kategorie A", "start_list":151, "dns":5,"dnq":5,"dnf":5, "finished":55, "awaited":16},
            {"id":2,"name":"kategorie B", "start_list":151, "dns":5,"dnq":5,"dnf":5, "finished":54, "awaited":17},
            {"id":3,"name":"kategorie C", "start_list":151, "dns":5,"dnq":5,"dnf":5, "finished":53, "awaited":18},
            ]         
            
                            
        for row_dict in row_dicts:            
            #call table-specific function, return "table-row"                                           
            row_table = self.db2tableRow(row_dict)                                                                                                                                                     
            #add row to the table             
            self.addRow(row_table)

        #enable user actions                                                                                                                                                                                                   
        self.params.datastore.Set("user_actions", self.params.datastore.Get("user_actions")-1)
        print "CountStartList:", self.CountStartList("ok")
        print "CountFinished:", self.CountFinished(185)
        
    #todo: move to users file
    def CountStartList(self, state, dbCategory = None):                                                                        
        
        if dbCategory:
            res = self.params.db.getParXX("users", [["state", state], ["category_id", dbCategory["id"]]], "AND")
        else:
            res = self.params.db.getParX("users", "state", state)
        return res
    #todo: move to times file
    def CountFinished(self, run_id, dbCategory = None):                        
        
        query = " SELECT * from times"
        
        if(self.params.datastore.Get('rfid') == 2):
            query = query + \
                " INNER JOIN tags ON times.user_id = tags.tag_id"+\
                " INNER JOIN users ON tags.user_nr = users.nr "
        else:
            query = query + \
            " INNER JOIN users ON times.user_id = users.id"
            
        query = query + \
                " WHERE (times.run_id = "+str(run_id)+")"\
                    " AND (users.state = \"ok\")"
        if dbCategory:                        
            query = query + \
                    " AND (users.category_id = "+dbCategory["id"]+")"
        query = query + \
            " GROUP by times.user_id"
        
        return query
        res = self.query(query)
        return res
        
                    
class RaceInfoProxyModel(myModel.myProxyModel):
    def __init__(self, params):                        
        
        #default proxy-model constructor
        myModel.myProxyModel.__init__(self, params)  
        

# view <- proxymodel <- model 
class RaceInfo(myModel.myTable):
    def  __init__(self, params):                                             
         
        #default table constructor
        myModel.myTable.__init__(self, params)
        
    #v modelu tahle funkce šahá do db, raceinfo nema tabulku v db        
    def updateDbCounter(self):
        pass
        
                            


        
       


        
        
            
            

        
        
    