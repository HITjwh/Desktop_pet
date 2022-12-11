"""
桌面类，用以生成桌面并且集成宠物图标类和文档类
"""
import os
import random
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Pet import Pet
from dialog_box import dialog_box
from Alarm import Alarm
from Weather import Weather
from Reminder import Reminder
import pyautogui
import time
import threading

# 长待机的界定时间，单位是ms，方便自己调试时一键修改
await_time = 9000


class Desktop(QWidget):

    def __init__(self, parent=None, **kwargs):
        super(Desktop, self).__init__(parent)

        # 类初始化中桌面类需要的相关设定
        # 记录鼠标位移距离
        self.mouse_drag_pos = None
        # 记录鼠标与宠物是否同时移动
        self.is_follow_mouse = None
        # 长待机界定时间
        self.await_time = None
        # GIF动图承载的容器
        self.pet_image = None
        # 对话窗口
        self.text = None
        # 对话窗口计时器
        self.talkTimer = None
        # 宠物形象计时器
        self.timer = None
        # 托盘菜单内容
        self.tray_icon_menu = None
        # 托盘图标
        self.tray_icon = None

        # 窗口初始化
        self.init_window()
        # 托盘化初始
        self.init_tray()
        # 宠物静态gif图加载
        self.initPetImage()
        # 宠物正常待机，实现随机切换动作
        self.petNormalAction()
        # 打招呼
        self.hello()
        # 开始工作计时
        self.initReminder()
        # 当日天气提醒
        self.initWeather()

        # 闹钟对象
        self.alarm = None
        # 锁，用来实现不同功能对宠物文本动作的正常调用
        self.winLock = threading.Lock()

    # 窗体初始化
    def init_window(self):
        # 初始化
        # 设置窗口属性:窗口无标题栏且固定在最前面
        # FrameWindowHint:无边框窗口
        # WindowStaysOnTopHint: 窗口总显示在最上面
        # SubWindow: 新窗口部件是一个子窗口，而无论窗口部件是否有父窗口部件
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # setAutoFillBackground(True)表示的是自动填充背景,False为透明背景
        self.setAutoFillBackground(True)
        # 窗口透明，窗体空间不透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 重绘组件、刷新
        self.repaint()

    # 托盘化设置初始化
    def init_tray(self):
        # 导入准备在托盘化显示上使用的图标
        icons = os.path.join('Icon.jpg')

        # 设置托盘菜单中的相关选项
        # triggered为点击后触发
        # hovered为悬浮就触发操作
        quit_action = QAction('退出', self, triggered=self.quit)
        # 设置该点击选项的左侧显示的图片
        quit_action.setIcon(QIcon(icons))
        # 菜单项显示，点击后调用showing函数
        showing = QAction(u'显示', self, triggered=self.show_out)

        # 新建一个菜单项控件
        self.tray_icon_menu = QMenu(self)
        # 分别添加退出和显示按钮
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon_menu.addAction(showing)
        # 闹钟功能选项
        alarm = self.tray_icon_menu.addMenu("闹钟")
        alarm.addAction(QAction("设置闹钟", self, triggered = self.setAlarm))
        alarm.addAction(QAction("关闭闹钟", self, triggered = self.closeAlarm))
        alarm.addAction(QAction("剩余时间", self, triggered = self.showRemainTime))
        # 天气功能选项
        weather = self.tray_icon_menu.addMenu("天气")
        weather.addAction(QAction("选择城市", self, triggered = self.selectCity))
        weather.addAction(QAction("今日天气", self, triggered = self.todayWeather))

        # QSystemTrayIcon类为应用程序在系统托盘中提供一个图标
        self.tray_icon = QSystemTrayIcon(self)
        # 设置托盘中的图片
        self.tray_icon.setIcon(QIcon(icons))
        # 设置托盘化菜单项
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        # 展示
        self.tray_icon.show()

    # 宠物静态gif图加载
    def initPetImage(self):
        # 对话框定义
        self.text = dialog_box(self)
        # 定义显示图片部分
        self.pet_image = Pet(self)
        # 重构窗口大小
        self.resize(1024, 1024)
        # 调用自定义的randomPosition，会使得宠物出现位置随机
        self.randomPosition()
        # 展示
        self.show()

    # 宠物随机位置
    def randomPosition(self):
        # screenGeometry（）函数提供有关可用屏幕几何的信息
        screen_geo = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        pet_geo = self.geometry()
        width = (screen_geo.width() - pet_geo.width()) * random.random()
        height = (screen_geo.height() - pet_geo.height()) * random.random()
        self.move(width, height)

    # 宠物正常待机动作
    def petNormalAction(self):
        # 每隔一段短时间做个动作
        # 定时器设置，间隔3000ms，时间到换一次
        self.timer = QTimer()
        self.timer.timeout.connect(self.pet_image.random_act_switch)
        self.timer.start(3000)
        # 每隔一段时间切换对话
        self.talkTimer = QTimer()
        self.talkTimer.timeout.connect(self.text.random_dialog_switch)
        self.talkTimer.start(3000)

        # 长定时器设置，间隔10000ms，时间到直接切到待机画面直到被点
        self.await_time = QTimer()
        self.await_time.timeout.connect(self.await_mode)
        self.await_time.start(await_time)

    # 鼠标产生点击时会进入此方法
    def mousePressEvent(self, event):
        # 每次鼠标点击后都会进入此方法，此时长短计时器均要求全部重新启动
        self.talkTimer.start(3000)
        self.timer.start(3000)
        self.await_time.start(await_time)

        # 鼠标左键按下时的相关操作
        if event.buttons() == Qt.LeftButton:
            self.pet_image.left_click_mode()
            self.text.left_click_mode()
            # 左键按下时直接绑定鼠标与宠物
            self.is_follow_mouse = True
            # globalPos() 事件触发点相对于桌面的位置
            # pos() 程序相对于桌面左上角的位置，实际是窗口的左上角坐标
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            # 拖动时鼠标图形的设置
            self.setCursor(QCursor(Qt.OpenHandCursor))

        # 鼠标右键按下时图画与对话框的相关操作，另有操作在contextMenuEvent方法中
        if event.buttons() == Qt.RightButton:
            self.text.right_click_mode()
            self.pet_image.right_click_mode()

    # 鼠标移动时调用，实现宠物随鼠标移动
    def mouseMoveEvent(self, event):
        # 如果鼠标左键按下，且处于绑定状态
        if Qt.LeftButton and self.is_follow_mouse:
            # 宠物随鼠标进行移动
            self.move(event.globalPos() - self.mouse_drag_pos)
            self.pet_image.move_mode()
            self.text.move_mode()
        event.accept()

    # 鼠标释放调用，取消绑定
    def mouseReleaseEvent(self, event):
        # print(type(event))
        self.is_follow_mouse = False
        # 鼠标图形设置为箭头
        self.setCursor(QCursor(Qt.ArrowCursor))

    # 宠物右键点击后的操作方法
    def contextMenuEvent(self, event):
        # 定义菜单
        menu = QMenu(self)
        # 闹钟功能选项
        alarm = menu.addMenu("闹钟")
        alarm.addAction(QAction("设置闹钟", self, triggered = self.setAlarm))
        alarm.addAction(QAction("关闭闹钟", self, triggered = self.closeAlarm))
        alarm.addAction(QAction("剩余时间", self, triggered = self.showRemainTime))
        # 天气功能选项
        weather = menu.addMenu("天气")
        weather.addAction(QAction("选择城市", self, triggered = self.selectCity))
        weather.addAction(QAction("今日天气", self, triggered = self.todayWeather))
        # 定义菜单项
        quitAction = menu.addAction("退出")
        hide = menu.addAction("隐藏")
        # 使用exec_()方法显示菜单。从鼠标右键事件对象中获得当前坐标。mapToGlobal()方法把当前组件的相对坐标转换为窗口（window）的绝对坐标。
        action = menu.exec_(self.mapToGlobal(event.pos()))
        # 点击事件为退出
        if action == quitAction:
            qApp.quit()
        # 点击事件为隐藏
        if action == hide:
            # 通过设置透明度方式隐藏宠物
            self.setWindowOpacity(0)

    # 鼠标移进时调用
    def enterEvent(self, event):
        # 设置鼠标形状 Qt.ClosedHandCursor   非指向手
        self.setCursor(Qt.ClosedHandCursor)

    # 进入待机状态的方法
    def await_mode(self):
        # 原短计时器关闭
        self.timer.stop()
        self.talkTimer.stop()
        # 系统环境进入待机状态
        self.pet_image.await_mode()
        self.text.await_mode()

    # 显示宠物
    def show_out(self):
        # setWindowOpacity（）设置窗体的透明度，通过调整窗体透明度实现宠物的展示和隐藏
        self.setWindowOpacity(1)

    # 退出程序
    def quit(self):
        self.close()
        sys.exit()

    def setAlarm(self):
        if self.alarm != None:
            reply = QMessageBox.question(self, "警告","您已经设置了闹钟，是否关闭并重新设置",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.alarm = None
                self.setAlarm()
        else:
            self.alarm = Alarm()
            self.alarm.closeSignel.connect(self.closeAlarm)
            self.alarm.timeOutSignel.connect(self.alarmTimeOut)
            self.alarm.show()
            self.alarm.confirmSignel.connect(self.settedAlarm)

    def settedAlarm(self):
        '''设置完闹钟后宠物对应的动作与文本'''
        self.talkTimer.start(3000)
        self.text.briefDia('到时间我会提醒你的哦')
        self.timer.start(3000)
        self.pet_image.setAlarm()

    def closeAlarm(self):
        if self.alarm != None:
            self.alarm = None
    def showRemainTime(self):
        '''显示剩余时间'''
        if self.alarm != None:
            # 获取锁
            self.winLock.acquire()
            self.show_out()
            # 获得剩余时间
            str = "还剩下"
            remainSec = self.alarm.remainTime()
            h = int(remainSec/3600)
            m = int((remainSec-h*3600)/60)
            s = remainSec - h*3600 - m*60
            if h>0:
                str += '{}小时'.format(h)
            if m>0:
                str += '{}分钟'.format(m)
            str += '{}秒'.format(s)
            # 宠物对应的文本与动作
            self.talkTimer.start(3000)
            self.text.briefDia(str)
            self.timer.start(3000)
            self.pet_image.remainTime()
            # 释放锁
            self.winLock.release()
        else:
            reply = QMessageBox.question(self, "警告","您还没有设置闹钟，是否设置",
                                     QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.setAlarm()

    def alarmTimeOut(self):
        '''
        闹钟时间到时的提醒
        宠物会移动到鼠标所在位置，并发生抖动，产生相应的文本与图片提醒
        '''
        # 获得锁
        self.winLock.acquire()
        # 若窗口被隐藏，显示窗口
        self.show_out()
        # 窗口移动到鼠标位置
        x, y = pyautogui.position()
        self.move(x-100, y-100)
        # 窗口抖动
        self.shake()
        # 时间到时宠物的提醒动作与文本
        self.talkTimer.start(5000)
        self.text.briefDia("主人，时间到了哦")
        self.timer.start(5000)
        self.pet_image.alarmRemind()
        # 释放锁
        self.winLock.release()
        # TODO: 要不要弹出提醒窗口

    def shake(self):
        '''窗口抖动'''
        self.moveThread = MoveThread(self.pos())
        self.moveThread.moveValue.connect(self.move)
        self.moveThread.start()

    def initReminder(self):
        self.reminder = Reminder()
        # 将Reminder对象中的时间到达信号与对应槽函数相连
        self.reminder.timeOutSignel.connect(self.reminderTimeOut)
    def hello(self):
        self.talkTimer.start(2000)
        self.text.sayHello()
        self.timer.start(2000)
        self.pet_image.hello()
    def reminderTimeOut(self):
        '''
        工作时间太长时的提醒
        包括窗口抖动，通过图片与文本发出提醒
        '''
        self.winLock.acquire()
        # 如果宠物被隐藏，显示宠物
        self.show_out()
        # 时间到时宠物的提醒动作与文本
        self.talkTimer.start(5000)
        self.text.briefDia("主人，您在电脑前工作时间太长了，休息一下吧")
        self.timer.start(5000)
        self.pet_image.workRemind()
        # 窗口抖动
        self.shake()
        self.winLock.release()
    def initWeather(self):
        self.weather = Weather()

    def selectCity(self):
        '''按下选择天气'''
        self.weather.selectCity()
    def todayWeather(self):
        '''按下今日天气'''
        if self.weather.getCityId() != None:
            self.showWeather()
        else:
            reply = QMessageBox.question(self, "警告","您还没有选择城市，是否选择",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.selectCity()
    def showWeather(self):
        '''通过文本与图片展示天气情况'''
        self.winLock.acquire()
        self.show_out()
        wea, temLow, temHig, win, clodTips, clothTips = self.weather.getWeather()
        self.talkTimer.start(5000)
        self.text.showWeather(wea, temLow, temHig, win, clodTips, clothTips)
        self.timer.start(5000)
        self.pet_image.showWeather(wea, int(temLow), int(temHig), win)
        self.winLock.release()

class MoveThread(QThread):
    '''窗口抖动线程，用以实现窗口抖动'''
    moveValue = pyqtSignal(QPoint)
    def __init__(self, sourcePos):
        super().__init__()
        self.sourcePos = sourcePos
    def run(self):
        for i in range(30):
            self.moveValue.emit(self.sourcePos + QPoint(random.randint(1, 50),
                                                         random.randint(1, 50)))
            time.sleep(0.1)