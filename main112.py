from camera import camera
from detect import detect
from gui import gui
import main_func_cfg as mfcfg
import time
import cv2
import random
import filter
import numpy as np


class XJTU:
    def __init__(self):
        self.gui = gui.Gui()
        self.camera = camera.Camera()
        self.detect = detect.Detect()
        self.outImage = []
        self.outText = {}
        self.outFilename = 'XJTU-XJTUfly3-Rx.txt'

        self.exsdic = {"CA001": 0,"CA002": 0,"CA003": 0,"CA004": 0,"CD001": 0,"CD002": 0,"CD003": 0,"CD004": 0,"CD005": 0,"CD006": 0,"ZA001": 0,"ZA002": 0,"ZA003": 0,
           "ZA004": 0,"ZA005": 0,"ZA006": 0,"ZB001": 0,"ZB002": 0,"ZB003": 0,"ZB004": 0,"ZB005": 0,"ZB006": 0,"ZB007": 0,"ZB008": 0,"ZB009": 0,"ZB010": 0,
           "ZC001": 0,"ZC002": 0,"ZC003": 0,"ZC004": 0,"ZC005": 0,"ZC006": 0,"ZC007": 0,"ZC008": 0,"ZC009": 0,"ZC010": 0,"ZC011": 0,"ZC012": 0,"ZC013": 0,
           "ZC014": 0,"ZC015": 0,"ZC016": 0,"ZC017": 0,"ZC018": 0,"ZC019": 0,"ZC020": 0,"ZC021": 0,"ZC022": 0,"ZC023": 0}
        self.numdic = {"CA001": 0,"CA002": 0,"CA003": 0,"CA004": 0,"CD001": 0,"CD002": 0,"CD003": 0,"CD004": 0,"CD005": 0,"CD006": 0,"ZA001": 0,"ZA002": 0,"ZA003": 0,
           "ZA004": 0,"ZA005": 0,"ZA006": 0,"ZB001": 0,"ZB002": 0,"ZB003": 0,"ZB004": 0,"ZB005": 0,"ZB006": 0,"ZB007": 0,"ZB008": 0,"ZB009": 0,"ZB010": 0,
           "ZC001": 0,"ZC002": 0,"ZC003": 0,"ZC004": 0,"ZC005": 0,"ZC006": 0,"ZC007": 0,"ZC008": 0,"ZC009": 0,"ZC010": 0,"ZC011": 0,"ZC012": 0,"ZC013": 0,
           "ZC014": 0,"ZC015": 0,"ZC016": 0,"ZC017": 0,"ZC018": 0,"ZC019": 0,"ZC020": 0,"ZC021": 0,"ZC022": 0,"ZC023": 0}
        self.doubledic = {"CA001": 0,"CA002": 0,"CA003": 0,"CA004": 0,"CD001": 0,"CD002": 0,"CD003": 0,"CD004": 0,"CD005": 0,"CD006": 0,"ZA001": 0,"ZA002": 0,"ZA003": 0,
           "ZA004": 0,"ZA005": 0,"ZA006": 0,"ZB001": 0,"ZB002": 0,"ZB003": 0,"ZB004": 0,"ZB005": 0,"ZB006": 0,"ZB007": 0,"ZB008": 0,"ZB009": 0,"ZB010": 0,
           "ZC001": 0,"ZC002": 0,"ZC003": 0,"ZC004": 0,"ZC005": 0,"ZC006": 0,"ZC007": 0,"ZC008": 0,"ZC009": 0,"ZC010": 0,"ZC011": 0,"ZC012": 0,"ZC013": 0,
           "ZC014": 0,"ZC015": 0,"ZC016": 0,"ZC017": 0,"ZC018": 0,"ZC019": 0,"ZC020": 0,"ZC021": 0,"ZC022": 0,"ZC023": 0}
        self.tridic = {"CA001": 0,"CA002": 0,"CA003": 0,"CA004": 0,"CD001": 0,"CD002": 0,"CD003": 0,"CD004": 0,"CD005": 0,"CD006": 0,"ZA001": 0,"ZA002": 0,"ZA003": 0,
           "ZA004": 0,"ZA005": 0,"ZA006": 0,"ZB001": 0,"ZB002": 0,"ZB003": 0,"ZB004": 0,"ZB005": 0,"ZB006": 0,"ZB007": 0,"ZB008": 0,"ZB009": 0,"ZB010": 0,
           "ZC001": 0,"ZC002": 0,"ZC003": 0,"ZC004": 0,"ZC005": 0,"ZC006": 0,"ZC007": 0,"ZC008": 0,"ZC009": 0,"ZC010": 0,"ZC011": 0,"ZC012": 0,"ZC013": 0,
           "ZC014": 0,"ZC015": 0,"ZC016": 0,"ZC017": 0,"ZC018": 0,"ZC019": 0,"ZC020": 0,"ZC021": 0,"ZC022": 0,"ZC023": 0}

        self.finaldic = {"CA001": 0,"CA002": 0,"CA003": 0,"CA004": 0,"CD001": 0,"CD002": 0,"CD003": 0,"CD004": 0,"CD005": 0,"CD006": 0,"ZA001": 0,"ZA002": 0,"ZA003": 0,
           "ZA004": 0,"ZA005": 0,"ZA006": 0,"ZB001": 0,"ZB002": 0,"ZB003": 0,"ZB004": 0,"ZB005": 0,"ZB006": 0,"ZB007": 0,"ZB008": 0,"ZB009": 0,"ZB010": 0,
           "ZC001": 0,"ZC002": 0,"ZC003": 0,"ZC004": 0,"ZC005": 0,"ZC006": 0,"ZC007": 0,"ZC008": 0,"ZC009": 0,"ZC010": 0,"ZC011": 0,"ZC012": 0,"ZC013": 0,
           "ZC014": 0,"ZC015": 0,"ZC016": 0,"ZC017": 0,"ZC018": 0,"ZC019": 0,"ZC020": 0,"ZC021": 0,"ZC022": 0,"ZC023": 0}

    def Processdic(self):
        for i in self.outText:
            if  self.outText[i] == 1:
                self.exsdic[i]= self.exsdic[i]+1
            if self.outText[i]> self.numdic[i]:
                self.numdic[i]=self.outText[i]
            if self.outText[i] ==2:
                self.doubledic[i]= self.doubledic[i]+1
            if self.outText[i] >=3:
                self.tridic[i]= self.tridic[i]+1
        for i in self.finaldic:
            if self.numdic[i]==1:
                if self.exsdic[i] >20:
                    self.finaldic[i] =1
            if self.numdic[i] ==2:
                if self.doubledic[i] > 10:
                    self.finaldic[i]=2
                else :
                    self.numdic[i]=1
            if self.numdic[i]==3:
                if self.tridic[i]>7:
                    self.finaldic[i]=3
                else:
                    self.numdic[i]=2

            '''
            if self.exsdic[i]>15:
                if self.numdic[i]==1:
                    self.finaldic[i]=self.numdic[i]
                if self.doubledic[i]>10 and self.numdic[i]==2:
                    self.finaldic[i]=2
                if self.tridic[i]>10 :
                    self.finaldic[i]=3
                elif self.tridic[i]>0 and self.doubledic[i]>10:
                     self.finaldic[i]=2
'''
    def disdurb(self,image):
            a = random.random()
            b = random.random()
            image  =  np.array(image)
            image = cv2.resize(image ,(1280 -int(10*b),720 - int(a *10)))
            image = image [0:image.shape[0]-int(a*10), 0:image.shape[1]-int(b *5)]
            return image
    def main(self):

        print('Waiting start...')
        total = []
        dicts = []
        #D3为第三个场景的单独的识别内容


        record = 0
        while not self.gui.start():
            time.sleep(1)

        start_time = time.time()
        while not self.gui.stop():
            time.sleep(0.1)
            print('start detect...')
            src = self.camera.frame()

            if (time.time()- start_time)>10.0 and (time.time()- start_time)<130:
                src = self.disdurb(src)

            self.outImage, self.outText = self.detect.detect(src)

            if (time.time()- start_time)>145.0 and (time.time()- start_time)<236:
                self.Processdic()


            self.gui.update(self.outImage, self.outText)
            mfcfg.alarmer(start_time, time.time())
            if mfcfg.record_if(start_time, time.time()):
                dicts.append(self.outText)
            else:
                record, total, dicts = mfcfg.record_fuse(dicts, record, start_time, time.time(), total)

        # with open(self.outFilename, 'w') as f:
        #     f.write(str(total))
        #print(total)
        num =0
        for i in self.finaldic:
            num = self.exsdic[i] + num
            if not self.finaldic[i]==0:
                print(i)
                print(self.finaldic[i])
        print("num")
        print(num)
        print("total")
        print(total)
        total = mfcfg.record_fuse2(total, self.finaldic)
        mfcfg.write_output(total, self.outFilename)

























if __name__ == '__main__':
    xjtu = XJTU()
    xjtu.main()
