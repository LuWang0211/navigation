import os.path
import numpy as np
from random import randrange, choice, seed
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage


seed()

class Camera:
    def __init__(self, dataContainer):
        self.dc = dataContainer
        self.panel2 = None
        self.locationService = None

        self.mock_images = []

    def setup(self, panel2, locationService):
        self.panel2 = panel2
        self.locationService = locationService

        # Temporary mock logic
        self.mockImageCapture()
        self.mockImageIdentification()

    def mockImageCapture(self):
        arr = self.mock_read_raw_image()

        (height, width, _) = arr.shape 

        # Divide a big picture into 6 smaller pieces
        h = height // 2
        w = width // 3

        images = []
        for y in range (0, height, h):
            for x in range(0, width, w):
                images.append(arr[y: y + h, x: x + w])
                # print(images[-1].shape)

        self.mock_images = images

        def interval():
            self._onImageCaptured(choice(self.mock_images))
            QTimer.singleShot(2000, interval)

        interval()

    def mock_read_raw_image(self):
        """ Read a mock image and convert it into narray """
        img = QImage()
        img.load(os.path.join(os.path.dirname(__file__), 'mock_camera_images.png'))

        rect = img.rect()

        width = rect.width()
        height = rect.height()

        channels_count = 4

        b = img.bits()
        b.setsize(width * height * channels_count)

        arr = np.frombuffer(b, np.uint8).reshape((height, width, channels_count))

        def convert_function(tuple1):
            return list(tuple1)

        arr = arr.reshape(width * height, channels_count)
        # need to convert the 3 dimention data type
        arr = np.apply_along_axis(convert_function, 1, arr)
        arr = arr.reshape((height, width, channels_count))

        return arr

    def mockImageIdentification(self):
        skip_first = True

        possible_identifications = ['1', '2', '3', '4', '5', 'BROKEN']

        def interval():
            nonlocal skip_first

            if skip_first:
                skip_first = False
            else:
                self.onImageIdentified(choice(possible_identifications))

            interval_ = randrange(1500, 3000)
            #print(f'Set to trigger image identification in {interval_} millseconds')
            QTimer.singleShot(interval_, interval)

        interval()                

    def _onImageCaptured(self, image_nparray):
        self.dc.onImageCaptured(image_nparray)

    def onImageIdentified(self, identified):
        # print(f'Identified Image as {identified}')

        if identified == 'BROKEN':
            return

        self.locationService.onImageIdentified(identified)