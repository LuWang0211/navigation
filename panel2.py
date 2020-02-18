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
    def __init__(self, dataContainer):
        self.widget = panel2
        self.dc = dataContainer
        pass

    def getWidget(self):
        return self.widget

    def setup(self):
        self.tableWidget = window.findChild(QTableWidget, "shoppingList")

        header = self.tableWidget.horizontalHeader()
           
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.resizeSection(2, 80)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.resizeSection(3, 80)
        
    def updateUI(self):

        shoppingItems = self.dc.get_shopping_list_items()

        numberOfItems = len(shoppingItems)

        self.tableWidget.clearContents()

        self.tableWidget.setRowCount(numberOfItems)

        rowId = 0

        for item in shoppingItems: 
            rowNumberWidgetItem = QTableWidgetItem(str(rowId + 1))
            nameWidgetItem = QTableWidgetItem(item.name)
            aisleWidgetItem = QTableWidgetItem(f"Aisle {item.aisle}")
            statusWidgetItem = QTableWidgetItem("pending")

            self.tableWidget.setItem(rowId, 0, rowNumberWidgetItem)
            self.tableWidget.setItem(rowId, 1, nameWidgetItem)
            self.tableWidget.setItem(rowId, 2, aisleWidgetItem)
            self.tableWidget.setItem(rowId, 3, statusWidgetItem)

            rowId += 1

        pass