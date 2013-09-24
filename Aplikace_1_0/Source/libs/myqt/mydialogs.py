# -*- coding: utf-8 -*-
'''
Created on 30.10.2009
@author: Lubos Melichar
'''

import os   
import sys
from PyQt4 import QtCore, QtGui, Qt
from ewitis.data.DEF_ENUM_STRINGS import *
                   
class MSGTYPE:
    warning, info, warning_dialog, question_dialog, get_integer, right_statusbar, statusbar = range(0,7)
      
class MyDialogs(Qt.QFileDialog):
    def __init__(self, parent = None):
        self.parent = parent            
        self.dirs = {}
        
    def showMessage(self, title, message, msgtype = MSGTYPE.warning, *params):
        """
        zobrazuje dialogy a updatuje status bary
        
        *Dialogy:*
            warning(OK), info(OK), warning_dialog(Yes, Cancel), input_integer(integer, OK)
            
        *Status bary:*
            right_statusbar - zarovnaný vpravo, zobrazuje stav závodu - not active, running, ...
            statusbar - zarovnaný vlevo, zobrazí hlášku z parametru
                
        """
        print "MD showmsg", msgtype                
        #Warning                                        
        if(msgtype == MSGTYPE.warning):
            QtGui.QMessageBox.warning(self.parent, title, message)
        #Info            
        elif(msgtype == MSGTYPE.info):
            QtGui.QMessageBox.information(self.parent, title, message)
        #warning dialog
        elif(msgtype == MSGTYPE.warning_dialog):            
            if not params:                
                ret = QtGui.QMessageBox.warning(self.parent, title, message, QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Yes)                
                if ret != QtGui.QMessageBox.Yes:
                    return False
            elif len(params) == 1:                
                ret = QtGui.QMessageBox.warning(self.parent, title, message, params[0], "Cancel", escapeButtonNumber=1)
                if ret == 1:
                    return False
            elif len(params) == 2:                
                ret = QtGui.QMessageBox.warning(self.parent, title, message, params[0], params[1], "Cancel", escapeButtonNumber=2)
                if ret == 2:
                    return False                                             
        #question dialog
        elif(msgtype == MSGTYPE.question_dialog):                        
            if not params:
                ret = QtGui.QMessageBox.warning(self.parent, title, message, QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Yes)
            elif len(params) == 1:
                ret = QtGui.QMessageBox.warning(self.parent, title, message, params[0], "Cancel", escapeButtonNumber=1)
                if ret == 1:
                    return False
            elif len(params) == 2:
                ret = QtGui.QMessageBox.warning(self.parent, title, message, params[0], params[1], "Cancel", escapeButtonNumber=2)
                if ret == 2:
                    return False
                
        #integer
        elif(msgtype == MSGTYPE.get_integer):
            print params
            print params[0]             
            i, ok = QtGui.QInputDialog.getInteger(self.parent, title, message, value = params[0])
            if ok:
                return i
            return None            
                                                                                                                             
        return True
    
    def update_statusbar(self, title, message):
        pass
        
    def update_right_statusbar(self, title, message):
        pass
    
    def getDirectoryParId(self, dir_id):
        #directorypath = self.datastore.Get(dir_id)
        if not dir_id in self.dirs:
            directorypath = QtCore.QDir().currentPath()
        else:
            directorypath = self.dirs[dir_id]
        return directorypath
    
    def setDirectoryParId(self, dir_id, path):
        self.dirs[dir_id] = path
        #self.datastore.Set(dir_id, path)        
    
          
    def getExistingDirectory(self, caption, inputdir = None):        
        if(inputdir == None):
            return Qt.QFileDialog.getExistingDirectory(self.parent, caption)            
        dirname = Qt.QFileDialog.getExistingDirectory(self.parent, caption, self.getDirectoryParName(inputdir) )          
        #self.datastore.Set("dir_getdir", os.path.dirname(str(CurrentDir.absoluteFilePath(filename))))       
        return dirname
     
    def getOpenFileName(self, caption, dir_id, myfilter, filename):                 
        #directory = self.getDirectoryParId(dir_id)+"/"+filename                
        
        filename = Qt.QFileDialog.getOpenFileName(self.parent, caption, self.getDirectoryParId(dir_id), myfilter)
        if(filename != ""):            
            CurrentDir = QtCore.QDir()
            self.setDirectoryParId(dir_id, os.path.dirname(str(CurrentDir.absoluteFilePath(filename))))              
        return filename
     
    def getSaveFileName(self, caption, dir_id, myfilter, filename):        
        #directory = self.getDirectoryParId(dir_id)+"/"+filename
        filename = Qt.QFileDialog.getSaveFileName(self.parent, caption, self.getDirectoryParId(dir_id), myfilter)
        if(filename != ""):            
            CurrentDir = QtCore.QDir()
            self.setDirectoryParId(dir_id, os.path.dirname(str(CurrentDir.absoluteFilePath(filename))))              
        return filename 


              



                      
    
        