from PyQt4 import QtCore, QtGui
from labeleritemmixin import LabelerItemMixin
import barcode

class LabelerBarcodeItem(QtGui.QGraphicsPixmapItem, LabelerItemMixin):
    def __init__(self, *args, **kwargs):
        
        super(LabelerBarcodeItem, self).__init__( *args, **kwargs)
        
        self.barcodeTypes = {'Code39':barcode.bar_3of9, 'Interlaced 2of5':barcode.bar_I2of5, 'Code128':barcode.bar_Code128}
        self.barcodeOrder  = ['Code39', 'Interlaced 2of5', 'Code128']
        self.currentBarcode = self.barcodeTypes[self.barcodeOrder[0]]
        
        properties = {'Data':('text','', self.data_changed),
                           'X Coord':('float', self.scenePos().x(), self.setX),
                           'Y Coord':('float', self.scenePos().y(), self.setY),
                           'Barcode Type':('list', self.barcodeTypes.keys(), self.change_barcode_type)}
        propOrder = ['Data', 'X Coord', 'Y Coord', 'Barcode Type']
        LabelerItemMixin.__init__(self, properties, propOrder)
        
        
        self.setFlags(self.ItemIsSelectable|self.ItemIsMovable|self.ItemIsFocusable)
        
        #self.scale(0.2,1.0)
        self.scale(0.2,1.0)
        
        
    def change_barcode_type(self, typeIndex):
        barcode = str(self.propWidgets['Barcode Type'].currentText())
        self.currentBarcode = self.barcodeTypes[barcode]
        self.data_changed()
        
    def get_merge_text(self):
        if not self.merging:
            return self.propWidgets['Data'].toPlainText()
        else:
            return self.mergeText
            
        
    def data_changed(self):
        data = self.propWidgets['Data'].toPlainText()
        #self.setPixmap(barcode.bar_I2of5(data))
        #self.setPixmap(barcode.bar_Code128(data))
        #self.setPixmap(barcode.bar_3of9(data))
        self.setPixmap(self.currentBarcode(data))
        
        
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
        
        self.propWidgets['Data'].setPlainText(text)