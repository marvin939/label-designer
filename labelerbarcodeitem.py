from PyQt5 import QtCore, QtGui, QtWidgets
from labeleritemmixin import LabelerItemMixin, LabelProp
import barcode

#class LabelerBarcodeItem(QtGui.QGraphicsPixmapItem, LabelerItemMixin):
class LabelerBarcodeItem(QtWidgets.QGraphicsPixmapItem, LabelerItemMixin):
    propLoadOrder = ["Data","X Coord","Y Coord","Barcode Type","X Scale","Y Scale"]
    def __init__(self, name, *args, **kwargs):
        
        super(LabelerBarcodeItem, self).__init__( *args, **kwargs)
        
        LabelerItemMixin.__init__(self, name)#properties, propOrder)
        self.objectType = "Barcode"
        
        self.barcodeTypes = {'Code39':barcode.bar_3of9, 'Interlaced 2of5':barcode.bar_I2of5, 'Code128':barcode.bar_Code128, 'QRCode':barcode.bar_qrcode}
        self.barcodeOrder  = ['Code128', 'Code39', 'Interlaced 2of5', 'QRCode']
        self.currentBarcode = self.barcodeTypes[self.barcodeOrder[0]]
        
        
        properties = (LabelProp(propName="Data", propType="textarea", propValue=""),
                      LabelProp(propName="X Coord", propType="double", propValue=self.scenePos().x()),
                      LabelProp(propName="Y Coord", propType="double", propValue=self.scenePos().y()),
                      LabelProp(propName="Barcode Type", propType="list", propValue=(self.barcodeOrder, None)),
                      LabelProp(propName="X Scale", propType="double", propValue=1),
                      LabelProp(propName="Y Scale", propType="double", propValue=1))
        
        self.propCallbacks["Data"] = self.data_changed
        self.propCallbacks["X Coord"] = self.setX
        self.propCallbacks["Y Coord"] = self.setY
        self.propCallbacks["Barcode Type"] = self.change_barcode_type
        self.propCallbacks["X Scale"] = self.scale_x
        self.propCallbacks["Y Scale"] = self.scale_y
        self.load_properties(properties)
        
        self.propNames["X Scale"].set_min(0.1)
        self.propNames["Y Scale"].set_min(0.1)
        self.propNames["X Scale"].set_step(0.1)
        self.propNames["Y Scale"].set_step(0.1)
        
        #properties = {'Data':('text','', self.data_changed),
        #                   'X Coord':('float', self.scenePos().x(), self.setX),
        #                   'Y Coord':('float', self.scenePos().y(), self.setY),
        #                   'Barcode Type':('list', self.barcodeTypes.keys(), self.change_barcode_type)}
        #propOrder = ['Data', 'X Coord', 'Y Coord', 'Barcode Type']
        
        
        self.setFlags(self.ItemIsSelectable|self.ItemIsMovable|self.ItemIsFocusable|self.ItemSendsGeometryChanges)
        
        #self.scale(0.2,1.0)
        #self.scale(0.2,1.0)
        
        self.currentScale = [1.0, 1.0]
        self.originalPixmap = None
        
    def scale_x(self, val):
        self.currentScale[0] = val#max(val, 1.0)
        self.update_scale()
        
    def scale_y(self, val):
        self.currentScale[1] = val
        self.update_scale()
        
        
    def update_scale(self):
        pixmap = QtGui.QPixmap(self.originalPixmap)
        if pixmap.isNull():
            return
        width = pixmap.width()
        height = pixmap.height()
        newWidth = width*self.currentScale[0]
        newHeight = height*self.currentScale[1]
        pixmap = pixmap.scaled(newWidth, newHeight)
        self.setPixmap(pixmap)
        
    def setPos(self, *args, **kwargs):
        
        super(LabelerBarcodeItem, self).setPos(*args, **kwargs)
        
        # Disables updating of widgets to avoid an infinite loop
        self.propNames["X Coord"].enable_updates(False)
        self.propNames["Y Coord"].enable_updates(False)
        
        self.propNames["X Coord"].set_double(self.scenePos().x())
        self.propNames["Y Coord"].set_double(self.scenePos().y())
        
        
        self.propNames["X Coord"].enable_updates(True)
        self.propNames["Y Coord"].enable_updates(True)
        
        
    def itemChange(self, change, value):
        """ Overrided to stop editing after losing selection """
        super(LabelerBarcodeItem,self).itemChange(change, value)
        
        if change == QtWidgets.QGraphicsItem.ItemPositionHasChanged:
            #self.propWidgets['X Coord'].setValue(self.x())
            #self.propWidgets['Y Coord'].setValue(self.y())
            self.propNames['X Coord'].update_double(self.x())
            self.propNames['Y Coord'].update_double(self.y())
        return value
        
    def setX(self, value):
        self.setPos(value, self.y())
        
    def setY(self, value):
        self.setPos(self.x(), value )
        
    def change_barcode_type(self, barcode):
        #barcode = str(self.propWidgets['Barcode Type'].currentText())
        self.currentBarcode = self.barcodeTypes[str(barcode)]
        self.data_changed()
        
    def get_merge_text(self):
        if not self.merging:
            return self.propNames['Data'].get_value()
        else:
            return self.mergeText
            
        
    def data_changed(self):
        #data = self.propWidgets['Data'].toPlainText()
        data = self.propNames["Data"].get_value()
        #self.setPixmap(barcode.bar_I2of5(data))
        #self.setPixmap(barcode.bar_Code128(data))
        #self.setPixmap(barcode.bar_3of9(data))
        if data != "":
            try:
                self.setPixmap(self.currentBarcode(data))
                self.originalPixmap = self.pixmap()
                self.update_scale()
            except:
                message = "Barcode data invalid"
                if self.merging:
                    message = "Record %d: Barcode data invalid. (\"%s\")" % (QtCore.QCoreApplication.instance().currentRecordNumber, data)
                QtCore.QCoreApplication.instance().log_message(message, "error")
                self.setPixmap(QtGui.QPixmap())
        else:
            self.setPixmap(QtGui.QPixmap())
        
    def start_merge(self):
        self.mergeText = self.propNames['Data'].get_value()
        self.merging = True
        
        
    def end_merge(self):
        self.propNames['Data'].set_text(self.mergeText)
        self.merging = False
        
        
    def merge_row(self, row):
        #text = str(self.mergeText)
        #matches = self.headerRE.findall(text)
        #matches = set(matches)
        #for i in matches:
        #    field = i.replace("{", "").replace("}","")
        #    text = text.replace(i, row[field])
            
        text = self.generate_merge_text(row)
        
        self.propNames['Data'].set_text(text)