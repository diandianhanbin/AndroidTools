# ecoding=utf-8
from Tkinter import *

import time

import common
import ConfigParser
import adb
import monkey
import multiprocessing

__author__ = "Sven_Weng"


class AndroidTools:
    def __init__(self):
        self.cm = common.Common()
        self.cf = ConfigParser.ConfigParser()
        self.cf.read('monkey.conf')
        self.ad = adb.Adb()
        self.mk = monkey.Monkey()

        master = Tk()
        master.title('Android_Tools  Design By Sven')

        Label(master, text='设备号').grid(row=0)
        Label(master, text='测试包名:-p com.weizq').grid(row=1)
        Label(master, text='日志地址').grid(row=2)
        Label(master, text='日志等级:-v').grid(row=3)
        Label(master, text='事件数量').grid(row=4)
        Label(master, text='延时').grid(row=5)
        Label(master, text='触摸事件:--pct-touch').grid(row=6)
        Label(master, text='手势事件:--pct-motion').grid(row=7)
        Label(master, text='缩放事件:--pct-pinchzoom').grid(row=8)
        Label(master, text='轨迹球事件:--pct-trackball').grid(row=9)
        Label(master, text='屏幕事件:--pct-rotation').grid(row=10)
        Label(master, text='导航事件:--pct-nav').grid(row=11)
        Label(master, text='主要事件:--pct-majornav').grid(row=12)
        Label(master, text='系统事件:--pct-syskeys').grid(row=13)
        Label(master, text='切屏事件:--pct-appswitch').grid(row=14)
        Label(master, text='键盘事件:--pct-flip').grid(row=15)
        Label(master, text='其他事件:--pct-anyevent').grid(row=16)
        Label(master, text="monkey进程").grid(row=17)
        Label(master, text="Android其他监控命令").grid(column=3, row=0, columnspan=3)
        Label(master, text="内存监控").grid(column=3, row=1)
        Label(master, text="cpu监控").grid(column=3, row=3)

        global log_path
        global ENTRYLIST
        global status

        device_name = Entry(master, fg='Red')
        package_name = Entry(master)
        log_path = Entry(master)
        log_level = Entry(master)
        count = Entry(master)
        delay = Entry(master)
        touch = Entry(master)
        motion = Entry(master)
        pinch = Entry(master)
        trackball = Entry(master)
        screen = Entry(master)
        nav = Entry(master)
        major = Entry(master)
        system = Entry(master)
        app = Entry(master)
        keyboard = Entry(master)
        anyevents = Entry(master)
        monkey_pid = Entry(master)
        status = Entry(master, width=50, fg='RED')
        mem_monitor = Entry(master)
        mem_monitor.insert(0, "请输入包名")
        self.memstatus = Entry(master)
        self.memstatus.insert(0, "尚未开始获取内存数据")
        cpu_monitor = Entry(master)
        cpu_monitor.insert(0, "请输入包名")
        self.cpustatus = Entry(master)
        self.cpustatus.insert(0, "尚未开始获取cpu数据")

        device_name.grid(row=0, column=1)
        package_name.grid(row=1, column=1)
        log_path.grid(row=2, column=1)
        log_level.grid(row=3, column=1)
        count.grid(row=4, column=1)
        delay.grid(row=5, column=1)
        touch.grid(row=6, column=1)
        motion.grid(row=7, column=1)
        pinch.grid(row=8, column=1)
        trackball.grid(row=9, column=1)
        screen.grid(row=10, column=1)
        nav.grid(row=11, column=1)
        major.grid(row=12, column=1)
        system.grid(row=13, column=1)
        app.grid(row=14, column=1)
        keyboard.grid(row=15, column=1)
        anyevents.grid(row=16, column=1)
        monkey_pid.grid(row=17, column=1)
        status.grid(row=18, column=0, columnspan=3)
        mem_monitor.grid(row=1, column=4)
        self.memstatus.grid(row=2, column=4)
        cpu_monitor.grid(row=3, column=4)
        self.cpustatus.grid(row=4, column=4)

        connect_text = Button(master, text='获取设备号',
                              command=lambda: self.cm.set_text(device_name, self.ad.get_devices()))
        up_pknm_conf = Button(master, text='修改包名',
                              command=lambda: self.cm.update_conf(status, 'package_name',
                                                                  self.cm.get_text(package_name)))
        up_log_path_conf = Button(master, text='修改日志地址',
                                  command=lambda: self.cm.update_conf(status, 'log_path', self.cm.get_text(log_path)))
        up_log_level_conf = Button(master, text='修改日志等级',
                                   command=lambda: self.cm.update_conf(status, 'log_level',
                                                                       self.cm.get_text(log_level)))
        up_count_conf = Button(master, text='修改测试数量',
                               command=lambda: self.cm.update_conf(status, 'count', self.cm.get_text(count)))
        up_delay_conf = Button(master, text='修改延时',
                               command=lambda: self.cm.update_conf(status, 'delay', self.cm.get_text(delay)))
        up_touch_conf = Button(master, text='修改触摸事件',
                               command=lambda: self.cm.update_conf(status, 'touch', self.cm.get_text(touch)))
        up_motion_conf = Button(master, text='修改手势事件',
                                command=lambda: self.cm.update_conf(status, 'motion', self.cm.get_text(motion)))
        up_pinch_conf = Button(master, text='修改缩放事件',
                               command=lambda: self.cm.update_conf(status, 'pinch', self.cm.get_text(pinch)))
        up_trackball_conf = Button(master, text='修改轨迹球事件',
                                   command=lambda: self.cm.update_conf(status, 'trackball',
                                                                       self.cm.get_text(trackball)))
        up_screen_conf = Button(master, text='修改屏幕事件',
                                command=lambda: self.cm.update_conf(status, 'screen', self.cm.get_text(screen)))
        up_nav_conf = Button(master, text='修改导航事件',
                             command=lambda: self.cm.update_conf(status, 'nav', self.cm.get_text(nav)))
        up_major_conf = Button(master, text='修改主要事件',
                               command=lambda: self.cm.update_conf(status, 'major', self.cm.get_text(major)))
        up_system_conf = Button(master, text='修改系统事件',
                                command=lambda: self.cm.update_conf(status, 'system', self.cm.get_text(system)))
        up_app_conf = Button(master, text='修改切屏事件',
                             command=lambda: self.cm.update_conf(status, 'app', self.cm.get_text(app)))
        up_keyboard_conf = Button(master, text='修改键盘事件',
                                  command=lambda: self.cm.update_conf(status, 'keyboard', self.cm.get_text(keyboard)))
        up_anyevents_conf = Button(master, text='修改其他事件',
                                   command=lambda: self.cm.update_conf(status, 'anyevents',
                                                                       self.cm.get_text(anyevents)))
        cat_monkey_pid = Button(master, text='显示Monkey进程',
                                command=lambda: self.cm.set_text(monkey_pid, self.ad.get_monkey_id()))
        start_monkey = Button(master, text='开始Monkey',
                              command=self.run_monkey)
        stop_monkey = Button(master, text='结束Monkey',
                             command=self.stop_monkey)

        get_monkey = Button(master, text='获取Monkey',
                            command=lambda: self.cm.set_text(status,
                                                             self.mk.get_monkey(self.cm.get_text(log_path),
                                                                                *self.cm.collect(*ENTRYLIST))))
        get_memm_info = Button(master, text='开始生成内存信息',
                               command=lambda: self.get_meminfo(self.cm.get_text(mem_monitor)))
        stop_mem_info = Button(master, text="停止生成内存信息", command=self.stop_meminfo)

        get_cpu_info = Button(master, text="开始生成cpu信息",
                              command=lambda: self.get_cpuinfo(self.cm.get_text(cpu_monitor)))
        stop_cpu_info = Button(master, text='停止生成cpu信息', command=self.stop_cpuinfo)

        connect_text.grid(row=0, column=2)
        up_pknm_conf.grid(row=1, column=2)
        up_log_path_conf.grid(row=2, column=2)
        up_log_level_conf.grid(row=3, column=2)
        up_count_conf.grid(row=4, column=2)
        up_delay_conf.grid(row=5, column=2)
        up_touch_conf.grid(row=6, column=2)
        up_motion_conf.grid(row=7, column=2)
        up_pinch_conf.grid(row=8, column=2)
        up_trackball_conf.grid(row=9, column=2)
        up_screen_conf.grid(row=10, column=2)
        up_nav_conf.grid(row=11, column=2)
        up_major_conf.grid(row=12, column=2)
        up_system_conf.grid(row=13, column=2)
        up_app_conf.grid(row=14, column=2)
        up_keyboard_conf.grid(row=15, column=2)
        up_anyevents_conf.grid(row=16, column=2)
        cat_monkey_pid.grid(row=17, column=2)
        start_monkey.grid(row=19, column=0)
        stop_monkey.grid(row=19, column=2)
        get_monkey.grid(row=19, column=1)
        get_memm_info.grid(row=1, column=5)
        stop_mem_info.grid(row=1, column=6)
        get_cpu_info.grid(row=3, column=5)
        stop_cpu_info.grid(row=3, column=6)

        self.cm.set_text(device_name, '点击右侧按钮查看设备号')
        self.cm.set_text(package_name, self.cf.get('monkey_conf', 'package_name'))
        self.cm.set_text(log_path, self.cf.get('monkey_conf', 'log_path'))
        self.cm.set_text(log_level, self.cf.get('monkey_conf', 'log_level'))
        self.cm.set_text(count, self.cf.get('monkey_conf', 'count'))
        self.cm.set_text(delay, self.cf.get('monkey_conf', 'delay'))
        self.cm.set_text(touch, self.cf.get('monkey_conf', 'touch'))
        self.cm.set_text(motion, self.cf.get('monkey_conf', 'motion'))
        self.cm.set_text(pinch, self.cf.get('monkey_conf', 'pinch'))
        self.cm.set_text(trackball, self.cf.get('monkey_conf', 'trackball'))
        self.cm.set_text(screen, self.cf.get('monkey_conf', 'screen'))
        self.cm.set_text(nav, self.cf.get('monkey_conf', 'nav'))
        self.cm.set_text(major, self.cf.get('monkey_conf', 'major'))
        self.cm.set_text(system, self.cf.get('monkey_conf', 'system'))
        self.cm.set_text(app, self.cf.get('monkey_conf', 'app'))
        self.cm.set_text(keyboard, self.cf.get('monkey_conf', 'keyboard'))
        self.cm.set_text(anyevents, self.cf.get('monkey_conf', 'anyevents'))

        # <===========界面初始化结束==================>

        # <===========常量数据==================>

        ENTRYLIST = [package_name, touch, motion, pinch, trackball, screen, nav, major,
                     system, app, keyboard, anyevents, log_level, count]

        # <===========常量数据==================>

        master.mainloop()

    def run_monkey(self):
        t = multiprocessing.Process(target=lambda: self.mk.merge_command(self.cm.get_text(log_path),
                                                                         *self.cm.collect(*ENTRYLIST)))
        t.start()

    def stop_monkey(self):
        self.ad.stop_monkey(status)

    def run_meminfo(self, package_name):
        self.cf.read('monkey.conf')
        self.cf.set('monkey_check', 'mark', 'True')
        self.cf.write(open('monkey.conf', 'w'))
        status = self.cf.get('monkey_check', 'mark')
        with open(self.ad.get_dir('meminfo'), 'w') as f:
            while status == 'True':
                f.write(self.ad.get_meminfo(package_name))
                f.write('\n')
                time.sleep(0.5)
                self.cf.read('monkey.conf')
                if self.cf.get('monkey_check', 'mark') == 'False':
                    break

    def get_meminfo(self, package_name):
        self.cm.set_text(self.memstatus, '正在获取内存信息.....')
        t = multiprocessing.Process(target=lambda: self.run_meminfo(package_name))
        t.start()

    def stop_meminfo(self):
        self.cf.set('cpu_check', 'mark', 'False')
        self.cf.write(open('monkey.conf', 'w'))
        self.cm.set_text(self.memstatus, '停止获取内存信息')

    def get_cpuinfo(self, package_name):
        self.cm.set_text(self.cpustatus, '正在获取cpu信息.....')
        t = multiprocessing.Process(target=lambda: self.ad.get_cpuinfo(package_name, 'cpuinfo'))
        t.start()

    def stop_cpuinfo(self):
        self.cf.set('cpu_check', 'mark', 'False')
        self.cf.write(open('monkey.conf', 'w'))
        self.cm.set_text(self.cpustatus, '停止获取cpu信息')


if __name__ == '__main__':
    AndroidTools()
