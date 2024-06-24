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
from ewitis.gui.dfTableRaceInfo import tableRaceInfo
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
        testname =  dstore.GetItem("racesettings-app", ['test_name'])
        filename = timeutils.getUnderlinedDatetime() + "_" + racename + "_" + testname
        dirname = utils.get_filename("backup/"+timeutils.getUnderlinedDatetime()+"_"+racename+suffix+"/")        
        os.makedirs(dirname+"/db")
        os.makedirs(dirname+"/conf") 
        copyfile("db/test_db.sqlite",dirname+"/db/test_db.sqlite")
        copyfile("conf/conf_work.json",dirname+"/conf/conf_work.json")
        
        zipf = zipfile.ZipFile(dirname+filename+".zip", 'w', zipfile.ZIP_DEFLATED)        
        self.zipdir(dirname+"/db", zipf)
        self.zipdir(dirname+"/conf", zipf)
        zipf.close() 
        
        #create&save report as txt file to backup directory
        #try:
        with open(dirname+filename+".txt", "w") as f:
            f.write(self.GetReport())
        #except:
        #    print "E: report - create or save"  
                
        uiAccesories.showMessage("Backup database", "DB stored", msgtype = MSGTYPE.statusbar)                                                                                                                                                                                            
       
    def GetReport(self):
        report_text = ""          
        
        report_notes = '-------------------------------' + '\n'
        report_notes = report_notes + 'NOTES \n'
        report_notes = report_notes + '-------------------------------' + '\n'
        report_notes = report_notes + dstore.GetItem("versions", ['app']) + '\n' + '\n'
        report_notes = report_notes + dstore.GetItem("racesettings-app", ['profile_desc']).encode('utf-8') + '\n' + '\n'       
        
        #
        #remove times with nr 0
        aux_timesDf = tableTimes.model.df[tableTimes.model.df['nr'] != 0].copy()
        aux_usersDf = tableUsers.model.df[tableUsers.model.df['nr'] > 0].copy()
        
        if not aux_timesDf.empty:                            
            
            #CELLTIMES NUMBER
            report_celltimes = '-------------------------------' + '\n'
            report_celltimes = report_celltimes + "CELLTIMES" + '\n'
            report_celltimes = report_celltimes + '-------------------------------' + '\n'
            try:
                #group by cell and get size
                serTimesByCell_size = aux_timesDf.groupby("cell", as_index=False).size()                                           
                #get first cell            
                first_cell = sorted(list(serTimesByCell_size.keys()))[0]                                   
                for (cell, nr_of_times) in serTimesByCell_size.iteritems():
                    #add cell and nr of times
                    report_celltimes = report_celltimes + "cell#"+str(cell)
                    if cell != 250: report_celltimes = report_celltimes + "  "
                    report_celltimes = report_celltimes + " : " + str(nr_of_times) + "time(s)"
                    
                    #CHECK #1: first cell and nr of times
                    if (cell == first_cell):
                        report_celltimes = report_celltimes + '  - první buňka -> OK' + '\n'
                    else:
                        if(nr_of_times == serTimesByCell_size[first_cell]):
                            report_celltimes = report_celltimes + '  - stejný počet časů jako od startovací buňky -> OK' + '\n'
                        elif(nr_of_times < serTimesByCell_size[first_cell]):
                            report_celltimes = report_celltimes + '  - menší počet časů než od první buňky -> KONTROLA' + '\n'
                        else:
                            report_celltimes = report_celltimes + '  - větší počet časů než od první buňky -> !! CHYBA !!' + '\n'
                report_text = report_text + report_celltimes + '\n' 
            except:
                print "E: report - celltimes"
                
            #USER RAWTIMES
            report_usertimes = '-------------------------------' + '\n'
            report_usertimes = report_usertimes + "USER RAWTIMEs" + '\n'
            report_usertimes = report_usertimes + '-------------------------------' + '\n'
            try:            
                #group by nr and get size
                groupTimesByNr = aux_timesDf.groupby("nr", as_index=False)            
                serTimesByNr_size = groupTimesByNr.size()            
                nr_of_users = len(serTimesByNr_size)            
                most_frequent_nr_times = serTimesByNr_size.value_counts().index[0]                                   
                report_usertimes = report_usertimes +  "(I) Nejčastější počet průjezdů branami (rawtimes): " + str(most_frequent_nr_times) + '\n'
                report_usertimes = report_usertimes +  "(I) Počet časů v profilu (autofill): " + str(dstore.GetItem("racesettings-app", ['autonumbers','nr_cells'])) + '\n'            
                
                
                for (nr, nr_of_times) in serTimesByNr_size.iteritems():                
                    #if nr < 10: report_text = report_text + " "
                    #if nr < 100: report_text = report_text + " "
                    nr_string = "nr#" +str(nr) + " : " + str(nr_of_times) + "time(s)"
                    #CHECK: user times check                
                    if(nr_of_times == most_frequent_nr_times):
                        pass
                    elif(nr_of_times < most_frequent_nr_times):
                        report_usertimes = report_usertimes + nr_string + '  - menší počet časů než je obvyklé -> !! CHYBA !!'  + '\n'
                    else:
                        report_usertimes = report_usertimes + nr_string + '  - větší počet časů než je obvyklé -> !! CHYBA !!'  + '\n'
                        
                if not "CHYBA" in report_usertimes:
                    report_usertimes = report_usertimes + ' - všichni závodníci mají stejný počet časů jako je obvyklé -> OK'  + '\n'
                report_text = report_text +  report_usertimes + '\n'
            except:
                print "E: report - user rawtimes"
                
            #TIME 1-4
            try:
                for i in range(4):          
                    seriesTimes = aux_timesDf["time"+str(i+1)].dropna()
                    seriesTimesNumber = seriesTimes.apply(lambda row: TimesUtils.TimesUtils.timestring2time(row, False))                            
                    if seriesTimes.empty:
                        continue                    
                    else: 
                        report_time = '-------------------------------' + '\n'
                        report_time = report_time + "TIME"+str(i+1) + '\n'            
                        report_time = report_time + '-------------------------------' + '\n'               
                        time_max = seriesTimes.max()
                        time_min = seriesTimes.min()
                        time_median = seriesTimesNumber.median()                
                        #report_section = report_section + "(I) Median: " + TimesUtils.TimesUtils.time2timestring(time_median) + '\n'
                        report_time = report_time + "(I) Očekávaný rozsah (min-max): " + TimesUtils.TimesUtils.time2timestring(time_median*0.5) + " - " + TimesUtils.TimesUtils.time2timestring(time_median*1.5) + '\n'
                        report_time = report_time + "(I) Nejvyšší/nejpomalejší čas: " + str(time_max) + '\n' 
                        report_time = report_time + "(I) Nejnižší/nejrychlejší čas: " + str(time_min) + '\n'
                        
                                        
                        #slow times
                        seriesTimesNumber_slow = seriesTimesNumber[seriesTimesNumber > (time_median * 1.5)]
                        report_time = report_time + 'ID časů vyšších/pomalejších než maximum: '
                        if seriesTimesNumber_slow.empty:
                            report_time = report_time + 'žádné časy -> OK'  + '\n'
                        else:
                            for nr in seriesTimesNumber_slow.index.values:
                                report_time = report_time + str(nr) + ', '                 
                            report_time = report_time + ' -> KONTROLA' + '\n'                              
                        
                        #fast times
                        seriesTimesNumber_fast = seriesTimesNumber[seriesTimesNumber < (time_median * 0.5)]                        
                        report_time = report_time + 'ID časů nižších/rychlejších než minimum: '
                        if seriesTimesNumber_fast.empty:
                            report_time = report_time + 'žádné časy -> OK'  + '\n'
                        else:
                            for nr in seriesTimesNumber_fast.index.values:                
                                report_time = report_time + str(nr) + ', '
                            report_time = report_time + ' -> KONTROLA' + '\n'
                                                        
                    report_text = report_text + report_time + '\n'
            except:
                print "E: report - time"
            
            report_text = report_text + '\n'
            report_text = report_text + '--- end of report ---' + '\n'
            
            #SUMMARY
            report_summary = '-------------------------------' + '\n'
            report_summary = report_summary + 'SUMMARY \n'
            report_summary = report_summary + '-------------------------------' + '\n'
            try:
                report_summary = report_summary + 'jelo ' + str(nr_of_users) + ' závodníků' + '\n'
                serDnsUsers = aux_usersDf.nr[~aux_usersDf.nr.isin(aux_timesDf.nr)]
                serUsersWithTime = aux_usersDf.nr[aux_usersDf.nr.isin(aux_timesDf.nr)]
                report_summary = report_summary + 'nejelo ' + str(serDnsUsers.size) + ' závodníků' + '\n'
                report_summary = report_summary + '\n' 
                
                report_summary = report_summary + 'jela čísla: '
                for idx,nr in serUsersWithTime.iteritems():                
                    report_summary = report_summary + str(nr) + ', '
                report_summary = report_summary + '\n'
                report_summary = report_summary + '\n'           
                
                report_summary = report_summary + 'nejela čísla: '
                for idx,nr in serDnsUsers.iteritems():                
                    report_summary = report_summary + str(nr) + ', '
                report_summary = report_summary + '\n'
                report_summary = report_summary + '\n'
            except:
                print "E: report - summary"
               
            report_text = report_summary + report_notes + report_text           
            
        return report_text
            
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
                dbRow['id'] = lasttime['id']+10000000
                print lasttime
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