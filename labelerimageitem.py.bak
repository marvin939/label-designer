from PyQt4 import QtCore, QtGui
from labeleritemmixin import LabelerItemMixin, LabelProp
import re
import defaults
import os.path
brTagRE = re.compile(r"<BR\s*/?>", re.IGNORECASE)
htmlFontRE = re.compile(r"<body style=\" font-family:'.*?';")
spanRemoveRE = re.compile(r"<span style.*?>")

class LabelerImageItem(QtGui.QGraphicsPixmapItem, LabelerItemMixin):
    propLoadOrder = ["Image Location","X Coord","Y Coord","Is Conditional","Condition","X Scale","Y Scale"]
    def __init__(self, name, *args, **kwargs):
        
        
        
        self.merging = False
        
        super(LabelerImageItem, self).__init__(*args, **kwargs)
        
        LabelerItemMixin.__init__(self, name)
        
        self.objectType = "Image"
        self.currentScale = [1.0, 1.0]
        self.oldScale = [1.0, 1.0]
        
        self.setScale(1.0)
             
        self.imageLoc = defaults.properties.defaultImage
        self.update_image(self.imageLoc)
        
        #self.originalPixmap = QtGui.QPixmap(self.imageLoc)
        #self.setPixmap(self.originalPixmap)
        #self.setTransformationMode(QtCore.Qt.SmoothTransformation)
        
        properties = [LabelProp(propName='Image Location', propType='filename', propValue=self.imageLoc),
                      LabelProp(propName='X Coord', propType='double', propValue=self.scenePos().x()),
                      LabelProp(propName='Y Coord', propType='double', propValue=self.scenePos().y()),
                      LabelProp(propName='Is Conditional', propType='boolean', propValue=False),
                      LabelProp(propName='Condition', propType='textarea', propValue=''),
                      LabelProp(propName="X Scale", propType="double", propValue=1),
                      LabelProp(propName="Y Scale", propType="double", propValue=1)
                      ]
        
        self.propCallbacks["Image Location"] = self.filename_changed
        self.propCallbacks["X Coord"] = self.setX
        self.propCallbacks["Y Coord"] = self.setY
        self.propCallbacks["Is Conditional"] = self.conditional_toggle  
        self.propCallbacks["Condition"] = self.update_condition
        self.propCallbacks["X Scale"] = self.scale_x
        self.propCallbacks["Y Scale"] = self.scale_y
        self.load_properties(properties)
        
        self.propNames["X Scale"].set_min(0.01)
        self.propNames["Y Scale"].set_min(0.01)
        self.propNames["X Scale"].set_step(0.01)
        self.propNames["Y Scale"].set_step(0.01)
        
        self.set_pos_by_mm(5,4)
        
        
        
        
        self.setFlags(self.ItemIsSelectable|self.ItemIsMovable|self.ItemIsFocusable|self.ItemSendsGeometryChanges|self.ItemSendsScenePositionChanges)
        self.setAcceptHoverEvents(True)
        
        
        
        self.conditional = self.propNames["Is Conditional"].get_value()
        self.condition = self.propNames["Condition"].get_value()
        self.propNames["Image Location"].set_file_filter("Images (*.png *.jpeg *.jpg *.tiff *.bmp *.gif *.tga *.tif);;")
        
        self.update_pos_props()
        
    def mouseReleaseEvent(self, *args, **kwargs):
        self.update_pos_props()
        super(LabelerImageItem, self).mouseReleaseEvent(*args, **kwargs)
        
    def update_pos_props(self):
        
        self.propNames["X Coord"].enable_updates(False)
        self.propNames["Y Coord"].enable_updates(False)
        
        self.propNames["X Coord"].set_double(self.scenePos().x())
        self.propNames["Y Coord"].set_double(self.scenePos().y())
        
        self.propNames["X Coord"].enable_updates(True)
        self.propNames["Y Coord"].enable_updates(True)
        
    def update_condition(self, value):
        self.condition = value
        
    def conditional_toggle(self, toggle):
        self.conditional = toggle
        
    def update_image(self, text):
        print "setting"
        pixmap = QtGui.QPixmap(text)
        
        self.setPixmap(pixmap)
        #self.setHtml("<img src=\"%s\">" % text) 
        
    def scale_x(self, val):
        self.currentScale[0] = val
        self.update_scale()
        
    def scale_y(self, val):
        self.currentScale[1] = val
        self.update_scale()
        
    def update_scale(self):
        #pixmap = QtGui.QPixmap(self.originalPixmap)
        #if pixmap.isNull():
        #    return
        
        #width = pixmap.width()
        #height = pixmap.height()
        #newWidth = width*self.currentScale[0]
        #newHeight = height*self.currentScale[1]
        #pixmap = pixmap.scaled(newWidth, newHeight)
        #self.setPixmap(pixmap)
        newScale = [(1.0/self.oldScale[0]) * self.currentScale[0], (1.0/self.oldScale[1]) * self.currentScale[1]]
        print newScale, self.oldScale, self.currentScale
        self.oldScale = self.currentScale[:]
        self.scale(*newScale)
        
    def setOffset(self, *args, **kwargs):
        
        super(LabelerImageItem, self).setPos(*args, **kwargs)
        
        # Disables updating of widgets to avoid an infinite loop
        self.update_pos_props()
        
    def setX(self, value):
        self.setOffset(value, self.y())
        
    def setY(self, value):
        self.setOffset(self.x(), value )
     
        
    def get_merge_text(self):
        if not self.merging:
            #return self.toPlainText()
            #return self.coreHtml
            return str(self.propNames["Image Location"].get_value())
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
        
    def start_merge(self):
        #self.mergeText = self.toPlainText()
        self.mergeText = self.imageLoc
        self.merging = True
        
        
    def end_merge(self):
        #self.setPlainText(self.mergeText)
        self.imageLoc = self.mergeText
        self.merging = False
        self.setVisible(True)
        
    
        
    def merge_row(self, row):
        if self.conditional:
            try:
                if "=" in self.condition:
                    left, right = self.condition.split("=")
                    left = self.get_merged_value(left, row)
                    right = self.get_merged_value(right, row)
                    if left <> right:
                        self.setVisible(False)
                        return
                    else:
                        self.setVisible(True)
                elif "<>" in self.condition:
                    left, right = self.condition.split("<>")
                    left = self.get_merged_value(left, row)
                    right = self.get_merged_value(right, row)
                    if left <> right:
                        self.setVisible(True)
                    else:
                        self.setVisible(False)
                        return
                elif "!=" in self.condition:
                    left, right = self.condition.split("!=")
                    left = self.get_merged_value(left, row)
                    right = self.get_merged_value(right, row)
                    if left <> right:
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
        
        if text <> self.mergeText:
            self.update_image(text)
            self.update_scale()
            
        
        
    def filename_changed(self):
        self.imageLoc = self.propNames['Image Location'].get_value()
        #if not os.path.isfile(self.imageLoc):
        #    self.originalPixmap = QtGui.QPixmap()
        #else:
        #    self.originalPixmap = QtGui.QPixmap(self.imageLoc)
        #self.setPixmap(self.originalPixmap)
        #self.update_scale()
        self.update_image(self.imageLoc)
        
            
    
    
    def mousePressEvent(self, event):
        if self.isSelected():
            if event.modifiers() == QtCore.Qt.ControlModifier:
                self.end_edit()
            else:
                self.start_edit()
            
        super(LabelerImageItem, self).mousePressEvent(event)
        
    def keyReleaseEvent(self, event):
        super(LabelerImageItem, self).keyReleaseEvent(event)
        if event.key() == QtCore.Qt.Key_Control:
                self.setCursor(QtCore.Qt.ArrowCursor)
        #self.propNames['Text'].set_text(self.toPlainText())
        self.propNames['Text'].set_text(self.coreHtml.replace(self.htmlLabelEnd, "").replace(self.htmlLabelStart, ""))
        
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
        
        
        else:
            super(LabelerImageItem, self).keyPressEvent(event)
   