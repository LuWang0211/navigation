import os.path
import csv
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QHeaderView

Form, Window = uic.loadUiType("panel2.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)

panel2 = window.findChild(QWidget, "panel2")

class Panel2:
    def __init__(self):
        self.widget = panel2
        pass

    def getWidget(self):
        return self.widget

    def setup(self):
        pass

    def updateUI(self):
        pass