import LabelDesigner
import sys, os, csv
import xlrd
import re
from labelertextitem import LabelerTextItem
from labelerbarcodeitem import LabelerBarcodeItem
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
DPMM = []


## TODO next, print directly to label printer

fontDB = QtGui.QFontDatabase()

propertyTypes = {'string':(QtGui.QLineEdit, QtCore.SIGNAL('textChanged(QString)')),
                 'text':(QtGui.QTextEdit, QtCore.SIGNAL('textChanged()')), 
                 'integer':(QtGui.QSpinBox, QtCore.SIGNAL('valueChanged(int)')), 
                 'float':(QtGui.QDoubleSpinBox, QtCore.SIGNAL('valueChanged(double)')), 
                 'list':(QtGui.QComboBox, QtCore.SIGNAL('currentIndexChanged(int)')), 
                 'boolean':(QtGui.QCheckBox, QtCore.SIGNAL('toggled(bool)')),
                 'font':(QtGui.QFontComboBox, QtCore.SIGNAL('currentFontChanged(QFont)'))}


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
        self.addItemList.append((self.ui.addBarcode, self.add_barcode))
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
        self.connect(self.ui.returnCheck, QtCore.SIGNAL('toggled(bool)'), self.toggle_return_address)
        self.connect(self.ui.returnAddress, QtCore.SIGNAL('textChanged()'), self.return_address_changed)
        self.connect(self.ui.headerList, QtCore.SIGNAL('itemDoubleClicked(QListWidgetItem*)'), self.add_header_text)
        self.connect(self.ui.printerList, QtCore.SIGNAL('currentIndexChanged(QString)'), self.set_printer)
        self.connect(self.ui.printButton, QtCore.SIGNAL('clicked()'), self.print_labels)        
        
        self.progressWindow = QtGui.QProgressDialog(self.MainWindow)
        self.progressWindow.setWindowTitle("PDF Generation Progress...")
        self.progressWindow.setMinimumWidth(300)
        
        self.ui.dataInfo.setText("No data loaded.")
        self.ui.permitCheck.setChecked(True)
        self.ui.permitEntry.setText("478")
        self.ui.returnCheck.setChecked(True)
        self.ui.returnAddress.setText("If Undelivered, Return To: Private Bag 39996, Wellington Mail Centre, Lower Hutt  5045")
        
        
        self.ui.zoomLevel.setValue(125.0)
        
        self.refresh_printer_list()
        
        
        
        #self.labelView.zoom_to(200.0)

        self.MainWindow.show()
        
        
    def refresh_printer_list(self):
        self.ui.printerList.clear()
        printers = QtGui.QPrinterInfo.availablePrinters()
        printers.reverse()
        for i in printers:
            self.ui.printerList.addItem(i.printerName())
        for i in printers:
            name = i.printerName()
            if "avery" in str(name).lower():
                self.ui.printerList.setCurrentIndex(self.ui.printerList.findText(name))
                break
        
    def set_printer(self, printerName):
        self.currentPrinter = printerName
        
    def toggle_return_address(self, toggle):
        self.showReturn = toggle
        self.ui.returnAddress.setEnabled(toggle)
        self.labelView.toggle_return_address(toggle)
        
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
        
    def return_address_changed(self):
        self.labelView.set_return_address(self.ui.returnAddress.toPlainText())
        
        
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
            
        if len(self.dataSet) == 0:
            self.ui.dataInfo.setText("Dataset is empty.")
        else:
            self.ui.dataInfo.setText("The dataset contains %d row%s."%(len(self.dataSet),"s" if len(self.dataSet) > 1 else ""))
            
        
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
                    elif cell.ctype == 4:
                        newrow.append("TRUE") if cell.value else newrow.append("FALSE")
                    elif cell.ctype == 2:
                        val = int(cell.value)
                        if val == cell.value:
                            newrow.append(str(int(cell.value)))
                        else:
                            newrow.append(str(cell.value))
                    else:
                        newrow.append(cell.value)
                data.append(newrow)
            return data
            
        

    def add_text(self, pos):#text, x, y):
        """ add a text item at pos """
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
        
    def add_barcode(self, pos):
        """ Add a barcode item """
        obj = LabelerBarcodeItem()
        self.labelView.scene().addItem(obj)
        
        obj.setPos(self.labelView.mapToScene(pos))
        
        item = QtGui.QTreeWidgetItem(self.itemList)
        item.setText(0, "BarcodeObj1")
        item.setData(1,0, obj)
        self.itemListObjects[obj] = item
        
        
        self.objectCollection.append(obj)
        
    
    def start_merge(self):
        self.labelView.start_merge()
        for obj in self.objectCollection:
            obj.start_merge()
            
        self.mergeDataSet = self.dataSet
        
        if self.ui.useSubset.checkState():
            self.mergeDataSet = self.dataSet[int(self.ui.subsetBottom.value()) -1:int(self.ui.subsetTop.value())]
        self.start_progress_bar(1, len(self.mergeDataSet))
        
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
        
    def start_progress_bar(self, minimum, maximum):
        self.progressWindow.setRange(minimum, maximum)
        newValue = 1
        progressText = "Generating Page %d of %d" % (newValue, self.progressWindow.maximum())
        self.progressWindow.setLabelText(progressText)
        self.progressWindow.show()
        
    def increment_progress_bar(self):
        newValue = self.progressWindow.value() + 1
        progressText = "Generating Page %d of %d" % (newValue, self.progressWindow.maximum())
        self.progressWindow.setValue(newValue)
        self.progressWindow.setLabelText(progressText)
        self.progressWindow.update()
        
    def render_pdf(self):
        self.labelView.scene().render(self.scenepainter)
        
    def create_pdf(self):
        """ Generates a pdf file based on data and layup """
        self.make_labels()
        
    def print_labels(self):
        self.make_labels("PRINT")
        
        
    def make_labels(self, method="PDF"):
            
        ## test text objects for header names as well as unselect everything
        headersMatched = True
        errorMessage = ""
        for obj in self.objectCollection:
            # if obj is type text
            obj.setSelected(False)
            text = str(obj.get_merge_text())
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
        
        #self.start_merge()
        #self.labelView.hide_bg()
        pp = QtGui.QPrinter()
        
        
        if method == "PDF":
            pp.setOutputFileName("Testing.pdf")
            pp.setOrientation(pp.Landscape)
            pp.setPaperSize(QtCore.QSizeF(45, 90), QtGui.QPrinter.Millimeter)
        else:
            pp.setPrinterName(self.currentPrinter)
            pp.setOrientation(pp.Portrait)
            pp.setPaperSize(QtCore.QSizeF(90, 180), QtGui.QPrinter.Millimeter)
        #pp.setOrientation(QtGui.QPrinter.Landscape)
        pp.setFullPage(True)
        
        painter = QtGui.QPainter()
        painter.begin(pp)
        
        self.start_merge()
        first = True
        
        for row in self.mergeDataSet:
            if first:
                first = False
            else:
                pp.newPage()
            self.merge_row(row)
            self.labelView.scene().render(painter)
            self.increment_progress_bar()
        self.end_merge()
        painter.end()
        
        self.labelView.show_bg()

        
MainApp = Labeler(sys.argv)      
        
if __name__ == '__main__':
    
    
    sys.exit(MainApp.exec_())