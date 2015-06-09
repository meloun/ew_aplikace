# -*- coding: utf-8 -*-
'''
Created on 8.12.2013

@author: Meloun
'''

from PyQt4 import QtCore
from ewitis.data.DEF_ENUM_STRINGS import *
from ewitis.gui.UiAccesories import uiAccesories
from libs.myqt.mydialogs import *
from ewitis.gui.Ui import Ui
from ewitis.data.dstore import dstore
import libs.utils.utils as utils

class HeaderGroup():    
    def __init__(self,  index):
        '''
        Constructor
        group items as class members        
        '''
        ui = Ui()        
        self.index = index
                                
        self.racename = getattr(ui, "lineExportHeaderRace"+str(index+1))  
        self.categoryname = getattr(ui, "lineExportHeaderCategory"+str(index+1))                                            
        self.description = getattr(ui, "lineExportHeaderDescription"+str(index+1))

    def CreateSlots(self):                
        QtCore.QObject.connect(self.racename, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("export_header", [self.index, "racename"],  utils.toUnicode(name)))                 
        QtCore.QObject.connect(self.categoryname, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("export_header", [self.index, "categoryname"],  utils.toUnicode(name)))        
        QtCore.QObject.connect(self.description, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("export_header", [self.index, "description"],  utils.toUnicode(name)))        
            
    def GetInfo(self):
        return dstore.GetItem("export_header", [self.index])
    
    def Update(self):        
        # set values from datastore              
        info = self.GetInfo() 
        uiAccesories.UpdateText(self.racename, info["racename"])  
        uiAccesories.UpdateText(self.categoryname, info["categoryname"])                                            
        uiAccesories.UpdateText(self.description, info["description"])                                            

class FilterSortGroup():    
    def __init__(self,  index):
        '''
        Constructor
        group items as class members        
        '''
        ui = Ui()        
        self.index = index
                                
        self.type = getattr(ui,    "comboExportType_" + str(index+1))
        self.filter = getattr(ui,    "comboExportFilter_" + str(index+1))
        self.sort1 = getattr(ui, "comboExportSort1_" + str(index+1))                                
        self.sortorder1 = getattr(ui,  "comboExportSortOrder1_" + str(index+1))
        self.sort2 = getattr(ui, "comboExportSort2_" + str(index+1))                             
        self.sortorder2 = getattr(ui,  "comboExportSortOrder2_" + str(index+1))                                              

    def CreateSlots(self):
        
        
        QtCore.QObject.connect(self.type, QtCore.SIGNAL("activated(const QString&)"), lambda x: dstore.SetItem("export_filtersort", [self.index, "type"], utils.toUnicode(x)))
        QtCore.QObject.connect(self.filter, QtCore.SIGNAL("activated(const QString&)"), lambda x: dstore.SetItem("export_filtersort", [self.index, "filter"], utils.toUnicode(x)))
                                                     
        QtCore.QObject.connect(self.sort1, QtCore.SIGNAL("activated(const QString&)"), lambda x: dstore.SetItem("export_filtersort", [self.index, "sort1"], utils.toUnicode(x)))                          
        QtCore.QObject.connect(self.sortorder1, QtCore.SIGNAL("activated(const QString&)"), lambda x: dstore.SetItem("export_filtersort", [self.index, "sortorder1"], utils.toUnicode(x)))
        QtCore.QObject.connect(self.sort2, QtCore.SIGNAL("activated(const QString&)"), lambda x: dstore.SetItem("export_filtersort", [self.index, "sort2"], utils.toUnicode(x)))                          
        QtCore.QObject.connect(self.sortorder2, QtCore.SIGNAL("activated(const QString&)"), lambda x: dstore.SetItem("export_filtersort", [self.index, "sortorder2"], utils.toUnicode(x)))
                           
            
    def GetInfo(self):
        return dstore.GetItem("export_filtersort", [self.index])
     
    def setEnabled(self, enabled):
        self.type.setEnabled(enabled)
        self.filter.setEnabled(enabled)   
        self.sort1.setEnabled(enabled)        
        self.sortorder1.setEnabled(enabled)
        self.sort2.setEnabled(enabled)        
        self.sortorder2.setEnabled(enabled)
    
    def Update(self):        
        # set values from datastore              
        info = self.GetInfo()                                
                                                     
        uiAccesories.SetCurrentIndex(self.type, info["type"])
        uiAccesories.SetCurrentIndex(self.filter, info["filter"])        
         
        uiAccesories.SetCurrentIndex(self.sort1, info["sort1"])
        uiAccesories.SetCurrentIndex(self.sortorder1, info["sortorder1"])
        
        uiAccesories.SetCurrentIndex(self.sort2, info["sort2"])
        uiAccesories.SetCurrentIndex(self.sortorder2, info["sortorder2"])
        

        
        


class ExportGroup():
    
    def __init__(self,  index):
        '''
        Constructor
        group items as class members
        format groupCell_1, checkCell_1.. groupCell_2, checkCell_2 
        '''
        ui = Ui()
        
        self.index = index
        self.enable_csv = getattr(ui, "pushExportCsvEnable_" + str(index+1))
        self.enable_htm = getattr(ui, "pushExportHtmEnable_" + str(index+1))
        
        #three columns groups
        self.time = [None] * NUMBER_OF.THREECOLUMNS
        self.lap = [None] * NUMBER_OF.THREECOLUMNS        
        self.order = [None] * NUMBER_OF.THREECOLUMNS        
        self.ordercat = [None] * NUMBER_OF.THREECOLUMNS        
        self.points = [None] * NUMBER_OF.POINTSCOLUMNS  
        self.un = [None] * NUMBER_OF.THREECOLUMNS  
        self.us = [None] * 1
              
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            self.time[i] = getattr(ui, "checkExportTime_"+str(i+1)+"_" + str(index+1)) 
            self.lap[i] = getattr(ui, "checkExportLap_"+str(i+1)+"_" + str(index+1))
            self.order[i] = getattr(ui, "checkExportOrder_"+str(i+1)+"_" + str(index+1))
            self.ordercat[i] = getattr(ui, "checkExportOrderCat_"+str(i+1)+"_" + str(index+1))
            self.points[i] = getattr(ui, "checkExportPoints_"+str(i+1)+"_" + str(index+1))
            self.un[i] = getattr(ui, "checkExportUn_"+str(i+1)+"_" + str(index+1))
            
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            self.points[i] = getattr(ui, "checkExportPoints_"+str(i+1)+"_" + str(index+1))

        i=0            
        self.us[i] = getattr(ui, "checkExportUs_"+str(i+1)+"_" + str(index+1))
         
         
        self.nr = getattr(ui, "checkExportNumber_" + str(index+1))
        self.name = getattr(ui, "checkExportName_" + str(index+1))
        self.category = getattr(ui, "checkExportCategory_" + str(index+1))
        self.year = getattr(ui, "checkExportYear_" + str(index+1))        
        self.sex = getattr(ui, "checkExportSex_" + str(index+1))        
        self.club = getattr(ui, "checkExportClub_" + str(index+1))      
                        
        self.option = [None] * NUMBER_OF.OPTIONCOLUMNS                
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):
            self.option[i] = getattr(ui, "checkExportOption_"+str(i+1)+"_" + str(index+1))
                                
        
        self.gap = getattr(ui, "checkExportGap_" + str(index+1))        
        self.status = getattr(ui, "checkExportStatus_" + str(index+1))    
        
        
        #collumns sorting
        self.s_time = [None] * NUMBER_OF.THREECOLUMNS
        self.s_lap = [None] * NUMBER_OF.THREECOLUMNS        
        self.s_order = [None] * NUMBER_OF.THREECOLUMNS        
        self.s_ordercat = [None] * NUMBER_OF.THREECOLUMNS        
        self.s_points = [None] * NUMBER_OF.POINTSCOLUMNS  
        self.s_un = [None] * NUMBER_OF.THREECOLUMNS  
        self.s_us = [None] * 1
              
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            self.s_time[i] = getattr(ui, "spinExportSortTime"+str(i+1)+"_" + str(index+1)) 
            self.s_lap[i] = getattr(ui, "spinExportSortLap"+str(i+1)+"_" + str(index+1))
            self.s_order[i] = getattr(ui, "spinExportSortOrder"+str(i+1)+"_" + str(index+1))
            self.s_ordercat[i] = getattr(ui, "spinExportSortOrderCat"+str(i+1)+"_" + str(index+1))
            self.s_points[i] = getattr(ui, "spinExportSortPoints"+str(i+1)+"_" + str(index+1))
            self.s_un[i] = getattr(ui, "spinExportSortUn"+str(i+1)+"_" + str(index+1))
            
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            self.s_points[i] = getattr(ui, "spinExportSortPoints"+str(i+1)+"_" + str(index+1))

        i=0            
        self.s_us[i] = getattr(ui, "spinExportSortUs"+str(i+1)+"_" + str(index+1))         
         
        self.s_nr = getattr(ui, "spinExportSortNumber_" + str(index+1))
        self.s_name = getattr(ui, "spinExportSortName_" + str(index+1))
        self.s_category = getattr(ui, "spinExportSortCategory_" + str(index+1))
        self.s_year = getattr(ui, "spinExportSortYear_" + str(index+1))        
        self.s_sex = getattr(ui, "spinExportSortSex_" + str(index+1))        
        self.s_club = getattr(ui, "spinExportSortClub_" + str(index+1))     
        
        self.s_option = [None] * NUMBER_OF.OPTIONCOLUMNS                
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):
            self.s_option[i] = getattr(ui, "spinExportSortOption"+str(i+1)+"_" + str(index+1))
                                        
        self.s_gap = getattr(ui, "spinExportSortGap_" + str(index+1))        
        self.s_status = getattr(ui, "spinExportSortStatus_" + str(index+1))
        
                
                                                  
                    
        
    def Init(self):        
        self.Update()
        self.createSlots()            

    def CreateSlots(self):                
 
        #export        
        QtCore.QObject.connect(self.enable_csv, QtCore.SIGNAL('toggled(bool)'), lambda state: dstore.SetItem("export", ["enabled_csv", self.index], state))
        QtCore.QObject.connect(self.enable_htm, QtCore.SIGNAL('toggled(bool)'), lambda state: dstore.SetItem("export", ["enabled_htm", self.index], state))
        
        """columns enable checkboxes """
        
        #three columns groups
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            QtCore.QObject.connect(self.time[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, idx = i: dstore.SetItem("export", ["checked", self.index, "time"+str(idx+1)], state)) 
            QtCore.QObject.connect(self.lap[i], QtCore.SIGNAL("stateChanged(int)"), lambda state,  idx = i: dstore.SetItem("export", ["checked", self.index, "lap"+str(idx+1)], state))                                            
            QtCore.QObject.connect(self.order[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, idx = i: dstore.SetItem("export", ["checked", self.index, "order"+str(idx+1)], state))
            QtCore.QObject.connect(self.ordercat[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, idx = i: dstore.SetItem("export", ["checked", self.index, "ordercat"+str(idx+1)], state))
            QtCore.QObject.connect(self.un[i], QtCore.SIGNAL("stateChanged(int)"), lambda state,  idx = i: dstore.SetItem("export", ["checked", self.index, "un"+str(idx+1)], state))
            
        i=0
        QtCore.QObject.connect(self.us[i], QtCore.SIGNAL("stateChanged(int)"), lambda state,  idx = i: dstore.SetItem("export", ["checked", self.index, "us"+str(idx+1)], state))
               
        QtCore.QObject.connect(self.nr, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: dstore.SetItem("export", ["checked", idx, "nr"], state))                                
        QtCore.QObject.connect(self.name, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: dstore.SetItem("export", ["checked", idx, "name"], state))                                
        QtCore.QObject.connect(self.category, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: dstore.SetItem("export", ["checked", idx, "category"], state))                                
        QtCore.QObject.connect(self.year, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: dstore.SetItem("export", ["checked", idx, "year"], state))                                
        QtCore.QObject.connect(self.sex, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: dstore.SetItem("export", ["checked", idx, "sex"], state))                                
        QtCore.QObject.connect(self.club, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: dstore.SetItem("export", ["checked", idx, "club"], state))
                                
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):  
            QtCore.QObject.connect(self.option[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, idx = i: dstore.SetItem("export", ["checked", self.index, "o"+str(idx+1)], state))            
            

        QtCore.QObject.connect(self.gap, QtCore.SIGNAL("stateChanged(int)"), lambda state: dstore.SetItem("export", ["checked", self.index, "gap"], state))
        
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            QtCore.QObject.connect(self.points[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, idx = i: dstore.SetItem("export", ["checked", self.index, "points"+str(idx+1)], state)) 
                
        QtCore.QObject.connect(self.status, QtCore.SIGNAL("stateChanged(int)"), lambda state: dstore.SetItem("export", ["checked", self.index, "status"], state))
        
        
        """columns sorting """
        
        #three columns groups
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            QtCore.QObject.connect(self.s_time[i], QtCore.SIGNAL("valueChanged(int)"), lambda state, idx = i: dstore.SetItem("export", ["sorted", self.index, "time"+str(idx+1)], state)) 
            QtCore.QObject.connect(self.s_lap[i], QtCore.SIGNAL("valueChanged(int)"), lambda state,  idx = i: dstore.SetItem("export", ["sorted", self.index, "lap"+str(idx+1)], state))                                            
            QtCore.QObject.connect(self.s_order[i], QtCore.SIGNAL("valueChanged(int)"), lambda state, idx = i: dstore.SetItem("export", ["sorted", self.index, "order"+str(idx+1)], state))
            QtCore.QObject.connect(self.s_ordercat[i], QtCore.SIGNAL("valueChanged(int)"), lambda state, idx = i: dstore.SetItem("export", ["sorted", self.index, "ordercat"+str(idx+1)], state))
            QtCore.QObject.connect(self.s_un[i], QtCore.SIGNAL("valueChanged(int)"), lambda state,  idx = i: dstore.SetItem("export", ["sorted", self.index, "un"+str(idx+1)], state))
            
        i=0
        QtCore.QObject.connect(self.s_us[i], QtCore.SIGNAL("valueChanged(int)"), lambda state,  idx = i: dstore.SetItem("export", ["sorted", self.index, "us"+str(idx+1)], state))
               
        QtCore.QObject.connect(self.s_nr, QtCore.SIGNAL("valueChanged(int)"), lambda state, idx=self.index: dstore.SetItem("export", ["sorted", idx, "nr"], state))                                
        QtCore.QObject.connect(self.s_name, QtCore.SIGNAL("valueChanged(int)"), lambda state, idx=self.index: dstore.SetItem("export", ["sorted", idx, "name"], state))                                
        QtCore.QObject.connect(self.s_category, QtCore.SIGNAL("valueChanged(int)"), lambda state, idx=self.index: dstore.SetItem("export", ["sorted", idx, "category"], state))                                
        QtCore.QObject.connect(self.s_year, QtCore.SIGNAL("valueChanged(int)"), lambda state, idx=self.index: dstore.SetItem("export", ["sorted", idx, "year"], state))                                
        QtCore.QObject.connect(self.s_sex, QtCore.SIGNAL("valueChanged(int)"), lambda state, idx=self.index: dstore.SetItem("export", ["sorted", idx, "sex"], state))                                
        QtCore.QObject.connect(self.s_club, QtCore.SIGNAL("valueChanged(int)"), lambda state, idx=self.index: dstore.SetItem("export", ["sorted", idx, "club"], state))
                                
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):  
            QtCore.QObject.connect(self.s_option[i], QtCore.SIGNAL("valueChanged(int)"), lambda state, idx = i: dstore.SetItem("export", ["sorted", self.index, "o"+str(idx+1)], state))            
            

        QtCore.QObject.connect(self.s_gap, QtCore.SIGNAL("valueChanged(int)"), lambda state: dstore.SetItem("export", ["sorted", self.index, "gap"], state))
        
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            QtCore.QObject.connect(self.s_points[i], QtCore.SIGNAL("valueChanged(int)"), lambda state, idx = i: dstore.SetItem("export", ["sorted", self.index, "points"+str(idx+1)], state)) 
                
        QtCore.QObject.connect(self.s_status, QtCore.SIGNAL("valueChanged(int)"), lambda state: dstore.SetItem("export", ["sorted", self.index, "status"], state))   
                

    def setEnabled(self, enabled):        
        
        for i in range(0, NUMBER_OF.THREECOLUMNS):                
            self.time[i].setEnabled(enabled)         
            self.lap[i].setEnabled(enabled)          
            self.order[i].setEnabled(enabled)            
            self.ordercat[i].setEnabled(enabled)            
            self.un[i].setEnabled(enabled)            
        self.us[0].setEnabled(enabled)            
        self.nr.setEnabled(enabled)        
        self.name.setEnabled(enabled)        
        self.category.setEnabled(enabled)        
        self.year.setEnabled(enabled)        
        self.sex.setEnabled(enabled)          
        self.club.setEnabled(enabled)    
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):                                                                        
            self.option[i].setEnabled(enabled)        
        #self.gap.setEnabled(enabled) 
        self.status.setEnabled(enabled) 
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):                
            self.points[i].setEnabled(enabled)
        self.status.setEnabled(enabled)
        
        #sorting columns 
        checked_info = self.GetCheckedInfo()        
        
        #print checked_info
        for i in range(0, NUMBER_OF.THREECOLUMNS):              
            self.s_time[i].setEnabled(enabled  and  bool(checked_info["time"+str(i+1)]))         
            self.s_lap[i].setEnabled(enabled   and  bool(checked_info["lap"+str(i+1)]))          
            self.s_order[i].setEnabled(enabled and  bool(checked_info["order"+str(i+1)]))            
            self.s_ordercat[i].setEnabled(enabled and  bool(checked_info["ordercat"+str(i+1)]))            
            self.s_un[i].setEnabled(enabled and bool(checked_info["un"+str(i+1)]))            
        self.s_us[0].setEnabled(enabled and bool(checked_info["us"+str(0+1)]))            
        self.s_nr.setEnabled(enabled and bool(checked_info["nr"]))        
        self.s_name.setEnabled(enabled and bool(checked_info["name"]))        
        self.s_category.setEnabled(enabled and bool(checked_info["category"]))        
        self.s_year.setEnabled(enabled and bool(checked_info["year"]))        
        self.s_sex.setEnabled(enabled and bool(checked_info["sex"]))          
        self.s_club.setEnabled(enabled and bool(checked_info["club"]))    
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):                                                                        
            self.s_option[i].setEnabled(enabled and bool(checked_info["o"+str(i+1)]))        
        self.s_gap.setEnabled(enabled  and bool(checked_info["gap"])) 
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):                
            self.s_points[i].setEnabled(enabled and bool(checked_info["points"+str(i+1)]))
        self.s_status.setEnabled(enabled and bool(checked_info["status"])) 
         
        
    
    def GetCheckedInfo(self):        
        return dstore.GetItem("export", ["checked", self.index])
        
    def GetSortedInfo(self):                
        return dstore.GetItem("export", ["sorted", self.index])    
    
    def IsEnabled(self, key = None):
        if key == "csv":
            return bool(dstore.GetItem("export", ["enabled_csv", self.index]))
        elif key == "htm":
            return bool(dstore.GetItem("export", ["enabled_htm", self.index]))
        else:                  
            return bool(dstore.GetItem("export", ["enabled_csv", self.index]) or dstore.GetItem("export", ["enabled_htm", self.index])) 
              
    def GetCheckedColumns(self, only_checked = True):
        """
        vrací list zaškrtnutých sloupců, seřazených podle "export, sortkeys"
        """
        info = self.GetCheckedInfo()
        aux_list = []        
        
        if(self.IsEnabled() == False):
            return aux_list                
                
        if only_checked:
            keys = [k for k, v in info.items() if v!=0]
        else:
            keys = info.keys()
                    
        keys_order = dstore.GetItem("export", ["sorted", self.index])   
        #print "KEYS: ", keys      
        #print "ORDER: ", keys_order
        aux_list =  sorted(keys, key=lambda k: keys_order[k])  
        #print "RESULT: ", aux_list      
                                               
        return aux_list

    
    def Update(self):        
        changed = False
        checked_info = self.GetCheckedInfo()
        checked_columns = self.GetCheckedColumns()
        
        self.setEnabled(self.IsEnabled())
        
        #enabled in additional info        
        if(self.IsEnabled()):
            ai = dstore.Get("additional_info")
            for i in range(0, NUMBER_OF.THREECOLUMNS):                
                if(ai["time"][i]["checked"] == 0):
                    dstore.SetItem("export", ["checked", self.index, "time"+str(i+1)], 0)
                    self.time[i].setEnabled(False)                
                    self.s_time[i].setEnabled(False)                
                if(ai["lap"][i]["checked"] == 0):                    
                    self.lap[i].setEnabled(False)
                    self.s_lap[i].setEnabled(False)
                    dstore.SetItem("export", ["checked", self.index, "lap"+str(i+1)], 0)                       
                if(ai["order"][i]["checked"] == 0):
                    dstore.SetItem("export", ["checked", self.index, "order"+str(i+1)], 0)                              
                    self.order[i].setEnabled(False)                          
                if(ai["order"][i]["checked"] == 0):
                    dstore.SetItem("export", ["checked", self.index, "ordercat"+str(i+1)], 0)                              
                    self.ordercat[i].setEnabled(False)                          
                if(ai["un"][i]["checked"] == 0):                            
                    dstore.SetItem("export", ["checked", self.index, "un"+str(i+1)], 0)                              
                    self.un[i].setEnabled(False)
                    self.s_un[i].setEnabled(False)
            for i in range(0, NUMBER_OF.POINTSCOLUMNS):                
                if(ai["points"][i]["checked"] == 0):
                    dstore.SetItem("export", ["checked", self.index, "points"+str(i+1)], 0)                              
                    self.points[i].setEnabled(False)
                    self.s_points[i].setEnabled(False)
                                        
            i = 0
            if(ai["us"][i]["checked"] == 0):                
                dstore.SetItem("export", ["checked", self.index, "us"+str(i+1)], 0)                              
                self.us[i].setEnabled(False)             
                self.s_us[i].setEnabled(False)             
                
            if(checked_columns != self.GetCheckedColumns()):                
                changed = True #because of dialog from tab race settings: aditional info
            
        
        enabled_csv_state = dstore.GetItem("export", ["enabled_csv", self.index])
        self.enable_csv.setChecked(enabled_csv_state)
        font = self.enable_csv.font()
        font.setBold(enabled_csv_state)
        self.enable_csv.setFont(font)
        
        enabled_htm_state = dstore.GetItem("export", ["enabled_htm", self.index])
        self.enable_htm.setChecked(enabled_htm_state)
        font = self.enable_htm.font()
        font.setBold(enabled_htm_state)
        self.enable_htm.setFont(font)
        
        """enabled checkboxes"""
        
        #three columns groups                       
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            self.time[i].setCheckState(checked_info["time"+str(i+1)])
            self.lap[i].setCheckState(checked_info["lap"+str(i+1)])                              
            self.order[i].setCheckState(checked_info["order"+str(i+1)])             
            self.ordercat[i].setCheckState(checked_info["ordercat"+str(i+1)])             
            self.un[i].setCheckState(checked_info["un"+str(i+1)])
            
        i=0        
        self.us[i].setCheckState(checked_info["us"+str(i+1)])             
        
        self.nr.setCheckState(checked_info["nr"])                                
        self.name.setCheckState(checked_info["name"])                                
        self.category.setCheckState(checked_info["category"])                                
        self.year.setCheckState(checked_info["year"])                                
        self.sex.setCheckState(checked_info["sex"])                                
        self.club.setCheckState(checked_info["club"])                                
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):                                                                        
            self.option[i].setCheckState(checked_info["o"+str(i+1)])        
        #self.gap.setCheckState(checked_info["gap"])
        self.status.setCheckState(checked_info["status"])
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):                
            self.points[i].setCheckState(checked_info["points"+str(i+1)])
             
        """sorting spinboxes"""
        sorted_info = self.GetSortedInfo()
        
        #three columns groups                       
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            self.s_time[i].setValue(sorted_info["time"+str(i+1)])
            self.s_lap[i].setValue(sorted_info["lap"+str(i+1)])                              
            self.s_order[i].setValue(sorted_info["order"+str(i+1)])             
            self.s_ordercat[i].setValue(sorted_info["ordercat"+str(i+1)])             
            self.s_un[i].setValue(sorted_info["un"+str(i+1)])
            
        i=0        
        self.s_us[i].setValue(sorted_info["us"+str(i+1)])             
        
        self.s_nr.setValue(sorted_info["nr"])                                
        self.s_name.setValue(sorted_info["name"])                                
        self.s_category.setValue(sorted_info["category"])                                
        self.s_year.setValue(sorted_info["year"])                                
        self.s_sex.setValue(sorted_info["sex"])                                
        self.s_club.setValue(sorted_info["club"])                                
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):                                                                        
            self.s_option[i].setValue(sorted_info["o"+str(i+1)])        
        self.s_gap.setValue(sorted_info["gap"])
        self.s_status.setValue(sorted_info["status"])
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):                
            self.s_points[i].setValue(sorted_info["points"+str(i+1)]) 
            
        return changed
            
class NamesGroup():
    
    def __init__(self):
        '''
        Constructor
        group items as class members
        format groupCell_1, checkCell_1.. groupCell_2, checkCell_2 
        '''
        ui = Ui()
        
        #three columns groups
        self.time = [None] * NUMBER_OF.THREECOLUMNS
        self.lap = [None] * NUMBER_OF.THREECOLUMNS        
        self.order = [None] * NUMBER_OF.THREECOLUMNS        
        self.ordercat = [None] * NUMBER_OF.THREECOLUMNS        
        self.points = [None] * NUMBER_OF.POINTSCOLUMNS  
        self.un = [None] * NUMBER_OF.THREECOLUMNS  
        self.us = [None] * 1  
              
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            self.time[i] = getattr(ui, "lineExportNameTime"+str(i+1)) 
            self.lap[i] = getattr(ui, "lineExportNameLap"+str(i+1))
            self.order[i] = getattr(ui, "lineExportNameOrder"+str(i+1))
            self.ordercat[i] = getattr(ui, "lineExportNameOrderCat"+str(i+1))
            self.points[i] = getattr(ui, "lineExportNamePoints"+str(i+1))
            self.un[i] = getattr(ui, "lineExportNameUn"+str(i+1))
        i=0
        self.us[i] = getattr(ui, "lineExportNameUs"+str(i+1))
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            self.points[i] = getattr(ui, "lineExportNamePoints"+str(i+1))
         
        self.nr = getattr(ui, "lineExportNameNr")
        self.name = getattr(ui, "lineExportNameName")
        self.category = getattr(ui, "lineExportNameCategory")
        self.year = getattr(ui, "lineExportNameYear")        
        self.sex = getattr(ui, "lineExportNameSex")        
        self.club = getattr(ui, "lineExportNameClub")        

                
        self.option = [None] * NUMBER_OF.OPTIONCOLUMNS                
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):
            self.option[i] = getattr(ui, "lineExportNameOption"+str(i+1))        
                                
        self.gap = getattr(ui, "lineExportNameGap")                                                  
        
    def Init(self):        
        self.Update()
        self.createSlots()            

    def CreateSlots(self):
        
        #three columns groups
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            QtCore.QObject.connect(self.order[i], QtCore.SIGNAL("textEdited(const QString&)"), lambda name, idx = i: dstore.SetItem("export", ["names", "order"+str(idx+1)],  utils.toUnicode(name)))
            QtCore.QObject.connect(self.ordercat[i], QtCore.SIGNAL("textEdited(const QString&)"), lambda name, idx = i: dstore.SetItem("export", ["names", "ordercat"+str(idx+1)],  utils.toUnicode(name)))
            QtCore.QObject.connect(self.time[i], QtCore.SIGNAL("textEdited(const QString&)"), lambda name, idx = i: dstore.SetItem("export", ["names", "time"+str(idx+1)],  utils.toUnicode(name))) 
            QtCore.QObject.connect(self.lap[i], QtCore.SIGNAL("textEdited(const QString&)"), lambda name, idx = i: dstore.SetItem("export", ["names", "lap"+str(idx+1)],  utils.toUnicode(name)))                                            
            QtCore.QObject.connect(self.un[i], QtCore.SIGNAL("textEdited(const QString&)"), lambda name, idx = i: dstore.SetItem("export", ["names", "un"+str(idx+1)],  utils.toUnicode(name)))
        i=0                                            
        QtCore.QObject.connect(self.us[i], QtCore.SIGNAL("textEdited(const QString&)"), lambda name, idx = i: dstore.SetItem("export", ["names", "us"+str(idx+1)],  utils.toUnicode(name)))                                            
               
        QtCore.QObject.connect(self.nr, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("export", ["names", "nr"],  utils.toUnicode(name)))                                
        QtCore.QObject.connect(self.name, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("export", ["names", "name"],  utils.toUnicode(name)))                                
        QtCore.QObject.connect(self.category, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("export", ["names", "category"],  utils.toUnicode(name)))                                
        QtCore.QObject.connect(self.year, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("export", ["names", "year"],  utils.toUnicode(name)))                                
        QtCore.QObject.connect(self.sex, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("export", ["names", "sex"],  utils.toUnicode(name)))                                
        QtCore.QObject.connect(self.club, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("export", ["names", "club"],  utils.toUnicode(name)))
                                
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):  
            QtCore.QObject.connect(self.option[i], QtCore.SIGNAL("textEdited(const QString&)"),  lambda name, idx = i: dstore.SetItem("export", ["names", "o"+str(idx+1)],  utils.toUnicode(name)))            
            

        QtCore.QObject.connect(self.gap, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("export", [self.index, "gap"],  utils.toUnicode(name)))
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            QtCore.QObject.connect(self.points[i], QtCore.SIGNAL("textEdited(const QString&)"),  lambda name, idx = i: dstore.SetItem("export", ["names", "points"+str(idx+1)],  utils.toUnicode(name))) 
                

    def setEnabled(self, enabled):
        
        self.enable.setChecked(enabled)
        
        for i in range(0, NUMBER_OF.THREECOLUMNS):                
            self.order[i].setEnabled(enabled)            
            self.ordercat[i].setEnabled(enabled)            
            self.time[i].setEnabled(enabled)         
            self.lap[i].setEnabled(enabled)          
            self.un[i].setEnabled(enabled)          
        self.us[0].setEnabled(enabled)          
        self.nr.setEnabled(enabled)        
        self.name.setEnabled(enabled)        
        self.category.setEnabled(enabled)        
        self.year.setEnabled(enabled)        
        self.sex.setEnabled(enabled)          
        self.club.setEnabled(enabled)    
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):                                                                        
            self.option[i].setEnabled(enabled)        
        #self.gap.setEnabled(enabled) 
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):                
            self.points[i].setEnabled(enabled) 
        
    
    def GetInfo(self):        
        return dstore.GetItem("export", ["names"])    

    
    def Update(self):
        info = self.GetInfo()
        #print "I",info
        
        #three columns groups               
        #print export_info
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            uiAccesories.UpdateText(self.order[i], info["order"+str(i+1)])
            uiAccesories.UpdateText(self.ordercat[i], info["ordercat"+str(i+1)])
            uiAccesories.UpdateText(self.time[i], info["time"+str(i+1)])
            uiAccesories.UpdateText(self.lap[i], info["lap"+str(i+1)])
            uiAccesories.UpdateText(self.un[i], info["un"+str(i+1)])
        i=0
        uiAccesories.UpdateText(self.un[i], info["un"+str(i+1)])
                      
        uiAccesories.UpdateText(self.nr, info["nr"])                                
        uiAccesories.UpdateText(self.name, info["name"])                                
        uiAccesories.UpdateText(self.category, info["category"])                                
        uiAccesories.UpdateText(self.year, info["year"])                                
        uiAccesories.UpdateText(self.sex, info["sex"])                                
        uiAccesories.UpdateText(self.club, info["club"])                                
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):                                                                        
            uiAccesories.UpdateText(self.option[i], info["o"+str(i+1)])        
        #uiAccesories.UpdateText(self.gap, info["gap"])
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):                
            uiAccesories.UpdateText(self.points[i], info["points"+str(i+1)]) 
        
class WWWExportGroup():
    
    def __init__(self, index):
        '''
        Constructor
        group items as class members
        format groupCell_1, checkCell_1.. groupCell_2, checkCell_2 
        '''
        ui = Ui()
        
        self.index = index
        
        #three columns groups
        self.css_filename = [None]
        self.load_css_filename = [None]
               
        
        self.filename = getattr(ui, "lineExportCss"+str(index+1)) 
        self.load_filename = getattr(ui, "pushExportLoadCss"+str(index+1)) 
        
    def Init(self):        
        self.Update()
        self.createSlots()            

    def CreateSlots(self):
                        
        QtCore.QObject.connect(self.load_filename,  QtCore.SIGNAL('clicked()'), self.sLoadCssFilename)
        QtCore.QObject.connect(self.filename, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: dstore.SetItem("export_www", [self.index, "css_filename"], utils.toUnicode(name)))
            
    def sLoadCssFilename(self):
        print "sLoadCssFilename"                            

    def setEnabled(self, enabled):        
                               
        self.load_filename.setEnabled(enabled)            
        self.filename.setEnabled(enabled)
        
    
    def GetInfo(self):                
        return dstore.GetItem("export_www", [self.index])    

    
    def Update(self):
        info = self.GetInfo()                                            
        uiAccesories.UpdateText(self.filename, info["css_filename"])
        
        

class TabExportSettings():    
      
    def __init__(self):
        '''
        Constructor
        '''        
        print "tabExportSettings: constructor"        
        
    def Init(self):                     
        self.addSlots()
        
    def addSlots(self):        
                       
        print "I: tabExportSettings: adding slots.."
        
        #exportgroups - year, club, etc.
        self.namesgroup = [None] * NUMBER_OF.EXPORTS
        self.exportgroups = [None] * NUMBER_OF.EXPORTS
        self.headergroups = [None] * NUMBER_OF.EXPORTS 
        self.wwwgroups = [None] * NUMBER_OF.EXPORTS 
        self.filtersortgroups = [None] * NUMBER_OF.EXPORTS        
        for i in range(0, NUMBER_OF.EXPORTS):            
            self.headergroups[i] = HeaderGroup(i)
            self.headergroups[i].CreateSlots()
            self.wwwgroups[i] = WWWExportGroup(i)
            self.wwwgroups[i].CreateSlots()
            self.filtersortgroups[i] = FilterSortGroup(i)
            self.filtersortgroups[i].CreateSlots()
            self.exportgroups[i] = ExportGroup(i)
            self.exportgroups[i].CreateSlots()
        self.namesgroup = NamesGroup()
        self.namesgroup.CreateSlots()
        
            
        
            
        QtCore.QObject.connect(Ui().radioExportLapsTimes,      QtCore.SIGNAL("toggled(bool)"), lambda index: dstore.SetItem("export_laps", ["column"], 0) if index else None)
        QtCore.QObject.connect(Ui().radioExportLapsLaptimes,  QtCore.SIGNAL("toggled(bool)"), lambda index: dstore.SetItem("export_laps", ["column"], 1) if index else None) 
        QtCore.QObject.connect(Ui().radioExportLapsPoints_1,  QtCore.SIGNAL("toggled(bool)"), lambda index: dstore.SetItem("export_laps", ["column"], 2) if index else None) 
        QtCore.QObject.connect(Ui().radioExportLapsPoints_2,  QtCore.SIGNAL("toggled(bool)"), lambda index: dstore.SetItem("export_laps", ["column"], 3) if index else None) 
        QtCore.QObject.connect(Ui().radioExportLapsPoints_3,  QtCore.SIGNAL("toggled(bool)"), lambda index: dstore.SetItem("export_laps", ["column"], 4) if index else None)                                       
            
    def IsEnabled(self, index, key = None):
        return self.exportgroups[index].IsEnabled(key)
         
    def Update(self, mode = UPDATE_MODE.all):                                
                                                  
        #export        
        #exportgroups                
        changed = False        
        self.namesgroup.Update()             
        for i in range(0, NUMBER_OF.EXPORTS):
            self.headergroups[i].Update()
            self.wwwgroups[i].Update()
            self.filtersortgroups[i].Update()                        
            a = self.exportgroups[i].Update()            
            changed = changed or a            
            
            column = dstore.GetItem("export_laps", ["column"])
            if column == ExportLapsFormat.FORMAT_TIMES:
                Ui().radioExportLapsTimes.setChecked(True)            
                Ui().radioExportLapsLaptimes.setChecked(False)
                Ui().radioExportLapsPoints_1.setChecked(False)
                Ui().radioExportLapsPoints_2.setChecked(False)
                Ui().radioExportLapsPoints_3.setChecked(False)
            elif column == ExportLapsFormat.FORMAT_LAPTIMES:            
                Ui().radioExportLapsTimes.setChecked(False)            
                Ui().radioExportLapsLaptimes.setChecked(True)
                Ui().radioExportLapsPoints_1.setChecked(False)
                Ui().radioExportLapsPoints_2.setChecked(False)
                Ui().radioExportLapsPoints_3.setChecked(False)
            elif column == ExportLapsFormat.FORMAT_POINTS_1:            
                Ui().radioExportLapsTimes.setChecked(False)            
                Ui().radioExportLapsLaptimes.setChecked(False)
                Ui().radioExportLapsPoints_1.setChecked(True)                                
                Ui().radioExportLapsPoints_2.setChecked(False)
                Ui().radioExportLapsPoints_3.setChecked(False)
            elif column == ExportLapsFormat.FORMAT_POINTS_2:            
                Ui().radioExportLapsTimes.setChecked(False)            
                Ui().radioExportLapsLaptimes.setChecked(False)
                Ui().radioExportLapsPoints_1.setChecked(False)                                
                Ui().radioExportLapsPoints_2.setChecked(True)
                Ui().radioExportLapsPoints_3.setChecked(False)
            elif column == ExportLapsFormat.FORMAT_POINTS_3:            
                Ui().radioExportLapsTimes.setChecked(False)            
                Ui().radioExportLapsLaptimes.setChecked(False)
                Ui().radioExportLapsPoints_1.setChecked(False)                                
                Ui().radioExportLapsPoints_2.setChecked(False)
                Ui().radioExportLapsPoints_3.setChecked(True)
            else:
                print "error: export laptimes"
                
        if(changed == True):            
            uiAccesories.showMessage("Additional info", "The column was disabled also for all exports.\n\n See the export tab. \n ", MSGTYPE.warning)
                
        #print dstore.Get("export")                                    
                                
        return True
    
tabExportSettings = TabExportSettings() 