import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My App")

        label = QLabel("This is a PyQt5 window!")

        # The `Qt` namespace has a lot of attributes to customise
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        button = QPushButton('Greet')
        button.show()

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(label)


app = QApplication(sys.argv)
app.setStyleSheet("QPushButton { margin: 50ex; }")

# layout = QVBoxLayout()

# window = QWidget()
window = MainWindow()
# window.setLayout(layout)
window.show()

app.exec_()