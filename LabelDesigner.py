# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Captain\workspace\Labeler\LabelDesigner.ui'
#
# Created: Thu Jun 14 18:28:49 2012
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
        self.imagePreview = QtGui.QGraphicsView(self.centralwidget)
        self.imagePreview.setGeometry(QtCore.QRect(370, 40, 400, 500))
        self.imagePreview.setInteractive(True)
        self.imagePreview.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.imagePreview.setObjectName(_fromUtf8("imagePreview"))
        self.addTextBtn = QtGui.QPushButton(self.centralwidget)
        self.addTextBtn.setGeometry(QtCore.QRect(50, 200, 75, 23))
        self.addTextBtn.setText(QtGui.QApplication.translate("MainWindow", "Add Text", None, QtGui.QApplication.UnicodeUTF8))
        self.addTextBtn.setObjectName(_fromUtf8("addTextBtn"))
        self.createPdfBtn = QtGui.QPushButton(self.centralwidget)
        self.createPdfBtn.setGeometry(QtCore.QRect(60, 240, 75, 23))
        self.createPdfBtn.setText(QtGui.QApplication.translate("MainWindow", "Create PDF", None, QtGui.QApplication.UnicodeUTF8))
        self.createPdfBtn.setObjectName(_fromUtf8("createPdfBtn"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 794, 21))
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

