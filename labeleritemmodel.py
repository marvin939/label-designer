#from PyQt4 import QtCore, QtGui
from PyQt5 import QtCore, QtGui

class LabelItemModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent):
        self.rootData = ["Item Name"]
        self.rootItem = LabelItem(self.rootData)
        self.itemList = []
        
    def setupItemModel(self, data):
        for i in data:
            self.itemList.append(LabelItem(i))
            
    def index(self, row, column, parent):
        # Marvin 17/11/2021 - Not too sure about this function. Maybe got cut off? Replaced below with pass.
        pass