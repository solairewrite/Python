# Author        : Zhixin.Ji
# Date          : 2019-12-06
# Description   : 创建.py的.bat执行文件
import os

py_path = 'F:\\Learn\\Python\\py\\tools\\Temp.py'
# py_path = 'F:\\Learn\\Python\\py\\Temp.py'
bat_path = 'F:\\Learn\\Python\\bat'


class CreatePythonBat:
    @staticmethod
    def create(in_py_file, in_bat_folder):
        """传入.py的路径和.bat的目录"""
        if not os.path.exists(in_py_file):
            print(in_py_file, ' 不存在')
            return
        if not os.path.exists(in_bat_folder):
            print(in_bat_folder, '不存在')
            return

        py_name = os.path.split(in_py_file)[1].replace('.py', '')
        bat_fullname = os.path.join(in_bat_folder, py_name + '.bat')

        with open(bat_fullname, 'w+', encoding='utf-8') as t_file:
            t_file.write('@echo off\n')
            t_file.write('cmd /k py -3 {}'.format(in_py_file))

        des = '成功' if os.path.exists(bat_fullname) else '失败'
        print('{} 创建{}'.format(bat_fullname, des))


def __test():
    CreatePythonBat.create(py_path, bat_path)


__test()
