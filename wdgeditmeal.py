# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QTime, QDate, QModelIndex
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QShortcut, QDialog, QInputDialog, QMessageBox, QProgressDialog
from PyQt5.QtSql import QSqlDatabase

import ui_wdgeditmeal

from foodtree import FoodTree
from dlggroup import DlgGroup
from dlgfood import DlgFood
from dlggrouptree import DlgGroupTree
from mealmodel import MealModel

class WdgEditMeal(QWidget):

    def __init__(self, parent=None):
        super(WdgEditMeal, self).__init__(parent)
        self.ui = ui_wdgeditmeal.Ui_WdgEditMeal()
        self.ui.setupUi(self)
        self.setObjectName('WdgEditMeal')
        self.current_days_id = -1
        self.foodtree = FoodTree(self)
        self.ui.FrmFood.layout().addWidget(self.foodtree)
        self.currow_in_finditemlist = -1
        self.finditemlist = []
        self.keyCtrlN  = QShortcut(QKeySequence("Ctrl+N"), self)
        self.keyCtrlN.activated.connect(self.gotoNextFind)
        self.keyCtrlP  = QShortcut(QKeySequence("Ctrl+P"), self)
        self.keyCtrlP.activated.connect(self.gotoPrevFind)
        self.keyCtrlF = QShortcut(QKeySequence("Ctrl+F"), self)
        self.keyCtrlF.activated.connect(self.slotShortcutCtrlF)
        self.ui.tbNext.setEnabled(False)
        self.ui.tbPrev.setEnabled(False)
        self.ui.tbAdd.clicked.connect(self.addFood)
        self.ui.tbAddGroup.clicked.connect(self.addGroup)
        self.ui.tbEdit.clicked.connect(self.editFoodRecord)
        self.ui.tbDel.clicked.connect(self.deleteFoodRecord)
        self.ui.tbMove.clicked.connect(self.moveFoodRecord)
        self.ui.tbNext.clicked.connect(self.gotoNextFind)
        self.ui.tbPrev.clicked.connect(self.gotoPrevFind)
        self.ui.leFind.textChanged.connect(self.findItems)

        self.ui.tbAddMeal.clicked.connect(self.addMeal)

        self.ui.tbAddMealToDay.clicked.connect(self.addMealToDay)

        self.emodel = MealModel()
        self.ui.tvEditMeal.setModel(self.emodel)


    def setDatabase(self, database):
        self.database  = database
        self.foodtree.setDatabase(self.database)
        self.foodtree.readData()

    def addMeal(self):
        if self.foodtree.currentItem():
            isgroup = int(self.foodtree.currentItem().text(FoodTree.ISGROUP))
            if isgroup==1:
                QMessageBox.information(self, "Edit meal", "The group is selected.")
                return
            rows = self.emodel.rowCount()
            if rows>0:
                time = self.emodel.data(self.emodel.index(rows-1, 1))
            else:
                time = QTime.currentTime()
            products_id = int(self.foodtree.currentItem().text(FoodTree.ID))
            name =self.foodtree.currentItem().text(FoodTree.NAME)

            self.emodel.insertRow(self.emodel.rowCount())
            row = self.emodel.rowCount() - 1
            self.emodel.setData(self.emodel.index(row,0), -1)
            self.emodel.setData(self.emodel.index(row,1), time)
            self.emodel.setData(self.emodel.index(row,2), name)
            self.emodel.setData(self.emodel.index(row,3), 0)
            self.emodel.setData(self.emodel.index(row,4), products_id)


    def addFood(self):
        item = self.foodtree.currentItem()
        dlg = DlgFood()
        dlg.setWindowTitle(self.tr("Add product (dish)"))
        parentid = 0
        print("item.text=",item.text(FoodTree.ISGROUP))
        if item:
            if int(item.text(FoodTree.ISGROUP))==0:
                item = item.parent()
            parentid = int(item.text(FoodTree.ID))
            if dlg.exec()==QDialog.Accepted:
                self.foodtree.appendRecord(parentid, 0, dlg.getName(), dlg.getCalory(), dlg.getProt(), dlg.getFat(), dlg.getCarb(), item)
        else:
            QMessageBox.information(self, "Food", "The group is not selected.")

    def addGroup(self):
        item = self.foodtree.currentItem()
        dlg = DlgGroup()
        dlg.setWindowTitle(self.tr("Add product group")) # Добавить группу
        if dlg.exec()==QDialog.Accepted:
            parentid = 0
            if dlg.isTopLevel():
                item = None
            else:
                if item:
                    if int(item.text(FoodTree.ISGROUP))==0:
                        item = item.parent()
                if item:
                    parentid = int(item.text(FoodTree.ID))
            self.foodtree.appendRecord(parentid, 1, dlg.getName(), 0, 0, 0, 0, item)

    def editFoodRecord(self):
        item = self.foodtree.currentItem()
        if item:
            is_group = int(item.text(FoodTree.ISGROUP))
            if is_group==1:
                dlg = DlgGroup()
                dlg.setData(item.parent()==0, item.text(FoodTree.NAME))
                dlg.setEditMode()
                dlg.setWindowTitle(self.tr("Edit name group"))
                if dlg.exec()==QDialog.Accepted:
                    self.foodtree.editRecord(dlg.getName(), 0, 0, 0, 0, item)
            else:
                dlg = DlgFood()
                dlg.setWindowTitle(self.tr("Edit product (dish)"))
                dlg.setData(item.text(FoodTree.NAME),
                            float(item.text(FoodTree.CALORY)),
                            float(item.text(FoodTree.PROTEIN)),
                            float(item.text(FoodTree.FAT)),
                            float(item.text(FoodTree.CARBOHYDRATE)),
                            )
                # pdlg.setEditMode()
                if dlg.exec()==QDialog.Accepted:
                    self.foodtree.editRecord(dlg.getName(),
                                        dlg.getCalory(),
                                        dlg.getProt(),
                                        dlg.getFat(),
                                        dlg.getCarb(),
                                        item)
        else:
            QMessageBox.warning(self, "", self.tr("No record selected."), QMessageBox.Ok)


    def deleteFoodRecord(self):
        item = self.foodtree.currentItem()
        if item:
            check = self.foodtree.checkDelete(item)
            if check==1:
                QMessageBox.warning(self, "Food", self.tr("The group has products (dishes). Deletion is not possible."), QMessageBox.Ok)
            elif check==2:
                QMessageBox.warning(self, "Food", self.tr("The product (dish) is used in accounting. Deletion is not possible."), QMessageBox.Ok)
            else:
                res = QMessageBox.question(self,"Food",self.tr("Delete record?"),QMessageBox.Yes|QMessageBox.No)
                if res==QMessageBox.Yes:
                    self.foodtree.deleteRecord(item)
        else:
            QMessageBox.warning(self, "",self.tr("No record selected."), QMessageBox.Ok)


    def moveFoodRecord(self):
        item = self.foodtree.currentItem()
        if item:
            dlg = DlgGroupTree(self)
            dlg.setDatabase(self.foodtree.database)
            if dlg.exec()==QDialog.Accepted:
                newparentid = dlg.getSelectedGroupID()
                if newparentid==-1:
                    QMessageBox.warning(self, self.tr("Food"), self.tr("No group selected. Moving is not possible."), QMessageBox.Ok)
                else:
                    self.foodtree.moveRecord(item, newparentid)
        else:
            QMessageBox.warning(self, self.tr("Food"), self.tr("No record selected."), QMessageBox.Ok)

    def findItems(self, text):
        if not text:
            self.ui.tbNext.setEnabled(False)
            self.currow_in_finditemlist = -1
            self.ui.lbFoundCount.setText("0")
            self.ui.lbFound.setText("0")
            self.ui.tbNext.setEnabled(False)
            self.ui.tbPrev.setEnabled(False)
        else:
            self.finditemlist = self.foodtree.findItems(text, Qt.MatchContains|Qt.MatchRecursive, 0)
            if len(self.finditemlist)>0:
                self.foodtree.setCurrentItem(self.finditemlist[0])
                self.currow_in_finditemlist = 0
                self.ui.tbNext.setEnabled(True)
                self.ui.lbFoundCount.setText(f"{len(self.finditemlist)}")
                self.ui.lbFound.setText(f"{self.currow_in_finditemlist+1}")
        self.ui.tbNext.setEnabled(not self.currow_in_finditemlist==len(self.finditemlist)-1)
        self.ui.tbPrev.setEnabled(self.currow_in_finditemlist>0)

    def gotoNextFind(self):
        itemcount = len(self.finditemlist)
        if itemcount==0:
            self.currow_in_finditemlist = -1
            self.ui.tbNext.setEnabled(False)
            self.ui.tbPrev.setEnabled(False)
            return
        if self.currow_in_finditemlist<itemcount-1:
            self.currow_in_finditemlist += 1
            self.ui.tbPrev.setEnabled(True)
        self.ui.tbNext.setEnabled(not self.currow_in_finditemlist==itemcount-1)
        self.ui.tbPrev.setEnabled(self.currow_in_finditemlist>0)
        self.foodtree.setCurrentItem(self.finditemlist[self.currow_in_finditemlist])
        self.ui.lbFound.setText(f"{self.currow_in_finditemlist+1}")

    def gotoPrevFind(self):
        itemcount = len(self.finditemlist)
        if itemcount==0:
            self.currow_in_finditemlist = -1
            self.ui.tbNext.setEnabled(False)
            self.ui.tbPrev.setEnabled(False)
            return
        if self.currow_in_finditemlist>0:
            self.currow_in_finditemlist -= 1
        self.ui.tbNext.setEnabled(not self.currow_in_finditemlist==itemcount-1)
        self.ui.tbPrev.setEnabled(self.currow_in_finditemlist>0)
        self.foodtree.setCurrentItem(self.finditemlist[self.currow_in_finditemlist])
        self.ui.lbFound.setText(f"{self.currow_in_finditemlist+1}")

    def slotShortcutCtrlF(self):
        self.ui.leFind.setFocus()

    def setEnableActions(self):
        self.ui.tbNext.setEnabled()
        self.ui.tbPrev.setEnabled()

    def addMealToDay(self):
        if self.emodel.rowCount()==0:
            QMessageBox.warning(self, self.tr("Food"), self.tr("No record in table."), QMessageBox.Ok)
            return
        meal_list = []
        for row in range(self.emodel.rowCount()):
            time = self.emodel.data(self.emodel.index(row,1))  # .toString("hh:mm")
            weight = self.emodel.data(self.emodel.index(row,3))
            products_id = int(self.emodel.data(self.emodel.index(row,4)))
            meal = {'time': time, 'weight': weight, 'days_id':  self.current_days_id, 'products_id': products_id}
            meal_list.append(meal)
        self.database.appendMealToDay1(meal_list)
