from PyQt4 import QtCore, QtGui

class ZoomGraphicsView(QtGui.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super(ZoomGraphicsView, self).__init__(*args, **kwargs)
        self.dpi  = (self.logicalDpiX(), self.logicalDpiY())
        self.dpmm = (self.dpi[0]/25.4, self.dpi[1]/25.4)
        self.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.lightGray))
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.setScene(QtGui.QGraphicsScene(0, 0, 0, 0))
        self.pageSizeRects = []
        
        if "pagesize" in kwargs:
            
            self.setPageSize(kwargs["pagesize"])
        
        
        self.scaleFactor = 1.15
        self.zoomLevel = 1
        
        
        self.update()
        
    def keyPressEvent(self, event):
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
        self.pageSizeRects.append(self.scene().addRect(pageRect, QtGui.QPen(QtCore.Qt.white), QtGui.QBrush(QtCore.Qt.white, QtCore.Qt.SolidPattern)))
        self.pageSizeRects.append(self.scene().addRect(greyBorderRect, QtGui.QPen(QtCore.Qt.gray)))
        
        
    
    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
        
            
            if event.delta() > 0:
                self.scale(self.scaleFactor, self.scaleFactor)
            else:
                self.scale(1.0/self.scaleFactor, 1.0/self.scaleFactor)
                
            pointAfterScale = QtCore.QPointF(self.mapToScene(event.pos()))
            
            self.centerOn(pointAfterScale)
            self.update()