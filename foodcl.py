# -*-coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import sys
import mainwindow

app = QApplication(sys.argv)
ico = QIcon('./resources/foodcl.png')
app.setWindowIcon(ico)
window = mainwindow.MainWindow()
window.show()
sys.exit(app.exec_())
