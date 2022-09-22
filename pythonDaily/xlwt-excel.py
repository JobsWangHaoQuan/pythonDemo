# 该项目是从b站学习的，跟着练习的，纯粹是提高自己代码能力的
"""
第一个项目比较简单，就是新建一个excel表的操作，然后根据坐标写入数据
excel用的包是xlwt
思考一下，新建一个包需要什么步骤，
1、首先是不是要新建一个excel表啊，对应第一步wb=xlwt.Workbook（）
2、excel有了，此时需要考虑表单sheet，也就是在excel中创建一个个的sheet，因为一个excel项目可以包括好多的sheet，
用到sh=wb.add_sheet('sheet的名字')
3、现在就可以往sheet表里面写数据了，定位坐标，sh.write(行，列，值),同样的写多个数也是这样操作
4、最后一步就是保存，整个excel表的保存，不是一个sheet，wb.save(’保存的文件名‘)
"""
import xlwt

# 创建一个excel
wb = xlwt.Workbook()
# 选择工作簿
sh = wb.add_sheet('电影')
# 写入数据 到单元格 定位
sh.write(0, 0, '你好，李焕英')
sh.write(0, 1, '1')

sh.write(1, 0, '复仇者联盟')
sh.write(1, 1, '1')

sh.write(2, 0, '夏洛特烦恼')
sh.write(2, 1, '1')

# 保存excel
wb.save('电影文件.xlsx')