# Author        : Zhixin.Ji
# Date          : 2019/12/4 0004
# Description   : 修改文件编码格式
# 问题: chardet检测encoding不准
#       空白的ANSI编码文件检测为None
#       全英文,ascii编码的.uc文件,转换utf-8无效
#       所以手动加了一行中文,而且中文不能删除,否则就不会被检测为utf-8

import os
import chardet  # 文件编码,项目设置中,进入pip,查找chardet,安装
import re  # 正则表达式

path = 'F:\\Work\\trunk\\Development\\Src\\TGAD18Game\\Classes'  # 文件目录
file_fullpath = 'F:\\Work\\trunk\\TGame\\Config\\DefaultAD18.ini'  # 单个修改文件的全路径
new_encoding = 'utf-8'  # 新的编码格式
filename_display_length = 40  # 文件名显示长度

b_print_curr_encoding = True  # 是否显示当前编码
b_change_all_file_encoding = False  # 是否修改文件夹下所有文件编码
b_change_one_file_encoding = False  # 是否修改一个文件的编码


def remove_line(in_fullname, instr):
    """删除文件中包含指定字符串的行"""
    with open(in_fullname, 'r', encoding=new_encoding) as t_read:
        lines = t_read.readlines()
    with open(in_fullname, 'w', encoding=new_encoding) as t_write:
        for line in lines:
            if instr in line:
                continue
            t_write.write(line)


def is_encoding(in_fullname, in_encoding):
    """检测文件是否是指定编码"""
    b_right_encode = False

    with open(in_fullname, 'rb+') as t_file:  # 代码块结束时,自动关闭文件
        t_data = t_file.read()
        # 获取文件编码,很可能获取到错误的编码,confidence: 精准度
        t_encode = chardet.detect(t_data).get('encoding')

        if t_encode is not None:
            # 检测字符串,不分大小写,记事本会保存为'UTF-8-SIG',所以不能直接检测 == 'utf-8'
            t_find_result = re.findall(in_encoding, t_encode, flags=re.IGNORECASE)
            if len(t_find_result) > 0:
                b_right_encode = True

    return b_right_encode


def print_change_result(in_fullname, b_change_success, in_curr_encode, in_target_encode):
    """打印转换编码结果"""
    t_path_str_list = in_fullname.split('\\')  # 字符串分割
    t_filename = t_path_str_list[len(t_path_str_list) - 1]
    t_des = ' 转换编码失败'
    if b_change_success:
        t_des = in_curr_encode + '\t->\t' + in_target_encode
    print(t_filename.ljust(filename_display_length), t_des)


def change_encoding(in_fullname, in_encoding):
    """修改文件编码"""
    b_change_success = False
    if is_encoding(in_fullname, in_encoding):
        return b_change_success

    with open(in_fullname, 'rb+') as t_file:  # 代码块结束时,自动关闭文件
        t_data = t_file.read()
        # 获取文件编码,很可能获取到错误的编码,confidence: 精准度
        t_encode = chardet.detect(t_data).get('encoding')

        try:
            print('------------------%s---------------------------' % in_fullname)
            # t_decode_data = t_data.decode(t_encode)
            t_decode_data = t_data.decode('ansi')  # ansi 被错误解析为 gb2312
            t_encode_data = t_decode_data.encode(in_encoding)  # byte
            # utf-8编码内如果没有中文,转换失败
            if in_encoding == 'utf-8':
                t_encode_data = '// 转为utf-8编码\n'.encode(in_encoding) + t_encode_data

            # 经测试,需要新建文件才能生效,再删除原文件
            t_new_fullname = in_fullname + '_new'
            with open(t_new_fullname, 'wb+') as temp:
                temp.write(t_encode_data)

            t_file.close()
            os.remove(in_fullname)
            os.rename(t_new_fullname, in_fullname)

            # remove_line(in_fullname, '转为utf-8编码')

            b_change_success = True
        except IOError:
            pass

    print_change_result(in_fullname, b_change_success, t_encode, in_encoding)

    return b_change_success


def change_all_file_encoding(inpath, in_encoding):
    t_filename_list = os.listdir(inpath)

    print('目录: ', inpath)
    print('文件数量: ', len(t_filename_list))

    t_change_count = 0
    for t_filename in t_filename_list:
        t_fullname = os.path.join(inpath, t_filename)
        if change_encoding(t_fullname, in_encoding):
            t_change_count += 1
    print('修改编码文件个数: ', t_change_count)


def print_all_file_encoding(inpath, indes=''):
    t_filename_list = os.listdir(inpath)

    print('目录: ', inpath)
    print('文件数量: ', len(t_filename_list))

    for t_filename in t_filename_list:
        t_fullname = os.path.join(inpath, t_filename)
        file = open(t_fullname, 'rb')  # rb: 以二进制打开,只读
        data = file.read()
        print(t_filename.ljust(filename_display_length), '\t', end='')  # 不换行
        print('{0}编码: '.format(indes), end='')
        print(chardet.detect(data).get('encoding'))


def main():
    if b_change_all_file_encoding:
        # print_all_file_encoding(path, '初始')
        print()
        change_all_file_encoding(path, new_encoding)
        print()
        print_all_file_encoding(path, '修改后')

    elif b_print_curr_encoding:
        print_all_file_encoding(path)

    if b_change_one_file_encoding:
        change_encoding(file_fullpath, new_encoding)


main()
