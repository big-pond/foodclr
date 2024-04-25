# -*- coding: utf-8 -*-


from PyQt5.QtCore import Qt, QDate, QModelIndex, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QInputDialog, QMessageBox, QProgressDialog
from PyQt5.QtSql import QSqlDatabase
# from database import 

import ui_wdgmeals

from dlgday import DlgDay

class WdgMeals(QWidget):

    gotoEditMeal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(WdgMeals, self).__init__(parent)
        self.ui = ui_wdgmeals.Ui_WdgMeals()
        self.ui.setupUi(self)
        self.setObjectName('WdgMeals')

        self.ui.tbAddDay.clicked.connect(self.appendDay)
        self.ui.tbEditDay.clicked.connect(self.editDay)
        self.ui.tbDelDay.clicked.connect(self.deleteDay)
        self.ui.tbAddMeal.clicked.connect(self.appendMeal)
        self.ui.tbEditMeal.clicked.connect(self.editMeal)
        self.ui.tbDelMeal.clicked.connect(self.deleteMeal)
        # self.ui.tbAddMeal.clicked.connect(self.goEditMeal)
        
    def setDatabase(self, database):
        self.database  = database
        self.ui.tvDays.setModel(database.daysmodel)

    def appendDay(self):
        model = self.ui.tvDays.model()
        date = QDate.currentDate()
        if model.rowCount():
            record = model.record(model.rowCount()-1)
            date = QDate.fromString(str(record.value("mdate")))
            date = date.addDays(1)
        weight = self.database.getLastWeight()
        dlg = DlgDay()
        dlg.setWindowTitle("Append day")
        dlg.setData(date, weight, 0, 0)
        if dlg.exec()==QDialog.Accepted:
            date, weight, waist, hips = dlg.getData()
            date = date.toString(Qt.ISODate)
            self.database.appendDay(date, weight, waist, hips)
            self.database.execDaysQuery()
            self.formatDaysTableView()

    def editDay(self):
        index = self.ui.tvDays.currentIndex()
        if index.isValid():
            weight = 0.0
            waist = 0
            hips = 0
            model = self.ui.tvDays.model()
            record = model.record(index.row())
            id_ = int(record.value("id"))
            mdate = QDate.fromString(str(record.value("mdate"))) #преобразовать str в QDate 
            if record.value("weight"):
                weight = int(record.value("weight"))
            if record.value("waist"):
                waist = int(record.value("waist"))
            if record.value("hips"):
                hips = int(record.value("hips"))
            dlg = DlgDay()
            dlg.setWindowTitle("Edit day")
            dlg.setData(mdate, weight, waist, hips)
            if dlg.exec()==QDialog.Accepted:
                mdate, weight, waist, hips = dlg.getData()
                mdate = mdate.toString(Qt.ISODate)
                self.database.editDay(id_, mdate, weight, waist, hips)
                self.database.execDaysQuery()
                self.formatDaysTableView()


    def deleteDay(self):
        index = self.ui.tvDays.currentIndex()
        if index.isValid():
            if QMessageBox.question(self, 'Days', 'Delete record?')==QMessageBox.Yes:
                id_ = int(self.ui.tvDays.model().record(index.row()).value("id"))
                count = self.database.dayMealCount(id_)
                if count==0:
                    result = self.database.deleteDay(id_)
                    if result:
                        self.database.execDaysQuery()
                        self.formatDaysTableView()
                        print("delete")
                else:
                    QMessageBox.information(self, 'Days', 'You cannot delete record because it has entries in the Meals table')



    def appendMeal(self):
        index = self.ui.tvDays.currentIndex()
        if index.isValid():
            days_id = self.ui.tvDays.model().data(index.sibling(index.row(), 0))
            self.gotoEditMeal.emit(days_id)

    def editMeal(self):
        index = self.ui.tvMeals.currentIndex() # Проверять выделенные строки
        if index.isValid():
            self.gotoEditMeal.emit()

    def deleteMeal(self):
        pass

    def formatDaysTableView(self):
        # self.ui.tvDays.setColumnHidden(0, True)
        # self.ui.tvDays.setColumnHidden(10, True)
        self.ui.tvDays.resizeColumnsToContents()
        self.ui.tvDays.resizeRowsToContents()

    # def goEditMeal(self):
    #     index = self.ui.tvPeriod.currentIndex()
    #     if index.isValid():
    #         id_ = int(self.ui.tvPeriod.model().data(index.sibling(index.row(),0)))
    #         self.database.current_periods_id = id_
    #         self.gotoDays.emit()

    
    def widgetShow(self, index):
        # print(index)
        if index==4:
            print('Days and Meals show current_period_id = ', self.database.current_periods_id)
            self.database.execDaysQuery()
            self.formatDaysTableView()
            sum_param, tooltip = self.database.execDaySumQuery()
            self.ui.lbDaySum.setText(sum_param)
            self.ui.lbDaySum.setToolTip(tooltip)
            row_count = self.database.daysmodel.rowCount()
            self.ui.tvDays.setCurrentIndex(self.database.daysmodel.index(row_count-1, 0))
