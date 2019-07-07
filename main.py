from camera import camera
from detect import detect
from gui import gui

import time


class XJTU:
    def __init__(self):
        self.camera = camera.Camera()
        self.detect = detect.Detect()
        self.gui = gui.Gui()
        self.outImage = []
        self.outText = {}
        self.outFilename = 'XJTU-XJTUfly3-Rx.txt'

    def main(self):
        while not self.gui.start:
            pass

        while not self.gui.stop:
            src = self.camera.frame()
            self.outImage, self.outText = self.detect.detect(src)
            self.gui.update(self.outImage, self.outText)
            time.sleep(1)

        with open(self.outFilename, 'w') as f:
            f.write(str(self.outText))


if __name__ == '__main__':
    xjtu = XJTU()
    xjtu.main()
