import os.path
import csv
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QHeaderView

Form, Base = uic.loadUiType("panel1.ui")

app = QApplication([])
base = Base()
form = Form()
form.setupUi(base)

panel1 = base

class Panel1:
    def __init__(self):
        self.widget = panel1
        pass

    def getWidget(self):
        return self.widget

    def setup(self):
        pass

    def updateUI(self):
        pass