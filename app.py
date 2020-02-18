import os.path
import csv
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView

from panel1 import Panel1
from panel2 import Panel2

Form, Window = uic.loadUiType("all.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)

class RootUI:
    def __init__(self, widget, panel1, panel2):
        self.state = 0
        self.widget = widget
        self.panel1 = panel1
        self.panel2 = panel2
        self.currentPanel = None
        self.placeHolder = None
        
        pass

    def setup(self):
        self.prevButton = self.widget.findChild(QPushButton, "prevButton")
        self.nextButton = self.widget.findChild(QPushButton, "nextButton")

        self.panel1.setup()
        self.panel2.setup()

        self.placeholder = self.widget.findChild(QWidget, "placeholder")

        layout = self.placeholder.layout() 

        if self.state == 0:
            self.currentPanel = self.panel1            
        else:
            self.currentPanel = self.panel2            

        self.prevButton.clicked.connect(self.changeState)
        self.nextButton.clicked.connect(self.changeState)
        
        self.updateUI()

    def updateUI(self):
        layout = self.placeholder.layout()

        print("layout", layout.count())
        if layout.count() > 0:
            childWidget = layout.takeAt(0).widget()
            
            layout.removeWidget(childWidget)
            childWidget.setParent(None)

        if self.state == 0:
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(True)
            layout.addWidget(self.panel1.getWidget())
        else:
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(False)
            layout.addWidget(self.panel2.getWidget())

    def changeState(self):
        print(self.state)
        self.state = 1 - self.state
        self.updateUI()

panel1 = Panel1()
panel2 = Panel2()

rootUI = RootUI(window, panel1, panel2)
rootUI.setup()

window.show()
app.exec_()
