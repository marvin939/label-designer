# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LabelDesigner.ui'
#
# Created: Tue Feb 26 13:35:01 2013
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1240, 684)
        MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.frame = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.groupBox = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 100))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.addBarcode = QtGui.QPushButton(self.groupBox)
        self.addBarcode.setCheckable(True)
        self.addBarcode.setObjectName(_fromUtf8("addBarcode"))
        self.gridLayout_2.addWidget(self.addBarcode, 2, 0, 1, 1)
        self.addText = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addText.sizePolicy().hasHeightForWidth())
        self.addText.setSizePolicy(sizePolicy)
        self.addText.setMinimumSize(QtCore.QSize(100, 0))
        self.addText.setCheckable(True)
        self.addText.setObjectName(_fromUtf8("addText"))
        self.gridLayout_2.addWidget(self.addText, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 3, 0, 1, 1)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.groupBox_3 = QtGui.QGroupBox(self.frame)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.layoutList = QtGui.QListWidget(self.groupBox_3)
        self.layoutList.setObjectName(_fromUtf8("layoutList"))
        self.horizontalLayout_7.addWidget(self.layoutList)
        self.horizontalLayout_4.addWidget(self.groupBox_3)
        self.groupBox_2 = QtGui.QGroupBox(self.frame)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.createPdfBtn = QtGui.QPushButton(self.groupBox_2)
        self.createPdfBtn.setObjectName(_fromUtf8("createPdfBtn"))
        self.verticalLayout_5.addWidget(self.createPdfBtn)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.printButton = QtGui.QPushButton(self.groupBox_2)
        self.printButton.setObjectName(_fromUtf8("printButton"))
        self.horizontalLayout_10.addWidget(self.printButton)
        self.printerList = QtGui.QComboBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.printerList.sizePolicy().hasHeightForWidth())
        self.printerList.setSizePolicy(sizePolicy)
        self.printerList.setObjectName(_fromUtf8("printerList"))
        self.horizontalLayout_10.addWidget(self.printerList)
        self.verticalLayout_5.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.useSubset = QtGui.QCheckBox(self.groupBox_2)
        self.useSubset.setObjectName(_fromUtf8("useSubset"))
        self.horizontalLayout_6.addWidget(self.useSubset)
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_6.addWidget(self.label_4)
        self.subsetBottom = QtGui.QSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subsetBottom.sizePolicy().hasHeightForWidth())
        self.subsetBottom.setSizePolicy(sizePolicy)
        self.subsetBottom.setObjectName(_fromUtf8("subsetBottom"))
        self.horizontalLayout_6.addWidget(self.subsetBottom)
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_6.addWidget(self.label_5)
        self.subsetTop = QtGui.QSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subsetTop.sizePolicy().hasHeightForWidth())
        self.subsetTop.setSizePolicy(sizePolicy)
        self.subsetTop.setObjectName(_fromUtf8("subsetTop"))
        self.horizontalLayout_6.addWidget(self.subsetTop)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_5.addWidget(self.label_2)
        self.copyCount = QtGui.QSpinBox(self.groupBox_2)
        self.copyCount.setMinimum(1)
        self.copyCount.setObjectName(_fromUtf8("copyCount"))
        self.horizontalLayout_5.addWidget(self.copyCount)
        self.copyUseField = QtGui.QCheckBox(self.groupBox_2)
        self.copyUseField.setObjectName(_fromUtf8("copyUseField"))
        self.horizontalLayout_5.addWidget(self.copyUseField)
        self.copyField = QtGui.QComboBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copyField.sizePolicy().hasHeightForWidth())
        self.copyField.setSizePolicy(sizePolicy)
        self.copyField.setObjectName(_fromUtf8("copyField"))
        self.horizontalLayout_5.addWidget(self.copyField)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.genSamples = QtGui.QCheckBox(self.groupBox_2)
        self.genSamples.setObjectName(_fromUtf8("genSamples"))
        self.horizontalLayout_11.addWidget(self.genSamples)
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_11.addWidget(self.label_6)
        self.sampleCount = QtGui.QSpinBox(self.groupBox_2)
        self.sampleCount.setMinimum(1)
        self.sampleCount.setObjectName(_fromUtf8("sampleCount"))
        self.horizontalLayout_11.addWidget(self.sampleCount)
        self.verticalLayout_5.addLayout(self.horizontalLayout_11)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        self.horizontalLayout_4.addWidget(self.groupBox_2)
        self.horizontalLayout_4.setStretch(0, 1)
        self.verticalLayout_4.addWidget(self.frame)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.layoutWidget = QtGui.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.zoomLevel = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.zoomLevel.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.zoomLevel.setMinimum(10.0)
        self.zoomLevel.setMaximum(1600.0)
        self.zoomLevel.setSingleStep(5.0)
        self.zoomLevel.setProperty("value", 100.0)
        self.zoomLevel.setObjectName(_fromUtf8("zoomLevel"))
        self.horizontalLayout.addWidget(self.zoomLevel)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.previewCheck = QtGui.QCheckBox(self.layoutWidget)
        self.previewCheck.setObjectName(_fromUtf8("previewCheck"))
        self.horizontalLayout_12.addWidget(self.previewCheck)
        self.label_7 = QtGui.QLabel(self.layoutWidget)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_12.addWidget(self.label_7)
        self.previewRecord = QtGui.QSpinBox(self.layoutWidget)
        self.previewRecord.setObjectName(_fromUtf8("previewRecord"))
        self.horizontalLayout_12.addWidget(self.previewRecord)
        self.gridLayout.addLayout(self.horizontalLayout_12, 7, 0, 1, 1)
        self.loadData = QtGui.QPushButton(self.layoutWidget)
        self.loadData.setObjectName(_fromUtf8("loadData"))
        self.gridLayout.addWidget(self.loadData, 1, 0, 1, 1)
        self.headersCheck = QtGui.QCheckBox(self.layoutWidget)
        self.headersCheck.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.headersCheck.setObjectName(_fromUtf8("headersCheck"))
        self.gridLayout.addWidget(self.headersCheck, 2, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.permitCheck = QtGui.QCheckBox(self.layoutWidget)
        self.permitCheck.setObjectName(_fromUtf8("permitCheck"))
        self.horizontalLayout_2.addWidget(self.permitCheck)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.permitEntry = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.permitEntry.sizePolicy().hasHeightForWidth())
        self.permitEntry.setSizePolicy(sizePolicy)
        self.permitEntry.setMaxLength(7)
        self.permitEntry.setObjectName(_fromUtf8("permitEntry"))
        self.horizontalLayout_2.addWidget(self.permitEntry)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.returnCheck = QtGui.QCheckBox(self.layoutWidget)
        self.returnCheck.setObjectName(_fromUtf8("returnCheck"))
        self.verticalLayout_3.addWidget(self.returnCheck)
        self.returnAddress = QtGui.QTextEdit(self.layoutWidget)
        self.returnAddress.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.returnAddress.sizePolicy().hasHeightForWidth())
        self.returnAddress.setSizePolicy(sizePolicy)
        self.returnAddress.setMinimumSize(QtCore.QSize(0, 75))
        self.returnAddress.setMaximumSize(QtCore.QSize(16777215, 75))
        self.returnAddress.setObjectName(_fromUtf8("returnAddress"))
        self.verticalLayout_3.addWidget(self.returnAddress)
        self.label_8 = QtGui.QLabel(self.layoutWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout_3.addWidget(self.label_8)
        self.logConsole = QtGui.QTextEdit(self.layoutWidget)
        self.logConsole.setReadOnly(True)
        self.logConsole.setObjectName(_fromUtf8("logConsole"))
        self.verticalLayout_3.addWidget(self.logConsole)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.graphicsView = ZoomGraphicsView(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter_2)
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_7.setMargin(0)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.splitter = QtGui.QSplitter(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.itemList = QtGui.QTreeWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.itemList.sizePolicy().hasHeightForWidth())
        self.itemList.setSizePolicy(sizePolicy)
        self.itemList.setBaseSize(QtCore.QSize(0, 100))
        self.itemList.setObjectName(_fromUtf8("itemList"))
        self.itemList.headerItem().setText(0, _fromUtf8("1"))
        self.tabWidget = QtGui.QTabWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(300, 0))
        self.tabWidget.setBaseSize(QtCore.QSize(0, 500))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.detailsTab = QtGui.QWidget()
        self.detailsTab.setObjectName(_fromUtf8("detailsTab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.detailsTab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scrollArea = QtGui.QScrollArea(self.detailsTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 292, 100))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.objectProperties = QtGui.QFormLayout()
        self.objectProperties.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.objectProperties.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.objectProperties.setObjectName(_fromUtf8("objectProperties"))
        self.verticalLayout_2.addLayout(self.objectProperties)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.tabWidget.addTab(self.detailsTab, _fromUtf8(""))
        self.verticalLayout_7.addWidget(self.splitter)
        self.headerList = QtGui.QTableWidget(self.verticalLayoutWidget)
        self.headerList.setEditTriggers(QtGui.QAbstractItemView.EditKeyPressed)
        self.headerList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.headerList.setObjectName(_fromUtf8("headerList"))
        self.headerList.setColumnCount(0)
        self.headerList.setRowCount(0)
        self.headerList.verticalHeader().setVisible(False)
        self.verticalLayout_7.addWidget(self.headerList)
        self.horizontalLayout_9.addWidget(self.splitter_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)
        self.verticalLayout_4.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1240, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Layup Items", None, QtGui.QApplication.UnicodeUTF8))
        self.addBarcode.setText(QtGui.QApplication.translate("MainWindow", "Add Barcode", None, QtGui.QApplication.UnicodeUTF8))
        self.addText.setText(QtGui.QApplication.translate("MainWindow", "Add Text", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("MainWindow", "Layouts", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Print Options", None, QtGui.QApplication.UnicodeUTF8))
        self.createPdfBtn.setText(QtGui.QApplication.translate("MainWindow", "Create PDF", None, QtGui.QApplication.UnicodeUTF8))
        self.printButton.setText(QtGui.QApplication.translate("MainWindow", "Print", None, QtGui.QApplication.UnicodeUTF8))
        self.useSubset.setText(QtGui.QApplication.translate("MainWindow", "Subset", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "From", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "To", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Copies", None, QtGui.QApplication.UnicodeUTF8))
        self.copyUseField.setText(QtGui.QApplication.translate("MainWindow", "Use Field", None, QtGui.QApplication.UnicodeUTF8))
        self.genSamples.setText(QtGui.QApplication.translate("MainWindow", "Generate Samples", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Amount:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Zoom:", None, QtGui.QApplication.UnicodeUTF8))
        self.previewCheck.setText(QtGui.QApplication.translate("MainWindow", "Show Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Record:", None, QtGui.QApplication.UnicodeUTF8))
        self.loadData.setText(QtGui.QApplication.translate("MainWindow", "Load Data", None, QtGui.QApplication.UnicodeUTF8))
        self.headersCheck.setText(QtGui.QApplication.translate("MainWindow", "Has Headers?", None, QtGui.QApplication.UnicodeUTF8))
        self.permitCheck.setText(QtGui.QApplication.translate("MainWindow", "Add Permit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Permit No.", None, QtGui.QApplication.UnicodeUTF8))
        self.returnCheck.setText(QtGui.QApplication.translate("MainWindow", "Add Return Address?", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Log Console", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.detailsTab), QtGui.QApplication.translate("MainWindow", "Object Details", None, QtGui.QApplication.UnicodeUTF8))

from zoomgraphicsview import ZoomGraphicsView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

