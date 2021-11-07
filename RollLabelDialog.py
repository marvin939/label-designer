# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RollLabelDialog.ui'
#
# Created: Thu Aug 11 16:32:10 2016
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit, QDialogButtonBox

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(QDialog):
    def __init__(self):
        super().__init__()
    
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 147)
        Dialog.setModal(False)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.jobNo = QLineEdit(Dialog)
        self.jobNo.setObjectName(_fromUtf8("jobNo"))
        self.gridLayout.addWidget(self.jobNo, 1, 1, 1, 1)
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.jobName = QLineEdit(Dialog)
        self.jobName.setObjectName(_fromUtf8("jobName"))
        self.gridLayout.addWidget(self.jobName, 2, 1, 1, 1)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)

        self.retranslateUi(Dialog)
        # Old Python 2 code:
#         QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
#         QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
#         QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Marvin 7/11/2021: Just testing some...
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self, Dialog):
        #Dialog.setWindowTitle(QApplication.translate("Dialog", "Roll Labels", None, QApplication.UnicodeUTF8))
        Dialog.setWindowTitle("Roll Labels")
        self.label.setText("Job No")
        self.label_2.setText("Job Name")
        self.label_3.setText("Would you like to print roll labels? If so, enter below.")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

