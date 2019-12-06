# Author        : Zhixin.Ji
# Date          : 2019-12-06
# Description   : 对齐字符串,使用中英文混合


class StringAlign:
    @staticmethod
    def get_str_length(in_str):
        """获取中英文字符串的宽度,每有一个中文宽度+1"""
        str_len = len(in_str)
        for t_char in in_str:
            if u'\u4e00' <= t_char <= u'\u9fa5':  # 中文字符
                str_len += 1
        return str_len

    @staticmethod
    def get_align_width(in_str: str, in_length=10, step=10):
        """获取中英文混合字符串的对齐宽度"""
        str_len = StringAlign.get_str_length(in_str)

        align_width = in_length
        while align_width < str_len:
            align_width += step
        return align_width

    @staticmethod
    def align(in_str: str, in_length=20, step=10):
        """对齐字符"""
        t_str_len = StringAlign.get_str_length(in_str)
        t_all_length = StringAlign.get_align_width(in_str, in_length, step)
        t_space_length = t_all_length - t_str_len

        char_space = ' '
        return in_str + char_space * t_space_length

    @staticmethod
    def get_list_width(in_list):
        """获取字符串数组,最小对齐宽度"""
        t_max_len = 0
        for t_str in in_list:
            t_len = StringAlign.get_align_width(t_str)
            if t_len > t_max_len:
                t_max_len = t_len
        return t_max_len


def __test():
    a = '一123三'
    b = '一二三四五abcdefgh'
    c = '一二三四abcde'

    t_list = [a, b, c]
    t_len = StringAlign.get_list_width(t_list)
    for t_str in t_list:
        print('{}|'.format(StringAlign.align(t_str, t_len)))


# __test()
