from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsTextItem
from constants import *

class ReturnText(QGraphicsTextItem):
    # Bottom-aligned Return Address text


    def __init__(self, parent=None, y_offset=0, *args, **kwargs):
    
        #super(ReturnText, self).__init__(*args, **kwargs)
        super().__init__()
        self.alignment_ = QtCore.Qt.AlignCenter
        
        
        self.parent = parent
        font = self.font()
        font.setPointSize(20)
        
        self.setFont(font)
        self.setScale(.3)
        
        self.y_offset = 0
        
        self.dpi  = QtCore.QCoreApplication.instance().dpi
        self.dpmm = QtCore.QCoreApplication.instance().dpmm
        self.init()
        
    def init(self):
        self.updateGeometry()
        # self.connect(self.document(), QtCore.SIGNAL('contentsChange(int, int, int)'), self.updateGeometry)
        
    #def setScale(self, scale):
    #    super(ReturnText, self).setScale(scale)
    #    self.dpi = (self.dpi[0]*scale, self.dpi[1]*scale)
    #    self.dpmm = (self.dpmm[0]*scale, self.dpmm[1]*scale)
        
    def updateGeometry(self, x=None, y=None, z=None):
        pageSize_mm_width = self.parent.pageSize_mm_width
        pageSize_mm_height = self.parent.pageSize_mm_height
        # print 'Parent pageSize_mm_width: %s' % pageSize_mm_width
        # print 'Parent pageSize_mm_height: %s' % pageSize_mm_height
        # print '[ReturnText] bounding rect: %s' % self.boundingRect()
        self.setTextWidth(pageSize_mm_width * self.dpmm[0] * (1.0/self.scale()))
        self.setPos(0, (pageSize_mm_height - RETURN_ADDRESS_BOTTOM) * self.dpmm[1] - self.sceneBoundingRect().height() - self.y_offset)
        
        # print 'ReturnText height: %d' % self.boundingRect().height()
        
        # Spaghetti code :-(
        print('From returntext.py: %d' % self.parent.pageSize_mm_height)
        # print 'recyclablePackagingText_visible: ' + self.parent.recyclablePackagingText_visible()
        #print 'Parent recyclablePackagingText: ' + self.parent.recyclablePackagingText

        # if self.parent.recyclablePackagingText.visible():
            # print('spaghetti')
    
            
    #def setAlignment(self, alignment):
    #    self.alignment_ = alignment
    #    blockformat = QtGui.QTextBlockFormat()
    #    blockformat.setAlignment(alignment)
    #    cursor = self.textCursor()
    #    cursor.select(QtGui.QTextCursor.Document)
    #    cursor.mergeBlockFormat(blockformat)
    #    cursor.clearSelection()
    #    self.setTextCursor(cursor)
    
##ReturnText()
