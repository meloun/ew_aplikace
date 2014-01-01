# -*- coding: utf-8 -*-
'''
Created on 30.10.2009
@author: Lubos Melichar
'''

import os   
import sys
from PyQt4 import QtCore, QtGui, Qt
from ewitis.data.dstore import dstore
                   
    
class myDialog(Qt.QFileDialog):
    def __init__(self, datastore):
        self.datastore = datastore
    def getExistingDirectory(self, parent, caption, datastore_inputdir = None):
        
        if(datastore_inputdir == None):
            return Qt.QFileDialog.getExistingDirectory(parent, caption)
        
        inputdir = dstore.Get(datastore_inputdir)        
        dirname = Qt.QFileDialog.getExistingDirectory(parent, caption, inputdir)  
        
        #dstore.Set("dir_getdir", os.path.dirname(str(CurrentDir.absoluteFilePath(filename))))       
        return dirname
     
    def getOpenFileName(self, parent, caption, dstore_directory, filter, filename):  
        print "dstore_directory",dstore_directory       
        directory = dstore.Get(dstore_directory)+"/"+filename
        print "directory",directory
        filename = Qt.QFileDialog.getOpenFileName(parent, caption, directory, filter)
        if(filename != ""):            
            CurrentDir = QtCore.QDir()
            dstore.Set(dstore_directory, os.path.dirname(str(CurrentDir.absoluteFilePath(filename))))              
        return filename
     
    def getSaveFileName(self, parent, caption, dstore_directory, filter, filename):        
        directory = dstore.Get(dstore_directory)+"/"+filename
        filename = Qt.QFileDialog.getSaveFileName(parent, caption, directory, filter)
        if(filename != ""):            
            CurrentDir = QtCore.QDir()
            dstore.Set(dstore_directory, os.path.dirname(str(CurrentDir.absoluteFilePath(filename))))              
        return filename 


              



                      
    
        