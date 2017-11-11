
class Pixel:
    max_val = 250
    r = max_val
    g = 0
    b = 0
    sequence = 1

    max_valRWG = 240
    fadespeedRWG = 20
    pauseRG = 20

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def rotateColour(self):
        if self.sequence == 6:
            if self.b > 0:
                self.b = self.b - 5
            else:
                self.sequence = 1
        if self.sequence == 5:
            if self.r < self.max_val:
                self.r = self.r + 5
            else:
                self.sequence = 6
        if self.sequence == 4:
            if self.g > 0:
                self.g = self.g - 5
            else:
                self.sequence = 5
        if self.sequence == 3:
            if self.b < self.max_val:
                self.b = self.b + 5
            else:
                self.sequence = 4
        if self.sequence == 2:
            if self.r > 0:
                self.r = self.r - 5
            else:
                self.sequence = 3
        if self.sequence == 1:
            if self.g < self.max_val:
                self.g = self.g + 5
            else:
                self.sequence = 2

    def rotateColourRWG(self):
        if self.sequence == 6:
            # Pause on red
            if self.pauseCounter > 0:
                self.pauseCounter = self.pauseCounter - 1
            else:
                self.sequence = 1
        if self.sequence == 5:
            # Fade to red
            if self.g > 0:
                self.g = self.g - self.fadespeedRWG
                self.b = self.b - self.fadespeedRWG
            else:
                self.pauseCounter = self.pauseRG
                self.sequence = 6
        if self.sequence == 4:
            # Fade to white
            if self.b < self.max_valRWG:
                self.b = self.b + self.fadespeedRWG
                self.r = self.r + self.fadespeedRWG
            else:
                self.sequence = 5
        if self.sequence == 3:
            # Pause on green
            if self.pauseCounter > 0:
                self.pauseCounter = self.pauseCounter - 1
            else:
                self.sequence = 4
        if self.sequence == 2:
            # Fade to green
            if self.b > 0:
                self.b = self.b - self.fadespeedRWG
                self.r = self.r - self.fadespeedRWG
            else:
                self.pauseCounter = self.pauseRG
                self.sequence = 3
        if self.sequence == 1:
            # Fade to white
            if self.g < self.max_valRWG:
                self.g = self.g + self.fadespeedRWG
                self.b = self.b + self.fadespeedRWG
            else:
                self.sequence = 2
