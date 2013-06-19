from PyQt4 import QtCore, QtGui

class ReturnText(QtGui.QGraphicsTextItem):
    def __init__(self, *args, **kwargs):
        super(ReturnText, self).__init__(*args, **kwargs)
        self.alignment_ = QtCore.Qt.AlignCenter
        
        
        font = self.font()
        font.setPointSize(20)
        
        self.setFont(font)
        self.setScale(.3)
        
        
        self.dpi  = QtCore.QCoreApplication.instance().dpi
        self.dpmm = QtCore.QCoreApplication.instance().dpmm
        self.init()
        
    def init(self):
        self.updateGeometry()
        self.connect(self.document(), QtCore.SIGNAL('contentsChange(int, int, int)'), self.updateGeometry)
        
    #def setScale(self, scale):
    #    super(ReturnText, self).setScale(scale)
    #    self.dpi = (self.dpi[0]*scale, self.dpi[1]*scale)
    #    self.dpmm = (self.dpmm[0]*scale, self.dpmm[1]*scale)
        
    def updateGeometry(self, x=None, y=None, z=None):
        heightPrev = self.boundingRect().height() * self.scale()
        widthPrev = self.boundingRect().width() * self.scale()
        topRightPrev = self.boundingRect().topRight()
        self.setTextWidth(-1)
        self.setTextWidth(self.boundingRect().width())
        #self.setAlignment(self.alignment_)
        topRight = self.boundingRect().topRight()
        if self.boundingRect().width() > self.dpmm[0] * 90 * (1.0/self.scale()):
            self.setTextWidth(self.dpmm[0] * 90 * (1.0/self.scale()))
        width = self.boundingRect().width() * self.scale()
        height = self.boundingRect().height() * self.scale()
        
        
        if self.alignment_ == QtCore.Qt.AlignRight:
            self.setPos(self.pos() + (topRightPrev - topRight))
        elif self.alignment_ == QtCore.Qt.AlignCenter:
            self.setPos(self.pos() - QtCore.QPointF(((width - widthPrev)/2),(height-heightPrev)))
            
    #def setAlignment(self, alignment):
    #    self.alignment_ = alignment
    #    blockformat = QtGui.QTextBlockFormat()
    #    blockformat.setAlignment(alignment)
    #    cursor = self.textCursor()
    #    cursor.select(QtGui.QTextCursor.Document)
    #    cursor.mergeBlockFormat(blockformat)
    #    cursor.clearSelection()
    #    self.setTextCursor(cursor)