import LabelDesigner
import sys, os, csv
import xlrd
import re
import random
from labelertextitem import LabelerTextItem
from labelerbarcodeitem import LabelerBarcodeItem
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
DPMM = []

random.seed()

## Add ability to save settings

fontDB = QtGui.QFontDatabase()

propertyTypes = {'string':(QtGui.QLineEdit, QtCore.SIGNAL('textChanged(QString)')),
                 'text':(QtGui.QTextEdit, QtCore.SIGNAL('textChanged()')), 
                 'integer':(QtGui.QSpinBox, QtCore.SIGNAL('valueChanged(int)')), 
                 'float':(QtGui.QDoubleSpinBox, QtCore.SIGNAL('valueChanged(double)')), 
                 'list':(QtGui.QComboBox, QtCore.SIGNAL('currentIndexChanged(int)')), 
                 'boolean':(QtGui.QCheckBox, QtCore.SIGNAL('toggled(bool)')),
                 'font':(QtGui.QFontComboBox, QtCore.SIGNAL('currentFontChanged(QFont)'))}

class LabelMainWindow(QtGui.QMainWindow):
    def closeEvent(self, event):
        quitBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Quit?", "Would you like to quit?", QtGui.QMessageBox.Yes|QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel)
        result = quitBox.exec_()
        if result == quitBox.No or result == quitBox.Cancel:
            event.ignore()
        elif result == quitBox.Yes:
            QtCore.QCoreApplication.instance().save_settings()
            
        


class Labeler(QtGui.QApplication):
    def __init__(self, *args, **kwargs):
        super(Labeler, self).__init__(*args, **kwargs)
        self.objectCollection = []
        self.ui = LabelDesigner.Ui_MainWindow()
        self.MainWindow = LabelMainWindow()
        self.merging = False
        self.currentRecordNumber = None
        
        self.itemListObjects = {}
        self.dataSet = []
        self.currentDirectory = os.getcwd()
        self.currentFile = None
        self.headers = []
        self.previewMode = False
        self.previewRow = 0
        self.rawData = [[]]
        self.layouts = []
        
        ## Load in settings from conf or generate if missing
        self.defaultSettings = {'permit':478,
                                'add permit':True,
                                'return address':'If Undelivered, Return To: Private Bag 39996, Wellington Mail Centre, Lower Hutt  5045',
                                'add return':True,
                                'copies':1,
                                'subset':False,
                                'subset from':0,
                                'subset to':0,
                                'generate samples':False,
                                'zoom':160.0,
                                'has headers':True,
                                'show preview':False,
                                'layout':'default',
                                }
        
        
        
        
        
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
        
       
        self.statusBar = self.MainWindow.statusBar()
        self.dataSetCount = QtGui.QLabel(self.MainWindow)
        self.statusBar.addPermanentWidget(self.dataSetCount)
        
        self.header_check(self.ui.headersCheck.isChecked())
        
        
        # Sets up the base widget for the layup
        self.labelView = self.ui.graphicsView
        self.labelView.setPageSize((self.dpmm[0]*90, self.dpmm[1]*45))
        
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
        self.connect(self.ui.itemList, QtCore.SIGNAL('currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)'), self.item_selected)
        self.connect(self.ui.headersCheck, QtCore.SIGNAL('toggled(bool)'), self.header_check)
        self.connect(self.ui.permitCheck, QtCore.SIGNAL('toggled(bool)'), self.toggle_permit)
        self.connect(self.ui.permitEntry, QtCore.SIGNAL('textChanged(QString)'), self.permit_number_changed)
        self.connect(self.ui.returnCheck, QtCore.SIGNAL('toggled(bool)'), self.toggle_return_address)
        self.connect(self.ui.returnAddress, QtCore.SIGNAL('textChanged()'), self.return_address_changed)
        self.connect(self.ui.headerList, QtCore.SIGNAL('itemDoubleClicked(QTableWidgetItem*)'), self.add_header_text)
        self.connect(self.ui.printerList, QtCore.SIGNAL('currentIndexChanged(QString)'), self.set_printer)
        self.connect(self.ui.printButton, QtCore.SIGNAL('clicked()'), self.print_labels)        
        self.connect(self.ui.subsetBottom, QtCore.SIGNAL('valueChanged(int)'), self.update_subset_bottom)
        self.connect(self.ui.subsetTop, QtCore.SIGNAL('valueChanged(int)'), self.update_subset_top)
        self.connect(self.ui.previewRecord, QtCore.SIGNAL('valueChanged(int)'), self.update_preview_record)
        self.connect(self.ui.previewCheck, QtCore.SIGNAL('toggled(bool)'), self.toggle_preview)
        self.connect(self.ui.layoutList, QtCore.SIGNAL('itemDoubleClicked(QListWidgetItem*)'), self.set_layout)
        
        self.progressWindow = QtGui.QProgressDialog(self.MainWindow)
        self.progressWindow.setWindowTitle("PDF Generation Progress...")
        self.progressWindow.setMinimumWidth(300)
        self.connect(self.progressWindow, QtCore.SIGNAL('canceled()'), self.cancel_label)
        
        self.dataSetCount.setText("No data loaded.")
        #self.ui.permitCheck.setChecked(True)
        #self.ui.permitEntry.setText("478")
        #self.ui.returnCheck.setChecked(True)
        #self.ui.returnAddress.setText("If Undelivered, Return To: Private Bag 39996, Wellington Mail Centre, Lower Hutt  5045")
        
        
        self.ui.zoomLevel.setValue(160.0)
        self.ui.headersCheck.setChecked(True)
        
        self.logAppendCursor = self.ui.logConsole.cursorForPosition(QtCore.QPoint(0,0))
        self.logScrollBar = self.ui.logConsole.verticalScrollBar()
        self.ui.logConsole.setLineWrapMode(self.ui.logConsole.NoWrap)
        
        
        
        self.refresh_printer_list()
       
        self.load_settings()
        
        
        #self.labelView.zoom_to(200.0)

        self.MainWindow.show()
        
    def save_settings(self):
        print "saving"
        self.settings.beginGroup("mainapp")
        self.settings.setValue("zoom", int(self.ui.zoomLevel.value()))
        self.settings.endGroup()
        
        
    def create_defaults(self):
        self.settings.beginGroup("default")
        self.settings.setValue("name", "Default Layout")
        self.settings.setValue("permit", "478")
        self.settings.setValue("return", "If Undelivered, Return To: Private Bag 39996, Wellington Mail Centre, Lower Hutt  5045")
        self.settings.setValue("usepermit", True)
        self.settings.setValue("usereturn", True)
        
        self.settings.beginGroup("properties")
        
        self.beginGroup("Address Block")
        self.settings.setValue("Value", "<<Address1>>\n<<Address2>>\n<<Address3>>\n<<Address4>>\n<<Address5>>\n<<Address6>>\n<<Address7>>\n<<Address8>>")
        self.settings.setValue("X Coord", 4.5)
        self.settings.setValue("Y Coord", 15.0)
        self.settings.setValue("Font", QtGui.QFont("Arial", 9.0, QtGui.QFont.Normal, False))
        self.settings.setValue("Skip Blanks", True)
        self.settings.setValue("suppress_address_errors", "ignore")
        self.settings.endGroup()
        
        self.settings.endGroup()
        
        
        self.settings.endGroup()
        
    def load_settings(self):
        
        
        self.settings = QtCore.QSettings("labelcore.conf", QtCore.QSettings.IniFormat)
      
        self.settings.beginGroup('mainapp')
        keys = []
        for x in self.settings.allKeys():
            keys.append(str(x))
        for key, value in self.defaultSettings.items():
            if key not in keys:
                self.settings.setValue(key, value)
        self.settings.sync()
        
        
        self.ui.zoomLevel.setValue(self.settings.value('zoom').toDouble()[0])
        self.ui.permitEntry.setText(self.settings.value('permit').toString())
        self.ui.permitCheck.setChecked(self.settings.value('add permit').toBool())
        self.ui.returnAddress.setText(self.settings.value('return address').toString())
        self.ui.returnCheck.setChecked(self.settings.value('add return').toBool())
        self.ui.copyCount.setValue(self.settings.value('copies').toInt()[0])
                
        self.settings.endGroup()
        layoutGroups = []
        
        self.settings.beginGroup("layouts")
        
        for group in self.settings.childGroups():
            layoutGroups.append(group)
        if len(layoutGroups) == 0:
            self.create_defaults()
            layoutGroups.append('default')
            
        
        self.ui.layoutList.clear()
        for layout in layoutGroups:
            self.settings.beginGroup(layout)
            item = QtGui.QListWidgetItem(self.settings.value('name').toString())
            item.setData(QtCore.Qt.UserRole, layout)
            self.ui.layoutList.addItem(item)
            self.settings.endGroup()
            
        self.settings.endGroup()
            
            
    def set_layout(self, item):
        print item.text()
        self.clear_layout()
        self.settings.beginGroup(str(item.data(QtCore.Qt.UserRole).toString()))
        
        self.ui.permitEntry.setText(self.settings.value("permit").toString())
        self.ui.permitCheck.setChecked(self.settings.value("usepermit").toBool())
        self.ui.returnAddress.setText(self.settings.value("return").toString())
        self.ui.returnCheck.setChecked(self.settings.value("useReturn").toBool())
        if str(self.settings.value("block").toString()) <> "":
            x = self.dpmm[0] * self.settings.value("blockx").toFloat()[0]
            y = self.dpmm[1] * self.settings.value("blocky").toFloat()[0]
            print x, y
            obj = self.add_text(QtCore.QPoint(x,y), posType = "rel")
            
            obj.setPlainText(self.settings.value("block").toString())
            obj.suppress_address_errors = self.settings.value("suppress_address_errors").toBool()
                
            
            
        self.settings.endGroup()
        
        
    def clear_layout(self):
        for obj in self.objectCollection[:]:
            
            self.remove_object(obj)
        
        
    def remove_object(self, obj):
        """ Removes an item from the layup """
        self.labelView.scene().removeItem(obj)
        self.objectCollection.remove(obj)
        self.ui.itemList.takeTopLevelItem(self.ui.itemList.indexOfTopLevelItem(self.itemListObjects[obj]))

        del self.itemListObjects[obj]
        del obj
        
    def log_message(self, message, level="log"):
        """ Logs a message to the console, levels include log, warning, and error """
        color = 'black'
        
        if level == "error":
            color = 'red'
        elif level == "warning":
            color = 'orange'
            
        
        text = "<FONT COLOR='%s'>%s</FONT><BR />" % (color, message)
            
        self.logAppendCursor.movePosition(self.logAppendCursor.End)
        self.logAppendCursor.insertHtml(text)
        self.logScrollBar.setValue(self.logScrollBar.maximum())    
 
    def toggle_preview(self, toggle):
        self.lock_editing(toggle)
        self.ui.addText.setEnabled(not toggle)
        self.ui.addBarcode.setEnabled(not toggle)
        self.ui.detailsTab.setEnabled(not toggle)
        self.labelView.scene().clearSelection()
        if toggle:
            self.start_merge(preview=True)
            
            self.currentRecordNumber = self.ui.previewRecord.value()
            self.merge_row(self.dataSet[self.ui.previewRecord.value()-1])
        else:
            self.end_merge()
        
    def lock_editing(self, lock=True):
        self.labelView.setInteractive(not lock)
        
    def cancel_label(self):
        self.labelInProgress = False
        
    def update_preview_record(self, val):
        self.ui.headerList.setUpdatesEnabled(False)
        row = 0
        self.currentRecordNumber = val
        for i in self.headers:
            item = QtGui.QTableWidgetItem(self.dataSet[val-1][i])
            self.ui.headerList.setItem(row, 1, item)
            row += 1
        self.ui.headerList.setUpdatesEnabled(True)
            
        if self.merging:
            self.merge_row(self.dataSet[val-1])
        
        
    def update_subset_bottom(self, val):
        if self.ui.subsetTop.value() < val:
            self.ui.subsetTop.setValue(val)
        
    
    def update_subset_top(self, val):
        if self.ui.subsetBottom.value() > val:
            self.ui.subsetBottom.setValue(val)

        
    def refresh_printer_list(self):
        """ Refreshes the list of printers, setting it to default on the first printer with "Avery" in its name, if any """
        self.ui.printerList.clear()
        printers = QtGui.QPrinterInfo.availablePrinters()
        printers.sort(key=lambda x: str(x.printerName()))
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
            self.ui.itemList.setCurrentItem(self.itemListObjects[items[0]])
        
    def toggle_permit(self, toggle):
        """ Called to toggle the on/off status of the permit label """
        self.showPermit = toggle
        #self.ui.permitPosition.setEnabled(toggle)
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
        self.dataSet = []
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
            self.headers = []
            for i in self.rawData[0]:
                if i not in self.headers or i.strip() == "":
                    self.headers.append(i)
                else:
                    added = False
                    count = 1
                    while not added:
                        field = i + " (%d)" % count
                        if field not in self.headers:
                            self.headers.append(field)
                            added = True
                        count += 1
        else:
            self.headers = [""] * len(self.rawData[0])
            
        emptyFieldCount = 0
        headEnum = []
        
        self.ui.headerList.setUpdatesEnabled(False)
        self.ui.headerList.clear()
        self.ui.headerList.setRowCount(len(self.headers))
        self.ui.headerList.setColumnCount(2)
        self.ui.headerList.setHorizontalHeaderLabels(["Header", "Record"])
        
        row = 0
        
        for i in range(len(self.headers)):
            self.ui.headerList.verticalHeader().resizeSection(row, 15)
            if self.headers[i].strip() == "":
                emptyFieldCount += 1
                self.headers[i] = "Field%d" % emptyFieldCount
            headEnum.append((i,self.headers[i]))
            item = QtGui.QTableWidgetItem(self.headers[i])
            self.ui.headerList.setItem(row, 0, item)
            row += 1
            
        for row in self.rawData[offset:]:
            newrow = {}
            for col, field in headEnum:
                newrow[field] = row[col]
            self.dataSet.append(newrow)
            
        if len(self.dataSet) == 0:
            self.dataSetCount.setText("Dataset is empty.")
            self.ui.subsetBottom.setMinimum(0)
            self.ui.subsetBottom.setMaximum(0)
            self.ui.subsetTop.setMinimum(0)
            self.ui.subsetTop.setMaximum(0)
            self.ui.previewRecord.setMinimum(0)
            self.ui.previewRecord.setMaximum(0)
            self.ui.copyField.clear()
        else:
            self.dataSetCount.setText("The dataset contains %d record%s."%(len(self.dataSet),"s" if len(self.dataSet) > 1 else ""))
            self.ui.subsetBottom.setMinimum(1)
            self.ui.subsetBottom.setMaximum(len(self.dataSet))
            self.ui.subsetTop.setMinimum(1)
            self.ui.subsetTop.setMaximum(len(self.dataSet))
            
            self.ui.previewRecord.setMinimum(1)
            self.ui.previewRecord.setMaximum(len(self.dataSet))
            
            row = 0
            self.ui.copyField.setUpdatesEnabled(False)
            self.ui.copyField.clear()
            for i in self.headers:
                record = str(self.dataSet[self.ui.previewRecord.value()-1][i])
                item = QtGui.QTableWidgetItem(record)
                self.ui.headerList.setItem(row, 1, item)
                self.ui.copyField.addItem(i)
                row += 1
            self.ui.copyField.setUpdatesEnabled(True)
        
        self.ui.headerList.setUpdatesEnabled(True)
            
        
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
            
        

    def add_text(self, pos, posType="abs"):#text, x, y):
        """ add a text item at pos, returns a point to the object. Pos type can be "abs" for absolute window co-ords, or "rel" for on-paper co-ords """
        obj = LabelerTextItem()
        
        self.labelView.scene().addItem(obj)
        
        
        if posType == "abs":
            obj.setPos(self.labelView.mapToScene(pos))
        elif posType == "rel":
            obj.setPos(QtCore.QPointF(pos))
        else:
            raise ValueError("Unrecognised position type %s" %posType)
        obj.setPlainText("Enter Text")
        
        
        self.objectCollection.append(obj)
        
        item = QtGui.QTreeWidgetItem(self.ui.itemList)
        item.setText(0, "TextObj1")
        item.setData(1,0, obj)
        self.itemListObjects[obj] = item
        
        
        obj.start_edit()
        cursor = obj.textCursor()
        
        cursor.movePosition(QtGui.QTextCursor.Start)
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.KeepAnchor)
        
        obj.setTextCursor(cursor)
        return obj
        
    def add_barcode(self, pos):
        """ Add a barcode item """
        obj = LabelerBarcodeItem()
        self.labelView.scene().addItem(obj)
        
        obj.setPos(self.labelView.mapToScene(pos))
        
        item = QtGui.QTreeWidgetItem(self.ui.itemList)
        item.setText(0, "BarcodeObj1")
        item.setData(1,0, obj)
        self.itemListObjects[obj] = item
        
        
        self.objectCollection.append(obj)
        
    
    def start_merge(self, preview=False):
        self.labelView.start_merge(preview)
        self.merging = True
        for obj in self.objectCollection:
            obj.start_merge()
            
        self.mergeDataSet = self.dataSet
        self.currentRecordNumber = 1
        
        if self.ui.useSubset.checkState():
            self.currentRecordNumber = int(self.ui.subsetBottom.value())
            self.mergeDataSet = self.dataSet[int(self.ui.subsetBottom.value()) -1:int(self.ui.subsetTop.value())]
            
        if self.ui.genSamples.checkState():
            self.mergeDataSet = random.sample(self.mergeDataSet, int(self.ui.sampleCount.value()))
            
        if self.mergeDataSet == []:
            self.mergeDataSet = [[]]
        if not preview:
            self.start_progress_bar(1, len(self.mergeDataSet))
        
    def end_merge(self):
        self.merging = False
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
            if self.labelView.isInteractive():
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
        """ Starts making labels, if method is set to "PRINT", it will also print to the selected printer """
            
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
                    if not obj.suppress_address_errors:
                        errorMessage += "Error, could not find header %s, please check your spelling.\n" % i
                        headersMatched = False
        if not headersMatched:
            QtGui.QMessageBox.critical(self.MainWindow, "Error Header Not Found", errorMessage)
            return
        
        printer = None
        if method == "PRINT":
            printer = QtGui.QPrinter()
            printer.setPrinterName(self.currentPrinter)
            printer.setOrientation(printer.Portrait)
            printer.setPaperSize(QtCore.QSizeF(90, 180), QtGui.QPrinter.Millimeter)
            printer.setFullPage(True)
            
            painter = QtGui.QPainter()
            painter.begin(printer)

        pdfPrint = QtGui.QPrinter()
        pdfPrint.setOutputFileName("Testing.pdf")
        pdfPrint.setOrientation(pdfPrint.Landscape)
        pdfPrint.setPaperSize(QtCore.QSizeF(45, 90), QtGui.QPrinter.Millimeter)
        pdfPrint.setFullPage(True)
        pdfPainter = QtGui.QPainter()
        pdfPainter.begin(pdfPrint)
        
        self.start_merge()
        first = True
        self.labelInProgress = True
        for row in self.mergeDataSet:
            
            self.merge_row(row)
            
            copies = self.ui.copyCount.value()
            if self.ui.copyUseField.isChecked():
                copies = int(row[str(self.ui.copyField.currentText())])
            
            for i in range(copies):
                if first:
                    first = False
                else:
                    if printer <> None:
                        printer.newPage()
                    pdfPrint.newPage()
            
                if printer <> None:
                    self.labelView.scene().render(painter)
                
                self.labelView.scene().render(pdfPainter)
            self.increment_progress_bar()
            if not self.labelInProgress:
                break
            self.currentRecordNumber += 1
            
        self.end_merge()
        if printer <> None:
            painter.end()
        pdfPainter.end()
        
        self.labelView.show_bg()

        
MainApp = Labeler(sys.argv)      
        
if __name__ == '__main__':
    
    
    sys.exit(MainApp.exec_())