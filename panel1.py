import os.path
import csv
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QListWidget, QListWidgetItem
import speech_recognition as sr

Form, Base = uic.loadUiType("panel1.ui")

app = QApplication([])
base = Base()
form = Form()
form.setupUi(base)

panel1 = base

class Panel1:
    def __init__(self, dataContainer):
        self.widget = panel1
        self.dc = dataContainer
        self.item_metadata = {}
        self.ordered_item_metadata = []
        self.current_selected_item_to_add = None

    def getWidget(self):
        return self.widget

    def setup(self):
        self.item_metadata = self.dc.get_item_metadata()

        self.ordered_item_metadata = list(self.item_metadata.values())

        self.combobox = self.widget.findChild(QComboBox, "comboBox")
        self.combobox.currentIndexChanged.connect(self.comboboxCurrentIndexChanged)

        self.addButton = self.widget.findChild(QPushButton, "addButton")
        self.addButton.clicked.connect(self.addButtonClicked)

        self.reduceButton = self.widget.findChild(QPushButton, "reduceButton")
        self.reduceButton.clicked.connect(self.reduceButtonClicked)

        self.voiceButton = self.widget.findChild(QPushButton, "voiceButton")
        self.voiceButton.clicked.connect(self.voiceButtonClicked)

        self.shoppingListWidget = self.widget.findChild(QListWidget, "shoppingItems")


    def updateUI(self):
        self.combobox.clear()

        item_names = [item.name for item in self.ordered_item_metadata]

        self.combobox.insertItems(0, item_names)
        self.current_selected_item_to_add = self.combobox.currentIndex()

        self.updateShoppingListUI()
    
    def updateShoppingListUI(self):
        self.shoppingListWidget.clear()

        shoppingItems = self.dc.get_shopping_list_items()

        for item in shoppingItems:
            self.shoppingListWidget.addItem(QListWidgetItem(f"{item.name} Count: {item.count}"))


    def comboboxCurrentIndexChanged(self, selected_index):
        self.current_selected_item_to_add = selected_index

    def addButtonClicked(self):
        if self.current_selected_item_to_add is None:
            return

        item_to_add = self.ordered_item_metadata[self.current_selected_item_to_add]

        self.dc.add_to_shopping_list(item_to_add)

        self.updateShoppingListUI()

    def reduceButtonClicked(self):
        if self.current_selected_item_to_add is None:
            return

        item_to_reduce = self.ordered_item_metadata[self.current_selected_item_to_add]

        self.dc.reduce_to_shopping_list(item_to_reduce)

        self.updateShoppingListUI()

    def voiceButtonClicked(self):
        # textChanged = QtCore.pyqtSignal(str)

        r = sr.Recognizer()
        m = sr.Microphone()

        # while True:
        print("Say somethig!")
        with m as source:
            audio = r.listen(source)
            print("Got it! Now to recognize it...")
            try:
                value = r.recognize_google(audio)
                # self.textChanged.emit(value)
                print("You said: {}".format(value))
                if self.current_selected_item_to_add is None:
                    return
                # need to modify
                item_to_add = self.ordered_item_metadata[self.current_selected_item_to_add]
                self.dc.add_to_shopping_list(item_to_add)
                self.updateShoppingListUI()
            except sr.UnknownValueError:
                print("Oops")