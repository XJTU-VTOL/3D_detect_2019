import tkinter as tk
from PIL import Image, ImageTk
import threading
import cv2
# 用于本文件中不同类之间的信息通道
gui_image = Image.open('black.jpg')
gui_text = {}
start = False
stop = False


# 修改根窗口
class GUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)  # 初始化窗口

        self.master = master
        self.master.title("Object detection solution")  # 窗口命名
        self.pack(fill=tk.BOTH, expand=1)

        # 分屏(left,rigth)
        # 分为(left,right,right&top,right&bottom)
        frame = tk.Frame(self.master)
        frame.pack()
        frame_l = tk.Frame(frame)
        frame_r = tk.Frame(frame)
        frame_l.pack(side='left')
        frame_r.pack(side='right')
        frame_rt = tk.Frame(frame_r)
        frame_rb = tk.Frame(frame_r)
        frame_rt.pack(side='top')
        frame_rb.pack(side='bottom')

        # 设置按钮
        tk.Button(frame_rb, text='开始', command=self.begin).pack(side='left')
        tk.Button(frame_rb, text='结束', command=self.end).pack(side='right')

        # 使用Label显示jpg图片
        img = Image.open('black.jpg')
        img1 = ImageTk.PhotoImage(img)
        self.label = tk.Label(frame_l, image=img1)  # 图片在左侧窗口显示
        self.label.pack(side='left')
        self.label.image = img1  # 防止图片闪现

        # 右侧框架置入标签框
        tk.Label(frame_rt, text='识别结果输出区').pack(side='top')

        # Label创建黑色背景，待显示结果调用
        self.counter = []
        for x in range(10):
            temporary = tk.Label(frame_rt, text="                       "
                                                "            ", bg='black', fg='white')
            self.counter.append(temporary)
            temporary.pack(side='top')

        # 定时刷新图片
        self.timer = threading.Timer(2, self.fun_timer)
        self.timer.start()

    # “开始”按钮调用函数
    def begin(self):
        global start
        start = True

    # “结束”按钮调用函数
    def end(self):
        global stop
        stop = False

    # Label更新图片
    def UpdateImage(self):
        # 无识别结果时调用文件夹中图片(黑色背景)
        global gui_image
        image_2 = gui_image.resize((500, 500))   # 修改图片大小使适合窗口
        image_3 = ImageTk.PhotoImage(image_2)
        self.label.config(image=image_3)  #更新图片
        self.label.image = image_3  # 防止闪现

    # text修改
    def UpdateText(self):
        global gui_text
        x = 0
        for item in gui_text:
            self.counter[x].config(text='目标物ID：' + item + ' 数量：' + str(gui_text[item]))
            x = x + 1

    # 定时刷新函数
    def fun_timer(self):
        self.UpdateImage()
        self.UpdateText()
        self.timer = threading.Timer(2, self.fun_timer)
        self.timer.start()


class Window:
    def __init__(self):
        root = tk.Tk()  # 创建根窗口
        root.geometry('800x500')  # 修改窗口大小
        self.app = GUI(root)
        root.mainloop()  # 主窗口循环


class Gui:
    def __init__(self):
        t1 = threading.Thread(target=Window)  # 窗口程序在子线程中运行
        t1.start()
        global stop, start
        self.start = start
        self.stop = stop

    def update(self, img=None, text=None):
        global gui_text, gui_image
        if img:
            image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            gui_image = image
        if text:
            gui_text = text
