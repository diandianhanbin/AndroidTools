# ecoding=utf-8
__author__ = "Sven_Weng"
import os
import ConfigParser
import common


class Monkey:
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read('monkey.conf')
        self.cm = common.Common()

    def run(self, command):
        """
        控制shell执行命令
        :param command:命令的文本
        :return:None
        """
        os.system(command)

    def get_conf(self):
        """
        获取配置信息
        :return:dict,配置信息
        """
        data = {
            'package_name': self.cf.get('monkey_conf', 'package_name'),
            'log_path': self.cf.get('monkey_conf', 'log_path'),
            'log_level': self.cf.get('monkey_conf', 'log_level'),
            'count': self.cf.get('monkey_conf', 'count'),
            'delay': self.cf.get('monkey_conf', 'delay'),
            'touch': self.cf.get('monkey_conf', 'touch'),
            'motion': self.cf.get('monkey_conf', 'motion'),
            'pinch': self.cf.get('monkey_conf', 'pinch'),
            'trackball': self.cf.get('monkey_conf', 'trackball'),
            'screen': self.cf.get('monkey_conf', 'screen'),
            'nav': self.cf.get('monkey_conf', 'nav'),
            'major': self.cf.get('monkey_conf', 'major'),
            'system': self.cf.get('monkey_conf', 'system'),
            'app': self.cf.get('monkey_conf', 'app'),
            'keyboard': self.cf.get('monkey_conf', 'keyboard'),
            'anyevents': self.cf.get('monkey_conf', 'anyevents')
        }
        return data

    def get_command(self):
        """
        获取命令文本,web端使用,已废弃
        :return: str,命令文本
        """
        data = self.get_conf()
        command = 'adb shell monkey {} {} {} {} {} {} {} {} {} {} {} {} {} {} > {}'.format(data['package_name'],
                                                                                           data['touch'],
                                                                                           data['motion'],
                                                                                           data['pinch'],
                                                                                           data['trackball'],
                                                                                           data['screen'],
                                                                                           data['nav'],
                                                                                           data['major'],
                                                                                           data['system'],
                                                                                           data['app'],
                                                                                           data['keyboard'],
                                                                                           data['anyevents'],
                                                                                           data['log_level'],
                                                                                           data['count'],
                                                                                           data['log_path'])
        return command

    def analysis_log(self):
        """
        分析日志,待完善
        :return:None
        """
        with open('monkeylog.txt', 'r') as f:
            content = f.read()
            if content.find('crash') == -1:
                print '没有出现crash'
            else:
                print 'crash出现在第{}个字符'.format(content.find('crash'))

    def merge_command(self, path, *args):
        """
        组合命令,Monkey使用
        :param path:日志地址
        :param args:Monkey命令中的其他参数
        :return:None
        """
        member = ' '.join(args)
        command = 'adb shell monkey {} > {}'.format(member, path)
        self.run(command)

    def get_monkey(self, path, *args):
        """
        获取Monkey命令
        :param path: 日志地址
        :param args: Monkey命令中的其他参数
        :return:
        """
        if self.check_total(*args):
            member = ' '.join(args)
            command = 'adb shell monkey {} > {}'.format(member, path)
            return command
        else:
            return '事件百分数大于100%,请修正后再获取'

    def check_total(self, *args):
        """
        检查事件百分比是否合规,大于100则返回False
        :param args:传入的事件列表
        :return:True
        """
        rst = []
        all_list = self.deal_list(*args)
        for x in all_list:
            x = x.split(' ')[1]
            rst.append(int(x))
        num = sum(rst)
        if num > 100:
            return False
        else:
            return True

    def deal_list(self, *args):
        """
        处理列表数据,返回只有事件的列表
        :param args:传入的列表数据
        :return:list
        """
        rst = []
        for x in range(1, 12):
            rst.append(args[x])
        print rst
        return rst


if __name__ == '__main__':
    mk = Monkey()
    # print mk.get_conf()
    # mk.get_command()
    # mk.run(mk.get_command())

    # mk.analysis_log()
    print mk.merge_command('4', *['1', '2', '3'])
