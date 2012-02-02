# -*- coding: utf-8 -*-
'''
Created on 30.10.2009
@author: Lubos Melichar
'''

from PyQt4 import QtCore, QtGui, Qt
import libs.dicts.dicts as Dicts
import sys

class myqtTable(QtGui.QTableWidget):
    '''
    classdocs
    '''
    def __init__(self,  dicts, object):
        self.dicts = dicts
        keys = Dicts.keys(dicts)
        QtGui.QTableWidget.__init__(self, len(dicts), len(keys), object)
        
        #se
        #self.setSortingEnabled(1)
        self.setDisabled(0)
        
        # set row height
        nrows = len(dicts)
        for row in range(nrows):
            self.setRowHeight(row, 18)
        self.setData(dicts)            
        
    def setData(self,dicts):
        keys_values = Dicts.keys_values(dicts)
        i = 0
        for rows in keys_values['values']:
            j = 0
            for item in rows:
                newitem = QtGui.QTableWidgetItem(item)
                newitem.setFont(QtGui.QFont("Courier New", 8))
                newitem.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
                #newitem.setFlags(newitem.flags())
                if(i%2):
                    newitem.setBackground(QtCore.Qt.lightGray)
                self.setItem(i, j, newitem)
                j = j+1
            i = i + 1
        self.setHorizontalHeaderLabels(keys_values['keys'])     
        
if __name__ == "__main__":
    dicts1 = [{u'jmeno':u"lubos", u'prijmeni':u"melichar", u'vek':u"16",u'stav':u"v pohode"},
            {u'prijmeni':u"sportovec", u'vek':u"10", u'barva':u"fialova"},
            {u'prijmeni':u"fremen", u'jazyk':u"c#", u'barva':u"cerna"},
            {u'jmeno':u"lubos", u'prijmeni':u"melichar", u'vek':u"16",u'stav':u"v pohode"},
            {u'prijmeni':u"sportovec", u'vek':u"10", u'barva':u"fialova"},
            {u'prijmeni':u"fremen", u'jazyk':u"c#", u'barva':u"cerna"}
            ]
    print dicts1[0].keys()
    print sorted(dicts1[0].keys())
    
    app = QtGui.QApplication(sys.argv)
    mainWindow = QtGui.QMainWindow()
    mainWindow.setWindowTitle("QStatusBar")
    mainWindow.setMinimumWidth(600)
    mainWindow.setMinimumHeight(600)
    
    mainWidget=QtGui.QWidget(mainWindow)
    mainWindow.setCentralWidget(mainWidget)
    
    myTable = myqtTable(dicts1, mainWidget) 
    myTable.setMinimumWidth(800)
    myTable.show()
    mainWindow.show()
    sys.exit(app.exec_())
    #
    
    #myDict = Dicts.keys(dicts1)
    #print len(myDict)
    #print "main"
    