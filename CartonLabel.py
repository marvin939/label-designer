# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CartonLabel.ui'
#
# Created: Thu Mar 13 09:31:51 2014
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog:
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.totalQuantity = QtWidgets.QSpinBox(Dialog)
        self.totalQuantity.setMinimum(1)
        self.totalQuantity.setMaximum(999999999)
        self.totalQuantity.setObjectName(_fromUtf8("totalQuantity"))
        self.gridLayout.addWidget(self.totalQuantity, 6, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 7, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 13, 0, 1, 6)
        self.printlinkLogo = QtWidgets.QRadioButton(Dialog)
        self.printlinkLogo.setText(_fromUtf8(""))
        self.printlinkLogo.setChecked(True)
        self.printlinkLogo.setObjectName(_fromUtf8("printlinkLogo"))
        self.gridLayout.addWidget(self.printlinkLogo, 8, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)
        self.stockName = QtWidgets.QLineEdit(Dialog)
        self.stockName.setObjectName(_fromUtf8("stockName"))
        self.gridLayout.addWidget(self.stockName, 4, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 9, 0, 1, 1)
        self.noLogo = QtWidgets.QRadioButton(Dialog)
        self.noLogo.setText(_fromUtf8(""))
        self.noLogo.setObjectName(_fromUtf8("noLogo"))
        self.gridLayout.addWidget(self.noLogo, 10, 1, 1, 1)
        self.bluestarLogo = QtWidgets.QRadioButton(Dialog)
        self.bluestarLogo.setText(_fromUtf8(""))
        self.bluestarLogo.setObjectName(_fromUtf8("bluestarLogo"))
        self.gridLayout.addWidget(self.bluestarLogo, 9, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 8, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 10, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 12, 0, 1, 1)
        self.cartonQuantity = QtWidgets.QSpinBox(Dialog)
        self.cartonQuantity.setMinimum(1)
        self.cartonQuantity.setMaximum(999999999)
        self.cartonQuantity.setObjectName(_fromUtf8("cartonQuantity"))
        self.gridLayout.addWidget(self.cartonQuantity, 7, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 2)
        self.jobNo = QtWidgets.QLineEdit(Dialog)
        self.jobNo.setObjectName(_fromUtf8("jobNo"))
        self.gridLayout.addWidget(self.jobNo, 3, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 3, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 11, 0, 1, 1)
        self.largeLabel = QtWidgets.QCheckBox(Dialog)
        self.largeLabel.setText(_fromUtf8(""))
        self.largeLabel.setChecked(True)
        self.largeLabel.setObjectName(_fromUtf8("largeLabel"))
        self.gridLayout.addWidget(self.largeLabel, 11, 1, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        # QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        # QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.jobNo, self.stockName)
        Dialog.setTabOrder(self.stockName, self.totalQuantity)
        Dialog.setTabOrder(self.totalQuantity, self.cartonQuantity)
        Dialog.setTabOrder(self.cartonQuantity, self.printlinkLogo)
        Dialog.setTabOrder(self.printlinkLogo, self.bluestarLogo)
        Dialog.setTabOrder(self.bluestarLogo, self.noLogo)
        Dialog.setTabOrder(self.noLogo, self.buttonBox)

    def retranslateUi(self, Dialog):
        # Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Carton Labels", None, QtGui.QApplication.UnicodeUTF8))
        Dialog.setWindowTitle("Carton Labels")
        self.label_3.setText("Quantity Per Ctn.")
        self.label.setText("Stock Type / Name")
        self.label_2.setText("Total Quantity")
        self.label_5.setText("Bluestar Logo")
        self.label_4.setText("Printlink Logo")
        self.label_6.setText("No Logo")
        self.label_7.setText("Carton Label Creation")
        self.label_8.setText("Job No")
        self.label_9.setText("Large Label?")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

