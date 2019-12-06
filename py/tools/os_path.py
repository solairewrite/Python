# Author        : Zhixin.Ji
# Date          : 2019-12-06
# Description   : 记录os的路径函数
import os

# __file__              文件路径
# os.getcwd()           目录路径
# os.path.abspath('.')  目录路径
# os.path.abspath('..') 上级目录
# os.path.dirname()     指定文件的目录
# os.path.abspath()     绝对路径
# os.path.split()       传入文件路径,输出目录和文件名
#                       传入目录,输出上级目录和文件夹名

print()

print(__file__)                     # F:/Learn/Python/py/tools/os_path.py
print(os.getcwd())                  # F:\Learn\Python\py\tools
print(os.path.abspath('.'))         # F:\Learn\Python\py\tools
print(os.path.abspath('..'))        # F:\Learn\Python\py
print('--------------------------------------')
print(os.path.dirname(__file__))    # F:/Learn/Python/py/tools
print(os.path.abspath(__file__))    # F:\Learn\Python\py\tools\os_path.py
print(os.path.split(__file__))      # ('F:/Learn/Python/py/tools', 'os_path.py')
print(os.path.split(os.getcwd()))   # ('F:\\Learn\\Python\\py', 'tools')
