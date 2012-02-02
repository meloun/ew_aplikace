# -*- coding: utf-8 -*-
'''
Created on 30.10.2009
@author: Lubos Melichar
'''

from PyQt4 import QtCore, QtGui, Qt
import sys
                    
def addRow(model, row):
    model.insertRow(0)
        
    nr_column = 0
    for item in row:
        #print "pridavam", item, nr_column            
        model.setData(model.index(0,nr_column), item)       
        nr_column = nr_column+1