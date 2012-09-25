# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import libs.timeutils.timeutils as timeutils
import libs.utils.utils as utils  

class TimesSlots():
    def __init__(self, times):
        
        self.times = times                
                
        #QtCore.QObject.connect(times.params.gui['show_all'] , QtCore.SIGNAL("stateChanged (int)"), self.sTimesShowAllTimesChanged)
        #QtCore.QObject.connect(times.params.gui['show_zero'], QtCore.SIGNAL("stateChanged (int)"), self.sTimesShowZerotimesChanged)
        #QtCore.QObject.connect(times.params.gui['show_additional_info'], QtCore.SIGNAL("stateChanged (int)"), self.sTimesShowAditionalInfoChanged)         
        QtCore.QObject.connect(times.params.gui['aDirectWwwExport'], QtCore.SIGNAL("triggered()"), self.times.sExport_directWWW)        
                        



        
    def sTimesShowAllTimesChanged(self, state):        
        if(state == 0):
            #self.times.model.showall = False
            self.times.params.datastore.Set('show_alltimes', False)
            self.times.params.gui['add'].setEnabled(True)            
        elif(state == 2):            
            #self.times.model.showall = True
            self.times.params.datastore.Set('show_alltimes', True)
            self.times.params.gui['add'].setEnabled(False)            
        self.times.update()
        
    def sTimesShowZerotimesChanged(self, state):        
        if(state == 0):            
            self.times.params.datastore.Set('show_zerotimes', False)
        elif(state == 2):            
            self.times.params.datastore.Set('show_zerotimes', True)
        self.times.update()
        
    def sTimesShowStarttimesChanged(self, state):        
        if(state == 0):            
            self.times.params.datastore.Set('show_starttimes', False)
        elif(state == 2):            
            self.times.params.datastore.Set('show_starttimes', True)
        self.times.update()
        
    def sTimesShowAditionalInfoChanged(self, state):
        print self.times.params.datastore.Get("additinal_info")      
        if(state == 0):
            self.times.params.datastore.SetItem("additinal_info",["enabled"], False)                        
        elif(state == 2):
            self.times.params.datastore.SetItem("additinal_info",["enabled"], True)                                    
        self.times.update()
        
#    def sTimesDirectWwwExport(self):
#        print "Direct Export www"
#        
#        #toDo: rozlisit podle modu z datastore
#        self.times.sExport_directWWW(filename="export/www/times_"+self.times.params.datastore.Get('race_name')+".htm")
#        #self.times.sExport_directWWW(filename="export/www/times_"+timeutils.getUnderlinedDatetime()+".htm")        
#        
