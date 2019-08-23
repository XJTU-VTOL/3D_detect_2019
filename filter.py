import numpy as np
import cv2
import math
thres = 70

class point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dis(self, c):
        dis = (self.x-c.x)*(self.x-c.x)+(self.y-c.y)*(self.y-c.y)
        return int(math.sqrt(dis))

    def match(self, l):
        for p in l:
            if self.dis(p)<thres :
                return 1
        return 0

def get_label(file_name):
    file = open(file_name,'r')
    txt = file.read()
    txt = txt.split('#')
    dic = []
    for image in txt:
        frame = {}
        content = image.strip(' ').strip('\n').split('\n')
        for line in content:
            line = line.split(' ')
            if line[0] not in frame.keys():
                frame[line[0]] = []
            frame[line[0]].append(point(int(line[6]),int(line[9])))
        dic.append(frame)
    return dic

def match_class(k,h):
    for his_img in h:
        if k not in his_img.keys():
            return 0
    return 1

def match_position(k, p, h):
    for his_img in h:
        if p.match(his_img[k])>thres:
            return 0
    return 1

def update(his, image):
    n = len(his)
    for i in range(n):
        if i == n-1:
            his[i] = image
        else:
            his[i] = his[i+1]


def main():
    statistic = get_label('data.txt')
    his = []
    output = {}
    for image in statistic:
        if len(his)<1:
            his.append(image)
            continue
        else:
            for k in image.keys():
                if match_class(k,his):
                    num = 0
                    for pro in image[k]:
                        if match_position(k,pro,his):
                            # 算一次检测成功
                            num += 1
                    if k not in output.keys():
                        output[k] = 0
                    output[k] = max(num,output[k])
            update(his, image)



    print(output)





if __name__ == '__main__':
   main()

