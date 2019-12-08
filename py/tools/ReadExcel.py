# Author        : Zhixin.Ji
# Date          : 2019-12-06
# Description   : 读取Excel
import xlrd
from StringAlign import StringAlign
from ColorPrint import ColorPrint, Color

# path = 'F:\\Learn\\Python\\Test\\小怪.xlsx'
path = 'E:\\Learn\\Python\\py_tools\\Test\\小怪.xlsx'


class ReadExecl:
    def __init__(self, filepath):
        self.excel = xlrd.open_workbook(filepath)
        self.sheet = self.excel.sheets()[0]
        self.print_sheet_name_list()

    def set_current_sheet(self, index=0):
        self.sheet = self.excel.sheets()[index]

    def set_current_sheet_by_name(self, name):
        if name not in self.excel.sheet_names():
            return
        index = self.excel.sheet_names().index(name)
        self.sheet = self.excel.sheets()[index]

    def get_row_count(self):
        return self.sheet.nrows

    def get_row(self, index):
        if index >= self.get_row_count():
            return None
        return self.sheet.row_values(index)

    def get_table(self):
        table = list()
        row_count = self.get_row_count()
        for i in range(row_count):
            table.append(self.get_row(i))
        return table

    def print_sheet_name_list(self):
        des = '所有的sheet: '
        for name in self.excel.sheet_names():
            des = des + name + '  '
        # cmd彩色输出不能在一行进行多次
        ColorPrint.color_print(des, Color.green)
        # print()

    def print_row(self, row_index=0, display_length=20):
        des = ''
        # row_values()是个函数,True会被解析为1,1会被解析为1.0
        for cell in self.sheet.row_values(row_index):
            if cell == '':
                cell = '/'
            t_str = StringAlign.align(str(cell), display_length)
            des = des + t_str
        if row_index == 0:
            ColorPrint.color_print(des)
        else:
            print(des)

    def print_title(self):
        self.print_row(0)

    @staticmethod
    def get_type_str(type_index):
        """sheet.row_types()返回的值(0,1,2...)对应的类型"""
        if type_index == 0:
            return 'None'
        elif type_index == 1:
            return 'str'
        elif type_index == 2:
            return 'int / float'
        elif type_index == 4:
            return 'bool'
        else:
            return '未知类型'

    def print_sheet(self):
        row_count = self.sheet.nrows
        for i in range(row_count):
            self.print_row(i)


def __test():
    excel = ReadExecl(path)
    excel.set_current_sheet_by_name('复用')
    excel.print_sheet()
    print()
    excel.set_current_sheet_by_name('换皮')
    excel.print_sheet()


if __name__ == '__main__':
    __test()
