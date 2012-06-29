# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LabelDesigner.ui'
#
# Created: Fri Jun 29 16:31:47 2012
#      by: PyQt4 UI code generator 4.8.5
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
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.headersCheck = QtGui.QCheckBox(self.centralwidget)
        self.headersCheck.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.headersCheck.setText(QtGui.QApplication.translate("MainWindow", "Has Headers?", None, QtGui.QApplication.UnicodeUTF8))
        self.headersCheck.setObjectName(_fromUtf8("headersCheck"))
        self.gridLayout_2.addWidget(self.headersCheck, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.permitCheck = QtGui.QCheckBox(self.centralwidget)
        self.permitCheck.setText(QtGui.QApplication.translate("MainWindow", "Add Permit", None, QtGui.QApplication.UnicodeUTF8))
        self.permitCheck.setObjectName(_fromUtf8("permitCheck"))
        self.horizontalLayout_2.addWidget(self.permitCheck)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Position", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.permitPosition = QtGui.QComboBox(self.centralwidget)
        self.permitPosition.setObjectName(_fromUtf8("permitPosition"))
        self.horizontalLayout_2.addWidget(self.permitPosition)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Zoom:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.zoomLevel = QtGui.QDoubleSpinBox(self.centralwidget)
        self.zoomLevel.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        self.zoomLevel.setMinimum(10.0)
        self.zoomLevel.setMaximum(1600.0)
        self.zoomLevel.setSingleStep(5.0)
        self.zoomLevel.setProperty("value", 100.0)
        self.zoomLevel.setObjectName(_fromUtf8("zoomLevel"))
        self.horizontalLayout.addWidget(self.zoomLevel)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.createPdfBtn = QtGui.QPushButton(self.centralwidget)
        self.createPdfBtn.setText(QtGui.QApplication.translate("MainWindow", "Create PDF", None, QtGui.QApplication.UnicodeUTF8))
        self.createPdfBtn.setObjectName(_fromUtf8("createPdfBtn"))
        self.gridLayout.addWidget(self.createPdfBtn, 1, 0, 1, 1)
        self.addTextBtn = QtGui.QPushButton(self.centralwidget)
        self.addTextBtn.setText(QtGui.QApplication.translate("MainWindow", "Add Text", None, QtGui.QApplication.UnicodeUTF8))
        self.addTextBtn.setObjectName(_fromUtf8("addTextBtn"))
        self.gridLayout.addWidget(self.addTextBtn, 2, 0, 1, 1)
        self.loadData = QtGui.QPushButton(self.centralwidget)
        self.loadData.setText(QtGui.QApplication.translate("MainWindow", "Load Data", None, QtGui.QApplication.UnicodeUTF8))
        self.loadData.setObjectName(_fromUtf8("loadData"))
        self.gridLayout.addWidget(self.loadData, 3, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.previewLayout = QtGui.QVBoxLayout()
        self.previewLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.previewLayout.setObjectName(_fromUtf8("previewLayout"))
        self.graphicsView = ZoomGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.previewLayout.addWidget(self.graphicsView)
        self.gridLayout_2.addLayout(self.previewLayout, 4, 1, 3, 1)
        self.itemList = QtGui.QTreeWidget(self.centralwidget)
        self.itemList.setObjectName(_fromUtf8("itemList"))
        self.itemList.headerItem().setText(0, _fromUtf8("1"))
        self.gridLayout_2.addWidget(self.itemList, 4, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Permit No.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.permitEntry = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.permitEntry.sizePolicy().hasHeightForWidth())
        self.permitEntry.setSizePolicy(sizePolicy)
        self.permitEntry.setMaxLength(7)
        self.permitEntry.setObjectName(_fromUtf8("permitEntry"))
        self.horizontalLayout_3.addWidget(self.permitEntry)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)
        self.itemDetails = QtGui.QListWidget(self.centralwidget)
        self.itemDetails.setEnabled(True)
        self.itemDetails.setModelColumn(0)
        self.itemDetails.setObjectName(_fromUtf8("itemDetails"))
        self.gridLayout_2.addWidget(self.itemDetails, 5, 0, 1, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1240, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass

from zoomgraphicsview import ZoomGraphicsView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

