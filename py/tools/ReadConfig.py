# Author        : Zhixin.Ji
# Date          : 2019-12-10
# Description   : 读取ini配置文件
from ColorPrint import ColorPrint


class ReadConfig:
    config_dict = dict()

    def __init__(self, path):
        self.config_dict = ReadConfig.__init_config_dict(path)

    @staticmethod
    def __init_config_dict(path):
        t_dict = dict()
        t_proj = ''
        t_class = ''

        file = open(path, 'r', encoding='utf-8')
        for line in file:
            if not len(line) or line.startswith(';'):
                continue

            if line.startswith('[') and line.endswith(']\n'):
                # 屏蔽以前错误的配置
                t_str_list = line.split('.')
                if len(t_str_list) < 2:
                    t_class = ''
                else:
                    t_proj = t_str_list[0].replace('[', '')
                    t_class = t_str_list[1].split(']')[0]

            if t_class == '':
                continue

            t_proj_class = '[{}.{}]'.format(t_proj, t_class)
            if t_proj_class not in t_dict:
                t_dict[t_proj_class] = dict()

            t_pair = line.split('=')
            if len(t_pair) >= 2:
                t_para = t_pair[0]
                t_para = t_para.replace(' ', '').replace('\t', '')

                if '(' in line and ',' in line and ')' in line:
                    t_value = line.split(')')[0].split('(')[1]
                    t_value = '({})'.format(t_value)
                else:
                    t_value = t_pair[1]
                if ';' in t_value:
                    t_value = t_value.split(';')[0]
                t_value = t_value.replace('\n', '').replace(' ', '').replace('\t', '')

                if t_para not in t_dict[t_proj_class]:
                    t_dict[t_proj_class][t_para] = t_value

        return t_dict

    def get_class(self, class_name):
        for t_proj_class in self.config_dict.keys():
            if '.{}]'.format(class_name) in t_proj_class:
                return t_proj_class, self.config_dict[t_proj_class]
        return None, None

    @staticmethod
    def print_class_info(proj_class, para_dict: dict, b_print_class=True, b_print_para=True):
        """打印类配置信息,并返回参数个数"""
        t_para_count = len(para_dict.keys())
        if b_print_class:
            ColorPrint.color_print('{} \t参数数量: {}'.format(proj_class, t_para_count))

        if not b_print_para:
            return t_para_count

        for t_para in para_dict.keys():
            t_value = para_dict[t_para]
            t_str = '{} = {}'.format(t_para, t_value)
            print(t_str)
        print()
        return t_para_count

    def print_config(self, b_print_class=True, b_print_para=True):
        t_para_count = 0
        for t_proj_class in self.config_dict.keys():
            t_para_count += ReadConfig.print_class_info(
                t_proj_class, self.config_dict[t_proj_class],
                b_print_class, b_print_para
            )

        t_class_count = len(self.config_dict.keys())
        ColorPrint.color_print('总共有{}个类,{}个参数'.format(t_class_count, t_para_count))
