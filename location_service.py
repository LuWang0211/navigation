class LocationService:
    def __init__(self, camera):
        self.camera = camera
        self.last_received_location = None
        self.panel2 = None
        pass

    def setup(self, panel2):
        self.panel2 = panel2
        pass
    
    def onLocationChanged(self):
        # print(f"Location changed to {self.last_received_location}")

        self.panel2.onLocationChanged(int(self.last_received_location))

        pass


    def onImageIdentified(self, identified):
        if identified != self.last_received_location:
            self.last_received_location = identified
            self.onLocationChanged()
