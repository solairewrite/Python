"""
Author      : Zhixin.Ji
Date        : 2019-12-04
Description : 检测.uc文件中的config变量与.ini中的变量差异
              列出uc中声明,但是ini未配置的变量;以及ini中配置,但是uc中未声明的变量
"""
import os
from enum import Enum
import ctypes  # 命令行彩色输出
import sys


# import chardet


class RunType(Enum):  # 运行模式
    pycharm = 0  # 编辑器运行文件
    cmd = 1  # 命令行运行文件


run_type = RunType.cmd  # 运行文件前请先选择运行模式!!!
uc_folder_path = 'F:\\Work\\trunk\\Development\\Src\\TGAD19Game\\Classes'
ini_fullname = 'F:\\Work\\trunk\\TGame\\Config\\DefaultAD19.ini'
# ini_fullname = 'F:\\Learn\\Python\\Test\\DefaultAD18.ini'
project_name = 'TGAD19Game'

b_print_right_info = False  # 是否打印正确信息
b_print_config_class = True  # 打印字典时,是否打印类
b_print_config_para = True  # 打印字典时,是否打印参数

ini_config_dict = {}  # ini文件变量字典
uc_config_dict = {}  # 目录下,所有uc文件,配置变量字典

error_info = list()  # 记录所有错误信息


def print_and_record(in_str='\n'):
    print(in_str)
    error_info.append(in_str)
    error_info.append('\n')


def read_ini():
    print_and_record('配置文件: ' + ini_fullname)
    # with open(ini_fullname, 'rb') as t_ini_binary:
    #     t_encode = chardet.detect(t_ini_binary.read()).get('encoding')
    # t_ini = open(ini_fullname, 'r', encoding=t_encode)
    t_ini = open(ini_fullname, 'r', encoding='utf-8')
    t_class = ''
    for line in t_ini:
        if not len(line) or line.startswith(';'):
            continue

        if (line.startswith('[' + project_name + '.')
                and line.endswith(']\n')):
            t_class = line.split('.')[1].split(']')[0]

        if t_class == '':
            continue
        if t_class not in ini_config_dict:
            ini_config_dict[t_class] = list()

        t_pair = line.split('=')
        t_para = t_pair[0]
        t_para = t_para.replace(' ', '')
        if len(t_pair) >= 2:
            if t_para not in ini_config_dict[t_class]:
                ini_config_dict[t_class].append(t_para)


def print_config_dict(t_config: dict, in_des=''):
    t_print_list = list()
    t_para_count = 0
    for t_class in t_config.keys():
        if b_print_config_class:
            t_print_list.append('类名: ' + t_class)
        if b_print_config_para:
            for t_para in t_config[t_class]:
                t_print_list.append(t_para)
                t_para_count += 1
        if b_print_config_para:
            t_print_list.append('')
    print_and_record('%s总共有 %d 个类, %d 个参数' % (in_des, len(t_config.keys()), t_para_count))
    for line in t_print_list:
        print_and_record(line)


def is_config_uc(in_fullpath):
    """判断是否是需要指定配置的文件"""
    # 配置字符串
    t_ini_str_arr = ini_fullname.split('\\')
    t_ini_str = t_ini_str_arr[-1]
    t_ini_str = t_ini_str.replace('Default', '')
    t_ini_str = t_ini_str.replace('.ini', '')
    t_ini_str = 'config(%s)' % t_ini_str

    t_file = open(in_fullpath, 'r', encoding='utf-8')
    for line in t_file:
        if t_ini_str in line:
            return True
        if line.startswith('var '):
            return False


def read_uc(in_fullpath):
    """读取代码的配置变量,写入全局字典"""
    if not is_config_uc(in_fullpath):
        return

    t_str_arr = in_fullpath.split('\\')
    t_class = t_str_arr[-1].replace('.uc', '')

    uc_config_dict[t_class] = list()

    t_file = open(in_fullpath, 'r', encoding='utf-8')
    for line in t_file:
        if line.startswith('var config '):
            t_str_arr = line.split(' ')
            # 发现如果代码写的不规范,两个空格导致中间会有空字符
            # 倒叙数组,0-100数组
            for i in reversed(range(len(t_str_arr))):
                if t_str_arr[i] == '':
                    del t_str_arr[i]

            if len(t_str_arr) >= 4:  # var config int i; // 注释
                t_config_para = t_str_arr[3].split(';')[0]
                uc_config_dict[t_class].append(t_config_para)


def read_folder(inpath):
    t_file_name_list = os.listdir(inpath)
    print_and_record('代码目录: ' + inpath + ', 文件数量' + str(len(t_file_name_list)))
    for t_file_name in t_file_name_list:
        if not t_file_name.endswith('.uc'):
            continue
        t_fullpath = os.path.join(inpath, t_file_name)
        read_uc(t_fullpath)


def get_class_and_para_count(in_dict: dict):
    t_class_count = 0
    t_para_count = 0
    for key in in_dict.keys():
        t_class_count += 1
        t_para_count += len(in_dict[key])
    return t_class_count, t_para_count


def compare_list(list_a, list_b):
    """返回共有元素列表,仅在a中元素的列表,仅在b中元素的列表"""
    both_list = list()
    only_a_list = list()
    only_b_list = list()
    for a in list_a:
        if a in list_b:
            both_list.append(a)
        else:
            only_a_list.append(a)
    for b in list_b:
        if b in list_a:
            if b not in both_list:
                both_list.append(b)
        else:
            only_b_list.append(b)
    return both_list, only_a_list, only_b_list


def change_cmd_color(in_color=0x0f):
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(-11)
    ctypes.windll.kernel32.SetConsoleTextAttribute(std_out_handle, in_color)


def color_print(in_str, color_index=33, color_cmd=0x0e):
    """彩色打印"""
    # 红31,绿32,黄33,蓝34,洋红35,青36
    # 红0x0c,绿0x0a,黄0x0e,蓝0x09,洋红0x0d,青0x0b

    # \033[     : 开头
    # \033[0m   : 结尾
    # 1         : 显示方式,高亮
    # 33        : 前景色
    # m         : 正文前面加
    if run_type == RunType.pycharm:
        print_and_record('\033[1;%dm%s\033[0m' % (color_index, in_str))
    elif run_type == RunType.cmd:
        change_cmd_color(color_cmd)
        sys.stdout.write(in_str)
        sys.stdout.write('\n')
        change_cmd_color()

        error_info.append(in_str)
        error_info.append('\n')


def print_red(in_str):
    color_print(in_str, 31, 0x0c)


def print_green(in_str):
    color_print(in_str, 32, 0x0a)


def print_blue(in_str):
    color_print(in_str, 34, 0x09)


def print_cyan(in_str):
    color_print(in_str, 36, 0x0b)


def print_list(in_list, in_title):
    print_cyan(in_title)
    for item in in_list:
        print_and_record(item)
    print_and_record()


def print_list_difference(list_both, list_ini, list_uc, element_des):
    print_green('%s数量: 公共: %d, 仅ini: %d, 仅uc: %d'
                % (element_des, len(list_both), len(list_ini), len(list_uc)))
    if b_print_right_info:
        print_list(list_both, '公共' + element_des)
    if len(list_ini):
        print_list(list_ini, '仅存在于ini中的' + element_des)
    if len(list_uc):
        print_list(list_uc, '仅存在于uc中的' + element_des)


def compare_dict_class():
    """对比ini和uc中的类,返回公共类"""
    ini_class_count, ini_para_count = get_class_and_para_count(ini_config_dict)
    uc_class_count, uc_para_count = get_class_and_para_count(uc_config_dict)
    color_print('ini文件 class数量: %d,\t 参数数量: %d' % (ini_class_count, ini_para_count))
    color_print(' uc文件 class数量: %d,\t 参数数量: %d' % (uc_class_count, uc_para_count))

    class_in_both, class_only_in_ini, class_only_in_uc \
        = compare_list(ini_config_dict.keys(), uc_config_dict.keys())
    print_list_difference(class_in_both, class_only_in_ini, class_only_in_uc, 'class')
    return class_in_both


def compare_class_para(in_class):
    """对比ini和uc类中的参数,返回是否找到不一样的参数"""
    para_in_both, para_in_ini, para_in_uc \
        = compare_list(ini_config_dict[in_class], uc_config_dict[in_class])
    if not len(para_in_ini) and not len(para_in_uc):
        return False
    print_red('错误类: ' + in_class)
    print_list_difference(para_in_both, para_in_ini, para_in_uc, '参数')
    return True


def compare_config():
    print_and_record()
    t_class_list = compare_dict_class()
    print_and_record()
    for t_class in t_class_list:
        compare_class_para(t_class)


def write_error_txt(txt_name='config_error_info.txt'):
    # current working directory
    t_fullname = os.getcwd() + '\\' + txt_name
    with open(t_fullname, 'w+', encoding='utf-8') as t_file:
        for line in error_info:
            t_file.write(line)
    print_red('数据写入' + t_fullname)


def main():
    read_ini()
    # print_config_dict(ini_config_dict, 'ini')
    read_folder(uc_folder_path)
    # print_config_dict(uc_config_dict, 'uc')
    compare_config()
    write_error_txt()


main()
