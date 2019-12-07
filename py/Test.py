# cmd运行时,需要将被import的文件目录,添加到环境变量中
# sys.path.append(os.path.abspath('../py/tools'))

# 或 pycharm,右击文件夹,Make Directory as: Sources Root
from tools.ColorPrint import ColorPrint, Color

str_hello = 'hello world'


def test_color_print():
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


def test():
    print()
    test_color_print()


test()
