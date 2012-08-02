from PyQt4 import QtCore, QtGui
from labeleritemmixin import LabelerItemMixin
import barcode

class LabelerBarcodeItem(QtGui.QGraphicsPixmapItem, LabelerItemMixin):
    def __init__(self, *args, **kwargs):
        
        super(LabelerBarcodeItem, self).__init__( *args, **kwargs)
        
        properties = {'Data':('text','', self.data_changed),
                           'X Coord':('float', self.scenePos().x(), self.setX),
                           'Y Coord':('float', self.scenePos().y(), self.setY)}
        propOrder = ['Data', 'X Coord', 'Y Coord']
        LabelerItemMixin.__init__(self, properties, propOrder)
        
        
        self.setFlags(self.ItemIsSelectable|self.ItemIsMovable|self.ItemIsFocusable)
        
        self.scale(0.2,1.0)
        
    def get_merge_text(self):
        if not self.merging:
            return self.propWidgets['Data'].toPlainText()
        else:
            return self.mergeText
            
        
    def data_changed(self):
        data = self.propWidgets['Data'].toPlainText()
        self.setPixmap(barcode.bar_I2of5(data))
        
        
    def start_merge(self):
        self.mergeText = self.propWidgets['Data'].toPlainText()
        self.merging = True
        
        
    def end_merge(self):
        self.propWidgets['Data'].setPlainText(self.mergeText)
        self.merging = False
        
        
    def merge_row(self, row):
        text = str(self.mergeText)
        matches = self.headerRE.findall(text)
        matches = set(matches)
        for i in matches:
            field = i.replace("<<", "").replace(">>","")
            text = text.replace(i, row[field])
        
        print row[field]
        print text, "merged"
        self.propWidgets['Data'].setPlainText(text)