from string import digits


def is_sililar_string(s1: str, s2: str):
    remove_number = str.maketrans('', '', digits)
    t1 = s1.translate(remove_number)
    t2 = s2.translate(remove_number)
    return t1 == t2


if __name__ == '__main__':
    ss1 = 'abc123edf456'
    ss2 = 'aec163edf476'
    print(is_sililar_string(ss1, ss2))
