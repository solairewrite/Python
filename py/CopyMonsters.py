# Author        : Zhixin.Ji
# Date          : 2019-12-07
# Description   : 复制小怪
import sys
import os

sys.path.append(os.path.abspath('tools'))
from ReadExcel import ReadExecl
from StringAlign import StringAlign
from ColorPrint import ColorPrint


class Monster:
    ch_name = ''  # 中文名
    old_proj = ''
    new_proj = ''
    old_name = ''
    new_name = ''

    old_str = ''  # 要被替换的字符串
    new_str = ''  # 用于替换的新字符串

    code_folder = 'F:\\Work\\trunk\\Development\\Src\\{}\\Classes'

    def init(self, ch_name, old_proj, old_name, new_proj, new_name):
        self.ch_name = ch_name
        self.old_proj = old_proj
        self.new_proj = new_proj
        self.old_name = old_name
        self.new_name = new_name

        self.old_str = str(self.old_proj).replace('TGAD', 'AD').replace('Game', '')
        self.new_str = str(self.new_proj).replace('TGAD', 'AD').replace('Game', '')

    def print_info(self):
        print('{} {}.{} <= {}.{}'
              .format(StringAlign.align(self.ch_name, 10),
                      self.new_proj,
                      StringAlign.align(self.new_name, 15),
                      self.old_proj,
                      self.old_name))

    def get_old_proj_code_folder(self):
        return self.code_folder.format(self.old_proj)

    def get_new_proj_code_folder(self):
        return self.code_folder.format(self.new_proj)

    def get_old_vcproj(self):
        return self.get_old_proj_code_folder().replace('Classes', '') \
               + '{}.vcproj'.format(self.old_proj)

    def get_new_vcproj(self):
        return self.get_new_proj_code_folder().replace('Classes', '') \
               + '{}.vcproj'.format(self.new_proj)

    # def is_monster_code(self, filename):
    #     """是否是这个小怪的代码文件"""
    #     if self.old_name not in filename:
    #         return False
    #     if 'Boss' in filename:
    #         return False
    #     # 包含怪名的其他小怪,需要手动排除
    #     # 如:MechanicalMaid 会被当成 Maid 的代码
    #     return True

    def get_new_filepath(self, old_file_path):
        new_file_path = old_file_path \
            .replace(self.old_str, self.new_str) \
            .replace(self.old_name, self.new_name)
        return new_file_path

    def get_all_monster_code_dict(self):
        t_dict = dict()
        with open(self.get_old_vcproj(), 'r', encoding='utf-8') as vcproj:
            b_in_mon = False
            for line in vcproj:
                if not b_in_mon:
                    if 'Name=\"{}\"'.format(self.old_name) in line:
                        b_in_mon = True
                if b_in_mon:
                    head = 'RelativePath=\".\\Classes\\'
                    tail = '.uc\"'
                    if head in line and tail in line:
                        filename = line.split(head)[1].split(tail)[0]
                        filename += '.uc'
                        old_file_path = os.path.join(self.get_old_proj_code_folder(), filename)
                        new_file_path = self.get_new_filepath(old_file_path)
                        t_dict[old_file_path] = new_file_path
                    if '</Filter>' in line:
                        break
        return t_dict


path = 'F:\\Learn\\Python\\Test\\小怪.xlsx'


class CopyMonsters:
    """根据excel配置表,复制小怪"""
    copy_sheet_name = '复用'
    change_sheet_name = '换皮'

    def __init__(self, excel_path):
        self.excel = ReadExecl(excel_path)
        self.copy_monsters = self.get_all_monsters(self.copy_sheet_name)
        self.change_monsters = self.get_all_monsters(self.change_sheet_name)

    def get_monster(self, index, in_new_proj=''):
        row = self.excel.get_row(index + 1)
        mon = Monster()
        # excel允许新项目名只在第一行设置
        t_new_proj = row[3]
        if row[3] == '' and in_new_proj != '':
            t_new_proj = in_new_proj
        mon.init(row[0], row[1], row[2], t_new_proj, row[4])
        return mon

    def get_all_monsters(self, sheet_name=copy_sheet_name):
        self.excel.set_current_sheet_by_name(sheet_name)
        mon_list = list()
        mon_count = self.excel.get_row_count() - 1
        new_proj = self.get_monster(0).new_proj
        for i in range(mon_count):
            mon = self.get_monster(i, new_proj)
            mon_list.append(mon)
        return mon_list

    def print_monsters(self):
        ColorPrint.color_print('{}: '.format(self.copy_sheet_name))
        for mon in self.copy_monsters:
            mon.print_info()
        ColorPrint.color_print('{}: '.format(self.change_sheet_name))
        for mon in self.change_monsters:
            mon.print_info()

    @staticmethod
    def get_new_line(old_line: str, mon: Monster, new_file_path):
        new_line = old_line
        if 'class' in old_line and 'extends' in old_line:
            old_class = old_line.split('class')[1].split('extends')[0]
            new_class = os.path.split(new_file_path)[1].replace('.uc', '')
            new_line = new_line.replace(old_class, ' {} '.format(new_class))
        if mon.old_str in old_line:
            new_line = new_line.replace(mon.old_str, mon.new_str)  # AD16->AD19
            new_line = new_line.replace(mon.old_name, mon.new_name)  # 继承的类
        return new_line

    @staticmethod
    def refresh_vcproj(vcproj_path, mon_name, mon_file_path_list):
        new_path = vcproj_path + '_new'
        old_file = open(vcproj_path, 'r', encoding='utf-8')
        new_file = open(new_path, 'w+', encoding='utf-8')

        b_find_mon = False
        b_in_mon = False
        tab_count = 0
        mon_vc_list = list()
        for line in old_file:
            if 'Name=\"Monster\"' in line:
                b_find_mon = True
                mon_vc_list.append(line)  # del
            if b_find_mon and '>' in line:
                b_in_mon = True
                mon_vc_list.append(line)  # del
                # temp = [line]
                # print(temp)
                filter_tab_count = line.count('\t')
                file_tab_count = filter_tab_count + 1
                path_tab_count = file_tab_count + 1
                # print(tab_count)
                mon_vc_list.append('\t' * filter_tab_count + '<Filter\n')
                mon_vc_list.append('\t' * file_tab_count + 'Name=\"{}\"\n'.format(mon_name))
                mon_vc_list.append('\t' * file_tab_count + '>\n')

                for t_path in mon_file_path_list:
                    mon_vc_list.append('\t' * file_tab_count + '<File\n')

                    t_line = os.path.split(t_path)[1]
                    t_line = 'RelativePath=\".\\Classes\\{}\"\n'.format(t_line)
                    mon_vc_list.append('\t' * path_tab_count + t_line)

                    mon_vc_list.append('\t' * path_tab_count + '>\n')
                    mon_vc_list.append('\t' * file_tab_count + '</File>\n')

                mon_vc_list.append('\t' * filter_tab_count + '</Filter>\n')

                break

        for line in mon_vc_list:
            print(line, end='')

        old_file.close()
        new_file.close()

    @staticmethod
    def copy_a_mon(mon: Monster):
        t_mons_dict = mon.get_all_monster_code_dict()
        mon.get_all_monster_code_dict()
        for old_file_path in t_mons_dict.keys():
            new_file_path = t_mons_dict[old_file_path]

            # old_file = open(old_file_path, 'r', encoding='ansi')
            # new_file = open(new_file_path, 'w+', encoding='utf-8')
            #
            # for old_line in old_file:
            #     new_line = CopyMonsters.get_new_line(old_line, mon, new_file_path)
            #     new_file.write(new_line)
            #
            # old_file.close()
            # new_file.close()

            # print(old_file_path)
            # ColorPrint.color_print(new_file_path)

        print()
        CopyMonsters.refresh_vcproj(
            mon.get_new_vcproj(), mon.new_name, t_mons_dict.values()
        )

    def copy_monsters_to_new_proj(self):
        for mon in self.copy_monsters:
            if mon.new_name == 'Rocket':
                CopyMonsters.copy_a_mon(mon)


if __name__ == '__main__':
    copy_monsters = CopyMonsters(path)
    # copy_monsters.print_monsters()
    copy_monsters.copy_monsters_to_new_proj()
