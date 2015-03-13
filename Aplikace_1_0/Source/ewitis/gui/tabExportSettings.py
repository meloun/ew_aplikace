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

class FilterSortGroup():    
    def __init__(self,  index):
        '''
        Constructor
        group items as class members        
        '''
        ui = Ui()        
        self.index = index
                                
        self.filter = getattr(ui,    "comboExportFilter_" + str(index+1))
        self.sort1 = getattr(ui, "comboExportSort1_" + str(index+1))                                
        self.sortorder1 = getattr(ui,  "comboExportSortOrder1_" + str(index+1))
        self.sort2 = getattr(ui, "comboExportSort2_" + str(index+1))                             
        self.sortorder2 = getattr(ui,  "comboExportSortOrder2_" + str(index+1))                                              

    def CreateSlots(self):
        
        
        QtCore.QObject.connect(self.filter, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("export_filtersort", [self.index, "filter"], utils.toUnicode(x)))
                      
        QtCore.QObject.connect(self.sort1, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("export_filtersort", [self.index, "sort1"], utils.toUnicode(x)))                          
        QtCore.QObject.connect(self.sortorder1, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("export_filtersort", [self.index, "sortorder1"], utils.toUnicode(x)))
        QtCore.QObject.connect(self.sort2, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("export_filtersort", [self.index, "sort2"], utils.toUnicode(x)))                          
        QtCore.QObject.connect(self.sortorder2, QtCore.SIGNAL("activated(const QString&)"), lambda x: uiAccesories.sGuiSetItem("export_filtersort", [self.index, "sortorder2"], utils.toUnicode(x)))
                           
            
    def GetInfo(self):
        return dstore.GetItem("export_filtersort", [self.index])
     
    def setEnabled(self, enabled):
        self.filter.setEnabled(enabled)   
        self.sort1.setEnabled(enabled)        
        self.sortorder1.setEnabled(enabled)
        self.sort2.setEnabled(enabled)        
        self.sortorder2.setEnabled(enabled)
    
    def Update(self):        
        # set values from datastore              
        info = self.GetInfo()                                
                                                     
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
        self.enable = getattr(ui, "pushExportEnable_" + str(index+1))
        
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
        self.optionname = getattr(ui, "lineExportOptionname_"+str(index+1))
                                
        self.gap = getattr(ui, "checkExportGap_" + str(index+1))
        
        
                
                                                  
                    
        
    def Init(self):        
        self.Update()
        self.createSlots()            

    def CreateSlots(self):                
 
        #export        
        QtCore.QObject.connect(self.enable, QtCore.SIGNAL('toggled(bool)'), lambda state: uiAccesories.sGuiSetItem("export", [self.index, "enabled"], state, self.Update))
        
        #three columns groups
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            QtCore.QObject.connect(self.time[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, idx = i: uiAccesories.sGuiSetItem("export", [self.index, "time", idx], state, self.Update)) 
            QtCore.QObject.connect(self.order[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, idx = i: uiAccesories.sGuiSetItem("export", [self.index, "order", idx], state, self.Update))
            QtCore.QObject.connect(self.lap[i], QtCore.SIGNAL("stateChanged(int)"), lambda state,  idx = i: uiAccesories.sGuiSetItem("export", [self.index, "lap" , idx], state, self.Update))                                            
               
        QtCore.QObject.connect(self.nr, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: uiAccesories.sGuiSetItem("export", [idx, "nr"], state, self.Update))                                
        QtCore.QObject.connect(self.name, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: uiAccesories.sGuiSetItem("export", [idx, "name"], state, self.Update))                                
        QtCore.QObject.connect(self.category, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: uiAccesories.sGuiSetItem("export", [idx, "category"], state, self.Update))                                
        QtCore.QObject.connect(self.year, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: uiAccesories.sGuiSetItem("export", [idx, "year"], state, self.Update))                                
        QtCore.QObject.connect(self.sex, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: uiAccesories.sGuiSetItem("export", [idx, "sex"], state, self.Update))                                
        QtCore.QObject.connect(self.club, QtCore.SIGNAL("stateChanged(int)"), lambda state, idx=self.index: uiAccesories.sGuiSetItem("export", [idx, "club"], state, self.Update))
                                
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):  
            QtCore.QObject.connect(self.option[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, idx = i: uiAccesories.sGuiSetItem("export", [self.index, "option", idx], state, self.Update))
            QtCore.QObject.connect(self.optionname, QtCore.SIGNAL("textEdited(const QString&)"), lambda name, idx = i: uiAccesories.sGuiSetItem("export", [self.index, "optionname", idx], utils.toUnicode(name)))
            

        QtCore.QObject.connect(self.gap, QtCore.SIGNAL("stateChanged(int)"), lambda state: uiAccesories.sGuiSetItem("export", [self.index, "gap"], state, self.Update))
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):
            QtCore.QObject.connect(self.points[i], QtCore.SIGNAL("stateChanged(int)"), lambda state, idx = i: uiAccesories.sGuiSetItem("export", [self.index, "points", idx], state, self.Update)) 
                

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
        #self.optionname.setEnabled(enabled) #spolecne pro vsechny
        self.gap.setEnabled(enabled) 
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):                
            self.points[i].setEnabled(enabled) 
        
    
    def GetInfo(self):        
        return dstore.GetItem("export", [self.index])          
    def GetAsList(self):
        info = self.GetInfo()
        aux_list = []
        
        if(info['enabled'] == False):
            return aux_list
        
        for k,v in info.items():
            if isinstance(v, int):
                if(v !=0):                
                    aux_list.append(k)
            else:
                for i,v2 in enumerate(v):
                    if isinstance(v2, int) and (v2 !=0):                
                        aux_list.append(k+str(i+1))                                                 
        return aux_list

    
    def Update(self):
        export_info = self.GetInfo()
        
        self.setEnabled(export_info["enabled"])
        
        #three columns groups               
        for i in range(0, NUMBER_OF.THREECOLUMNS):
            self.time[i].setCheckState(export_info["time"][i])
            self.lap[i].setCheckState(export_info["lap"][i])                                
            self.order[i].setCheckState(export_info["order"][i])             

        
        self.nr.setCheckState(export_info["nr"])                                
        self.name.setCheckState(export_info["name"])                                
        self.category.setCheckState(export_info["category"])                                
        self.year.setCheckState(export_info["year"])                                
        self.sex.setCheckState(export_info["sex"])                                
        self.club.setCheckState(export_info["club"])                                
        #self.laptime.setCheckState(export_info["laptime"])
        #self.bestlaptime.setCheckState(export_info["best_laptime"])
        for i in range(0, NUMBER_OF.OPTIONCOLUMNS):                                                                        
            self.option[i].setCheckState(export_info["option"][i])
        self.optionname.setText(export_info["optionname"][i])
        self.gap.setCheckState(export_info["gap"])
        for i in range(0, NUMBER_OF.POINTSCOLUMNS):                
            self.points[i].setCheckState(export_info["points"][i])
        
        

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
        self.exportgroups = [None] * NUMBER_OF.EXPORTS
        self.filtersortgroups = [None] * NUMBER_OF.EXPORTS
        for i in range(0, NUMBER_OF.EXPORTS):            
            self.exportgroups[i] = ExportGroup(i)
            self.exportgroups[i].CreateSlots()
            self.filtersortgroups[i] = FilterSortGroup(i)
            self.filtersortgroups[i].CreateSlots()
            
        QtCore.QObject.connect(Ui().radioExportLapsTimes,      QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("export_laps", ["column"], 0, self.Update) if index else None)
        QtCore.QObject.connect(Ui().radioExportLapsLaptimes,  QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("export_laps", ["column"], 1, self.Update) if index else None) 
        QtCore.QObject.connect(Ui().radioExportLapsPoints_1,  QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("export_laps", ["column"], 2, self.Update) if index else None) 
        QtCore.QObject.connect(Ui().radioExportLapsPoints_2,  QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("export_laps", ["column"], 3, self.Update) if index else None) 
        QtCore.QObject.connect(Ui().radioExportLapsPoints_3,  QtCore.SIGNAL("toggled(bool)"), lambda index: uiAccesories.sGuiSetItem("export_laps", ["column"], 4, self.Update) if index else None)                                       
            
        
    def Update(self, mode = UPDATE_MODE.all):                                
                                                  
        #export        
        #exportgroups
        for i in range(0, NUMBER_OF.EXPORTS):             
            self.exportgroups[i].Update()
            self.filtersortgroups[i].Update()            
            
            
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