from PyQt4 import QtCore, QtGui

class ZoomGraphicsView(QtGui.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(ZoomGraphicsView, self).__init__(*args, **kwargs)
        self.dpi  = (self.logicalDpiX(), self.logicalDpiY())
        self.dpmm = (self.dpi[0]/25.4, self.dpi[1]/25.4)
        self.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.lightGray))
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.setScene(QtGui.QGraphicsScene(0, 0, 0, 0))
        self.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        

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
        self.permitImage.setPos(self.dpmm[0]*46, self.dpmm[1] * 1)
        self.permitText = self.scene().addText("")
        font = QtGui.QFont("Arial Narrow")
        font.setPointSize(8)
        self.permitText.setFont(font)
        self.permitText.setTextWidth(self.dpmm[0]*24)
        self.permitText.setPos(self.dpmm[0]*46.2, self.dpmm[1]*0.9)
        
        print self.dpmm[0]*43
        self.permitImage.setSelected(True)
        self.scaleFactor = 1.15
        self.zoomLevel = 1
        
        
        self.update()
        
    def set_permit_number(self, val):
        if str(val).isdigit():
            self.permitNo = str(val)
        else:
            self.permitNo = ""
            
        self.permitPlainText = "New Zealand\nPermit No.  %s" % self.permitNo
        self.permitText.setPlainText(self.permitPlainText)
        
        
        
        
    def toggle_permit(self, toggle):
        self.permitImage.setVisible(toggle)
        self.permitText.setVisible(toggle)
        
    def keyPressEvent(self, event):
        print self.permitImage.width()
        super(ZoomGraphicsView, self).keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Delete:
            for i in self.scene().selectedItems():
                QtGui.QApplication.instance().remove_object(i)
                
        
    def scale(self, x, y):
        assert x == y
        super(ZoomGraphicsView, self).scale(x, y)
        self.zoomLevel *= x
        print self.zoomLevel
        
    def setPageSize(self, pagesize):
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
        if event.modifiers() == QtCore.Qt.ControlModifier:
        
            
            if event.delta() > 0:
                self.scale(self.scaleFactor, self.scaleFactor)
            else:
                self.scale(1.0/self.scaleFactor, 1.0/self.scaleFactor)
                
            pointAfterScale = QtCore.QPointF(self.mapToScene(event.pos()))
            
            self.centerOn(pointAfterScale)
            self.update()