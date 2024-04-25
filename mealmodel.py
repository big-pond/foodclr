#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QTime


class Meal:
    def __init__(self, id_: int = 0, time: QTime = QTime.currentTime(), name: str = '', weight: int = 0, products_id: int = 0):
        self.id = id_  # id in table `meals`
        self.time = time
        self.name = name
        self.weight = weight
        self.products_id = products_id

class MealModel(QAbstractTableModel):
    COL_COUNT = 5
    # defaultColW = [10, 14, 25, 10]

    def __init__(self):
        super(MealModel, self).__init__()
        self.meal_list = []

    def rowCount(self, index=QModelIndex()):
        return len(self.meal_list)

    def columnCount(self, index=QModelIndex()):
        return MealModel.COL_COUNT

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        meal = self.meal_list[index.row()]
        if index.column() == 0: # id
            if role == Qt.TextAlignmentRole:
                return Qt.AlignRight | Qt.AlignVCenter
            elif role == Qt.DisplayRole:
                return meal.id
            # elif role == Qt.EditRole:
            #     return meal.id
        elif index.column() == 1:  # time
            if role == Qt.TextAlignmentRole:
                return Qt.AlignRight | Qt.AlignVCenter
            elif role == Qt.DisplayRole:
                return meal.time
            elif role == Qt.EditRole:
                return meal.time
        elif index.column() == 2:  # name
            if role == Qt.TextAlignmentRole:
                return Qt.AlignLeft | Qt.AlignVCenter
            elif role == Qt.DisplayRole:
                return meal.name
            # elif role == Qt.EditRole:
            #     return meal.name
        elif index.column() == 3:  # weight
            if role == Qt.TextAlignmentRole:
                return Qt.AlignRight | Qt.AlignVCenter
            elif role == Qt.DisplayRole:
                return meal.weight
            elif role == Qt.EditRole:
                return meal.weight
        elif index.column() == 4:  # product_id
            if role == Qt.TextAlignmentRole:
                return Qt.AlignRight | Qt.AlignVCenter
            elif role == Qt.DisplayRole:
                return meal.products_id
            # elif role == Qt.EditRole:
            #     return meal.products_id
        return None

    def setData(self, index, value, role=Qt.EditRole):
        success = False
        if index.isValid() and role == Qt.EditRole:
            if index.column() == 0:
                self.meal_list[index.row()].id = value
            elif index.column() == 1:
                self.meal_list[index.row()].time = value
            elif index.column() == 2:
                self.meal_list[index.row()].name = value
            elif index.column() == 3:
                self.meal_list[index.row()].weight = value
            elif index.column() == 4:
                self.meal_list[index.row()].products_id = value
            self.dataChanged.emit(index, index)
            success = True
        return success

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        v = None
        if orientation == Qt.Horizontal:
            if section == 0:
                v = self.tr("id")
            elif section == 1:
                v = self.tr("Time")
            elif section == 2:
                v = self.tr("Food name")
            elif section == 3:
                v = self.tr("Weight, g")
            elif section == 4:
                v = self.tr("product_id")
        elif orientation == Qt.Vertical:
            v = section + 1
        return v

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        flag = QAbstractTableModel.flags(self, index)
        return flag | Qt.ItemIsEditable if index.isValid() else flag

    def removeRows(self, row: int, count: int, parent: QModelIndex = QModelIndex()) -> bool:
        size = len(self.meal_list)
        if size <= 0 or row > size or count <= 0:
            return False
        self.beginRemoveRows(parent, row, row + count - 1)
        for i in range(row, row + count):
            self.meal_list.pop(row)
        self.endRemoveRows()
        return True

    def insertRows(self, row: int, count: int, parent: QModelIndex = QModelIndex()) -> bool:
        size = len(self.meal_list)
        if row < 0 or row > size or count <= 0:
            return False
        self.beginInsertRows(parent, row, row + count - 1)
        for i in range(count):
            if row < size - 1:
                self.meal_list.insert(row + i, Meal())
            else:
                self.meal_list.append(Meal())
        self.endInsertRows()
        return True


    def getMeal(self, row):
        return self.meal_list[row]

    def getMealList(self):
        return self.meal_list



if __name__ == '__main__':
    p1 = Meal(1, QTime.currentTime(), 'Колбаса', 51)
    p2 = Meal(2, QTime.currentTime(), 'Хлеб', 99)
    model = MealModel()
    model.insertRow(0)
    model.insertRow(0)
    # model.insertRows(0, 1)
    model.setData(model.index(0,0), p1.id)
    model.setData(model.index(0,1), p1.time)
    model.setData(model.index(0,2), p1.name)
    model.setData(model.index(0,3), p1.weight)
    # model.insertRows(1, 1)
    model.setData(model.index(1,0), p2.id)
    model.setData(model.index(1,1), p2.time)
    model.setData(model.index(1,2), p2.name)
    model.setData(model.index(1,3), p2.weight)
    model.insertRow(2)
    print(model.rowCount())
    print(model.getMeal(0).id)
    print(model.getMeal(1).id)
