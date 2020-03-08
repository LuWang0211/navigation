import os.path
import numpy as np
from random import randrange, choice, seed
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage
from imutils.video import VideoStream
from imutils.object_detection import non_max_suppression
import cv2
import time
import argparse
import imutils
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
import pytesseract

seed()

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-east", "--east", type=str, required=True,
	help="path to input EAST text detector")
ap.add_argument("-v", "--video", type=str,
	help="path to optinal input video file")
ap.add_argument("-c", "--min-confidence", type=float, default=0.5,
	help="minimum probability required to inspect a region")
ap.add_argument("-w", "--width", type=int, default=320,
	help="resized image width (should be multiple of 32)")
ap.add_argument("-e", "--height", type=int, default=320,
	help="resized image height (should be multiple of 32)")
args = vars(ap.parse_args())

class CameraCaptureThread(QThread):
    
    changePixmap = pyqtSignal(QImage)
    changecartlocation = pyqtSignal(int)

    def decode_predictions(self, scores, geometry):
        # grab the number of rows and columns from the scores volume, then
        # initialize our set of bounding box rectangles and corresponding
        # confidence scores
        (numRows, numCols) = scores.shape[2:4]
        rects = []
        confidences = []

        # loop over the number of rows
        for y in range(0, numRows):
            # extract the scores (probabilities), followed by the
            # geometrical data used to derive potential bounding box
            # coordinates that surround text
            scoresData = scores[0, 0, y]
            xData0 = geometry[0, 0, y]
            xData1 = geometry[0, 1, y]
            xData2 = geometry[0, 2, y]
            xData3 = geometry[0, 3, y]
            anglesData = geometry[0, 4, y]

            # loop over the number of columns
            for x in range(0, numCols):
                # if our score does not have sufficient probability,
                # ignore it
                if scoresData[x] < args["min_confidence"]:
                    continue

                # compute the offset factor as our resulting feature
                # maps will be 4x smaller than the input image
                (offsetX, offsetY) = (x * 4.0, y * 4.0)

                # extract the rotation angle for the prediction and
                # then compute the sin and cosine
                angle = anglesData[x]
                cos = np.cos(angle)
                sin = np.sin(angle)

                # use the geometry volume to derive the width and height
                # of the bounding box
                h = xData0[x] + xData2[x]
                w = xData1[x] + xData3[x]

                # compute both the starting and ending (x, y)-coordinates
                # for the text prediction bounding box
                endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                startX = int(endX - w)
                startY = int(endY - h)

                # add the bounding box coordinates and probability score
                # to our respective lists
                rects.append((startX, startY, endX, endY))
                confidences.append(scoresData[x])

        # return a tuple of the bounding boxes and associated confidences
        return (rects, confidences)

    def run(self):
        # define the two output layer names for the EAST detector model that
        # we are interested -- the first is the output probabilities and the
        # second can be used to derive the bounding box coordinates of text
        layerNames = [
            "feature_fusion/Conv_7/Sigmoid",
            "feature_fusion/concat_3"]

        # net = cv2.dnn.readNet("./frozen_east_text_detection.pd")

        # load the pre-trained EAST text detector
        print("[INFO] loading EAST text detector...")
        print(args["east"], type(args["east"]))
        net = cv2.dnn.readNet(args["east"])

        # initialize the original frame dimensions, new frame dimensions,
        # and ratio between the dimensions
        (W, H) = (None, None)
        (newW, newH) = (args["width"], args["height"])
        (rW, rH) = (None, None)

        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            # if our frame dimensions are None, we still need to compute the
            # ratio of old frame dimensions to new frame dimensions
            if (W is None or H is None) and (frame is not None):
                (H, W) = frame.shape[:2]
                rW = W / float(newW)
                rH = H / float(newH)

            # resize the frame, this time ignoring aspect ratio
            # frame = cv2.resize(frame, (newW, newH))
            if ret:

                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w

                # construct a blob from the frame and then perform a forward pass
                # of the model to obtain the two output layer sets
                blob = cv2.dnn.blobFromImage(rgbImage, 1.0, (newW, newH),
                    (123.68, 116.78, 103.94), swapRB=True, crop=False)
                net.setInput(blob)
                (scores, geometry) = net.forward(layerNames)

                # print("(scores, geometry)", (scores, geometry))
                
                # decode the predictions, then  apply non-maxima suppression to
                # suppress weak, overlapping bounding boxes
                (rects, confidences) = self.decode_predictions(scores, geometry)
                boxes = non_max_suppression(np.array(rects), probs=confidences)
                # print(rects, confidences)

                # if len(boxes) > 0:
                #     print("boxes", boxes)

                # loop over the bounding boxes
                for (startX, startY, endX, endY) in boxes:
                    # scale the bounding box coordinates based on the respective
                    # ratios
                    startX = int(startX * rW)
                    startY = int(startY * rH)
                    endX = int(endX * rW)
                    endY = int(endY * rH)

                    # draw the bounding box on the frame
                    # cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    cv2.rectangle(rgbImage, (startX, startY), (endX, endY), (0, 255, 0), 2)

                    r = rgbImage[startY:endY, startX:endX]
                    configuration = ("-l eng --oem 1 --psm 8")
                    # configuration = ("-l eng --oem 1 --psm 8 -c tessedit_char_whitelist=0123456789")
                    pytesseract.pytesseract.tesseract_cmd = r'C:/Users/luwan/AppData/Local/Tesseract-OCR/tesseract.exe'
                    text = pytesseract.image_to_string(r, config=configuration)
                    print(text)

                    text_lower = text.lower()
                    if text_lower in ['4', '64', '7', '6', 'sung', 'samsung', 'evo']:
                        print('updated')
                        self.changecartlocation.emit(5)
                    elif text_lower in ['4', 'yogurt', 'juices', 'butter', 'ice', 'cream', 'desserts', 'dessert','cheese']:
                        self.changecartlocation.emit(4)
                    elif text_lower in ['3', 'pizza', 'dinner', 'breakfast', 'frozen']:
                        self.changecartlocation.emit(3)
                    elif text_lower in ['2', 'soup', 'canned', 'cake','food']:
                        self.changecartlocation.emit(2)
                    elif text_lower in ['1', 'pasta', 'dinner', 'dinners', 'condiments','can']:
                        self.changecartlocation.emit(1)
                
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)

                self.changePixmap.emit(convertToQtFormat)


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
        # self.mockImageIdentification()

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
