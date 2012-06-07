import LabelDesigner
import sys
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
    
class Labeler(QtGui.QApplication):
    def __init__(self, *args, **kwargs):
        super(Labeler, self).__init__(*args, **kwargs)
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
        
        
        self.MainWindow.show()
        
        
        
if __name__ == '__main__':
    
    app = Labeler(sys.argv)
    
    sys.exit(app.exec_())