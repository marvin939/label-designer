# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CartonLabel.ui'
#
# Created: Thu Mar 13 09:31:51 2014
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.totalQuantity = QtGui.QSpinBox(Dialog)
        self.totalQuantity.setMinimum(1)
        self.totalQuantity.setMaximum(999999999)
        self.totalQuantity.setObjectName(_fromUtf8("totalQuantity"))
        self.gridLayout.addWidget(self.totalQuantity, 6, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 13, 0, 1, 6)
        self.printlinkLogo = QtGui.QRadioButton(Dialog)
        self.printlinkLogo.setText(_fromUtf8(""))
        self.printlinkLogo.setChecked(True)
        self.printlinkLogo.setObjectName(_fromUtf8("printlinkLogo"))
        self.gridLayout.addWidget(self.printlinkLogo, 8, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)
        self.stockName = QtGui.QLineEdit(Dialog)
        self.stockName.setObjectName(_fromUtf8("stockName"))
        self.gridLayout.addWidget(self.stockName, 4, 1, 1, 1)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 9, 0, 1, 1)
        self.noLogo = QtGui.QRadioButton(Dialog)
        self.noLogo.setText(_fromUtf8(""))
        self.noLogo.setObjectName(_fromUtf8("noLogo"))
        self.gridLayout.addWidget(self.noLogo, 10, 1, 1, 1)
        self.bluestarLogo = QtGui.QRadioButton(Dialog)
        self.bluestarLogo.setText(_fromUtf8(""))
        self.bluestarLogo.setObjectName(_fromUtf8("bluestarLogo"))
        self.gridLayout.addWidget(self.bluestarLogo, 9, 1, 1, 1)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 8, 0, 1, 1)
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 10, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 12, 0, 1, 1)
        self.cartonQuantity = QtGui.QSpinBox(Dialog)
        self.cartonQuantity.setMinimum(1)
        self.cartonQuantity.setMaximum(999999999)
        self.cartonQuantity.setObjectName(_fromUtf8("cartonQuantity"))
        self.gridLayout.addWidget(self.cartonQuantity, 7, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.label_7 = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 2)
        self.jobNo = QtGui.QLineEdit(Dialog)
        self.jobNo.setObjectName(_fromUtf8("jobNo"))
        self.gridLayout.addWidget(self.jobNo, 3, 1, 1, 1)
        self.label_8 = QtGui.QLabel(Dialog)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 11, 0, 1, 1)
        self.largeLabel = QtGui.QCheckBox(Dialog)
        self.largeLabel.setText(_fromUtf8(""))
        self.largeLabel.setChecked(True)
        self.largeLabel.setObjectName(_fromUtf8("largeLabel"))
        self.gridLayout.addWidget(self.largeLabel, 11, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.jobNo, self.stockName)
        Dialog.setTabOrder(self.stockName, self.totalQuantity)
        Dialog.setTabOrder(self.totalQuantity, self.cartonQuantity)
        Dialog.setTabOrder(self.cartonQuantity, self.printlinkLogo)
        Dialog.setTabOrder(self.printlinkLogo, self.bluestarLogo)
        Dialog.setTabOrder(self.bluestarLogo, self.noLogo)
        Dialog.setTabOrder(self.noLogo, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Carton Labels", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Quantity Per Ctn.", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Stock Type / Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Total Quantity", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Bluestar Logo", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Printlink Logo", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "No Logo", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "Carton Label Creation", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "Job No", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "Large Label?", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

