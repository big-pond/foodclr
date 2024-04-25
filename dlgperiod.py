# from logging import fatal
from PyQt5.QtCore import QSettings, Qt, QDate
from PyQt5.QtWidgets import QDialog

import ui_dlgperiod

class DlgPeriod(QDialog):

    def __init__(self, parent=None):
        super(DlgPeriod, self).__init__(parent)
        self.ui = ui_dlgperiod.Ui_DlgPeriod()
        self.ui.setupUi(self)
        self.ui.deStart.setDate(QDate.currentDate())
        self.setObjectName('DlgPeriod')
        self.readSettings()

    def done(self, a0: int) -> None:
        self.writeSettings()
        return super().done(a0)

    def setData(self, start_date, height, weight, activity, prot, fat, carb, variation, note):
        self.ui.deStart.setDate(start_date)
        self.ui.sbHeight.setValue(height)
        self.ui.sbWeight.setValue(weight)
        self.ui.cbActivity.setCurrentIndex(activity)
        self.ui.sbProt.setValue(prot)
        self.ui.sbFat.setValue(fat)
        self.ui.sbCarb.setValue(carb)
        self.ui.sbVariation.setValue(variation)
        self.ui.teNote.setPlainText(note)

    def getData(self):
        start_date = self.ui.deStart.date()
        height = self.ui.sbHeight.value()
        weight = self.ui.sbWeight.value()
        activity = self.ui.cbActivity.currentIndex()
        prot = self.ui.sbProt.value()
        fat = self.ui.sbFat.value()
        carb = self.ui.sbCarb.value()
        variation = self.ui.sbVariation.value()
        note = self.ui.teNote.toPlainText()
        return start_date, height, weight, activity, prot, fat, carb, variation, note

    def writeSettings(self):
        settings = QSettings('foodcl.ini', QSettings.IniFormat)
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
