# -*- coding: utf-8 -*-
'''
Created on 8.12.2013

@author: Meloun
'''

from PyQt4 import QtCore
from ewitis.data.DEF_ENUM_STRINGS import *
from ewitis.gui.UiAccesories import uiAccesories
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

    def CreateSlots(self):                
        QtCore.QObject.connect(self.racename, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: uiAccesories.sGuiSetItem("export_header", ["header", self.index, "racename"],  utils.toUnicode(name), self.Update))                 
        QtCore.QObject.connect(self.categoryname, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: uiAccesories.sGuiSetItem("export_header", ["header", self.index, "categoryname"],  utils.toUnicode(name), self.Update))        
            
    def GetInfo(self):
        return dstore.GetItem("export_header", [self.index])
    
    def Update(self):        
        # set values from datastore              
        info = self.GetInfo() 
        uiAccesories.UpdateText(self.racename, info["racename"])  
        uiAccesories.UpdateText(self.categoryname, info["categoryname"])                                            

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
        
        
        QtCore.QObject.connect(self.type, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("export_filtersort", [self.index, "type"], utils.toUnicode(x)))
        QtCore.QObject.connect(self.filter, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("export_filtersort", [self.index, "filter"], utils.toUnicode(x)))
                      
        QtCore.QObject.connect(self.sort1, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("export_filtersort", [self.index, "sort1"], utils.toUnicode(x)))                          
        QtCore.QObject.connect(self.sortorder1, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("export_filtersort", [self.index, "sortorder1"], utils.toUnicode(x)))
        QtCore.QObject.connect(self.sort2, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("export_filtersort", [self.index, "sort2"], utils.toUnicode(x)))                          
        QtCore.QObject.connect(self.sortorder2, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("export_filtersort", [self.index, "sortorder2"], utils.toUnicode(x)))
                           
            
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
        self.points = [None] * NUMBER_OF.THREECOLUMNS  
              
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            self.time[i] = getattr(ui, "checkExportTime_"+str(i+1)+"_" + str(index+1)) 
            self.lap[i] = getattr(ui, "checkExportLap_"+str(i+1)+"_" + str(index+1))
            self.order[i] = getattr(ui, "checkExportOrder_"+str(i+1)+"_" + str(index+1))
            self.points[i] = getattr(ui, "checkExportPoints_"+str(i+1)+"_" + str(index+1))
         
         
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
        
        
                
                                                  
                    
        
    def Init(self):        
        self.Update()
        self.createSlots()            

    def CreateSlots(self):                
 
        #export        
        QtCore.QObject.connect(self.enable_csv, QtCore.SIGNAL('toggled(bool)'), lambda state: uiAccesories.sGuiSetItem("export", ["enabled_csv", self.index], state, self.Update))
        QtCore.QObject.connect(self.enable_htm, QtCore.SIGNAL('toggled(bool)'), lambda state: uiAccesories.sGuiSetItem("export", ["enabled_htm", self.index], state, self.Update))
        
        #three columns groups
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            QtCore.QObject.connect(self.time[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, idx = i: uiAccesories.sGuiSetItem("export", ["checked", self.index, "time"+str(idx+1)], state, self.Update)) 
            QtCore.QObject.connect(self.order[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, idx = i: uiAccesories.sGuiSetItem("export", ["checked", self.index, "order"+str(idx+1)], state, self.Update))
            QtCore.QObject.connect(self.lap[i], QtCore.SIGNAL("stateChanged(int)"), lambda state,  idx = i: uiAccesories.sGuiSetItem("export", ["checked", self.index, "lap"+str(idx+1)], state, self.Update))                                            
               
        QtCore.QObject.connect(self.nr, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: uiAccesories.sGuiSetItem("export", ["checked", idx, "nr"], state, self.Update))                                
        QtCore.QObject.connect(self.name, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: uiAccesories.sGuiSetItem("export", ["checked", idx, "name"], state, self.Update))                                
        QtCore.QObject.connect(self.category, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: uiAccesories.sGuiSetItem("export", ["checked", idx, "category"], state, self.Update))                                
        QtCore.QObject.connect(self.year, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: uiAccesories.sGuiSetItem("export", ["checked", idx, "year"], state, self.Update))                                
        QtCore.QObject.connect(self.sex, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: uiAccesories.sGuiSetItem("export", ["checked", idx, "sex"], state, self.Update))                                
        QtCore.QObject.connect(self.club, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: uiAccesories.sGuiSetItem("export", ["checked", idx, "club"], state, self.Update))
                                
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):  
            QtCore.QObject.connect(self.option[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, idx = i: uiAccesories.sGuiSetItem("export", ["checked", self.index, "option"+str(idx+1)], state, self.Update))            
            

        QtCore.QObject.connect(self.gap, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", ["checked", self.index, "gap"], state, self.Update))
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            QtCore.QObject.connect(self.points[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, idx = i: uiAccesories.sGuiSetItem("export", ["checked", self.index, "points"+str(idx+1)], state, self.Update)) 
                

    def setEnabled(self, enabled):        
        
        for i in range(0, NUMBER_OF.THREECOLUMNS):                
            self.time[i].setEnabled(enabled)         
            self.lap[i].setEnabled(enabled)          
            self.order[i].setEnabled(enabled)            
        self.nr.setEnabled(enabled)        
        self.name.setEnabled(enabled)        
        self.category.setEnabled(enabled)        
        self.year.setEnabled(enabled)        
        self.sex.setEnabled(enabled)          
        self.club.setEnabled(enabled)    
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):                                                                        
            self.option[i].setEnabled(enabled)        
        self.gap.setEnabled(enabled) 
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):                
            self.points[i].setEnabled(enabled) 
        
    
    def GetCheckedInfo(self):        
        return dstore.GetItem("export", ["checked", self.index])    
    
    def IsEnabled(self, key = None):
        if key == "csv":
            return bool(dstore.GetItem("export", ["enabled_csv", self.index]))
        elif key == "htm":
            return bool(dstore.GetItem("export", ["enabled_htm", self.index]))
        else:                  
            return bool(dstore.GetItem("export", ["enabled_csv", self.index]) or dstore.GetItem("export", ["enabled_htm", self.index])) 
              
    def GetCheckedCollumns(self):
        """
        vrací list zaškrtnutých sloupců, seřazených podle "export, sortkeys"
        """
        info = self.GetCheckedInfo()
        aux_list = []        
        
        if(self.IsEnabled() == False):
            return aux_list                
                
        keys = {k: v for k, v in info.items() if v!=0}                
        keys_order = dstore.GetItem("export", ["sorted"])         
        aux_list =  sorted(keys, key=lambda k: keys_order.index(k))
                                               
        return aux_list

    
    def Update(self):        
        checked_info = self.GetCheckedInfo()
        
        self.setEnabled(self.IsEnabled())
        
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
        
        #three columns groups               
        #print export_info
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            self.time[i].setCheckState(checked_info["time"+str(i+1)])
            self.lap[i].setCheckState(checked_info["lap"+str(i+1)])                              
            self.order[i].setCheckState(checked_info["order"+str(i+1)])             

        
        self.nr.setCheckState(checked_info["nr"])                                
        self.name.setCheckState(checked_info["name"])                                
        self.category.setCheckState(checked_info["category"])                                
        self.year.setCheckState(checked_info["year"])                                
        self.sex.setCheckState(checked_info["sex"])                                
        self.club.setCheckState(checked_info["club"])                                
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):                                                                        
            self.option[i].setCheckState(checked_info["option"+str(i+1)])        
        self.gap.setCheckState(checked_info["gap"])
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):                
            self.points[i].setCheckState(checked_info["points"+str(i+1)]) 
            
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
        self.points = [None] * NUMBER_OF.THREECOLUMNS  
              
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            self.time[i] = getattr(ui, "lineExportNameTime"+str(i+1)) 
            self.lap[i] = getattr(ui, "lineExportNameLap"+str(i+1))
            self.order[i] = getattr(ui, "lineExportNameOrder"+str(i+1))
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
            QtCore.QObject.connect(self.time[i], QtCore.SIGNAL("textEdited(const QString&)"), lambda name, idx = i: uiAccesories.sGuiSetItem("export", ["names", "time"+str(idx+1)],  utils.toUnicode(name), self.Update)) 
            QtCore.QObject.connect(self.order[i], QtCore.SIGNAL("textEdited(const QString&)"), lambda name, idx = i: uiAccesories.sGuiSetItem("export", ["names", "order"+str(idx+1)],  utils.toUnicode(name), self.Update))
            QtCore.QObject.connect(self.lap[i], QtCore.SIGNAL("textEdited(const QString&)"), lambda name, idx = i: uiAccesories.sGuiSetItem("export", ["names", "lap"+str(idx+1)],  utils.toUnicode(name), self.Update))                                            
               
        QtCore.QObject.connect(self.nr, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: uiAccesories.sGuiSetItem("export", ["names", "nr"],  utils.toUnicode(name), self.Update))                                
        QtCore.QObject.connect(self.name, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: uiAccesories.sGuiSetItem("export", ["names", "name"],  utils.toUnicode(name), self.Update))                                
        QtCore.QObject.connect(self.category, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: uiAccesories.sGuiSetItem("export", ["names", "category"],  utils.toUnicode(name), self.Update))                                
        QtCore.QObject.connect(self.year, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: uiAccesories.sGuiSetItem("export", ["names", "year"],  utils.toUnicode(name), self.Update))                                
        QtCore.QObject.connect(self.sex, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: uiAccesories.sGuiSetItem("export", ["names", "sex"],  utils.toUnicode(name), self.Update))                                
        QtCore.QObject.connect(self.club, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: uiAccesories.sGuiSetItem("export", ["names", "club"],  utils.toUnicode(name), self.Update))
                                
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):  
            QtCore.QObject.connect(self.option[i], QtCore.SIGNAL("textEdited(const QString&)"),  lambda name, idx = i: uiAccesories.sGuiSetItem("export", ["names", "option"+str(idx+1)],  utils.toUnicode(name), self.Update))            
            

        QtCore.QObject.connect(self.gap, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: uiAccesories.sGuiSetItem("export", [self.index, "gap"],  utils.toUnicode(name), self.Update))
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            QtCore.QObject.connect(self.points[i], QtCore.SIGNAL("textEdited(const QString&)"),  lambda name, idx = i: uiAccesories.sGuiSetItem("export", ["names", "points"+str(idx+1)],  utils.toUnicode(name), self.Update)) 
                

    def setEnabled(self, enabled):
        
        self.enable.setChecked(enabled)
        
        for i in range(0, NUMBER_OF.THREECOLUMNS):                
            self.time[i].setEnabled(enabled)         
            self.lap[i].setEnabled(enabled)          
            self.order[i].setEnabled(enabled)            
        self.nr.setEnabled(enabled)        
        self.name.setEnabled(enabled)        
        self.category.setEnabled(enabled)        
        self.year.setEnabled(enabled)        
        self.sex.setEnabled(enabled)          
        self.club.setEnabled(enabled)    
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):                                                                        
            self.option[i].setEnabled(enabled)        
        self.gap.setEnabled(enabled) 
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
            uiAccesories.UpdateText(self.time[i], info["time"+str(i+1)])
            uiAccesories.UpdateText(self.lap[i], info["lap"+str(i+1)])
            uiAccesories.UpdateText(self.order[i], info["order"+str(i+1)])
                      
        uiAccesories.UpdateText(self.nr, info["nr"])                                
        uiAccesories.UpdateText(self.name, info["name"])                                
        uiAccesories.UpdateText(self.category, info["category"])                                
        uiAccesories.UpdateText(self.year, info["year"])                                
        uiAccesories.UpdateText(self.sex, info["sex"])                                
        uiAccesories.UpdateText(self.club, info["club"])                                
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):                                                                        
            uiAccesories.UpdateText(self.option[i], info["option"+str(i+1)])        
        uiAccesories.UpdateText(self.gap, info["gap"])
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):                
            uiAccesories.UpdateText(self.points[i], info["points"+str(i+1)]) 
        
        

class TabExportSettings():    
      
    def __init__(self):
        '''
        Constructor
        '''        
        print "tabExportSettings: constructor"        
        
    def Init(self):                     
        self.addSlots()
        
    def addSlots(self):        
               
        print "tabExportSettings: adding slots"
        
        #exportgroups - year, club, etc.
        self.namesgroup = [None] * NUMBER_OF.EXPORTS
        self.exportgroups = [None] * NUMBER_OF.EXPORTS
        self.headergroups = [None] * NUMBER_OF.EXPORTS 
        self.filtersortgroups = [None] * NUMBER_OF.EXPORTS        
        for i in range(0, NUMBER_OF.EXPORTS):            
            self.headergroups[i] = HeaderGroup(i)
            self.headergroups[i].CreateSlots()
            self.filtersortgroups[i] = FilterSortGroup(i)
            self.filtersortgroups[i].CreateSlots()
            self.exportgroups[i] = ExportGroup(i)
            self.exportgroups[i].CreateSlots()
        self.namesgroup = NamesGroup()
        self.namesgroup.CreateSlots()
        
            
        
            
        QtCore.QObject.connect(Ui().radioExportLapsTimes,      QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("export_laps", ["column"], 0, self.Update) if index else None)
        QtCore.QObject.connect(Ui().radioExportLapsLaptimes,  QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("export_laps", ["column"], 1, self.Update) if index else None) 
        QtCore.QObject.connect(Ui().radioExportLapsPoints_1,  QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("export_laps", ["column"], 2, self.Update) if index else None) 
        QtCore.QObject.connect(Ui().radioExportLapsPoints_2,  QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("export_laps", ["column"], 3, self.Update) if index else None) 
        QtCore.QObject.connect(Ui().radioExportLapsPoints_3,  QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("export_laps", ["column"], 4, self.Update) if index else None)                                       
            
    def IsEnabled(self, index, key = None):
        return self.exportgroups[index].IsEnabled(key)
         
    def Update(self, mode = UPDATE_MODE.all):                                
                                                  
        #export        
        #exportgroups
        self.namesgroup.Update()             
        for i in range(0, NUMBER_OF.EXPORTS):
            self.headergroups[i].Update()
            self.filtersortgroups[i].Update()            
            self.exportgroups[i].Update()
            
            
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
                
        #print dstore.Get("export")                                    
                                
        return True
    
tabExportSettings = TabExportSettings() 