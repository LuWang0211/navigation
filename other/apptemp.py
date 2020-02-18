import os.path
import csv
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHeaderView

Form, Window = uic.loadUiType("apptemp_0.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

tableWidget = window.findChild(QTableWidget, "shoppingList")

print(tableWidget)

def setupTableWidget(tableWidget):
    header = tableWidget.horizontalHeader()
           
    header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
    header.setSectionResizeMode(1, QHeaderView.Stretch)
    header.setSectionResizeMode(2, QHeaderView.Fixed)
    header.resizeSection(2, 80)
    header.setSectionResizeMode(3, QHeaderView.Fixed)
    header.resizeSection(3, 80)

def loadDataToTableWidget(tableWidget):

    numberOfItems = 0

    items = []

    with open(os.path.join(os.path.dirname(__file__), 'shoppingList.csv'), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            items.append([row[0], row[1]])
            numberOfItems += 1

    tableWidget.setRowCount(numberOfItems)

    rowId = 0

    for item in items: 
        rowNumberWidgetItem = QTableWidgetItem(str(rowId + 1))
        nameWidgetItem = QTableWidgetItem(item[0])
        aisleWidgetItem = QTableWidgetItem(item[1])
        statusWidgetItem = QTableWidgetItem("pending")

        tableWidget.setItem(rowId, 0, rowNumberWidgetItem)
        tableWidget.setItem(rowId, 1, nameWidgetItem)
        tableWidget.setItem(rowId, 2, aisleWidgetItem)
        tableWidget.setItem(rowId, 3, statusWidgetItem)

        rowId += 1

setupTableWidget(tableWidget)
loadDataToTableWidget(tableWidget)

app.exec_()