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
        self.headertext = getattr(ui, "lineExportHeaderText"+str(index+1))
        self.categoryname = getattr(ui, "lineExportHeaderCategory"+str(index+1))                                            
        self.description = getattr(ui, "lineExportHeaderDescription"+str(index+1))

    def CreateSlots(self):                
        QtCore.QObject.connect(self.racename, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("export_header", [self.index, "racename"],  utils.toUnicode(name)))                 
        QtCore.QObject.connect(self.headertext, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("export_header", [self.index, "headertext"],  utils.toUnicode(name)))
        QtCore.QObject.connect(self.categoryname, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("export_header", [self.index, "categoryname"],  utils.toUnicode(name)))        
        QtCore.QObject.connect(self.description, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("export_header", [self.index, "description"],  utils.toUnicode(name)))        
            
    def GetInfo(self):
        return dstore.GetItem("export_header", [self.index])
    
    def Update(self):        
        # set values from datastore              
        info = self.GetInfo() 
        uiAccesories.UpdateText(self.racename, info["racename"])  
        uiAccesories.UpdateText(self.headertext, info["headertext"])
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
                                
        self.onerow = getattr(ui,  "checkExportOnerow_" + str(index+1))
        self.type = getattr(ui,    "comboExportType_" + str(index+1))
        self.filter = getattr(ui,    "comboExportFilter_" + str(index+1))
        self.sort1 = getattr(ui, "comboExportSort1_" + str(index+1))                                
        self.sortorder1 = getattr(ui,  "comboExportSortOrder1_" + str(index+1))
        self.sort2 = getattr(ui, "comboExportSort2_" + str(index+1))                             
        self.sortorder2 = getattr(ui,  "comboExportSortOrder2_" + str(index+1))                                              

    def CreateSlots(self):
        
        
        QtCore.QObject.connect(self.onerow, QtCore.SIGNAL("stateChanged(int)"), lambda x: dstore.SetItem("export_filtersort", [self.index, "onerow"], x))
        QtCore.QObject.connect(self.type, QtCore.SIGNAL("activated(const QString&)"), lambda x: dstore.SetItem("export_filtersort", [self.index, "type"], utils.toUnicode(x)))
        QtCore.QObject.connect(self.filter, QtCore.SIGNAL("activated(const QString&)"), lambda x: dstore.SetItem("export_filtersort", [self.index, "filter"], utils.toUnicode(x)))
                                                     
        QtCore.QObject.connect(self.sort1, QtCore.SIGNAL("activated(const QString&)"), lambda x: dstore.SetItem("export_filtersort", [self.index, "sort1"], utils.toUnicode(x)))                          
        QtCore.QObject.connect(self.sortorder1, QtCore.SIGNAL("activated(const QString&)"), lambda x: dstore.SetItem("export_filtersort", [self.index, "sortorder1"], utils.toUnicode(x)))
        QtCore.QObject.connect(self.sort2, QtCore.SIGNAL("activated(const QString&)"), lambda x: dstore.SetItem("export_filtersort", [self.index, "sort2"], utils.toUnicode(x)))                          
        QtCore.QObject.connect(self.sortorder2, QtCore.SIGNAL("activated(const QString&)"), lambda x: dstore.SetItem("export_filtersort", [self.index, "sortorder2"], utils.toUnicode(x)))
                           
            
    def GetInfo(self):
        return dstore.GetItem("export_filtersort", [self.index])
     
    def setEnabled(self, enabled):
        self.onerow.setEnabled(enabled)
        self.type.setEnabled(enabled)
        self.filter.setEnabled(enabled)   
        self.sort1.setEnabled(enabled)        
        self.sortorder1.setEnabled(enabled)
        self.sort2.setEnabled(enabled)        
        self.sortorder2.setEnabled(enabled)
    
    def Update(self):        
        # set values from datastore              
        info = self.GetInfo()                                
                                                     
        self.onerow.setCheckState(info["onerow"])
        
        uiAccesories.SetCurrentIndex(self.type, info["type"])
        uiAccesories.SetCurrentIndex(self.filter, info["filter"])        
         
        uiAccesories.SetCurrentIndex(self.sort1, info["sort1"])
        uiAccesories.SetCurrentIndex(self.sortorder1, info["sortorder1"])
        
        uiAccesories.SetCurrentIndex(self.sort2, info["sort2"])
        uiAccesories.SetCurrentIndex(self.sortorder2, info["sortorder2"])
        

        
        


 
        
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
        self.transpose = getattr(ui, "checkExportTranspose"+str(index+1))
        self.firsttimes = getattr(ui, "spinExportFirsttimes"+str(index+1)) 
        self.lasttimes = getattr(ui, "spinExportLasttimes"+str(index+1))                      
        self.css_filename = getattr(ui, "lineExportCss"+str(index+1)) 
        self.css_load_filename = getattr(ui, "pushExportLoadCss"+str(index+1))
        self.js_filename = getattr(ui, "lineExportJs"+str(index+1)) 
        self.js_load_filename = getattr(ui, "pushExportLoadJs"+str(index+1))  
        
    def Init(self):        
        self.Update()
        self.createSlots()            

    def CreateSlots(self):
                        
        QtCore.QObject.connect(self.transpose, QtCore.SIGNAL("stateChanged(int)"), lambda x: dstore.SetItem("export_www", [self.index, "transpose"], x))
        QtCore.QObject.connect(self.firsttimes, QtCore.SIGNAL("valueChanged(int)"), lambda state: dstore.SetItem("export_www", [self.index, "firsttimes"], state))
        QtCore.QObject.connect(self.lasttimes, QtCore.SIGNAL("valueChanged(int)"), lambda state: dstore.SetItem("export_www", [self.index, "lasttimes"], state))
        QtCore.QObject.connect(self.css_load_filename,  QtCore.SIGNAL('clicked()'), self.sLoadCssFilename)
        QtCore.QObject.connect(self.css_filename, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: dstore.SetItem("export_www", [self.index, "css_filename"], utils.toUnicode(name)))
        QtCore.QObject.connect(self.js_load_filename,  QtCore.SIGNAL('clicked()'), self.sLoadJsFilename)
        QtCore.QObject.connect(self.js_filename, QtCore.SIGNAL("textEdited(const QString&)"), lambda name: dstore.SetItem("export_www", [self.index, "js_filename"], utils.toUnicode(name)))
            
    def sLoadCssFilename(self):
        print "sLoadCssFilename"
    def sLoadJsFilename(self):
        print "sLoadJsFilename"                                

    """
    def setEnabled(self, enabled):        
                               
        self.css_load_filename.setEnabled(enabled)            
        self.css_filename.setEnabled(enabled)
        self.js_load_filename.setEnabled(enabled)            
        self.js_filename.setEnabled(enabled)
     """   
    
    def GetInfo(self):                
        return dstore.GetItem("export_www", [self.index])    

    
    def Update(self):
        info = self.GetInfo()        
        self.transpose.setCheckState(info["transpose"])
        self.firsttimes.setValue(info["firsttimes"])         
        self.lasttimes.setValue(info["lasttimes"])                                                
        uiAccesories.UpdateText(self.css_filename, info["css_filename"])
        uiAccesories.UpdateText(self.js_filename, info["js_filename"])
        
class SmsExportGroup():
    NR_FORWARD = 2
    NR_COLLUMNS = 2
    
    def __init__(self, index):
        ''' Constructor '''
        ui = Ui()        
        self.index = index
        
        
                
        #one column
        if(self.index == 0):
            self.phone_column = [None] * self.NR_COLLUMNS
            self.forward_usernr = [None] * self.NR_FORWARD
            self.forward_phonenr = [None] * self.NR_FORWARD
            
            for i in range(0, self.NR_COLLUMNS): 
                self.phone_column[i] = getattr(ui,    "comboExportPhoneColumn" + str(i+1))
            for i in range(0, self.NR_FORWARD):
                self.forward_usernr[i] = getattr(ui,  "spinExportForwardUsernr" + str(i+1))
                self.forward_phonenr[i] = getattr(ui, "lineExportForwardPhonenr" + str(i+1))
            
        #three columns groups
        self.text = getattr(ui, "textExportSms"+str(index+1))  
        self.lcd = getattr(ui, "lcdExportSms"+str(index+1))
        
    def Init(self):        
        self.Update()
        self.createSlots()            

    def CreateSlots(self):  
        if(self.index == 0):
            for i in range(0, self.NR_COLLUMNS):
                QtCore.QObject.connect(self.phone_column[i], QtCore.SIGNAL("activated(const QString&)"), lambda x, idx = i: dstore.SetItem("export_sms", ["phone_column", idx], utils.toUnicode(x)))
            for i in range(0, self.NR_FORWARD):
                QtCore.QObject.connect(self.forward_usernr[i], QtCore.SIGNAL("valueChanged(int)"), lambda state, idx = i: dstore.SetItem("export_sms", ["forward", idx, "user_nr"], state))
                QtCore.QObject.connect(self.forward_phonenr[i], QtCore.SIGNAL("textEdited(const QString&)"), lambda name, idx = i: dstore.SetItem("export_sms", ["forward", idx, "phone_nr"], utils.toUnicode(name)))
    
        QtCore.QObject.connect(self.text, QtCore.SIGNAL("textChanged()"), self.sTextChanged)                                

            
    """                 """
    """ EXPLICIT SLOTS  """
    """                 """
    def sTextChanged(self):                    
        uiAccesories.sGuiSetItem("export_sms", ["text", self.index], utils.toUnicode( self.text.toPlainText()), self.Update)
        self.lcd.display(self.text.toPlainText().length())
                                        
    
    def GetInfo(self):                
        return dstore.Get("export_sms")    
    
    def Update(self):
        info = self.GetInfo() 
        
        if(self.index == 0):
            for i in range(0, self.NR_COLLUMNS):
                uiAccesories.SetCurrentIndex(self.phone_column[i], info["phone_column"][i])
            for i in range(0, self.NR_FORWARD):
                self.forward_usernr[i].setValue(info["forward"][i]["user_nr"])
                uiAccesories.UpdateText(self.forward_phonenr[i], info["forward"][i]["phone_nr"])
                  
        uiAccesories.UpdateText(self.text, info["text"][self.index])                                                                              
                

class TabExportSettings():    
      
    def __init__(self):
        '''
        Constructor
        '''                  
        print "I: CREATE: tabExportSettings"      
        
    def Init(self):                     
        self.addSlots()
        
    def addSlots(self):        
                               
        print "I: SLOTS: tabExportSettings"
        
        #exportgroups - year, club, etc.

        self.headergroups = [None] * NUMBER_OF.EXPORTS 
        self.wwwgroups = [None] * NUMBER_OF.EXPORTS 
        self.smsgroups = [None] * NUMBER_OF.EXPORTS
        self.filtersortgroups = [None] * NUMBER_OF.EXPORTS        
        for i in range(0, NUMBER_OF.EXPORTS):            
            self.headergroups[i] = HeaderGroup(i)
            self.headergroups[i].CreateSlots()
            self.wwwgroups[i] = WWWExportGroup(i)
            self.wwwgroups[i].CreateSlots()
            self.smsgroups[i] = SmsExportGroup(i)
            self.smsgroups[i].CreateSlots()
            self.filtersortgroups[i] = FilterSortGroup(i)
            self.filtersortgroups[i].CreateSlots()

        
            
        
            
        #QtCore.QObject.connect(Ui().radioExportLapsTimes,      QtCore.SIGNAL("toggled(bool)"), lambda index: dstore.SetItem("export_laps", ["column"], 0) if index else None)
        #QtCore.QObject.connect(Ui().radioExportLapsLaptimes,  QtCore.SIGNAL("toggled(bool)"), lambda index: dstore.SetItem("export_laps", ["column"], 1) if index else None) 
        #QtCore.QObject.connect(Ui().radioExportLapsPoints_1,  QtCore.SIGNAL("toggled(bool)"), lambda index: dstore.SetItem("export_laps", ["column"], 2) if index else None) 
        #QtCore.QObject.connect(Ui().radioExportLapsPoints_2,  QtCore.SIGNAL("toggled(bool)"), lambda index: dstore.SetItem("export_laps", ["column"], 3) if index else None) 
        #QtCore.QObject.connect(Ui().radioExportLapsPoints_3,  QtCore.SIGNAL("toggled(bool)"), lambda index: dstore.SetItem("export_laps", ["column"], 4) if index else None)                                       
            
    def IsEnabled(self, index, key = None):
        return self.exportgroups[index].IsEnabled(key)
         
    def Update(self, mode = UPDATE_MODE.all):                                
                                                  
        #export        
        #exportgroups                
        changed = False                             
        for i in range(0, NUMBER_OF.EXPORTS):
            self.headergroups[i].Update()
            self.wwwgroups[i].Update()
            self.smsgroups[i].Update()
            self.filtersortgroups[i].Update()                        
          
            
#             column = dstore.GetItem("export_laps", ["column"])
#             if column == ExportLapsFormat.FORMAT_TIMES:
#                 Ui().radioExportLapsTimes.setChecked(True)            
#                 Ui().radioExportLapsLaptimes.setChecked(False)
#                 Ui().radioExportLapsPoints_1.setChecked(False)
#                 Ui().radioExportLapsPoints_2.setChecked(False)
#                 Ui().radioExportLapsPoints_3.setChecked(False)
#             elif column == ExportLapsFormat.FORMAT_LAPTIMES:            
#                 Ui().radioExportLapsTimes.setChecked(False)            
#                 Ui().radioExportLapsLaptimes.setChecked(True)
#                 Ui().radioExportLapsPoints_1.setChecked(False)
#                 Ui().radioExportLapsPoints_2.setChecked(False)
#                 Ui().radioExportLapsPoints_3.setChecked(False)
#             elif column == ExportLapsFormat.FORMAT_POINTS_1:            
#                 Ui().radioExportLapsTimes.setChecked(False)            
#                 Ui().radioExportLapsLaptimes.setChecked(False)
#                 Ui().radioExportLapsPoints_1.setChecked(True)                                
#                 Ui().radioExportLapsPoints_2.setChecked(False)
#                 Ui().radioExportLapsPoints_3.setChecked(False)
#             elif column == ExportLapsFormat.FORMAT_POINTS_2:            
#                 Ui().radioExportLapsTimes.setChecked(False)            
#                 Ui().radioExportLapsLaptimes.setChecked(False)
#                 Ui().radioExportLapsPoints_1.setChecked(False)                                
#                 Ui().radioExportLapsPoints_2.setChecked(True)
#                 Ui().radioExportLapsPoints_3.setChecked(False)
#             elif column == ExportLapsFormat.FORMAT_POINTS_3:            
#                 Ui().radioExportLapsTimes.setChecked(False)            
#                 Ui().radioExportLapsLaptimes.setChecked(False)
#                 Ui().radioExportLapsPoints_1.setChecked(False)                                
#                 Ui().radioExportLapsPoints_2.setChecked(False)
#                 Ui().radioExportLapsPoints_3.setChecked(True)
#             else:
#                 print "error: export laptimes"
                
        if(changed == True):            
            uiAccesories.showMessage("Additional info", "The column was disabled also for all exports.\n\n See the export tab. \n ", MSGTYPE.warning)
                
        #print dstore.Get("export")                                    
                                
        return True
    
tabExportSettings = TabExportSettings() 