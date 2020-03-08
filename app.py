import os.path
import csv
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage

from camera import Camera, CameraCaptureThread
from location_service import LocationService
from panel1 import Panel1
from panel2 import Panel2
from dataContainer import DataContainer

Form, Window = uic.loadUiType("all.ui")

app = QApplication([])
form = Form()


class ThreadWindow(Window):
    def __init__(self):
        super().__init__()

    def setup(self, dc, locationService):
        self.dc = dc
        self.locationService = locationService
        self.startVideo()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.dc.onImageCaptured(image)
    
    @pyqtSlot(int)
    def setText(self, text):
        self.locationService.onImageIdentified(text)

    def startVideo(self):

        th = CameraCaptureThread(self)
        th.changePixmap.connect(self.setImage)
        th.changecartlocation.connect(self.setText)
        th.start()

        # text = CameraCaptureThread(self)
        # text.changecartlocation.connect(self.setText)
        # text.start()

window = ThreadWindow()

form.setupUi(window)

class RootUI:
    def __init__(self, widget, panel1, panel2, dataContainer):
        self.state = 0
        self.widget = widget
        self.panel1 = panel1
        self.panel2 = panel2
        self.currentPanel = None
        self.placeHolder = None
        self.dc = dataContainer
        self.count = 0
        
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
        self.count  += 1
        # print(self.count )
        layout = self.placeholder.layout()

        if layout.count() > 0:
            childWidget = layout.takeAt(0).widget()

            layout.removeWidget(childWidget)
            childWidget.setParent(None)

        if self.state == 0:
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(True)
            layout.addWidget(self.panel1.getWidget())
            self.panel2.activated = False
            self.panel1.activated = True
            self.panel1.updateUI()
        else:
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(False)
            layout.addWidget(self.panel2.getWidget())
            self.panel1.activated = False
            self.panel2.activated = True
            self.panel2.updateUI()

    def changeState(self):
        self.state = 1 - self.state
        self.updateUI()

dataContainer = DataContainer()

camera = Camera(dataContainer)
locationService = LocationService(camera)

panel1 = Panel1(dataContainer)
panel2 = Panel2(dataContainer, camera, locationService)

dataContainer.setup(panel2)
camera.setup(panel2, locationService)
locationService.setup(panel2)

rootUI = RootUI(window, panel1, panel2, dataContainer)
rootUI.setup()

window.setup(dataContainer, locationService)

window.show()
app.exec_()
