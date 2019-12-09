# Author        : Zhixin.Ji
# Date          : 2019/12/6
# Description   : 彩色打印,通过命令行参数检测运行方式,pycharm 或 cmd
from enum import Enum
import ctypes
import sys
import argparse
from colorama import init  # cmd输出彩色文字的模块

init(autoreset=True)  # cmd也能彩色输出,autoreset:自动恢复到默认颜色


class RunType(Enum):
    """启动py文件的方式"""
    pycharm = 0  # 编辑器运行文件
    cmd = 1  # 命令行运行文件


class ColorValue:
    """颜色值结构"""
    # print()函数的颜色
    print_value = 37

    # cmd颜色
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
    __b_finish_set_run_type = False

    @staticmethod
    def __get_run_type():
        """根据命令行参数获取运行类型"""
        if ColorPrint.__b_finish_set_run_type:
            return ColorPrint.__run_type

        parser = argparse.ArgumentParser(description='命令行参数分析')
        parser.add_argument('-c', '--bcmd',
                            action='store_true',
                            default=False,
                            help='程序是否以命令行启动')
        args = parser.parse_args()
        if args.bcmd:
            ColorPrint.__run_type = RunType.cmd
        ColorPrint.__b_finish_set_run_type = True

        return ColorPrint.__run_type

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
        """彩色输出"""
        ColorPrint.__default_color_print(in_str, in_color_value.print_value, end)
        # if ColorPrint.__get_run_type() == RunType.pycharm:
        #     ColorPrint.__default_color_print(in_str, in_color_value.print_value, end)
        # elif ColorPrint.__get_run_type() == RunType.cmd:
        #     ColorPrint.__cmd_color_print(in_str, in_color_value.cmd_value, end)
