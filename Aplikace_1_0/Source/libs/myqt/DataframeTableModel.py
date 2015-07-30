# -*- coding: utf-8 -*-
'''
Created on 28. 7. 2015

@author: Meloun
'''
from PyQt4 import QtCore, QtGui
import pandas as pd
import numpy
import time

'''
 http://stackoverflow.com/questions/17697352/pyqt-implement-a-qabstracttablemodel-for-display-in-qtableview
'''


'''
Model
'''
class DataframeTableModel(QtCore.QAbstractTableModel): 
    header_labels = ['Column 1', 'Column 2', 'Column 3', 'Column 4']
    def __init__(self, parent=None, *args): 
        super(DataframeTableModel, self).__init__()
        self.df = pd.DataFrame()        
        QtCore.QObject.connect(self, QtCore.SIGNAL("dataChanged(const QModelIndex&, const QModelIndex&)"), self.sModelChanged)                

    #virtual function to override
    def GetDataframe(self):
        myheader = ["test1", "test2", "test3"]
        random_nr = int(round(time.clock() * 10))            
        myrow1 =   [ random_nr,  random_nr+400, 250]
        myrow2 =   [ random_nr+1,  random_nr+400, 250]
        df = pd.DataFrame([myrow1]*10 + [myrow2]*10, columns = myheader)
        return df
    
    def sModelChanged(self, index1, index2):
        print "MODEL CHANGED", index1, index2
        #QtCore.QAbstractItemModel.reset(self)
        
    def Update(self):        
        ztime = time.clock()    
        self.layoutAboutToBeChanged.emit()        
        self.df = self.GetDataframe()              
        self.layoutChanged.emit()
        print 'Model.Update()', time.clock() - ztime,"s"        
                    
        
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.df.columns[section]
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)      
        
     
    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0        
        return len(self.df.index) 
        
    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.df.columns.values)
     
    def setData(self, index, value, role = QtCore.Qt.EditRole):  
        #if role == QtCore.Qt.EditRole:       
        #    self.dataChanged.emit(index, index)
        return True
        
    
        
    def data(self, index, role=QtCore.Qt.DisplayRole):
        
        if (role == QtCore.Qt.DisplayRole) or (role == QtCore.Qt.EditRole):
            i = index.row()
            j = index.column()
            item = self.df.iget_value(i, j)
            if isinstance( item, numpy.int64 ):                
                item = int(item)            
            #return QtCore.QVariant((self.datatable.iget_value(i, j)))
            #return '{0}'.format(self.datatable.iget_value(i, j))
            return item
        else:
            return QtCore.QVariant()
    
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable


if __name__ == "__main__":
    from DataframeTableModelUI import Ui_MainWindow
    i = 0
    def getDf():
        global i
        myheader = ["id", "nr", "cell", "time1", "lap1", "time2", "lap2", "time3", "lap3", "name", "category", "order1", "order2", "order3", "start", "points1", "points2", "points3", "points4", "points5", "un1", "un2", "un3", "us1", "timeraw"]
        mytime =   [i, 2, 250, "00:00:01.39", 1, "00:00:01.49", 2, "00:00:01.59", 3, "Luboš Melichar", "Kategorie +žíářýžíáé", 3, 2, 1, 1, 12, 11, 259, 0, 98, 68, 59, 47, "us1", "09:31:25,68"]
        mytime1 =  [i+1, 2, 250, "00:00:01.40", 1, "00:00:01.49", 2, "00:00:01.59", 3, "Luboš Melichar", "Kategorie +žíářýžíáé", 3, 2, 1, 1, 12, 11, 259, 0, 98, 68, 59, 47, "us1", "09:31:25,68"]              
        df1 = pd.DataFrame([mytime]*5000 + [mytime1]*5000, columns = myheader)
        i = i+1
        return df1
        
    def sButton():        
        myModel2.Update()
        print "refresh"
    
    import sys, time
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    QtCore.QObject.connect(ui.button, QtCore.SIGNAL("clicked()"), sButton)
    
    #my part
    
    myModel = QtGui.model = QtGui.QStandardItemModel(0, 2)  
    myModel.insertRow(0)  
    myModel.setData(myModel.index(0, 0), 1)
    myModel.insertRow(0)  
    myModel.setData(myModel.index(0, 0), 2)

    
     
    
    myModel2 = DataframeTableModel()
        
    
    myModel2.Update()
        
    ui.tableView.setModel(myModel2)

    
    
    #end of my part
    
    
    
    MainWindow.show()
    sys.exit(app.exec_())
