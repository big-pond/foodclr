# -*- coding: utf-8 -*-

import ui_dlggroup
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QShortcut, QDialog, QInputDialog, QMessageBox, QProgressDialog


class DlgGroup(QDialog):

    def __init__(self, parent=None):
        super(DlgGroup, self).__init__(parent)
        self.ui = ui_dlggroup.Ui_DlgGroup()
        self.ui.setupUi(self)
        self.setObjectName('DlgGroup')
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

    def isTopLevel(self):
        return self.ui.chTopLevel.isChecked()

    def getName(self):
        return self.ui.leName.text()

    def setEditMode(self):
        self.ui.chTopLevel.setEnabled(False)

    def setData(self, istoplevel, name):
        self.ui.chTopLevel.setChecked(istoplevel)
        self.ui.leName.setText(name)

    def clear(self):
        self.ui.chTopLevel.setChecked(False)
        self.ui.leName.clear()
