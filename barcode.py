from PyQt4 import QtGui, QtCore
import math

_i2of5 = {'0':'nnwwn',
          '1':'wnnnw',
          '2':'nwnnw',
          '3':'wwnnn',
          '4':'nnwnw',
          '5':'wnwnn',
          '6':'nwwnn',
          '7':'nnnww',
          '8':'wnnwn',
          '9':'nwnwn',
          'start':'nnnn',
          'end':'Wnn'}



def bar_I2of5(data):
    _dpi = (QtCore.QCoreApplication.instance().desktop().physicalDpiX(), QtCore.QCoreApplication.instance().desktop().physicalDpiY())
    _dpmm = (_dpi[0] / 25.4, _dpi[1] / 25.4)
    """ Returns a QPixmap containing the barcode """
    datatext = str(data) 
    if not datatext.isdigit():
        raise TypeError("i2of5 can only contain digits 0-9")
    
    
    if len(datatext) % 2 == 1:
        datatext = '0' + datatext
    
    n = 2.4
    c = len(datatext)
    x = 5.0 #0.508 * _dpmm[0]
    #x = 2.0
    
    width = math.ceil(((c * ((2*n) + 3)) + 6 + n ) * x)
    
    height = 20.0
    
    bitmap = QtGui.QPixmap(width, height)
    
    bitmap.fill()
    
    
    painter = QtGui.QPainter(bitmap)
    painter.setBrush(QtCore.Qt.black)
    currentPos = 0.0
    
    currentPos = _draw_i2of5_line(painter, _i2of5['start'], currentPos)
    
    for i in range(c/2):
        first = _i2of5[datatext[(i*2)]]
        second = _i2of5[datatext[(i*2)+1]]
        
        code = ''
        for h in range(5):
            code += first[h] + second[h]
            
        currentPos = _draw_i2of5_line(painter, code, currentPos)
        
    _draw_i2of5_line(painter, _i2of5['end'], currentPos)
        
    return bitmap
            
    
        
def _draw_i2of5_line(painter, digitcode, currentPos):
    """ Digitcode is the interlaced code (nnwnw...) """
    #_dpi = (QtCore.QCoreApplication.instance().desktop().physicalDpiX(), QtCore.QCoreApplication.instance().desktop().physicalDpiY())
    #_dpmm = (_dpi[0] / 25.4, _dpi[1] / 25.4)
    n = 2.4
    x = 5.0 #0.508 * _dpmm[0]
    #x = 2.0
    height = 20.0
    newPos = currentPos
    space = False
    for i in digitcode:
        if i == 'n':
            size = x
        else:
            size = x*n
        newPos += size/2.0
        if not space:
            start = QtCore.QPointF(newPos, 0.0)
            end = QtCore.QPointF(newPos, height)
            
            pen = painter.pen()
            pen.setWidthF(size)
            painter.setPen(pen)
            
            painter.drawLine(start, end)
        newPos += size/2.0
        space = not space
    return newPos
    
    