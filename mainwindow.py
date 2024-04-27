# -*-coding: utf-8 -*-

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLabel, QPushButton
from PyQt5.QtSql import QSqlDatabase

from database import Database
from foodtree import FoodTree
import ui_mainwindow
from wdgfood import WdgFood
from wdgperiods import WdgPeriods
from wdgmeals import WdgMeals
from wdgeditmeal import WdgEditMeal


class MainWindow(QMainWindow):

    SIGNIN, SIGNUP, FOOD, PERIOD, DAYS, EDIT_MEAL  = range(6)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.ui = ui_mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.lbUser = QLabel("User: Guest")
        self.pbLogout = QPushButton()
        self.pbLogout.setText("Logout")
        maintoolbar = self.addToolBar('mainToolBar')
        maintoolbar.setObjectName('mainToolBar')
        maintoolbar.addWidget(self.lbUser)
        maintoolbar.addSeparator()
        maintoolbar.addWidget(self.pbLogout)
        self.pbLogout.setEnabled(False)
        # maintoolbar.addSeparator()

        # Hide tab line
        # self.ui.tabWidget.tabBar().setStyleSheet(""" QTabBar::tab { width: 0; height: 0; margin: 0; padding: 0; border: none; } """)

        self.wdgfood = WdgFood()
        self.ui.tabWidget.addTab(self.wdgfood, "Food")

        self.wdgperiods = WdgPeriods()
        self.ui.tabWidget.addTab(self.wdgperiods, "Periods")
        self.ui.tabWidget.currentChanged.connect(self.wdgperiods.widgetShow)
        self.wdgperiods.gotoDays.connect(self.goDays)

        self.wdgmeals = WdgMeals()
        self.ui.tabWidget.addTab(self.wdgmeals, "Meals")
        self.ui.tabWidget.currentChanged.connect(self.wdgmeals.widgetShow)
        self.wdgmeals.gotoEditMeal.connect(self.goEditMeal)

        self.wdgeditmeal = WdgEditMeal()
        self.ui.tabWidget.addTab(self.wdgeditmeal, "Edit meal")

        self.database = Database(self)

        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionFood.triggered.connect(self.food)
        self.ui.pbGotoSignup.clicked.connect(self.goSignup)
        self.ui.pbSignin.clicked.connect(self.signin)
        self.ui.pbSignup.clicked.connect(self.signup)
        self.pbLogout.clicked.connect(self.logout)
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.actionAbout_Qt.triggered.connect(self.aboutQt)

        if self.database.connectToSQLiteDatabase("./db/foodcl_db.sqlite3"):
            print("db Ok")
            self.wdgfood.foodtree.setDatabase(self.database)
            self.wdgperiods.setDatabase(self.database)
            self.wdgmeals.setDatabase(self.database)
            self.wdgeditmeal.setDatabase(self.database)
        self.copyright = '<p><span style="font-size:10pt; color:#000055;">Copyright &copy; 2024 Big Pond</span></p>'
        self.readSettings()
            
    def writeSettings(self):
        settings = QSettings('foodcl.ini', QSettings.IniFormat)
        settings.beginGroup(self.objectName())
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue('windowState', self.saveState())
        settings.setValue("wdgeditmeal_splitter_state", self.wdgeditmeal.ui.splitter.saveState())
        settings.endGroup()

    def readSettings(self):
        settings = QSettings('foodcl.ini', QSettings.IniFormat)
        settings.beginGroup(self.objectName())
        # cnt = settings.contains("geometry")
        # if cnt:
        #     self.restoreGeometry(settings.value('geometry'))
        # cnt = settings.contains("windowState")
        # if cnt:
        #     self.restoreState(settings.value('windowState'))
        # cnt = settings.contains("wdgeditmeal_splitter_state")
        # if cnt:
        #     self.wdgeditmeal.ui.splitter.restoreState(settings.value("wdgeditmeal_splitter_state"))
        # settings.endGroup()
        if settings.contains("geometry"):
            self.restoreGeometry(settings.value('geometry'))
        if settings.contains("windowState"):
            self.restoreState(settings.value('windowState'))
        if settings.contains("wdgeditmeal_splitter_state"):
            self.wdgeditmeal.ui.splitter.restoreState(settings.value("wdgeditmeal_splitter_state"))
        settings.endGroup()

    def closeEvent(self, event):
        self.writeSettings()
        super(MainWindow, self).closeEvent(event)

    def food(self):
        self.ui.tabWidget.setCurrentIndex(MainWindow.FOOD)
        self.wdgfood.foodtree.clear()
        self.wdgfood.foodtree.readData()

    def goSignup(self):
        self.ui.tabWidget.setCurrentIndex(MainWindow.SIGNUP)

    def goDays(self):
        self.ui.tabWidget.setCurrentIndex(MainWindow.DAYS)

    def goEditMeal(self, days_id):
        self.ui.tabWidget.setCurrentIndex(MainWindow.EDIT_MEAL)
        self.wdgeditmeal.current_days_id =days_id

    def signin(self):
        if not self.database.checkExistingLogin(self.ui.leLogin.text()):
            QMessageBox.information(self, 'Sign in', f'There is no user with login "{self.ui.leLogin.text()}". You need to sign up.')
            return
        user_id, user_name = self.database.signin(self.ui.leLogin.text(), self.ui.lePassword.text())
        if user_id==-1:
            QMessageBox.information(self, 'Sign in', 'Incorrect password!')
            return
        self.lbUser.setText(f'User: {user_name}')
        self.ui.tabWidget.setCurrentIndex(MainWindow.PERIOD)
        self.pbLogout.setEnabled(True)

    def signup(self):
        if len(self.ui.leLoginReg.text())<4:
            QMessageBox.information(self, 'Sign up', 'Login must be more than 4 characters long!')
            return
        if len(self.ui.leNameReg.text())<4:
            QMessageBox.information(self, 'Sign up', 'Name must be more than 4 characters long!')
            return
        if self.ui.lePassword1.text()!=self.ui.lePassword2.text():
            QMessageBox.information(self, 'Sign up', 'Password and the confirmation of password do not match!')
            return
        if self.database.checkExistingLogin(self.ui.leLoginReg.text()):
            QMessageBox.information(self, 'Sign up', f'User with login "{self.ui.leLoginReg.text()}" is already present in the database!')
            return

        result, user_id = self.database.signup(self.ui.leLoginReg.text(),
                                           self.ui.leNameReg.text(),
                                           self.ui.deBirthdayReg.date(),
                                           self.ui.cbGenderReg.currentIndex(),
                                           self.ui.lePassword1.text())
        if result:
            QMessageBox.information(self, 'Sign up', 'You have successfully registered!')
            self.lbUser.setText(f'User: {self.ui.leNameReg.text()} id ')
            self.ui.tabWidget.setCurrentIndex(MainWindow.PERIOD)
            self.pbLogout.setEnabled(True)
        else:
            QMessageBox.information(self, 'Sign up', 'The registration attempt failed!')

    def logout(self):
        self.database.current_users_id = -1
        self.database.current_periods_id = -1
        self.database.current_user_name = "Guest"
        self.lbUser.setText(f'User: {self.database.current_user_name}')
        self.ui.tabWidget.setCurrentIndex(MainWindow.SIGNIN)
        self.pbLogout.setEnabled(False)

    def about(self):
        QMessageBox.about(self, self.tr('About'), 
                          '<h2 align="center"><font color="#008000">foodcl 1.0 alpha</font></h2>'
                          '<p align="center"><font color="#000080" face="Times New Roman" size="4">'
                          f'<b>Calorie Counter</b></font></p><p>{self.copyright}</p>')

    def aboutQt(self):
        QMessageBox.aboutQt(self)
