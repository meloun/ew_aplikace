# -*- coding: utf-8 -*-
'''
Created on 28. 7. 2015

@author: Meloun
'''
from PyQt4 import QtCore, QtGui
import pandas as pd
import pandas.io.sql as psql
import numpy
import time

'''
 http://stackoverflow.com/questions/17697352/pyqt-implement-a-qabstracttablemodel-for-display-in-qtableview
'''

class ModelUtils():
    def __init__(self): 
        pass 
    
    def row(self, r):
        """
        vrací řádek jako list[] unicode stringů
        """
        myrow = [self.data(self.index(r, c)).toString() for c in xrange(self.columnCount())]
        return myrow
    def rows(self):
        """
        vrací řádek jako list[] unicode stringů
        """
        rows = []
        for r in  xrange(self.rowCount()):
            rows.append(self.row(r))
        return rows
    
    def header(self):
        """
        vrací hlavičku tabulky jako list[]
        """
        header = [self.headerData(c, QtCore.Qt.Horizontal) for c in xrange(self.columnCount())]
        return header 


'''
Model
'''
class DataframeTableModel(QtCore.QAbstractTableModel, ModelUtils): 
    header_labels = ['Column 1', 'Column 2', 'Column 3', 'Column 4']
    def __init__(self, name, parent=None): 
        super(DataframeTableModel, self).__init__()
        self.name = name
        self.df = pd.DataFrame()        
        QtCore.QObject.connect(self, QtCore.SIGNAL("dataChanged(const QModelIndex&, const QModelIndex&)"), self.sModelChanged)                
    
    #virtual function to override
    def GetDataframe(self):
        myheader = ["test1", "test2", "test3"]
        random_nr = int(round(time.clock() * 10))            
        myrow1 =   [ random_nr,  random_nr+400, 250]
        myrow2 =   [ random_nr+1,  random_nr+400, 250]
        df = pd.DataFrame([myrow1]*10 + [myrow2]*10, columns = myheader)
        print "GetDataframe"
        return df
    
    def getDefaultRow(self):
        """
        vraci radek naplneny zakladnimi daty
        """
        if self.df.empty == False:
            id = self.df["id"].max() + 1
        else:
            id = 1
        row = {"id":id}
        return row
    
    def sModelChanged(self, index1, index2):
        print "MODEL CHANGED", self.data(index1), self.data(index2)
        self.Update()
        
    def Update(self):    
        ztime = time.clock()    
        self.layoutAboutToBeChanged.emit()        
        self.df = self.GetDataframe()              
        self.layoutChanged.emit()
        #@print 'DataframeTableModel.Update()', time.clock() - ztime,"s"       
     
    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0        
        return len(self.df.index) 
        
    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.df.columns.values)
     
    def setData(self, index, value, role = QtCore.Qt.EditRole):  
        if role == QtCore.Qt.EditRole:
            
            id = self.data(self.index(index.row(), 0))
            header = self.headerData(index.column(), QtCore.Qt.Horizontal)
            
            value_int = value.toInt()
            if(value_int[1] == True):
                ret_value = value_int[0]
            else:
                ret_value = value.toString()
                
            self.setDataFromDict({'id':id, header: ret_value})
                  
            self.dataChanged.emit(index, index)
            return True
        return True
    
    def setDataFromDict(self, mydict):
        print "setDataFromDict()", mydict
        
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            #print "TADY SI TO BERU", section, self.df.columns[section]
            return self.df.columns[section]
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)  
        
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




def f(x):
    i = 0
    while(1):
        print x, str(i)
        i = i + 1
        c = i * i
    return i    
if __name__ == "__main__":
    from DataframeTableModelUI import Ui_MainWindow
    from multiprocessing import Pool
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
     
     
    
    myModel2 = DataframeTableModel("CGroups")
    
    myProxymodel = QtGui.QSortFilterProxyModel()
    myProxymodel.setSourceModel(myModel2)
    
    myModel2.Update()
    
    print "model:", myModel2.headerData(1, QtCore.Qt.Horizontal)
    print "proxymodel:", myProxymodel.headerData(1, QtCore.Qt.Horizontal).toPyObject()        
    
        
    ui.tableView.setModel(myProxymodel)

    

    p = Pool(2)
    print(p.apply_async(f, ["A"]))
    print(p.apply_async(f, ["B"]))
    while(1):
        time.sleep(1)
        print "Konexc"
    

    
    
    
    MainWindow.show()
    sys.exit(app.exec_())