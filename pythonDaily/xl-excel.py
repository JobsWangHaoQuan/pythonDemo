# 在这个文件下主要是对excel内容进行修改的操作
"""
对文件进行修改的操作，我们可以在源文件上进行直接修改，当然也可以复制一个文件副本，在文件副本上进行修改
1、首先读取要操作的文件，使用open_workbook()方法
2、对读取的文件复制出一个副本，记为wb，使用copy方法
3、此时相当于已经有了一个excel，但我们还没有选择工作簿，使用get_sheet()方法选择要操作的工作簿，
接下来就可以对工作簿里面的内容进行修改
4、要是新创建一个工作簿，则类似于第一个文件里的sheet创建，使用add_sheet()方法
5、接下里的操作类似，最后保存文件
"""
import xlrd
from xlutils.copy import copy

# 打开excel
read_book = xlrd.open_workbook('电影文件.xlsx')
# 复制数据
wb = copy(read_book)
# 选择工作簿
sh = wb.get_sheet(0)

# 增加一条数据
sh.write(3, 0, '保家卫国')
sh.write(3, 1, '0.112')

# 增加一个工作簿
sh2 = wb.add_sheet('汇总数据')

count = 0
rs = read_book.sheet_by_index(0)
for i in range(1, rs.nrows):
    num = rs.cell_value(i, 1)
    count += 1

sh2.write(0, 0, '总票房')
sh2.write(0, 1, str(count)+'亿')

# 保存，一定要这一步，要不然前面操作的放在哪里呢
wb.save('电影文件02修改.xlsx')