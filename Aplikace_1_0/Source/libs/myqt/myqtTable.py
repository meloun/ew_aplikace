# -*- coding: utf-8 -*-
'''
Created on 30.10.2009
@author: Lubos Melichar
'''

from PyQt4 import QtCore, QtGui, Qt
import sys
                    
def addRow(tableWidget, row):
    tableWidget.insertRow(tableWidget.rowCount())
    
    nr_column = 0
    for item in row:                
        tableWidget.setItem(tableWidget.rowCount() - 1, nr_column, QtGui.QTableWidgetItem(str(item)))
        nr_column = nr_column+1