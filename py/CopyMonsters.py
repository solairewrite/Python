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
    ch_name = ''
    old_proj = ''
    new_proj = ''
    old_name = ''
    new_name = ''

    def init(self, ch_name, old_proj, old_name, new_proj, new_name):
        self.ch_name = ch_name
        self.old_proj = old_proj
        self.new_proj = new_proj
        self.old_name = old_name
        self.new_name = new_name

    def print_info(self):
        print('{} {}.{} <= {}.{}'
              .format(StringAlign.align(self.ch_name, 10),
                      self.new_proj,
                      StringAlign.align(self.new_name, 15),
                      self.old_proj,
                      self.old_name))


path = 'E:\\Learn\\Python\\py_tools\\Test\\小怪.xlsx'


class CopyMonsters:
    """根据excel配置表,复制小怪"""

    def __init__(self, excel_path):
        self.excel = ReadExecl(excel_path)
        self.copy_monsters = self.get_all_monsters('复用')
        self.change_monsters = self.get_all_monsters('换皮')

    def get_monster(self, index, in_new_proj=''):
        row = self.excel.get_row(index + 1)
        mon = Monster()
        # excel允许新项目名只在第一行设置
        t_new_proj = row[3]
        if row[3] == '' and in_new_proj != '':
            t_new_proj = in_new_proj
        mon.init(row[0], row[1], row[2], t_new_proj, row[4])
        return mon

    def get_all_monsters(self, sheet_name='复用'):
        self.excel.set_current_sheet_by_name(sheet_name)
        mon_list = list()
        mon_count = self.excel.get_row_count() - 1
        new_proj = self.get_monster(0).new_proj
        for i in range(mon_count):
            mon = self.get_monster(i, new_proj)
            mon_list.append(mon)
        return mon_list

    def print_monsters(self):
        ColorPrint.color_print('复用怪: ')
        for mon in self.copy_monsters:
            mon.print_info()
        ColorPrint.color_print('换皮怪: ')
        for mon in self.change_monsters:
            mon.print_info()


if __name__ == '__main__':
    copy_monsters = CopyMonsters(path)
    copy_monsters.print_monsters()
