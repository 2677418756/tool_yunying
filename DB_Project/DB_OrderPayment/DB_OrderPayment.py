# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 10:31:30 2022

@author: Admin
"""

import pandas as pd
import datetime as datetime
import numpy as np
import os


class AutoExtractFiles():
    
    
    
    def __init__(self,文件夹路径,需打开表格名列表):      
        # 实例变量初始化
        self.输出字典 = {}
        self.文件夹路径 = 文件夹路径
        self.需打开表格名列表 = 需打开表格名列表       
        
    def handle(self):
        
        所有文件名列表 = os.listdir(self.文件夹路径)
        计数满足 = len(self.需打开表格名列表)
        
        for file in 所有文件名列表:
            #判断列表中元素是否存在，若存在则打开
            文件名前缀 = os.path.splitext(file)[0]
            表格类型 = 文件名前缀.split('-')[2]  #FOLA旗舰店-抖音-剩余金额表-2022-05-14.xlsx
            for need_workbook in self.需打开表格名列表:
                if 表格类型 == need_workbook:
                    #记录需打开的文件名，最后返回
                    计数满足 = 计数满足 - 1 #若所需文件全部都存在，则最后计数为0
                    temp = self.文件夹路径 + '\\' + file
                    self.输出字典[表格类型] = temp
                    
        return self.输出字典

def 函数_提取日期(去重后,字符串日期):
    近20天日期列表 = []
    for 订单创建日期 in 去重后.loc[:,f'{字符串日期}']:
        近20天日期列表.append(订单创建日期)
    return 近20天日期列表

def 函数_计算日期差值(订单创建日期,对应实际结算日期列表):
    
    存放空间 = []
    创建日期 = datetime.datetime.strptime(订单创建日期,'%Y-%m-%d')
    for 实际结算日期 in 对应实际结算日期列表 :
        
        结算日期 = datetime.datetime.strptime(实际结算日期,'%Y-%m-%d')
        
        差值 = 结算日期 - 创建日期
        
        存放空间.append(差值.days + 1)
    
    存放空间.sort()
    
    return 存放空间

def one_decimal(x_data):
    #【浮点数先转字符串，再转浮点数】让数据保留一位小数，且自动四舍五入
    x_str = '%.1f' % x_data #变成字符串来保留一位小数了
    return float(x_str)

def two_decimal(x_data):
    #【浮点数先转字符串，再转浮点数】让数据保留一位小数，且自动四舍五入
    x_str = '%.2f' % x_data #变成字符串来保留一位小数了
    return float(x_str)

def 结算金额回款表(data):
        
    # 对应的时间转换成日期，以前的实际结算日期变成现在的实际结算日期和售后申请日期，使用授信本金作为数值项
    # 第一句将时间戳转换为datatime时间组件，第二句将短日期组件提取出来，第三句转换成str方便用户查看
    
    #时间格式转换模块：从时间戳转换成时间组件
    data['订单创建日期'] = pd.to_datetime(data['订单创建时间'])
    data['订单创建日期'] = data['订单创建日期'].dt.date
    data['订单创建日期'] = data['订单创建日期'].astype(str) 
    #时间格式转换模块：从时间戳转换成时间组件
    data['实际结算日期'] = pd.to_datetime(data['实际结算时间'])
    data['实际结算日期'] = data['实际结算日期'].dt.date
    data['实际结算日期'] = data['实际结算日期'].astype(str)    
    #时间格式转换模块：从时间戳转换成时间组件
    data['售后申请日期'] = pd.to_datetime(data['售后申请时间'])
    data['售后申请日期'] = data['售后申请日期'].dt.date
    data['售后申请日期'] = data['售后申请日期'].astype(str)     
    # #时间格式转换模块：从时间戳转换成时间组件
    # data['物流日期'] = pd.to_datetime(data['物流时间'])
    # data['物流日期'] = data['物流日期'].dt.date
    # data['物流日期'] = data['物流日期'].astype(str)        
    data['系统结算日期'] = data[['实际结算日期','售后申请日期']].max(axis=1)
    data = data[~data['系统结算日期'].isin(['2000-01-01'])]
    
    data['实际结算金额'] = data['实际结算金额'].map(two_decimal)
    用于合并 = pd.DataFrame()
    
    回款总表 = pd.pivot_table(data,index=['系统结算日期'],values=['实际结算金额'],aggfunc = [np.sum])
    回款总表.columns = 回款总表.columns.droplevel(0)
    回款总表.rename(columns={'实际结算金额':'总计金额'},inplace = True)
    
    按订单创建日期回款表 = pd.pivot_table(data,index=['订单创建日期'],values=['实际结算金额'],aggfunc = [np.sum])
    按订单创建日期回款表.columns = 按订单创建日期回款表.columns.droplevel(0)
    按订单创建日期回款表.rename(columns={'实际结算金额':'总计金额'},inplace = True)
    
    提取 = data.copy()
    去重 = data.copy()    
    去重 = 去重.drop_duplicates('订单创建日期')
    横切用N列表 = 函数_提取日期(去重,'订单创建日期')
    #排序，从小到大
    横切用N列表.sort()

    for 订单创建日期 in 横切用N列表:
        #提取某一天执行操作
        横切表 = 提取[(提取['订单创建日期'] == 订单创建日期)]
        #获取同一个订单日期有几个动账日期
        获取 = 横切表.copy()
        #去除重复的动账日期
        获取 = 获取.drop_duplicates('系统结算日期')
        #将系统结算日期提取出来，返回形式为列表
        对应系统结算日期列表 = 函数_提取日期(获取,'系统结算日期')
        # print(对应系统结算日期列表)
        #再用每一个动账日期减去订单日期，得到一组整数
        数字列表 = 函数_计算日期差值(订单创建日期,对应系统结算日期列表)

        #【数据透析表】
        横切透析 = pd.pivot_table(横切表,index=['订单创建日期'],columns=['系统结算日期'],values=['实际结算金额'],aggfunc = [np.sum])
        #去除表头sum
        横切透析.columns = 横切透析.columns.droplevel(0)
        #创造字典，最后再修改字典
        明细字典2 = {f'第{i}天': 0 for i in range(1,91)} #range 区间是左闭右开
        
        #利用整数
        计数 = 0
        for 天数 in 数字列表 :
            #在字典处定位需修改的地方，修改值为透析表中已经求和好的部分
             if 天数 >= 1 :

                 求和值 = 横切透析.iloc[0,计数]
                 计数 = 计数 + 1
                 明细字典2[f'第{天数}天'] = float(求和值)


        某一天明细 = pd.Series(明细字典2)
        某一天明细.name = 订单创建日期
        #不断合并统计好的日期
        用于合并 = 用于合并.append(某一天明细)

    明细字典2 = {f'第{i}天': 0 for i in range(1, 91)}
    用于列顺序维护 = list(明细字典2)
    用于合并 = 用于合并.loc[:,用于列顺序维护]
    用于合并.index.name="订单创建日期"
    return 回款总表,用于合并,按订单创建日期回款表

def 本金回款表(data):
        
    # 对应的时间转换成日期，以前的实际结算日期变成现在的实际结算日期和售后申请日期，使用授信本金作为数值项
    # 第一句将时间戳转换为datatime时间组件，第二句将短日期组件提取出来，第三句转换成str方便用户查看

    # 只统计已回的部分，为了整体结构不变，将已退和回退对应金额变为0
    def 授信转换(status_str):
        if status_str == '已回':
            return 1
        else:
            return 0

    data['授信标志'] = data['回退状态'].map(授信转换)
    data['授信本金'] = data['授信本金']*data['授信标志']

    #时间格式转换模块：从时间戳转换成时间组件
    data['订单创建日期'] = pd.to_datetime(data['订单创建时间'])
    data['订单创建日期'] = data['订单创建日期'].dt.date
    data['订单创建日期'] = data['订单创建日期'].astype(str) 
    #时间格式转换模块：从时间戳转换成时间组件
    data['实际结算日期'] = pd.to_datetime(data['实际结算时间'])
    data['实际结算日期'] = data['实际结算日期'].dt.date
    data['实际结算日期'] = data['实际结算日期'].astype(str)    
    #时间格式转换模块：从时间戳转换成时间组件
    data['售后申请日期'] = pd.to_datetime(data['售后申请时间'])
    data['售后申请日期'] = data['售后申请日期'].dt.date
    data['售后申请日期'] = data['售后申请日期'].astype(str)     
    # #时间格式转换模块：从时间戳转换成时间组件
    # data['物流日期'] = pd.to_datetime(data['物流时间'])
    # data['物流日期'] = data['物流日期'].dt.date
    # data['物流日期'] = data['物流日期'].astype(str)        
    data['系统结算日期'] = data[['实际结算日期','售后申请日期']].max(axis=1)
    data = data[~data['系统结算日期'].isin(['2000-01-01'])]
    data['授信本金'] = data['授信本金'].map(two_decimal)   
    
    用于合并 = pd.DataFrame()
    # 将浮点数按一位小数使用
    
    
    回款总表 = pd.pivot_table(data,index=['系统结算日期'],values=['授信本金'],aggfunc = [np.sum])
    回款总表.columns = 回款总表.columns.droplevel(0)
    回款总表.rename(columns={'授信本金':'总计金额'},inplace = True)
    
    按订单创建日期回款表 = pd.pivot_table(data,index=['订单创建日期'],values=['授信本金'],aggfunc = [np.sum]) 
    按订单创建日期回款表.columns = 按订单创建日期回款表.columns.droplevel(0)
    按订单创建日期回款表.rename(columns={'授信本金':'总计金额'},inplace = True)
    
    提取 = data.copy()
    去重 = data.copy()    
    去重 = 去重.drop_duplicates('订单创建日期')
    横切用N列表 = 函数_提取日期(去重,'订单创建日期')
    #排序，从小到大
    横切用N列表.sort()

    for 订单创建日期 in 横切用N列表:
        #提取某一天执行操作
        横切表 = 提取[(提取['订单创建日期'] == 订单创建日期)]
        #获取同一个订单日期有几个动账日期
        获取 = 横切表.copy()
        #去除重复的动账日期
        获取 = 获取.drop_duplicates('系统结算日期')
        #将系统结算日期提取出来，返回形式为列表
        对应系统结算日期列表 = 函数_提取日期(获取,'系统结算日期')
        # print(对应系统结算日期列表)
        #再用每一个动账日期减去订单日期，得到一组整数
        数字列表 = 函数_计算日期差值(订单创建日期,对应系统结算日期列表)

        #【数据透析表】
        横切透析 = pd.pivot_table(横切表,index=['订单创建日期'],columns=['系统结算日期'],values=['授信本金'],aggfunc = [np.sum])
        #去除表头sum
        横切透析.columns = 横切透析.columns.droplevel(0)
        #创造字典，最后再修改字典
        明细字典1 = {f'第{i}天': 0 for i in range(1,91)} #range 区间是左闭右开
        
        #利用整数
        计数 = 0
        for 天数 in 数字列表 :
            #在字典处定位需修改的地方，修改值为透析表中已经求和好的部分
             if 天数 >= 1 :

                 求和值 = 横切透析.iloc[0,计数]
                 计数 = 计数 + 1
                 明细字典1[f'第{天数}天'] = float(求和值)


        某一天明细 = pd.Series(明细字典1)
        某一天明细.name = 订单创建日期
        #不断合并统计好的日期
        用于合并 = 用于合并.append(某一天明细)

    用于列顺序维护 = list(明细字典1)
    用于合并 = 用于合并.loc[:,用于列顺序维护]
    用于合并.index.name="订单创建日期"



    return 回款总表,用于合并,按订单创建日期回款表


from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget
from ui_DB_OrderPayment import Ui_Form

class Window(QWidget):

    def __init__(self):
        super().__init__()
        # 使用ui_Clean文件导入界面定义类
        self.ui = Ui_Form()
        self.ui.setupUi(self)  # 传入QWidget对象
        self.ui.retranslateUi(self)

        # 实例变量
        self.输入文件夹绝对路径 = ''
        self.保存文件绝对路径 = ''
        self.操作人 = ''
        self.备注 = ''
        self.temp = ''  # 用于保存打开文件的路径
        

        self.ui.InputButton.clicked.connect(self.getInputDir)
        self.ui.OutputButton.clicked.connect(self.getOutputDir)
        self.ui.RunButton.clicked.connect(self.handel)


    def getInputDir(self):
        # self.temp = QFileDialog.getExistingDirectory(self, "选择输入文件夹",'', QFileDialog.DontUseNativeDialog)  # 不使用本地对话框，可以查看文件夹内文件
        self.temp = QFileDialog.getExistingDirectory(self, "选择输入文件夹")
        if self.temp != '':
            self.输入文件夹绝对路径 = self.temp
            self.ui.InputDir.setText(self.输入文件夹绝对路径)  # 显示路径
    def getOutputDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")  # 使用本地对话框
        # self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径", '', QFileDialog.DontUseNativeDialog)  # 不使用本地对话框，可以查看文件夹内文件
        if self.temp != '':
            self.保存文件绝对路径 = self.temp
            self.ui.OutputDir.setText(self.保存文件绝对路径)  # 显示路径

    def handel(self):

        # 获取输入值
        self.操作人 = self.ui.User.text()
        self.备注 = self.ui.Remark.text()
        需打开表格名列表 = ['订单明细表']
        # 实例化对象,调用方法
        自动提取文件 = AutoExtractFiles(self.输入文件夹绝对路径,需打开表格名列表)
        需打开表格字典 = 自动提取文件.handle()
        #【在前端提前避免一些错误，如空值检测】
        # 输入值为空时
        if self.输入文件夹绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择输入路径')
            return
        if self.保存文件绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择保存路径')
            return
        if self.操作人 == '':
            QMessageBox.about(self, "报错！", '请输入操作人')
            return
        
        if self.备注 == '' :
            self.备注 = '无'
        

        文件名 = os.path.basename(需打开表格字典['订单明细表']) # loose-天猫-账单表-清洗后.xlsx
            
        文件名前缀 = os.path.splitext(文件名)[0] # loose-天猫-账单表-清洗后
        # 表格类型 = 文件名前缀.split('-')[2]
        平台类型 = 文件名前缀.split('-')[1] # loose-【天猫】-账单表-清洗后
        客户名称 = 文件名前缀.split('-')[0] # 【loose】-天猫-账单表-清洗后
        #设置两个空的datafrmae是为了抖音两个表格之间做比较时，防止无对象传入
        for k,v in 需打开表格字典.items():
            if k == '订单明细表':
                订单明细表 = pd.read_excel(v,sheet_name = '可收本金明细表',usecols=['订单创建时间','售后申请时间','实际结算时间','实际结算金额','回退状态','授信本金'])

        #如果读取的是空表，则加入一条记录进去
        if 订单明细表.empty:
            字典 = {'订单创建时间':'2001-01-01','售后申请时间':'2001-01-01','实际结算时间':'2001-01-01','实际结算金额':0,'回退状态':'已回','授信本金':0}
            temp = pd.Series(字典)
            temp.name = '2001-01-01'
            #不断合并统计好的日期
            订单明细表 = 订单明细表.append(temp)

        一表共用 = 订单明细表.copy()
        结算金额回款总表,结算金额明细表,结算金额按订单创建日期回款表 = 结算金额回款表(订单明细表)
        本金回款总表,本金明细表,本金按订单创建日期回款表 = 本金回款表(一表共用)
        
        
        输出文件名格式 = f'\\{客户名称}-{平台类型}-订单回款表-{self.操作人}-{self.备注}.xlsx'
        输出路径 = self.保存文件绝对路径 + 输出文件名格式

        #————————————————————————————————————————————————————————————————————————输出模块        
        #【writer】使用writer将dataframe放入不同的excel的sheet中
        #使用pd.ExcelWriter

        writer = pd.ExcelWriter(输出路径)
        
        结算金额明细表.to_excel(writer, sheet_name='结算金额明细表')
        # 回款透析1.to_excel(writer, sheet_name='实际结算时间透析表')
        结算金额回款总表.to_excel(writer, sheet_name='结算金额回款总表')
        # 回款透析2.to_excel(writer, sheet_name='订单创建时间透析表')
        结算金额按订单创建日期回款表.to_excel(writer, sheet_name='结算金额按订单创建日期回款表')
        
        本金明细表.to_excel(writer, sheet_name='本金明细表')
        # 回款透析1.to_excel(writer, sheet_name='实际结算时间透析表')
        本金回款总表.to_excel(writer, sheet_name='本金回款总表')
        # 回款透析2.to_excel(writer, sheet_name='订单创建时间透析表')
        本金按订单创建日期回款表.to_excel(writer, sheet_name='本金按订单创建日期回款表')
        
        writer.save()
        #不用删掉，不然文件短时间内不能编辑，只能读取
        writer.close()

    
        #成功后消息提醒
        QMessageBox.about(self, "处理结果", f'成功！\n请于“{self.保存文件绝对路径}”查看结果文件')


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()

# data = pd.read_excel(r'C:\Users\Wind_Aleady_Here\Desktop\快手-TB品牌鞋服\TB品牌鞋服-快手-订单明细表-GYH-统计揽收2022-10-12.xlsx',sheet_name='可收本金明细表')

# 结算金额回款总表,结算金额明细表,结算金额按订单创建日期回款表 = 结算金额回款表(data)
# 本金回款总表,本金明细表,本金按订单创建日期回款表 = 本金回款表(data)

# writer = pd.ExcelWriter(r'C:\Users\Wind_Aleady_Here\Desktop\快手-TB品牌鞋服\TB品牌鞋服-快手-订单回款表-GYH-统计揽收2022-10-12.xlsx')

# 结算金额明细表.to_excel(writer, sheet_name='结算金额明细表')
# # 回款透析1.to_excel(writer, sheet_name='实际结算时间透析表')
# 结算金额回款总表.to_excel(writer, sheet_name='结算金额回款总表')
# # 回款透析2.to_excel(writer, sheet_name='订单创建时间透析表')
# 结算金额按订单创建日期回款表.to_excel(writer, sheet_name='结算金额按订单创建日期回款表')

# 本金明细表.to_excel(writer, sheet_name='本金明细表')
# # 回款透析1.to_excel(writer, sheet_name='实际结算时间透析表')
# 本金回款总表.to_excel(writer, sheet_name='本金回款总表')
# # 回款透析2.to_excel(writer, sheet_name='订单创建时间透析表')
# 本金按订单创建日期回款表.to_excel(writer, sheet_name='本金按订单创建日期回款表')

# writer.save()
# #不用删掉，不然文件短时间内不能编辑，只能读取
# writer.close()
# # H.to_excel(r'C:\Users\Admin\Desktop\手动版\黄金-订单回款表-GYH.xlsx')
