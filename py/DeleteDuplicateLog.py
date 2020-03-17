# Author        : Zhixin.Ji
# Date          : 2020-01-04
# Description   : 删除重复的log行
# 使用方法: 先运行GetLogErrorAndWarning.py,获取提取警告后的log,路径设为log_path
# 然后修改output_path即可运行
# 自定义写入的内容: 修改函数write_error_warning_log()
# 添加: or XXX in line,即可过滤掉含有XXX的行
from string import digits

log_path = 'C:\\Users\\jizhixin\\Desktop\\warning_error_log.txt'  # 初始log路径
output_path = 'C:\\Users\\jizhixin\\Desktop\\formated_log.txt'  # 提取警告后的log路径

all_line_list = list()
no_duplicate_line_list = list()
log_info_line = ''
error_line_list = list()
warning_line_list = list()
my_log_list = list()


def no_number_str(in_str: str):
    remove_number = str.maketrans('', '', digits)
    t = in_str.translate(remove_number)
    return t


def is_sililar_string(s1: str, s2: str):
    remove_number = str.maketrans('', '', digits)
    t1 = s1.translate(remove_number)
    t2 = s2.translate(remove_number)
    return t1 == t2


def set_all_line_list(in_log_path):
    """获取log所有的行"""
    t_encode = 'utf-8'

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


def set_no_duplicate_line_list():
    t_list = list()
    global no_duplicate_line_list
    for line in all_line_list:
        t_no_number_line = no_number_str(line)
        if t_no_number_line not in t_list:
            t_list.append(t_no_number_line)
            no_duplicate_line_list.append(line)


def set_log_list():
    for line in no_duplicate_line_list:
        if 'Init: Command line:' in line:
            global log_info_line
            log_info_line = line

        if 'error' in line or 'Error' in line:
            global error_line_list
            error_line_list.append(line)

        if 'warning' in line or 'Warning' in line:
            global warning_line_list
            warning_line_list.append(line)

        if '[mokai]' in line or 'jzx' in line:
            global my_log_list
            my_log_list.append(line)


def write_error_warning_log(in_output_path):
    with open(in_output_path, 'w+', encoding='utf-8') as t_file:
        for line in error_line_list:
            # Temp
            if 'Log: [shadowguo]error PackageName' in line:
                continue
            t_file.write(line)

        t_file.write('\n\n')
        for line in warning_line_list:
            # Temp,删除材质警告
            if ('Material' in line
                    or 'Texture' in line
                    or 'have duplicate NetIndex' in line
                    or 'Particle' in line
                    or 'GfxWarning' in line):
                continue
            t_file.write(line)
            t_file.write('\n')

        t_file.write('\n\n')
        for line in my_log_list:
            t_file.write(line)


if __name__ == '__main__':
    set_all_line_list(log_path)
    print('将log存在数组中成功')
    set_no_duplicate_line_list()
    print('删除重复警告成功')
    set_log_list()
    print('获取警告成功')
    write_error_warning_log(output_path)
    print('写入新log成功')
