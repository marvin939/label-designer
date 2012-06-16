from PyQt4 import QtCore, QtGui

class LabelItem(object):
    def __init__(self, data, parent = None):
        self.parentItem = parent
        self.data = data
        self.childItems = []
        
    def appendChild(self, item):
        self.childItems.append(item)
        
    def child(self, row):
        return self.childItems[row]
    
    def childCount(self):
        return len(self.childItems)
    
    def parent(self):
        return self.parentItem
    
    def row(self):
        if self.parentItem <> None:
            return self.parentItem.childItems.index(self)
        else:
            return None
        
    def columnCount(self):
        return len(self.data)
        
    def data(self, column):
        return self.itemData[column]