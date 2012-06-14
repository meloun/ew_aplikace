# -*- coding: utf-8 -*-
'''
Created on 30.10.2009
@author: Lubos Melichar
'''

from PyQt4 import QtCore, QtGui, Qt
import sys
import os   
                   
    
class myDialog(Qt.QFileDialog):
    def __init__(self, datastore):
        self.datastore = datastore
    def getExistingDirectory(self, parent, caption, datastore_inputdir = None):
        
        if(datastore_inputdir == None):
            return Qt.QFileDialog.getExistingDirectory(parent, caption)
        
        inputdir = self.datastore.Get(datastore_inputdir)        
        dirname = Qt.QFileDialog.getExistingDirectory(parent, caption, inputdir)  
        
        #self.datastore.Set("dir_getdir", os.path.dirname(str(CurrentDir.absoluteFilePath(filename))))       
        return dirname
     
    def getOpenFileName(self, parent, caption, dstore_directory, filter, filename):  
        print "dstore_directory",dstore_directory       
        directory = self.datastore.Get(dstore_directory)+"/"+filename
        print "directory",directory
        filename = Qt.QFileDialog.getOpenFileName(parent, caption, directory, filter)
        if(filename != ""):            
            CurrentDir = QtCore.QDir()
            self.datastore.Set(dstore_directory, os.path.dirname(str(CurrentDir.absoluteFilePath(filename))))              
        return filename
     
    def getSaveFileName(self, parent, caption, dstore_directory, filter, filename):        
        directory = self.datastore.Get(dstore_directory)+"/"+filename
        filename = Qt.QFileDialog.getSaveFileName(parent, caption, directory, filter)
        if(filename != ""):            
            CurrentDir = QtCore.QDir()
            self.datastore.Set(dstore_directory, os.path.dirname(str(CurrentDir.absoluteFilePath(filename))))              
        return filename 


              



                      
    
        