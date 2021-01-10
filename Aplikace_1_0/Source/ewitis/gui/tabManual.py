# -*- coding: utf-8 -*-
'''
Created on 14.12.2013

@author: Meloun
'''
from PyQt4 import QtCore, QtGui
from ewitis.gui.aTab import MyTab, UPDATE_MODE
from ewitis.gui.Ui import Ui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

#
class TabManual(MyTab):
    def __init__(self):
        print "I: CREATE: tabManaual"

    
    def Init(self):        
        ui = Ui()
        ui.webViewApp.setUrl(QtCore.QUrl(_fromUtf8("manual/manual.html")))        
    
    def Update(self, mode = UPDATE_MODE.all):
        pass
        
tabManual = TabManual() 

