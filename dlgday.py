from PyQt5.QtCore import QSettings, Qt, QDate
from PyQt5.QtWidgets import QDialog

import ui_dlgday

class DlgDay(QDialog):

    def __init__(self, parent=None):
        super(DlgDay, self).__init__(parent)
        self.ui = ui_dlgday.Ui_DlgDay()
        self.ui.setupUi(self)
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.setObjectName('DlgDay')
        self.readSettings()

    def done(self, a0: int) -> None:
        self.writeSettings()
        return super().done(a0)

    def setData(self, mday, weight, waist, hips):
        self.ui.dateEdit.setDate(mday)
        self.ui.sbWeight.setValue(weight)
        self.ui.sbWaist.setValue(waist)
        self.ui.sbHips.setValue(hips)

    def getData(self):
        mday = self.ui.dateEdit.date()
        weight = self.ui.sbWeight.value()
        waist = self.ui.sbWaist.value()
        hips = self.ui.sbHips.value()
        return mday, weight, waist, hips

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
