# -*- coding: utf-8 -*-

# from statistics import mode
from tkinter import YES
from unittest import result
import ui_wdgperiods

from PyQt5.QtCore import Qt, QDate, QModelIndex, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QAbstractItemView, QInputDialog, QMessageBox, QProgressDialog

from dlgperiod import DlgPeriod

class WdgPeriods(QWidget):
    gotoDays = pyqtSignal()

    def __init__(self, parent=None):
        super(WdgPeriods, self).__init__(parent)
        self.ui = ui_wdgperiods.Ui_WdgPeriods()
        self.ui.setupUi(self)
        self.setObjectName('WdgPeriods')
        self.ui.tvPeriod.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tvPeriod.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tvPeriod.setAlternatingRowColors(True)
        self.ui.tbAdd.clicked.connect(self.appendRecord)
        self.ui.tbDel.clicked.connect(self.delRecord)
        self.ui.tbEdit.clicked.connect(self.editRecord)
        self.ui.tbMeals.clicked.connect(self.goMeals)

    def setDatabase(self, database):
        self.database  = database
        self.ui.tvPeriod.setModel(database.periodsmodel)

    def appendRecord(self):
        dlg = DlgPeriod(self)
        dlg.setWindowTitle("Append period")
        # dlg.setDatabase(self.foodtree.database)
        if dlg.exec()==QDialog.Accepted:
            start_date, height, weight, activity, prot, fat, carb, variation, note = dlg.getData()
            start_date = start_date.toString(Qt.ISODate)
            self.database.appendPeriod(start_date, height, weight, activity, prot, fat, carb, variation, note)
            self.database.execPeriodQuery()
            self.formatTableView()


    def editRecord(self):
        index = self.ui.tvPeriod.currentIndex()
        if index.isValid():
            dlg = DlgPeriod(self)
            dlg.setWindowTitle("Edit period")
            row = index.row()
            model = self.ui.tvPeriod.model()
            dlg.setData(QDate.fromString(model.data(index.sibling(row,1)),),
                        model.data(index.sibling(row,2)),
                        model.data(index.sibling(row,3)),
                        model.data(index.sibling(row,4)),
                        model.data(index.sibling(row,5)),
                        model.data(index.sibling(row,6)),
                        model.data(index.sibling(row,7)),
                        model.data(index.sibling(row,8)),
                        model.data(index.sibling(row,9))
                        )
            if dlg.exec()==QDialog.Accepted:
                id_ = int(model.data(index.sibling(row,0)))
                start_date, height, weight, activity, prot, fat, carb, variation, note = dlg.getData()
                start_date = start_date.toString(Qt.ISODate)
                self.database.editPeriod(id_, start_date, height, weight, activity, prot, fat, carb, variation, note)
                self.database.execPeriodQuery()
                self.formatTableView()

    def delRecord(self):
        index = self.ui.tvPeriod.currentIndex()
        if index.isValid():
            if QMessageBox.question(self, 'Periods', 'Delete record?')==QMessageBox.Yes:
                id_ = int(self.ui.tvPeriod.model().data(index.sibling(index.row(),0)))
                count = self.database.periodDayCount(id_)
                if count==0:
                    # id_ = int(self.ui.tvPeriod.model().data(index.sibling(index.row(),0)))
                    result = self.database.deletePeriod(id_)
                    if result:
                        self.database.execPeriodQuery()
                        self.formatTableView()
                        # print("delete")
                else:
                    QMessageBox.information(self, 'Periods', 'You cannot delete record because it has entries in the Days table')
    
    def formatTableView(self):
        # self.ui.tvPeriod.setColumnHidden(0, True)
        # self.ui.tvPeriod.setColumnHidden(10, True)
        self.ui.tvPeriod.resizeColumnsToContents()
        self.ui.tvPeriod.resizeRowsToContents()

    def goMeals(self):
        index = self.ui.tvPeriod.currentIndex()
        if index.isValid():
            id_ = int(self.ui.tvPeriod.model().data(index.sibling(index.row(),0)))
            self.database.current_periods_id = id_
            self.gotoDays.emit()

    def widgetShow(self, index):
        # print(index)
        if index==3:
            print('Period show')
            self.database.execPeriodQuery()
            self.formatTableView()
            row_count = self.database.periodsmodel.rowCount()
            self.ui.tvPeriod.setCurrentIndex(self.database.periodsmodel.index(row_count-1, 0))
