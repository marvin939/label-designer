import LabelDesigner
import sys
import _winreg
from PyQt4 import QtCore, QtGui
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

   
 
class LabelerTextItem(QtGui.QGraphicsTextItem):
    def __init__(self, *args, **kwargs):
        
        super(LabelerTextItem, self).__init__(*args, **kwargs)
        self.setFlags(self.ItemIsSelectable|self.ItemIsMovable|self.ItemIsFocusable)
        self.dpi = MainApp.dpi
        self.dpmm = MainApp.dpmm
        self.set_pos_by_mm(50,40)
        font = QtGui.QFont("Helvetica")
        font.setPointSize(50)
        self.setFont(font)
        
        
        
    def get_pos_mm(self):
        """ returns position in millimeters """
        return self.x() / self.dpmm[0], self.y() / self.dpmm[1]
    
    def set_pos_by_mm(self, x, y):
        self.setPos(x*self.dpmm[0], y*self.dpmm[1])
    
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
        self.dpi  = ( self.MainWindow.logicalDpiX(), self.MainWindow.logicalDpiY())
        self.dpmm = (self.dpi[0]/25.4, self.dpi[1]/25.4)
        self.ui.setupUi(self.MainWindow)
        
        self.labelImage = QtGui.QGraphicsScene(0, 0, 400, 500)
        x = self.labelImage.addText("Hello")
        self.ui.imagePreview.setScene(self.labelImage)
        x.setFlags(x.ItemIsSelectable|x.ItemIsMovable|x.ItemIsFocusable)
        x.setSelected(True)
        x.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.ui.imagePreview.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        
        
        self.connect(self.ui.addTextBtn, QtCore.SIGNAL('clicked()'), self.add_text_dialog)
        self.connect(self.ui.createPdfBtn, QtCore.SIGNAL('clicked()'), self.create_pdf)
        
        self.MainWindow.show()
        

    def add_text(self, text, x, y):
        obj = LabelerTextItem()
        
        self.labelImage.addItem(obj)
        obj.setPlainText(text)
        obj.setPos(200,200)
        self.objectCollection.append(obj)
        
        
    def add_text_dialog(self):
        result = QtGui.QInputDialog.getText(self.MainWindow, 'What text to add?', "Enter text")
        if result[1] == True:
            text = result[0]
            self.add_text(text, 0, 0)
            
    def create_pdf(self):
        pdf = canvas.Canvas("hello.pdf")
        for obj in self.objectCollection:
            font = obj.font()
            x, y = obj.get_pos_mm()
            textobj = pdf.beginText(x, y)
            
            
            textobj.setStrokeColorCMYK(0, 0, 0, 1, None)
            try:
                pdf.setFont(str(font.family()), font.pointSize(), font.kerning())
            except KeyError:
                key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts', 0, _winreg.KEY_READ)
                try:
                    fontname = _winreg.QueryValueEx(key,  str(font.family()) + " (TrueType)")
                except:
                    pass
                else:
                    pdfmetrics.registerFont(TTFont(str(font.family()),fontname[0]))
                    textobj.setFont(str(font.family()), font.pointSize(), 2+font.pointSize())
           
            
            textobj.textLines(str(obj.toPlainText()))
            pdf.drawText(textobj)
        pdf.showPage()
        pdf.save()
            
        
MainApp = Labeler(sys.argv)      
        
if __name__ == '__main__':
    
    
    
    sys.exit(MainApp.exec_())