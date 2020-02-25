import os.path
import csv
import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPen, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, \
     QGraphicsView, QGraphicsScene, QLabel, QGraphicsItem, QGraphicsPixmapItem

Form, Window = uic.loadUiType("panel2.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)

panel2 = window.findChild(QWidget, "panel2")

class MyForm(Form):
    def resizeEvent(self, event):
        print("resize")
        Form.resizeEvent(self, event)

class Panel2:
    def __init__(self, dataContainer, camera, locationService):
        self.widget = panel2
        self.dc = dataContainer
        self.camera = camera
        self.locationService = locationService
        self.mapGraphicsScene = None
        self.mapGraphicsView = None
        self.cameraGraphicsView = None
        self.cameraGraphicsViewScene = None
        self.shoppingCart = None
        self.shoppingCartLocation = None        
        self.anchor_coordinates = {}
        self.aisle_anchor_map = {}
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

        with open(os.path.join(os.path.dirname(__file__), 'aisle_anchor.csv'), newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                aisle = int(row[0])
                anchor = row[1]                
                self.aisle_anchor_map[aisle] = anchor

        
        # Setup QTableWidget
        self.tableWidget = window.findChild(QTableWidget, "shoppingList")

        header = self.tableWidget.horizontalHeader()
           
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.resizeSection(2, 80)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.resizeSection(3, 80)

        # Get shopping cart element
    
        self.shoppingCart = window.findChild(QLabel, "cart")
        
        # Setup QGraphicsScene
        self.mapGraphicsView = window.findChild(QGraphicsView, "graphicsView")
        self.mapGraphicsScene = QGraphicsScene(0, 0, 815, 236)
        self.mapGraphicsView.setScene(self.mapGraphicsScene)
        self.mapGraphicsView.setStyleSheet("background: transparent")

        # Setup camera view
        self.cameraGraphicsView = window.findChild(QGraphicsView, "cameraVideo")
        rect = self.cameraGraphicsView.geometry()
        self.cameraGraphicsViewScene = QGraphicsScene(0, 0, 300, 130)
        # self.cameraGraphicsViewScene = QGraphicsScene(self.cameraGraphicsView)
        self.cameraGraphicsView.setScene(self.cameraGraphicsViewScene)

        # Bring to front
        self.mapGraphicsView.raise_()

        self.shoppingCartLocation = 'A'
        
    def updateUI(self):
        # display shopping route
        shoppingItems = self.dc.get_shopping_list_items()

        # print(shoppingItems)

        numberOfItems = len(shoppingItems)

        sortedItems = sorted(shoppingItems, key=lambda item: int(item.aisle))

        self.tableWidget.clearContents()

        self.tableWidget.setRowCount(numberOfItems)

        rowId = 0

        for item in sortedItems: 
            rowNumberWidgetItem = QTableWidgetItem(str(rowId + 1))
            nameWidgetItem = QTableWidgetItem(item.name)
            nameWidgetItem.setTextAlignment(0x84)
            aisleWidgetItem = QTableWidgetItem(f"Aisle {item.aisle}")
            aisleWidgetItem.setTextAlignment(0x84)
            print(aisleWidgetItem)
            statusWidgetItem = QTableWidgetItem("pending")
            # if (self.count in [5, 6, 8]):
            #     statusWidgetItem = QTableWidgetItem("Checked")
            # else:
            #     statusWidgetItem = QTableWidgetItem("pending")
            self.tableWidget.setItem(rowId, 0, rowNumberWidgetItem)            
            self.tableWidget.setItem(rowId, 1, aisleWidgetItem)
            self.tableWidget.setItem(rowId, 2, nameWidgetItem)
            self.tableWidget.setItem(rowId, 3, statusWidgetItem)

            rowId += 1

        route = self.dc.calculateRoutePlan()

        print("shopping route", route)

        self.mapGraphicsScene.clear()

        pen = QPen(Qt.red, 3)

        if len(route) > 1:
            start = route.pop(0)

            while len(route) > 0:
                next_ = route.pop(0)

                [x1, y1] = self.anchor_coordinates[start]
                [x2, y2] = self.anchor_coordinates[next_]
                self.mapGraphicsScene.addLine( x1, y1, x2, y2, pen)
                start = next_

        # display cart location
        self.update_cart_location()

        # update camera image
        self.update_camera_image()

    def update_cart_location(self):
        """ Display the location of the shopping cart """
        if self.shoppingCartLocation not in self.anchor_coordinates:
            # if the anchor is not registerd, do nothing
            return

        [x, y] = self.anchor_coordinates[self.shoppingCartLocation]

        current_geometry = self.shoppingCart.geometry()

        y = current_geometry.y()

        self.shoppingCart.move(x - current_geometry.width() / 2, y)

    def update_camera_image(self):
        image_arrary = self.dc.get_last_captured_image()

        if image_arrary is None:
            return
        if self.cameraGraphicsViewScene is None:
            return

        qpixmap = self._convert_numpy_to_qpixmap(image_arrary) 

        # Create a scene item and add it to scene
        scene_width, scene_height = (self.cameraGraphicsViewScene.width(), self.cameraGraphicsViewScene.height())

        # Scale the QPixmap, so it fits in the graphic scene
        qpixmap = qpixmap.scaled(QSize(scene_width, scene_height), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        rect = qpixmap.rect()
        width, height = (rect.width(), rect.height())

        item = QGraphicsPixmapItem(qpixmap)

        # Center the scene item horizotally and vertically
        if scene_width > width:
            item.setX( (scene_width - width) // 2)
        if scene_height > height:
            item.setY( (scene_height - height) // 2)

        self.cameraGraphicsViewScene.clear()
        self.cameraGraphicsViewScene.addItem(item)

    def onLocationChanged(self, new_location):
        print(f'panel2 location changed to: {new_location}')

        if new_location in self.aisle_anchor_map:
            self.shoppingCartLocation = self.aisle_anchor_map[new_location]
            self.update_cart_location()

    def onImageCaptured(self):
        self.update_camera_image()

    def _convert_numpy_to_qpixmap(self, image_array):
        #image_array = np.transpose(image_array, (0,1,2)).copy()
        image_array = image_array.copy()
        shape = image_array.shape
        qimage = QImage(image_array, shape[1], shape[0], QImage.Format_RGB32) 

        return QPixmap.fromImage(qimage)