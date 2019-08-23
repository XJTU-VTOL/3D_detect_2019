import argparse
import numpy as np
import torch
from detect.utils import *
from detect.models import *
from detect.deep_model import *
from detect.torch_utils import *
from detect.datasets import *
from detect.parse_config import *
import random
import cv2


class Detect:
    def __init__(self, weights="detect/latest.pt", deep_weights="detect/deep_latest.pt", data_cfg='detect/3d.data', img_size=416, conf_thres=0.5, nms_thres=0.4, bg_thres=0.5, bg_w=50):
        self.device = select_device()
        # dark-net
        self.model = Darknet("detect/yolov3.cfg", img_size)
        self.model.load_state_dict(torch.load(weights, map_location=self.device)['model'])
        self.model.fuse()
        self.model.to(self.device).eval()
        # deep-img

        # self.deep_model = Deep_model()
        # self.deep_model.load_state_dict(torch.load(deep_weights, map_location=self.device)['model'])
        # self.deep_model.to(self.device).eval()
        self.bg_w = bg_w
        #para
        self.conf_thres = conf_thres
        self.nms_thres = nms_thres
        self.img_size = img_size
        self.bg_thres = bg_thres
        self.classes = load_classes(parse_data_cfg(data_cfg)['names'])
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(self.classes))]

    # 深度比较
    def deep_detect(self,src):
        hsv = cv2.cvtColor(src, cv2.COLOR_RGB2HSV)
        h = hsv[:,:,0]
        cv2.bilateralFilter(h, 5, 0.5, 2, h)


    # 背景比较
    def background(self, src):
        left_on = src[:self.bg_w, :self.bg_w, :]
        right_on = src[:self.bg_w, :self.bg_w, :]
        back_patch = np.concatenate([left_on, right_on], axis=0)
        return back_patch

    def cp_bg(self, src1, src2):
        bg1 = self.background(src1)
        bg2 = self.background(src2)
        diff = np.abs(bg1-bg2)
        diff = np.sum(diff)
        return diff<self.bg_thres



    def detect(self, src) -> tuple:
        '''

        :param src: input image
        :return: tuple (outImage: numpy.ndarray, outText: dict)
        '''
        color = src[0]
        deep = src[1]
        conf_thres = self.conf_thres
        nms_thres = self.nms_thres
        img, _, _, _ = letterbox(color, new_shape=self.img_size, mode='square')
        # Normalize RGB
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB
        img = np.ascontiguousarray(img, dtype=np.float32)  # uint8 to float32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        img = torch.from_numpy(img).unsqueeze(0).to(self.device)
        pred, _ = self.model(img)
        det = non_max_suppression(pred, conf_thres, nms_thres)[0]
        if det is None:
            return (None, {})
        pre_det = det.split([1]*det.shape[0], 0)
        num_pre = len(pre_det)
        depth_img = deep
        real_detect = torch.tensor([0]*num_pre)
        for ind,obj in enumerate(pre_det):
          obj = obj.squeeze()
          x1 = int(obj[0].item())
          y1 = int(obj[1].item())
          x2 = int(obj[2].item())
          y2 = int(obj[3].item())
          if x1>x2:
              x1, x2 = x2, x1
          if y1>y2:
              y1,y2 = y2,y1
          depth_bbox = depth_img[x1:x2,y1:y2,:]
          # depth_bbox, _, _, _ = letterbox(depth_bbox, 50, mode='square')
          # depth_bbox = depth_bbox[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB
          # depth_bbox = np.ascontiguousarray(depth_bbox, dtype=np.float32)  # uint8 to float32
          # depth_bbox /= 255.0  # 0 - 255 to 0.0 - 1.0
          # depth_bbox = torch.from_numpy(depth_bbox).unsqueeze(0).to(self.device)
          # conf = self.deep_model(depth_bbox)
          # conf = conf.cpu()
          # if conf>self.real_thres:
          #     real_detect[ind] = 1
          conf_d = self.deep_detect(depth_bbox)

        indi = torch.nonzero(real_detect).squeeze()

        det = det[indi]
        det = det.view(-1,7)
        out_dict = {}


        if det is not None and len(det)>0:
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], color.shape).round()
            print('%gx%g ' % img.shape[2:], end='')  # print image size
            for c in det[:, -1].unique():
                n = (det[:, -1] == c).sum().item()
                if self.classes[int(c)] in out_dict:
                    out_dict[self.classes[int(c)]]+=n
                else:
                    out_dict[self.classes[int(c)]]=n
                print('%g %ss' % (n, self.classes[int(c)]), end=', ')
            for *xyxy, conf, cls_conf, cls in det:
                # Add bbox to the image
                label = '%s %.2f' % (self.classes[int(cls)], conf)
                plot_one_box(xyxy, color, label=label, color=self.colors[int(cls)])
        return (color, out_dict)



    def main(self):
        col = cv2.imread('0706color14.jpg')
        dep = cv2.imread('0706depth14.jpg')
        out, text=self.detect(col, dep)
        cv2.imwrite('out.jpg',out)
        print(text)



if __name__ == '__main__':
    detect = Detect()
    detect.main()
