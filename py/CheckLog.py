# Author        : Zhixin.Ji
# Date          : 2020-03-10
# Description   : 检测所有`Log,提取出无作者,无字符串描述,不规范的Log

log_path = 'C:\\Users\\jizhixin\\Desktop\\all_log.txt'  # 初始log路径
output_path = 'C:\\Users\\jizhixin\\Desktop\\out_log.txt'  # 输出的log路径

all_line_list = list()


def read_old_log(in_log_path):
    t_encode = 'utf-8'
    with open(in_log_path, 'r', encoding=t_encode) as t_file:
        # 将所有行存入内存中
        t_list = list()
        for line in t_file:
            t_list.append(line)

    # 删除正常的log
    line = ''
    global all_line_list
    for i in range(len(t_list) - 1):
        line = t_list[i]

        # 删除规则数组
        pass_condition_arr = [
            '`log(' not in line and '`Log(' not in line,
            '`log(' not in line and '`Log(' not in line,
            '//`log(' in line or '//`Log(' in line,
            '`log(\"' in line or '`Log(\"' in line,
            '`log( \"' in line or '`Log( \"' in line,
            '\");' in line,
            '//\t`log' in line,
            (len(line.split('\"')) - 1) >= 2,  # 有两个以上(")

            # 根据实际情况删除的行
            '`log(`location' in line,
            'GfxMovie' in line,
            'Src\\Engine\\' in line,
            'Src\\UTGame\\' in line,
            'Src\\TGAD' in line,
            'Src\\TGPEPGameNative' in line,
            'Src\\TGBio3Game' in line,
            'Src\\TGBPGame' in line,
            'Src\\TGBP2Game' in line,
            'Src\\TGSportGame' in line,
            'Src\\TGCCMGame' in line,
        ]

        b_should_pass = False
        for condition in pass_condition_arr:
            if condition:
                b_should_pass = True
                break
        if not b_should_pass:
            all_line_list.append(line)


def write_new_log(in_log_path):
    with open(in_log_path, 'w+', encoding='utf-8') as t_file:
        for line in all_line_list:
            t_file.write(line)


if __name__ == '__main__':
    read_old_log(log_path)
    print('读取旧log成功')
    write_new_log(output_path)
    print('写入新log成功')
