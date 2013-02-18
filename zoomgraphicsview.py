from PyQt4 import QtCore, QtGui
from returntext import ReturnText
from labelertextitem import LabelerTextItem

import barcode

class ZoomGraphicsView(QtGui.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(ZoomGraphicsView, self).__init__(*args, **kwargs)
        self.dpi  = (self.logicalDpiX(), self.logicalDpiY())
        self.dpmm = (self.dpi[0]/25.4, self.dpi[1]/25.4)
        self.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.lightGray))
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.setScene(QtGui.QGraphicsScene(0, 0, 0, 0))
        self.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        #self.permitImage.setPos(self.dpmm[0]*44, self.dpmm[1]*3)
        #self.scene().update()
        
        self.pageSizeRects = []
        
        if "pagesize" in kwargs:
            self.setPageSize(kwargs["pagesize"])
        pix = QtGui.QPixmap("PermitPost.png")
        #self.permitImage = self.scene().addPixmap(pix.scaledToWidth(self.dpmm[0]*43))
        # setup permit image
        
        
        self.permitImage = self.scene().addPixmap(pix)
        self.permitImage.setTransformationMode(QtCore.Qt.SmoothTransformation)
        self.permitImage.scale((self.dpmm[0]*43)/self.permitImage.boundingRect().width(), (self.dpmm[1]*10)/self.permitImage.boundingRect().height())
        self.permitImage.setPos(self.dpmm[0]*46, self.dpmm[1] * 3)
        self.permitText = self.scene().addText("")
        #self.permitText = LabelerTextItem()
        #self.scene().addItem(self.permitText)
        font = QtGui.QFont("Arial Narrow")
        font.setPointSize(16)
        #font.setLetterSpacing(font.AbsoluteSpacing,1.0)
        print font.letterSpacing()
        self.permitText.setFont(font)
        self.permitText.setScale(.5)
        self.permitText.setTextWidth(self.dpmm[0]*48)
        self.permitText.setPos(self.dpmm[0]*46.2, self.dpmm[1]*4)
        self.zoomUpdate = QtCore.SIGNAL("zoomUpdated(PyQt_PyObject)")
        
        self.permitImage.setSelected(True)
        self.scaleFactor = 1.15
        self.zoomLevel = 1
        
        self.addItemList = None
        
        self.returnAddress = ReturnText()
        self.returnAddress.setPos(45*self.dpmm[0], 42*self.dpmm[1])
        
        self.scene().addItem(self.returnAddress)
        print self.returnAddress.pos().x(), self.returnAddress.pos().y(), self.returnAddress.textWidth()
        
        
        #bar = QtGui.QGraphicsPixmapItem(barcode.bar_I2of5('44454545'))
        #bar.scale(.2,1.0)
        #bar.setFlags(bar.ItemIsSelectable|bar.ItemIsMovable|bar.ItemIsFocusable)
        #self.scene().addItem(bar)
        
        self.update()
        
    def set_add_item_list(self, itemList):
        self.addItemList = itemList
        
    def set_permit_number(self, val):
        """ sets the permit label to val """
        if str(val).isdigit():
            self.permitNo = str(val)
        else:
            self.permitNo = ""
            
        self.permitPlainText = "New Zealand\nPermit No.  %s" % self.permitNo
        self.permitText.setPlainText(self.permitPlainText)
        
    def set_return_address(self, text):
        self.returnAddress.setPlainText(text)
        
        
    def start_merge(self, preview):
        if not preview:
            self.hide_bg()
        
    def end_merge(self):
        self.show_bg()
        
    
    def refresh_preview(self):
        pass
        
        
    def hide_bg(self):
        for i in self.pageSizeRects:
            i.setVisible(False)
            
            
    def show_bg(self):
        for i in self.pageSizeRects:
            i.setVisible(True)
        
        
    def toggle_permit(self, toggle):
        self.permitImage.setVisible(toggle)
        self.permitText.setVisible(toggle)
        
    def toggle_return_address(self, toggle):
        self.returnAddress.setVisible(toggle)
        
        
    def keyPressEvent(self, event):
        super(ZoomGraphicsView, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Delete:
            dontDelete = False
            for i in self.scene().selectedItems():
                try:
                    if QtCore.Qt.TextEditorInteraction == i.textInteractionFlags():
                        dontDelete = True
                        break
                except AttributeError:
                    pass
            if not dontDelete:
                for i in self.scene().selectedItems():
                    QtGui.QApplication.instance().remove_object(i)
        elif event.key() == QtCore.Qt.Key_Control:
            item = self.itemAt(self.mapFromGlobal(self.cursor().pos()))
            if item <> None:
                item.keyPressEvent(event)
                
    def keyReleaseEvent(self, event):
        super(ZoomGraphicsView, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Control:
            item = self.itemAt(self.mapFromGlobal(self.cursor().pos()))
            if item <> None:
                item.keyReleaseEvent(event)
                    
    def mousePressEvent(self, event):
        adding = False
        for item, caller in self.addItemList:
            if item.isChecked():
                adding = True
                caller(event.pos())
                item.toggle()
                break
            
        if not adding:
            super(ZoomGraphicsView, self).mousePressEvent(event)
                
        
    def scale(self, x, y):
        """ Overridden to keep count of what magnification we're at """
        assert x == y
        oldzoom = self.zoomLevel
        
        self.zoomLevel *= x
        if self.zoomLevel > 16:
            self.zoomLevel = 16.0
            x = y = 16.0 / oldzoom
            
        super(ZoomGraphicsView, self).scale(x, y)
        
    def zoom_by(self, percentage):
        """ Increments the zoom level of the view by percentage """
        z = self.zoomLevel + (percentage/100.0)
        zoom = z / self.zoomLevel
        self.scale(zoom, zoom) 
        
    def zoom_to(self, percentage):
        """ Sets the zoom level of the view to percentage """
        zoom = (percentage/100.0)/ self.zoomLevel
        self.scale(zoom, zoom) 
        
    def setPageSize(self, pagesize):
        """ sets up the page border, setting current pagesize to pagesize """
        self.pageSize = pagesize
        for i in self.pageSizeRects:
            self.scene().removeItem(i)
            del i
        self.pageSizeRects = []
        
        pageRect = QtCore.QRectF(0, 0, self.pageSize[0], self.pageSize[1])

        blackBoxRect = QtCore.QRectF(3, 3, self.pageSize[0], self.pageSize[1])
        greyBorderRect = QtCore.QRectF(-1, -1, self.pageSize[0] + 2, self.pageSize[1] + 2)
        self.scene().setSceneRect(pageRect)
        self.pageSizeRects.append(self.scene().addRect(blackBoxRect, QtGui.QPen(QtCore.Qt.black), QtGui.QBrush(QtCore.Qt.black, QtCore.Qt.SolidPattern)))
        
        self.pageSizeRects.append(self.scene().addRect(greyBorderRect, QtGui.QPen(QtCore.Qt.gray), QtGui.QBrush(QtCore.Qt.gray, QtCore.Qt.SolidPattern)))
        self.pageSizeRects.append(self.scene().addRect(pageRect, QtGui.QPen(QtCore.Qt.white), QtGui.QBrush(QtCore.Qt.white, QtCore.Qt.SolidPattern)))
        
        for i in self.pageSizeRects:
            i.setZValue(-1)
        
    
    def wheelEvent(self, event):
        """ Overridden to allow for zooming when holding down ctrl """
        if event.modifiers() == QtCore.Qt.ControlModifier:
        
            
            if event.delta() > 0:
                self.zoom_by(15)
            else:
                self.zoom_by(-15)
            self.emit(self.zoomUpdate, self.zoomLevel*100)
                