import os.path
import numpy as np
from random import randrange, choice, seed
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage
from imutils.video import VideoStream
import cv2
import time
import argparse
import imutils
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot

# # construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", type=str,
# 	help="path to optinal input video file")
# args = vars(ap.parse_args())


seed()

class CameraCaptureThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                # orig = frame.copy()

                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                # p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(convertToQtFormat)

                # cv2.imshow("Text Detection", orig)


class Camera:
    def __init__(self, dataContainer):
        self.dc = dataContainer
        self.panel2 = None
        self.locationService = None

        self.mock_images = []

        self.vs = None

    def setup(self, panel2, locationService):
        self.panel2 = panel2
        self.locationService = locationService

        # Temporary mock logic
        self.mockImageIdentification()

    def mockImageCapture(self):
        arr = self.mock_read_raw_image()
        arr = self.startVideo()

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
            # self._onImageCaptured(choice(self.mock_images))
            self._onImageCaptured(self.mock_images)
            QTimer.singleShot(2000, interval)

        interval()
        pass

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
        print(arr)
        print(arr.shape)

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

    # def startVideo2(self):
    #     # if a video path was not supplied, grab the reference to the web cam
    #     if not args.get("video", False):
    #         print("[INFO] starting video stream...")
    #         self.vs = VideoStream(src=0).start()
    #         time.sleep(1.0)

    #     # otherwise, grab a reference to the video file
    #     else:
    #         self.vs = cv2.VideoCapture(args["video"])

    #     def interval():

    #         frame = self.vs.read()
    #         # if ret:
    #         frame = frame[1] if args.get("video", False) else frame
    #         orig = frame.copy()

    #         rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         h, w, ch = rgbImage.shape
    #         bytesPerLine = ch * w
    #         img = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)

    #         self._onImageCaptured(img)
    #         cv2.imshow("Text Detection", orig)


    #         QTimer.singleShot(100, interval)

    #     interval()
