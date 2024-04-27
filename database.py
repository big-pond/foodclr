# -*-coding: utf-8 -*-

import hashlib
from random import weibullvariate
import indicators
from PyQt5.QtCore import Qt, QObject, QFileInfo, QFile, QIODevice, QTextStream, QDate
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import QMessageBox

class Database(QObject):

    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.deficit_color = "#0000bb"
        self.norm_color = "#007000"
        self.excess_color = "#dd0000"

        self.current_users_id = -1
        self.current_user_name = 'Guest'
        self.current_periods_id = -1

    def connectToSQLiteDatabase(self, filename):
        result = False
        if not QFileInfo.exists(filename):
            result = self.restoreDatabase(filename)
        else:
            result = self.openDatabase(filename)
        if result:
            self.createModels()
        return result

    def connectToMySqlDatabase(self, host, db_name, user_name, password):
        db = QSqlDatabase.addDatabase('QMYSQL')
        db.setHostName(host)
        db.setDatabaseName(db_name)
        db.setUserName(user_name)
        db.setPassword(password)
        db.open()

    def openDatabase(self, filename):
        """ База данных открывается по заданному пути и имени базы данных, если она существует """
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setHostName("HN")
        self.db.setDatabaseName(filename)
        result = self.db.open()
        return result

    def restoreDatabase(self, filename):
        result = False
        if self.openDatabase(filename):
            result = self.createTables()
            if result:
                if QMessageBox.question(None, 'Database', "Add food records to the table?")==QMessageBox.Yes:
                    result = self.fillFoodTable()
        return result

    def closeDatabase(self):
        self.db.close()

    def createTables(self):
        result = True
        file = QFile("./db/create_db.sql")
        if file.open(QIODevice.ReadOnly or QIODevice.Text):
            stream = QTextStream(file)
            stream.setCodec("UTF-8")
            sql = stream.readAll()
            file.close()
            query_list = []
            slist = sql.split(';')
            for s in slist:
                s = s.strip()
                if s:
                    query_list.append(s+';')
            query = QSqlQuery(self.db)
            for query_string in query_list:
                if not query.exec(query_string):
                    result = False
                    break
        return result

    def fillFoodTable(self):
        result = True
        file = QFile("./db/products.sql")
        if file.open(QIODevice.ReadOnly or QIODevice.Text):
            stream = QTextStream(file)
            stream.setCodec("UTF-8")
            query_list = []
            while not stream.atEnd():
                query_list.append(stream.readLine().strip())
            file.close()
            query = QSqlQuery(self.db)
            for query_string in query_list:
                if query_string:
                    if not query.exec(query_string):
                        result = False
                        break
        return result

    def createModels(self):
        self.periodsmodel = QSqlQueryModel()
        self.daysmodel = QSqlQueryModel()
        self.mealmodel = QSqlQueryModel()

    def setPeriodModelHeaders(self):
        self.periodsmodel.setHeaderData(0, Qt.Horizontal, self.tr("id"))
        self.periodsmodel.setHeaderData(1, Qt.Horizontal, self.tr("Start\nDate"))
        self.periodsmodel.setHeaderData(2, Qt.Horizontal, self.tr("Height,\nsm"))
        self.periodsmodel.setHeaderData(3, Qt.Horizontal, self.tr("Weight,\nkg"))
        self.periodsmodel.setHeaderData(4, Qt.Horizontal, self.tr("Activity"))
        self.periodsmodel.setHeaderData(5, Qt.Horizontal, self.tr("P, %"))
        self.periodsmodel.setHeaderData(6, Qt.Horizontal, self.tr("F, %"))
        self.periodsmodel.setHeaderData(7, Qt.Horizontal, self.tr("C, %"))
        self.periodsmodel.setHeaderData(8, Qt.Horizontal, self.tr("Vatiate,%"))
        self.periodsmodel.setHeaderData(9, Qt.Horizontal, self.tr("Note"))
        self.periodsmodel.setHeaderData(10, Qt.Horizontal, self.tr("User id"))

    def setDayModelHeaders(self): 
        self.daysmodel.setHeaderData(0, Qt.Horizontal, self.tr("id"))  # id
        self.daysmodel.setHeaderData(1, Qt.Horizontal, self.tr("Date"))  # Дата 
        self.daysmodel.setHeaderData(2, Qt.Horizontal, self.tr("Eaten\nweight,\ng")) # Вес\nсъеденного,\nг 
        self.daysmodel.setHeaderData(3, Qt.Horizontal, self.tr("Energy\nvalue,\nkcal")) #  Б,г
        self.daysmodel.setHeaderData(4, Qt.Horizontal, self.tr("P,\ng")) #  Б,г
        self.daysmodel.setHeaderData(5, Qt.Horizontal, self.tr("F,\ng")) #  Ж,г
        self.daysmodel.setHeaderData(6, Qt.Horizontal, self.tr("C,\ng")) #  У,г
        self.daysmodel.setHeaderData(7, Qt.Horizontal, self.tr("My\nweight,\nkg")) # Мой\nвес,\nкг
        self.daysmodel.setHeaderData(8, Qt.Horizontal, self.tr("Waist,\ncm"))
        self.daysmodel.setHeaderData(9, Qt.Horizontal, self.tr("Hips,\ncm"))

    def setMealModelHeaders(self):
        self.mealmodel.setHeaderData(0, Qt.Horizontal, self.tr("id"))   #id
        self.mealmodel.setHeaderData(1, Qt.Horizontal, self.tr("Time"))   #Время
        self.mealmodel.setHeaderData(2, Qt.Horizontal, self.tr("products_id"))  #id Продукта (блюда)
        self.mealmodel.setHeaderData(3, Qt.Horizontal, self.tr("Product (dish) name"))  #Продукт (блюдо)
        self.mealmodel.setHeaderData(4, Qt.Horizontal, self.tr("Weight,\ng"))  #Вес, г
        self.mealmodel.setHeaderData(5, Qt.Horizontal, self.tr("Calorie content\nper 100 g,\nkcal"))  #Калорийность 100 г, ккал
        self.mealmodel.setHeaderData(6, Qt.Horizontal, self.tr("Calorie\ncontent,\n kcal"))  #Калорийность,\n ккал
        self.mealmodel.setHeaderData(7, Qt.Horizontal, self.tr("P,\ng"))  # Б,г
        self.mealmodel.setHeaderData(8, Qt.Horizontal, self.tr("F,\ng"))  # Ж,г
        self.mealmodel.setHeaderData(9, Qt.Horizontal, self.tr("C,\ng"))  # У,г

    def signin(self, login, password):
        self.current_users_id = -1
        self.current_user_name = 'Guest'
        # user_gender = -1
        user_password = ''
        query = QSqlQuery(self.db)
        query.prepare("SELECT `id`, `login`, `name`, `password`, `gender` FROM `users` WHERE `login` = ?")
        query.bindValue(0, login)
        query.exec()
        if query.next():
            user_password = query.record().value("password")
            if Database.verify_password(password, user_password):
                self.current_users_id = int(query.record().value("id"))
                self.current_user_name = str(query.record().value("name"))
                # user_gender = int(query.record().value("gender"))
        return self.current_users_id, self.current_user_name

    def checkExistingLogin(self, login):
        query = QSqlQuery(self.db)
        query.prepare("SELECT `login` FROM `users` WHERE `login` = ?")
        query.bindValue(0, login)
        query.exec()
        print(login)
        return query.next()

    def signup(self, login: str, name: str, bdate: QDate, gender: int, password: str):
        self.current_users_id = -1
        self.current_user_name = 'Guest'
        password = Database.hash_password(password)
        query = QSqlQuery(self.db)
        query.prepare("INSERT INTO `users` (`login`, `name`, `password`, `birthdate`, `gender`)  VALUES (?, ?, ?, ?, ?)")
        query.bindValue(0, login)
        query.bindValue(1, name)
        query.bindValue(2, password)
        query.bindValue(3, bdate)
        query.bindValue(4, gender)
        result = query.exec()
        if result:
            self.current_user_name = name
        query.exec("SELECT LAST_INSERT_ROWID();")
        if query.next():
            self.current_users_id = int(query.record().value(0))
        return result, self.current_users_id

    @staticmethod
    def hash_password(password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    @staticmethod
    def verify_password(input_password, stored_hash):
        hashed_input_password = hashlib.sha256(input_password.encode()).hexdigest()
        return hashed_input_password == stored_hash

    def appendDay(self, date, weight, waist, hips):
        fld_str = "`mdate`, "
        val_str = "?, "
        if weight>1.0:
            fld_str += "`weight`, "
            val_str += "?, "
        if waist:
            fld_str += "`waist`, "
            val_str += "?, "
        if hips:
            fld_str += "`hips`, "
            val_str += "?, "
        fld_str += "`periods_id`"
        val_str += "?"
        query = QSqlQuery(self.db)
        query.prepare(f"INSERT INTO `days` ({fld_str}) VALUES ({val_str});")
        index = 0
        query.bindValue(index, date)
        if weight>1.0:
            index += 1
            query.bindValue(index, weight)
        if waist:
            index += 1
            query.bindValue(index, waist)
        if hips:
            index += 1
            query.bindValue(index, hips)
        index += 1
        query.bindValue(index, self.current_periods_id)
        result = query.exec()
        id_ = -1
        if result:
            query.exec("SELECT LAST_INSERT_ROWID();")
            if query.next():
                id_ = int(query.value(0))
        return id_


    def editDay(self, id_, date, weight, waist, hips):
        fld_str = "`mdate`=?"
        if weight>1.0:
            fld_str += ", `weight`=?"
        if waist:
            fld_str += ", `waist`=?"
        if hips:
            fld_str += ", `hips`=?"
        query = QSqlQuery(self.db)
        query.prepare(f"UPDATE `days` SET {fld_str} WHERE `id`=?;")
        index = 0
        query.bindValue(index, date)
        if weight>1.0:
            index += 1
            query.bindValue(index, weight)
        if waist:
            index += 1
            query.bindValue(index, waist)
        if hips:
            index += 1
            query.bindValue(index, hips)
        index += 1
        query.bindValue(index, id_)
        result = query.exec()

    def deleteDay(self, id_):
        query = QSqlQuery(self.db)
        query.prepare("DELETE FROM `days` WHERE `id`=?;")
        query.bindValue(0, id_)
        return query.exec()

    def dayMealCount(self, id_):
        query = QSqlQuery(self.db)
        query.prepare("SELECT count() FROM `meals` WHERE `days_id`=?;")
        query.bindValue(0, id_)
        query.exec()
        count = 0
        if query.next():
            count = int(query.record().value(0))
        return count

    def dayCount(self):
        query = QSqlQuery(self.db)
        query.exec("SELECT count() FROM `days`;")
        count = 0
        if query.next():
            count = int(query.record().value(0))
        return count

    def getLastWeight(self):
        weight = 0.0
        print("self.current_periods_id",self.current_periods_id)
        query = QSqlQuery(self.db)
        query.prepare("SELECT max(`mdate`), `weight` FROM `days` WHERE `periods_id`=? AND `weight` IS NOT NULL;")
        query.bindValue(0, self.current_periods_id)
        query.exec()
        if query.next():
            if query.value('weight'):
                weight = float(query.value('weight'))
            else:
                query.prepare("SELECT `weight` FROM `periods` WHERE `id`=?;")
                query.bindValue(0, self.current_periods_id)
                query.exec()
                if query.next():
                    if query.value('weight'):
                        weight = float(query.value('weight'))
        return weight

    def execDaysQuery(self):
        query = QSqlQuery(self.db)
        query.prepare("SELECT days.id, days.mdate, "
                "(SELECT sum(meals.weight) FROM meals WHERE meals.days_id=days.id) AS mweight, "
                "round((SELECT sum(meals.weight*products.calory/100.0) FROM meals, products WHERE meals.days_id=days.id AND meals.products_id=products.id),0) AS ccal, "
                "round((SELECT sum(meals.weight*products.protein/100.0) FROM meals, products WHERE meals.days_id=days.id AND meals.products_id=products.id),1) AS prot, "
                "round((SELECT sum(meals.weight*products.fat/100.0) FROM meals, products WHERE meals.days_id=days.id AND meals.products_id=products.id),1) AS fats, "
                "round((SELECT sum(meals.weight*products.carbohydrate/100.0) FROM meals, products WHERE meals.days_id=days.id AND meals.products_id=products.id),1) AS carb, "
                "days.weight, days.waist, days.hips " 
                "FROM days WHERE days.periods_id=? ORDER BY days.mdate;")
        query.bindValue(0, self.current_periods_id)
        result = query.exec()
        self.daysmodel.setQuery(query)
        self.setDayModelHeaders()
        while self.daysmodel.canFetchMore(): # Чтобы в tvDays выводились все строки, а не 256
            self.daysmodel.fetchMore()
    
    def execDaySumQuery(self):
        sum_w = sum_k = sum_p = sum_f = sum_c = 0.0
        query = QSqlQuery(self.db)
        query.exec("SELECT sum(`meal.weight`) as W, "
            "sum(`meals`.`weight`*`products`.`calory`/100.0),"
            "sum(`meals`.`weight`*`products`.`protein`/100.0),"
            "sum(`meals`.`weight`*`products`.`fat`/100.0),"
            "sum(`meals`.`weight`*`products`.`carbohydrate`/100.0) "
            "FROM `meals`, `products` WHERE `meals`.`products_id`=`products`.`id`;")
        if query.next():
            sum_w = float(query.value(0))
            sum_k = float(query.value(1))
            sum_p = float(query.value(2))
            sum_f = float(query.value(3))
            sum_c = float(query.value(4))

            daycount = self.dayCount()
            if daycount>0:
                sum_w /= daycount
                sum_k /= daycount
                sum_p /= daycount
                sum_f /= daycount
                sum_c /= daycount
        k_color = self.norm_color
        p_color = self.norm_color
        f_color = self.norm_color
        c_color = self.norm_color

        norm_kcal, norm_prot, norm_fat, norm_carb, pm_prot, pm_fat, pm_carb = self.calcNormCPFC()

        if sum_k<1200.0:
            k_color = self.deficit_color
        elif sum_k>norm_kcal:
            k_color = self.excess_color
        if sum_p<(norm_prot-pm_prot):
            p_color = self.deficit_color
        elif sum_p>(norm_prot+pm_prot):
            p_color = self.excess_color
        if sum_f<(norm_fat-pm_fat):
            f_color = self.deficit_color
        elif sum_f>(norm_fat+pm_fat):
            f_color = self.excess_color
        if sum_c<(norm_carb-pm_carb):
            c_color = self.deficit_color
        elif sum_c>(norm_carb+pm_carb):
            c_color = self.excess_color
        sum_param = self.tr('<span style="font-style:italic">Daily average:</span>'
                    f' {sum_w:.1f} g'
                    f'<font color="{k_color}">&nbsp;&nbsp;  {sum_k:.1f} kcal </font>'
                    f'<font color="{p_color}">&nbsp;&nbsp; P: {sum_p:.1f} g</font>'
                    f'<font color="{f_color}">&nbsp;&nbsp; F: {sum_f:.1f} g</font>'
                    f'<font color="{c_color}">&nbsp;&nbsp; C: {sum_c:.1f} g</font>')
        
        tooltip = self.tr(f'Norm:<br><font color="{self.norm_color}">'
            f'&nbsp;&nbsp; 1200-{norm_kcal:.1f} kcal<br>'
            f'&nbsp;&nbsp; P: {norm_prot:.1f}±{pm_prot:.1f} g<br>'
            f'&nbsp;&nbsp; F: {norm_fat:.1f}±{pm_fat:.1f} g<br>'
            f'&nbsp;&nbsp; C: {norm_carb:.1f}±{pm_carb:.1f} g.</font><br>'
            f'<font color="{self.deficit_color}">█ This color shows values that are <b>less</b> than the norm</font><br>'
            f'<font color="{self.norm_color}">█ this color shows values that <b>correspond</b> to the norm</font><br>'
            f'<font color="{self.excess_color}">█ this color shows values that <b>exceed</b> the norm.</font>'
            )

        return sum_param, tooltip

    def execMealSumQuery(self, id_, mdate):
        sum_w = sum_k = sum_p = sum_f = sum_c = 0.0
        query = QSqlQuery(self.db)
        query.prepare("SELECT sum(meals.weight) AS w, "
            "sum(meals.weight*products.calory/100.0) AS kc, "
            "sum(meals.weight*products.protein/100.0) AS prot, "
            "sum(meals.weight*products.fat/100.0) AS fats, "
            "sum(meals.weight*products.carbohydrate/100.0) AS carb "
            "FROM meals, products WHERE meals.products_id=products.id "
            "AND meals.days_id=?")
        query.bindValue(0, id_)
        print("execMealSunQuery", id_)
        query.exec()
        if query.next():
            if query.value("w"):
                sum_w = float(query.value("w"))
            if query.value("kc"):
                sum_k = float(query.value("kc"))
            if query.value("prot"):
                sum_p = float(query.value("prot"))
            if query.value("fats"):
                sum_f = float(query.value("fats"))
            if query.value("carb"):
                sum_c = float(query.value("carb"))
        k_color = self.norm_color
        p_color = self.norm_color
        f_color = self.norm_color
        c_color = self.norm_color

        norm_kcal, norm_prot, norm_fat, norm_carb, pm_prot, pm_fat, pm_carb = self.calcNormCPFC()

        if sum_k<1200.0:
            k_color = self.deficit_color
        elif sum_k>norm_kcal:
            k_color = self.excess_color
        if sum_p<(norm_prot-pm_prot):
            p_color = self.deficit_color
        elif sum_p>(norm_prot+pm_prot):
            p_color = self.excess_color
        if sum_f<(norm_fat-pm_fat):
            f_color = self.deficit_color
        elif sum_f>(norm_fat+pm_fat):
            f_color = self.excess_color
        if sum_c<(norm_carb-pm_carb):
            c_color = self.deficit_color
        elif sum_c>(norm_carb+pm_carb):
            c_color = self.excess_color

        sum_param = self.tr(f'<span style="font-style:italic">Total {mdate} average:</span>'
                    f' {sum_w:.1f} g'
                    f'<font color="{k_color}">&nbsp;&nbsp;  {sum_k:.1f} kcal </font>'
                    f'<font color="{p_color}">&nbsp;&nbsp; P: {sum_p:.1f} g</font>'
                    f'<font color="{f_color}">&nbsp;&nbsp; F: {sum_f:.1f} g</font>'
                    f'<font color="{c_color}">&nbsp;&nbsp; C: {sum_c:.1f} g</font>')
        
        tooltip = self.tr(f'Norm:<br><font color="{self.norm_color}">'
            f'&nbsp;&nbsp; 1200-{norm_kcal:.1f} kcal<br>'
            f'&nbsp;&nbsp; P: {norm_prot:.1f}±{pm_prot:.1f} g<br>'
            f'&nbsp;&nbsp; F: {norm_fat:.1f}±{pm_fat:.1f} g<br>'
            f'&nbsp;&nbsp; C: {norm_carb:.1f}±{pm_carb:.1f} g.</font><br>'
            f'<font color="{self.deficit_color}">█ This color shows values that are <b>less</b> than the norm</font><br>'
            f'<font color="{self.norm_color}">█ this color shows values that <b>correspond</b> to the norm</font><br>'
            f'<font color="{self.excess_color}">█ this color shows values that <b>exceed</b> the norm.</font>'
            )
        return sum_param, tooltip

    def calcNormCPFC(self): #, double &kcal, double &prot, double &fat, double &carb, double &pm_prot, double &pm_fat, double &pm_carb
        query = QSqlQuery(self.db)
        query.prepare("SELECT `birthdate`, `gender` FROM `users` WHERE `id`=?;")
        query.bindValue(0, self.current_users_id)
        query.exec()
        print(f"calcNormCPFC  user_id = {self.current_users_id}")
        if query.next():
            birhdate = indicators.convertToDate(str(query.value("birthdate")))
            old =indicators.calcAge(birhdate)
            sex = int(query.value("gender"))
            print(f'old = {old}  sex = {sex}')

        query.prepare("SELECT * FROM `periods` WHERE `id`=?;")
        query.bindValue(0, self.current_periods_id)
        query.exec()
        if query.next():
            w = float(query.value("weight"))
            h = float(query.value("height"))
            i = int(query.value("activity"))
            prot_norm = float(query.value("prot"))/100
            fat_norm = float(query.value("fat"))/100
            carb_norm = float(query.value("carb"))/100
            plus_minus = float(query.value("variate"))/100   # например +- 2.5% от нормы
            coefa = indicators.activityData(i)
        query.prepare("SELECT max(`mdate`), `weight` FROM `days` WHERE `periods_id`=? AND `weight` IS NOT NULL;")
        if query.next():
            w = query.value("weight").toDouble()

        kmj = indicators.fMaffinJeor(w,h,old,sex)
        kcal = coefa*kmj
        prot = kcal*prot_norm/4
        fat = kcal*fat_norm/9
        carb = kcal*carb_norm/4
        pm_prot = kcal*plus_minus/4
        pm_fat = kcal*plus_minus/9
        pm_carb = kcal*plus_minus/4
        #    qDebug() << prot << "+-" << pm_prot;
        #    qDebug() << fat << "+-" << pm_fat;
        #    qDebug() << carb << "+-" << pm_carb;
        return kcal, prot, fat, carb, pm_prot, pm_fat, pm_carb

    def execMealQuery(self, id_, mdate):
        query = QSqlQuery(self.db)
        query.prepare("SELECT meals.id, meals.mtime, meals.products_id, "
                        "products.name, meals.weight, products.calory, "
                        "round(products.calory*meals.weight/100.0, 1) as ccal, "
                        "round(products.protein*meals.weight/100.0, 1) as prot, "
                        "round(products.fat*meals.weight/100.0, 1) as fat, "
                        "round(products.carbohydrate*meals.weight/100.0, 1) as carb "
                        "FROM meals, products WHERE meals.products_id=products.id AND meals.days_id=? "
                        "ORDER BY meals.mtime")
        query.bindValue(0, id_)
        query.exec()
        self.mealmodel.setQuery(query)
        self.setMealModelHeaders()

    def appendPeriod(self, start_date, height, weight, activity, prot, fat, carb, variation, note):
        query = QSqlQuery(self.db)
        query.prepare("INSERT INTO `periods` (`startdate`, `height`, `weight`, `activity`, `prot`, `fat`, `carb`, `variate`, `note`, `users_id`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);")
        query.bindValue(0, start_date)
        query.bindValue(1, height)
        query.bindValue(2, weight)
        query.bindValue(3, activity)
        query.bindValue(4, prot)
        query.bindValue(5, fat)
        query.bindValue(6, carb)
        query.bindValue(7, variation)
        query.bindValue(8, note)
        query.bindValue(9, self.current_users_id)
        result = query.exec()
        id_ = -1
        query.exec("SELECT LAST_INSERT_ROWID();")
        if query.next():
            id_ = int(query.record().value(0))
        return id_

    def editPeriod(self, id_, start_date, height, weight, activity, prot, fat, carb, variation, note):
        query = QSqlQuery(self.db)
        query.prepare("UPDATE `periods` SET `startdate`=?, `height`=?, `weight`=?, `activity`=?, `prot`=?, `fat`=?, `carb`=?, `variate`=?, `note`=? WHERE `id`=?;")
        query.bindValue(0, start_date)
        query.bindValue(1, height)
        query.bindValue(2, weight)
        query.bindValue(3, activity)
        query.bindValue(4, prot)
        query.bindValue(5, fat)
        query.bindValue(6, carb)
        query.bindValue(7, variation)
        query.bindValue(8, note)
        query.bindValue(9, id_)
        self.db.transaction()
        result = query.exec()
        self.db.commit()
        print(result, id_, start_date, height, weight, activity, prot, fat, carb, variation, note)
        return result

    def periodDayCount(self, id_):
        query = QSqlQuery(self.db)
        query.prepare("SELECT count() FROM `days` WHERE `periods_id`=?;")
        query.bindValue(0, id_)
        query.exec()
        count = 0
        if query.next():
            count = int(query.record().value(0))
        return count

    def deletePeriod(self, id_):
        query = QSqlQuery(self.db)
        query.prepare("DELETE FROM `periods` WHERE `id`=?;")
        query.bindValue(0, id_)
        return query.exec()

    def execPeriodQuery(self):
        query = QSqlQuery(self.db)
        query.prepare("SELECT * FROM `periods` WHERE `users_id`=?;")
        query.bindValue(0, self.current_users_id)
        query.exec()
        self.periodsmodel.setQuery(query)
        self.setPeriodModelHeaders()

    def appendFood(self, products_id, is_group, name, calory, prot, fat, carb):
        query = QSqlQuery(self.db)
        if is_group==1:
            query.prepare("INSERT INTO `products` (`name`, `isgroup`, `products_id`)  VALUES (?, ?, ?);")
            query.bindValue(0, name)
            query.bindValue(1, is_group)
            query.bindValue(2, products_id)
        else:
            query.prepare("INSERT INTO `products` (`name`, `isgroup`, `calory`, `protein`, `fat`, `carbohydrate`, `products_id`)  VALUES (?, ?, ?, ?, ?, ?, ?);")
            query.bindValue(0, name)
            query.bindValue(1, is_group)
            query.bindValue(2, calory)
            query.bindValue(3, prot)
            query.bindValue(4, fat)
            query.bindValue(5, carb)
            query.bindValue(6, products_id)
        query.exec()
        id_ = -1
        query.exec("SELECT LAST_INSERT_ROWID();")
        if query.next():
            id_ = int(query.record().value(0))
        return id_

    def editFood(self, id_, is_group, name, calory, prot, fat, carb):
        query = QSqlQuery(self.db)
        if is_group==1:
            query.prepare("UPDATE `products` SET `name`=? WHERE `id`=?;")
            query.bindValue(0, name)
            query.bindValue(1, id_)
        else:
            query.prepare("UPDATE `products` SET `name`=?, `calory`=?, `protein`=?, `fat`=?, `carbohydrate`=? WHERE `id`=?;")
            query.bindValue(0, name)
            query.bindValue(1, calory)
            query.bindValue(2, prot)
            query.bindValue(3, fat)
            query.bindValue(4, carb)
            query.bindValue(5, id_)
        return query.exec()

    def checkNoFoodDelete(self, id_):
        query = QSqlQuery(self.db)
        query.prepare("SELECT count() FROM `meals` WHERE `products_id`=?;")
        query.bindValue(0, id_)
        query.exec()
        count = 0
        if query.next():
            count = query.record().value(0)
        return count > 0

    def deleteFood(self, id_):
        query = QSqlQuery(self.db)
        query.prepare("DELETE FROM `products` WHERE `id`=?;")
        query.bindValue(0, id_)
        return query.exec()

    def moveFood(self, newparent_id, item_id):
        query = QSqlQuery(self.db)
        query.prepare("UPDATE `products` SET `parent_id`=? WHERE `id`=?;")
        query.bindValue(0, newparent_id)
        query.bindValue(1, item_id)
        return query.exec()

    def appendMealToDay(self, time, weight, days_id, products_id):
        query = QSqlQuery(self.db)
        query.prepare("INSERT INTO `meals` (`mtime`, `weight`, `days_id`, `products_id`)  VALUES (?, ?, ?, ?);")
        query.bindValue(0, time.toString("hh:mm"))
        query.bindValue(1, weight)
        query.bindValue(2, days_id)
        query.bindValue(3, products_id)
        return query.exec()

    def appendMealToDay1(self, meal_list):
        self.db.transaction()
        query = QSqlQuery(self.db)
        query.prepare("INSERT INTO `meals` (`mtime`, `weight`, `days_id`, `products_id`)  VALUES (?, ?, ?, ?);")
        for meal in meal_list:
            query.bindValue(0, meal['time'].toString("hh:mm"))
            query.bindValue(1, meal['weight'])
            query.bindValue(2, meal['days_id'])
            query.bindValue(3, meal['products_id'])
            query.exec()
        self.db.commit()
