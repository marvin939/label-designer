#!python2.6
import sys
import os
import csv


import constants

# SERVER_LOCATION = os.environ["dataserv"]
# Marvin 21/11/2021 - Not used it seems.


import LabelDesigner
import PageSetup
import CartonLabel
import RollLabelDialog
import xlrd
import re
import datetime
import random
import shutil
import math
import codecs


layoutNameRegex = re.compile("(.+?)[+.?]$")

# TODO
# Filename in status bar
# Search function ala Excel's search
# Database of rappers - use last.fm


import zipfile

from labelertextitem import LabelerTextItem
from labelerbarcodeitem import LabelerBarcodeItem
from labelerimageitem import LabelerImageItem
#from PyQt4 import QtCore, QtGui
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport

#from propertylistitem import PropertyListItem

import tables

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, asc, desc

from labelitemproperty import LabelProp

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s): return s


DPMM = []

random.seed()

# Add ability to save settings

#fontDB = QtGui.QFontDatabase()
fontDB = None
# Instantiation moved to Labeler class constructor. This variable doesn't look like it's being used.

# propertyTypes = {'string': (QtGui.QLineEdit, QtCore.SIGNAL('textChanged(QString)')),
#                  'text': (QtGui.QTextEdit, QtCore.SIGNAL('textChanged()')),
#                  'integer': (QtGui.QSpinBox, QtCore.SIGNAL('valueChanged(int)')),
#                  'float': (QtGui.QDoubleSpinBox, QtCore.SIGNAL('valueChanged(double)')),
#                  'list': (QtGui.QComboBox, QtCore.SIGNAL('currentIndexChanged(int)')),
#                  'boolean': (QtGui.QCheckBox, QtCore.SIGNAL('toggled(bool)')),
#                  'font': (QtGui.QFontComboBox, QtCore.SIGNAL('currentFontChanged(QFont)'))}

# propertyTypes = {'string': (QtWidgets.QLineEdit, QtCore.SIGNAL('textChanged(QString)')),
#                  'text': (QtWidgets.QTextEdit, QtCore.SIGNAL('textChanged()')),
#                  'integer': (QtWidgets.QSpinBox, QtCore.SIGNAL('valueChanged(int)')),
#                  'float': (QtWidgets.QDoubleSpinBox, QtCore.SIGNAL('valueChanged(double)')),
#                  'list': (QtWidgets.QComboBox, QtCore.SIGNAL('currentIndexChanged(int)')),
#                  'boolean': (QtWidgets.QCheckBox, QtCore.SIGNAL('toggled(bool)')),
#                  'font': (QtWidgets.QFontComboBox, QtCore.SIGNAL('currentFontChanged(QFont)'))}
# ^^ Not used?


class LayoutDelegate(QtWidgets.QAbstractItemDelegate):
    def __init__(self, *args, **kwargs):
        super(QtWidgets.QAbstractItemDelegate, self).__init__(*args, **kwargs)

    def paint(self, painter, option, index):
        rect = option.rect
        pen = QtGui.QPen(self.parent().ui.layoutList.palette().color(
            QtGui.QPalette.Text), 1, QtCore.Qt.SolidLine)
        if option.state & QtWidgets.QStyle.State_MouseOver:

            painter.fillRect(rect, self.parent().ui.layoutList.palette().color(
                QtGui.QPalette.Highlight).lighter())
        elif option.state & QtWidgets.QStyle.State_Selected:

            painter.fillRect(rect, self.parent().ui.layoutList.palette().color(
                QtGui.QPalette.Highlight).lighter())
        else:

            painter.fillRect(
                rect, self.parent().ui.layoutList.palette().color(QtGui.QPalette.Base))
        painter.setPen(pen)
        name = index.data(QtCore.Qt.UserRole) #.toString()
        date = index.data(QtCore.Qt.DisplayRole) #.toString()

        r = rect.adjusted(5, 0, -80, 0)
        painter.setFont(QtGui.QFont("Arial", 9, QtGui.QFont.Normal))
        painter.drawText(r.left(), r.top(), r.width(), r.height(
        ), QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft, name)

        pen2 = QtGui.QPen(QtCore.Qt.gray, 1, QtCore.Qt.SolidLine)
        painter.setPen(pen2)
        f = QtGui.QFont("Arial", 9, QtGui.QFont.Normal)
        f.setItalic(True)
        rect = rect.adjusted(0, 0, -5, 0)
        painter.setFont(f)
        painter.drawText(rect.left(), rect.top(), rect.width(), rect.height(
        ), QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight, date)

    def sizeHint(self, option, index):
        return QtCore.QSize(100, 18)


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """

    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def __next__(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def __next__(self):
        row = next(self.reader)
        return [str(s, "utf-8") for s in row]

    def __iter__(self):
        return self


class LabelMainWindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        #        quitBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Quit?", "Would you like to quit?", QtGui.QMessageBox.Yes|QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel)
        #        result = quitBox.exec_()
        #        if result == quitBox.No or result == quitBox.Cancel:
        #            event.ignore()
        #        elif result == quitBox.Yes:
        #            QtCore.QCoreApplication.instance().save_settings()
        pass


class LabelLayout(object):
    def __init__(self, name, permit, returnAddress, permitEnabled, returnEnabled, pageWidth, pageHeight, objectList, recyclablePackagingEnabled=True):
        self.name = name
        self.permit = permit
        self.returnAddress = returnAddress
        self.permitEnabled = permitEnabled
        self.returnEnabled = returnEnabled
        self.pageWidth = pageWidth
        self.pageHeight = pageHeight
        self.objectList = objectList
        self.recyclablePackagingEnabled = recyclablePackagingEnabled


class Labeler(QtWidgets.QApplication):
    def __init__(self, *args, **kwargs):
        #self.dpi  = (self.MainWindow.logicalDpiX(), self.MainWindow.logicalDpiY())
        self.dpi = (96, 96)
        self.dpmm = (self.dpi[0]/25.4, self.dpi[1]/25.4)
        DPMM.append(self.dpi[0]/25.4)
        DPMM.append(self.dpi[1]/25.4)
        
        super(Labeler, self).__init__(*args, **kwargs)
        self.objectCollection = []
        self.objectTypes = {"Text": LabelerTextItem,
                            "Barcode": LabelerBarcodeItem, "Image": LabelerImageItem}
        
        # Set DPMM(dots per mm) based on QT's DPI
        
        
        self.ui = LabelDesigner.Ui_MainWindow()
        self.MainWindow = LabelMainWindow()
        self.merging = False
        self.currentRecordNumber = None
        self.objectGarbage = []
        
        global fontDB
        fontDB = QtGui.QFontDatabase()

        self.sortByDate = False

        self.itemListObjects = {}
        self.dataSet = []
        thisYear = datetime.date.today().strftime('%Y')
        thisMonth = datetime.date.today().strftime('%B %Y')

        self.headers = []
        self.previewMode = False
        self.previewRow = 0
        self.rawData = [[]]
        self.layouts = []
        self.itemNames = []
        fontTest = self.MainWindow.font()
        fontTest.setFamily("Sans")
        self.MainWindow.setFont(fontTest)

        # Set up the database connection
        #self.dbEngine = create_engine("postgresql://labeldesigner:labelmaker666@pldatafile01:5432/labelmaker")
        self.dbEngine = create_engine(
            "postgresql://labeldesigner:labelmaker666@pldatafile01:5432/labelmakertest2")
        tables.Base.metadata.create_all(self.dbEngine)
        self.sessionMaker = sessionmaker(self.dbEngine)

        # Load in settings from conf or generate if missing
        self.defaultSettings = {'permit': 478,
                                'add permit': True,
                                'return address': 'If Undelivered, Return To: Private Bag 39996, Wellington Mail Centre, Lower Hutt  5045',
                                'add return': True,
                                'copies': 1,
                                'subset': False,
                                'subset from': 0,
                                'subset to': 0,
                                'generate samples': False,
                                'zoom': 160.0,
                                'has headers': True,
                                'show preview': False,
                                'layout': 'default',
                                }

        # Maps file extensions to functions for decoding them
        self.fileLoaders = {}
        self.fileLoaders[".csv"] = self.load_csv
        self.fileLoaders[".xls"] = self.load_xls
        self.fileLoaders[".xlsx"] = self.load_xls

        

        self.ui.setupUi(self.MainWindow)
        print((self.dpi, self.dpmm))

        self.statusBar = self.MainWindow.statusBar()
        self.dataSetCount = QtWidgets.QLabel(self.MainWindow)
        self.statusBar.addPermanentWidget(self.dataSetCount)

        self.filenameStatus = QtWidgets.QLabel('')
        self.filenameStatus.setAlignment(QtCore.Qt.AlignLeft)
        self.statusBar.addWidget(self.filenameStatus, 1)

        self.header_check(self.ui.headersCheck.isChecked())

        # Sets up the base widget for the layup
        self.currentPageSize = (90, 45)
        self.labelView = self.ui.graphicsView
        self.labelView.setPageSize(
            (self.dpmm[0]*self.currentPageSize[0], self.dpmm[1]*self.currentPageSize[1]))

        # set up list of add item buttons
        self.addItemList = []
        self.addItemList.append((self.ui.addText, self.add_text))
        self.addItemList.append((self.ui.addBarcode, self.add_barcode))
        self.addItemList.append((self.ui.addImage, self.add_image))
        self.labelView.set_add_item_list(self.addItemList)

        # make sure the correct permit state is set
        self.toggle_permit(self.ui.permitCheck.isChecked())
        self.labelView.set_permit_number(self.ui.permitEntry.text())

        # A RegEx for looking for headers in items
        #self.headerRE = re.compile('\{.*?\}')

        # New Style RE, matches {*}[*]
        self.headerRE = re.compile('(\{.*?\})(\[.*?\])*')

        self.ui.subsetBottom.setKeyboardTracking(False)
        self.ui.subsetTop.setKeyboardTracking(False)

        # Set up printer
        self.printer = QtPrintSupport.QPrinter()
        self.refresh_printer_selection()

        self.pageSetupUi = PageSetup.Ui_Dialog()
        self.pageProperties = QtWidgets.QDialog(self.MainWindow)
        self.pageSetupUi.setupUi(self.pageProperties)
        pageSize = self.currentPageSize
        self.pageSetupUi.pageWidth.setValue(pageSize[0])
        self.pageSetupUi.pageHeight.setValue(pageSize[1])

#         self.connect(self.pageProperties, QtCore.SIGNAL(
#             'accepted()'), self.set_page_size)
        self.pageProperties.accepted.connect(self.set_page_size)
#         self.connect(self.pageProperties, QtCore.SIGNAL(
#             'rejected()'), self.reset_page_properties)
        self.pageProperties.rejected.connect(self.reset_page_properties)

        # set up roll label dialog
        self.rollLabelDialog = QtWidgets.QDialog(self.MainWindow)
        self.rollLabelUi = RollLabelDialog.Ui_Dialog()
        self.rollLabelUi.setupUi(self.rollLabelDialog)

        # Set up carton label dialog
        self.cartonDialog = QtWidgets.QDialog(self.MainWindow)
        self.cartonUi = CartonLabel.Ui_Dialog()
        self.cartonUi.setupUi(self.cartonDialog)

#         self.connect(self.ui.createCartonLabels, QtCore.SIGNAL(
#             'clicked()'), self.show_carton_dialog)
        self.ui.createCartonLabels.clicked.connect(self.show_carton_dialog)

#         self.connect(self.cartonDialog, QtCore.SIGNAL(
#             'finished(int)'), self.create_carton_labels)
        self.cartonDialog.finished.connect(self.create_carton_labels)


        #self.pageProperties = QtGui.QPageSetupDialog(self.printer, self.MainWindow)

#         self.connect(self.ui.loadData, QtCore.SIGNAL(
#             'clicked()'), self.open_file)
        self.ui.loadData.clicked.connect(self.open_file)
#         self.connect(self.ui.clearData, QtCore.SIGNAL(
#             'clicked()'), self.clear_dataset)
        self.ui.clearData.clicked.connect(self.clear_dataset)

        #self.connect(self.ui.addTextBtn, QtCore.SIGNAL('clicked()'), self.add_text_dialog)
#         self.connect(self.ui.zoomLevel, QtCore.SIGNAL(
#             'valueChanged(double)'), self.zoom_spin_changed)
        self.ui.zoomLevel.valueChanged.connect(self.zoom_spin_changed)

#         self.connect(self.labelView, QtCore.SIGNAL(
#             "zoomUpdated(PyQt_PyObject)"), self.zoom_from_mouse)
        self.labelView.zoomUpdated.connect(self.zoom_from_mouse)
#         self.connect(self.labelView.scene(), QtCore.SIGNAL(
#             "selectionChanged()"), self.scene_selection_changed)
        self.labelView.scene().selectionChanged.connect(self.scene_selection_changed)
#         self.connect(self.ui.itemList, QtCore.SIGNAL(
#             'currentItemChanged(QTreeWidgetItem*,QTreeWidgetItem*)'), self.item_selected)
        self.ui.itemList.currentItemChanged.connect(self.item_selected)
#         self.connect(self.ui.headersCheck, QtCore.SIGNAL(
#             'toggled(bool)'), self.header_check)
        self.ui.headersCheck.toggled.connect(self.header_check)
#         self.connect(self.ui.permitCheck, QtCore.SIGNAL(
#             'toggled(bool)'), self.toggle_permit)
        self.ui.permitCheck.toggled.connect(self.toggle_permit)
#         self.connect(self.ui.permitEntry, QtCore.SIGNAL(
#             'textChanged(QString)'), self.permit_number_changed)
        self.ui.permitEntry.textChanged.connect(self.permit_number_changed)
#         self.connect(self.ui.returnCheck, QtCore.SIGNAL(
#             'toggled(bool)'), self.toggle_return_address)
        self.ui.returnCheck.toggled.connect(self.toggle_return_address)
#         self.connect(self.ui.returnAddress, QtCore.SIGNAL(
#             'textChanged()'), self.return_address_changed)
        self.ui.returnAddress.textChanged.connect(self.return_address_changed)
#         self.connect(self.ui.headerList, QtCore.SIGNAL(
#             'itemDoubleClicked(QTableWidgetItem*)'), self.add_header_text)
        self.ui.headerList.itemDoubleClicked.connect(self.add_header_text)
        self.ui.recyclablePackagingCheck.stateChanged.connect(self.recyclablePackagingCheck_stateChanged)

#         self.connect(self.ui.subsetBottom, QtCore.SIGNAL(
#             'valueChanged(int)'), self.update_subset_bottom)
        self.ui.subsetBottom.valueChanged.connect(self.update_subset_bottom)
#         self.connect(self.ui.subsetTop, QtCore.SIGNAL(
#             'valueChanged(int)'), self.update_subset_top)
        self.ui.subsetTop.valueChanged.connect(self.update_subset_top)
#         self.connect(self.ui.previewRecord, QtCore.SIGNAL(
#             'valueChanged(int)'), self.update_preview_record)
        self.ui.previewRecord.valueChanged.connect(self.update_preview_record)
#         self.connect(self.ui.previewCheck, QtCore.SIGNAL(
#             'toggled(bool)'), self.toggle_preview)
        self.ui.previewCheck.toggled.connect(self.toggle_preview)
#         self.connect(self.ui.layoutList, QtCore.SIGNAL(
#             'itemDoubleClicked(QListWidgetItem*)'), self.load_layout)
        self.ui.layoutList.itemDoubleClicked.connect(self.load_layout)

#         self.connect(self.ui.itemList, QtCore.SIGNAL(
#             'itemChanged(QTreeWidgetItem*, int)'), self.item_name_changed)
        self.ui.itemList.itemChanged.connect(self.item_name_changed)

        # Layout management
        # -----------------
#         self.connect(self.ui.saveLayout, QtCore.SIGNAL(
#             'clicked()'), self.save_layout)
        self.ui.saveLayout.clicked.connect(self.save_layout)
#         self.connect(self.ui.loadLayout, QtCore.SIGNAL(
#             'clicked()'), self.load_layout)
        self.ui.loadLayout.clicked.connect(self.load_layout)
#         self.connect(self.ui.removeLayout, QtCore.SIGNAL(
#             'clicked()'), self.remove_layout)
        self.ui.removeLayout.clicked.connect(self.remove_layout)
#         self.connect(self.ui.renameLayout, QtCore.SIGNAL(
#             'clicked()'), self.rename_layout)
        self.ui.renameLayout.clicked.connect(self.rename_layout)
#         self.connect(self.ui.refreshLayoutList, QtCore.SIGNAL(
#             'clicked()'), self.refresh_layout_list)
        self.ui.refreshLayoutList.clicked.connect(self.refresh_layout_list)
#         self.connect(self.ui.filterEdit, QtCore.SIGNAL(
#             'textChanged(QString)'), self.refresh_layout_list)
        self.ui.filterEdit.textChanged.connect(self.refresh_layout_list)
#         self.connect(self.ui.clearFilter, QtCore.SIGNAL(
#             'clicked()'), self.ui.filterEdit.clear)
        self.ui.clearFilter.clicked.connect(self.ui.filterEdit.clear)

        # Printer related signals
        # -----------------------
#         self.connect(self.ui.pageSetup, QtCore.SIGNAL(
#             'clicked()'), self.show_page_setup)
        self.ui.pageSetup.clicked.connect(self.show_page_setup)
#         self.connect(self.ui.printButton, QtCore.SIGNAL('clicked()'),
#                      self.show_printer_properties)  # self.print_labels)
        self.ui.printButton.clicked.connect(self.show_printer_properties)

#         self.connect(self.ui.createPdfBtn, QtCore.SIGNAL(
#             'clicked()'), self.create_pdf)
        self.ui.createPdfBtn.clicked.connect(self.create_pdf)
#         self.connect(self.ui.averyRadio, QtCore.SIGNAL(
#             'clicked()'), self.refresh_printer_selection)
        self.ui.averyRadio.clicked.connect(self.refresh_printer_selection)
#         self.connect(self.ui.zebraRadio, QtCore.SIGNAL(
#             'clicked()'), self.refresh_printer_selection)
        self.ui.zebraRadio.clicked.connect(self.refresh_printer_selection)

#         self.connect(self.ui.dateSort, QtCore.SIGNAL(
#             'toggled(bool)'), self.sort_by_date)
        self.ui.dateSort.toggled.connect(self.sort_by_date)

        # Setup a base progress window

        self.dataSetCount.setText("No data loaded.")

        self.ui.zoomLevel.setValue(160.0)
        self.ui.headersCheck.setChecked(True)

        self.logAppendCursor = self.ui.logConsole.cursorForPosition(
            QtCore.QPoint(0, 0))
        self.logScrollBar = self.ui.logConsole.verticalScrollBar()
        # self.ui.logConsole.setLineWrapMode(self.ui.logConsole.NoWrap)

        self.load_settings()

        # Check system args and load passed file list, and directory as default.

        self.currentDirectory = '\\\\pleqol01\\data\\%s\\%s' % (
            thisYear, thisMonth)
        self.currentFile = None

        if len(sys.argv) > 1:
            if os.path.isfile(sys.argv[1]):
                files = open(sys.argv[1], "rb").read().split("\n")

                if os.path.isfile(files[0]):
                    self.load_dataset(files[0])
                    #self.currentDirectory = os.path.split(files[0])[0]
                    self.currentFile = files[0]
        if len(sys.argv) > 2:
            self.currentDirectory = sys.argv[2]
        elif self.currentFile != None:
            self.currentDirectory = os.path.split(self.currentFile)[0]

        self.ui.splitByRollAmount.setValue(3950)

        # Hide unused print options
        self.ui.individualPdfs.setHidden(True)
        self.ui.pdfNameFormat.setHidden(True)
        self.ui.label_2.setHidden(True)
        self.ui.genSamples.setHidden(True)
        self.ui.label_6.setHidden(True)
        self.ui.sampleCount.setHidden(True)

        self.ui.layoutList.setItemDelegate(LayoutDelegate(self))

        self.MainWindow.show()

    def recyclablePackagingCheck_stateChanged(self, state):
        self.labelView.recyclablePackagingText.setVisible(state)

    def sort_by_date(self, toggle):
        self.sortByDate = toggle
        self.refresh_layout_list()

    def show_carton_dialog(self):
        """ Shows the carton label creation dialog. """
        self.cartonDialog.show()
        self.cartonUi.jobNo.setFocus()

    def refresh_printer_selection(self):
        #printers = QtGui.QPrinterInfo.availablePrinters()
        printers = QtPrintSupport.QPrinterInfo.availablePrinters()

        printerType = str(
            self.ui.printerSelectGroup.checkedButton().text()).lower()
        if printerType == 'zebra':
            printerType = '110xi4'

        defaultPrinter = None
        for i in printers:
            name = i.printerName()
            if printerType in str(name).lower():
                defaultPrinter = name

        if not defaultPrinter:
            defaultPrinter = QtPrintSupport.QPrinterInfo.defaultPrinter().printerName()

        #self.printer = QtGui.QPrinter()
        self.print = QtPrintSupport.QPrinter()
        self.printer.setPrinterName(defaultPrinter)

    def create_carton_labels(self, accepted):
        """ Will create carton labels based on fields entered in the carton label creation dialog. """
        if accepted:

            self.ui.previewCheck.setChecked(False)

            self.clear_layout()

            logo = None
            if self.cartonUi.bluestarLogo.isChecked():
                logo = "bluestar.png"
            elif self.cartonUi.printlinkLogo.isChecked():
                logo = "printlink.png"

            stock = self.cartonUi.stockName.text()
            total = self.cartonUi.totalQuantity.value()
            cartonQuantity = self.cartonUi.cartonQuantity.value()
            jobNo = self.cartonUi.jobNo.text()
            largeLabel = self.cartonUi.largeLabel.isChecked()
            if largeLabel:
                self.pageSetupUi.pageWidth.setValue(102)
                self.pageSetupUi.pageHeight.setValue(73)
            else:
                self.pageSetupUi.pageWidth.setValue(90)
                self.pageSetupUi.pageHeight.setValue(45)
            self.set_page_size()

            cartons = int(math.ceil(float(total) / cartonQuantity))

            data = [["Total", "CartonQuantity", "CartonNumber", "Total Cartons"]]

            for i in range(cartons):
                row = []
                row.append(str(total))

                if i+1 != cartons:
                    row.append(str(cartonQuantity))
                else:
                    val = total % cartonQuantity
                    if val:
                        row.append(str(val))
                    else:
                        row.append(str(cartonQuantity))
                row.append(str(i+1))
                row.append(str(cartons))

                data.append(row)
            self.rawData = data
            self.setup_data()

            jobNoLabel = self.add_text((5, 14), "relmm", select=False)
            jobNoLabel.propNames["Text"].set_value("Job:")

            jobNoText = self.add_text((38, 14), "relmm", select=False)
            jobNoText.propNames["Text"].set_value("%s" % jobNo)
            font = jobNoText.propNames["Font"].get_value()
            font.setPointSize(12)
            font.setBold(True)
            # jobNoText.propNames["Font"].set_value(font)

            stockLabel = self.add_text((5, 20), "relmm", select=False)
            stockLabel.propNames["Text"].set_value("Description:")

            stockText = self.add_text((38, 20), "relmm", select=False)
            stockText.propNames["Text"].set_value("%s" % stock)
            font = stockText.propNames["Font"].get_value()
            font.setPointSize(10)
            font.setBold(True)
            # stockText.propNames["Font"].set_value(font)

            qtyTextLabel1 = self.add_text((5, 26), "relmm", select=False)
            qtyTextLabel1.propNames["Text"].set_value("Quantity in carton:")

            qtyTextLabel2 = self.add_text((5, 32), "relmm", select=False)
            qtyTextLabel2.propNames["Text"].set_value("Carton:")

            qtyText1 = self.add_text((38, 26), "relmm", select=False)
            qtyText1.propNames["Text"].set_value("{CartonQuantity}")

            qtyText2 = self.add_text((38, 32), "relmm", select=False)
            qtyText2.propNames["Text"].set_value(
                "{CartonNumber} of {Total Cartons}")

            if logo:
                logoText = self.add_text(
                    (45 + (largeLabel*13), 5), "relmm", select=False)
                logoText.propNames["Text"].set_value("<IMG SRC='%s'>" % logo)

            self.ui.previewCheck.setChecked(True)

        self.cartonUi.printlinkLogo.setChecked(True)
        self.cartonUi.stockName.setText("")
        self.cartonUi.totalQuantity.setValue(1)
        self.cartonUi.cartonQuantity.setValue(1)
        self.cartonUi.jobNo.setText("")
        self.cartonUi.largeLabel.setChecked(True)

    def remove_layout(self):
        layoutItem = self.ui.layoutList.currentItem()
        if layoutItem != None:
            ret = QtWidgets.QMessageBox.warning(self.MainWindow, 'Remove Layout',
                                            'Are you sure you would like to remove the \'%s\' layout?' % str(
                                                layoutItem.data(QtCore.Qt.UserRole).toString()),
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if ret == QtWidgets.QMessageBox.Yes:
                session = self.sessionMaker()
                q = session.query(tables.Layout).filter_by(name=str(
                    layoutItem.data(QtCore.Qt.UserRole).toString())).first()
                if q:

                    session.delete(q)
                    session.commit()
                    self.refresh_layout_list()
                # self.settings.beginGroup("layouts")
                # self.settings.remove(layoutItem.text())
                # self.settings.endGroup()
                # self.load_settings()
        else:
            self.log_message('No layout selected', 'error')
            self.beep()

    def save_layout_to_conf(self, layout):
        self.settings.beginGroup("layouts")
        self.settings.remove(layout.name)
        self.settings.beginGroup(layout.name)

        self.settings.setValue("permit", layout.permit)
        self.settings.setValue("return", layout.returnAddress)
        self.settings.setValue("usepermit", layout.permitEnabled)
        self.settings.setValue("usereturn", layout.returnEnabled)

        for objName, objType, props in layout.objectList:
            self.settings.beginGroup(objName)
            self.settings.setValue("type", objType)
            for propName, propVal in props:
                self.settings.setValue(propName, propVal)
            self.settings.endGroup()
        self.settings.endGroup()
        self.settings.endGroup()

    def save_layout_to_db(self, layout):
        session = self.sessionMaker()

        # First Test to see if a layout by this name already exists
        q = session.query(tables.Layout).filter_by(name=layout.name).first()
        if q:
            session.delete(q)
            session.commit()

        newLayout = tables.Layout(layout.name, layout.permit, layout.returnAddress,
                                  layout.permitEnabled, layout.returnEnabled, layout.pageWidth, layout.pageHeight)
        session.add(newLayout)
        session.commit()
        for objName, objType, props in layout.objectList:
            obj = tables.LayoutObject(newLayout.id, str(objName), objType)
            session.add(obj)
            session.commit()

            for propName, propVal in props:
                prop = tables.ObjectProperty(obj.id, propName, propVal)
                session.add(prop)
                session.commit()

    def rename_layout(self):
        selected = self.ui.layoutList.selectedItems()
        if len(selected) == 0:
            QtWidgets.QMessageBox.critical(self.MainWindow, "Error, no layout selected.",
                                       "Error, there is no layout selected, please select one first!")
            return

        oldName = str(selected[0].data(QtCore.Qt.UserRole).toString())

        newName, useName = QtWidgets.QInputDialog.getText(
            self.MainWindow, "Enter in new name", "Please enter in the new label name", text=oldName)

        newName = str(newName)
        if useName:
            session = self.sessionMaker()
            res = session.query(tables.Layout).filter_by(name=newName).first()
            if res:
                QtWidgets.QMessageBox.critical(self.MainWindow, "Error, name is in use.",
                                           "Error, the layout name is already in use, try again!")
                return
            else:
                layout = session.query(tables.Layout).filter_by(
                    name=oldName).first()
                if layout:
                    layout.name = newName
                    session.commit()
                    self.refresh_layout_list()
                else:
                    QtWidgets.QMessageBox.critical(self.MainWindow, "Error!.",
                                               "There was an error renaming '%s', it could not be found!" % oldName)

    def save_layout(self):
        item = self.ui.layoutList.currentItem()
        if item:
            current = item.data(QtCore.Qt.UserRole).toString()
            itemText = item.data(QtCore.Qt.UserRole).toString()
        else:
            current = QtCore.QString()
            itemText = None
        text = ""
        question = "Enter the name of the layout"
        while str(text).strip() == "":
            text, ok = QtWidgets.QInputDialog.getText(
                self.MainWindow, "Name of Layout", question, QtWidgets.QLineEdit.Normal, current)
            if ok and str(text).strip() != "":
                layoutName = str(text).strip()
                # OK, Valid Name
                permit = str(self.ui.permitEntry.text())
                returnAddress = str(self.ui.returnAddress.toPlainText())
                permitEnabled = self.ui.permitCheck.isChecked()
                returnEnabled = self.ui.returnCheck.isChecked()
                pageWidth = self.currentPageSize[0]
                pageHeight = self.currentPageSize[1]

                objects = []

                for obj in self.objectCollection:
                    objName = obj.name
                    objType = obj.objectType
                    props = []

                    #self.settings.setValue("name", obj.name)
                    for name, prop in list(obj.propNames.items()):

                        props.append(
                            (name, str(QtCore.QVariant(prop.get_value()).toString())))
                    objects.append((objName, objType, props))
                layout = LabelLayout(layoutName, permit, returnAddress,
                                     permitEnabled, returnEnabled, pageWidth, pageHeight, objects)

                # self.save_layout_to_conf(layout)
                self.save_layout_to_db(layout)
                # self.load_settings()
                self.refresh_layout_list()
                if itemText:
                    item = self.ui.layoutList.findItems(
                        itemText, QtCore.Qt.MatchExactly)[0]
                    self.ui.layoutList.setCurrentItem(item)
            elif ok and str(text).strip() == "":
                # OK, Invalid name, try again
                question = "Value was blank, please enter in a non-blank name"
            else:
                # Canceled
                break

    def create_defaults(self):
        self.settings.beginGroup("Default Layout")
        #
        self.settings.setValue("permit", "478")
        self.settings.setValue(
            "return", "If Undelivered, Return To: Private Bag 39996, Wellington Mail Centre, Lower Hutt  5045")
        self.settings.setValue("usepermit", True)
        self.settings.setValue("usereturn", True)
        #
        #
        self.settings.beginGroup("Address Block")
        ##
        self.settings.setValue("type", "Text")
        self.settings.setValue(
            "Text", "{Address1}\n{Address2}\n{Address3}\n{Address4}\n{Address5}\n{Address6}\n{Address7}\n{Address8}")
        self.settings.setValue("X Coord", 4.5)
        self.settings.setValue("Y Coord", 15.0)
        self.settings.setValue("Font", QtGui.QFont(
            "Arial", 9.0, QtGui.QFont.Normal, False))
        self.settings.setValue("Skip Blanks", True)
        self.settings.setValue("Line Spacing", 100.0)
        ##
        self.settings.endGroup()
        #
        self.settings.endGroup()

    def refresh_layout_list(self):
        selected = self.ui.layoutList.selectedItems()
        if selected:
            selected = selected[0].data(QtCore.Qt.UserRole)
        session = self.sessionMaker()
        if self.sortByDate:

            layouts = [(x.name, x.lastPrinted) for x in session.query(tables.Layout).order_by(
                desc(tables.Layout.lastPrinted)).order_by(tables.Layout.name).all()]

        else:
            layouts = [(x.name, x.lastPrinted) for x in session.query(
                tables.Layout).order_by(tables.Layout.name).all()]
        filtered = []
        filterText = str(self.ui.filterEdit.text()).lower()
        if filterText != "":
            for layout in layouts:
                if filterText in layout[0].lower():
                    filtered.append(layout)
        else:
            filtered = layouts[:]

        self.ui.layoutList.clear()
        currentRow = None
        x = 0
        for layout in filtered:
            name, date = layout

            if name == selected:
                currentRow = x
            x += 1
            date = date.strftime("%Y-%m-%d")
            text = "%s  [%s]" % (name, date)
            item = QtWidgets.QListWidgetItem(text)
            #item = LayoutDelegate()

            item.setData(QtCore.Qt.UserRole, name)
            item.setData(QtCore.Qt.DisplayRole, date)
            self.ui.layoutList.addItem(item)
        if currentRow is not None:
            self.ui.layoutList.setCurrentRow(currentRow)

    def load_settings(self):
        #currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        #shutil.copy("labelcore.conf", "confArchive\\labelcore.conf.bak.%s" % currentTime)

        self.settings = QtCore.QSettings(
            "labelcore.conf", QtCore.QSettings.IniFormat)

        self.settings.beginGroup('mainapp')
        keys = []
        for x in self.settings.allKeys():
            keys.append(str(x))
        for key, value in list(self.defaultSettings.items()):
            if key not in keys:
                self.settings.setValue(key, value)
        self.settings.sync()

        self.refresh_layout_list()

        print("self.settings.value('zoom'): " + self.settings.value('zoom'))
        #self.ui.zoomLevel.setValue(self.settings.value('zoom').toDouble()[0])
        self.ui.zoomLevel.setValue(float(self.settings.value('zoom')))
        self.ui.permitEntry.setText(self.settings.value('permit'))
#         self.ui.permitCheck.setChecked(
#             self.settings.value('usepermit').toBool())
        print("self.settings.value('usepermit'): " + str(self.settings.value('usepermit')))
        self.ui.permitCheck.setChecked(
            bool(self.settings.value('usepermit')))
#         self.ui.returnAddress.setPlainText(
#             self.settings.value('return').toString())
        self.ui.returnAddress.setPlainText(
            self.settings.value('return'))
#         self.ui.returnCheck.setChecked(
#             self.settings.value('usereturn').toBool())
        self.ui.returnCheck.setChecked(
            bool(self.settings.value('usereturn')))
        # self.ui.copyCount.setValue(self.settings.value('copies').toInt()[0])

        self.settings.endGroup()
        layoutGroups = []

        self.settings.beginGroup("layouts")

        for group in self.settings.childGroups():
            layoutGroups.append(group)
        if len(layoutGroups) == 0:
            self.create_defaults()
            layoutGroups.append('Default Layout')

        # self.ui.layoutList.clear()
        # for layout in layoutGroups:
        #    self.settings.beginGroup(layout)
        #    item = QtGui.QListWidgetItem(layout)
        #    item.setData(QtCore.Qt.UserRole, layout)
        #    self.ui.layoutList.addItem(item)
        #    self.settings.endGroup()

        self.settings.endGroup()

    def load_layout(self, item=None):
        check = self.ui.previewCheck.isChecked()
        if self.ui.previewCheck.isChecked():
            self.ui.previewCheck.setChecked(False)
        if not item:
            item = self.ui.layoutList.currentItem()
        if item != None:
            # self.set_layout(item)
            # self.load_layout_from_conf(item)
            layout = self.load_layout_from_db(item)
            if layout:
                self.set_layout(layout)
            else:
                self.log_message("Error loading layout from database", "error")

        else:
            self.log_message('No layout selected', 'error')
            self.beep()
        self.ui.previewCheck.setChecked(check)

    def load_layout_from_db(self, item):
        """ Creates a layout from the db connection """
        session = self.sessionMaker()

        name = str(item.data(QtCore.Qt.UserRole))

        statement = session.query(tables.Layout, tables.LayoutObject,
                                  tables.ObjectProperty).filter(tables.Layout.id == tables.LayoutObject.layoutId,
                                                                tables.LayoutObject.id == tables.ObjectProperty.layoutObjectId,
                                                                tables.Layout.name == name).order_by(asc(tables.LayoutObject.name))
        results = statement.all()

        if results == []:
            # Layout possibly has no objects, so lets just grab the layout details
            results = [(x, None, None) for x in session.query(
                tables.Layout).filter(tables.Layout.name == name)]

        name = None

        objects = []
        objName = None
        objType = None
        props = None
        permit = None
        returnAddress = None
        permitEnabled = None
        returnEnabled = None
        pageWidth = None
        pageHeight = None

        for layout, layoutobject, objectproperty in results:
            if name == None:
                name = layout.name
                permit = layout.permit
                returnAddress = layout.returnAddress
                permitEnabled = layout.permitEnable
                returnEnabled = layout.returnEnable
                pageWidth = layout.pageWidth
                pageHeight = layout.pageHeight

            if layoutobject != None:
                if objName != layoutobject.name:
                    # objAdded.append(objName)
                    if objName != None:
                        if props != None:
                            props.sort(key=lambda x: self.objectTypes[str(
                                objType)].propLoadOrder.index(x[0]))

                        objects.append((objName, objType, props))
                    objName = layoutobject.name
                    objType = layoutobject.objType
                    props = []

            if objectproperty != None:
                props.append((objectproperty.propType, objectproperty.propVal))

        if name != None:
            if objName != None:
                objects.append((objName, objType, props))
            layoutObj = LabelLayout(
                name, permit, returnAddress, permitEnabled, returnEnabled, pageWidth, pageHeight, objects)

            return layoutObj

        else:

            return False

    def load_layout_from_conf(self, item):
        """ Creates a layout from a conf file """
        name = item.text()
        self.clear_layout()
        self.settings.beginGroup("layouts")
        self.settings.beginGroup(name)

        permit = self.settings.value("permit").toString()
        returnAddress = self.settings.value("return").toString()
        permitEnabled = self.settings.value("usepermit").toBool()
        returnEnabled = self.settings.value("useReturn").toBool()
        pageWidth = 90
        pageHeight = 45

        objects = []
        for objectName in self.settings.childGroups():
            self.settings.beginGroup(objectName)

            objType = str(self.settings.value("type").toString())

            props = []
            for propName in self.settings.childKeys():
                if str(propName) == "type":
                    continue
                propVal = self.settings.value(propName)
                props.append((propName, propVal))
            objectDesc = (objectName, objType, props)
            objects.append(objectDesc)
            self.settings.endGroup()
        self.settings.endGroup()
        self.settings.endGroup()

        layout = LabelLayout(name, permit, returnAddress, permitEnabled,
                             returnEnabled, pageWidth, pageHeight, objects)
        return layout

        # self.set_layout(layout)

    def set_layout(self, layout):
        self.clear_layout()
        self.currentLayout = layout

        self.ui.permitEntry.setText(layout.permit)
        self.ui.permitCheck.setChecked(layout.permitEnabled)
        if "<html>" in str(layout.returnAddress).lower():
            self.ui.returnAddress.setHtml(layout.returnAddress)
        else:
            self.ui.returnAddress.setPlainText(layout.returnAddress)

        self.toggle_return_address(layout.returnEnabled)
        self.ui.returnCheck.setChecked(layout.returnEnabled)
        for objectName, objType, props in layout.objectList:

            obj = self.objectTypes[str(objType)](objectName)

            self.add_object(obj)
            for propName, propVal in props:
                if str(propName) == "type":
                    continue
                obj.propNames[str(propName)].set_value(
                    QtCore.QVariant(propVal))

        self.currentPageSize = (layout.pageWidth, layout.pageHeight)
        self.pageSetupUi.pageWidth.setValue(layout.pageWidth)
        self.pageSetupUi.pageHeight.setValue(layout.pageHeight)
        self.set_page_size()

    def clear_layout(self):
        for obj in self.objectCollection[:]:
            self.remove_object(obj)

        self.ui.permitCheck.setChecked(False)
        self.ui.returnCheck.setChecked(False)
        self.ui.returnAddress.setHtml("")
        self.ui.permitEntry.setText("")

        self.clear_object_properties()

        self.log_message("Layout Cleared")

    def remove_object(self, obj):
        """ Removes an object from the scene, and object collections """
        self.labelView.scene().removeItem(obj)
        self.objectCollection.remove(obj)
        self.ui.itemList.takeTopLevelItem(
            self.ui.itemList.indexOfTopLevelItem(self.itemListObjects[obj]))

        current = self.ui.itemList.currentItem()
        prev = self.itemListObjects[obj]

        self.itemNames.remove(obj.name)
        del self.itemListObjects[obj]
        self.clear_object_properties()
        self.processEvents()
        self.item_selected(current, prev)

        # self.objectGarbage.append(obj)

    def log_message(self, message, level="log"):
        """ Logs a message to the console, levels include log, warning, and error """
        color = 'black'

        if level == "error":
            color = 'red'
        elif level == "warning":
            color = 'orange'

        timestamp = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S - ")
        text = timestamp + \
            "<FONT COLOR='%s'>%s</FONT><BR />" % (color, message)

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
            item = QtWidgets.QTableWidgetItem(self.dataSet[val-1][i])
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
        # self.ui.permitPosition.setEnabled(toggle)
        self.ui.permitEntry.setEnabled(toggle)
        self.labelView.toggle_permit(toggle)

    def permit_number_changed(self, text):
        """ Called when the permit number is updated in the text field """
        self.labelView.set_permit_number(str(text))

    def return_address_changed(self):
        """ Called to update the return address """
        self.labelView.set_return_address(self.ui.returnAddress.toPlainText())
        self.labelView.returnAddress.updateGeometry()

    def header_check(self, toggle):
        """ Called when the header checkbox is toggled to set headers on/off in the dataset """
        self.hasHeaders = toggle
        self.setup_data()

    def open_file(self):
        """ Shows an open file dialog, then proceeds to load the file as data """
        filename = str(QtWidgets.QFileDialog.getOpenFileName(
            self.MainWindow, "Select File", self.currentDirectory))
        if filename != "":
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

    def clear_dataset(self):
        self.rawData = []
        self.dataSet = []
        self.headers = []
        self.ui.headerList.clear()
        self.ui.headerList.setRowCount(0)
        self.dataSetCount.setText("Dataset is empty.")
        self.ui.subsetBottom.setMinimum(0)
        self.ui.subsetBottom.setMaximum(0)
        self.ui.subsetTop.setMinimum(0)
        self.ui.subsetTop.setMaximum(0)
        self.ui.previewRecord.setMinimum(0)
        self.ui.previewRecord.setMaximum(0)
        self.ui.copyField.clear()
        self.filenameStatus.setText("")

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
                maxLen = max(maxLen, len(row))
            for row in self.rawData:
                if len(row) < maxLen:
                    row += [""] * (maxLen-len(row))
            self.filenameStatus.setText(filename)
            self.setup_data()
        else:
            # Extension not recognised
            self.log_message('unknown format %s' % ext, "error")
            self.filenameStatus.setText("")

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
            headEnum.append((row, self.headers[row]))
            item = QtWidgets.QTableWidgetItem(self.headers[row])
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
            self.dataSetCount.setText("The dataset contains %d record%s." % (
                len(self.dataSet), "s" if len(self.dataSet) > 1 else ""))
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
                record = str(
                    self.dataSet[self.ui.previewRecord.value()-1][i])
                item = QtWidgets.QTableWidgetItem(record)
                self.ui.headerList.setItem(row, 1, item)
                self.ui.copyField.addItem(i)
                row += 1
            self.ui.copyField.setUpdatesEnabled(True)

        self.ui.headerList.setUpdatesEnabled(True)

    def add_header_text(self, item):
        #itemSelection = self.labelView.scene().selectedItems()

        currentItem = self.ui.itemList.currentItem()
        row = item.row()
        headerItem = self.ui.headerList.item(row, 0)

        if currentItem:
            obj = currentItem.data(0, QtCore.Qt.UserRole).toPyObject()
            if obj.objectType == "Text":
                obj.propNames["Text"].insert_text(
                    "{%s}<BR \>\n" % str(headerItem.text()))
            elif obj.objectType == "Barcode":
                x = []
                for i in range(self.ui.headerList.rowCount()):
                    x.append(
                        "{" + str(self.ui.headerList.item(i, 0).text()) + "}")
                obj.propNames["Data"].insert_text(",".join(x))
        # if len(itemSelection) == 1:
        #    itemSelection[0].textCursor().insertText("{%s}" % unicode(item.text()))
        #    itemSelection[0].update_text()
        #    self.labelView.setFocus(True)
        #    itemSelection[0].setFocus(True)

    def load_csv(self, filename):
        return [row for row in UnicodeReader(open(filename, "rb"), encoding='cp1252')]

    def load_xls(self, filename):
        """ loads both xls and xlsx, providing that xlrd 0.9+ is used """
        """ Marvin 18/11/2021: We mostly use CSV... this function is deprecated. """
        xlfile = xlrd.open_workbook(filename)
        sheets = xlfile.sheet_names()
        # Ask the user which sheet to use
        name, result = QtWidgets.QInputDialog.getItem(self.MainWindow,
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
                        celldate = xlrd.xldate_as_tuple(
                            cell.value, xlfile.datemode)
                        if cell.xf_index == None:
                            celldate = datetime.datetime(
                                *celldate).strftime("%d %B %Y")
                        # Type is a date, so it will read into a datetime.datetime object
                        newrow.append(celldate)

                    elif cell.ctype == 4:
                        # cell is a boolean type
                        newrow.append(
                            "TRUE") if cell.value else newrow.append("FALSE")
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

    def add_text(self, pos, posType="abs", select=True):  # text, x, y):
        """ add a text item at pos, returns a point to the object. Pos type can be "abs" for absolute window co-ords, or "rel" for on-paper co-ords """
        name = "Text"
        count = 0
        while name in self.itemNames:
            count += 1
            name = "Text%d" % count
        # self.itemNames.append(name)
        obj = LabelerTextItem(name)

        self.add_object(obj)

        if posType == "abs":
            obj.setPos(self.labelView.mapToScene(pos))
        elif posType == "rel":
            obj.setPos(QtCore.QPointF(pos))
        elif posType == "relmm":
            # Set by mm
            obj.set_pos_by_mm(*pos)
        else:
            raise ValueError("Unrecognised position type %s" % posType)
        obj.setHtml("Enter Text")

        obj.propNames["Font"].set_value(obj.propNames["Font"].get_font())
        if select:
            item = self.ui.itemList.findItems(name, QtCore.Qt.MatchExactly)[0]
            self.ui.itemList.setCurrentItem(item)

        return obj

    def add_image(self, pos):
        name = "Image"
        count = 0
        while name in self.itemNames:
            count += 1
            name = "Image%d" % count

        obj = LabelerImageItem(name)

        self.add_object(obj)

        obj.setPos(self.labelView.mapToScene(pos))

        item = self.ui.itemList.findItems(name, QtCore.Qt.MatchExactly)[0]
        self.ui.itemList.setCurrentItem(item)

    def add_barcode(self, pos):
        """ Add a barcode item """

        name = "Barcode"
        count = 0
        while name in self.itemNames:
            count += 1
            name = "Barcode%d" % count

        obj = LabelerBarcodeItem(name)

        self.add_object(obj)

        obj.setPos(self.labelView.mapToScene(pos))

        item = self.ui.itemList.findItems(name, QtCore.Qt.MatchExactly)[0]
        self.ui.itemList.setCurrentItem(item)

    def add_object(self, obj):
        """ Adds the object to the Scene, list of objects,  """
        self.labelView.scene().addItem(obj)
        #item = PropertyListItem(self.ui.itemList)

        self.itemNames.append(obj.name)
        item = QtWidgets.QTreeWidgetItem(self.ui.itemList)

        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        item.setText(0, obj.name)
        item.setData(0, QtCore.Qt.UserRole, obj)
        self.itemListObjects[obj] = item

        self.objectCollection.append(obj)

    def item_name_changed(self, item, col):

        obj = item.data(col, QtCore.Qt.UserRole).toPyObject()
        if obj != None:
            newName = item.text(col)
            oldName = obj.name
            if newName not in self.itemNames:
                if oldName in self.itemNames:
                    self.itemNames.remove(oldName)
                obj.name = newName
                self.itemNames.append(newName)
            elif newName != oldName:
                self.log_message(
                    "An item already exists with the name %s" % newName, "error")
                self.beep()
                item.setText(col, oldName)

    def show_printer_properties(self):
#         self.printProperties = QtWidgets.QPrintDialog(
        self.printProperties = QtPrintSupport.QPrintDialog(
            self.printer, self.MainWindow)
        self.connect(self.printProperties, QtCore.SIGNAL(
            'accepted()'), self.print_labels)

        self.printProperties.show()

    def show_page_setup(self):
        self.pageProperties.show()

    def set_page_size(self):
        self.currentPageSize = (
            self.pageSetupUi.pageWidth.value(), self.pageSetupUi.pageHeight.value())
        self.labelView.setPageSize(
            (self.dpmm[0]*self.currentPageSize[0], self.dpmm[1]*self.currentPageSize[1]))


    def reset_page_properties(self):
        pageSize = self.currentPageSize
        self.pageSetupUi.pageWidth.setValue(pageSize[0])
        self.pageSetupUi.pageHeight.setValue(pageSize[1])

    def start_merge(self, preview=False):
        self.labelView.start_merge(preview)
        self.merging = True
        for obj in self.objectCollection:
            obj.start_merge()

        self.mergeDataSet = self.dataSet
        self.currentRecordNumber = 1

        if self.ui.useSubset.checkState():
            self.currentRecordNumber = int(self.ui.subsetBottom.value())
            self.mergeDataSet = self.dataSet[int(
                self.ui.subsetBottom.value()) - 1:int(self.ui.subsetTop.value())]

        if self.ui.genSamples.checkState():
            self.mergeDataSet = random.sample(
                self.mergeDataSet, int(self.ui.sampleCount.value()))

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

    def merge_value(self, value, row):
        text = str(value)
        matches = self.headerRE.findall(text)

        matches = set(matches)
        for fieldname, substring in matches:
            field = fieldname.replace("{", "").replace("}", "")

            replaceString = fieldname+substring
            if substring:
                vals = substring.replace("[", "").replace("]", "").split(":")
                if len(vals) == 1:
                    text = text.replace(fieldname+substring,
                                        row[field][int(vals[0])])
                else:
                    start, end = vals
                    if start.strip() == "":
                        text = text.replace(
                            replaceString, row[field][:int(end)])
                    elif end.strip() == "":
                        text = text.replace(
                            replaceString, row[field][int(start):])
                    else:
                        text = text.replace(
                            replaceString, row[field][int(start):int(end)])
            else:
                text = text.replace(replaceString, row[field])

        return text

    def clear_object_properties(self):
        while True:
            # Loops through all the current properties on the property page, and hides them
            widgetItem = self.ui.objectProperties.takeAt(0)
            # This check is made due to a bug with the formlayout incorrectly
            # keeping track of how many items it has
            if widgetItem != None:
                widget = widgetItem.widget()
                widget.setVisible(False)
            else:
                break

    def item_selected(self, currentItem, previousItem):
        """ Selects the currentItem on the label view, and populates its properties """
        self.ui.objectPropertyArea.setUpdatesEnabled(False)
        if currentItem != None:
            # print self.ui.objectProperties.rowCount()
            # for i in range(self.ui.objectProperties.rowCount()):
            self.clear_object_properties()
            # Get a reference to the object
            obj = currentItem.data(0, QtCore.Qt.UserRole).toPyObject()
            if self.labelView.isInteractive():
                # The label view is currently in edit mode
                if not obj.isSelected():
                    # Select the object if it isn't already
                    obj.scene().clearSelection()
                    obj.setSelected(True)
            for field in obj.properties:
                # Populate the property list for this widgets items
                for widget in field.widgetOrder:
                    self.ui.objectProperties.addRow("%s %s" % (
                        field.name, widget), field.widgets[widget])
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
        self.progressWindow = QtWidgets.QProgressDialog(self.MainWindow)
        self.progressWindow.setWindowTitle("PDF Generation Progress...")
        self.progressWindow.setMinimumWidth(300)
        self.connect(self.progressWindow, QtCore.SIGNAL(
            'canceled()'), self.cancel_label)
        self.progressWindow.setRange(minimum, maximum)
        newValue = 1
        progressText = "Generating Page %d of %d" % (
            newValue, self.progressWindow.maximum())
        self.progressWindow.setValue(newValue)
        self.progressWindow.setLabelText(progressText)
        self.progressWindow.show()

    def increment_progress_bar(self, amount=1):
        """ This should be called each time the progress increases by one stage """
        newValue = self.progressWindow.value() + amount
        progressText = "Generating Page %d of %d" % (
            newValue, self.progressWindow.maximum())
        self.progressWindow.setValue(newValue)
        self.progressWindow.setLabelText(progressText)
        # self.progressWindow.update()

    def end_progress_window(self):
        self.progressWindow.setParent(None)
        del self.progressWindow

    # def render_pdf(self):
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
        fieldMessage = ""
        substringMessage = ""
        for obj in self.objectCollection:
            # Unselect it
            obj.setSelected(False)

            # Test text for any merge fields, then test that against the header listing
            text = str(obj.get_merge_text())
            matches = self.headerRE.findall(text)
            matches = sorted(set(matches))
            for field, substring in matches:
                x = field.replace("{", "").replace("}", "")
                if substring != "":
                    vals = substring.replace(
                        "[", "").replace("]", "").split(":")

                    if len(vals) == 0 or len(vals) > 2:
                        if not obj.suppress_address_errors:
                            # Was unable to find a match for this substring, so issue a warning
                            substringMessage += " %s," % x
                            headersMatched = False
                    else:
                        for i in vals:
                            if not i.strip().isdigit() and i.strip() != "":
                                if not obj.suppress_address_errors:
                                    # Was unable to find a match for this substring, so issue a warning
                                    substringMessage += " %s," % x
                                    headersMatched = False
                                break
                if x not in self.headers:
                    if not obj.suppress_address_errors:
                        # Was unable to find a match for this header, so issue a warning
                        fieldMessage += " %s," % x
                        #self.log_message("Error, could not find header %s, please check your spelling.\n" % x, "error")
                        headersMatched = False
        if not headersMatched:
            if fieldMessage:
                self.log_message(
                    "Error, the following fields could not be found: " + fieldMessage[1:-1], "error")
            if substringMessage:
                self.log_message(
                    "Error, the substring formatting is incorrect for: " + substringMessage[1:-1], "error")

            self.beep()

        return headersMatched

    def make_labels(self, method="PDF"):
        """ Starts making labels, if method is set to "PRINT", it will also 
            print to the selected printer """
        if self.ui.individualPdfs.isChecked() and self.currentFile == None:
            self.log_message("No file opened for individual PDFs", "error")
            return
        # preserve preview state
        if method == "PRINT":
            result = self.rollLabelDialog.exec_()
            if not result:
                res = QtWidgets.QMessageBox.question(
                    self.MainWindow, "Cancel labels", "Did you want to cancel the labels?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if res == QtWidgets.QMessageBox.Yes:
                    return
                rollLabels = False
            else:
                rollLabels = True
        previewState = self.ui.previewCheck.isChecked()

        # now disable it
        self.ui.previewCheck.setChecked(False)

        if not self.field_check():
            # field matching failed, abort
            self.ui.previewCheck.setChecked(previewState)
            return

        # self.MainWindow.hide()
        if method == "PRINT":
            # If method type is set to PRINT, also set up a printer to the currently
            # selected printer
            #printer = QtGui.QPrinter()
            # printer.setPrinterName(self.currentPrinter)
            # printer.setOrientation(printer.Portrait)

            # Due to something to do with the Avery printer, we need to set the
            # dimensions to be 2x their normal width and height
            self.printer.setPaperSize(QtCore.QSizeF(
                self.currentPageSize[0], self.currentPageSize[1]), QtPrintSupport.QPrinter.Millimeter)
            self.printer.setFullPage(True)
            self.printer.setColorMode(self.printer.GrayScale)

            painter = QtGui.QPainter()
            painter.begin(self.printer)

        # Set up a printer to output to PDF

        outputName = "Testing.pdf"

        # Set pdf name to inputname + '_labels.pdf' if currentFile is not none

        if not self.ui.individualPdfs.isChecked():
            # Not set to individualise PDFs, create one file
            if self.currentFile != None:

                outputName = os.path.splitext(self.currentFile)[
                    0] + '_labels.pdf'
            pdfPrint = QtPrintSupport.QPrinter()
            pdfPrint.setOutputFileName(outputName)
            pdfPrint.setOrientation(pdfPrint.Portrait)

            pdfPrint.setPaperSize(QtCore.QSizeF(
                self.currentPageSize[0], self.currentPageSize[1]), QtPrintSupport.QPrinter.Millimeter)
            pdfPrint.setFullPage(True)
            pdfPrint.setColorMode(pdfPrint.GrayScale)
            pdfPainter = QtGui.QPainter()
            pdfPainter.begin(pdfPrint)

        self.start_merge()
        first = True
        self.labelInProgress = True
        # Start merging!
        count = 0
        if self.ui.individualPdfs.isChecked() and method == "PDF":

            length = len(self.mergeDataSet)
            zipFilename = os.path.splitext(self.currentFile)[
                0] + ("_%d_labels.zip" % length)
            archive = zipfile.ZipFile(zipFilename, "w")

        splitCount = self.ui.splitByRollAmount.value()
        splitOn = self.ui.SplitByRoll.isChecked()
        labelFont = QtGui.QFont('Arial')
        labelFont.setBold(True)
        labelFont.setPointSize(20)
        labelCount = int(math.ceil(len(self.dataSet) / float(splitCount)))
        endLabel = QtWidgets.QLabel("")
        endLabel.setStyleSheet(
            'QLabel {background-color : white; color : black;}')
        endLabel.setFont(labelFont)
        endLabel.setAlignment(QtCore.Qt.AlignCenter)
        endLabel.setSizePolicy(QtGui.QSizePolicy.Fixed,
                               QtGui.QSizePolicy.Fixed)
        endLabel.setMinimumHeight(self.currentPageSize[1]*self.dpmm[1])
        endLabel.setMaximumHeight(self.currentPageSize[1]*self.dpmm[1])
        endLabel.setMinimumWidth(self.currentPageSize[0]*self.dpmm[0])
        endLabel.setMaximumWidth(self.currentPageSize[0]*self.dpmm[0])
        endLabel.setWordWrap(True)

        currentRoll = 1

        for row in self.mergeDataSet:
            if self.ui.individualPdfs.isChecked() and method == "PDF":

                outputName = os.path.split(self.currentFile)[
                    0] + "\\" + self.merge_value(self.ui.pdfNameFormat.text(), row)

                pdfPrint = QtPrintSupport.QPrinter()
                pdfPrint.setOutputFileName(outputName)
                pdfPrint.setOrientation(pdfPrint.Portrait)

                pdfPrint.setPaperSize(QtCore.QSizeF(
                    self.currentPageSize[0], self.currentPageSize[1]), QtPrintSupport.QPrinter.Millimeter)
                pdfPrint.setFullPage(True)
                pdfPrint.setColorMode(pdfPrint.GrayScale)
                pdfPainter = QtGui.QPainter()
                pdfPainter.begin(pdfPrint)
                first = True

            if method == "PRINT" and count % splitCount == 0 and count != 0 and splitOn:
                if rollLabels:
                    text = "%s\n%s\nRoll %d of %d" % (self.rollLabelUi.jobNo.text(),
                                                      self.rollLabelUi.jobName.text(), currentRoll, labelCount)
                    self.printer.newPage()
                    endLabel.setText(text)
                    endLabel.render(painter)
                    painter.end()

                if count != len(self.dataSet)-1:
                    QtWidgets.QMessageBox.information(self.MainWindow, "Roll %d Complete" % currentRoll,
                                                  "Roll %d has finished sending to the printer, press OK to continue print" % currentRoll)
                currentRoll += 1
                painter = QtGui.QPainter()
                painter.begin(self.printer)
                first = True
            count += 1
            self.processEvents()
            self.merge_row(row)

            #copies = self.ui.copyCount.value()
            copies = 1
            if self.ui.copyUseField.isChecked():
                # use field in the database if asked to
                copies = int(row[str(self.ui.copyField.currentText())])
            # Repeat for as many copies as needed
            for _ in range(copies):
                # If this is not the first time looping, make sure to call "newPage" on the printer
                # the printer variable tells us if we are printing to a "Printer" as well as a PDF
                if first:
                    first = False
                else:
                    if method == "PRINT":
                        self.printer.newPage()
                    pdfPrint.newPage()

                if method == "PRINT":
                    self.labelView.scene().render(painter)

                self.labelView.scene().render(pdfPainter)
            self.increment_progress_bar()
            if not self.labelInProgress:
                if self.ui.individualPdfs.isChecked() and method == "PDF":
                    pdfPainter.end()
                    os.remove(outputName)
                # If at any point the merging is canceled, this will break the merge loop.
                break
            self.currentRecordNumber += 1

            if self.ui.individualPdfs.isChecked() and method == "PDF":
                pdfPainter.end()
                archive.write(outputName, os.path.split(outputName)[1])
                os.remove(outputName)

        if self.ui.individualPdfs.isChecked() and method == "PDF":
            archive.close()

        if method == "PRINT":
            if rollLabels:
                text = "%s\n%s\nRoll %d of %d" % (self.rollLabelUi.jobNo.text(),
                                                  self.rollLabelUi.jobName.text(), currentRoll, labelCount)
                self.printer.newPage()
                endLabel.setText(text)
                endLabel.render(painter)
                painter.end()

        # Clean up merging
        self.end_merge()

        if method == "PRINT":
            painter.end()
        if not self.ui.individualPdfs.isChecked():
            pdfPainter.end()
        self.end_progress_window()
        self.labelView.setVisible(True)
        # self.MainWindow.show()

        # Restore state of widget
        self.labelView.show_bg()
        self.ui.previewCheck.setChecked(previewState)
        s = self.sessionMaker()
        res = s.query(tables.Layout).filter(
            tables.Layout.name == self.currentLayout.name).first()
        res.printed()
        s.commit()

        self.refresh_layout_list()


if __name__ == '__main__':
    MainApp = Labeler([])
    sys.exit(MainApp.exec_())
    shutdownJVM()
