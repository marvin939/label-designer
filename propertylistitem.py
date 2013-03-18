from PyQt4 import QtGui, QtCore

class PropertyListItem(QtGui.QTreeWidgetItem):
    def setText(self, column, text):
        super(PropertyListItem, self).setText(column, text)
        self.emitDataChanged()
        
        print "v"
        
    def setData(self, col, role, value):
        super(PropertyListItem, self).setData(col, role, value)
        if role == QtCore.Qt.EditRole:
            print "GGGGG"
            self.emitDataChanged()