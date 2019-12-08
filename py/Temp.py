import os

if __name__ == "__main__":
    a = os.path.abspath('.')
    b = os.path.abspath('E:\\Learn\\Python\\py_tools\\bat\\py_Test.bat')
    print(a)
    print(b)
    b_to_a = os.path.relpath(a, b)
    print(b_to_a)
    print(os.path.join(b, b_to_a))
