# -*-coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QTreeWidget, QWidget, QTreeWidgetItem, QStyle
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class FoodTree(QTreeWidget):

    NAME, ID, ISGROUP, CALORY, PROTEIN, FAT, CARBOHYDRATE, PRODUCTS_ID = range(8)

    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.labels = [self.tr("Name"), self.tr("id"), self.tr("isgroup"), self.tr("calory"), self.tr("protein"), self.tr("fat"), self.tr("carbohydrate"), self.tr("products_id")]
        self.setHeaderLabels(self.labels)
        self.setColumnWidth(FoodTree.NAME, 200)
        # self.setColumnWidth(FoodTree.ID, 30)
        # self.setColumnWidth(FoodTree.PRODUCTS_ID, 30D)
        # self.setColumnWidth(FoodTree.ISGROUP, 30)
        self.setColumnWidth(FoodTree.CALORY, 60)
        self.setColumnWidth(FoodTree.PROTEIN, 60)
        self.setColumnWidth(FoodTree.FAT, 60)
        self.setColumnWidth(FoodTree.CARBOHYDRATE, 60)

        self.setColumnHidden(FoodTree.ID, True)
        self.setColumnHidden(FoodTree.PRODUCTS_ID, True)
        self.setColumnHidden(FoodTree.ISGROUP, True)

        self.folderIcon = QIcon()
        self.folderIcon.addPixmap(self.style().standardPixmap(QStyle.SP_DirClosedIcon), QIcon.Normal, QIcon.Off)
        self.folderIcon.addPixmap(self.style().standardPixmap(QStyle.SP_DirOpenIcon), QIcon.Normal, QIcon.On)
        # documentIcon.addPixmap(style()->standardPixmap(QStyle::SP_FileIcon));
        self.documentIcon =QIcon()
        self.documentIcon.addPixmap(QPixmap(":/resources/meal.png"))

    def setDatabase(self, database):
        self.database  = database

    def readData(self):
        query = QSqlQuery(self.database.db)
        query.prepare("SELECT * FROM products WHERE products_id = ?")
        query.bindValue(0, 0)
        query.exec()
        while query.next():
            rec = query.record()
            self.parseRecord(rec, None)
        self.sortItems(0, Qt.AscendingOrder)

    def parseRecord( self, record, parentItem):
        item = self.createItem(record, parentItem)
        query = QSqlQuery(self.database.db)
        query.prepare("SELECT * FROM products WHERE products_id = ?")
        query.bindValue(0, record.value("id"))
        query.exec()
        while query.next():
            rec = query.record()
            self.parseRecord(rec, item)

    def createItem(self, record, parentItem):
        id_ = record.value("id")
        name =record.value("name")
        isgroup = record.value("isgroup")
        calory = record.value("calory")
        protein = record.value("protein")
        fat = record.value("fat")
        carbohydrate = record.value("carbohydrate")
        products_id = record.value("products_id")
        return self.createItem1(id_, name, isgroup, calory, protein, fat, carbohydrate, products_id, parentItem)

    def createItem1(self, id_, name, isgroup, calory, protein, fat, carbohydrate, products_id, parentItem):
        if parentItem:
            item = QTreeWidgetItem(parentItem)
        else:
            item = QTreeWidgetItem(self)

        if isgroup==0:
            item.setIcon(FoodTree.NAME, self.documentIcon)
            item.setText(FoodTree.NAME, name)
            item.setText(FoodTree.ID, str(id_))
            item.setText(FoodTree.ISGROUP, str(isgroup))
            item.setText(FoodTree.CALORY, str(calory))
            item.setText(FoodTree.PROTEIN, str(protein))
            item.setText(FoodTree.FAT, str(fat))
            item.setText(FoodTree.CARBOHYDRATE, str(carbohydrate))
        else:
            item.setIcon(FoodTree.NAME, self.folderIcon)
            item.setText(FoodTree.ID, str(id_))
            item.setText(FoodTree.ISGROUP, str(isgroup))
            item.setText(FoodTree.PRODUCTS_ID, str(products_id))
            item.setText(FoodTree.NAME, name)
        return item

    def appendRecord(self, products_id, isgroup, name, calory, prot, fat, carb, parentItem):
        id_ = self.database.appendFood(products_id, isgroup, name, calory, prot, fat, carb)
        return self.createItem1(id_, name, isgroup, calory, prot, fat, carb, products_id, parentItem)

    def editRecord(self, name, calory, prot, fat, carb, edit_item):
        id_ = int(edit_item.text(FoodTree.ID))
        is_group = int(edit_item.text(FoodTree.ISGROUP))
        result = self.database.editFood(id_, is_group, name, calory, prot, fat, carb)
        if result:
            edit_item.setText(FoodTree.NAME,name)
            if is_group==0:
                edit_item.setText(FoodTree.CALORY, f'{calory:.1f}')
                edit_item.setText(FoodTree.PROTEIN, f'{prot:.1f}')
                edit_item.setText(FoodTree.FAT, f'{fat:.1f}')
                edit_item.setText(FoodTree.CARBOHYDRATE, f'{carb:.1f}')

    def checkDelete(self, item):
        res = 0
        if item:
            if item.childCount()>0:
                res = 1
            else:
                id_ = int(item.text(FoodTree.ID))
                if self.database.checkNoFoodDelete(id_):
                    res = 2
        return res

    def deleteRecord(self, item):
        if item:
            id_ = int(item.text(FoodTree.ID))
            if self.database.deleteFood(id_):
                parent_item = item.parent() # get the parent of the selected item
                if parent_item is not None:
                    parent_item.removeChild(item) # remove the selected item from its parent
                else:
                    self.invisibleRootItem().removeChild(item) # if no parent, remove from the root


    def moveRecord(self, item, newparent_id):
        item_list =  self.findItems(str(newparent_id), Qt.MatchFixedString | Qt.MatchRecursive, FoodTree.ID)
        if len(item_list)>0:
            item_id = int(item.text(FoodTree.ID))
            newParentItem = item_list[0]
            if newParentItem:
                oldParentItem = item.parent()
                if oldParentItem:
                    oldParentItem.removeChild(item)
                else:
                    idx = self.indexOfTopLevelItem ( item )
                    item = self.takeTopLevelItem(idx)
                newParentItem.addChild(item)
                self.database.moveFood(newparent_id, item_id)
