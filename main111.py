from camera import camera
from detect import detect
from gui import gui
import main_func_cfg as mfcfg
import time
import cv2
import filter




class XJTU:
    def __init__(self):
        self.gui = gui.Gui()
        self.camera = camera.Camera()
        self.detect = detect.Detect()
        self.outImage = []
        self.position = {}
        self.outText = {}
        self.outFilename = 'XJTU-XJTUfly3-Rx.txt'
        # 背景图像堆栈
        self.img_stack = []

        # 识别处理
        self.his = []      # 储存历史的识别记录
        self.OutText = {}  # 作为一个背景下的所有数据
        self.all = {}      # 最后作为输出

    # ----------------------------------------------------------------------------
    def up_date_same(self):
        if len(self.his) < 2:
                self.his.append(self.position)
                return
        else:
            image = self.position
            for k in image.keys():
                if detect.point.match_class(k, self.his):
                    num = 0
                    for pro in image[k]:
                        last_frame = self.his[-1].copy()
                        if detect.point.match_position(k, pro, last_frame):
                            # 算一次检测成功
                            num += 1
                    if k not in self.OutText.keys():
                        self.OutText[k] = 0
                    self.OutText[k] = max(num, self.OutText[k])

            # stack in image
            n = len(self.his)
            for i in range(n):
                if i == n - 1:
                    self.his[i] = image
                else:
                    self.his[i] = self.his[i + 1]

    def up_date_diff(self):
        for k in self.OutText.keys():
            if k not in self.all.keys():
                self.all[k] = self.OutText[k]
            else:
                self.all[k] += self.OutText[k]


    def main(self):

        while not self.gui.start():
            time.sleep(1)

        while not self.gui.stop():
            print('start detect...')
            (col, dep) = self.camera.frame()
            src = (col, dep)

            self.outImage, self.position = self.detect.detect(src)

            # 背景比较 -----------------------------------------------------------------------------------#
            # if self.detect.cp_bg(col, self.img_stack[0]) and self.detect.cp_bg(col, self.img_stack[1]):
            self.up_date_same()
            print(self.OutText)
            # else:
            #     self.up_date_diff()
            #     print("differnet image")
            #     self.OutText.clear()
            #     self.img_stack[0], self.img_stack[1] = self.img_stack[1], col
            # # --------------------------------------------------------------------------------------------#

            self.gui.update(self.outImage, self.OutText)


        with open(self.outFilename, 'w') as f:
            f.write(str(self.all))


























if __name__ == '__main__':
    xjtu = XJTU()
    xjtu.main()
