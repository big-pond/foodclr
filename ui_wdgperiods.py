# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wdgperiods.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WdgPeriods(object):
    def setupUi(self, WdgPeriods):
        WdgPeriods.setObjectName("WdgPeriods")
        WdgPeriods.resize(400, 300)
        WdgPeriods.setWindowTitle("")
        self.verticalLayout = QtWidgets.QVBoxLayout(WdgPeriods)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_3 = QtWidgets.QFrame(WdgPeriods)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.tbAdd = QtWidgets.QToolButton(self.frame_3)
        self.tbAdd.setGeometry(QtCore.QRect(88, 2, 38, 38))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tbAdd.setIcon(icon)
        self.tbAdd.setIconSize(QtCore.QSize(32, 32))
        self.tbAdd.setObjectName("tbAdd")
        self.tbDel = QtWidgets.QToolButton(self.frame_3)
        self.tbDel.setGeometry(QtCore.QRect(130, 2, 38, 38))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/resources/minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tbDel.setIcon(icon1)
        self.tbDel.setIconSize(QtCore.QSize(32, 32))
        self.tbDel.setObjectName("tbDel")
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setGeometry(QtCore.QRect(10, 10, 60, 20))
        self.label.setObjectName("label")
        self.tbEdit = QtWidgets.QToolButton(self.frame_3)
        self.tbEdit.setGeometry(QtCore.QRect(170, 1, 38, 38))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/resources/pen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tbEdit.setIcon(icon2)
        self.tbEdit.setIconSize(QtCore.QSize(32, 32))
        self.tbEdit.setObjectName("tbEdit")
        self.tbMeals = QtWidgets.QToolButton(self.frame_3)
        self.tbMeals.setGeometry(QtCore.QRect(240, 1, 38, 38))
        self.tbMeals.setIconSize(QtCore.QSize(32, 32))
        self.tbMeals.setObjectName("tbMeals")
        self.verticalLayout.addWidget(self.frame_3)
        self.tvPeriod = QtWidgets.QTableView(WdgPeriods)
        self.tvPeriod.setObjectName("tvPeriod")
        self.verticalLayout.addWidget(self.tvPeriod)

        self.retranslateUi(WdgPeriods)
        QtCore.QMetaObject.connectSlotsByName(WdgPeriods)

    def retranslateUi(self, WdgPeriods):
        _translate = QtCore.QCoreApplication.translate
        self.tbAdd.setText(_translate("WdgPeriods", "..."))
        self.tbDel.setText(_translate("WdgPeriods", "..."))
        self.label.setText(_translate("WdgPeriods", "<html><head/><body><p><span style=\" font-size:12pt; color:#0000ff;\">Period</span></p></body></html>"))
        self.tbEdit.setText(_translate("WdgPeriods", "..."))
        self.tbMeals.setText(_translate("WdgPeriods", "Meals"))
import foodcl_rc