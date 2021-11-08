# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PageSetup.ui'
#
# Created: Thu Mar 06 13:30:37 2014
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pageWidth = QtWidgets.QSpinBox(Dialog)
        self.pageWidth.setMinimum(1)
        self.pageWidth.setMaximum(9999)
        self.pageWidth.setObjectName(_fromUtf8("pageWidth"))
        self.gridLayout.addWidget(self.pageWidth, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.pageHeight = QtWidgets.QSpinBox(Dialog)
        self.pageHeight.setMinimum(1)
        self.pageHeight.setMaximum(9999)
        self.pageHeight.setObjectName(_fromUtf8("pageHeight"))
        self.gridLayout.addWidget(self.pageHeight, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

    def retranslateUi(self, Dialog):
#         Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Page Setup", None, QtGui.QApplication.UnicodeUTF8))
#         self.label.setText(QtGui.QApplication.translate("Dialog", "Page Width (mm)", None, QtGui.QApplication.UnicodeUTF8))
#         self.label_2.setText(QtGui.QApplication.translate("Dialog", "Page Height(mm)", None, QtGui.QApplication.UnicodeUTF8))
        Dialog.setWindowTitle("Page Setup")
        self.label.setText("Page Width (mm)")
        self.label_2.setText("Page Height(mm)")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
    #input()
    #app.exec_()
    

