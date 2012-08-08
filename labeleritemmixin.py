from PyQt4 import QtGui, QtCore
import re

class LabelerItemMixin:
    fontDB = QtGui.QFontDatabase()
    propertyTypes = {'string':(QtGui.QLineEdit, QtCore.SIGNAL('textChanged(QString)')),
                 'text':(QtGui.QTextEdit, QtCore.SIGNAL('textChanged()')), 
                 'integer':(QtGui.QSpinBox, QtCore.SIGNAL('valueChanged(int)')), 
                 'float':(QtGui.QDoubleSpinBox, QtCore.SIGNAL('valueChanged(double)')), 
                 'list':(QtGui.QComboBox, QtCore.SIGNAL('currentIndexChanged(int)')), 
                 'boolean':(QtGui.QCheckBox, QtCore.SIGNAL('toggled(bool)')),
                 'font':(QtGui.QFontComboBox, QtCore.SIGNAL('currentFontChanged(QFont)'))}
    headerRE = re.compile('<<.*?>>')
    def __init__(self, properties = None, proporder = None):
        if properties == None:
            self.properties = {}
            self.propOrder = []
        else:
            self.properties = properties
            if proporder <> None:
                self.propOrder = proporder 
            else:
                self.proporder = self.properties.keys()
                self.proporder.sort()
        self.propWidgets = {}
        
        self.create_property_widgets()
        
        
        self.dpi = QtCore.QCoreApplication.instance().dpi
        self.dpmm = QtCore.QCoreApplication.instance().dpmm
        
    def get_merge_text(self):
        """ Override this method to return any merge values e.g. anything that will contain header text """
            
    def start_merge(self):
        """ Override this to do any preparation for merging, e.g. storing the merge text/field """
        pass
    
    def end_merge(self):
        """ Override this to restore the object to its state before merging began """
        pass
    
    def merge_row(self, row):
        """ Override this to merge the data row into this object """
        pass
    
    def create_property_widgets(self):
        for field in self.propOrder:
            propertyType, value, slot = self.properties[field]
            widget, signal = self.propertyTypes[propertyType]
            if propertyType == 'boolean':
                editor = widget()
                editor.setCheckState(value)
            elif propertyType == 'float' or propertyType == 'integer':
                editor = widget()
                editor.setValue(value)
                editor.setMinimum(-1000)
                editor.setMaximum(1000)
            elif propertyType == 'font':
                editor = widget()
                editor.setCurrentFont(self.fontDB.font(*value))
            else:
                editor = widget(value)
            editor.setVisible(False)
            if slot <> None:
                editor.connect(editor, signal, slot)
            self.propWidgets[field] = editor
            
    def get_pos_mm(self):
        """ returns position in millimeters """
        return self.pos().x() / self.dpmm[0], self.pos().y() / self.dpmm[1]
    
    def set_pos_by_mm(self, x, y):
        """ sets position in mm """
        self.setPos(x*self.dpmm[0], y*self.dpmm[1])
        