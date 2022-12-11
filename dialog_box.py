"""
文本框类，用以生成桌面的对话框内容
"""
import random

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class dialog_box(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        # 对话框状态码
        self.tmp = None
        self.condition = 0
        # 对话框位置
        self.setGeometry(0, 0, 100, 100)
        # 将宠物正常待机状态的对话放入dialog中
        self.dialog = []
        # 读取目录下dialog文件
        with open("dialog.txt", "r") as f:
            text = f.read()
            # 以\n 即换行符为分隔符，分割放进dialog中
            self.dialog = text.split("\n")
        self.first_txt()

    def first_txt(self):
        self.setText('你好鸭！')
        # 设置样式
        self.setStyleSheet(
            "font: bold;"
            "font:25pt '楷体';"
            "color:white;"
            "background-color: white"
            "url(:/)"
        )
        # 根据内容自适应大小
        self.adjustSize()

    # 宠物随机对话时的方法
    def random_dialog_switch(self):
        self.setText(random.choice(self.dialog))
        # 设置样式
        self.setStyleSheet(
            "font: bold;"
            "font:15pt '楷体';"
            "color:white;"
            "background-color: white"
            "url(:/)"
        )
        # 根据内容自适应大小
        self.adjustSize()

    # 长时间挂机时专属对话
    def await_mode(self):
        self.condition = 2
        self.setText('世事漫随流水，算来一梦浮生')
        self.setStyleSheet(
            "font: bold;"
            "font:15pt '楷体';"
            "color:white;"
            "background-color: white"
            "url(:/)"
        )
        self.adjustSize()

    # 被左键点击时调用的方法
    def left_click_mode(self):
        self.condition = 1
        self.setText("痒~别挠~别挠")
        self.setStyleSheet(
            "font: bold;"
            "font:25pt '楷体';"
            "color:white;"
            "background-color: white"
            "url(:/)"
        )
        self.adjustSize()
        # 设置定时器，保证被点击后2s才更换对话
        self.tmp = QTimer()
        self.tmp.timeout.connect(self.time_to_end)
        self.tmp.start(2000)

    def time_to_end(self):
        self.tmp.stop()
        self.condition = 0
        self.random_dialog_switch()

    def move_mode(self):
        self.setText('走咯走咯')
        self.setStyleSheet(
            "font: bold;"
            "font:25pt '楷体';"
            "color:white;"
            "background-color: white"
            "url(:/)"
        )
        self.adjustSize()

    def right_click_mode(self):
        self.setText('找我干嘛鸭')
        self.setStyleSheet(
            "font: bold;"
            "font:25pt '楷体';"
            "color:white;"
            "background-color: white"
            "url(:/)"
        )
        self.adjustSize()

    def showWeather(self, wea, temLow, temHig, win, clodTips, clothTips):
        self.setText("今日天气{}，气温{}至{}℃, 风力{}\n".format(wea,temLow,temHig,win) +
                     clodTips + clothTips)
        self.setStyleSheet(
            "font: bold;"
            "font:15pt '楷体';"
            "color:white;"
            "background-color: white"
            "url(:/)"
        )
        self.adjustSize()
    def sayHello(self):
        self.setText('主人，你好呀')
        self.setStyleSheet(
            "font: bold;"
            "font:25pt '楷体';"
            "color:white;"
            "background-color: white"
            "url(:/)"
        )
        self.adjustSize()

    def drag_file_mode(self):
        self.setText('好吃好吃~')
        self.setStyleSheet(
            "font: bold;"
            "font:25pt '楷体';"
            "color:white;"
            "background-color: white"
            "url(:/)"
        )
        self.adjustSize()

    def briefDia(self, str):
        self.setText(str)
        self.setStyleSheet(
            "font: bold;"
            "font:15pt '楷体';"
            "color:white;"
            "background-color: white"
            "url(:/)"
        )
        self.adjustSize()
