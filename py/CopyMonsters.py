# Author        : Zhixin.Ji
# Date          : 2019-12-07
# Description   : 复制小怪
from ReadExcel import ReadExecl


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
              .format(self.ch_name, self.new_proj, self.new_name,
                      self.old_proj, self.old_name))


path = 'E:\\Learn\\Python\\py_tools\\Test\\小怪.xlsx'

excel = ReadExecl(path)
excel.set_current_sheet_by_name('复用')


def get_monster(index, in_new_proj=''):
    row = excel.get_row(index + 1)
    mon = Monster()
    t_new_proj = row[3]
    if row[3] == '' and in_new_proj != '':
        t_new_proj = in_new_proj
    mon.init(row[0], row[1], row[2], t_new_proj, row[4])
    return mon


def get_all_monsters(sheet_name='复用'):
    excel.set_current_sheet_by_name(sheet_name)
    mon_list = list()
    mon_count = excel.get_row_count() - 1
    new_proj = get_monster(0).new_proj
    for i in range(mon_count):
        mon = get_monster(i, new_proj)
        mon_list.append(mon)
    return mon_list


copy_monsters = get_all_monsters()
for mon in copy_monsters:
    mon.print_info()
