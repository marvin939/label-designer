import LabelDesigner
import sys
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
    
class LabelerTextItem(QtGui.QGraphicsTextItem):
    def __init__(self, *args, **kwargs):
        super(LabelerTextItem, self).__init__(*args, **kwargs)
        self.setFlags(self.ItemIsSelectable|self.ItemIsMovable|self.ItemIsFocusable)
    
    def mouseDoubleClickEvent(self, event):
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.setFocus(True)
        
        
    def itemChange(self, change, value):
        super(LabelerTextItem,self).itemChange(change, value)
        if change == QtGui.QGraphicsItem.ItemSelectedChange:
            if value == False:
                self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
                self.clearFocus()
        return value
    
    
class Labeler(QtGui.QApplication):
    def __init__(self, *args, **kwargs):
        super(Labeler, self).__init__(*args, **kwargs)
        self.objectCollection = []
        self.ui = LabelDesigner.Ui_MainWindow()
        self.MainWindow = QtGui.QMainWindow()
        self.ui.setupUi(self.MainWindow)
        
        self.labelImage = QtGui.QGraphicsScene()
        x = self.labelImage.addText("Hello")
        self.ui.imagePreview.setScene(self.labelImage)
        x.setFlags(x.ItemIsSelectable|x.ItemIsMovable|x.ItemIsFocusable)
        x.setSelected(True)
        x.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.ui.imagePreview.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        
        
        self.connect(self.ui.addTextBtn, QtCore.SIGNAL('clicked()'), self.add_text_dialog)
        
        self.MainWindow.show()
        

    def add_text(self, text, x, y):
        obj = LabelerTextItem()
        
        self.labelImage.addItem(obj)
        obj.setPlainText(text)
        obj.setPos(200,200)
        #obj.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        print obj.isVisible(), obj.x()
        print [i.toPlainText() for i in self.labelImage.items()]
        self.objectCollection.append(obj)
        
        
    def add_text_dialog(self):
        result = QtGui.QInputDialog.getText(self.MainWindow, 'What text to add?', "Enter text")
        if result[1] == True:
            text = result[0]
            self.add_text(text, 0, 0)
            
        
        
        
if __name__ == '__main__':
    
    app = Labeler(sys.argv)
    
    sys.exit(app.exec_())