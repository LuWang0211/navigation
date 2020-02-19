import os.path
import csv
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, \
     QGraphicsView, QGraphicsScene

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
        self.graphicsScene = None
        self.graphicsView = None
        self.anchor_coordinates = {}
        pass

    def getWidget(self):
        return self.widget

    def setup(self):
        # Read metadata
        with open(os.path.join(os.path.dirname(__file__), 'anchor_location.csv'), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                anchor = row[0]
                x = int(row[1])
                y = int(row[2])
                self.anchor_coordinates[anchor] = [x, y]
        
        # Setup QTableWidget
        self.tableWidget = window.findChild(QTableWidget, "shoppingList")

        header = self.tableWidget.horizontalHeader()
           
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.resizeSection(2, 80)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.resizeSection(3, 80)
        
        # Setup QGraphicsScene
        self.graphicsView = window.findChild(QGraphicsView, "graphicsView")
        self.graphicsScene = QGraphicsScene(0, 0, 815, 340)
        self.graphicsView.setScene(self.graphicsScene)
        self.graphicsView.setStyleSheet("background: transparent")

        # Bring to front
        self.graphicsView.raise_()
        
    def updateUI(self):

        shoppingItems = self.dc.get_shopping_list_items()

        numberOfItems = len(shoppingItems)

        self.tableWidget.clearContents()

        self.tableWidget.setRowCount(numberOfItems)

        rowId = 0

        for item in shoppingItems: 
            rowNumberWidgetItem = QTableWidgetItem(str(rowId + 1))
            nameWidgetItem = QTableWidgetItem(item.name)
            nameWidgetItem.setTextAlignment(0x84)
            aisleWidgetItem = QTableWidgetItem(f"Aisle {item.aisle}")
            aisleWidgetItem.setTextAlignment(0x84)
            statusWidgetItem = QTableWidgetItem("pending")

            self.tableWidget.setItem(rowId, 0, rowNumberWidgetItem)            
            self.tableWidget.setItem(rowId, 1, aisleWidgetItem)
            self.tableWidget.setItem(rowId, 2, nameWidgetItem)
            self.tableWidget.setItem(rowId, 3, statusWidgetItem)

            rowId += 1

        route = self.dc.calculateRoutePlan()

        print("shopping route", route)

        self.graphicsScene.clear()

        pen = QPen(Qt.red, 3)

        if len(route) > 1:
            start = route.pop(0)

            while len(route) > 0:
                next_ = route.pop(0)

                [x1, y1] = self.anchor_coordinates[start]
                [x2, y2] = self.anchor_coordinates[next_]
                self.graphicsScene.addLine( x1, y1, x2, y2, pen)
                start = next_