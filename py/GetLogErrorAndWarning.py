# Author        : Zhixin.Ji
# Date          : 2019-12-25
# Description   : 获取Log中的error,warning
# 使用方法: 修改log_path,output_path即可运行
import chardet

# log_path = 'F:\\Work\\trunk\\TGame\\Logs\\Launch_2.log'
log_path = 'C:\\Users\\jizhixin\\Desktop\\e.txt'  # 初始log路径
output_path = 'C:\\Users\\jizhixin\\Desktop\\warning_error_log2.txt'  # 提取警告后的log路径

all_line_list = list()
log_info_line = ''
error_line_list = list()
warning_line_list = list()
my_log_list = list()


def set_all_line_list(in_log_path):
    """获取log所有的行"""
    # 获取log编码
    # with open(in_log_path, 'rb+') as t_file:
    #     t_data = t_file.read()
    #     t_encode = chardet.detect(t_data).get('encoding')
    # if t_encode is None or t_encode == '':
    #     t_encode = 'utf-8'
    # 强制使用编码
    t_encode = 'ansi'

    with open(in_log_path, 'r', encoding=t_encode) as t_file:
        # 将所有行存入内存中
        t_list = list()
        for line in t_file:
            t_list.append(line)

    # 格式化log,将多行的log放进一行
    # 开始代码中的log,而不是前面的信息行
    start_code_log = False
    line = ''
    global all_line_list
    for i in range(len(t_list) - 1):
        if not start_code_log:
            if '[' in t_list[i]:
                start_code_log = True
            else:
                all_line_list.append(t_list[i])
        if start_code_log:
            if '[' in t_list[i]:
                all_line_list.append(line)
                line = t_list[i]
            else:
                line += t_list[i]


def set_log_list():
    for line in all_line_list:
        if 'Init: Command line:' in line:
            global log_info_line
            log_info_line = line

        if 'error' in line or 'Error' in line:
            global error_line_list
            error_line_list.append(line)

        if 'warning' in line or 'Warning' in line:
            global warning_line_list
            warning_line_list.append(line)

        if '[mokai]' in line:
            global my_log_list
            my_log_list.append(line)


def write_error_warning_log(in_output_path):
    with open(in_output_path, 'w+', encoding='utf-8') as t_file:
        t_file.write(log_info_line)

        t_file.write('error line count: {}\n'.format(len(error_line_list)))
        t_file.write('warning line count: {}\n'.format(len(warning_line_list)))

        t_file.write('\n\n')
        for line in error_line_list:
            t_file.write(line)

        t_file.write('\n\n')
        for line in warning_line_list:
            t_file.write(line)

        t_file.write('\n\n')
        for line in my_log_list:
            t_file.write(line)


if __name__ == '__main__':
    set_all_line_list(log_path)
    print('将log存在数组中成功')
    set_log_list()
    print('获取警告成功')
    write_error_warning_log(output_path)
    print('写入新log成功')
