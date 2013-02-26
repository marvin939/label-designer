from PyQt4 import QtGui, QtCore

class LabelItemProperty(QtCore.QObject):
    pass
        
        
class LabelFontProperty(LabelItemProperty):
    def __init__(self, font=None):
        """ Takes a QFont as the property """
        super(LabelFontProperty, self).__init__()
        if font <> None:
            self.value = font
        else:
            self.value = QtGui.QFont("Arial", 9, QtGui.QFont.Bold, False)
        self.widgetOrder = ["Family", "Size", "Bold", "Italic", "Spacing"]
        self.widgets = {}
        
        self.widgets["Family"] = QtGui.QFontComboBox()
        self.widgets["Family"].setCurrentFont(self.value)
        
        self.widgets["Point Size"] = QtGui.QDoubleSpinBox()
        self.widgets["Point Size"].setValue(self.value.pointSizeF())
        self.widgets["Point Size"].setMinimum(1.0)
        self.widgets["Point Size"].setMaximum(1000.0)
        
        self.widgets["Bold"] = QtGui.QCheckBox("")
        self.widgets["Bold"].setChecked(self.value.weight() == self.value.Bold)
        
        self.widgets["Italic"] = QtGui.QCheckBox("")
        self.widgets["Italic"].setChecked(self.value.italic())
        
        self.widgets["Spacing"] = QtGui.QDoubleSpinBox()
        self.widgets["Spacing"].setValue(self.value.pointSizeF())
        self.widgets["Spacing"].setMinimum(1.0)
        self.widgets["Spacing"].setMaximum(1000.0)
        
        
        self.updateSignal = QtCore.SIGNAL("fontChanged(QFont)")
        
    def get_font(self):
        return self.value
        
    def restore(self, value):
        """ This takes a QVariant (like that returned by QSettings), and restores the font """
        self.value = QtGui.QFont.fromString(value.toString())
        return self.value
    
    def family(self):
        return self.value.family()
    
    def size(self):
        return self.value.pointSizeF()
    
    def bold(self):
        return self.value.weight() == self.value.Bold
    
    def italic(self):
        return self.value.italic()
        
    def set_family(self, family):
        self.value.setFamily(family)
        self.emit(self.updateSignal, self.value)
    
    def set_size(self, size):
        self.value.setSizeF(size)
        
    def set_bold(self, bold=True):
        if bold:
            self.value.setWeight(self.value.Bold)
        else:
            self.value.setWeight(self.value.Normal)
            
    def set_italic(self, italic=True):
        self.value.setItalic(italic)
            
        
        