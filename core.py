import LabelDesigner
from zoomgraphicsview import ZoomGraphicsView
import sys, os, csv
import xlrd, xlwt
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


 
class LabelerTextItem(QtGui.QGraphicsTextItem):
    def __init__(self, *args, **kwargs):
        
        super(LabelerTextItem, self).__init__(*args, **kwargs)
        self.setFlags(self.ItemIsSelectable|self.ItemIsMovable|self.ItemIsFocusable)
        self.dpi = MainApp.dpi
        self.dpmm = MainApp.dpmm
        self.set_pos_by_mm(5,4)
        self.lineSpacing = 1.2
        
        font = QtGui.QFont("Arial")
        font.setPointSize(9)
        self.setFont(font)
        
        
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
        
    def mouseDoubleClickEvent(self, event):
        """ Overrided to make text editable after being double clicked TODO make sure cursor is showing """
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.setFocus(True)
        
    def setFont(self, *args, **kwargs):
        """ Overrided to add calc for leading/line spacing """
        super(LabelerTextItem, self).setFont(*args, **kwargs)
        self.leading = self.font().pointSize()*self.lineSpacing
        
        
    def itemChange(self, change, value):
        """ Overrided to stop editing after losing selection: TODO clear selection """
        super(LabelerTextItem,self).itemChange(change, value)
        if change == QtGui.QGraphicsItem.ItemSelectedChange:
            if value == False:
                self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
                self.textCursor().clearSelection()
                self.clearFocus()
        return value
    
    
class Labeler(QtGui.QApplication):
    def __init__(self, *args, **kwargs):
        super(Labeler, self).__init__(*args, **kwargs)
        self.objectCollection = []
        self.ui = LabelDesigner.Ui_MainWindow()
        self.MainWindow = QtGui.QMainWindow()
        self.itemListObjects = {}
        self.dataSet = []
        self.currentDirectory = "C:\\"
        self.currentFile = None
        
        #set up funcs to load in different file formats
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
        
        
        self.labelView = self.ui.graphicsView
        self.labelView.setPageSize((self.dpmm[0]*90, self.dpmm[1]*45))
        self.itemList = self.ui.itemList
        
        
        
        # make sure the correct permit state is set
        self.toggle_permit(self.ui.permitCheck.isChecked())
        self.labelView.set_permit_number(self.ui.permitEntry.text())
        
        self.headerRE = re.compile('<<.*?>>')
        
        
        
        self.connect(self.ui.loadData, QtCore.SIGNAL('clicked()'), self.open_file)
        self.connect(self.ui.addTextBtn, QtCore.SIGNAL('clicked()'), self.add_text_dialog)
        self.connect(self.ui.createPdfBtn, QtCore.SIGNAL('clicked()'), self.create_pdf)
        self.connect(self.ui.zoomLevel, QtCore.SIGNAL('valueChanged(double)'), self.zoom_spin_changed)
        self.connect(self.labelView, QtCore.SIGNAL("zoomUpdated(PyQt_PyObject)"), self.zoom_from_mouse)
        self.connect(self.itemList, QtCore.SIGNAL('currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)'), self.item_selected)
        self.connect(self.ui.headersCheck, QtCore.SIGNAL('toggled(bool)'), self.header_check)
        self.connect(self.ui.permitCheck, QtCore.SIGNAL('toggled(bool)'), self.toggle_permit)
        self.connect(self.ui.permitEntry, QtCore.SIGNAL('textChanged(QString)'), self.permit_number_changed)
        
        #make sure scale factor and header state are correct
        #self.scaleFactor = self.ui.zoomLevel.value()
        #self.zoom_changed()
        self.ui.zoomLevel.setValue(250.0)
        #self.labelView.zoom_to(200.0)

        self.MainWindow.show()
        
    def toggle_permit(self, toggle):
        self.showPermit = toggle
        self.ui.permitPosition.setEnabled(toggle)
        self.ui.permitEntry.setEnabled(toggle)
        self.labelView.toggle_permit(toggle)
        
    def permit_number_changed(self, text):
        self.labelView.set_permit_number(str(text))
        
        
    def header_check(self, toggle):
        self.hasHeaders = toggle
        
    def remove_object(self, obj):
        self.labelView.scene().removeItem(obj)
        self.objectCollection.remove(obj)
        #self.itemList.removeItemWidget(self.itemListObjects[obj], 1)
        self.itemList.takeTopLevelItem(self.itemList.indexOfTopLevelItem(self.itemListObjects[obj]))

        del self.itemListObjects[obj]
        del obj
        
    def open_file(self):
        filename = str(QtGui.QFileDialog.getOpenFileName(self.MainWindow, "Select File", self.currentDirectory))
        if filename <> "":
            self.currentDirectory = os.path.split(filename)[0]
            print filename
            self.load_dataset(filename)
        
    def load_dataset(self, filename):
        self.currentFile = filename
        ext = os.path.splitext(filename)[1].lower()
        try:
            self.dataSet = self.fileLoaders[ext](filename)
        except KeyError:
            print 'unknown format %s' % ext
        
        
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
            
        

    def add_text(self, text, x, y):
        """ add a text item at x, y """
        obj = LabelerTextItem()
        
        self.labelView.scene().addItem(obj)
        
        
        
        obj.setPlainText(text)
        self.objectCollection.append(obj)
        
        item = QtGui.QTreeWidgetItem(self.itemList)
        item.setText(0, "TextObj1")
        item.setData(1,0, obj)
        self.itemListObjects[obj] = item
        
    def item_selected(self, currentItem, previousItem):
        """ sets selection in the graphicsview/scene when chosen from treeview """
        if currentItem <> None:
            obj = currentItem.data(1,0).toPyObject()
            obj.scene().clearSelection()
            obj.setSelected(True)
        
        
    def zoom_spin_changed(self, zoom):
        """ TODO Needs fixing, to account for scroll zooming """
        #scale = ((100.0/self.scaleFactor) * self.ui.zoomLevel.value()) / 100
        #self.scaleFactor = self.ui.zoomLevel.value()
        self.labelView.zoom_to(zoom)
        #self.ui.imagePreview.scale(scale, scale)
        
    def zoom_from_mouse(self, zoom):
        print zoom
        self.ui.zoomLevel.setValue(zoom)
        
        
        
    def add_text_dialog(self):
        """ Gets input from the user to add a text item """
        result = QtGui.QInputDialog.getText(self.MainWindow, 'What text to add?', "Enter text")
        if result[1] == True:
            text = result[0]
            self.add_text(text, 0, 0)
            
    def retrieve_font_filename(self, font):
        """ Returns a font's system filename, for use with reportlab to embed/link in fonts """
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows NT\\CurrentVersion\\Fonts', 0, _winreg.KEY_READ)
        fontname = _winreg.QueryValueEx(key,  str(font) + " (TrueType)")
        return fontname
            
    def create_pdf(self):
        """ Generates a pdf file based on data and layup """
        if self.hasHeaders:
            headers = [i.lower() for i in self.dataSet[0]]
        else:
            headers = None
            
        ## test text objects for header names
        headersMatched = True
        for obj in self.objectCollection:
            # if obj is type text
            text = str(obj.toPlainText())
            matches = self.headerRE.findall(text)
            matches = set(matches)
            for i in matches:
                x = i.replace("<<", "").replace(">>","").lower()
                if headers == None:
                    if x.strip("0123456789") <> "field":
                        print "error, missing heading %s, check spelling" % i
                        headersMatched = False
                elif not x in headers:
                    print "error, missing heading %s, check spelling" % i
                    headersMatched = False
        if not headersMatched:
            return
            
        pdf = canvas.Canvas("hello.pdf", (mm*90, mm*45))
        
        if headers:
            rowrange = self.dataSet[1:]
        else:
            rowrange = self.dataSet
        for row in rowrange:
            if self.ui.permitCheck.isChecked():
                #displays permit impression TODO add centering, base on page size
                try:
                    pdf.setFont('Arial Narrow', 8, 10)
                except KeyError:
                    # font not loaded, request it
                    fontname = self.retrieve_font_filename("Arial Narrow")
                    pdfmetrics.registerFont(TTFont("Arial Narrow",fontname[0]))
                    pdf.setFont('Arial Narrow', 8, 10)
                
                pdf.drawImage("PermitPost.png", mm*46, mm*34, mm*43, mm*10)
                permitTextObj = pdf.beginText(46.6*mm, ((45-.9)*mm-13))
                permitTextObj.textLines(self.labelView.permitPlainText)
                pdf.drawText(permitTextObj)
            for obj in self.objectCollection:
                
                
                font = obj.font()
                x, y = obj.get_pos_for_pdf()
                
                
                textobj = pdf.beginText(x*mm, ((45-y)*mm) - obj.leading)
                
                
                try:
                    pdf.setFont(str(font.family()), font.pointSize(), obj.leading)
                except KeyError:
                    # font not loaded, request it
                    fontname = self.retrieve_font_filename(font.family())
                    pdfmetrics.registerFont(TTFont(str(font.family()),fontname[0]))
                    pdf.setFont(str(font.family()), font.pointSize(), obj.leading)
               
                
                text = str(obj.toPlainText())
                matches = self.headerRE.findall(text)
                matches = set(matches)
                for i in matches:
                    x = i.replace("<<", "").replace(">>","").lower()
                    index = headers.index(x)
                    text = text.replace(i, row[index])
                
                
            
                textobj.textLines(text)
            
            
                pdf.drawText(textobj)
            pdf.showPage()
        pdf.save()
            
        
MainApp = Labeler(sys.argv)      
        
if __name__ == '__main__':
    
    
    sys.exit(MainApp.exec_())