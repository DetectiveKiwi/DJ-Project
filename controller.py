class controller:
    def __init__(self):
        self.idxLeft = None
        self.idxRight = None
        self.bpm = 130
        
    def setLeftIdx(self, val):
        self.idxLeft = val
        
    def setRightIdx(self, val):
        self.idxRight = val