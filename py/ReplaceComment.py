"""
Author      : Zhixin.Ji
Date        : 2019-12-03
Description : 替换utf-8编码的.uc文件的新建注释
问题         : 虽然写如文件的编码是utf-8,但无法填写中文描述
"""
import time
import os

path = 'F:\\Work\\trunk\\Development\\Src\\TGAD19Game\\Classes'

b_delete_old_comment = True
b_add_new_comment = True

author = 'Zhixin.ji'
date = time.strftime('%Y-%m-%d', time.localtime())
description = 'no description'
key_display_length = 15

comments = list()
comments.append('/**')
comments.append('\n *Author'.ljust(key_display_length) + ': ' + author)  # ljust(): 左对齐,并且用空格补全指定长度
comments.append('\n *Date'.ljust(key_display_length) + ': ' + date)
comments.append('\n *Description'.ljust(key_display_length) + ': ' + description)
comments.append('\n */\n')


def delete_old_comment(inpath):
    print('删除旧的新建注释,文件数量: ', len(os.listdir(inpath)))
    for t_old_filename in os.listdir(inpath):

        # 仅删除.uc文件的注释
        if not t_old_filename.endswith('.uc'):
            continue

        t_old_fullname = os.path.join(inpath, t_old_filename)
        t_new_fullname = t_old_fullname + '_new'

        t_old_file = open(t_old_fullname, 'r', encoding='utf-8')
        t_new_file = open(t_new_fullname, 'w+', encoding='utf_8')

        t_comment_finish = False
        for line in t_old_file:
            if not t_comment_finish:
                if 'class' in line and 'extends' in line:
                    t_comment_finish = True
                    t_new_file.write(line)
            else:
                t_new_file.write(line)

        t_old_file.close()
        t_new_file.close()

        os.remove(t_old_fullname)
        os.rename(t_new_fullname, t_old_fullname)


def add_new_comment(inpath):
    print('添加新的新建注释,文件数量: ', len(os.listdir(inpath)))
    for t_old_filename in os.listdir(inpath):

        t_old_fullname = os.path.join(inpath, t_old_filename)
        t_new_fullname = t_old_fullname + '_new'

        t_old_file = open(t_old_fullname, 'r', encoding='utf-8')
        t_new_file = open(t_new_fullname, 'w+', encoding='utf_8')

        # 数据只能写到文件末尾
        for line in comments:
            t_new_file.write(line)

        for line in t_old_file:
            t_new_file.write(line)

        t_old_file.close()
        t_new_file.close()

        os.remove(t_old_fullname)
        os.rename(t_new_fullname, t_old_fullname)


if __name__ == '__main__':
    if b_delete_old_comment:
        delete_old_comment(path)
    if b_add_new_comment:
        add_new_comment(path)
