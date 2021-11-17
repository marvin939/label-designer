from PyQt5 import QtGui, QtCore, QtWidgets
import re
from labelitemproperty import *

class LabelerItemMixin:
    fontDB = QtGui.QFontDatabase()
#    propertyTypes = {'string':(QtGui.QLineEdit, QtCore.SIGNAL('textChanged(QString)')),
#                 'text':(QtGui.QTextEdit, QtCore.SIGNAL('textChanged()')), 
#                 'integer':(QtGui.QSpinBox, QtCore.SIGNAL('valueChanged(int)')), 
#                 'float':(QtGui.QDoubleSpinBox, QtCore.SIGNAL('valueChanged(double)')), 
#                 'list':(QtGui.QComboBox, QtCore.SIGNAL('currentIndexChanged(int)')), 
#                 'boolean':(QtGui.QCheckBox, QtCore.SIGNAL('toggled(bool)')),
#                 'font':(QtGui.QFontComboBox, QtCore.SIGNAL('currentFontChanged(QFont)'))}
    
    
    headerRE = re.compile('(\{.*?\})(\[.*?\])*')
    def __init__(self, name):
        
        self.propertyTypes = {'textarea':LabelTextAreaProperty,
                     'textline':LabelTextLineProperty,
                     'integer':LabelIntegerProperty,
                     'double':LabelDoubleProperty,
                     'list':LabelListProperty,
                     'font':LabelFontProperty,
                     'boolean':LabelBooleanProperty,
                     'list':LabelListProperty,
                     'filename':LabelFilenameProperty}
        
        self.propItems = []
        self.propCallbacks = {}
        self.properties = []
        self.propNames = {}
        self.name = name
        self.objectType = "ERROR"
        self.mergeText = ""
        #if properties == None:
        #    self.properties = {}
        #    self.propOrder = []
        #else:
        #    self.properties = properties
        #    if proporder <> None:
        #        self.propOrder = proporder 
        #    else:
        #        self.proporder = self.properties.keys()
        #        self.proporder.sort()
        
        
        #self.propWidgets = {}
        self.suppress_address_errors = False
        
        #self.create_property_widgets()
        self.merging = False
        
        
        self.dpi = QtWidgets.QCoreApplication.instance().dpi
        self.dpmm = QtWidgets.QCoreApplication.instance().dpmm
        
    def clean_up_widgets(self):
        for i in self.propItems:
            i.clean_up()
        
        
    def load_properties(self, properties):
        """ This method takes a dictionary object with  """
        #for key, value in properties.items():
        for prop in properties:
            propItem = self.propertyTypes[prop.propType](prop.propName, prop.propValue)
            propItem.connect(propItem, propItem.updateSignal, self.propCallbacks[prop.propName])
            self.properties.append(propItem)
            self.propNames[prop.propName] = propItem
            
    def void(self, *args, **kwargs):
        pass
    
    def get_merged_value(self, value, row):
        value = str(value)
        text = value.replace("{ white-space: pre-wrap; }", "")
        matches = self.headerRE.findall(text)
        matches = set(matches)
        for fieldname, substring in matches:
            field = fieldname.replace("{", "").replace("}","")
            
            replaceString = fieldname+substring
            if substring:
                vals = substring.replace("[", "").replace("]", "").split(":")
                if len(vals) == 1:
                    text = text.replace(fieldname+substring, row[field][int(vals[0])])
                else:
                    start, end = vals
                    if start.strip() == "":
                        text = text.replace(replaceString, row[field][:int(end)])
                    elif end.strip() == "":
                        text = text.replace(replaceString, row[field][int(start):])
                    else:
                        text = text.replace(replaceString, row[field][int(start):int(end)])
                        
            else:
                text = text.replace(replaceString, row[field].replace("<", "&lt;").replace(">", "&gt;").replace("{",  "&#123;").replace("}", "&#125;"))
        return text
        
    def generate_merge_text(self, row):
#         text = unicode(self.mergeText).replace("{ white-space: pre-wrap; }", "")
#         matches = self.headerRE.findall(text)
#         matches = set(matches)
#         for fieldname, substring in matches:
#             field = fieldname.replace("{", "").replace("}","")
#             
#             replaceString = fieldname+substring
#             if substring:
#                 vals = substring.replace("[", "").replace("]", "").split(":")
#                 if len(vals) == 1:
#                     text = text.replace(fieldname+substring, row[field][int(vals[0])])
#                 else:
#                     start, end = vals
#                     if start.strip() == "":
#                         text = text.replace(replaceString, row[field][:int(end)])
#                     elif end.strip() == "":
#                         text = text.replace(replaceString, row[field][int(start):])
#                     else:
#                         text = text.replace(replaceString, row[field][int(start):int(end)])
#                         
#             else:
#                 text = text.replace(replaceString, row[field])
        return self.get_merged_value(self.mergeText, row)
        
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
    
    #def create_property_widgets(self):
    #    for prop in self.propOrder:
    #        propItem = self.propertyTypes[prop](prop)
        
#        for field in self.propOrder:
#            propertyType, value, slot = self.properties[field]
#            widget, signal = self.propertyTypes[propertyType]
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
#                editor.setCurrentFont(self.fontDB.font(*value))
#            elif propertyType == 'list':
#                editor = widget()
#                editor.addItems(value)
#            else:
#                editor = widget(value)
#            editor.setVisible(False)
#            if slot <> None:
#                editor.connect(editor, signal, slot)
#            self.propWidgets[field] = editor
        
            
    def get_pos_mm(self):
        """ returns position in millimeters """
        return self.pos().x() / self.dpmm[0], self.pos().y() / self.dpmm[1]
    
    def set_pos_by_mm(self, x, y):
        """ sets position in mm """
        self.setPos(x*self.dpmm[0], y*self.dpmm[1])
        