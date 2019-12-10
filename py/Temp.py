# -*- coding:utf-8 -*-
from colorama import init, Fore, Back
from ReadConfig import ReadConfig

path = 'F:\\Work\\trunk\\TGame\\Config\\DefaultADGame_3.ini'

if __name__ == '__main__':
    read_config = ReadConfig(path)
    # read_config.print_config(b_print_para=True)
    t_proj_class, t_para_dict = read_config.get_class('TGAD14RocketWeap_ATSL哇')
    if t_para_dict is None:
        print('类不存在')
    else:
        ReadConfig.print_class_info(t_proj_class, t_para_dict)
