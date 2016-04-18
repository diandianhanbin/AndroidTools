# ecoding=utf-8
__author__ = "Sven_Weng"
from Tkinter import *
import ConfigParser


class Common:
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read('monkey.conf')
        self.all_list = ['package_name', 'log_path']

    def set_text(self, entry, text):
        """
        设置tkinter控件的文本信息
        :param entry: tkinter中的Entry
        :param text: 设置的文本
        :return: None
        """
        entry.delete(0, END)
        entry.insert(0, text)

    def get_text(self, entry):
        """
        获取Tkinter控件的文本信息
        :param entry: tkinter中的Entry
        :return: 获取的文本
        """
        return entry.get()

    def update_conf(self, entry, option, value, section='monkey_conf'):
        """
        更新配置文件
        :param entry:tkinter中的Entry,处理status的文本信息
        :param option:配置文件中的option
        :param value:修改的文本
        :param section:配置文件中的节点,默认为monkey_conf
        :return:None
        """
        self.cf.set(section, option, value)
        self.cf.write(open('monkey.conf', 'w'))
        self.set_text(entry, option+'修改成功')

    def collect(self, *args):
        """
        收集参数中的元素,转换为列表返回
        :param args:传入的参数
        :return:list
        """
        str_list = []
        for x in args:
            str_list.append(self.get_text(x))
        return str_list


if __name__ == '__main__':
    cm = Common()
    # cm.update_conf('package_name', '123jklqwe')
    # cm.collect()