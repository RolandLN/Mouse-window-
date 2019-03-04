#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author：liuneng

import pythoncom
import pyHook
import time
import threading
import psutil
import win32gui
import win32process
import hashlib

a = False
b = False
c = False
d = False


def onMouse_leftdown(event):        # 左键button
    # 监听鼠标左键按下事件
    global Ldown_num, a
    a = False
    Ldown_num += 1
    # print "left DOWN " + str(Ldown_num)
    a = True
    return True
    # 返回 True 表示响应此事件，False表示拦截


def onMouse_leftup(event):
    # 监听鼠标左键弹起事件
    global Lup_num, b
    b = False
    Lup_num += 1
    # print "left UP " + str(Lup_num)
    b = True
    return True


def onMouse_rightdown(event):        # 右键button
    # 监听鼠标右键按下事件
    global Rdown_num, c
    c = False
    Rdown_num += 1
    # print "right DOWN " + str(Rdown_num)
    c = True
    return True
    # 返回 True 表示响应此事件，False表示拦截


def onMouse_rightup(event):
    # 监听鼠标右键弹起事件
    global RTup_num, d
    d = False
    RTup_num += 1
    # print "right UP " + str(RTup_num)
    d = True
    return True


def onMouseEvent(event):
    # "处理鼠标position事件"
    global a, b, c, d
    # fobj.writelines('ME.B  ')
    fobj.writelines("%f  " % time.time())
    fobj.writelines("%s  " % str(event.Position))

    # 监控鼠标button命令
    if a:
        fobj.writelines('LFDW ')
        a = False
    elif b:
        fobj.writelines('LFUP ')
        b = False
    elif c:
        fobj.writelines('RGDW ')
        c = False
    elif d:
        fobj.writelines('RGUP ')
        d = False
    else:
        fobj.writelines('NONE ')

    # 进程pid和进程名
    e = 0
    hwnd = win32gui.GetForegroundWindow()
    # 这个hwnd是一个int对象.窗口句柄代号.
    t, pid = win32process.GetWindowThreadProcessId(hwnd)
    # 获得了线程id和进程id.
    e = pid
    # print t, pid, e

    # 获取进程名和进程名hash值
    p = psutil.Process(e)
    # print('Process name : %s' % p.name())
    # fobj.writelines("%d  " % e)   # 进程pid‘e’

    # 进程名hash
    md5 = hashlib.md5()  # 应用MD5算法
    data = p.name()
    md5.update(data.encode('utf-8'))
    # print md5.hexdigest()
    fobj.writelines("%s  " % md5.hexdigest())  # 进程名hash值

    fobj.writelines("%s  " % p.name())  # 进程名

    # fobj.writelines("MessageName:%s\n" % str(event.MessageName))
    # fobj.writelines("Message:%d\n" % event.Message)
    # fobj.writelines("Time_sec:%d\n" % event.Time)
    # fobj.writelines("%s " % str(event.Window))
    # fobj.writelines("%s " % str(event.WindowName))
    # fobj.writelines("%s " % str(os.getpid()))

    fobj.writelines('\n')
    return True


def main(hm1):

    hm1.MouseLeftDown = onMouse_leftdown

    hm1.MouseLeftUp = onMouse_leftup

    hm1.MouseRightDown = onMouse_rightdown

    hm1.MouseRightUp = onMouse_rightup

    hm1.HookMouse()

    # 进入循环，如不手动关闭，程序将一直处于监听状态


if __name__ == "__main__":

    # 打开日志文件
    # 电脑开机时间作为文件名
    from datetime import datetime
    dt = datetime.fromtimestamp(psutil.boot_time())
    windowsstarttime = dt.strftime("%Y-%m-%d-%H-%M-%S")
    # print windowsstarttime, 'hello'
    fobj = open("D:\pycharm\pydata\mouse-" + windowsstarttime + ".txt", "a")
    # fobj.write("时间    位置    操作     进程名hash值   进程名  \n")

    # 以日期为文件名

    # fobj = open("D:\pycharm\pydata\mouse-"+datetime.now().date().strftime('%Y%m%d') + '.txt', 'a')

    # 新线程执行的代码:
    print('thread %s is running...' % threading.current_thread().name)
    print(windowsstarttime, '\n    welcome ........', "\ndon't click in the window please !!!")
    print('check in [D:pycharm\pydata]')
    # 创建hook句柄
    hm = pyHook.HookManager()

    # 监控鼠标position
    hm.MouseAll = onMouseEvent
    hm.HookMouse()

    # 监控鼠标button命令
    Ldown_num = 0
    Lup_num = 0
    Rdown_num = 0
    RTup_num = 0
    main(hm)

    # 循环获取消息
    pythoncom.PumpMessages()

    # 关闭日志文件
    fobj.close()
