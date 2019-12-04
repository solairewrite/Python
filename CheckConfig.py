"""
Author      : Zhixin.Ji
Date        : 2019-12-04
Description : 检测.uc文件中的config变量与.ini中的变量差异
              列出uc中声明,但是ini未配置的变量;以及ini中配置,但是uc中未声明的变量
"""
import os

uc_folder_path = 'F:\\Learn\\Python\\Test'
ini_fullname = 'F:\\Learn\\Python\\Test\\DefaultAD18.ini'
project_name = 'TGAD18Game'

b_print_config_class = True
b_print_config_para = False

config_dict = {}


def read_ini():
    print('配置文件: ', ini_fullname)
    t_ini = open(ini_fullname, 'r', encoding='utf-8')
    t_class = ''
    for line in t_ini:
        if not len(line) or line.startswith(';'):
            continue

        if (line.startswith('[' + project_name + '.')
                and line.endswith(']\n')):
            t_class = line.split('.')[1].split(']')[0]

        if t_class == '':
            return
        if t_class not in config_dict:
            config_dict[t_class] = {}

        t_pair = line.split('=')
        if len(t_pair) == 2:
            t_value = t_pair[1]
            t_value = t_value.replace(' ', '')
            t_value = t_value.replace('\t', '')
            t_value = t_value.replace('\n', '')
            if ';' in t_value:
                t_value = t_value.split(';')[0]
            config_dict[t_class][t_pair[0]] = t_value


def print_config(t_config: dict):
    print('配置文件总共有 %d 个类' % len(t_config.keys()))
    t_para_count = 0
    for t_class in t_config.keys():
        if b_print_config_class:
            print('类名: ' + t_class)
        for t_key in t_config[t_class].keys():
            if b_print_config_para:
                print(t_key, '=', t_config[t_class][t_key])
            t_para_count += 1
        if b_print_config_para:
            print()
    print('配置文件总共有 %d 个类, %d 个参数' % (len(t_config.keys()), t_para_count))


def read_uc(in_fullpath):
    t_file = open(in_fullpath, 'r', encoding='utf-8')
    b_config_uc = False
    for line in t_file:
        # TODO: 真实配置
        if not b_config_uc and ('config(%s)' % 'AD18') in line:
            b_config_uc = True
            t_str_arr = in_fullpath.split('\\')
            print('类名: ', t_str_arr[len(t_str_arr) - 1])
        if not b_config_uc and line.startswith('var '):  # 无需配置
            return
        if b_config_uc and line.startswith('var config '):
            t_str_arr = line.split(' ')
            if len(t_str_arr) == 4:  # var config int i;
                # TODO: 后面的注释里可能有';'
                if len(t_str_arr[3]) >= 2 and t_str_arr[3].endswith(';\n'):
                    t_config_para = t_str_arr[3].split(';')[0]
                    print(t_config_para)
    print()


def read_folder(inpath):
    t_file_name_list = os.listdir(inpath)
    print('代码目录: ', inpath)
    print('文件数量', len(t_file_name_list))
    for t_file_name in t_file_name_list:
        if not t_file_name.endswith('.uc'):
            continue
        t_fullpath = os.path.join(inpath, t_file_name)
        read_uc(t_fullpath)


def main():
    read_ini()
    # print_config(config_dict)
    # print(config_dict)
    read_folder(uc_folder_path)


main()
