from random import randrange, choice, seed
from PyQt5.QtCore import QTimer

seed()

class Camera:
    def __init__(self):
        self.panel2 = None
        self.locationService = None
        pass

    def setup(self, panel2, locationService):
        self.panel2 = panel2
        self.locationService = locationService

        # Temporary mock logic
        self.mockImageIdentification()
        pass

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

    def onImageCaptured(self):
        pass

    def onImageIdentified(self, identified):
        # print(f'Identified Image as {identified}')

        if identified == 'BROKEN':
            return

        self.locationService.onImageIdentified(identified)