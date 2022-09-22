"""
对excel表进行一些基础设置的操作
1、首先按照前面的创建一个excel表和工作簿
2、字体设置，包括调用方法看清楚，使用font和style
3、单元格设置，使用row col等设置，单元格边框使用border设置边框样式和颜色
4、背景设置，使用pattern
5、设置居中位置，使用horz和vert
这些使用都需要定义一个style来将他们与数据发生联系
最后保存
"""
import xlwt

wb = xlwt.Workbook()
sh = wb.add_sheet('数据')

# 设置字体
ft = xlwt.Font()
ft.name = '微软雅黑'
ft.colour_index = 2
ft.height = 11 * 20
ft.bold = True
ft.underline = True
ft.italic = True # 斜体

# 设置单元格高度
sh.row(3).height_mismatch = True
sh.row(3).height = 10 * 256
# 设置单元格宽度
sh.col(3).width = 20 * 256

# 设置单元格边框
border = xlwt.Borders()
border.top = 1
border.left = 1
border.right = 1
border.bottom = 1
border.bottom_colour = 1
border.top_colour = 2
border.left_colour = 3
border.right_colour = 4

# 设置背景颜色
patten = xlwt.Pattern()
patten.pattern = xlwt.Pattern.SOLID_PATTERN
patten.pattern_fore_colour = 5

alg = xlwt.Alignment()
alg.horz = 2 # 1左, 2中, 3右
alg.vert = 1 # 0上, 1中, 2下

style = xlwt.XFStyle()
style.font = ft
style2 = xlwt.XFStyle()
style2.alignment = alg
style3 = xlwt.XFStyle()
style3.borders = border
style4 = xlwt.XFStyle()
style4.pattern = patten

sh.write(0, 0, '吕布')
sh.write(1, 0, '吕布', style)
sh.write(2, 0, '貂蝉')
sh.write(3, 0, '貂蝉', style2)
sh.write(4, 1, '悟空', style3)
sh.write(5, 2, '孙尚香', style4)

wb.save('04_excel样式.xlsx')