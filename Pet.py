"""
宠物类，用以生成宠物图片以及图片的相关操作
"""
import os
import random

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Pet(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        # 宠物状态，0位正常待机，1为被点击，2为长待机
        self.condition = 0
        # QMovie放映gif
        self.movie = QMovie("welcome/welcome.gif")
        # 设置gif大小
        self.movie.setScaledSize(QSize(200, 200))
        # 将Qmovie在定义的image中显示
        self.setMovie(self.movie)
        self.setGeometry(0, 50, 200, 200)
        self.movie.start()
        # 将宠物正常待机状态的动图放入gifs中
        self.gifs = []
        for i in os.listdir("gifs"):
            self.gifs.append("gifs/" + i)



    # 随机选择装载在pet1里面的gif图进行展示，实现随机切换
    def random_act_switch(self):
        self.setFixedSize(200, 200)
        self.movie = QMovie(random.choice(self.gifs))
        # 宠物大小
        self.movie.setScaledSize(QSize(200, 200))
        # 将动画添加到label中
        self.setMovie(self.movie)
        # 开始播放动画
        self.movie.start()

    # 被左键点击的宠物需要完成的动作
    def left_click_mode(self):
        self.condition = 1
        # 读取特殊状态图片路径
        self.movie = QMovie("./click/left_click.gif")
        # 宠物大小
        self.movie.setScaledSize(QSize(200, 200))

        # 将动画添加到label中
        self.setMovie(self.movie)
        # 开始播放动画
        self.movie.start()
        # 宠物状态设置为正常待机
        self.condition = 0

    # 被右键点击的宠物需要完成的动作
    def right_click_mode(self):
        self.movie = QMovie('./click/right_click.gif')
        # 宠物大小
        self.movie.setScaledSize(QSize(200, 200))
        # 将动画添加到label中
        self.setMovie(self.movie)
        # 开始播放动画
        self.movie.start()

    # 长待机下的方法
    def await_mode(self):
        self.condition = 2
        # 重置为await中的长挂机gif
        self.movie = QMovie('./await/await.gif')
        # 宠物大小
        self.movie.setScaledSize(QSize(200, 200))
        # 将动画添加到label中
        self.setMovie(self.movie)
        # 开始播放动画
        self.movie.start()

    # 移动过程中调用的方法
    def move_mode(self):
        self.movie = QMovie('./move/move.gif')
        # 宠物大小
        self.movie.setScaledSize(QSize(200, 200))
        # 将动画添加到label中
        self.setMovie(self.movie)
        # 开始播放动画
        self.movie.start()

    def alarmRemind(self):
        self.movie = QMovie('./remind/alarm.gif')
        self.movie.setScaledSize(QSize(200,200))
        self.setMovie(self.movie)
        self.movie.start()

    def setAlarm(self):
        self.movie = QMovie('./remind/alarmset.gif')
        self.movie.setScaledSize(QSize(200,200))
        self.setMovie(self.movie)
        self.movie.start()

    def hello(self):
        self.movie = QMovie('./remind/hello.gif')
        self.movie.setScaledSize(QSize(200,200))
        self.setMovie(self.movie)
        self.movie.start()

    def workRemind(self):
        self.movie = QMovie('./remind/reminder.gif')
        self.movie.setScaledSize(QSize(200,200))
        self.setMovie(self.movie)
        self.movie.start()

    def remainTime(self):
        self.movie = QMovie('./remind/remainTime.gif')
        self.movie.setScaledSize(QSize(200,200))
        self.setMovie(self.movie)
        self.movie.start()

    def showWeather(self, wea, temLow, temHig, wind):
        if '雨' in wea: #雨天
            self.movie = QMovie('./weather/rain.gif')
        elif '雪' in wea: #雪天
            self.movie = QMovie('./weather/snow.gif')
        elif '6' in wind: #大风天
            self.movie = QMovie('./weather/wind.gif')
        elif (temLow + temHig)/2 < 5:
            self.movie = QMovie('./weather/cold.gif')
        elif '晴' in wea and (temLow + temHig) > 25:
            self.movie = QMovie('./weather/hot.gif')
        else:
            self.movie = QMovie('./weather/normal.gif')
        self.movie.setScaledSize(QSize(200,200))
        self.setMovie(self.movie)
        self.movie.start()
    # 拖动文件时需要完成的动作
    def drag_file_mode(self, file_path):
        # 为吃东西放大做准备
        self.setFixedSize(500, 500)
        self.movie = QMovie('./eat/eat.gif')
        # 宠物大小
        self.movie.setScaledSize(QSize(500, 500))
        # 将动画添加到label中
        self.setMovie(self.movie)
        # 开始播放动画
        self.movie.start()
        os.remove(file_path[8:])
        #self.setFixedSize(200, 200)
