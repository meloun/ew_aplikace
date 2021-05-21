# -*- coding: utf-8 -*-
'''
Created on 09.04.2014

@author: Meloun
'''
from PyQt4 import QtCore, QtGui
from ewitis.gui.Ui import appWindow, Ui 
from ewitis.data.dstore import dstore 
from ewitis.gui.UiAccesories import MSGTYPE, uiAccesories
from ewitis.data.DEF_ENUM_STRINGS import * 
from ewitis.gui.tabCells import tabCells
from ewitis.gui.tabDevice import tabDevice
from ewitis.gui.multiprocessingManager import mgr
from shutil import copyfile
import libs.utils.utils as utils
from ewitis.data.db import db  
import libs.timeutils.timeutils as timeutils
import os
import zipfile
from ewitis.gui.tabRaceSettings import tabRaceSettings
from ewitis.gui.dfTableTimes import tableTimes
from ewitis.gui.dfTableUsers import tableUsers
import ewitis.gui.TimesUtils as TimesUtils

class BarCellActions():
    STATUS_COLOR = ["#d7d6d5", COLORS.green, COLORS.orange, COLORS.red]
    
    
    
    def __init__(self):
        self.clear_database_changed = False        
        self.lastcheck = {"wdg_calc":0, "wdg_comm":0}
        self.lastcheckKO = {"wdg_calc":0, "wdg_comm":0}
        self.toggle_status = True
        self.test_cnt = 0
        self.active_numbers_list = []
    def Init(self):
        self.InitGui()        
    
    def InitGui(self):
        ui = Ui()
        self.nr = 6 #dstore.Get("nr_cells")
        
        #toolbar because of css color-settings
        self.toolbar_ping = getattr(ui, "toolBarCellPing")
        self.toolbar_missing_time_flag = getattr(ui, "toolBarCellMissingTimeFlag")
        self.toolbar_enable = getattr(ui, "toolBarCellEnable")
        self.toolbar_generate = getattr(ui, "toolBarCellGenerate")
        
        self.check_hw =  getattr(ui, "aHwCheck")
        self.check_app = getattr(ui, "aAppCheck")
        self.active_numbers = getattr(ui, "aActiveNumbers")
        self.active_numbers.setText(self.active_numbers.text() + ' INIT')
        self.dnf_for_active_numbers = getattr(ui, "aDNFforActiveNumbers")
        #self.dnf_for_active_numbers.setText(self.dnf_for_active_numbers.text() + ' INIT')

        
        # list of dict
        # in each dict all gui item
        self.cells_actions = [dict() for _ in range(self.nr)]
        
        
        #                       
        for i, cell_actions in enumerate(self.cells_actions):                                                                                 
            
            #take care about finish time
            i = self.Collumn2TaskNr(i)
            
                             
            # define gui items             
            cell_actions['ping_cell'] = getattr(ui, "aPingCell_"+str(i))
            cell_actions['enable_cell'] = getattr(ui, "aEnableCell_"+str(i))
            cell_actions['generate_celltime'] = getattr(ui, "aGenerateCelltime_"+str(i))
            cell_actions['disable_cell'] = getattr(ui, "aDisableCell_"+str(i))
            self.toolbar_ping.widgetForAction(cell_actions['ping_cell'] ).setObjectName("w_ping_cell"+str(i))
            cell_actions['missing_time_flag'] = getattr(ui, "aMissingTimeFlag_"+str(i))
            self.toolbar_missing_time_flag.widgetForAction(cell_actions['missing_time_flag'] ).setObjectName("w_missing_time_flag"+str(i))
            
        self.auto_enable = Ui().aAutoEnable
        
        self.toolbar_ping.widgetForAction(self.auto_enable).setObjectName("w_auto_enable")
        self.toolbar_enable.widgetForAction(self.check_hw).setObjectName("w_check_hw")                
        self.toolbar_generate.widgetForAction(self.check_app).setObjectName("w_check_app")
            
                         
    def Collumn2TaskNr(self, idx):
        #take care about finish time
        if idx == (self.nr - 1):
            idx = 250 - 1
        return idx+1 
                                
            
    def createSlots(self):
        
        for i, cell_actions in enumerate(self.cells_actions):
            
            #take care about finish time
            i = self.Collumn2TaskNr(i)
            
            if i == 1:
                #add starttime shortcut ("+S")                
                cell_actions['enable_cell'].setShortcuts([cell_actions['enable_cell'].shortcut(), QtGui.QKeySequence("Alt+S")])
                cell_actions['disable_cell'].setShortcuts([cell_actions['disable_cell'].shortcut(), QtGui.QKeySequence("Alt+Ctrl+S")])
                cell_actions['generate_celltime'].setShortcuts([cell_actions['generate_celltime'].shortcut(), QtGui.QKeySequence("Ctrl+S")])
            if i == 250:
                #add finishtime shortcut ("+F")                
                cell_actions['enable_cell'].setShortcuts([cell_actions['enable_cell'].shortcut(), QtGui.QKeySequence("Alt+F")])
                cell_actions['disable_cell'].setShortcuts([cell_actions['disable_cell'].shortcut(), QtGui.QKeySequence("Alt+Ctrl+F")])
                cell_actions['generate_celltime'].setShortcuts([cell_actions['generate_celltime'].shortcut(), QtGui.QKeySequence("Ctrl+F")])
                
            
            # add slots                    
            QtCore.QObject.connect(cell_actions['ping_cell'], QtCore.SIGNAL("triggered()"), lambda task=i : dstore.Set("get_cell_last_times", task, "SET"))
            QtCore.QObject.connect(cell_actions['enable_cell'], QtCore.SIGNAL("triggered()"), lambda task=i: dstore.Set("enable_cell", task, "SET"))                    
            QtCore.QObject.connect(cell_actions['generate_celltime'], QtCore.SIGNAL("triggered()"), lambda task=i: dstore.Set("generate_celltime", {'task':task, 'user_id':0}, "SET"))        
            #QtCore.QObject.connect(cell_actions['generate_celltime'], QtCore.SIGNAL("triggered()"), self.sGenerateCelltime)
            QtCore.QObject.connect(cell_actions['disable_cell'], QtCore.SIGNAL("triggered()"), lambda task=i: dstore.Set("disable_cell", task, "SET"))
        
        
        QtCore.QObject.connect(Ui().aAutoEnableCells_ON, QtCore.SIGNAL("triggered()"), lambda : self.sAutoEnableCells(1))            
        QtCore.QObject.connect(Ui().aAutoEnableCells_OFF, QtCore.SIGNAL("triggered()"), lambda : self.sAutoEnableCells(0))
        QtCore.QObject.connect(Ui().aQuitTiming, QtCore.SIGNAL("triggered()"), self.sQuitTiming)
        QtCore.QObject.connect(Ui().aBackupDatabase, QtCore.SIGNAL("triggered()"), self.sBackupDatabase)
        QtCore.QObject.connect(Ui().aClearDatabase, QtCore.SIGNAL("triggered()"), self.sClearDatabase)
        QtCore.QObject.connect(Ui().aDNFforActiveNumbers, QtCore.SIGNAL("triggered()"), self.sDnfForActiveNumbers)
             
    def sShortcutTest(self):
        print "pressed!"
        

                                                                                                                                                                                                                                 
    def sGenerateCelltime(self):
        print "sGenerateCelltime", self.test_cnt
        self.test_cnt = self.test_cnt + 1 
        #dstore.Set("generate_celltime", {'task':task, 'user_id':nr}, "SET")                                                                                                  


    def zipdir(self, path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), os.path.join(os.path.basename(root), file))


    def sAutoEnableCells(self, value):
        Ui().spinAutoenableCell.setValue(value)

           
    def sBackupDatabase(self, suffix = "_Backup"):        
        racename = dstore.GetItem("racesettings-app", ['race_name']) 
        dirname = utils.get_filename("backup/"+timeutils.getUnderlinedDatetime()+"_"+racename+suffix+"/")        
        os.makedirs(dirname+"/db")
        os.makedirs(dirname+"/conf") 
        copyfile("db/test_db.sqlite",dirname+"/db/test_db.sqlite")
        copyfile("conf/conf_work.json",dirname+"/conf/conf_work.json")
        
        zipf = zipfile.ZipFile(dirname+timeutils.getUnderlinedDatetime()+"_"+racename+".zip", 'w', zipfile.ZIP_DEFLATED)        
        self.zipdir(dirname+"/db", zipf)
        self.zipdir(dirname+"/conf", zipf)
        zipf.close() 
                
        uiAccesories.showMessage("Backup database", "DB stored", msgtype = MSGTYPE.statusbar)                                                                                                                                                                                            
        
        
    def sQuitTiming(self):
        if (uiAccesories.showMessage("Quit Timing", "Are you sure you want to quit timing? \n ", msgtype = MSGTYPE.warning_dialog) != True):            
            return
        
        self.sBackupDatabase("_QuitTiming")
        
        print "A: Generate quit time"                                                                                                                                                                                            
        dstore.Set("quit_timing", 0x00, "SET")
         
    def sClearDatabase(self):
        if (uiAccesories.showMessage("Clear Database", "Are you sure you want to clear all database?\n It will take 30 seconds.\n ", msgtype = MSGTYPE.warning_dialog) != True):            
            return
        
        self.sBackupDatabase("_ClearDb")
                
        uiAccesories.showMessage("Clear Database", "clearing database, please wait.. it will take 30 seconds.", msgtype = MSGTYPE.statusbar)                                                                                                                                                                                            
        dstore.Set("clear_database", 0x00, "SET")
        self.clear_database_changed = True
        
    def sDnfForActiveNumbers(self):
        active_nrs = tableTimes.Get_ActiveNumbers()        
        self.active_numbers.setText('-'.join(str(x) for x in active_nrs))  
        if (uiAccesories.showMessage("DNF for active users", "Are you sure you want generate finish time for all active users?\n\n Active Users: "+('-'.join(str(x) for x in active_nrs)), msgtype = MSGTYPE.warning_dialog) != True):            
            return
               
        #get default row
        dbRow = tableTimes.model.getDefaultRow() 
        if (dbRow['id'] == None):
            uiAccesories.showMessage("DNF for active users", "ERROR: id is NONE", MSGTYPE.warning) 
            return
        
        #state
        dbRow['state'] = '--M'
        dbRow['us1'] = 'DNF'
        
        '''iterate the active numbers and write finish time(cell=250)'''
        for i, dfTime in tableTimes.dfActiveNrs.iterrows():
            #print "DF for active nrs: nr:", dfTime['nr']        
            
            #get user
            user = tableUsers.model.getUserParNr(int(dfTime['nr']))                                                                      
            if (user == None) :
                uiAccesories.showMessage("DNF for active users", "ERROR: no user found", MSGTYPE.warning) 
                continue
            dbRow['user_id'] = user['id']
            
            #get last time
            ttDf = tableTimes.model.GetDataframe()     
            if 'nr' in ttDf.columns:
                lasttime = ttDf[(ttDf.nr==dfTime['nr']) & (ttDf.cell!=0) & (ttDf.timeraw!=None)].iloc[-1]
                #print "lasttime", lasttime            
            try:
                dbRow['time_raw'] = TimesUtils.TimesUtils.timestring2time(lasttime['timeraw']) + 300000
            except TimesUtils.TimeFormat_Error:
                uiAccesories.showMessage("DNF for active users", "E: wrong time format", MSGTYPE.warning) 
                continue
            
            #print dbRow
                                              
            if(dbRow != None): 
                ret = db.insert_from_dict("Times", dbRow)  
                print "ret", ret
                if ret == True: 
                    dbRow['id'] = dbRow['id'] + 1         
                    uiAccesories.showMessage("DNF for active users", "succesfully (nr:"+str(dfTime['nr'])+" id:"+str(dbRow['id'])+")", MSGTYPE.statusbar) 
                else:
                    uiAccesories.showMessage("DNF for active users", "E: writing in db failes", MSGTYPE.warning)

    def GetHwStatus(self):
        status = STATUS.none
        if dstore.Get("port")["opened"]:
            status = tabCells.GetStatus()
            device_status = tabDevice.GetStatus()            
            if device_status > status:                
                status = device_status  
        
        return status
    
    def GetAppStatus(self):
        
        status = STATUS.ok             
        
        #get wdg counters
        wdg_calc = mgr.GetInfo()["wdg_calc"]        
        wdg_comm = dstore.Get("systemcheck")["wdg_comm"]        
        
        if(dstore.Get("port")["opened"] and (self.clear_database_changed == False) and self.lastcheck["wdg_comm"] == wdg_comm):        
            if self.lastcheckKO["wdg_comm"] < WDG.comm:
                self.lastcheckKO["wdg_comm"] = self.lastcheckKO["wdg_comm"] + 1
        else:
            self.lastcheckKO["wdg_comm"] = 0
                        
                
        if (self.lastcheck["wdg_calc"] == wdg_calc):
            if self.lastcheckKO["wdg_calc"] < WDG.calc:
                self.lastcheckKO["wdg_calc"] = self.lastcheckKO["wdg_calc"] + 1
        else:                    
            self.lastcheckKO["wdg_calc"] = 0

                
                
        if self.lastcheckKO["wdg_comm"] != WDG.comm and self.lastcheckKO["wdg_calc"] != WDG.calc:                    
            status = STATUS.ok #everything fine
        else:            
            status = STATUS.error #something is wrong
            #print "Error: wdg: ", self.lastcheckKO
                    
        #copy        
        self.lastcheck["wdg_calc"] = wdg_calc
        self.lastcheck["wdg_comm"] = wdg_comm
        #print self.lastcheckKO,  self.lastcheck                        
        return status
              
    ''' UpdateToolbarActiveNrs() '''
    def UpdateToolbarActiveNrs(self):
        active_nrs = tableTimes.Get_ActiveNumbers()        
        self.active_numbers.setText('-'.join(str(x) for x in active_nrs))        
        
    def Update(self):  
        
        #update toolBarActiveNumbers
        self.UpdateToolbarActiveNrs()
        
        #self.lineCellSynchronizedOnce.setStyleSheet("background:"+COLORS.green)
        
        cell = tabCells.GetCellParTask(1)
        cell_actions = self.cells_actions[0]
#         if cell != None and dstore.Get("port")["opened"]:
#             css_string = "" 
#             info = cell.GetInfo()
#             print "I: ", info
#         font = cell_actions['missing_time_flag'].font()        
#         font.setBold(True)
#         font.setUnderline(True)
#         cell_actions['missing_time_flag'].setFont(font)                        
#         css_string = "QToolButton {width:31px; height:5px;} QToolButton#w_missing_time_flag250{ background:"+COLORS.green+";width: 28px;}"
#         self.toolbar_missing_time_flag.setStyleSheet(css_string) 
            
        
        css_string = ""      
        css_string2 = "QToolButton {height:1px;}"      
        
        #enable/disable items in cell toolbar 
        '''IR'''                                     
        for i, cell_actions in enumerate(self.cells_actions):
                                        
            #convert index to task nr
            i = self.Collumn2TaskNr(i)
            
            cell = tabCells.GetCellParTask(i)            
            if cell != None and dstore.Get("port")["opened"]:
               
                #get info
                info = cell.GetInfo()
                #print "INFO: ", i, info                                   
                                     
                # PING, set bold if cell active
                if info['active']:                    
                    font = cell_actions['ping_cell'].font()
                    font.setBold(True)
                    font.setUnderline(True)
                    cell_actions['ping_cell'].setFont(font)                        
                    css_string = css_string + "QToolButton#w_ping_cell"+str(i)+"{ background:"+COLORS.green+";width: 28px;}"
                                        
                else:
                    font = cell_actions['ping_cell'].font()
                    font.setBold(False)
                    font.setUnderline(False)
                    cell_actions['ping_cell'].setFont(font)
                    css_string = css_string + "QToolButton#w_ping_cell"+str(i)+"{ background:"+COLORS.red+"; width: 28px;}"
                                                                                                                                                                    
                # MISSING TIME FLAG, set bold if cell active
                if info['missing_time_flag']:                        
                    css_string2 = css_string2 + "QToolButton#w_missing_time_flag"+str(i)+"{ background:"+COLORS.red+"; width: 28px;}"                                                                      
                else:
                    css_string2 = css_string2 + "QToolButton#w_missing_time_flag"+str(i)+"{ background:"+COLORS.green+"; width: 28px;}"
                
                # enable/disable all actions
                if(info['trigger'] == 3): #MANUAL
                    cell_actions['ping_cell'].setEnabled(False)
                    cell_actions['enable_cell'].setEnabled(False)
                    cell_actions['disable_cell'].setEnabled(False)
                    cell_actions['generate_celltime'].setEnabled(True)
                else:
                    cell_actions['ping_cell'].setEnabled(True)
                    cell_actions['enable_cell'].setEnabled(True)
                    cell_actions['disable_cell'].setEnabled(True)
                    cell_actions['generate_celltime'].setEnabled(True)
                    #for key, action in cell_actions.items():                                                                
                    #    action.setEnabled(True)
                    
            else:
                #DISABLE all actions, cell not configured or no connection with device
                font = cell_actions['ping_cell'].font()
                font.setBold(False)
                font.setUnderline(False)
                cell_actions['ping_cell'].setFont(font)
                css_string2 = css_string2 + "QToolButton#w_missing_time_flag"+str(i)+"{ width: 31px;}"                    
                for key, action in cell_actions.items(): 
                    action.setEnabled(False)
             
                                
        #auto enable cells
        self.auto_enable.setEnabled(dstore.Get("port")["opened"])
        Ui().aAutoEnableCells_ON.setEnabled(dstore.Get("port")["opened"])
        Ui().aAutoEnableCells_OFF.setEnabled(dstore.Get("port")["opened"])
        timing_settings = dstore.Get("timing_settings", "GET")
        
        if dstore.Get("port")["opened"]:
            if timing_settings["autoenable_cell"]:                    
                font = self.auto_enable.font()
                font.setBold(True)
                font.setUnderline(True)
                self.auto_enable.setFont(font)                        
                css_string = css_string + "QToolButton#w_auto_enable"+"{ background:"+COLORS.green+";width: 28px;}"
                                    
            else:
                font = self.auto_enable.font()
                font.setBold(False)
                font.setUnderline(False)
                self.auto_enable.setFont(font)
                css_string = css_string + "QToolButton#w_auto_enable"+"{ background:"+COLORS.red+";width: 28px;}"
        else:
            font = self.auto_enable.font()
            font.setBold(False)
            font.setUnderline(False)
            self.auto_enable.setFont(font)
                                           
        #background to the toolbars
        hw_status = self.GetHwStatus()   
        app_status = self.GetAppStatus()                      
        self.toolbar_ping.setStyleSheet(css_string)  #cell enabled => green, bold            
        self.toolbar_missing_time_flag.setStyleSheet(css_string2) #cell missing time flag => green, bold
        #self.toolbar_enable.setStyleSheet("QToolButton#w_check_hw{ background:"+BarCellActions.STATUS_COLOR[hw_status]+"; }")
        #self.toolbar_generate.setStyleSheet("QToolButton#w_check_app{ background:"+BarCellActions.STATUS_COLOR[app_status]+"; }")
        
       
        self.toggle_status = self.toggle_status + 1                            
        if self.toggle_status == 2:
            if app_status != STATUS.ok:
                app_status = STATUS.none
            if hw_status != STATUS.ok:
                hw_status = STATUS.none                
            self.toggle_status = 0
                        
        self.toolbar_generate.setStyleSheet("QToolButton#w_check_app{ background:"+BarCellActions.STATUS_COLOR[app_status]+"; }")
        self.toolbar_enable.setStyleSheet("QToolButton#w_check_hw{ background:"+BarCellActions.STATUS_COLOR[hw_status]+"; }")

        
#             font = self.check_app.font()
#             font.setItalic(not font.italic())
#             self.check_app.setFont(font)               
            
        #enabled only when blackbox is connected
        if dstore.Get("port")["opened"]:            
            Ui().aClearDatabase.setEnabled(True)
            Ui().aQuitTiming.setEnabled(True)
        else:
            Ui().aQuitTiming.setEnabled(False)
            Ui().aClearDatabase.setEnabled(False)
            
        #asynchron messages
        if self.clear_database_changed:
            if(dstore.IsChanged("clear_database") == False):
                uiAccesories.showMessage("Clear Database", "Database is empty now", msgtype = MSGTYPE.statusbar)
                self.clear_database_changed = False
                                                          
            
barCellActions = BarCellActions()