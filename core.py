import LabelDesigner
import sys
import _winreg
import math
from PyQt4 import QtCore, QtGui
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class ZoomGraphicsView(QtGui.QGraphicsView):
    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            pointBeforeScale =  QtCore.QPointF(self.mapToScene(event.pos()))
            
            screenCenter = QtCore.QPointF(self.sceneRect().center())
            
            scaleFactor = 1.15
            
            if event.delta() > 0:
                self.scale(scaleFactor, scaleFactor)
            else:
                self.scale(1.0/scaleFactor, 1.0/scaleFactor)
                
            pointAfterScale = QtCore.QPointF(self.mapToScene(event.pos()))
            
            offset = pointBeforeScale - pointAfterScale
            
            self.centerOn(pointAfterScale)
            #newcenter = screenCenter + offset
            #newrect  = self.sceneRect()
            #newrect.moveCenter(pointAfterScale)
            #self.updateSceneRect(newrect)
 
class LabelerTextItem(QtGui.QGraphicsTextItem):
    def __init__(self, *args, **kwargs):
        
        super(LabelerTextItem, self).__init__(*args, **kwargs)
        self.setFlags(self.ItemIsSelectable|self.ItemIsMovable|self.ItemIsFocusable)
        self.dpi = MainApp.dpi
        self.dpmm = MainApp.dpmm
        self.set_pos_by_mm(5,4)
        self.lineSpacing = 1.2
        
        font = QtGui.QFont("Helvetica")
        font.setPointSize(9)
        self.setFont(font)
        
        
    def get_pos_mm(self):
        """ returns position in millimeters """
        return self.pos().x() / self.dpmm[0], self.pos().y() / self.dpmm[1]
    
    def set_pos_by_mm(self, x, y):
        self.setPos(x*self.dpmm[0], y*self.dpmm[1])
        
    def get_pos_for_pdf(self):
        y = self.y() + self.boundingRect().height()
        return self.x()/self.dpmm[0], (self.y()/self.dpmm[1]) 
        
    def mouseDoubleClickEvent(self, event):
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.setFocus(True)
        
    def setFont(self, *args, **kwargs):
        super(LabelerTextItem, self).setFont(*args, **kwargs)
        self.leading = self.font().pointSize()*self.lineSpacing
        
        
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
        self.scaleFactor = self.ui.zoomLevel.value()
        
        self.labelImage = QtGui.QGraphicsScene(0, 0, self.dpmm[0]*90, self.dpmm[1]*45)
        self.labelView = ZoomGraphicsView()
        self.labelView.setMaximumSize(int(math.ceil(self.dpmm[0]*90)+5), int(math.ceil(self.dpmm[1]*45)+5))
        self.ui.previewLayout.addWidget(self.labelView)
        self.labelView.setScene(self.labelImage)
        self.labelView.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        
        
        self.connect(self.ui.addTextBtn, QtCore.SIGNAL('clicked()'), self.add_text_dialog)
        self.connect(self.ui.createPdfBtn, QtCore.SIGNAL('clicked()'), self.create_pdf)
        self.connect(self.ui.zoomLevel, QtCore.SIGNAL('editingFinished()'), self.zoom_changed)
    
        self.MainWindow.show()
        

    def add_text(self, text, x, y):
        obj = LabelerTextItem()
        
        self.labelImage.addItem(obj)
        obj.setPlainText(text)
        self.objectCollection.append(obj)
        
    def zoom_changed(self):
        scale = ((100.0/self.scaleFactor) * self.ui.zoomLevel.value()) / 100
        self.scaleFactor = self.ui.zoomLevel.value()
        
        self.ui.imagePreview.scale(scale, scale)
        
        
        
    def add_text_dialog(self):
        result = QtGui.QInputDialog.getText(self.MainWindow, 'What text to add?', "Enter text")
        if result[1] == True:
            text = result[0]
            self.add_text(text, 0, 0)
            
    def create_pdf(self):
        pdf = canvas.Canvas("hello.pdf", (mm*90, mm*45))
        for obj in self.objectCollection:
            font = obj.font()
            #x, y = obj.get_pos_mm()
            x, y = obj.get_pos_for_pdf()
            print x,y 
            textobj = pdf.beginText(x*mm, ((45-y)*mm) - obj.leading)
            
            textobj.setStrokeColorCMYK(0, 0, 0, 1, None)
            try:
                pdf.setFont(str(font.family()), font.pointSize(), obj.leading)
            except KeyError:
                key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts', 0, _winreg.KEY_READ)
                try:
                    fontname = _winreg.QueryValueEx(key,  str(font.family()) + " (TrueType)")
                except:
                    pass
                else:
                    pdfmetrics.registerFont(TTFont(str(font.family()),fontname[0]))
                    pdf.setFont(str(font.family()), font.pointSize(), obj.leading)
           
            
            textobj.textLines(str(obj.toPlainText()))
            pdf.drawText(textobj)
        pdf.showPage()
        pdf.save()
            
        
MainApp = Labeler(sys.argv)      
        
if __name__ == '__main__':
    
    
    
    sys.exit(MainApp.exec_())