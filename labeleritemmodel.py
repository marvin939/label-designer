from PyQt4 import QtCore, QtGui

class LabelItemModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent):
        self.rootData = ["Item Name"]
        self.rootItem = LabelItem(self.rootData)
        self.itemList = []
        
    def setupItemModel(self, data):
        for i in data:
            self.itemList.append(LabelItem(i))
            
    def index(self, row, column, parent):
        