from PyQt5 import QtCore, QtGui, QtWidgets
from labeleritemmixin import LabelerItemMixin, LabelProp
import re
brTagRE = re.compile(r"<BR\s*/?>", re.IGNORECASE)
htmlFontRE = re.compile(r"<body style=\" font-family:'.*?';")
spanRemoveRE = re.compile(r"<span style.*?>")

class LabelerTextItem(QtWidgets.QGraphicsTextItem, LabelerItemMixin):
    propLoadOrder = ["Skip Blanks","Line Spacing","Is Conditional","Condition","Wrap Text","Width","Rotation","X Coord","Y Coord","Text","Font"]
    
    def __init__(self, name, *args, **kwargs):
        
        self.htmlLabelStart = "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
        self.htmlLabelEnd = "</p></body></html>"
        self.editing = False
        
        
        self.skipBlanks = False
        self.merging = False
        self._setTextFromUpdate = False
        self.coreHtml = ""
        super(LabelerTextItem, self).__init__(*args, **kwargs)
        LabelerItemMixin.__init__(self, name)
        textOpt = self.document().defaultTextOption()
        textOpt.setUseDesignMetrics(True)
        self.document().setDefaultTextOption(textOpt)
        #self.setUp = False
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
        #self.coreHtml = self.htmlLabelStart + self.htmlLabelEnd
        #self.setHtml(self.coreHtml)
    
        properties = [LabelProp(propName='Text', propType='textarea', propValue=self.coreHtml),#LabelProp(propName='Text', propType='textarea', propValue=self.toPlainText()),
                      LabelProp(propName='Skip Blanks', propType='boolean', propValue=True),
                      LabelProp(propName='Font', propType='font', propValue=None),
                      LabelProp(propName='X Coord', propType='double', propValue=self.scenePos().x()),
                      LabelProp(propName='Y Coord', propType='double', propValue=self.scenePos().y()),
                      LabelProp(propName='Line Spacing', propType='double', propValue=100),
                      LabelProp(propName='Is Conditional', propType='boolean', propValue=False),
                      LabelProp(propName='Condition', propType='textarea', propValue=''),
                      LabelProp(propName='Wrap Text', propType='boolean', propValue=False),
                      LabelProp(propName='Width', propType='double', propValue=70),
                      LabelProp(propName='Rotation', propType = 'double', propValue=0)
                      ]
        self.propCallbacks["Text"] = self.text_changed
        self.propCallbacks["Skip Blanks"] = self.skip_blanks_toggle
        self.propCallbacks["Font"] = self.font_changed
        self.propCallbacks["X Coord"] = self.setX
        self.propCallbacks["Y Coord"] = self.setY
        self.propCallbacks["Line Spacing"] = self.line_space_changed
        self.propCallbacks["Is Conditional"] = self.conditional_toggle  
        self.propCallbacks["Condition"] = self.update_condition
        self.propCallbacks["Wrap Text"] = self.toggle_text_wrap
        self.propCallbacks["Width"] = self.update_width
        self.propCallbacks["Rotation"] = self.change_rotation
        #self.propOrder = ['Text', 'Skip Blanks', 'Font', 'X Coord', 'Y Coord', 'Line Spacing']
        self.load_properties(properties)
        #self.setUp = True
        self.set_pos_by_mm(5,4)
        # Prop callbacks are managed here because the conf file won't be storing any referene to a callback
        
        
        
        #self.setFont(font)
        self.propNames["Font"].set_value(font)
        self.setFont(font)
        
        
        
        self.setFlags(self.ItemIsSelectable|self.ItemIsMovable|self.ItemIsFocusable|self.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        
        
        #self.mergeText = self.toPlainText()
        self.strip_html()
        self.mergeText = self.coreHtml
        
        
        self.conditional = self.propNames["Is Conditional"].get_value()
        self.condition = self.propNames["Condition"].get_value()
        self.skipBlanks = self.propNames["Skip Blanks"].get_value()
        self.setScale(1.0)
        
        
    def change_rotation(self):
        self.setRotation(self.propNames["Rotation"].get_value())
        
    def toggle_text_wrap(self, wrap):
        if wrap:
            self.setTextWidth(self.propNames["Width"].get_value()*self.dpmm[0])
        else:
            self.setTextWidth(-1)
    
    def update_width(self, value):
        if self.propNames["Wrap Text"].get_value():
            self.setTextWidth(value*self.dpmm[0])
            
        
    def update_condition(self, value):
        self.condition = value
        
    def conditional_toggle(self, toggle):
        self.conditional = toggle
        
    def strip_html(self):
        """ This function takes the html for this text box, and strips out anything before/after what goes on the label, writing back to self.coreHtml """
        html = str(self.toHtml(), 'latin-1')
        html = brTagRE.sub("<BR />\n", html)
        html.replace("{ white-space: pre-wrap; }", "")
        # This will strip out everything thats unecessary for the user to be looking at, e.g. header, body, html, etc.
        #try:
        html = html.replace("<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">", self.htmlLabelStart)
        core = html[html.index(self.htmlLabelStart)+len(self.htmlLabelStart):html.index(self.htmlLabelEnd)]
        #except ValueError:
        #    core = html
        
        self.coreHtml = core
        
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
            #return self.toPlainText()
            #return self.coreHtml
            return str(self.propNames["Text"].get_value())
        else:
            return self.mergeText
        
    def start_edit(self):
        pass
        # EDITING DISABLED
        #self.editing = True
        #self.scene().clearSelection()
        #self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        #self.setFocus(True)
        #self.setSelected(True)
        
    def end_edit(self):
        self.editing = False
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)
        
    def start_merge(self):
        #self.mergeText = self.toPlainText()
        self.mergeText = self.toHtml()
        self.merging = True
        
        
    def end_merge(self):
        #self.setPlainText(self.mergeText)
        self.setHtml(self.mergeText)
        self.merging = False
        self.setVisible(True)
        
    
        
    def merge_row(self, row):
        if self.conditional:
            try:
                if "=" in self.condition:
                    left, right = self.condition.split("=")
                    left = self.get_merged_value(left, row)
                    right = self.get_merged_value(right, row)
                    if left != right:
                        self.setVisible(False)
                        return
                    else:
                        self.setVisible(True)
                elif "<>" in self.condition:
                    left, right = self.condition.split("<>")
                    left = self.get_merged_value(left, row)
                    right = self.get_merged_value(right, row)
                    if left != right:
                        self.setVisible(True)
                    else:
                        self.setVisible(False)
                        return
                elif "!=" in self.condition:
                    left, right = self.condition.split("!=")
                    left = self.get_merged_value(left, row)
                    right = self.get_merged_value(right, row)
                    if left != right:
                        self.setVisible(True)
                    else:
                        self.setVisible(False)
                        return
                else:
                    raise ValueError("No operator found for comparrison in conditional")
            except ValueError:
                QtCore.QCoreApplication.instance().log_message("Incorrectly written condition on %s." % self.name, "error")
                QtCore.QCoreApplication.instance().cancel_label()
        
        text = self.generate_merge_text(row)
                    
                
        
        
        finalText = ""
        #if self.propWidgets['Skip Blanks'].isChecked():
        if self.propNames["Skip Blanks"].get_value():
        #print "TEST"
        #if True:
            for line in text.split("\n"):
                if line.strip() != "":
                    finalText += line +"\n"
            finalText = finalText.rstrip("\n")
        else:
            finalText = text
            
        #self.setPlainText(finalText)
        self.setHtml(finalText)
            
        
        
    def text_changed(self):
        string = self.htmlLabelStart + self.propNames['Text'].get_value() + self.htmlLabelEnd 
        self._setTextFromUpdate = True
        #if string <> self.toPlainText():
        #    self.setPlainText(string)
        if string != self.coreHtml:
            self.setHtml(string)
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
        #self.propNames['Text'].set_text(self.toPlainText())
        #self.propNames['Text'].set_text(self.coreHtml.replace(self.htmlLabelEnd, "").replace(self.htmlLabelStart, ""))
        
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
        print(event)
        if event.key() == QtCore.Qt.Key_Control:
            self.setCursor(QtCore.Qt.SizeAllCursor)
            self.update()
        
        elif event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            if event.modifiers() in (QtCore.Qt.NoModifier, QtCore.Qt.KeypadModifier):
                self.end_edit()
            elif event.modifiers() in (QtCore.Qt.ControlModifier, QtCore.Qt.ControlModifier|QtCore.Qt.KeypadModifier):
                self.textCursor().insertHtml("<BR \\>\n")
        else:
            super(LabelerTextItem, self).keyPressEvent(event)
        
    def setFont(self, font):
        """ Overrided to add calc for leading/line spacing, and to correct QT bug with letter spacing under 16pt """
        #self.setScale(1)
        self.setHtml(htmlFontRE.sub("<body style=\" font-family:'%s'; font-size:%d" % (font.family(), font.pointSizeF()), str(self.toHtml())))
        #super(LabelerTextItem, self).setFont(font)
        #width = float(self.document().size().height())

        #size = font.pointSizeF()
        metric = QtGui.QFontMetricsF(font)
        #width = metric.width(self.toPlainText())
        
        #width = metric.width(self.toHtml())
        #height = metric.height()
        #height = self.document().size().width()
        height = metric.boundingRect(self.toPlainText()).width()
        
        #height = metric.boundingRect(self.toHtml()).height()
        size = font.pointSizeF()
        if size < 20.0 and str(self.toPlainText()) != "":
            font.setPointSizeF(20.0)
            super(LabelerTextItem, self).setFont(font)
            metric = QtGui.QFontMetricsF(font)
            #newwidth = float(self.document().size().height())
            #print width, newwidth
            #newheight = self.document().size().width()
            newheight = metric.boundingRect(self.toPlainText()).width()
            if 0 in (height, newheight) :
                new = size / self.perfectFontSize
                self.setScale(new)
            else:
                #newy = height / newheight
                newy = size / self.perfectFontSize
                newy = height/newheight
                #newx = width/newwidth
                self.setScale(newy)
        else:
            self.setScale(1.0)
        
        super(LabelerTextItem, self).setFont(font)
            
        self.leading = self.font().pointSize()*self.lineSpacing
        
    def update_block_formatting(self):
        cur = self.textCursor()
        cur.select(cur.Document)
        
        bf = cur.blockFormat()
        bf.setLineHeight(self.lineSpacing, bf.ProportionalHeight)
        cur.setBlockFormat(bf)  
        
        
    def setHtml(self, text):
        #super(LabelerTextItem, self).setPlainText(text)
        super(LabelerTextItem, self).setHtml(text)
        #if not self.setUp:
        #    print "DDDDDDDDDD"
        #self.strip_html()
        #self.update_text()
        #print self.toHtml()
        #
        #    if string <> self.propWidgets['Value'].toPlainText():
        #        self.propWidgets['Value'].setPlainText(self.toPlainText())
                
        self.update_block_formatting()
              
        
        #cur.clearSelection()
        #self.setTextCursor(cur)
        
    def update_text(self):
        #if self.setUp:
            if not self.merging and not self._setTextFromUpdate:
                self.propNames["Text"].enable_updates(False)
                
                #self.propNames["Text"].set_text(self.toPlainText())
                text = self.coreHtml.replace(self.htmlLabelEnd, "").replace(self.htmlLabelStart, "")
                text = spanRemoveRE.sub("", text)
                text = text.replace("</span>", "")
                self.propNames["Text"].set_text(text)
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
