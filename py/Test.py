# 使用from ... import ...,需要为python解释器指定搜索路径 PYTHONPATH
# sys.path.append()
# 或 pycharm,右击文件夹,Mark Directory as: Sources Root
import sys
import os

sys.path.append(os.path.abspath('../py/tools'))

from ColorPrint import ColorPrint, Color


def test_color_print():
    str_hello = 'hello world'
    print(str_hello)

    ColorPrint.color_print(str_hello)
    ColorPrint.color_print(str_hello, Color.black)
    ColorPrint.color_print(str_hello, Color.red)
    ColorPrint.color_print(str_hello, Color.green)
    ColorPrint.color_print(str_hello, Color.yellow)
    ColorPrint.color_print(str_hello, Color.blue)
    ColorPrint.color_print(str_hello, Color.magenta)
    ColorPrint.color_print(str_hello, Color.white)
    ColorPrint.color_print(str_hello, Color.cyan)

    print(str_hello)


# 计算机不能理解高级语言,只能理解机器语言
# 必须把高级语言翻译成机器语言,计算机才能执行高级语言编写的程序
# 编译型语言: C++
#   在程序执行前,需要专门的编译过程,把程序编译为机器语言,效率高
# 解释型语言: Python,JavaScript
#   无需编译,程序运行时才翻译,效率低

# Python程序运行时,从模块顶层开始,逐行执行,不需要程序入口(main())
# __name__: Python内置变量,指当前模块
#   如果是被执行的.py文件,值为'__main__',如果是被导入的模块,值为模块名
# __main__: 被执行的模块
# if __name__ == '__main__': 仅当模块是被执行的模块时,代码才运行
#   如果是被引入的模块,代码不执行
if __name__ == '__main__':
    print()
    test_color_print()
