from PyQt4 import QtCore, QtGui
from labeleritemmixin import LabelerItemMixin

class LabelerTextItem(QtGui.QGraphicsTextItem, LabelerItemMixin):
    def __init__(self, *args, **kwargs):
        self.editing = False
        super(LabelerTextItem, self).__init__(*args, **kwargs)
        self.fontScale = 1.0
        self.currentFontSize = self.font().pointSizeF()
        self.perfectFontSize = 16.0
        self.lineSpacing = 1.2
        font = QtGui.QFont("Verdana")
        font.setPointSize(9)
        self.setFont(font)
        properties = {'Value':('text','', self.text_changed), 
                           'Skip Blanks':('boolean', False, None),
                           'Font Size':('float', 9.0, self.set_font_size),
                           'Font':('font', (self.font().family(),self.font().styleName(), self.font().pointSizeF()), self.set_font_family),
                           'Font Bold':('boolean', self.font().bold(), self.set_font_bold),
                           'Font Italic':('boolean', self.font().italic(), self.set_font_italic),
                           'X Coord':('float', self.scenePos().x(), self.setX),
                           'Y Coord':('float', self.scenePos().y(), self.setY)}
        propOrder = ['Value', 'Skip Blanks', 'Font', 'Font Size', 'Font Bold', 'Font Italic', 'X Coord', 'Y Coord']
        LabelerItemMixin.__init__(self, properties, propOrder)
        
        
        self.setFlags(self.ItemIsSelectable|self.ItemIsMovable|self.ItemIsFocusable|self.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        
        self.merging = False
        self.mergeText = self.toPlainText()
        
        
        
        self.skipBlanks = False
        
        
        self.set_pos_by_mm(5,4)
        
    def get_merge_text(self):
        if not self.merging:
            return self.toPlainText()
        else:
            return self.mergeText
        
    def start_edit(self):
        self.editing = True
        self.scene().clearSelection()
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.setFocus(True)
        self.setSelected(True)
        
    def end_edit(self):
        self.editing = False
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)
        
    def start_merge(self):
        self.mergeText = self.toPlainText()
        self.merging = True
        
        
    def end_merge(self):
        self.setPlainText(self.mergeText)
        self.merging = False
        
    def merge_row(self, row):
        text = str(self.mergeText)
        matches = self.headerRE.findall(text)
        matches = set(matches)
        for i in matches:
            field = i.replace("<<", "").replace(">>","")
            text = text.replace(i, row[field])
        
        
        finalText = ""
        if self.propWidgets['Skip Blanks'].isChecked():
            for line in text.split("\n"):
                if line.strip() <> "":
                    finalText += line +"\n"
            finalText = finalText.rstrip("\n")
        else:
            finalText = text
            
        self.setPlainText(finalText)
            
        
        
    def text_changed(self):
        string = self.propWidgets['Value'].toPlainText()
        if string <> self.toPlainText():
            self.setPlainText(string)
            
    def set_font_size(self, size):
        font = self.font()
        font.setPointSizeF(size)
        self.setFont(font)
        
    def set_font_family(self, newFont):
        font = self.font()
        font.setFamily(newFont.family())
        self.setFont(font)
        
    def set_font_bold(self, toggle):
        font = self.font()
        font.setBold(toggle)
        self.setFont(font)
        
    def set_font_italic(self, toggle):
        font = self.font()
        font.setItalic(toggle)
        self.setFont(font)
        
            
#    def create_property_widgets(self):
#        for field in self.propOrder:
#            propertyType, value, slot = self.properties[field]
#            widget, signal = propertyTypes[propertyType]
#            if propertyType == 'boolean':
#                editor = widget()
#                editor.setCheckState(value)
#            elif propertyType == 'float' or propertyType == 'integer':
#                editor = widget()
#                editor.setValue(value)
#                editor.setMinimum(-1000)
#                editor.setMaximum(1000)
#            elif propertyType == 'font':
#                editor = widget()
#                editor.setCurrentFont(fontDB.font(*value))
#            else:
#                editor = widget(value)
#            editor.setVisible(False)
#            if slot <> None:
#                editor.connect(editor, signal, slot)
#            self.propWidgets[field] = editor
#        
#    def get_pos_mm(self):
#        """ returns position in millimeters """
#        return self.pos().x() / self.dpmm[0], self.pos().y() / self.dpmm[1]
#    
#    def set_pos_by_mm(self, x, y):
#        """ sets position in mm """
#        self.setPos(x*self.dpmm[0], y*self.dpmm[1])
#        
#    def get_pos_for_pdf(self):
#        """ same as get pos by mm? """
#        #y = self.y() + self.boundingRect().height()
#        return self.x()/self.dpmm[0], (self.y()/self.dpmm[1]) 
#        
    #def mouseDoubleClickEvent(self, event):
    #    """ Overrided to make text editable after being double clicked TODO make sure cursor is showing """
    #    self.start_edit()
    
    def mousePressEvent(self, event):
        if self.isSelected():
            if event.modifiers() == QtCore.Qt.ControlModifier:
                self.end_edit()
            else:
                self.start_edit()
            
        super(LabelerTextItem, self).mousePressEvent(event)
        
    def keyReleaseEvent(self, event):
        super(LabelerTextItem, self).keyReleaseEvent(event)
        if event.key() == QtCore.Qt.Key_Control:
                self.setCursor(QtCore.Qt.ArrowCursor)
        self.propWidgets['Value'].setPlainText(self.toPlainText())
        
#    def hoverLeaveEvent(self, event):
#        self.setCursor(QtCore.Qt.ArrowCursor)
#        super(LabelerTextItem, self).hoverLeaveEvent(event)
#        
    def hoverEnterEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            self.setCursor(QtCore.Qt.SizeAllCursor)
        else:
            self.setCursor(QtCore.Qt.ArrowCursor)
#            
#    def hoverMoveEvent(self, event):
#        if event.modifiers() == QtCore.Qt.ControlModifier:
#            self.setCursor(QtCore.Qt.SizeAllCursor)
#        else:
#            self.setCursor(QtCore.Qt.ArrowCursor)
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Control:
            self.setCursor(QtCore.Qt.SizeAllCursor)
            self.update()
        
        if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            if event.modifiers() in (QtCore.Qt.NoModifier, QtCore.Qt.KeypadModifier):
                self.end_edit()
            elif event.modifiers() in (QtCore.Qt.ControlModifier, QtCore.Qt.ControlModifier|QtCore.Qt.KeypadModifier):
                self.textCursor().insertText("\n")
        else:
            super(LabelerTextItem, self).keyPressEvent(event)
        
    def setFont(self, font):
        """ Overrided to add calc for leading/line spacing """
        size = font.pointSizeF()
        if size < 14.0:
            if self.fontScale <> 1.0:
                old = 1.0 / self.fontScale
                self.scale(old, old)
            new = size / self.perfectFontSize
            self.scale(new, new)
            self.fontScale = new
            font.setPointSizeF(16.0)
        elif self.fontScale <> 1:
            new = 1.0 / self.fontScale
            self.scale(new, new)
            self.fontScale = 1.0
        
        super(LabelerTextItem, self).setFont(font)
            
        self.leading = self.font().pointSize()*self.lineSpacing
        
    def setPlainText(self, text):
        super(LabelerTextItem, self).setPlainText(text)
        string = self.toPlainText()
        if not self.merging:
            if string <> self.propWidgets['Value'].toPlainText():
                self.propWidgets['Value'].setPlainText(self.toPlainText())
        
        
    def itemChange(self, change, value):
        """ Overrided to stop editing after losing selection """
        super(LabelerTextItem,self).itemChange(change, value)
        if change == QtGui.QGraphicsItem.ItemSelectedChange:
            if value == False:
                self.end_edit()
                self.clearFocus()
        elif change == QtGui.QGraphicsItem.ItemPositionHasChanged:
            self.propWidgets['X Coord'].setValue(self.x())
            self.propWidgets['Y Coord'].setValue(self.y())
        return value