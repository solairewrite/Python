:: 不显示命令,直接输出结果
@echo off
:: 声明变量,=前后不能有空格
set title=运行.py文件
:: cmd标题
@title %title%
:: 打印字符串
echo hellow world
:: 彩色输出,两个16进制数字分别表示背景色和前景色
color 0c
:: 打印空行
echo=
:: 打印变量, echo %title%
echo 这个cmd的标题是: %title%

:: 显示当前目录,或: echo %cd%
cd
:: 切换目录,这里可以使用变量
cd ../py
cd

set py_file=Test.py
:: 条件语句,else 不能换行,()内不能加注释
:: 当前文件夹下是否有指定文件
:: 运行.py: py -3 ReadExcel.py
if exist %py_file% (
    echo 开始运行文件: %py_file%
    py -3 %py_file% -c
) else (
    echo 文件不存在
)

:: /k: 执行完命令后不关闭cmd
cmd /k