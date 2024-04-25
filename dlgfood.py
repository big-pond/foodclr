# -*- coding: utf-8 -*-

import ui_dlgfood
from PyQt5.QtCore import QSettings
# from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QDialog


class DlgFood(QDialog):

    def __init__(self, parent=None):
        super(DlgFood, self).__init__(parent)
        self.ui = ui_dlgfood.Ui_DlgFood()
        self.ui.setupUi(self)
        self.setObjectName('DlgFood')
        self.readSettings()

    def done(self, a0: int) -> None:
        self.writeSettings()
        return super().done(a0)


    def writeSettings(self):
        settings = QSettings('foodcl.ini', QSettings.IniFormat)
        # QSettings settings(QString("%1.ini").arg(QApplication::applicationName()),QSettings::IniFormat)
        settings.beginGroup(self.objectName())
        settings.setValue("geometry", self.saveGeometry())
        settings.endGroup()
 
    def readSettings(self):
        settings = QSettings('foodcl.ini', QSettings.IniFormat)
        settings.beginGroup(self.objectName())
        cnt = settings.contains("geometry")
        if cnt:
            self.restoreGeometry(settings.value('geometry', ''))
        settings.endGroup()

    def clear(self):
        self.ui.leName.clear()
        self.ui.sbCalories.clear()
        self.ui.sbProt.clear()
        self.ui.sbFat.clear()
        self.ui.sbCarbo.clear()

    def getName(self):
        return self.ui.leName.text()

    def getCalory(self):
        return self.ui.sbCalories.value()

    def getProt(self):
        return self.ui.sbProt.value()

    def getFat(self):
        return self.ui.sbFat.value()

    def getCarb(self):
        return self.ui.sbCarbo.value()

    def setData(self, name, calory, prot,  fat, carb):
        self.ui.leName.setText(name)
        self.ui.sbCalories.setValue(calory)
        self.ui.sbProt.setValue(prot)
        self.ui.sbFat.setValue(fat)
        self.ui.sbCarbo.setValue(carb)
