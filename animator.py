import numpy as np
import math
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPen
from config import SHOULD_ANIMATE_MAP_ROUTE_SPEED

class ShoppingRouteAnimator:
    def __init__(self, mapGraphicsScene):
        self.graphicsScene = mapGraphicsScene
        self.state = None
        self.route = None
        self.pen = QPen(Qt.red, 3)
        self.nextNode = None
        self.previousNode = None
        self.step = 0
        self.stepVector = None
        self.stepGoalDistance = 0
        self.lastLineItem = None
        self.timer = None

    def start(self, route):
        self.reset()
        self.route = route        
        
        if len(self.route) == 0:
            return
        
        self.nextNode = np.array(route.pop(0))

        self.graphicsScene.clear()

        self.tick()

        self.state = 'started'

    def tick(self):
        if self.step * SHOULD_ANIMATE_MAP_ROUTE_SPEED >= self.stepGoalDistance:
            if len(self.route) == 0:
                self.complete()
                return

            self.previousNode = self.nextNode
            self.nextNode = np.array(self.route.pop(0))

            vector = np.subtract(self.nextNode, self.previousNode)
            self.stepGoalDistance = np.linalg.norm(vector)
            self.step = 0
            self.stepVector = vector / self.stepGoalDistance
            self.lastLineItem = None

        # print(self.previousNode, self.nextNode, self.step, self.stepVector, self.stepGoalDistance)

        self.step += 1
        [x1, y1] = self.previousNode
        move_distance = min(self.step * SHOULD_ANIMATE_MAP_ROUTE_SPEED, self.stepGoalDistance)
        [x2, y2] = self.previousNode + self.stepVector * move_distance

        if self.lastLineItem is None:
            self.lastLineItem = self.graphicsScene.addLine( x1, y1, x2, y2, self.pen)
        else:
            self.lastLineItem.setLine(x1, y1, x2, y2)

        self.state = 'progress'

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.tick)
        self.timer.start(20)

    def complete(self):
        # print('done')
        self.state = 'done'
        pass

    def reset(self):
        if self.timer is not None and self.timer.isActive():
            self.timer.stop()

        self.previousNode = None
        self.nextNode = None

        self.stepGoalDistance = 0
        self.step = 0
        self.stepVector = None
        self.lastLineItem = None

    def restart(self):
        pass