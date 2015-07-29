'''
Created on 28. 7. 2015

@author: Meloun
'''
from PyQt4 import QtCore, QtGui
from tableView import Ui_MainWindow
import pandas as pd
import numpy

'''
 http://stackoverflow.com/questions/17697352/pyqt-implement-a-qabstracttablemodel-for-display-in-qtableview
'''
class TableModel(QtCore.QAbstractTableModel): 
    def __init__(self, parent=None, *args): 
        super(TableModel, self).__init__()
        self.datatable = None

        
    def update(self, dataIn):
        print 'Updating Model'
        self.datatable = dataIn
        print 'Datatable : {0}'.format(self.datatable)
        
     
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.datatable.index) 
        
    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.datatable.columns.values) 
        
    def data(self, index, role=QtCore.Qt.DisplayRole):
        
        if (role == QtCore.Qt.DisplayRole) or (role == QtCore.Qt.EditRole):
            i = index.row()
            j = index.column()
            item = self.datatable.iget_value(i, j)
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
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    #my part
    
    myModel = QtGui.model = QtGui.QStandardItemModel(0, 2)  
    myModel.insertRow(0)  
    myModel.setData(myModel.index(0, 0), 1)
    myModel.insertRow(0)  
    myModel.setData(myModel.index(0, 0), 2)


    intlist = [1,1,2,1]    
    
    df = pd.DataFrame({'Name':['a','b','c','d'], 'First':['a','b','c','d'], 'Last':intlist, 'Class':intlist, 'Valid':intlist})
    df = pd.DataFrame({'Name':[1, "C",3,4,], 'First':['a','b','c','d'], 'Last':[1,1,2,33]})
    #df[["Last"]] = df[["Last"]].astype(object) 
    print df.dtypes
    myModel2 = TableModel()    
    myModel2.update(df)
    
    ui.tableView.setModel(myModel2)
    ui.treeView.setModel(myModel2)
    
    
    #end of my part
    
    
    
    MainWindow.show()
    sys.exit(app.exec_())
