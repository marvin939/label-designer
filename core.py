import LabelDesigner
from zoomgraphicsview import ZoomGraphicsView
import sys, os, csv
import xlrd#, xlwt
import _winreg
import math
import re
from PyQt4 import QtCore, QtGui
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
DPMM = []

fontDB = QtGui.QFontDatabase()

propertyTypes = {'string':(QtGui.QLineEdit, QtCore.SIGNAL('textChanged(QString)')),
                 'text':(QtGui.QTextEdit, QtCore.SIGNAL('textChanged()')), 
                 'integer':(QtGui.QSpinBox, QtCore.SIGNAL('valueChanged(int)')), 
                 'float':(QtGui.QDoubleSpinBox, QtCore.SIGNAL('valueChanged(double)')), 
                 'list':(QtGui.QComboBox, QtCore.SIGNAL('currentIndexChanged(int)')), 
                 'boolean':(QtGui.QCheckBox, QtCore.SIGNAL('toggled(bool)')),
                 'font':(QtGui.QFontComboBox, QtCore.SIGNAL('currentFontChanged(QFont)'))}


 
class LabelerTextItem(QtGui.QGraphicsTextItem):
    def __init__(self, *args, **kwargs):
        self.editing = False
        super(LabelerTextItem, self).__init__(*args, **kwargs)
        self.setFlags(self.ItemIsSelectable|self.ItemIsMovable|self.ItemIsFocusable|self.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self.dpi = MainApp.dpi
        self.dpmm = MainApp.dpmm
        self.lineSpacing = 1.2
        self.merging = False
        self.mergeText = self.toPlainText()
        
        font = QtGui.QFont("Arial")
        font.setPointSize(9)
        self.setFont(font)
        self.properties = {'Value':('text','', self.text_changed), 
                           'Skip Blanks':('boolean', False, None),
                           'Font Size':('float', 9.0, self.set_font_size),
                           'Font':('font', (self.font().family(),self.font().styleName(), self.font().pointSizeF()), self.set_font_family),
                           'Font Bold':('boolean', self.font().bold(), self.set_font_bold),
                           'Font Italic':('boolean', self.font().italic(), self.set_font_italic),
                           'X Coord':('float', self.scenePos().x(), self.setX),
                           'Y Coord':('float', self.scenePos().y(), self.setY)}
        self.propOrder = ['Value', 'Skip Blanks', 'Font', 'Font Size', 'Font Bold', 'Font Italic', 'X Coord', 'Y Coord']
        self.propWidgets = {}
        self.skipBlanks = False
        self.create_property_widgets()
        
        self.headerRE = re.compile('<<.*?>>')
        
        self.set_pos_by_mm(5,4)
        
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
        
            
    def create_property_widgets(self):
        for field in self.propOrder:
            propertyType, value, slot = self.properties[field]
            widget, signal = propertyTypes[propertyType]
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
                editor.setCurrentFont(fontDB.font(*value))
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
        
    def get_pos_for_pdf(self):
        """ same as get pos by mm? """
        y = self.y() + self.boundingRect().height()
        return self.x()/self.dpmm[0], (self.y()/self.dpmm[1]) 
        
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
        
    def setFont(self, *args, **kwargs):
        """ Overrided to add calc for leading/line spacing """
        super(LabelerTextItem, self).setFont(*args, **kwargs)
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
    
    
class Labeler(QtGui.QApplication):
    def __init__(self, *args, **kwargs):
        super(Labeler, self).__init__(*args, **kwargs)
        self.objectCollection = []
        self.ui = LabelDesigner.Ui_MainWindow()
        self.MainWindow = QtGui.QMainWindow()
        self.itemListObjects = {}
        self.dataSet = []
        self.currentDirectory = os.getcwd()
        self.currentFile = None
        self.headers = []
        self.previewMode = False
        self.previewRow = 0
        self.rawData = [[]]
        
        # Maps file extensions to functions for decoding them
        self.fileLoaders = {}
        self.fileLoaders[".csv"] = self.load_csv
        self.fileLoaders[".xls"] = self.load_xls
        
        
        #Set DPMM(dots per mm) based on QT's DPI
        self.dpi  = (self.MainWindow.logicalDpiX(), self.MainWindow.logicalDpiY())
        self.dpmm = (self.dpi[0]/25.4, self.dpi[1]/25.4)
        DPMM.append(self.dpi[0]/25.4)
        DPMM.append(self.dpi[1]/25.4)
        
        self.ui.setupUi(self.MainWindow)
        
        
       
        
        
        self.header_check(self.ui.headersCheck.isChecked())
        
        
        # Sets up the base widget for the layup
        self.labelView = self.ui.graphicsView
        self.labelView.setPageSize((self.dpmm[0]*90, self.dpmm[1]*45))
        self.itemList = self.ui.itemList
        
        #set up list of add item buttons
        self.addItemList = []
        self.addItemList.append((self.ui.addText, self.add_text))
        self.labelView.set_add_item_list(self.addItemList)
        
        
        # make sure the correct permit state is set
        self.toggle_permit(self.ui.permitCheck.isChecked())
        self.labelView.set_permit_number(self.ui.permitEntry.text())
        
        
        # A RegEx for looking for headers in items
        self.headerRE = re.compile('<<.*?>>')
        
        
        
        self.connect(self.ui.loadData, QtCore.SIGNAL('clicked()'), self.open_file)
        #self.connect(self.ui.addTextBtn, QtCore.SIGNAL('clicked()'), self.add_text_dialog)
        self.connect(self.ui.createPdfBtn, QtCore.SIGNAL('clicked()'), self.create_pdf)
        self.connect(self.ui.zoomLevel, QtCore.SIGNAL('valueChanged(double)'), self.zoom_spin_changed)
        self.connect(self.labelView, QtCore.SIGNAL("zoomUpdated(PyQt_PyObject)"), self.zoom_from_mouse)
        self.connect(self.labelView.scene(), QtCore.SIGNAL("selectionChanged()"), self.scene_selection_changed)
        self.connect(self.itemList, QtCore.SIGNAL('currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)'), self.item_selected)
        self.connect(self.ui.headersCheck, QtCore.SIGNAL('toggled(bool)'), self.header_check)
        self.connect(self.ui.permitCheck, QtCore.SIGNAL('toggled(bool)'), self.toggle_permit)
        self.connect(self.ui.permitEntry, QtCore.SIGNAL('textChanged(QString)'), self.permit_number_changed)
        self.connect(self.ui.headerList, QtCore.SIGNAL('itemDoubleClicked(QListWidgetItem*)'), self.add_header_text)
        
        
        self.ui.zoomLevel.setValue(250.0)
        #self.labelView.zoom_to(200.0)

        self.MainWindow.show()
        
    def scene_selection_changed(self):
        """ Called when the selection of the scene has changed, to select the correct item in the object list """
        items = self.labelView.scene().selectedItems()
        if len(items) == 1:
            self.itemList.setCurrentItem(self.itemListObjects[items[0]])
        
    def toggle_permit(self, toggle):
        """ Called to toggle the on/off status of the permit label """
        self.showPermit = toggle
        self.ui.permitPosition.setEnabled(toggle)
        self.ui.permitEntry.setEnabled(toggle)
        self.labelView.toggle_permit(toggle)
        
    def permit_number_changed(self, text):
        """ Called when the permit number is updated in the text field """
        self.labelView.set_permit_number(str(text))
        
        
    def header_check(self, toggle):
        """ Called when the header checkbox is toggled to set headers on/off in the dataset """
        self.hasHeaders = toggle
        self.setup_data()
        
    def remove_object(self, obj):
        """ Removes an item from the layup """
        self.labelView.scene().removeItem(obj)
        self.objectCollection.remove(obj)
        self.itemList.takeTopLevelItem(self.itemList.indexOfTopLevelItem(self.itemListObjects[obj]))

        del self.itemListObjects[obj]
        del obj
        
    def open_file(self):
        """ Shows an open file dialog, then proceeds to load the file as data """
        filename = str(QtGui.QFileDialog.getOpenFileName(self.MainWindow, "Select File", self.currentDirectory))
        if filename <> "":
            self.currentDirectory = os.path.split(filename)[0]
            self.load_dataset(filename)
        
    def load_dataset(self, filename):
        """ Loads the file, datatype determined by extension """
        self.currentFile = filename
        ext = os.path.splitext(filename)[1].lower()
        self.rawData = []
        try:
            self.rawData = self.fileLoaders[ext](filename)
        except KeyError:
            print 'unknown format %s' % ext
        else:
            maxLen = 0
            for row in self.rawData:
                maxLen = max(maxLen,len(row))
            for row in self.rawData:
                if len(row) < maxLen:
                    row += [""] * (maxLen-len(row))
            self.setup_data()
                    
    def setup_data(self):
        """ Takes the raw data and arranges it into a dict, based on whether or not it has headers """
        self.dataSet = []
        offset = 0
        if self.hasHeaders:
            offset = 1
            self.headers = self.rawData[0]
        else:
            self.headers = [""] * len(self.rawData[0])
            
        emptyFieldCount = 0
        headEnum = []
        self.ui.headerList.clear()
        for i in range(len(self.headers)):
            if self.headers[i].strip() == "":
                emptyFieldCount += 1
                self.headers[i] = "Field%d" % emptyFieldCount
            headEnum.append((i,self.headers[i]))
            self.ui.headerList.addItem(self.headers[i])
        for row in self.rawData[offset:]:
            newrow = {}
            for col, field in headEnum:
                newrow[field] = row[col]
            self.dataSet.append(newrow)
            
        
    def add_header_text(self, item):
        itemSelection = self.labelView.scene().selectedItems()
        if len(itemSelection) == 1:
            itemSelection[0].textCursor().insertText("<<%s>>" % str(item.text()))
            self.labelView.setFocus(True)
            itemSelection[0].setFocus(True)
        
    def load_csv(self, filename):
        return [row for row in csv.reader(open(filename, "rb"))]
            
        
    def load_xls(self, filename):
        """ loads XLS only, not xlsx, uses xlrd TODO use win32com for xlsx and others """
        xlfile = xlrd.open_workbook(filename)
        sheets = xlfile.sheet_names()
        name, result = QtGui.QInputDialog.getItem(self.MainWindow, "Select which sheet you would like to use", "Which sheet would you like to use?", sheets, editable=False)
        if result == True:
            sheetname = str(name)
            sheet = xlfile.sheet_by_name(sheetname)
            data = []
            for i in range(sheet.nrows):
                row = sheet.row(i)
                newrow = []
                for cell in row:
                    if cell.ctype == 3:
                        newrow.append(xlrd.xldate_as_tuple(cell.value, xlfile.datemode))
                    elif cell.ctype == 2:
                        newrow.append("TRUE") if cell.value else newrow.append("FALSE")
                    else:
                        newrow.append(cell.value)
                data.append(newrow)
            return data
            
        

    def add_text(self, pos):#text, x, y):
        """ add a text item at x, y """
        obj = LabelerTextItem()
        
        self.labelView.scene().addItem(obj)
        
        
        
        obj.setPos(self.labelView.mapToScene(pos))
        obj.setPlainText("Enter Text")
        
        
        self.objectCollection.append(obj)
        
        item = QtGui.QTreeWidgetItem(self.itemList)
        item.setText(0, "TextObj1")
        item.setData(1,0, obj)
        self.itemListObjects[obj] = item
        
        
        obj.start_edit()
        cursor = obj.textCursor()
        
        cursor.movePosition(QtGui.QTextCursor.Start)
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.KeepAnchor)
        obj.setTextCursor(cursor)
    
    def start_merge(self):
        self.labelView.start_merge()
        for obj in self.objectCollection:
            obj.start_merge()
        
    def end_merge(self):
        self.labelView.end_merge()
        for obj in self.objectCollection:
            obj.end_merge()
        
    def merge_row(self, row):
        for obj in self.objectCollection:
            obj.merge_row(row)
    
        
    def item_selected(self, currentItem, previousItem):
        """ sets selection in the graphicsview/scene when chosen from treeview """
        if currentItem <> None:
            for i in range(self.ui.objectProperties.rowCount()):
                widgetItem = self.ui.objectProperties.takeAt(0)
                if widgetItem <> None:
                    widget = widgetItem.widget()
                    widget.setVisible(False)
                else:
                    break
            obj = currentItem.data(1,0).toPyObject()
            if not obj.isSelected():
                obj.scene().clearSelection()
                obj.setSelected(True)
            for field in obj.propOrder:
                widget = obj.propWidgets[field]
                self.ui.objectProperties.addRow(field, widget)
                widget.setVisible(True)
            
    def item_selection_cleared(self):
        self.ui.itemDetails.clear()
        self.ui.itemDetails.setEnabled(False)
        
        
    def zoom_spin_changed(self, zoom):
        self.labelView.zoom_to(zoom)
        
    def zoom_from_mouse(self, zoom):
        self.ui.zoomLevel.setValue(zoom)
        
            
    def retrieve_font_filename(self, font):
        """ Returns a font's system filename, for use with reportlab to embed/link in fonts """
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts', 0, _winreg.KEY_READ)
        fontname = _winreg.QueryValueEx(key,  str(font) + " (TrueType)")
        return fontname
            
    def create_pdf(self):
        """ Generates a pdf file based on data and layup """
            
        ## test text objects for header names as well as unselect everything
        headersMatched = True
        errorMessage = ""
        for obj in self.objectCollection:
            # if obj is type text
            obj.setSelected(False)
            text = str(obj.toPlainText())
            matches = self.headerRE.findall(text)
            matches = set(matches)
            for i in matches:
                x = i.replace("<<", "").replace(">>","")
                if not x in self.headers:
                    errorMessage += "Error, could not find header %s, please check your spelling.\n" % i
                    headersMatched = False
        if not headersMatched:
            QtGui.QMessageBox.critical(self.MainWindow, "Error Header Not Found", errorMessage)
            return
        
        self.labelView.hide_bg()
        pp = QtGui.QPrinter()
        pp.setPaperSize(QtCore.QSizeF(45, 90), QtGui.QPrinter.Millimeter)
        pp.setOutputFileName("Testing.pdf")
        pp.setOrientation(QtGui.QPrinter.Landscape)
        pp.setFullPage(True)
        
        painter = QtGui.QPainter()
        painter.begin(pp)
        self.start_merge()
        first = True
        for row in self.dataSet:
            if first:
                first = False
            else:
                pp.newPage()
            self.merge_row(row)
            self.labelView.scene().render(painter)
        self.end_merge()
        painter.end()
        
        self.labelView.show_bg()

        
MainApp = Labeler(sys.argv)      
        
if __name__ == '__main__':
    
    
    sys.exit(MainApp.exec_())