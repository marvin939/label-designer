# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.6 (v3.6.6:4cf1f54eb7, Jun 27 2018, 02:47:15) [MSC v.1900 32 bit (Intel)]
# Embedded file name: \\pldatafile01\data\misc\labeldesigner\LabelDesigner.py
# Compiled at: 2020-03-04 11:56:02
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8('MainWindow'))
        MainWindow.resize(1218, 891)
        MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8('centralwidget'))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_4.setObjectName(_fromUtf8('verticalLayout_4'))
        self.frame = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8('frame'))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8('horizontalLayout_4'))
        self.groupBox_4 = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setObjectName(_fromUtf8('groupBox_4'))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_8.setObjectName(_fromUtf8('verticalLayout_8'))
        self.headerList = QtGui.QTableWidget(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headerList.sizePolicy().hasHeightForWidth())
        self.headerList.setSizePolicy(sizePolicy)
        self.headerList.setMinimumSize(QtCore.QSize(300, 0))
        self.headerList.setEditTriggers(QtGui.QAbstractItemView.EditKeyPressed)
        self.headerList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.headerList.setObjectName(_fromUtf8('headerList'))
        self.headerList.setColumnCount(0)
        self.headerList.setRowCount(0)
        self.headerList.verticalHeader().setVisible(False)
        self.verticalLayout_8.addWidget(self.headerList)
        self.horizontalLayout_4.addWidget(self.groupBox_4)
        self.groupBox_3 = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setFlat(False)
        self.groupBox_3.setObjectName(_fromUtf8('groupBox_3'))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_7.setObjectName(_fromUtf8('horizontalLayout_7'))
        self.verticalLayout_10 = QtGui.QVBoxLayout()
        self.verticalLayout_10.setObjectName(_fromUtf8('verticalLayout_10'))
        self.layoutList = QtGui.QListWidget(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layoutList.sizePolicy().hasHeightForWidth())
        self.layoutList.setSizePolicy(sizePolicy)
        self.layoutList.setMinimumSize(QtCore.QSize(500, 250))
        self.layoutList.setObjectName(_fromUtf8('layoutList'))
        self.verticalLayout_10.addWidget(self.layoutList)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8('horizontalLayout_8'))
        self.filterLabel = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterLabel.sizePolicy().hasHeightForWidth())
        self.filterLabel.setSizePolicy(sizePolicy)
        self.filterLabel.setObjectName(_fromUtf8('filterLabel'))
        self.horizontalLayout_8.addWidget(self.filterLabel)
        self.filterEdit = QtGui.QLineEdit(self.groupBox_3)
        self.filterEdit.setObjectName(_fromUtf8('filterEdit'))
        self.horizontalLayout_8.addWidget(self.filterEdit)
        self.dateSort = QtGui.QCheckBox(self.groupBox_3)
        self.dateSort.setObjectName(_fromUtf8('dateSort'))
        self.horizontalLayout_8.addWidget(self.dateSort)
        self.verticalLayout_10.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7.addLayout(self.verticalLayout_10)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8('verticalLayout_6'))
        self.loadLayout = QtGui.QPushButton(self.groupBox_3)
        self.loadLayout.setObjectName(_fromUtf8('loadLayout'))
        self.verticalLayout_6.addWidget(self.loadLayout)
        self.saveLayout = QtGui.QPushButton(self.groupBox_3)
        self.saveLayout.setObjectName(_fromUtf8('saveLayout'))
        self.verticalLayout_6.addWidget(self.saveLayout)
        self.renameLayout = QtGui.QPushButton(self.groupBox_3)
        self.renameLayout.setObjectName(_fromUtf8('renameLayout'))
        self.verticalLayout_6.addWidget(self.renameLayout)
        self.refreshLayoutList = QtGui.QPushButton(self.groupBox_3)
        self.refreshLayoutList.setObjectName(_fromUtf8('refreshLayoutList'))
        self.verticalLayout_6.addWidget(self.refreshLayoutList)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem)
        self.removeLayout = QtGui.QPushButton(self.groupBox_3)
        self.removeLayout.setObjectName(_fromUtf8('removeLayout'))
        self.verticalLayout_6.addWidget(self.removeLayout)
        self.clearFilter = QtGui.QPushButton(self.groupBox_3)
        self.clearFilter.setObjectName(_fromUtf8('clearFilter'))
        self.verticalLayout_6.addWidget(self.clearFilter)
        self.horizontalLayout_7.addLayout(self.verticalLayout_6)
        self.horizontalLayout_4.addWidget(self.groupBox_3)
        self.groupBox_2 = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName(_fromUtf8('groupBox_2'))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setObjectName(_fromUtf8('verticalLayout_5'))
        self.createPdfBtn = QtGui.QPushButton(self.groupBox_2)
        self.createPdfBtn.setObjectName(_fromUtf8('createPdfBtn'))
        self.verticalLayout_5.addWidget(self.createPdfBtn)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8('horizontalLayout_10'))
        self.printButton = QtGui.QPushButton(self.groupBox_2)
        self.printButton.setObjectName(_fromUtf8('printButton'))
        self.horizontalLayout_10.addWidget(self.printButton)
        self.pageSetup = QtGui.QPushButton(self.groupBox_2)
        self.pageSetup.setObjectName(_fromUtf8('pageSetup'))
        self.horizontalLayout_10.addWidget(self.pageSetup)
        self.verticalLayout_5.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8('horizontalLayout_13'))
        self.averyRadio = QtGui.QRadioButton(self.groupBox_2)
        self.averyRadio.setChecked(False)
        self.averyRadio.setAutoRepeat(False)
        self.averyRadio.setObjectName(_fromUtf8('averyRadio'))
        self.printerSelectGroup = QtGui.QButtonGroup(MainWindow)
        self.printerSelectGroup.setObjectName(_fromUtf8('printerSelectGroup'))
        self.printerSelectGroup.addButton(self.averyRadio)
        self.horizontalLayout_13.addWidget(self.averyRadio)
        self.zebraRadio = QtGui.QRadioButton(self.groupBox_2)
        self.zebraRadio.setChecked(True)
        self.zebraRadio.setObjectName(_fromUtf8('zebraRadio'))
        self.printerSelectGroup.addButton(self.zebraRadio)
        self.horizontalLayout_13.addWidget(self.zebraRadio)
        self.verticalLayout_5.addLayout(self.horizontalLayout_13)
        self.line = QtGui.QFrame(self.groupBox_2)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8('line'))
        self.verticalLayout_5.addWidget(self.line)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8('horizontalLayout_6'))
        self.useSubset = QtGui.QCheckBox(self.groupBox_2)
        self.useSubset.setObjectName(_fromUtf8('useSubset'))
        self.horizontalLayout_6.addWidget(self.useSubset)
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName(_fromUtf8('label_4'))
        self.horizontalLayout_6.addWidget(self.label_4)
        self.subsetBottom = QtGui.QSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subsetBottom.sizePolicy().hasHeightForWidth())
        self.subsetBottom.setSizePolicy(sizePolicy)
        self.subsetBottom.setObjectName(_fromUtf8('subsetBottom'))
        self.horizontalLayout_6.addWidget(self.subsetBottom)
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setObjectName(_fromUtf8('label_5'))
        self.horizontalLayout_6.addWidget(self.label_5)
        self.subsetTop = QtGui.QSpinBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subsetTop.sizePolicy().hasHeightForWidth())
        self.subsetTop.setSizePolicy(sizePolicy)
        self.subsetTop.setObjectName(_fromUtf8('subsetTop'))
        self.horizontalLayout_6.addWidget(self.subsetTop)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.line_2 = QtGui.QFrame(self.groupBox_2)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8('line_2'))
        self.verticalLayout_5.addWidget(self.line_2)
        self.horizontalLayout_16 = QtGui.QHBoxLayout()
        self.horizontalLayout_16.setObjectName(_fromUtf8('horizontalLayout_16'))
        self.SplitByRoll = QtGui.QCheckBox(self.groupBox_2)
        self.SplitByRoll.setChecked(True)
        self.SplitByRoll.setObjectName(_fromUtf8('SplitByRoll'))
        self.horizontalLayout_16.addWidget(self.SplitByRoll)
        self.splitByRollAmount = QtGui.QSpinBox(self.groupBox_2)
        self.splitByRollAmount.setMinimum(1)
        self.splitByRollAmount.setMaximum(999999)
        self.splitByRollAmount.setObjectName(_fromUtf8('splitByRollAmount'))
        self.horizontalLayout_16.addWidget(self.splitByRollAmount)
        self.verticalLayout_5.addLayout(self.horizontalLayout_16)
        self.line_3 = QtGui.QFrame(self.groupBox_2)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8('line_3'))
        self.verticalLayout_5.addWidget(self.line_3)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8('horizontalLayout_5'))
        self.copyUseField = QtGui.QCheckBox(self.groupBox_2)
        self.copyUseField.setObjectName(_fromUtf8('copyUseField'))
        self.horizontalLayout_5.addWidget(self.copyUseField)
        self.copyField = QtGui.QComboBox(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copyField.sizePolicy().hasHeightForWidth())
        self.copyField.setSizePolicy(sizePolicy)
        self.copyField.setObjectName(_fromUtf8('copyField'))
        self.horizontalLayout_5.addWidget(self.copyField)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8('horizontalLayout_11'))
        self.genSamples = QtGui.QCheckBox(self.groupBox_2)
        self.genSamples.setObjectName(_fromUtf8('genSamples'))
        self.horizontalLayout_11.addWidget(self.genSamples)
        self.label_6 = QtGui.QLabel(self.groupBox_2)
        self.label_6.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName(_fromUtf8('label_6'))
        self.horizontalLayout_11.addWidget(self.label_6)
        self.sampleCount = QtGui.QSpinBox(self.groupBox_2)
        self.sampleCount.setMinimum(1)
        self.sampleCount.setMaximum(99999999)
        self.sampleCount.setObjectName(_fromUtf8('sampleCount'))
        self.horizontalLayout_11.addWidget(self.sampleCount)
        self.verticalLayout_5.addLayout(self.horizontalLayout_11)
        self.verticalLayout_11 = QtGui.QVBoxLayout()
        self.verticalLayout_11.setObjectName(_fromUtf8('verticalLayout_11'))
        self.individualPdfs = QtGui.QCheckBox(self.groupBox_2)
        self.individualPdfs.setObjectName(_fromUtf8('individualPdfs'))
        self.verticalLayout_11.addWidget(self.individualPdfs)
        self.horizontalLayout_15 = QtGui.QHBoxLayout()
        self.horizontalLayout_15.setObjectName(_fromUtf8('horizontalLayout_15'))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8('label_2'))
        self.horizontalLayout_15.addWidget(self.label_2)
        self.pdfNameFormat = QtGui.QLineEdit(self.groupBox_2)
        self.pdfNameFormat.setObjectName(_fromUtf8('pdfNameFormat'))
        self.horizontalLayout_15.addWidget(self.pdfNameFormat)
        self.verticalLayout_11.addLayout(self.horizontalLayout_15)
        self.verticalLayout_5.addLayout(self.verticalLayout_11)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.horizontalLayout_4.addWidget(self.groupBox_2)
        self.verticalLayout_4.addWidget(self.frame)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8('horizontalLayout_9'))
        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8('splitter_2'))
        self.layoutWidget = QtGui.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(_fromUtf8('layoutWidget'))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8('verticalLayout_3'))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8('gridLayout'))
        self.headersCheck = QtGui.QCheckBox(self.layoutWidget)
        self.headersCheck.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.headersCheck.setObjectName(_fromUtf8('headersCheck'))
        self.gridLayout.addWidget(self.headersCheck, 11, 0, 1, 1)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8('horizontalLayout_12'))
        self.previewCheck = QtGui.QCheckBox(self.layoutWidget)
        self.previewCheck.setObjectName(_fromUtf8('previewCheck'))
        self.horizontalLayout_12.addWidget(self.previewCheck)
        self.label_7 = QtGui.QLabel(self.layoutWidget)
        self.label_7.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName(_fromUtf8('label_7'))
        self.horizontalLayout_12.addWidget(self.label_7)
        self.previewRecord = QtGui.QSpinBox(self.layoutWidget)
        self.previewRecord.setObjectName(_fromUtf8('previewRecord'))
        self.horizontalLayout_12.addWidget(self.previewRecord)
        self.gridLayout.addLayout(self.horizontalLayout_12, 16, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8('horizontalLayout'))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8('label'))
        self.horizontalLayout.addWidget(self.label)
        self.zoomLevel = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.zoomLevel.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.zoomLevel.setMinimum(10.0)
        self.zoomLevel.setMaximum(1600.0)
        self.zoomLevel.setSingleStep(5.0)
        self.zoomLevel.setProperty('value', 100.0)
        self.zoomLevel.setObjectName(_fromUtf8('zoomLevel'))
        self.horizontalLayout.addWidget(self.zoomLevel)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.createCartonLabels = QtGui.QPushButton(self.layoutWidget)
        self.createCartonLabels.setObjectName(_fromUtf8('createCartonLabels'))
        self.gridLayout.addWidget(self.createCartonLabels, 1, 0, 1, 1)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8('horizontalLayout_14'))
        self.loadData = QtGui.QPushButton(self.layoutWidget)
        self.loadData.setObjectName(_fromUtf8('loadData'))
        self.horizontalLayout_14.addWidget(self.loadData)
        self.clearData = QtGui.QPushButton(self.layoutWidget)
        self.clearData.setObjectName(_fromUtf8('clearData'))
        self.horizontalLayout_14.addWidget(self.clearData)
        self.gridLayout.addLayout(self.horizontalLayout_14, 3, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8('horizontalLayout_2'))
        self.permitCheck = QtGui.QCheckBox(self.layoutWidget)
        self.permitCheck.setObjectName(_fromUtf8('permitCheck'))
        self.horizontalLayout_2.addWidget(self.permitCheck)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName(_fromUtf8('label_3'))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.permitEntry = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.permitEntry.sizePolicy().hasHeightForWidth())
        self.permitEntry.setSizePolicy(sizePolicy)
        self.permitEntry.setMaxLength(7)
        self.permitEntry.setObjectName(_fromUtf8('permitEntry'))
        self.horizontalLayout_2.addWidget(self.permitEntry)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8('horizontalLayout_3'))
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        
        # Add "100% Recyclable Packaging" textbox.
        self.recyclablePackagingCheck = QtGui.QCheckBox("100% Recyclable Packaging in Soft Plastics", parent=self.layoutWidget)
        self.verticalLayout_3.addWidget(self.recyclablePackagingCheck)
        self.recyclablePackagingCheck.setCheckState(Qt.Checked)
        
        self.returnCheck = QtGui.QCheckBox(self.layoutWidget)
        self.returnCheck.setObjectName(_fromUtf8('returnCheck'))
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
        self.returnAddress.setObjectName(_fromUtf8('returnAddress'))
        self.verticalLayout_3.addWidget(self.returnAddress)
        self.groupBox = QtGui.QGroupBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox.setObjectName(_fromUtf8('groupBox'))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8('gridLayout_2'))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem3, 4, 0, 1, 1)
        self.addText = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addText.sizePolicy().hasHeightForWidth())
        self.addText.setSizePolicy(sizePolicy)
        self.addText.setMinimumSize(QtCore.QSize(100, 0))
        self.addText.setCheckable(True)
        self.addText.setObjectName(_fromUtf8('addText'))
        self.gridLayout_2.addWidget(self.addText, 0, 0, 1, 1)
        self.addBarcode = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addBarcode.sizePolicy().hasHeightForWidth())
        self.addBarcode.setSizePolicy(sizePolicy)
        self.addBarcode.setMinimumSize(QtCore.QSize(100, 0))
        self.addBarcode.setCheckable(True)
        self.addBarcode.setObjectName(_fromUtf8('addBarcode'))
        self.gridLayout_2.addWidget(self.addBarcode, 1, 0, 1, 1)
        self.addImage = QtGui.QPushButton(self.groupBox)
        self.addImage.setCheckable(True)
        self.addImage.setObjectName(_fromUtf8('addImage'))
        self.gridLayout_2.addWidget(self.addImage, 2, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem4)
        self.graphicsView = ZoomGraphicsView(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setMinimumSize(QtCore.QSize(0, 290))
        self.graphicsView.viewport().setProperty('cursor', QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.graphicsView.setObjectName(_fromUtf8('graphicsView'))
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter_2)
        self.verticalLayoutWidget.setObjectName(_fromUtf8('verticalLayoutWidget'))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_7.setMargin(0)
        self.verticalLayout_7.setObjectName(_fromUtf8('verticalLayout_7'))
        self.splitter = QtGui.QSplitter(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8('splitter'))
        self.itemList = QtGui.QTreeWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.itemList.sizePolicy().hasHeightForWidth())
        self.itemList.setSizePolicy(sizePolicy)
        self.itemList.setBaseSize(QtCore.QSize(0, 100))
        self.itemList.setObjectName(_fromUtf8('itemList'))
        self.itemList.headerItem().setText(0, _fromUtf8('Layout Items'))
        self.tabWidget = QtGui.QTabWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(350, 0))
        self.tabWidget.setBaseSize(QtCore.QSize(0, 500))
        self.tabWidget.setObjectName(_fromUtf8('tabWidget'))
        self.detailsTab = QtGui.QWidget()
        self.detailsTab.setObjectName(_fromUtf8('detailsTab'))
        self.verticalLayout = QtGui.QVBoxLayout(self.detailsTab)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8('verticalLayout'))
        self.objectPropertyArea = QtGui.QScrollArea(self.detailsTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.objectPropertyArea.sizePolicy().hasHeightForWidth())
        self.objectPropertyArea.setSizePolicy(sizePolicy)
        self.objectPropertyArea.setWidgetResizable(True)
        self.objectPropertyArea.setObjectName(_fromUtf8('objectPropertyArea'))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 342, 242))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8('scrollAreaWidgetContents'))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(_fromUtf8('verticalLayout_2'))
        self.objectProperties = QtGui.QFormLayout()
        self.objectProperties.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.objectProperties.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.objectProperties.setObjectName(_fromUtf8('objectProperties'))
        self.verticalLayout_2.addLayout(self.objectProperties)
        self.objectPropertyArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.objectPropertyArea)
        self.tabWidget.addTab(self.detailsTab, _fromUtf8(''))
        self.verticalLayout_7.addWidget(self.splitter)
        self.horizontalLayout_9.addWidget(self.splitter_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8('verticalLayout_9'))
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setObjectName(_fromUtf8('label_8'))
        self.verticalLayout_9.addWidget(self.label_8)
        self.logConsole = QtGui.QTextEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logConsole.sizePolicy().hasHeightForWidth())
        self.logConsole.setSizePolicy(sizePolicy)
        self.logConsole.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.logConsole.setReadOnly(True)
        self.logConsole.setObjectName(_fromUtf8('logConsole'))
        self.verticalLayout_9.addWidget(self.logConsole)
        self.verticalLayout_4.addLayout(self.verticalLayout_9)
        self.verticalLayout_4.setStretch(1, 2)
        self.verticalLayout_4.setStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1218, 21))
        self.menubar.setObjectName(_fromUtf8('menubar'))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8('statusbar'))
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        
        

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate('MainWindow', 'MainWindow', None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate('MainWindow', 'Headers', None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate('MainWindow', 'Layouts', None, QtGui.QApplication.UnicodeUTF8))
        self.filterLabel.setText(QtGui.QApplication.translate('MainWindow', 'Filter', None, QtGui.QApplication.UnicodeUTF8))
        self.dateSort.setText(QtGui.QApplication.translate('MainWindow', 'Sort by date', None, QtGui.QApplication.UnicodeUTF8))
        self.loadLayout.setText(QtGui.QApplication.translate('MainWindow', 'Load Layout', None, QtGui.QApplication.UnicodeUTF8))
        self.saveLayout.setText(QtGui.QApplication.translate('MainWindow', 'Save Layout', None, QtGui.QApplication.UnicodeUTF8))
        self.renameLayout.setText(QtGui.QApplication.translate('MainWindow', 'Rename Layout', None, QtGui.QApplication.UnicodeUTF8))
        self.refreshLayoutList.setText(QtGui.QApplication.translate('MainWindow', 'Refresh List', None, QtGui.QApplication.UnicodeUTF8))
        self.removeLayout.setText(QtGui.QApplication.translate('MainWindow', 'Remove Layout', None, QtGui.QApplication.UnicodeUTF8))
        self.clearFilter.setText(QtGui.QApplication.translate('MainWindow', 'Clear Filter', None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate('MainWindow', 'Print Options', None, QtGui.QApplication.UnicodeUTF8))
        self.createPdfBtn.setText(QtGui.QApplication.translate('MainWindow', 'Create PDF', None, QtGui.QApplication.UnicodeUTF8))
        self.printButton.setText(QtGui.QApplication.translate('MainWindow', 'Print', None, QtGui.QApplication.UnicodeUTF8))
        self.pageSetup.setText(QtGui.QApplication.translate('MainWindow', 'Page Setup', None, QtGui.QApplication.UnicodeUTF8))
        self.averyRadio.setText(QtGui.QApplication.translate('MainWindow', 'Avery', None, QtGui.QApplication.UnicodeUTF8))
        self.zebraRadio.setText(QtGui.QApplication.translate('MainWindow', 'Zebra', None, QtGui.QApplication.UnicodeUTF8))
        self.useSubset.setText(QtGui.QApplication.translate('MainWindow', 'Subset', None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate('MainWindow', 'From', None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate('MainWindow', 'To', None, QtGui.QApplication.UnicodeUTF8))
        self.SplitByRoll.setText(QtGui.QApplication.translate('MainWindow', 'Split By Amount:', None, QtGui.QApplication.UnicodeUTF8))
        self.copyUseField.setText(QtGui.QApplication.translate('MainWindow', 'Use Field for Copies', None, QtGui.QApplication.UnicodeUTF8))
        self.genSamples.setText(QtGui.QApplication.translate('MainWindow', 'Generate Samples', None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate('MainWindow', 'Amount:', None, QtGui.QApplication.UnicodeUTF8))
        self.individualPdfs.setText(QtGui.QApplication.translate('MainWindow', 'Individual PDFs?', None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setToolTip(QtGui.QApplication.translate('MainWindow', '<html><head/><body><p>Same convention as label variables.</p><p>    e.g.&quot;Staff_{Name}_{Seq}.pdf&quot;</p></body></html>', None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate('MainWindow', 'Naming Format', None, QtGui.QApplication.UnicodeUTF8))
        self.headersCheck.setText(QtGui.QApplication.translate('MainWindow', 'Has Headers?', None, QtGui.QApplication.UnicodeUTF8))
        self.previewCheck.setText(QtGui.QApplication.translate('MainWindow', 'Show Preview', None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate('MainWindow', 'Record:', None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate('MainWindow', 'Zoom:', None, QtGui.QApplication.UnicodeUTF8))
        self.createCartonLabels.setText(QtGui.QApplication.translate('MainWindow', 'Create Carton Labels', None, QtGui.QApplication.UnicodeUTF8))
        self.loadData.setText(QtGui.QApplication.translate('MainWindow', 'Load Data', None, QtGui.QApplication.UnicodeUTF8))
        self.clearData.setText(QtGui.QApplication.translate('MainWindow', 'Clear Data', None, QtGui.QApplication.UnicodeUTF8))
        self.permitCheck.setText(QtGui.QApplication.translate('MainWindow', 'Add Permit', None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate('MainWindow', 'Permit No.', None, QtGui.QApplication.UnicodeUTF8))
        self.returnCheck.setText(QtGui.QApplication.translate('MainWindow', 'Add Return Address?', None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate('MainWindow', 'Layup Items', None, QtGui.QApplication.UnicodeUTF8))
        self.addText.setText(QtGui.QApplication.translate('MainWindow', 'Add Text', None, QtGui.QApplication.UnicodeUTF8))
        self.addBarcode.setText(QtGui.QApplication.translate('MainWindow', 'Add Barcode', None, QtGui.QApplication.UnicodeUTF8))
        self.addImage.setText(QtGui.QApplication.translate('MainWindow', 'Add Image', None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.detailsTab), QtGui.QApplication.translate('MainWindow', 'Object Details', None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate('MainWindow', 'Log Console', None, QtGui.QApplication.UnicodeUTF8))
        return


from zoomgraphicsview import ZoomGraphicsView
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
# okay decompiling LabelDesigner.pyc
