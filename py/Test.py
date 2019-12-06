import sys
import os

# cmd运行时,需要将被import的文件目录,添加到环境变量中
sys.path.append(os.path.abspath('../py/tools'))
from ColorPrint import ColorPrint, RunType, Color

str_hello = 'hello world'


def test_color_print():
    print(str_hello)

    color_print = ColorPrint()
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
    test_color_print()


main()
