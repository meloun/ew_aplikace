# -*- coding: utf-8 -*-
'''
Created on 14.12.2013

@author: Meloun
'''
from PyQt4 import QtCore
from ewitis.gui.aTab import MyTab
from ewitis.data.DEF_ENUM_STRINGS import *
from ewitis.gui.UiAccesories import uiAccesories
from libs.myqt.mydialogs import *
from ewitis.gui.tabRaceSettings import tabRaceSettings
from ewitis.gui.Ui import Ui
from ewitis.data.dstore import dstore
import libs.utils.utils as utils
import time
from shutil import copyfile

class KeywordGroup():    
    def __init__(self,  index):
        '''
        Constructor
        group items as class members        
        '''
        ui = Ui()        
        self.index = index
                                
        self.keyword = getattr(ui, "PM_lineKeyword_"+str(index+1))  
        self.value = getattr(ui, "PM_lineValue_"+str(index+1))
        self.description = getattr(ui, "PM_lineDescription_"+str(index+1))                                            
        

    def CreateSlots(self):                
        QtCore.QObject.connect(self.keyword, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("profilemaker-keywords", [self.index, "keyword"],  utils.toUnicode(name)))                 
        QtCore.QObject.connect(self.value, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("profilemaker-keywords", [self.index, "value"],  utils.toUnicode(name)))
        QtCore.QObject.connect(self.description, QtCore.SIGNAL("textEdited(const QString&)"),  lambda name: dstore.SetItem("profilemaker-keywords", [self.index, "description"],  utils.toUnicode(name)))

                
            
    def GetInfo(self):
        return dstore.GetItem("profilemaker-keywords", [self.index])
    
    def Update(self):        
        # set values from datastore            
        info = self.GetInfo() 
        uiAccesories.UpdateText(self.keyword, info["keyword"])  
        uiAccesories.UpdateText(self.value, info["value"])
        uiAccesories.UpdateText(self.description, info["description"])
        
        
class TabProfileMaker():    
      
    def __init__(self):                
        print "I: CREATE: tabProfileMaker"      
        
    def Init(self):                     
        self.addSlots()        
        
    def addSlots(self):                               
        print "I: SLOTS: tabProfileMaker"
        
        QtCore.QObject.connect(Ui().pm_pushLoadProfile, QtCore.SIGNAL('clicked()'),  lambda:tabRaceSettings.sLoadProfile("tjson"))
        QtCore.QObject.connect(Ui().pm_pushSaveProfile, QtCore.SIGNAL('clicked()'),  lambda:tabRaceSettings.sSaveProfile("tjson"))         
        QtCore.QObject.connect(Ui().pm_pushReplaceProfile, QtCore.SIGNAL('clicked()'), self.sReplaceProfile)

        self.keywordgroups = [None] * NUMBER_OF.KEYWORDS
        for i in range(0, NUMBER_OF.KEYWORDS):
            self.keywordgroups[i] = KeywordGroup(i)
            self.keywordgroups[i].CreateSlots()

         
    def Update(self, mode = UPDATE_MODE.all):
        print "PM-Update", time.clock()    
        #print type(dstore.GetAllPermanents())

#              
        #keywordgroups
        for i in range(0, NUMBER_OF.KEYWORDS):
            self.keywordgroups[i].Update()
        
        return True
    
    def sReplaceProfile(self):
        copyfile("conf/conf_work.json","conf/conf_work.tjson")        
        
#         with open("conf/conf_work.tjson", "r") as fin:
#             with open("conf/conf_work.json", "w") as fout:
#                 for line in fin:
#                     for keyword in dstore.Get("profilemaker-keywords"):                        
#                         keyword_str = '$'+keyword["keyword"]+'$'                                        
#                         #print keyword_str," -> ", keyword["value"]
#                         if keyword_str in line:
#                             cnt_replacements = cnt_replacements + 1
#                             print "PROFILE MAKER: ", keyword_str," -> ", keyword["value"]
#                         line = line.replace(keyword_str, keyword["value"])
#                     fout.write(line)
        new_text = ""
        report = ""
        with open("conf/conf_work.json", "r") as fin:
            new_text = fin.read()
            for keyword in dstore.Get("profilemaker-keywords"):                        
                keyword_str = '$'+keyword["keyword"]+'$'
                keyword_str = utils.getUtf8String(keyword_str)                                                                                
                report = report + str(new_text.count(keyword_str)) + "x : " +keyword_str + " -> " + keyword["value"] + "\n"
                keyword_value = utils.getUtf8String(keyword["value"])                 
                new_text = new_text.replace(keyword_str, keyword_value)                                
         
        with open("conf/conf_work.json", "w") as f:
            f.write(new_text)           
        
        dstore.Update(dstore.db.load())         
        uiAccesories.showMessage("PROFILE MAKER", report, msgtype = MSGTYPE.info)
        
        
#
tabProfileMaker = TabProfileMaker() 

