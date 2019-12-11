# Author        : Zhixin.Ji
# Date          : 2019-12-07
# Description   : 复制小怪
"""
运行前配置:
1, 按照指定格式,创建excel
2, 设置 code_folder

py完成的功能:
1, 读取Excel,获取需要复制或换皮的小怪
2, 读取旧.vcproj,找出小怪的类
3, 将小怪的类复制进入新项目,并更新新项目的.vcproj
4, 对于每个小怪的类,更新类顶部注释
5, _conent.uc,保留旧的SkeletalMesh等资源
6, 对于每个小怪的类,检查是否有配置
7, 将旧配置改为'config(AD19)'
8, 同时将旧的.ini文件关于该类的配置,复制到新项目的.ini文件中

需要手动完成:
1, TGAD19Types.uc文件添加自己小怪的枚举
2, 引用了旧的.vcproj中不存在的类,手动添加该类
"""
import os
import sys

sys.path.append(os.path.abspath('tools'))
from ReadExcel import ReadExecl
from StringAlign import StringAlign
from ColorPrint import ColorPrint, Color
from ReplaceUCComment import ReplaceUCComment
from ReadConfig import ReadConfig

path = 'F:\\Learn\\Python\\Test\\小怪.xlsx'  # excel 路径
code_folder = 'F:\\Work\\trunk\\Development\\Src\\{}\\Classes'  # 代码路径的格式化字符串,{}是占位符
ini_path_format_str = 'F:\\Work\\trunk\\TGame\\Config\\Default{}.ini'  # 配置路径的格式化字符串


class Monster:
    ch_name = ''  # 中文名
    old_proj = ''
    new_proj = ''
    old_name = ''
    new_name = ''

    old_str = ''  # 要被替换的字符串
    new_str = ''  # 用于替换的新字符串

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
        return code_folder.format(self.old_proj)

    def get_new_proj_code_folder(self):
        return code_folder.format(self.new_proj)

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
    def refresh_ini(old_ini_short_name, new_ini_short_name,
                    old_class_name, new_class_name,
                    new_proj_name):
        """更新ini文件,短命类似 'AD19' """
        # 检测是否已经有配置
        new_ini_path = ini_path_format_str.format(new_ini_short_name)
        new_config_dict = ReadConfig(new_ini_path)
        new_proj_class, para_dict = new_config_dict.get_class(new_class_name)
        if new_proj_class is not None:
            return

        # 获取旧的配置
        old_ini_path = ini_path_format_str.format(old_ini_short_name)
        old_config_dict = ReadConfig(old_ini_path)
        old_proj_class, para_dict = old_config_dict.get_class(old_class_name)
        # uc声明了配置文件,但是配置文件并没配置那个类
        if old_proj_class is None:
            return

        # 写入新配置
        temp_path = new_ini_path + '_new'
        file = open(new_ini_path, 'r', encoding='utf-8')
        temp_file = open(temp_path, 'w+', encoding='utf-8')

        for line in file:
            temp_file.write(line)

        temp_file.write('\n\n; add by python tool by Zhixin.Ji\n')
        # todo: 替换为计算出的项目名
        t_proj_class = '[{}.{}]'.format(new_proj_name, new_class_name)
        temp_file.write(t_proj_class + '\n')
        for t_para in para_dict.keys():
            t_value = para_dict[t_para]
            t_str = '{} = {}'.format(t_para, t_value)
            temp_file.write(t_str + '\n')

        file.close()
        temp_file.close()
        os.remove(new_ini_path)
        os.rename(temp_path, new_ini_path)

    @staticmethod
    def replace_config(in_srt, new_config_content,
                       old_class_name, new_class_name,
                       new_proj_name):
        config_head = 'Config('
        config_tail = ')'
        t_head = ''
        if config_head in in_srt and config_tail in in_srt:
            t_head = config_head
        elif config_head.lower() in in_srt and config_tail in in_srt:
            t_head = config_head.lower()
        if t_head != '':
            char_before_config = in_srt[in_srt.index(t_head) - 1]
            # 屏蔽不规范的代码,可能是两个空格
            char_before_config = char_before_config \
                .replace(' ', '').replace('\t', '').replace('\n', '')
            if char_before_config == '':
                config_content = in_srt.split(t_head)[1].split(config_tail)[0]
                t_srt = in_srt.replace(config_content, new_config_content)

                CopyMonsters.refresh_ini(
                    config_content.replace(' ', ''), new_config_content,
                    old_class_name, new_class_name,
                    new_proj_name
                )

                return t_srt, True  # 修改了配置
        return in_srt, False

    @staticmethod
    def get_new_line(old_line: str, mon: Monster, new_file_path):
        """传入旧的.uc文件的一行代码,获取新的.uc文件的一行代码"""
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
    def get_vcproj_str_list(filter_tab_count, mon_name, mon_file_path_list):
        str_list = list()
        file_tab_count = filter_tab_count + 1
        path_tab_count = file_tab_count + 1
        str_list.append('\t' * filter_tab_count + '<Filter\n')
        str_list.append('\t' * file_tab_count + 'Name=\"{}\"\n'.format(mon_name))
        str_list.append('\t' * file_tab_count + '>\n')

        for t_path in mon_file_path_list:
            str_list.append('\t' * file_tab_count + '<File\n')

            t_line = os.path.split(t_path)[1]
            t_line = 'RelativePath=\".\\Classes\\{}\"\n'.format(t_line)
            str_list.append('\t' * path_tab_count + t_line)

            str_list.append('\t' * path_tab_count + '>\n')
            str_list.append('\t' * file_tab_count + '</File>\n')

        str_list.append('\t' * filter_tab_count + '</Filter>\n')
        return str_list

    @staticmethod
    def is_mon_in_vcproj(vcproj_path, mon_name):
        """检测小怪是否已经在vcproj"""
        with open(vcproj_path, 'r', encoding='utf-8') as vcproj_file:
            for line in vcproj_file:
                if 'Name=\"{}\"'.format(mon_name) in line:
                    return True
        return False

    @staticmethod
    def refresh_vcproj(vcproj_path, mon_name, mon_file_path_list):
        if CopyMonsters.is_mon_in_vcproj(vcproj_path, mon_name):
            return

        new_path = vcproj_path + '_new'
        #  for line in old_file 只能迭代一次
        old_file = open(vcproj_path, 'r', encoding='utf-8')
        new_file = open(new_path, 'w+', encoding='utf-8')

        b_in_monster_filter = False
        for line in old_file:
            new_file.write(line)

            if 'Name=\"Monster\"' in line:
                b_in_monster_filter = True

            if b_in_monster_filter and '>' in line:
                filter_tab_count = line.count('\t')

                mon_vc_list = CopyMonsters.get_vcproj_str_list(
                    filter_tab_count, mon_name, mon_file_path_list)

                for t_str in mon_vc_list:
                    new_file.write(t_str)

                b_in_monster_filter = False

        old_file.close()
        new_file.close()

        os.remove(vcproj_path)
        os.rename(new_path, vcproj_path)

    @staticmethod
    def replace_mon_comment(mon_file_path_list):
        for mon_path in mon_file_path_list:
            ReplaceUCComment.delete_comment(mon_path)
            author = 'python tool by Zhixin.Ji'
            description = ''
            ReplaceUCComment.add_comment(mon_path, author, description)

    @staticmethod
    def is_ignore_line(old_file_path, old_line):
        """此行代码是否无需替换"""
        if old_file_path.endswith('_Content.uc'):
            ignore_str_list = ['AnimSets.Add',
                               'AnimTree\'',
                               'SkeletalMesh\'',
                               'PhysicsAsset\'']
            for ignore_str in ignore_str_list:
                if ignore_str in old_line:
                    return True
        return False

    @staticmethod
    def copy_a_mon(mon: Monster):
        t_mons_dict = mon.get_all_monster_code_dict()
        ColorPrint.color_print('复制: {}, 文件数量: {}'.format(mon.ch_name, len(t_mons_dict)))
        for old_file_path in t_mons_dict.keys():
            new_file_path = t_mons_dict[old_file_path]

            old_class_name = os.path.split(old_file_path)[1].replace('.uc', '')
            new_class_name = os.path.split(new_file_path)[1].replace('.uc', '')

            old_file = open(old_file_path, 'r', encoding='ansi')
            new_file = open(new_file_path, 'w+', encoding='utf-8')

            b_need_replace_config = True
            max_config_line = 30
            line_index = 0
            for old_line in old_file:
                # 如果是动画资源,不替换
                if CopyMonsters.is_ignore_line(old_file_path, old_line):
                    new_file.write(old_line)
                else:
                    new_line = CopyMonsters.get_new_line(old_line, mon, new_file_path)
                    # 替换配置
                    line_index += 1
                    if line_index >= max_config_line:
                        b_need_replace_config = False
                    if b_need_replace_config:
                        new_line, b_config_replaced = \
                            CopyMonsters.replace_config(
                                new_line, mon.new_str,
                                old_class_name, new_class_name, mon.new_proj)
                        if b_config_replaced:
                            b_need_replace_config = False
                    new_file.write(new_line)

            old_file.close()
            new_file.close()

            # print(old_file_path)
            # ColorPrint.color_print(new_file_path)
        CopyMonsters.refresh_vcproj(
            mon.get_new_vcproj(), mon.new_name, t_mons_dict.values()
        )

        CopyMonsters.replace_mon_comment(t_mons_dict.values())
        ColorPrint.color_print(mon.ch_name + ' 复制成功', Color.green)

    @staticmethod
    def copy_mon_list(mon_list, b_only_copy_one=False, mon_new_name=''):
        for mon in mon_list:
            if b_only_copy_one:
                if mon.new_name == mon_new_name:
                    CopyMonsters.copy_a_mon(mon)
            else:
                CopyMonsters.copy_a_mon(mon)

    def copy_monsters_to_new_proj(self, b_only_copy_one=False, mon_new_name=''):
        CopyMonsters.copy_mon_list(self.copy_monsters, b_only_copy_one, mon_new_name)
        CopyMonsters.copy_mon_list(self.change_monsters, b_only_copy_one, mon_new_name)


if __name__ == '__main__':
    copy_monsters = CopyMonsters(path)
    copy_monsters.print_monsters()

    t_b_only_copy_one = False
    t_mon_new_name = 'Whore'
    copy_monsters.copy_monsters_to_new_proj(t_b_only_copy_one, t_mon_new_name)
