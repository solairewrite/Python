# Author        : Zhixin.Ji
# Date          : 2019-12-10
# Description   : 替换utf-8编码的.uc文件的新建注释,无法添加中文
import os
import time


class ReplaceUCComment:
    @staticmethod
    def delete_comment(filepath: str):
        if not filepath.endswith('.uc'):
            return

        old_filepath = filepath
        new_filepath = old_filepath + '_new'

        t_old_file = open(old_filepath, 'r', encoding='utf-8')
        t_new_file = open(new_filepath, 'w+', encoding='utf_8')

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

        os.remove(old_filepath)
        os.rename(new_filepath, old_filepath)

    @staticmethod
    def get_comments(author, description):
        date = time.strftime('%Y-%m-%d', time.localtime())
        key_len = 15

        comments = list()
        comments.append('/**')
        comments.append('\n *{}: {}'.format('Author'.ljust(key_len), author))
        comments.append('\n *{}: {}'.format('Date'.ljust(key_len), date))
        comments.append('\n *{}: {}'.format('Description'.ljust(key_len), description))
        comments.append('\n */\n')

        return comments

    @staticmethod
    def add_comment(filepath: str, author, description):
        if not filepath.endswith('.uc'):
            return

        old_filepath = filepath
        new_filepath = old_filepath + '_new'

        t_old_file = open(old_filepath, 'r', encoding='utf-8')
        t_new_file = open(new_filepath, 'w+', encoding='utf_8')

        comments = ReplaceUCComment.get_comments(author, description)
        for line in comments:
            t_new_file.write(line)

        for line in t_old_file:
            t_new_file.write(line)

        t_old_file.close()
        t_new_file.close()

        os.remove(old_filepath)
        os.rename(new_filepath, old_filepath)
