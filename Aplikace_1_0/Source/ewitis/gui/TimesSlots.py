# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import libs.timeutils.timeutils as timeutils 

class TimesSlots():
    def __init__(self, times):
        
        self.times = times                
                
        QtCore.QObject.connect(times.params.gui['show_all'] , QtCore.SIGNAL("stateChanged (int)"), self.sTimesShowAllChanged)
        QtCore.QObject.connect(times.params.gui['show_zero'], QtCore.SIGNAL("stateChanged (int)"), self.sTimesShowZeroChanged)
        QtCore.QObject.connect(times.params.gui['aDirectWwwExport'], QtCore.SIGNAL("triggered()"), self.sTimesDirectWwwExport)        
                        



        
    def sTimesShowAllChanged(self, state):        
        if(state == 0):
            self.times.model.showall = False
            self.times.params.gui['add'].setEnabled(True)            
        elif(state == 2):            
            self.times.model.showall = True
            self.times.params.gui['add'].setEnabled(False)            
        self.times.update()
        
    def sTimesShowZeroChanged(self, state):        
        if(state == 0):
            self.times.model.showzero = False
        elif(state == 2):
            self.times.model.showzero = True
        self.times.update()
        
    def sTimesDirectWwwExport(self):
        
        #toDo: rozlisit podle modu z datastore
        self.times.sExport_directWWW(filename="export/www/times_"+self.times.params.guidata.measure_setting["name"]+".htm")
        #self.times.sExport_directWWW(filename="export/www/times_"+timeutils.getUnderlinedDatetime()+".htm")        
        
