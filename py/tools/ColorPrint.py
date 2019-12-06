# Author        : Zhixin.Ji
# Date          : 2019/12/6
# Description   : 彩色打印,包括pycharm运行,或cmd运行
from enum import Enum
import ctypes
import sys


class RunType(Enum):
    """启动py文件的方式"""
    pycharm = 0  # 编辑器运行文件
    cmd = 1  # 命令行运行文件


class ColorValue:
    """颜色值结构"""
    # print()函数的颜色
    # 黑30,红31,绿32,黄33,蓝34,洋红35,青36,白37
    print_value = 37

    # cmd颜色
    # 黑0x00,红0x0c,绿0x0a,黄0x0e,蓝0x09,洋红0x0d,青0x0b,白0x0e
    cmd_value = 0x0e

    # 构造函数
    def __init__(self, print_value=37, cmd_value=0x0e):
        self.print_value = print_value
        self.cmd_value = cmd_value


class Color:
    black = ColorValue(30, 0x00)
    red = ColorValue(31, 0x0c)
    green = ColorValue(32, 0x0a)
    yellow = ColorValue(33, 0x0e)
    blue = ColorValue(34, 0x09)
    magenta = ColorValue(35, 0x0d)  # 洋红
    cyan = ColorValue(36, 0x0b)
    white = ColorValue(37, 0x0f)


class ColorPrint:
    """彩色输出,pycharm运行或cmd运行"""
    __run_type = RunType.pycharm

    @staticmethod
    def change_run_type(new_type=RunType.pycharm):
        ColorPrint.__run_type = new_type

    @staticmethod
    def default_run_type():
        ColorPrint.change_run_type()

    # 函数名前加上'__'表示私有函数,默认函数为public
    @staticmethod
    def __default_color_print(in_str: str, in_color=Color.yellow.print_value, end='\n'):
        """pycharm启动文件,彩色输出"""
        print('\033[1;%dm%s\033[0m' % (in_color, in_str), end=end)

    @staticmethod
    def __change_cmd_color(in_color=Color.white.cmd_value):
        """修改cmd输出颜色"""
        std_out_handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.SetConsoleTextAttribute(std_out_handle, in_color)

    @staticmethod
    def __cmd_color_print(in_srt: str, in_color=Color.yellow.cmd_value, end='\n'):
        """cmd启动文件,彩色输出"""
        ColorPrint.__change_cmd_color(in_color)
        sys.stdout.write(in_srt)
        sys.stdout.write(end)
        ColorPrint.__change_cmd_color()

    @staticmethod
    def color_print(in_str, in_color_value=Color.yellow, end='\n'):
        """彩色输出,需要手动设置启动模式"""
        if ColorPrint.__run_type == RunType.pycharm:
            ColorPrint.__default_color_print(in_str, in_color_value.print_value, end)
        elif ColorPrint.__run_type == RunType.cmd:
            ColorPrint.__cmd_color_print(in_str, in_color_value.cmd_value, end)
