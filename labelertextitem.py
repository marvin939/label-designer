from PyQt4 import QtCore, QtGui
from labeleritemmixin import LabelerItemMixin, LabelProp

class LabelerTextItem(QtGui.QGraphicsTextItem, LabelerItemMixin):
    def __init__(self, name, *args, **kwargs):
        self.editing = False
        super(LabelerTextItem, self).__init__(*args, **kwargs)
        LabelerItemMixin.__init__(self, name)
        self.objectType = "Text"
        self.lineSpacing = 90
        self.currentFontSize = 9.0
        self.perfectFontSize = 20.0
        self.fontScale = 1.0
        self.fontScaleX = 1.0
        self.fontScaleY = 1.0
        font = self.font()
        font.setFamily("Arial")
        font.setPointSizeF(9.0)
        self.setFont(font)
        self.skipBlanks = False
        
        self._setTextFromUpdate = False
        
#         OLD property management, left as a reference for now
#        properties = {'Text':('text','', self.text_changed), 
#                           'Skip Blanks':('boolean', False, None),
#                           'Font Size':('float', 9.0, self.set_font_size),
#                           'Font':('font', (self.font().family(),self.font().styleName(), self.font().pointSizeF()), self.set_font_family),
#                           'Font Bold':('boolean', self.font().bold(), self.set_font_bold),
#                           'Font Italic':('boolean', self.font().italic(), self.set_font_italic),
#                           'X Coord':('float', self.scenePos().x(), self.setX),
#                           'Y Coord':('float', self.scenePos().y(), self.setY),
#                           'Line Spacing':('integer', self.lineSpacing, self.line_space_changed)}
#        propOrder = ['Text', 'Skip Blanks', 'Font', 'Font Size', 'Font Bold', 'Font Italic', 'X Coord', 'Y Coord', 'Line Spacing']
        
        
        properties = [LabelProp(propName='Text', propType='textarea', propValue=self.toPlainText()),
                      LabelProp(propName='Skip Blanks', propType='boolean', propValue=True),
                      LabelProp(propName='Font', propType='font', propValue=None),
                      LabelProp(propName='X Coord', propType='double', propValue=self.scenePos().x()),
                      LabelProp(propName='Y Coord', propType='double', propValue=self.scenePos().y()),
                      LabelProp(propName='Line Spacing', propType='double', propValue=100),
                      ]
        self.propCallbacks["Text"] = self.text_changed
        self.propCallbacks["Skip Blanks"] = self.skip_blanks_toggle
        self.propCallbacks["Font"] = self.font_changed
        self.propCallbacks["X Coord"] = self.setX
        self.propCallbacks["Y Coord"] = self.setY
        self.propCallbacks["Line Spacing"] = self.line_space_changed                     
        #self.propOrder = ['Text', 'Skip Blanks', 'Font', 'X Coord', 'Y Coord', 'Line Spacing']
        self.load_properties(properties)
        self.set_pos_by_mm(5,4)
        # Prop callbacks are managed here because the conf file won't be storing any referene to a callback
        
        
        
        
        
        
        self.setFlags(self.ItemIsSelectable|self.ItemIsMovable|self.ItemIsFocusable|self.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        
        self.merging = False
        self.mergeText = self.toPlainText()
        
        
        
        self.skipBlanks = False
        
        
    def setPos(self, *args, **kwargs):
        
        super(LabelerTextItem, self).setPos(*args, **kwargs)
        
        # Disables updating of widgets to avoid an infinite loop
        self.propNames["X Coord"].enable_updates(False)
        self.propNames["Y Coord"].enable_updates(False)
        
        self.propNames["X Coord"].set_double(self.scenePos().x())
        self.propNames["Y Coord"].set_double(self.scenePos().y())
        
        self.propNames["X Coord"].enable_updates(True)
        self.propNames["Y Coord"].enable_updates(True)
        
    def setX(self, value):
        self.setPos(value, self.y())
        
    def setY(self, value):
        self.setPos(self.x(), value )
        
    def skip_blanks_toggle(self, toggle):
        self.skipBlanks = toggle
        
    def line_space_changed(self):
        self.lineSpacing = int(self.propNames["Line Spacing"].get_value())
        self.update_block_formatting()
        
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
            if field not in row:
                if self.suppress_address_errors:
                    text = text.replace(i, "")
                else:
                    raise IndexError("Field %s not found in record" % field)
            else:
                text = text.replace(i, row[field])
                    
                
        
        
        finalText = ""
        #if self.propWidgets['Skip Blanks'].isChecked():
        if self.propNames["Skip Blanks"].get_value():
            for line in text.split("\n"):
                if line.strip() <> "":
                    finalText += line +"\n"
            finalText = finalText.rstrip("\n")
        else:
            finalText = text
            
        self.setPlainText(finalText)
            
        
        
    def text_changed(self):
        string = self.propNames['Text'].get_value()
        self._setTextFromUpdate = True
        if string <> self.toPlainText():
            self.setPlainText(string)
        self._setTextFromUpdate = False
            
    def set_font_size(self, size):
        self.currentFontSize = size
        font = self.font()
        #font.setPointSizeF(size)
        self.setFont(font)
        
    def font_changed(self, font):
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
        self.propNames['Text'].set_text(self.toPlainText())
        
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
        """ Overrided to add calc for leading/line spacing, and to correct QT bug with letter spacing under 16pt """
        size = font.pointSizeF()
        metric = QtGui.QFontMetricsF(font)
        width = metric.width(self.toPlainText())
        #height = metric.height()
        height = metric.boundingRect(self.toPlainText()).height()
        #size = self.currentFontSize
        if size < 16.0:
            #if self.fontScaleX <> 1.0 or self.fontScaleY <> 1.0:
            #    #old = 1.0 / self.fontScale
            #    oldx = 1.0 / self.fontScaleX
            #    oldy = 1.0 / self.fontScaleY
            #    self.scale(oldx, oldy)
            font.setPointSizeF(20.0)
            metric = QtGui.QFontMetricsF(font)
            newwidth = metric.width(self.toPlainText())
            newheight = metric.boundingRect(self.toPlainText()).height()
            if 0 in (width, newwidth, height, newheight) :
                new = size / self.perfectFontSize
                self.setScale(new)
                #newx = newy = math.sqrt((new**2) + (new**2))
            else:
                #newx = width / newwidth
                newy = height / newheight
                self.setScale(newy)
            #
            #print newx, newy
            #self.scale(newx, newy)
            
            #self.fontScaleX = newx
            #self.fontScaleY = newy
            
        #elif self.fontScaleX <> 1 or self.fontScaleY <> 1:
        #    newx = 1.0 / self.fontScaleX
        #    newy = 1.0 / self.fontScaleY
        else:
            #self.scale(newx, newy)
            self.setScale(1.0)
            #self.fontScaleX = 1.0
            #self.fontscaleY = 1.0
        #elif size >= 16.0:
        #    font.setPointSizeF(size)
        
        
        super(LabelerTextItem, self).setFont(font)
            
        self.leading = self.font().pointSize()*self.lineSpacing
        
    def update_block_formatting(self):
        cur = self.textCursor()
        cur.select(cur.Document)
        
        bf = cur.blockFormat()
        bf.setLineHeight(self.lineSpacing, bf.ProportionalHeight)
        cur.setBlockFormat(bf)  
        
        
    def setPlainText(self, text):
    
        super(LabelerTextItem, self).setPlainText(text)
        self.update_text()
        #
        #    if string <> self.propWidgets['Value'].toPlainText():
        #        self.propWidgets['Value'].setPlainText(self.toPlainText())
                
        self.update_block_formatting()
              
        
        #cur.clearSelection()
        #self.setTextCursor(cur)
        
    def update_text(self):
        if not self.merging and not self._setTextFromUpdate:
            self.propNames["Text"].enable_updates(False)
            self.propNames["Text"].set_text(self.toPlainText())
            self.propNames["Text"].enable_updates(True)
        

        
        
    def itemChange(self, change, value):
        """ Overrided to stop editing after losing selection """
        super(LabelerTextItem,self).itemChange(change, value)
        if change == QtGui.QGraphicsItem.ItemSelectedChange:
            if value == False:
                self.end_edit()
                self.clearFocus()
        elif change == QtGui.QGraphicsItem.ItemPositionHasChanged:
            #self.propWidgets['X Coord'].setValue(self.x())
            #self.propWidgets['Y Coord'].setValue(self.y())
            self.propNames['X Coord'].update_double(self.x())
            self.propNames['Y Coord'].update_double(self.y())
        return value