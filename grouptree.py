# -*-coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTreeWidget, QWidget, QTreeWidgetItem, QStyle
from PyQt5.QtSql import QSqlQuery

class GroupTree(QTreeWidget) :

    NAME, ID, ISGROUP, PRODUCTS_ID = range(4)

    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.labels = [self.tr("Group name"), self.tr("id"), self.tr("isgroup"), self.tr("products_id")]
        self.setHeaderLabels(self.labels)
        self.setColumnWidth(GroupTree.NAME, 200)

        self.setColumnHidden(GroupTree.ID, True)
        self.setColumnHidden(GroupTree.PRODUCTS_ID, True)
        self.setColumnHidden(GroupTree.ISGROUP, True)

        self.folderIcon = QIcon()
        self.folderIcon.addPixmap(self.style().standardPixmap(QStyle.SP_DirClosedIcon), QIcon.Normal, QIcon.Off)
        self.folderIcon.addPixmap(self.style().standardPixmap(QStyle.SP_DirOpenIcon), QIcon.Normal, QIcon.On)

    def setDatabase(self, database):
        self.database  = database

    def readData(self):
        query = QSqlQuery(self.database.db)
        query.prepare("SELECT `name`, `id`, `products_id`, `isgroup` FROM `products` WHERE `isgroup`=1 AND `products_id`=?;")
        query.bindValue(0, 0)
        query.exec()
        while query.next():
            rec = query.record()
            self.parseRecord(rec, None)
        self.sortItems(0,Qt.AscendingOrder)

    def parseRecord(self, record, parentItem):
        item = self.createItem(record, parentItem)
        query = QSqlQuery(self.database.db)
        query.prepare("SELECT `name`, `id`, `products_id`, `isgroup` FROM `products` WHERE `isgroup`=1 AND `products_id`=?;")
        query.bindValue(0, int(record.value("id")))
        query.exec()
        while query.next():
            rec = query.record()
            self.parseRecord(rec, item)

    def createItem(self, record, parentItem):
        id_ = record.value("id")
        name =record.value("name")
        isgroup = record.value("isgroup")
        products_id = record.value("products_id")
        return self.createItem1(id_, products_id, isgroup, name, parentItem)

    def createItem1(self, id_, products_id, isgroup, name, parentItem):
        if parentItem:
            item = QTreeWidgetItem(parentItem)
        else:
            item = QTreeWidgetItem(self)
        item.setIcon(GroupTree.NAME, self.folderIcon)
        item.setText(GroupTree.NAME, name)
        item.setText(GroupTree.ID, str(id_))
        item.setText(GroupTree.PRODUCTS_ID, str(products_id))
        item.setText(GroupTree.ISGROUP, str(isgroup))
        return item
