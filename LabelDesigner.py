# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LabelDesigner.ui'
#
# Created: Fri Jun 15 17:58:22 2012
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
        MainWindow.resize(794, 600)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.addTextBtn = QtGui.QPushButton(self.centralwidget)
        self.addTextBtn.setText(QtGui.QApplication.translate("MainWindow", "Add Text", None, QtGui.QApplication.UnicodeUTF8))
        self.addTextBtn.setObjectName(_fromUtf8("addTextBtn"))
        self.gridLayout.addWidget(self.addTextBtn, 2, 0, 1, 1)
        self.createPdfBtn = QtGui.QPushButton(self.centralwidget)
        self.createPdfBtn.setText(QtGui.QApplication.translate("MainWindow", "Create PDF", None, QtGui.QApplication.UnicodeUTF8))
        self.createPdfBtn.setObjectName(_fromUtf8("createPdfBtn"))
        self.gridLayout.addWidget(self.createPdfBtn, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Zoom:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.zoomLevel = QtGui.QDoubleSpinBox(self.centralwidget)
        self.zoomLevel.setMinimum(10.0)
        self.zoomLevel.setMaximum(1000.0)
        self.zoomLevel.setProperty("value", 100.0)
        self.zoomLevel.setObjectName(_fromUtf8("zoomLevel"))
        self.horizontalLayout.addWidget(self.zoomLevel)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.objDetailsArea = QtGui.QScrollArea(self.centralwidget)
        self.objDetailsArea.setWidgetResizable(True)
        self.objDetailsArea.setObjectName(_fromUtf8("objDetailsArea"))
        self.detailsContents = QtGui.QWidget()
        self.detailsContents.setGeometry(QtCore.QRect(0, 0, 383, 454))
        self.detailsContents.setObjectName(_fromUtf8("detailsContents"))
        self.formLayout = QtGui.QFormLayout(self.detailsContents)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.objDetailsArea.setWidget(self.detailsContents)
        self.gridLayout_2.addWidget(self.objDetailsArea, 1, 0, 1, 1)
        self.previewLayout = QtGui.QVBoxLayout()
        self.previewLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.previewLayout.setObjectName(_fromUtf8("previewLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.previewLayout.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.previewLayout, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 794, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

