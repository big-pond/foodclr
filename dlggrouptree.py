# -*- coding: utf-8 -*-

from PyQt5.QtCore import QRect, QSettings, Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QMessageBox

from grouptree import GroupTree

class DlgGroupTree(QDialog):

    def __init__(self, parent=None):
        super(DlgGroupTree, self).__init__(parent)
        vbl = QVBoxLayout()
        self.setLayout(vbl)
        self.grouptree = GroupTree(self)
        vbl.addWidget(self.grouptree)
        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        vbl.addWidget(self.buttonbox)
        self.setWindowTitle(self.tr("Select group"))
        self.buttonbox.accepted.connect(self.accept)
        self.buttonbox.rejected.connect(self.reject)
        self.setObjectName('DlgGroupTree')
        self.readSettings()

    def done(self, a0: int) -> None:
        self.writeSettings()
        return super().done(a0)


    def setDatabase(self, database):
        self.grouptree.setDatabase(database)
        self.grouptree.readData()

    # def accept(self) . None:
    #     return super().accept()
    
    # def reject(self) . None:
    #     return super().reject()
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

    def getSelectedGroupID(self):
        id = -1
        item = self.grouptree.currentItem()
        if item:
            id = int(item.text(GroupTree.ID))
        return id

    def getListGroupID(self):
        id_list = []
        item = self.grouptree.currentItem()
        if item:
            id = int(item.text(GroupTree.ID))
            id_list.append(id)
            self.readChildID(id_list, item)
        return id_list

    def setCurrentTopLevelFirstItem(self):
        item = self.grouptree.topLevelItem(0)
        if item:
            self.grouptree.setCurrentItem(item)

    def readChildID(self, id_list, item):
        count  = item.childCount()
        for i in range(count):
            childitem = item.child(i)
            id_ = int(childitem.text(GroupTree.ID))
            id_list.append(id_)
            self.readChildID(id_list, childitem)
