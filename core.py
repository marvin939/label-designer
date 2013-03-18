import LabelDesigner
import sys, os, csv
import xlrd
import re
import datetime
import random
from labelertextitem import LabelerTextItem
from labelerbarcodeitem import LabelerBarcodeItem
from PyQt4 import QtCore, QtGui
from propertylistitem import PropertyListItem


from labelitemproperty import LabelProp

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
#        quitBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Quit?", "Would you like to quit?", QtGui.QMessageBox.Yes|QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel)
#        result = quitBox.exec_()
#        if result == quitBox.No or result == quitBox.Cancel:
#            event.ignore()
#        elif result == quitBox.Yes:
#            QtCore.QCoreApplication.instance().save_settings()
        pass
            
        


class Labeler(QtGui.QApplication):
    def __init__(self, *args, **kwargs):
        super(Labeler, self).__init__(*args, **kwargs)
        self.objectCollection = []
        self.objectTypes = {"Text":LabelerTextItem}
        self.ui = LabelDesigner.Ui_MainWindow()
        self.MainWindow = LabelMainWindow()
        self.merging = False
        self.currentRecordNumber = None
        self.objectGarbage = []
        
        self.itemListObjects = {}
        self.dataSet = []
        thisYear = datetime.date.today().strftime('%Y')
        thisMonth = datetime.date.today().strftime('%B %Y')
        self.currentDirectory = '\\\\pldmpp\\data\\%s\\%s' % (thisYear, thisMonth)
        self.currentFile = None
        self.headers = []
        self.previewMode = False
        self.previewRow = 0
        self.rawData = [[]]
        self.layouts = []
        self.itemNames = []
        fontTest = self.MainWindow.font()
        fontTest.setFamily("Sans")
        self.MainWindow.setFont(fontTest)
        
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
        self.fileLoaders[".xlsx"] = self.load_xls
        
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
        self.connect(self.ui.saveLayout, QtCore.SIGNAL('clicked()'), self.save_layout)
        self.connect(self.ui.loadLayout, QtCore.SIGNAL('clicked()'), self.load_layout)
        self.connect(self.ui.itemList, QtCore.SIGNAL('itemChanged(QTreeWidgetItem*, int)'), self.item_name_changed)
        self.connect(self.ui.removeLayout, QtCore.SIGNAL('clicked()'), self.remove_layout)
        
        
        # Setup a base progress window
        
        
        self.dataSetCount.setText("No data loaded.")
  
        self.ui.zoomLevel.setValue(160.0)
        self.ui.headersCheck.setChecked(True)
        
        self.logAppendCursor = self.ui.logConsole.cursorForPosition(QtCore.QPoint(0,0))
        self.logScrollBar = self.ui.logConsole.verticalScrollBar()
        #self.ui.logConsole.setLineWrapMode(self.ui.logConsole.NoWrap)
        
        
        
        self.refresh_printer_list()
       
        self.load_settings()

        self.MainWindow.show()
        
    def remove_layout(self):
        layoutItem = self.ui.layoutList.currentItem()
        if layoutItem <> None:
            ret = QtGui.QMessageBox.warning(self.MainWindow, 'Remove Layout', 
                                     'Are you sure you would like to remove the \'%s\' layout?' % str(layoutItem.text()), 
                                     QtGui.QMessageBox.Yes|QtGui.QMessageBox.No, QtGui.QMessageBox.No )
            if ret == QtGui.QMessageBox.Yes:
                print "Well done"
        else:
            self.log_message('No layout selected', 'error')
            self.beep()
        
        
    def save_layout(self):
        item = self.ui.layoutList.currentItem()
        if item:
            current = item.text()
        else:
            current = QtCore.QString()
        text = ""
        question = "Enter the name of the layout"
        while str(text).strip() == "":
            text, ok = QtGui.QInputDialog.getText(self.MainWindow, "Name of Layout", question, QtGui.QLineEdit.Normal, current)
            if ok and str(text).strip() <> "":
                # OK, Valid Name
                self.settings.beginGroup("layouts")
                self.settings.remove(text)
                self.settings.beginGroup(text)
                self.settings.setValue("permit", self.ui.permitEntry.text())
                self.settings.setValue("return", self.ui.returnAddress.toPlainText())
                self.settings.setValue("usepermit", self.ui.permitCheck.isChecked())
                self.settings.setValue("usereturn", self.ui.returnCheck.isChecked())
                
                for obj in self.objectCollection:
                    print obj.name
                    self.settings.beginGroup(obj.name)
                    
                    self.settings.setValue("type", obj.objectType)
                    #self.settings.setValue("name", obj.name)
                    for name, prop in obj.propNames.items():
                        
                        self.settings.setValue(name, prop.get_value())
                    self.settings.endGroup()
                self.settings.endGroup()    
                self.settings.endGroup()
            elif ok and str(text).strip() == "":
                #OK, Invalid name, try again
                question = "Value was blank, please enter in a non-blank name"
            else:
                # Canceled
                break
        
        
    def create_defaults(self):
        self.settings.beginGroup("Default Layout")
        #
        self.settings.setValue("permit", "478")
        self.settings.setValue("return", "If Undelivered, Return To: Private Bag 39996, Wellington Mail Centre, Lower Hutt  5045")
        self.settings.setValue("usepermit", True)
        self.settings.setValue("usereturn", True)
        #
        #
        self.settings.beginGroup("Address Block")
        ##
        self.settings.setValue("type", "Text")
        self.settings.setValue("Text", "<<Address1>>\n<<Address2>>\n<<Address3>>\n<<Address4>>\n<<Address5>>\n<<Address6>>\n<<Address7>>\n<<Address8>>")
        self.settings.setValue("X Coord", 4.5)
        self.settings.setValue("Y Coord", 15.0)
        self.settings.setValue("Font", QtGui.QFont("Arial", 9.0, QtGui.QFont.Normal, False))
        self.settings.setValue("Skip Blanks", True)
        self.settings.setValue("Line Spacing", 100.0)
        ##
        self.settings.endGroup()
        #
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
        self.ui.permitCheck.setChecked(self.settings.value('usepermit').toBool())
        self.ui.returnAddress.setText(self.settings.value('return').toString())
        self.ui.returnCheck.setChecked(self.settings.value('usereturn').toBool())
        self.ui.copyCount.setValue(self.settings.value('copies').toInt()[0])
                
        self.settings.endGroup()
        layoutGroups = []
        
        self.settings.beginGroup("layouts")
        
        for group in self.settings.childGroups():
            layoutGroups.append(group)
        if len(layoutGroups) == 0:
            self.create_defaults()
            layoutGroups.append('Default Layout')
            
        
        self.ui.layoutList.clear()
        for layout in layoutGroups:
            self.settings.beginGroup(layout)
            item = QtGui.QListWidgetItem(layout)
            item.setData(QtCore.Qt.UserRole, layout)
            self.ui.layoutList.addItem(item)
            self.settings.endGroup()
            
        self.settings.endGroup()
        
    def load_layout(self):
        item = self.ui.layoutList.currentItem()
        if item <> None:
            self.set_layout(item)
        else:
            self.log_message('No layout selected', 'error')
            self.beep()
            
            
            
    def set_layout(self, item):
        try:
            self.clear_layout()
            self.settings.beginGroup("layouts")
            self.settings.beginGroup(item.text())
            
            self.ui.permitEntry.setText(self.settings.value("permit").toString())
            self.ui.permitCheck.setChecked(self.settings.value("usepermit").toBool())
            self.ui.returnAddress.setText(self.settings.value("return").toString())
            self.ui.returnCheck.setChecked(self.settings.value("useReturn").toBool())
            for objectName in self.settings.childGroups():
                self.settings.beginGroup(objectName)
                objType = str(self.settings.value("type").toString())
                
                obj = self.objectTypes[str(objType)](objectName)
                #self.objectCollection.append(obj)
                self.add_object(obj)
                for propName in self.settings.childKeys():
                    if str(propName) == "type":
                        continue
                    obj.propNames[str(propName)].set_value(self.settings.value(propName))
                self.settings.endGroup()
            self.settings.endGroup()
            self.settings.endGroup()
        except Exception as e:
            import traceback
            print traceback.print_tb(sys.exc_info()[2])
        
    def clear_layout(self):
        print self.itemNames
        for obj in self.objectCollection[:]:
            self.remove_object(obj)
        print self.itemNames
        
            
        self.log_message("Layout Cleared")
        
        
    def remove_object(self, obj):
        """ Removes an object from the scene, and object collections """
        self.labelView.scene().removeItem(obj)
        self.objectCollection.remove(obj)
        self.ui.itemList.takeTopLevelItem(self.ui.itemList.indexOfTopLevelItem(self.itemListObjects[obj]))
        print obj.name
        self.itemNames.remove(obj.name)
        del self.itemListObjects[obj]
        #self.objectGarbage.append(obj)
        
    def log_message(self, message, level="log"):
        """ Logs a message to the console, levels include log, warning, and error """
        color = 'black'
        
        if level == "error":
            color = 'red'
        elif level == "warning":
            color = 'orange'
            
        timestamp = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S - ")
        text = timestamp + "<FONT COLOR='%s'>%s</FONT><BR />" % (color, message)
            
        self.logAppendCursor.movePosition(self.logAppendCursor.End)
        self.logAppendCursor.insertHtml(text)
        self.logScrollBar.setValue(self.logScrollBar.maximum())    
 
    def toggle_preview(self, toggle):
        if toggle:
            # If trying to enable a preview. This check also prevents an infinite loop
            if not self.field_check():
                # If not all fields were found, re-disable the preview check and exit
                self.ui.previewCheck.setChecked(False)
                return
        self.lock_editing(toggle)
        self.ui.addText.setEnabled(not toggle)
        self.ui.addBarcode.setEnabled(not toggle)
        self.ui.detailsTab.setEnabled(not toggle)
        self.labelView.scene().clearSelection()
        if toggle:
            self.start_merge(preview=True)
            self.currentRecordNumber = self.ui.previewRecord.value()
            if len(self.dataSet) > 0:
                self.merge_row(self.dataSet[self.ui.previewRecord.value()-1])
        else:
            if self.merging:
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
            if len(self.dataSet) > 0:
                self.merge_row(self.dataSet[val-1])
        
        
    def update_subset_bottom(self, val):
        if self.ui.subsetTop.value() < val:
            self.ui.subsetTop.setValue(val)
        
    
    def update_subset_top(self, val):
        if self.ui.subsetBottom.value() > val:
            self.ui.subsetBottom.setValue(val)

        
    def refresh_printer_list(self):
        """ Refreshes the list of printers, setting it to default on the first printer with "Avery" in its name, if any """
        # Clear the list and query a new one
        self.ui.printerList.clear()
        printers = QtGui.QPrinterInfo.availablePrinters()
        # Sort alphabetically, as the order seems to be reversed, at least on windows
        printers.sort(key=lambda x: str(x.printerName()))
        for i in printers:
            # add to the list
            self.ui.printerList.addItem(i.printerName())
        # Loop through, looking for an "Avery" printer first
        for i in printers:
            name = i.printerName()
            if "avery" in str(name).lower():
                self.ui.printerList.setCurrentIndex(self.ui.printerList.findText(name))
                break
        
    def set_printer(self, printerName):
        self.currentPrinter = printerName
        
    def toggle_return_address(self, toggle):
        # enable/disable the return address entry and remove it from the layup
        self.showReturn = toggle
        self.ui.returnAddress.setEnabled(toggle)
        self.labelView.toggle_return_address(toggle)
        
    def scene_selection_changed(self):
        """ Called when the a new object is selected, and brings up its properties page """
        # Get the list of selected items
        items = self.labelView.scene().selectedItems()
        if len(items) == 1:
            # If only one is selected, then sets the selection 
            self.ui.itemList.setCurrentItem(self.itemListObjects[items[0]])
        
    def toggle_permit(self, toggle):
        """ Toggles the permit on and off """
        self.showPermit = toggle
        #self.ui.permitPosition.setEnabled(toggle)
        self.ui.permitEntry.setEnabled(toggle)
        self.labelView.toggle_permit(toggle)
        
    def permit_number_changed(self, text):
        """ Called when the permit number is updated in the text field """
        self.labelView.set_permit_number(str(text))
        
    def return_address_changed(self):
        """ Called to update the return address """
        self.labelView.set_return_address(self.ui.returnAddress.toPlainText())
        
        
    def header_check(self, toggle):
        """ Called when the header checkbox is toggled to set headers on/off in the dataset """
        self.hasHeaders = toggle
        self.setup_data()
        
    
        
    def open_file(self):
        """ Shows an open file dialog, then proceeds to load the file as data """
        filename = str(QtGui.QFileDialog.getOpenFileName(self.MainWindow, "Select File", self.currentDirectory))
        if filename <> "":
            # Preserve preview state
            previewState = self.ui.previewCheck.isChecked()
            # Now disable it
            self.ui.previewCheck.setChecked(False)
            
            # Set the current file directory and filename
            self.currentDirectory = os.path.split(filename)[0]
            self.currentFile = filename
            # Set up the data
            self.load_dataset(filename)
            # Now restore the preview state
            self.ui.previewCheck.setChecked(previewState)
        
    def load_dataset(self, filename):
        """ Loads the file, datatype determined by extension """
        
        # Determine extension to open file
        ext = os.path.splitext(filename)[1].lower()
        self.rawData = []
        self.dataSet = []
        if ext in self.fileLoaders:
            self.rawData = self.fileLoaders[ext](filename)
            maxLen = 0
            for row in self.rawData:
                maxLen = max(maxLen,len(row))
            for row in self.rawData:
                if len(row) < maxLen:
                    row += [""] * (maxLen-len(row))
            self.setup_data()
        else:
            # Extension not recognised
            self.log_message('unknown format %s' % ext, "error") 
            
                    
    def setup_data(self):
        """ Takes the raw data and arranges it into a dict, based on whether or not it has headers """
        self.dataSet = []
        
        offset = 0
        if self.hasHeaders:
            # Create unique names for any conflicting headers, adds "1", "2" etc on to each repeated name
            # If the header is blank, it simply creates "Field 1" etc names, which is done a little late on
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
        
        # Clear out the current list of headers, and re-update with the new ones
        self.ui.headerList.setUpdatesEnabled(False)
        self.ui.headerList.clear()
        self.ui.headerList.setRowCount(len(self.headers))
        self.ui.headerList.setColumnCount(2)
        self.ui.headerList.setHorizontalHeaderLabels(["Header", "Record"])
        
        # This is where is will create field names for any blank fields, and for databases
        # that do not have field names
        for row in range(len(self.headers)):
            self.ui.headerList.verticalHeader().resizeSection(row, 15)
            if self.headers[row].strip() == "":
                emptyFieldCount += 1
                self.headers[row] = "Field%d" % emptyFieldCount
            headEnum.append((row,self.headers[row]))
            item = QtGui.QTableWidgetItem(self.headers[row])
            self.ui.headerList.setItem(row, 0, item)
            
        # Loop through the data, convert each row to a dict, and add it to the set
        # Uses offset to determine if it has headers or not
        for row in self.rawData[offset:]:
            newrow = {}
            for col, field in headEnum:
                newrow[field] = row[col]
            self.dataSet.append(newrow)
            
        if len(self.dataSet) == 0:
            # There is not data, except maybe headers
            # Set all row based entry fields to 0
            self.dataSetCount.setText("Dataset is empty.")
            self.ui.subsetBottom.setMinimum(0)
            self.ui.subsetBottom.setMaximum(0)
            self.ui.subsetTop.setMinimum(0)
            self.ui.subsetTop.setMaximum(0)
            self.ui.previewRecord.setMinimum(0)
            self.ui.previewRecord.setMaximum(0)
            self.ui.copyField.clear()
        else:
            # Set the hint in the status bar to reflect how many records there are
            self.dataSetCount.setText("The dataset contains %d record%s."%(len(self.dataSet),"s" if len(self.dataSet) > 1 else ""))
            # Now set the min and maxes for the subset input boxes and preview record number
            self.ui.subsetBottom.setMinimum(1)
            self.ui.subsetBottom.setMaximum(len(self.dataSet))
            self.ui.subsetTop.setMinimum(1)
            self.ui.subsetTop.setMaximum(len(self.dataSet))
            
            self.ui.previewRecord.setMinimum(1)
            self.ui.previewRecord.setMaximum(len(self.dataSet))
            
            row = 0
            self.ui.copyField.setUpdatesEnabled(False)
            self.ui.copyField.clear()
            # Populate the combo box for selecting the field which contains the amount of copies
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
            itemSelection[0].update_text()
            self.labelView.setFocus(True)
            itemSelection[0].setFocus(True)
        
    def load_csv(self, filename):
        return [row for row in csv.reader(open(filename, "rb"))]
            
        
    def load_xls(self, filename):
        """ loads both xls and xlsx, providing that xlrd 0.9+ is used """
        xlfile = xlrd.open_workbook(filename)
        sheets = xlfile.sheet_names()
        # Ask the user which sheet to use
        name, result = QtGui.QInputDialog.getItem(self.MainWindow, 
                                                  "Select which sheet you would like to use", 
                                                  "Which sheet would you like to use?", 
                                                  sheets, editable=False)
        if result == True:
            sheetname = str(name)
            sheet = xlfile.sheet_by_name(sheetname)
            data = []
            for i in range(sheet.nrows):
                row = sheet.row(i)
                newrow = []
                for cell in row:
                    if cell.ctype == 3:
                        # Type is a date, so it will read into a datetime.datetime object
                        newrow.append(xlrd.xldate_as_tuple(cell.value, xlfile.datemode))
                    elif cell.ctype == 4:
                        # cell is a boolean type
                        newrow.append("TRUE") if cell.value else newrow.append("FALSE")
                    elif cell.ctype == 2:
                        # cell is a number type
                        val = int(cell.value)
                        if val == cell.value:
                            newrow.append(str(int(cell.value)))
                        else:
                            newrow.append(str(cell.value))
                    else:
                        # cell is probably a text/string value
                        newrow.append(cell.value)
                data.append(newrow)
            return data
            
        

    def add_text(self, pos, posType="abs"):#text, x, y):
        """ add a text item at pos, returns a point to the object. Pos type can be "abs" for absolute window co-ords, or "rel" for on-paper co-ords """
        name = "Text"
        count = 0
        while name in self.itemNames:
            count += 1
            name = "Text%d" % count
        #self.itemNames.append(name)
        obj = LabelerTextItem(name)
        
       
        
        self.add_object(obj)
        
        if posType == "abs":
            obj.setPos(self.labelView.mapToScene(pos))
        elif posType == "rel":
            obj.setPos(QtCore.QPointF(pos))
        else:
            raise ValueError("Unrecognised position type %s" %posType)
        obj.setPlainText("Enter Text")
        
        
        #self.objectCollection.append(obj)
        
        #item = QtGui.QTreeWidgetItem(self.ui.itemList)
        #item.setText(0, obj.name)
        #item.setData(1,0, obj)
        #self.itemListObjects[obj] = item
        
        
        obj.start_edit()
        cursor = obj.textCursor()
        
        cursor.movePosition(QtGui.QTextCursor.Start)
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.KeepAnchor)
        
        obj.setTextCursor(cursor)
        return obj
        
    def add_barcode(self, pos):
        """ Add a barcode item """
        obj = LabelerBarcodeItem()
        
        self.add_object(obj)
        
        obj.setPos(self.labelView.mapToScene(pos))
        
        
        
    def add_object(self, obj):
        """ Adds the object to the Scene, list of objects,  """
        self.labelView.scene().addItem(obj)
        #item = PropertyListItem(self.ui.itemList)
        
        self.itemNames.append(obj.name)
        item = QtGui.QTreeWidgetItem(self.ui.itemList)
        
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        item.setText(0, obj.name)
        item.setData(0, QtCore.Qt.UserRole, obj)
        self.itemListObjects[obj] = item
        
        self.objectCollection.append(obj)
        
    def item_name_changed(self, item, col):
        
        obj = item.data(col, QtCore.Qt.UserRole).toPyObject()
        if obj <> None:
            newName = item.text(col)
            oldName =  obj.name
            if newName not in self.itemNames:
                if oldName in self.itemNames:
                    self.itemNames.remove(oldName)
                obj.name = newName
                self.itemNames.append(newName)
            elif newName <> oldName:
                self.log_message("An item already exists with the name %s" % newName, "error")
                self.beep()
                item.setText(col, oldName)
        
    
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
        """ calls the merge_row method on every object in the collection, using row as data """
        for obj in self.objectCollection:
            obj.merge_row(row)
    
        
    def item_selected(self, currentItem, previousItem):
        """ Selects the currentItem on the label view, and populates its properties """
        self.ui.objectPropertyArea.setUpdatesEnabled(False)
        if currentItem <> None:
            print self.ui.objectProperties.rowCount()
            #for i in range(self.ui.objectProperties.rowCount()):
            while True:
                # Loops through all the current properties on the property page, and hides them
                widgetItem = self.ui.objectProperties.takeAt(0)
                # This check is made due to a bug with the formlayout incorrectly 
                # keeping track of how many items it has
                if widgetItem <> None:
                    widget = widgetItem.widget()
                    widget.setVisible(False)
                    print widget
                else:
                    break
            # Get a reference to the object
            obj = currentItem.data(0,QtCore.Qt.UserRole).toPyObject()
            if self.labelView.isInteractive():
                # The label view is currently in edit mode
                if not obj.isSelected():
                    # Select the object if it isn't already
                    obj.scene().clearSelection()
                    obj.setSelected(True)
            for field in obj.properties:
                # Populate the property list for this widgets items
                for widget in field.widgetOrder:
                    self.ui.objectProperties.addRow("%s %s" % (field.name,widget), field.widgets[widget])
                    field.widgets[widget].setVisible(True)
            self.ui.objectPropertyArea.update()
            self.ui.objectPropertyArea.setUpdatesEnabled(True)
            
    def item_selection_cleared(self):
        self.ui.itemDetails.clear()
        self.ui.itemDetails.setEnabled(False)
        
        
    def zoom_spin_changed(self, zoom):
        self.labelView.zoom_to(zoom)
        
    def zoom_from_mouse(self, zoom):
        self.ui.zoomLevel.setValue(zoom)
        
    def start_progress_bar(self, minimum, maximum):
        """ Opens the progress window, setting the current number of stages the
            progress will go through, this is usually used when merging """
        self.progressWindow = QtGui.QProgressDialog(self.MainWindow)
        self.progressWindow.setWindowTitle("PDF Generation Progress...")
        self.progressWindow.setMinimumWidth(300)
        self.connect(self.progressWindow, QtCore.SIGNAL('canceled()'), self.cancel_label)
        self.progressWindow.setRange(minimum, maximum)
        newValue = 1
        progressText = "Generating Page %d of %d" % (newValue, self.progressWindow.maximum())
        self.progressWindow.setLabelText(progressText)
        self.progressWindow.show()
        
    def increment_progress_bar(self, amount=1):
        """ This should be called each time the progress increases by one stage """
        newValue = self.progressWindow.value() + amount
        progressText = "Generating Page %d of %d" % (newValue, self.progressWindow.maximum())
        self.progressWindow.setValue(newValue)
        self.progressWindow.setLabelText(progressText)
        #self.progressWindow.update()
        
    def end_progress_window(self):
        self.progressWindow.setParent(None)
        del self.progressWindow
        
    #def render_pdf(self):
    #    self.labelView.scene().render(self.scenepainter)
        
    def create_pdf(self):
        """ Generates a pdf file based on data and layup """
        self.make_labels()
        
    def print_labels(self):
        """ Calls make labels, telling it to also send to the printer, 
            this is a convenience method for a QT signal """
        self.make_labels("PRINT")
        
    def field_check(self):
        """ Will check all objects' merge fields to make sure that the fields are available. 
            returns True if all headers used were found, otherwise False, then will log an
            error message to the console """
        headersMatched = True
        # For each object
        message = ""
        for obj in self.objectCollection:
            # Unselect it
            obj.setSelected(False)
            
            # Test text for any merge fields, then test that against the header listing
            text = str(obj.get_merge_text())
            matches = self.headerRE.findall(text)
            matches = sorted(set(matches))
            for i in matches:
                x = i.replace("<<", "").replace(">>","")
                if not x in self.headers:
                    if not obj.suppress_address_errors:
                        # Was unable to find a match for this header, so issue a warning
                        message += " %s," % x
                        #self.log_message("Error, could not find header %s, please check your spelling.\n" % x, "error")
                        headersMatched = False
        if not headersMatched:
            message = self.log_message("Error, the following fields could not be found: " + message[1:-1], "error")
                
            self.beep()
             
        return headersMatched
        
    def make_labels(self, method="PDF"):
        """ Starts making labels, if method is set to "PRINT", it will also 
            print to the selected printer """
        if not self.field_check():
            # field matching failed, abort
            
            return
        
        # preserve preview state    
        previewState = self.ui.previewCheck.isChecked()
        
        # now disable it
        self.ui.previewCheck.setChecked(False)
        
        
        
        self.MainWindow.hide()
        printer = None
        if method == "PRINT":
            # If method type is set to PRINT, also set up a printer to the currently 
            # selected printer
            printer = QtGui.QPrinter()
            printer.setPrinterName(self.currentPrinter)
            printer.setOrientation(printer.Portrait)
            # Due to something to do with the Avery printer, we need to set the 
            # dimensions to be 2x their normal width and height
            printer.setPaperSize(QtCore.QSizeF(90, 180), QtGui.QPrinter.Millimeter)
            printer.setFullPage(True)
            
            painter = QtGui.QPainter()
            painter.begin(printer)

        # Set up a printer to output to PDF
        pdfPrint = QtGui.QPrinter()
        outputName = "Testing.pdf"
        
        # Set pdf name to inputname + '_labels.pdf' if currentFile is not none
        if self.currentFile <> None:
            outputName = os.path.splitext(self.currentFile)[0] +'_labels.pdf'

        pdfPrint.setOutputFileName(outputName)
        pdfPrint.setOrientation(pdfPrint.Landscape)
        
        pdfPrint.setPaperSize(QtCore.QSizeF(45, 90), QtGui.QPrinter.Millimeter)
        pdfPrint.setFullPage(True)
        pdfPainter = QtGui.QPainter()
        pdfPainter.begin(pdfPrint)
        
        self.start_merge()
        first = True
        self.labelInProgress = True
        # Start merging!
        count = 0
        for row in self.mergeDataSet:
            count += 1
            if count % 200 == 0:
                self.processEvents()
            self.merge_row(row)
            
            copies = self.ui.copyCount.value()
            if self.ui.copyUseField.isChecked():
                # use field in the database if asked to
                copies = int(row[str(self.ui.copyField.currentText())])
            # Repeat for as many copies as needed
            for i in range(copies):
                # If this is not the first time looping, make sure to call "newPage" on the printer
                # the printer variable tells us if we are printing to a "Printer" as well as a PDF
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
                # If at any point the merging is canceled, this will break the merge loop.
                break
            self.currentRecordNumber += 1
            
        # Clean up merging
        self.end_merge()
        if printer <> None:
            painter.end()
        pdfPainter.end()
        self.end_progress_window()
        self.labelView.setVisible(True)
        self.MainWindow.show()
        
        #Restore state of widget
        self.labelView.show_bg()
        self.ui.previewCheck.setChecked(previewState)

        
     
        
if __name__ == '__main__':
    MainApp = Labeler(sys.argv) 
    sys.exit(MainApp.exec_())