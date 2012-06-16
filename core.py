import LabelDesigner
from zoomgraphicsview import ZoomGraphicsView
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
    
DPMM = []


 
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
        self.itemListObjects = {}
        
        
        #Set DPMM(dots per mm) based on QT's DPI
        self.dpi  = (self.MainWindow.logicalDpiX(), self.MainWindow.logicalDpiY())
        self.dpmm = (self.dpi[0]/25.4, self.dpi[1]/25.4)
        DPMM.append(self.dpi[0]/25.4)
        DPMM.append(self.dpi[1]/25.4)
        
        self.ui.setupUi(self.MainWindow)
        self.scaleFactor = self.ui.zoomLevel.value()
        
        
        #self.labelView = ZoomGraphicsView((self.dpmm[0]*90, self.dpmm[1]*45))
        self.labelView = self.ui.graphicsView
        self.labelView.setPageSize((self.dpmm[0]*90, self.dpmm[1]*45))
        self.itemList = self.ui.itemList
        #self.labelView.setMaximumSize(int(math.ceil(self.dpmm[0]*90)+5), int(math.ceil(self.dpmm[1]*45)+5))
        #self.ui.previewLayout.addWidget(self.labelView)
        #self.labelView.setScene(self.labelImage)
        
        
        
        
        self.connect(self.ui.addTextBtn, QtCore.SIGNAL('clicked()'), self.add_text_dialog)
        self.connect(self.ui.createPdfBtn, QtCore.SIGNAL('clicked()'), self.create_pdf)
        self.connect(self.ui.zoomLevel, QtCore.SIGNAL('editingFinished()'), self.zoom_changed)
        self.connect(self.itemList, QtCore.SIGNAL('currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)'), self.item_selected)
    
        self.MainWindow.show()
        
    def remove_object(self, obj):
        self.labelView.scene().removeItem(obj)
        self.objectCollection.remove(obj)
        #self.itemList.removeItemWidget(self.itemListObjects[obj], 1)
        self.itemList.takeTopLevelItem(self.itemList.indexOfTopLevelItem(self.itemListObjects[obj]))

        del self.itemListObjects[obj]
        del obj
        
        

    def add_text(self, text, x, y):
        obj = LabelerTextItem()
        
        self.labelView.scene().addItem(obj)
        
        
        
        obj.setPlainText(text)
        self.objectCollection.append(obj)
        
        item = QtGui.QTreeWidgetItem(self.itemList)
        item.setText(0, "TextObj1")
        item.setData(1,0, obj)
        self.itemListObjects[obj] = item
        
    def item_selected(self, currentItem, previousItem):
        if currentItem <> None:
            obj = currentItem.data(1,0).toPyObject()
            obj.scene().clearSelection()
            obj.setSelected(True)
        
        
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
        for i in range(20000):
            for obj in self.objectCollection:
                font = obj.font()
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