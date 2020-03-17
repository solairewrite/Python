# Author        : Zhixin.Ji
# Date          : 2020-03-17
# Description   : 恢复武器筛选器,在合入腾讯引擎版本后使用
# 传入武器名数组,在包含武器的项目的.vcproj文件中添加路径
# 包含武器的项目有:
# TGWeapon
# UTGameContent
# PVEGame
# PVEGameContent

import os
from colorama import Fore, Style

# ---------------------运行前需要填写的变量-----------------------
# 项目根目录
project_root_path = 'F:\\Work\\trunk'
# 要恢复的武器名称列表
weapon_list = [
    'CaneSword',  # 手杖剑
    'Sacredheart',  # 圣心手雷
    'BoneKnife',  # 骨刃
    'FrenchSword',  # 法式剑
    'Axegun',  # 战斧茅
    'Guitar',  # 魔琴
    'Scepter',  # 萨满法杖
    'Werewolf',  # 狼人双刃
]
# 包含武器文件的项目,不需要改动
weapon_projcet_list = [
    'TGWeapon',
    'UTGameContent',
    'PVEGame',
    'PVEGameContent',
]

# ---------------------全局变量---------------------------
weapon_file_count = 0


def get_weapon_file_list(in_weap_name, in_proj_name):
    """获取指定项目,指定武器,的所有文件路径列表"""
    if in_weap_name == '' or in_proj_name == '':
        return

    global project_root_path
    class_path = '{}\\Development\\Src\\{}\\Classes' \
        .format(project_root_path, in_proj_name)

    #  获取项目目录中所有的武器文件路径
    t_weapon_file_name_list = list()
    all_file_list = os.listdir(class_path)
    for file_path in all_file_list:
        file_name = os.path.split(file_path)[1]
        if in_weap_name in file_name:
            t_weapon_file_name_list.append(file_name)

    return t_weapon_file_name_list


def is_name_in_line(in_name_list, in_line):
    """是否有指定武器的任意文件名在行中"""
    for name in in_name_list:
        if name in in_line:
            return True
    return False


def print_add_result(in_weapon_name, in_proj_name):
    print(Fore.GREEN + in_proj_name)
    # print(Style.RESET_ALL)
    file_name_list = get_weapon_file_list(in_weapon_name, in_proj_name)
    for name in file_name_list:
        print(Fore.WHITE + name, end='\n')


def refresh_vcproj_weapon(in_weap_name, in_proj_name):
    """在指定项目的.vcproj中,更新武器"""
    if in_weap_name == '' or in_proj_name == '':
        return

    weapon_file_name_list = get_weapon_file_list(weapon_name, in_proj_name)

    # 读取就的vcproj,创建新vcporj,并更新武器,如果成功则保留新的
    global project_root_path
    old_vcproj_path = '{0}\\Development\\Src\\{1}\\{1}.vcproj' \
        .format(project_root_path, in_proj_name)
    new_vcproj_path = old_vcproj_path + '_new'

    old_vcproj = open(old_vcproj_path, 'r', encoding='utf-8')
    new_vcproj = open(new_vcproj_path, 'w+', encoding='utf-8')

    # 将旧的行存入内存
    t_line_arr = list()
    for line in old_vcproj:
        t_line_arr.append(line)

    # 倒序遍历,删除已经存在的武器
    for i in range(len(t_line_arr) - 1, -1, -1):
        if i == len(t_line_arr) - 1:
            continue
        if is_name_in_line(weapon_file_name_list, t_line_arr[i + 1]):
            del t_line_arr[i:i + 4]

    b_find_weapon_filter = False
    b_has_add_weapon = False
    for line in t_line_arr:
        new_vcproj.write(line)

        if b_has_add_weapon:
            continue

        # 检测武器位置
        if not b_find_weapon_filter:
            # 武器筛选器开始的层级名称
            filter_flag = 'Weapon'
            if in_proj_name == 'TGWeapon':
                filter_flag = 'TGWeapons'
            elif in_proj_name == 'UTGameContent':
                filter_flag = 'TGWeaponContent'

            if 'Name=\"{}\"'.format(filter_flag) in line:
                b_find_weapon_filter = True
        # 添加武器,这行应该是'>'
        else:
            b_has_add_weapon = True

            t_tab_count = line.count('\t')
            for weapon_file_name in weapon_file_name_list:
                t_line = '\t' * t_tab_count + '<File'
                new_vcproj.write(t_line + '\n')

                t_line = '{}RelativePath=\".\\Classes\\{}\"' \
                    .format('\t' * (t_tab_count + 1), weapon_file_name)
                new_vcproj.write(t_line + '\n')

                t_line = '\t' * (t_tab_count + 1) + '>'
                new_vcproj.write(t_line + '\n')

                t_line = '\t' * t_tab_count + '</File>'
                new_vcproj.write(t_line + '\n')

    old_vcproj.close()
    new_vcproj.close()

    os.remove(old_vcproj_path)
    os.rename(new_vcproj_path, old_vcproj_path)

    global weapon_file_count
    weapon_file_count += len(weapon_file_name_list)

    print_add_result(in_weap_name, in_proj_name)


if __name__ == '__main__':
    for weapon_name in weapon_list:
        split = '-' * 20
        print(Fore.CYAN + split + weapon_name + split)
        for project_name in weapon_projcet_list:
            refresh_vcproj_weapon(weapon_name, project_name)

    print()
    print(Fore.MAGENTA + '总共处理了{}个武器文件'.format(weapon_file_count))
