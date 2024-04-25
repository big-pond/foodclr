# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dlgperiod.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DlgPeriod(object):
    def setupUi(self, DlgPeriod):
        DlgPeriod.setObjectName("DlgPeriod")
        DlgPeriod.resize(380, 418)
        DlgPeriod.setMinimumSize(QtCore.QSize(380, 418))
        DlgPeriod.setMaximumSize(QtCore.QSize(380, 418))
        DlgPeriod.setWindowTitle("")
        self.buttonBox = QtWidgets.QDialogButtonBox(DlgPeriod)
        self.buttonBox.setGeometry(QtCore.QRect(30, 380, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.deStart = QtWidgets.QDateEdit(DlgPeriod)
        self.deStart.setGeometry(QtCore.QRect(140, 30, 90, 22))
        self.deStart.setObjectName("deStart")
        self.lbStartDate = QtWidgets.QLabel(DlgPeriod)
        self.lbStartDate.setGeometry(QtCore.QRect(20, 32, 60, 13))
        self.lbStartDate.setObjectName("lbStartDate")
        self.lbUser = QtWidgets.QLabel(DlgPeriod)
        self.lbUser.setGeometry(QtCore.QRect(30, 6, 261, 16))
        self.lbUser.setAlignment(QtCore.Qt.AlignCenter)
        self.lbUser.setObjectName("lbUser")
        self.label = QtWidgets.QLabel(DlgPeriod)
        self.label.setGeometry(QtCore.QRect(20, 62, 60, 13))
        self.label.setObjectName("label")
        self.sbHeight = QtWidgets.QSpinBox(DlgPeriod)
        self.sbHeight.setGeometry(QtCore.QRect(140, 60, 70, 22))
        self.sbHeight.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbHeight.setMinimum(50)
        self.sbHeight.setMaximum(250)
        self.sbHeight.setProperty("value", 170)
        self.sbHeight.setObjectName("sbHeight")
        self.sbWeight = QtWidgets.QDoubleSpinBox(DlgPeriod)
        self.sbWeight.setGeometry(QtCore.QRect(140, 90, 70, 22))
        self.sbWeight.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbWeight.setDecimals(1)
        self.sbWeight.setMinimum(20.0)
        self.sbWeight.setMaximum(300.0)
        self.sbWeight.setProperty("value", 80.0)
        self.sbWeight.setObjectName("sbWeight")
        self.label_2 = QtWidgets.QLabel(DlgPeriod)
        self.label_2.setGeometry(QtCore.QRect(20, 92, 60, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(DlgPeriod)
        self.label_3.setGeometry(QtCore.QRect(20, 122, 47, 13))
        self.label_3.setObjectName("label_3")
        self.cbActivity = QtWidgets.QComboBox(DlgPeriod)
        self.cbActivity.setGeometry(QtCore.QRect(140, 120, 231, 22))
        self.cbActivity.setObjectName("cbActivity")
        self.cbActivity.addItem("")
        self.cbActivity.addItem("")
        self.cbActivity.addItem("")
        self.cbActivity.addItem("")
        self.cbActivity.addItem("")
        self.label_4 = QtWidgets.QLabel(DlgPeriod)
        self.label_4.setGeometry(QtCore.QRect(30, 158, 320, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(DlgPeriod)
        self.label_5.setGeometry(QtCore.QRect(20, 182, 64, 13))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(DlgPeriod)
        self.label_6.setGeometry(QtCore.QRect(20, 272, 71, 13))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(DlgPeriod)
        self.label_7.setGeometry(QtCore.QRect(20, 212, 64, 13))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(DlgPeriod)
        self.label_8.setGeometry(QtCore.QRect(20, 242, 97, 13))
        self.label_8.setObjectName("label_8")
        self.sbProt = QtWidgets.QSpinBox(DlgPeriod)
        self.sbProt.setGeometry(QtCore.QRect(140, 180, 70, 22))
        self.sbProt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbProt.setMinimum(0)
        self.sbProt.setMaximum(100)
        self.sbProt.setProperty("value", 20)
        self.sbProt.setObjectName("sbProt")
        self.sbFat = QtWidgets.QSpinBox(DlgPeriod)
        self.sbFat.setGeometry(QtCore.QRect(140, 210, 70, 22))
        self.sbFat.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbFat.setMinimum(0)
        self.sbFat.setMaximum(100)
        self.sbFat.setProperty("value", 20)
        self.sbFat.setObjectName("sbFat")
        self.sbCarb = QtWidgets.QSpinBox(DlgPeriod)
        self.sbCarb.setGeometry(QtCore.QRect(140, 240, 70, 22))
        self.sbCarb.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbCarb.setMinimum(0)
        self.sbCarb.setMaximum(100)
        self.sbCarb.setProperty("value", 20)
        self.sbCarb.setObjectName("sbCarb")
        self.sbVariation = QtWidgets.QDoubleSpinBox(DlgPeriod)
        self.sbVariation.setGeometry(QtCore.QRect(140, 270, 70, 22))
        self.sbVariation.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sbVariation.setDecimals(1)
        self.sbVariation.setMinimum(0.0)
        self.sbVariation.setMaximum(10.0)
        self.sbVariation.setProperty("value", 2.5)
        self.sbVariation.setObjectName("sbVariation")
        self.label_9 = QtWidgets.QLabel(DlgPeriod)
        self.label_9.setGeometry(QtCore.QRect(20, 320, 47, 13))
        self.label_9.setObjectName("label_9")
        self.teNote = QtWidgets.QPlainTextEdit(DlgPeriod)
        self.teNote.setGeometry(QtCore.QRect(140, 300, 231, 71))
        self.teNote.setObjectName("teNote")

        self.retranslateUi(DlgPeriod)
        self.buttonBox.accepted.connect(DlgPeriod.accept) # type: ignore
        self.buttonBox.rejected.connect(DlgPeriod.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DlgPeriod)

    def retranslateUi(self, DlgPeriod):
        _translate = QtCore.QCoreApplication.translate
        self.lbStartDate.setText(_translate("DlgPeriod", "Start Date"))
        self.lbUser.setText(_translate("DlgPeriod", "Guest"))
        self.label.setText(_translate("DlgPeriod", "Height, sm"))
        self.label_2.setText(_translate("DlgPeriod", "Weight, kg"))
        self.label_3.setText(_translate("DlgPeriod", "Activity"))
        self.cbActivity.setItemText(0, _translate("DlgPeriod", "Sedentary lifestyle"))
        self.cbActivity.setItemText(1, _translate("DlgPeriod", "Small (sports 1-3 days a week)"))
        self.cbActivity.setItemText(2, _translate("DlgPeriod", "Medium (sport 3-5 days a week)"))
        self.cbActivity.setItemText(3, _translate("DlgPeriod", "High (sport 6-7 days a week) "))
        self.cbActivity.setItemText(4, _translate("DlgPeriod", "Very high (physical work, 2 workouts per day"))
        self.label_4.setText(_translate("DlgPeriod", "<html><head/><body><p><span style=\" font-size:9pt; color:#0000ff;\">Ratio of protein, fat, carbohydrates to achieve the goal:</span></p></body></html>"))
        self.label_5.setText(_translate("DlgPeriod", "Proteins, %"))
        self.label_6.setText(_translate("DlgPeriod", "Variation, %"))
        self.label_7.setText(_translate("DlgPeriod", "Fats, %"))
        self.label_8.setText(_translate("DlgPeriod", "Carbohydrates, %"))
        self.label_9.setText(_translate("DlgPeriod", "Note"))
