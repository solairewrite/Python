"""
Author      : Zhixin.Ji
Date        : 2019-12-03
Description : 批量修改文件名,文件内容
"""
import os

path = 'F:\\Work\\AD19Scripts'  # 文件目录

b_replace_filename = True  # 是否替换文件名
old_filename_str = 'AD17'  # 文件名,要被替换的旧字符串
new_filename_str = 'AD19'  # 文件名,用于替换的新字符串

b_replace_file_content = True  # 是够替换文件内容
old_file_content_str = old_filename_str  # 文件内容,要被替换的旧字符串
new_file_content_str = new_filename_str  # 文件内容,用于替换的新字符串


def replace_filename(inpath, in_old_str, in_new_str):
    """替换文件名"""
    t_filename_list = os.listdir(inpath)

    print('目录: ', inpath)
    print('文件数量: ', len(t_filename_list))

    for i, t_old_filename in enumerate(t_filename_list):
        t_new_filename = t_old_filename.replace(in_old_str, in_new_str)

        t_old_fullname = os.path.join(inpath, t_old_filename)
        t_new_fullname = os.path.join(inpath, t_new_filename)

        os.rename(t_old_fullname, t_new_fullname)

        print(i, ': ', t_old_filename, '\t->\t', t_new_filename)


def replace_file_content(in_filename, in_old_str, in_new_str):
    """替换文件内容"""
    t_filename = in_filename + '_new'

    # python 不能直接修改文件,需要新建一个文件,写入数据,然后替换原文件
    file = open(in_filename, 'r', encoding='utf-8')  # r: 只读
    file_new = open(t_filename, 'w+', encoding='utf-8')  # w: 写入, +: 允许新建

    for line in file:
        if in_old_str in line:
            line = line.replace(in_old_str, in_new_str)
        file_new.write(line)

    file.close()
    file_new.close()

    os.remove(in_filename)
    os.rename(t_filename, in_filename)


def replace_folder_file_content(inpath, in_old_str, in_new_str):
    """替换目录下所有文件的内容"""
    for t_filename in os.listdir(inpath):
        t_fullname = os.path.join(inpath, t_filename)
        replace_file_content(t_fullname, in_old_str, in_new_str)


def main():
    """程序入口"""
    if b_replace_filename:
        print('文件名替换: ', old_filename_str, ' -> ', new_filename_str)
        replace_filename(path, old_filename_str, new_filename_str)
        print('文件名替换完成')

    if b_replace_file_content:
        print()
        print('文件内容替换: ', old_file_content_str, ' -> ', new_file_content_str)
        replace_folder_file_content(path, old_file_content_str, new_file_content_str)
        print('文件内容替换完成')


main()
