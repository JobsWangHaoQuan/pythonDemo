# xlrd 读取excel数据
"""
关于读取excel文件的操作就是几步，首先是读取excel文件，然后选择一个工作簿sheet，然后从工作簿中读取数据
1、选择要读取的表单open_workbook()函数
2、选择要进行读取的工作簿sheet，sheet_by_name()或者sheet_by_index()方法
3、按照想要操作的方式进行读取，按行读取，按列读取，全部读取等操作，sheet.?_value方法
"""
import xlrd
# 打开一个excel文件，用wb表示
wb = xlrd.open_workbook('电影文件.xlsx')

# excel 表中有几个sheet表单
print(wb.nsheets)
# sheet工作簿的名字
print(wb.sheet_names())

# 选择工作簿
sh1 = wb.sheet_by_index(0)
sh2 = wb.sheet_by_name('电影')

# 获取一个单元格具体的数值
print(f'第一行第二列的值：{sh1.cell_value(0,1)}')
# 获取整行/列的数值
print(f'第一行的数值：{sh1.row(0)}')
print(f'第一行的数值：{sh1.row_values(0)}')
# 获取所有的值
for i in range(sh1.nrows):
    print(f'第{i}行的数值为：{sh1.row_values(i)}')
    i += 1
