# import sys
# import os
# cmd运行时,需要将被import的文件目录,添加到环境变量中
# sys.path.append(os.path.abspath('../py/tools'))
import argparse

# 或 pycharm,右击文件夹,Make Directory as: Sources Root
# from ColorPrint import ColorPrint, RunType, Color
from tools.ColorPrint import ColorPrint, RunType, Color

bcmd = False  # 是否以命令行启动
str_hello = 'hello world'


def test_parser():
    parser = argparse.ArgumentParser(description='命令行参数分析')
    parser.add_argument('-A', '--author', default='未知作者')
    parser.add_argument('-bcmd', type=bool, default=False)
    args = parser.parse_args()
    # print(args)
    # author = args.author
    # print(author)
    global bcmd  # 外部变量,否则默认是局部变量
    bcmd = args.bcmd
    # print(bcmd)


def test_color_print():
    print(str_hello)

    color_print = ColorPrint()
    if bcmd:
        color_print.change_run_type(RunType.cmd)

    color_print.color_print(str_hello)
    color_print.color_print(str_hello, Color.black)
    color_print.color_print(str_hello, Color.red)
    color_print.color_print(str_hello, Color.green)
    color_print.color_print(str_hello, Color.yellow)
    color_print.color_print(str_hello, Color.blue)
    color_print.color_print(str_hello, Color.magenta)
    color_print.color_print(str_hello, Color.white)
    color_print.color_print(str_hello, Color.cyan)

    print(str_hello)


def main():
    print()
    test_parser()
    test_color_print()


main()
