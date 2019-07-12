import torch
import torch.nn as nn
import torch.nn.functional as F

class Deep_model(nn.Module):
    def __init__(self):
        super(Deep_model,self).__init__()
        self.conv0 = nn.Sequential(  # input shape (1, 28, 28)
            nn.Conv2d(
                in_channels=3,  # input height
                out_channels=1,  # n_filters
                kernel_size=1,  # filter size
                stride=1,  # filter movement/step
                padding=0,  # 如果想要 con2d 出来的图片长宽没有变化, padding=(kernel_size-1)/2 当 stride=1
            ),
        )
        self.conv1 = nn.Sequential(  # input shape (1, 28, 28)
            nn.Conv2d(
                in_channels=1,  # input height
                out_channels=16,  # n_filters
                kernel_size=3,  # filter size
                stride=1,  # filter movement/step
                padding=0,  # 如果想要 con2d 出来的图片长宽没有变化, padding=(kernel_size-1)/2 当 stride=1
            ),  # output shape (16, 28, 28)
            nn.ReLU(),  # activation
            nn.MaxPool2d(kernel_size=2),  # 在 2x2 空间里向下采样, output shape (16, 14, 14)
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(16, 32, 3, 1, 1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(32, 64, 5, 1, 0),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.out = nn.Linear(64 * 4 * 4, 1)  # fully connected layer, output 10 classes

    def forward(self, x):
        x = self.conv0(x)
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = x.view(x.size(0), -1)
        output = torch.sigmoid(self.out(x))
        return output
