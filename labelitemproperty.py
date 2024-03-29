from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from collections import namedtuple
import os.path
import defaults

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
        
    def clean_up(self):
        for widget in list(self.widgets.values()):
            widget.setParent(None)
        
    def override_value(self, value):
        self.value = self.type(value)
        self.emit_update()
        
    def enable_updates(self, update = True):
        """ Call this before updating if you do not want a signal being emitted, call again to turn it on, update is whether to turn it on or off """
        self._updateEnabled = update
        
    def get_value(self):
        """ Returns a copy of the underlying value """
        return self.type(self.value)
    
    def set_value(self, value):
        """ This must be overridden to set the value, based on a value coming from QSettings """
        print("ERRRRRR")
        
    def emit_update(self):
        """ Convenience Method, This will call the properties' self.updateSignal, with a copy of self.value, using self.type to create, as its only argument """
        if not self._updateEnabled:
            return
            
        if self.updateSignal != None and self.value != None:
#             self.emit(self.updateSignal, self.type(self.value))
            print("emit_update self.type:", self.type)
            print("emit_update self.value:", self.value)
            # print("to be emitted:", self.type(self.value))
            # print("dir(self.updateSignal.emit):", dir(self.updateSignal.emit))
            self.updateSignal.emit(self.type(self.value))
        else:
            raise ValueError("updateSignal or value not set")
        
class LabelFontProperty(LabelItemProperty):
    fontChanged = pyqtSignal(QtGui.QFont)
    
    def __init__(self, name, font=None):
        """ Accepts a QFont, or QVariant as the property """
        super(LabelFontProperty, self).__init__(name)
        
        self.type = QtGui.QFont
        if font != None:
            self.value = QtGui.QFont(font)
        else:
            self.value = QtGui.QFont("Arial", 9, QtGui.QFont.Normal, False)
        for i in  ["Family", "Point Size", "Bold", "Italic"]:
            self.widgetOrder.append(i)
        #self.widgets = {}
        
        self.widgets["Family"] = QtWidgets.QFontComboBox()
        self.widgets["Family"].setCurrentFont(self.value)
        # self.connect(self.widgets["Family"], QtCore.SIGNAL("currentFontChanged(QFont)"), self.update_font_family)
        self.widgets["Family"].currentFontChanged.connect(self.update_font_family)
        
        self.widgets["Point Size"] = QtWidgets.QDoubleSpinBox()
        self.widgets["Point Size"].setValue(self.value.pointSizeF())
        self.widgets["Point Size"].setMinimum(1.0)
        self.widgets["Point Size"].setMaximum(1000.0)
        self.widgets["Point Size"].setKeyboardTracking(False)
        #self.connect(self.widgets["Point Size"], QtCore.SIGNAL("valueChanged(double)"), self.update_font_point_size)
        self.widgets["Point Size"].valueChanged.connect(self.update_font_point_size)
        
        self.widgets["Bold"] = QtWidgets.QCheckBox("")
        self.widgets["Bold"].setChecked(self.value.bold())
        #self.connect(self.widgets["Bold"], QtCore.SIGNAL("toggled(bool)"), self.update_font_bold)
        self.widgets["Bold"].toggled.connect(self.update_font_bold)
        
        self.widgets["Italic"] = QtWidgets.QCheckBox("")
        self.widgets["Italic"].setChecked(self.value.italic())
        #self.connect(self.widgets["Italic"], QtCore.SIGNAL("toggled(bool)"), self.update_font_italic)
        self.widgets["Italic"].toggled.connect(self.update_font_italic)
        
        #self.widgets["Spacing"] = QtWidgets.QDoubleSpinBox()
        #self.widgets["Spacing"].setValue(self.value.pointSizeF())
        #self.widgets["Spacing"].setMinimum(1.0)
        #self.widgets["Spacing"].setMaximum(1000.0)
        #self.connect(self.widgets["Spacing"], QtCore.SIGNAL("valueChanged(double)"), self.update_font_spacing)
        
        
        #self.updateSignal = QtCore.SIGNAL("fontChanged(QFont)")
        self.updateSignal = self.fontChanged
        
        
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
    
    def set_value(self, value):
        self.value = QtGui.QFont(value)
        self.widgets["Family"].setCurrentFont(self.value)
        self.widgets["Point Size"].setValue(self.value.pointSizeF())
        self.widgets["Bold"].setChecked(self.value.bold())
        self.widgets["Italic"].setChecked(self.value.italic())
        self.emit_update()
        
        
class LabelTextAreaProperty(LabelItemProperty):
    textChanged = pyqtSignal(str)
    
    def __init__(self, name, text=None):
        
        super(LabelTextAreaProperty, self).__init__(name)
#         if text != None:
#             self.value = QtCore.QString(text)
#         else:
#             self.value = QtCore.QString()
        self.text = "" or text
        self.type = str
            
        self.widgetOrder.append("Value")
        self.widgets["Value"] = QtWidgets.QTextEdit()
        self.widgets["Value"].setPlainText(self.value)
        #self.connect(self.widgets["Value"], QtCore.SIGNAL("textChanged()"), self.update_text)
        self.widgets["Value"].textChanged.connect(self.update_text)
        
#         self.updateSignal = QtCore.SIGNAL("textChanged(QString)")
        self.updateSignal = self.textChanged
        
    def set_text(self, text):
        self.widgets["Value"].setPlainText(text)
        self.emit_update()
        
    def update_text(self):
        self.value = self.widgets["Value"].toPlainText()
        
        self.emit_update()
        
    def insert_text(self, text):
        self.widgets["Value"].textCursor().insertText(text)
        
    def set_value(self, value):
#         try:
#             self.value = QtCore.QString(value.toString())
#         except:
#             self.value = QtCore.QString(value)
        self.value = str(value.value())
        self.widgets["Value"].setPlainText(self.value)
        self.emit_update()
        
class LabelTextLineProperty(LabelItemProperty):
    textChanged = pyqtSignal(str)
    
    def __init__(self, name, text=None):
        
        super(LabelTextLineProperty, self).__init__(name)
#         if text != None:
#             self.value = QtCore.QString(text)
#         else:
#             self.value = QtCore.QString()
        self.value = text or ""
            
        #self.type = QtCore.QString
        self.type = str
            
        self.widgetOrder.append("Value")
        self.widgets["Value"] = QtWidgets.QLineEdit()
        self.widgets["Value"].setPlainText(self.value)
        #self.connect(self.widgets["Value"], QtCore.SIGNAL("textChanged(QString)"), self.update_text)
#         self.widgets["Value"].textChanged(QString).connect(self.update_text)
        self.widgets["Value"].textChanged.connect(self.update_text)
        #self.updateSignal = QtCore.SIGNAL("textChanged(QString)")
        self.updateSignal = self.textChanged
        
    def set_text(self, text):
        self.widgets["Value"].setPlainText(text)
        self.emit_update()
        
    def update_text(self, text):
        #self.value = QtCore.QString(text)
        self.value = str(text)
        self.emit_update()
        
    def set_value(self, value):
        #self.value = QtCore.QString(value)
        self.value = str(value)
        self.widgets["Value"].setPlainText(self.value)
        self.emit_update()
        
class LabelFilenameProperty(LabelItemProperty):
    textChanged = pyqtSignal(str)
    
    def __init__(self, name, text=None):
        
        super(LabelFilenameProperty, self).__init__(name)
        
        self.fileFilter = ""
        self.fileDialog = QtWidgets.QFileDialog()
        self.fileDialog.setFileMode(self.fileDialog.ExistingFile)
        self.filterUsed = ""
        if text != None and text != '':
            self.currentDirectory = os.path.split(text)[0]
            if self.currentDirectory == '':
                self.currentDirectory = defaults.properties.imageDirectory
            self.value = QtCore.QString(text)
        else:
            self.currentDirectory = defaults.properties.imageDirectory
            #self.value = QtCore.QString(defaults.properties.imageDirectory)
            self.value = defaults.properties.imageDirectory
        
        self.fileDialog.setDirectory(self.currentDirectory)
            
        
        #self.type = QtCore.QString
        self.type = str
            
        self.widgetOrder.append("Value")
        self.widgetOrder.append("Select File...")
        self.widgets["Value"] = QtWidgets.QLineEdit()
        self.widgets["Select File..."] = QtWidgets.QPushButton("Select File...")
        self.widgets["Value"].setText(self.value)
        #self.connect(self.widgets["Value"], QtCore.SIGNAL("textChanged(QString)"), self.update_text)
        self.widgets["Value"].textChanged.connect(self.update_text)
        #self.connect(self.widgets["Select File..."], QtCore.SIGNAL("clicked()"), self.get_filename)
        self.widgets["Select File..."].clicked.connect(self.get_filename)
        
        #self.updateSignal = QtCore.SIGNAL("textChanged(QString)")
        # replaced with pyqtSignal just above __init__.
        self.updateSignal = self.textChanged
        
    def set_text(self, text):
        self.widgets["Value"].setPlainText(text)
        self.emit_update()
        
    def set_file_filter(self, fileFilter):
        self.fileFilter = fileFilter
        
        
    def get_filename(self):
        print((self.currentDirectory))
        ret = QtWidgets.QFileDialog.getOpenFileNameAndFilter(parent=self.widgets["Value"].window(), caption="Open an Image...", directory=self.currentDirectory, filter=self.fileFilter) 
        if str(ret[0]) != '':
            self.currentDirectory = os.path.split(str(ret[0]))[0]
            self.value = str(ret[0])
            self.widgets["Value"].setText(self.value)
            #self.emit_update()

    
    def update_text(self, text):
        #self.value = QtCore.QString(text)
        self.value = str(text)
        self.emit_update()
        
    def set_value(self, value):
        print(value)
        if type(value) == QtCore.QVariant:
            #self.value = value.toString()
            self.value = str(value.value())
        else:
            self.value = QtCore.QString(value)
        self.widgets["Value"].setText(self.value)
        self.emit_update()
        
class LabelDoubleProperty(LabelItemProperty):
    valueChanged = pyqtSignal(float)
    
    def __init__(self, name, value=None):
        super(LabelDoubleProperty, self).__init__(name)
        self.type = float
        if value != None:
            self.value = float(value)
        else:
            self.value = 0.0
            
        
        self.widgetOrder.append("Value")
        self.widgets["Value"] = QtWidgets.QDoubleSpinBox()
        self.widgets["Value"].setMinimum(0.0)
        self.widgets["Value"].setMaximum(1000.0)
        self.widgets["Value"].setKeyboardTracking(False)
        
        self.widgets["Value"].setValue(self.value)
        #self.connect(self.widgets["Value"], QtCore.SIGNAL("valueChanged(double)"), self.update_double)
        self.widgets["Value"].valueChanged.connect(self.update_double)
        
        #self.updateSignal = QtCore.SIGNAL("valueChanged(double)")
        self.updateSignal = self.valueChanged
        
    
    def set_min(self, minimum):
        self.widgets["Value"].setMinimum(float(minimum))
        
    def set_max(self, maximum):
        self.widgets["Value"].setMaximum(float(maximum))
        
    def set_range(self, maximum, minimum):
        self.widgets["Value"].setMinimum(float(minimum))
        self.widgets["Value"].setMaximum(float(maximum))
        
    def set_step(self, step):
        self.widgets["Value"].setSingleStep(step)
        
    def set_double(self, value):
        self.widgets["Value"].setValue(value)

    def update_double(self, value):
        self.value = float(value)
        self.emit_update()
        
    def set_value(self, value):
        # print("[LabelDoubleProperty] set_value value:", value)
        # from pprint import pprint
        # print("dir(value): ")
        # pprint(dir(value))
        # print("[LabelDoubleProperty] set_value value value():", value.value())
    
        try:
            #self.value = value.toFloat()[0]
            self.value = value.toFloat()[0]
        except:
            self.value = value.value()
        self.widgets["Value"].setValue(float(self.value))
        self.emit_update()
        
class LabelIntegerProperty(LabelItemProperty):
    valueChanged = pyqtSignal(int)
    
    def __init__(self, name, value=None):
        super(LabelIntegerProperty, self).__init__(name)
        self.type = int
        if value != None:
            self.value = int(value)
        else:
            self.value = 0
            
        self.widgetOrder.append("Value")
        self.widgets["Value"] = QtWidgets.QSpinBox()
        self.widgets["Value"].setMinimum(0)
        self.widgets["Value"].setMaximum(10000)
        self.widgets["Value"].setValue(self.value)
        self.widgets["Value"].setKeyboardTracking(False)
        #self.connect(self.widgets["Value"], QtCore.SIGNAL("valueChanged(int)"), self.update_integer)
        self.widgets["Value"].valueChanged.connect(self.update_integer)
        
        
        #self.updateSignal = QtCore.SIGNAL("valueChanged(int)")
        self.updateSignal = self.valueChanged
        
        
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
        
    def set_value(self, value):
        self.value = int(value)
        self.widgets["Value"].setValue(self.value)
        self.emit_update()
        
class LabelListProperty(LabelItemProperty):
    #selectionChanged = pyqtSignal(QtCore.QObject)
    # Marvin 15/12/2021: Maybe use python's "object" class instead?
    # It works :D No more error involving extra unexpected arguments passed!
    selectionChanged = pyqtSignal(object)
    
    def __init__(self, name, value=None):
        super(LabelListProperty, self).__init__(name)
        
        self.type = str
        #self.updateSignal = QtCore.SIGNAL("selectionChanged(PyQt_PyObject)")
        self.updateSignal = self.selectionChanged
        
        if value[1] == None:
            #self.value = QtCore.QString(value[0][0])
            self.value = str(value[0][0])
        else:
            #self.value = QtCore.QString(value[1])
            self.value = str(value[1])
        
        self.widgetOrder.append("Value")
        self.widgets["Value"] = QtWidgets.QComboBox()
        self.widgets["Value"].addItems(value[0])
        
        if value[1] != None:
            #index = self.widgets["Value"].findData(QtCore.QString(self.value))
            index = self.widgets["Value"].findData(str(self.value))
            if index != -1:
                self.widgets["Value"].setCurrentIndex(index)
            else:
                
                raise ValueError("'%s', value not in list" % str(self.value))
            
        #self.connect(self.widgets["Value"], QtCore.SIGNAL("currentIndexChanged(QString)"), self.update_selection)
        self.widgets["Value"].currentIndexChanged.connect(self.update_selection)
        
    def update_selection(self, value):
        #self.value = QtCore.QString(value) # <-- Original.
        
        #self.value = str(value)
        
        # Marvin 15/12/2021 - Maybe this should work?
        if isinstance(value, QtCore.QVariant):
            self.value = str(value.value())
        else:
            self.value = str(value)
            
        self.emit_update()
        
    def set_value(self, value):
        # try:
            # #self.value = QtCore.QString(value)
            # self.value = str(value.value())
        # except TypeError:
            # self.value = value.toString()
            
        try:
            self.value = str(value.value())
        except TypeError:
            #self.value = value.toString()
            self.value = str(value)
            
        index = self.widgets["Value"].findText(str(self.value))
        if index != -1:
            self.widgets["Value"].setCurrentIndex(index)
        else:
            raise ValueError("'%s', value not in list" % str(self.value))
        self.emit_update()
        
    def get_value(self):
        return self.value
                
        

class LabelBooleanProperty(LabelItemProperty):
    toggled = pyqtSignal(bool)
    
    def __init__(self, name, value=None):
        super(LabelBooleanProperty, self).__init__(name)
        #self.updateSignal = QtCore.SIGNAL("toggled(bool)")
        self.updateSignal = self.toggled
        
        self.type = bool
        if value == None:
            self.value = False
        else:
            self.value = value
        
        self.widgetOrder.append("Value")
        self.widgets["Value"] = QtWidgets.QCheckBox("")
        self.widgets["Value"].setChecked(self.value)
        # self.connect(self.widgets["Value"], QtCore.SIGNAL("toggled(bool)"), self.update_checked)
        self.widgets["Value"].toggled.connect(self.update_checked)
        
    def update_checked(self, toggle):
        self.value = bool(toggle)
        self.emit_update()
        
    def set_value(self, value):
        if type(value) == QtCore.QVariant:
            self.value = bool(value.value()) #.toBool()
        else:
            self.value = bool(value)
        self.widgets["Value"].setChecked(self.value)
        self.emit_update()
        