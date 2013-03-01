from PyQt4 import QtGui, QtCore
from collections import namedtuple


LabelProp = namedtuple("LabelProp", ("propName", "propType", "propValue"))

class LabelItemProperty(QtCore.QObject):
    def __init__(self, name):
        super(LabelItemProperty, self).__init__()
        self._updateEnabled = True
        self.name = name
        self.widgets = {}
        self.widgetOrder = []
        self.updateSignal = None
        self.value = None
        self.type = None
        
    def enable_updates(self, update = True):
        """ Call this before updating if you do not want a signal being emitted, call again to turn it on, update is whether to turn it on or off """
        self._updateEnabled = update
        
    def get_value(self):
        """ Returns a copy of the underlying value """
        return self.type(self.value)
        
    def emit_update(self):
        """ Convenience Method, This will call the properties' self.updateSignal, with a copy of self.value, using self.type to create, as its only argument """
        if not self._updateEnabled:
            return
        if self.updateSignal <> None and self.value <> None:
            self.emit(self.updateSignal, self.type(self.value))
        else:
            raise ValueError("updateSignal or value not set")
        
class LabelFontProperty(LabelItemProperty):
    def __init__(self, name, font=None):
        """ Accepts a QFont, or QVariant as the property """
        super(LabelFontProperty, self).__init__(name)
        
        self.type = QtGui.QFont
        if font <> None:
            self.value = QtGui.QFont(font)
        else:
            self.value = QtGui.QFont("Arial", 9, QtGui.QFont.Normal, False)
        for i in  ["Family", "Size", "Bold", "Italic"]:
            self.widgetOrder.append(i)
        #self.widgets = {}
        
        self.widgets["Family"] = QtGui.QFontComboBox()
        self.widgets["Family"].setCurrentFont(self.value)
        self.connect(self.widgets["Family"], QtCore.SIGNAL("currentFontChanged(QFont)"), self.update_font_family)
        
        self.widgets["Point Size"] = QtGui.QDoubleSpinBox()
        self.widgets["Point Size"].setValue(self.value.pointSizeF())
        self.widgets["Point Size"].setMinimum(1.0)
        self.widgets["Point Size"].setMaximum(1000.0)
        self.connect(self.widgets["Point Size"], QtCore.SIGNAL("valueChanged(double)"), self.update_font_point_size)
        
        self.widgets["Bold"] = QtGui.QCheckBox("")
        self.widgets["Bold"].setChecked(self.value.bold())
        self.connect(self.widgets["Bold"], QtCore.SIGNAL("toggled(bool)"), self.update_font_bold)
        
        self.widgets["Italic"] = QtGui.QCheckBox("")
        self.widgets["Italic"].setChecked(self.value.italic())
        self.connect(self.widgets["Italic"], QtCore.SIGNAL("toggled(bool)"), self.update_font_italic)
        
        #self.widgets["Spacing"] = QtGui.QDoubleSpinBox()
        #self.widgets["Spacing"].setValue(self.value.pointSizeF())
        #self.widgets["Spacing"].setMinimum(1.0)
        #self.widgets["Spacing"].setMaximum(1000.0)
        #self.connect(self.widgets["Spacing"], QtCore.SIGNAL("valueChanged(double)"), self.update_font_spacing)
        
        
        self.updateSignal = QtCore.SIGNAL("fontChanged(QFont)")
        
    
        
    def update_font_family(self, font):
        """ This method takes a QFont and uses it to alter the font family of the underlying font """
        self.value.setFamily(font.family())
        self.emit_update()
        
    def update_font_bold(self, bold):
        self.value.setBold(bold)
        self.emit_update()
        
    def update_font_point_size(self, size):
        self.value.setPointSizeF(size)
        self.emit_update()
        
    def update_font_italic(self, italic):
        self.value.setItalic(italic)
        self.emit_update()
        
    def get_font(self):
        """ This returns a copy of the underlying font """
        return QtGui.QFont(self.value)
    
    def get_value(self):
        """ Returns the font """
        return QtGui.QFont(self.value)
        
        
class LabelTextAreaProperty(LabelItemProperty):
    def __init__(self, name, text=None):
        
        super(LabelTextAreaProperty, self).__init__(name)
        if text <> None:
            self.value = QtCore.QString(text)
        else:
            self.value = QtCore.QString()
            
        self.widgetOrder.append("Text")
        self.widgets["Value"] = QtGui.QTextEdit()
        self.widgets["Value"].setPlainText(self.value)
        self.connect(self.widgets["Value"], QtCore.SIGNAL("textChanged(QString)"), self.update_text)
        
        self.updateSignal = QtCore.SIGNAL("textChanged(QString)")
        
    def set_text(self, text):
        self.widgets["Value"].setPlainText(text)
        
    def update_text(self, text):
        self.value = QtCore.QString(text)
        self.emit_update()
            
        
class LabelTextLineProperty(LabelItemProperty):
    def __init__(self, name, text=None):
        
        super(LabelTextLineProperty, self).__init__(name)
        if text <> None:
            self.value = QtCore.QString(text)
        else:
            self.value = QtCore.QString()
            
        self.widgetOrder.append("Text")
        self.widgets["Text"] = QtGui.QLineEdit()
        self.widgets["Text"].setPlainText(self.value)
        self.connect(self.widgets["Text"], QtCore.SIGNAL("textChanged(QString)"), self.update_text)
        
        self.updateSignal = QtCore.SIGNAL("textChanged(QString)")
        
    def set_text(self, text):
        self.widgets["Text"].setPlainText(text)
        
    def update_text(self, text):
        self.value = QtCore.QString(text)
        self.emit_update()
        
class LabelDoubleProperty(LabelItemProperty):
    def __init__(self, name, value=None):
        super(LabelDoubleProperty, self).__init__(name)
        self.type = float
        if value <> None:
            self.value = float(value)
        else:
            self.value = 0.0
        
        self.widgetOrder.append("Value")
        self.widgets["Value"] = QtGui.QDoubleSpinBox()
        self.widgets["Value"].setValue(self.value)
        self.widgets["Value"].setMinimum(0.0)
        self.widgets["Value"].setMaximum(1000.0)
        self.connect(self.widgets["Value"], QtCore.SIGNAL("valueChanged(double)"), self.update_double)
        
        self.updateSignal = QtCore.SIGNAL("valueChanged(double)")
        
    
    def set_min(self, minimum):
        self.widgets["Value"].setMinimum(float(minimum))
        
    def set_max(self, maximum):
        self.widgets["Value"].setMaximum(float(maximum))
        
    def set_range(self, maximum, minimum):
        self.widgets["Value"].setMinimum(float(minimum))
        self.widgets["Value"].setMaximum(float(maximum))
        
    def set_value(self, value):
        self.widgets["Value"].setValue(value)

    def update_double(self, value):
        self.value = float(value)
        self.emit_update()
        
class LabelIntegerProperty(LabelItemProperty):
    def __init__(self, name, value=None):
        super(LabelIntegerProperty, self).__init__(name)
        self.type = int
        if value <> None:
            self.value = int(value)
        else:
            self.value = 0
            
        self.widgetOrder.append("Value")
        self.widgets["Value"] = QtGui.QSpinBox()
        self.widgets["Value"].setMinimum(0)
        self.widgets["Value"].setMaximum(10000)
        self.widgets["Value"].setValue(self.value)
        self.connect(self.widgets["Value"], QtCore.SIGNAL("valueChanged(int)"), self.update_integer)
        
        
        self.updateSignal = QtCore.SIGNAL("valueChanged(int)")
        
    def update_integer(self, value):
        self.value = int(value)
        self.emit_update()
        
    def set_min(self, minimum):
        self.widgets["Value"].setMinimum(int(minimum))
        
    def set_max(self, maximum):
        self.widgets["Value"].setMaximum(int(maximum))
        
    def set_range(self, maximum, minimum):
        self.widgets["Value"].setMinimum(int(minimum))
        self.widgets["Value"].setMaximum(int(maximum))
        
class LabelListProperty(LabelItemProperty):
    def __init__(self, name, value=None):
        super(LabelListProperty, self).__init__(name)
        self.updateSignal = QtCore.SIGNAL("selectionChanged(QString)")

class LabelBooleanProperty(LabelItemProperty):
    def __init__(self, name, value=None):
        super(LabelBooleanProperty, self).__init__(name)
        self.updateSignal = QtCore.SIGNAL("toggled(bool)")
        self.type = bool
        if value == None:
            self.value = False
        else:
            self.value = True
        
        self.widgets["Value"] = QtGui.QCheckBox("")
        self.widgets["Value"].setChecked(self.value)
        self.connect(self.widgets["Value"], QtCore.SIGNAL("toggled(bool)"), self.update_checked)
        
    def update_checked(self, toggle):
        self.value = bool(toggle)
        self.emit_update()
        