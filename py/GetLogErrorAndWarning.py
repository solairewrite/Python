# Author        : Zhixin.Ji
# Date          : 2019-12-25
# Description   : 获取Log中的error,warning
import os
import chardet

# log_path = 'F:\\Work\\trunk\\TGame\\Logs\\Launch.log'
log_path = 'C:\\Users\\jizhixin\\Desktop\\AD18-Capital_180_Main.19702.log'
output_path = 'C:\\Users\\jizhixin\\Desktop\\warning_error_log.txt'


def get_error_warning_log(in_log_path, in_output_path):
    # 获取log编码
    # with open(in_log_path, 'rb+') as t_file:
    #     t_data = t_file.read()
    #     t_encode = chardet.detect(t_data).get('encoding')
    # if t_encode is None or t_encode == '':
    #     t_encode = 'utf-8'
    t_encode = 'ansi'

    # 读取 error, warning 行
    log_info_line = ''
    error_line_list = list()
    warning_line_list = list()
    with open(in_log_path, 'r', encoding=t_encode) as t_file:
        for line in t_file:
            if 'Init: Command line:' in line:
                log_info_line = line
            if 'error' in line or 'Error' in line:
                error_line_list.append(line)
            if 'warning' in line or 'Warning' in line:
                warning_line_list.append(line)

    # 写入新 log
    with open(in_output_path, 'w+', encoding='utf-8') as t_file:
        if 'server' in log_info_line:
            t_file.write('This is Server\n')
        else:
            t_file.write('This is Client\n')
        t_file.write(log_info_line)

        t_file.write('error line count: {}\n'.format(len(error_line_list)))
        t_file.write('warning line count: {}\n'.format(len(warning_line_list)))

        t_file.write('\n\n')
        for line in error_line_list:
            t_file.write(line)

        t_file.write('\n\n')
        for line in warning_line_list:
            t_file.write(line)


if __name__ == '__main__':
    get_error_warning_log(log_path, output_path)
