# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 13:45:05 2022

@author: Admin
"""

import pandas as pd
import os
import os.path
import numpy as np
import datetime

def 日期连续性(dataframe,列名):
    
    #需要处理的列中元素类型为什么？
    日期连续性 = []
    最大日期字符串 = dataframe[f'{列名}'].max()
    最小日期字符串 = dataframe[f'{列名}'].min()
    最大日期 = datetime.datetime.strptime(最大日期字符串,'%Y-%m-%d').date() 
    最小日期 = datetime.datetime.strptime(最小日期字符串,'%Y-%m-%d').date()

    行进日期 = 最小日期
    while 行进日期 <= 最大日期:
        日期连续性.append(str(行进日期))
        行进日期 = 行进日期 + datetime.timedelta(days=+1)
    # dataframe.set_index([f'{列名}'],inplace=True)
    
    #初始化额外空间，然后上下合并到透析表中
    temp_dataframe = pd.DataFrame(data = 日期连续性,dtype = str)
    temp_dataframe.rename({0:f'{列名}'},axis=1,inplace=True) #单列表转换成dataframe，其列索引值为0，所以重命名0即可

    final_dataframe = pd.concat([dataframe,temp_dataframe]).reset_index(drop=True)
    # final_dataframe.index.name = f'{列名}'
    return final_dataframe

def 时长范围内判断(time_int) :
    if time_int == 0:
        return 1
    else:
        return 0
def 时长超过范围判断(time_int):
    if time_int >= 0:
        return 1
    else:
        return 0  

def 中间过程判断(V,性质,时长计算,精确天数):
    
    #数据类型转换成int型才能进行算术运算
    精确天数 = int(精确天数)
    # #【格式】去掉订单创建日期中的00：00：00
    # V['订单创建日期'] = V['订单创建日期'].dt.date
    # V['订单创建日期'] = V['订单创建日期'].astype(str)
    #提取订单创建日期中的最大值

    try:
        #偷懒的让各个平台不同字段兼容一下的try
        #如果本身是字符串则直接提取max值
        最大日期字符串 = V['订单创建日期'].max()
        最大日期 = datetime.datetime.strptime(最大日期字符串,'%Y-%m-%d').date() 
    except(TypeError):
        V['订单创建日期'] = V['订单创建日期'].dt.date
        V['订单创建日期'] = V['订单创建日期'].astype(str)
        最大日期字符串 = V['订单创建日期'].max()
        最大日期 = datetime.datetime.strptime(最大日期字符串,'%Y-%m-%d').date() 
    最大日期 = 最大日期 + datetime.timedelta(days=+1)
    #初始化数据
    cols = []
    补充格 = [f'{最大日期}']
    #只提取Timedelta时间段的days部分
    V[f'{性质}时长'] = V[f'{性质}时长'].astype('timedelta64[D]').astype(int) 
    
    #循环判断时长是否是当天的，判断完一次，时长天数-1
    i = 1 
    temp = 0
    while i <= 精确天数:
                
        V[f'是否{temp+24}内{性质}'] = V[f'{时长计算}'].map(时长范围内判断) #生成新的一列并进行对应判断
        V[f'{性质}时长'] = V[f'{性质}时长'].map(lambda x : x - 1) #天数 - 1操作，方便循环判断
        V[f'{性质}GMV（{temp}~{temp+24}h）'] = V[f'是否{temp+24}内{性质}'] * V['订单应付金额']
        
        #拓展可移动的格子，及对应索引名称
        cols.append(f'{性质}GMV（{temp}~{temp+24}h）')
        补充格.append(f'补充格{i}')
        
        #维护循环的参数
        temp = i*24
        i = i + 1
    
    #生成最后一列并进行对应判断
    V[f'是否超过{temp}{性质}'] = V[f'{时长计算}'].map(时长超过范围判断) 
    V[f'{性质}GMV大于（{temp}h）'] = V[f'是否超过{temp}{性质}'] * V['订单应付金额']
    cols.append(f'{性质}GMV大于（{temp}h）')
       
    #数据透析
    透视表 = pd.pivot_table(V,index=['订单创建日期'],values = cols,aggfunc = [np.sum])
    透视表.columns = 透视表.columns.droplevel(0)
    透视表[f'{性质}总计'] = 透视表.apply(lambda x: x.sum(), axis=1) # 按行求和，添加为新列
    cols.insert(0,f'{性质}总计')
    
    #改变列的序列
    透视表 = 透视表.loc[:,cols]
    
    #初始化额外空间，然后上下合并到透析表中
    临时空间 = pd.DataFrame(columns = cols,index = 补充格,dtype = float)  
    金额速度表 = pd.concat([透视表,临时空间])
    金额速度表.index.name = '发货自然日'
    
    j = 1
    temp = 0   
    while j <= 精确天数:
            
        #循环向下移动格子
        金额速度表[f'{性质}GMV（{temp}~{temp+24}h）'] = 金额速度表[f'{性质}GMV（{temp}~{temp+24}h）'].shift(j)
        
        #维护循环的参数
        temp = j*24
        j = j + 1
        
    #向下移动最后一列   
    金额速度表[f'{性质}GMV大于（{temp}h）'] = 金额速度表[f'{性质}GMV大于（{temp}h）'].shift(j)
        
    return 金额速度表,透视表


def 抖音揽收速度表(订单表,运单表,精确天数):

    # 数据清洗【去除退货退款的】
    订单表 = 订单表[~(订单表.售后状态.isin(['待买家退货'])|订单表.售后状态.isin(['待商家处理'])|订单表.售后状态.isin(['待商家收货'])|订单表.售后状态.isin(['同意退款，退款成功']))]

    
    #读取后分两个表执行操作
    #——————————————————————————————————————————————订单编号与提交时间合一
    订单与时间合一 = 订单表.copy()
    订单与时间合一.drop(['订单应付金额'],axis= 1,inplace=True)
    订单与时间合一 = 订单与时间合一.drop_duplicates('订单编号')
    #——————————————————————————————————————————————订单编号与提交时间合一
     
    #——————————————————————————————————————————————同一订单编号的金额求和
    #【分组求和】将订单表内同一订单编号的不同商品对应订单金额求和
    订单金额求和 = 订单表.copy()
    订单金额求和.drop(['订单创建时间'],axis= 1,inplace=True)
    订单金额求和.drop(['订单创建日期'],axis= 1,inplace=True)
    temp = 订单金额求和.groupby(['订单编号'])['订单应付金额'].sum()
    #——————————————————————————————————————————————同一订单编号的金额求和
    
    运单表['订单编号'] = 运单表['订单编号'].astype(np.int64)
    
    #【Vlookup】本次V操作主要以运单表为主，使用right
    V = pd.merge(订单与时间合一,运单表,left_on ='订单编号',right_on ='订单编号',how ='inner') 
    
    #【重点】此处操作将同一订单编号但不同运单号的订单只保留一项
    V.drop_duplicates('订单编号')
    V = pd.merge(V,temp,left_on ='订单编号',right_on ='订单编号',how ='left') 

    #【0614加入数据转换】————————————————————————
    V['订单创建日期'] = V['订单创建日期'].dt.date
    V['订单创建日期'] = V['订单创建日期'].astype(str)
    
    V2 = 日期连续性(V,'订单创建日期') #使得日期连续
    #【0614加入数据转换】————————————————————————
    
    #抖音的时间格式本来就是字符串格式，现转换成时间戳
    V2['订单创建时间'] = pd.to_datetime(V2['订单创建时间'])
    V2['揽件时间']  = pd.to_datetime(V2['揽件时间'])
    
    V2['揽收时长'] = (V2['揽件时间'] - V2['订单创建时间'])  

    性质 = '揽收'
    时长计算 = '揽收时长' 
    
    #【0614加入数据转换】————————————————————————
    V2[f'{性质}时长'].fillna(pd.Timedelta(seconds=0),inplace=True)
    #【0614加入数据转换】————————————————————————
    
    金额速度表,金额时间表 = 中间过程判断(V2,性质,时长计算,精确天数)
    
    return 金额速度表,金额时间表

    
def 快手揽收速度表(订单表,运单表,精确天数):
  
    # 数据清洗【去除退货退款的】
    订单表 = 订单表[~(订单表.退货退款.isin(['退款成功']))]
             
    订单表['订单编号'] = 订单表['订单编号'].astype(str)
    运单表['订单编号'] = 运单表['订单编号'].astype(str)
       
    # #本次V操作主要以运单表为主，所以集合变小
    V = pd.merge(订单表,运单表,left_on ='订单编号',right_on ='订单编号',how ='inner') 
    
    #【1101加入数据转换】————————————————————————
    # V['订单创建日期'] = V['订单创建日期'].dt.date
    V['订单创建日期'] = V['订单创建日期'].astype(str)
    
    V2 = 日期连续性(V,'订单创建日期') #使得日期连续
    #【1101加入数据转换】————————————————————————
    
    #快手的时间格式本来就是字符串格式，需要转换成datetime类型
    V2['订单创建时间'] = pd.to_datetime(V2['订单创建时间'])
    V2['发货时间']  = pd.to_datetime(V2['发货时间'])
    # V['订单创建时间'] = datetime.datetime.strptime(V['订单创建时间'],'%Y-%m-%d %H:%M:%S')
    # V['发货时间'] = datetime.datetime.strptime(V['发货时间'],'%Y-%m-%d %H:%M:%S')
    #通过减法获取发货时长
    V2['发货时长'] = (V2['发货时间'] - V2['订单创建时间']) 
    
    #————————————————————————————————————————————————以下是运单表V订单表相关操作
    时长计算 = '发货时长'
    性质 = '发货'
    
    #【1101加入数据转换】————————————————————————
    V2[f'{性质}时长'].fillna(pd.Timedelta(seconds=0),inplace=True)
    #【1101加入数据转换】————————————————————————    

    金额速度表,金额时间表 = 中间过程判断(V2,性质,时长计算,精确天数)
    
    
    return 金额速度表,金额时间表
    
    
def 拼多多揽收速度表(订单表,运单表,精确天数):

    # 数据清洗【去除退货退款的】共有两个：退款成功和售后处理中，暂时不加售后处理中
    订单表 = 订单表[~(订单表.售后状态.isin(['退款成功']))]
    
    # 精确天数 = int(精确天数)         
    订单表['订单编号'] = 订单表['订单编号'].astype(str)
    运单表['订单编号'] = 运单表['订单编号'].astype(str)
       
    # #本次V操作主要以运单表为主，所以集合变小
    V = pd.merge(订单表,运单表,left_on ='订单编号',right_on ='订单编号',how ='inner') 
    
    
    #快手的时间格式本来就是字符串格式，需要转换成datetime类型
    V['订单创建时间'] = pd.to_datetime(V['订单创建时间'])
    V['发货时间']  = pd.to_datetime(V['发货时间'])

    #通过减法获取揽收时长
    V['发货时长'] = (V['发货时间'] - V['订单创建时间'])

    
    #将相关字段传入函数，程序才能自动识别表格内需要的字段
    时长计算 = '发货时长'
    性质 = '发货'
    
    金额速度表,金额时间表 = 中间过程判断(V,性质,时长计算,精确天数)
       
    return 金额速度表,金额时间表


def 天猫揽收速度表(订单表,精确天数):

    def 是否退货退款(退货退款金额):
        if 退货退款金额 !='没有申请退款' or  退货退款金额 !='退款关闭':
            return 1
        else :
            return 0

    # 数据清洗【去除退货退款的】
    #将没退的保留下来
    订单表['是否退货退款'] = 订单表['售后状态'].map(是否退货退款)
    订单表 = 订单表[(订单表.是否退货退款.isin([0]))]



    #快手的时间格式本来就是字符串格式，需要转换成datetime类型
    订单表['订单创建时间'] = pd.to_datetime(订单表['订单创建时间'])
    订单表['发货时间']  = pd.to_datetime(订单表['发货时间'])
    # 订单表['订单创建时间'] = datetime.datetime.strptime(订单表['订单创建时间'],'%Y-%m-%d %H:%M:%S')
    # 订单表['发货时间'] = datetime.datetime.strptime(订单表['发货时间'],'%Y-%m-%d %H:%M:%S')
    
    #先删除发货时间不存在的单元格
    订单表.dropna(axis = 0 ,how = 'any',subset=['发货时间'],inplace=True)
    
    #通过减法获取揽收时长
    订单表['发货时长'] = (订单表['发货时间'] - 订单表['订单创建时间'])
    
    
    #————————————————————————————————————————————————以下是运单表订单表订单表相关操作
    时长计算 = '发货时长'
    性质 = '发货'
       
    金额速度表,金额时间表 = 中间过程判断(订单表,性质,时长计算,精确天数)
    
    
    return 金额速度表,金额时间表



#——————————————————————————————————————————————————————主程序开始————————————————————————————————————————————————#
#输入表格命名规则：客户名称-平台名称-表格名称-操作人-精确天数
#输出表格命名规则：客户名称-订单金额表-操作人-精确天数
#自动获取：客户名称-0、精确天数-4、
#用户输入：订单表路径、运单表路径、操作人、精确天数


#——————————————————————————————————————————————————————————————————————————————用户输入模块
from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget
from ui_ReceiveSpeed import Ui_Form

class Window(QWidget):
    def __init__(self):
        super().__init__()
        # 使用ui_Clean文件导入界面定义类
        self.ui = Ui_Form()
        self.ui.setupUi(self)  # 传入QWidget对象
        self.ui.retranslateUi(self)

        # 实例变量
        self.订单表文件绝对路径 = ''
        self.运单表文件绝对路径 = ''
        self.保存文件绝对路径 = ''
        self.操作人 = ''
        self.精确天数 = 10 #默认为10
        self.temp = ''  # 用于保存打开文件的路径

        self.ui.InputButton_1.clicked.connect(self.getOrderForm)
        self.ui.InputButton_2.clicked.connect(self.getWaybillForm)
        self.ui.OutputButton.clicked.connect(self.getOutputDir)
        self.ui.RunButton.clicked.connect(self.handel)

    def getOrderForm(self):
        self.temp, _ = QFileDialog.getOpenFileName(self, "选择订单表", '', "Forms(*.xlsx *.csv)")
        if self.temp != '':
            self.订单表文件绝对路径 = self.temp
            self.ui.InputFile_1.setText(self.订单表文件绝对路径)  # 显示路径

    def getWaybillForm(self):
        self.temp, _ = QFileDialog.getOpenFileName(self, "选择运单表", '', "Forms(*.xlsx *.csv)")
        if self.temp != '':
            self.运单表文件绝对路径 = self.temp
            self.ui.InputFile_2.setText(self.运单表文件绝对路径)

    def getOutputDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")  # 不使用本地对话框，可以查看文件夹内文件
        # self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")
        if self.temp != '':
            self.保存文件绝对路径 = self.temp
            self.ui.OutputDir.setText(self.保存文件绝对路径)

    def handel(self):

        # 获取输入值
        self.操作人 = self.ui.User.text()
        self.精确天数 = self.ui.Remark.text()  # 精确天数默认为5
        # 输入值为空时
        if self.订单表文件绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择订单表')
            return
        # if self.运单表文件绝对路径 == '':
        #     QMessageBox.about(self, "报错！", '请选择运单表')
        #     return
        if self.保存文件绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择保存路径')
            return
        if self.操作人 == '':
            QMessageBox.about(self, "报错！", '请输入操作人')
            return


        #文件名提取模块
        订单表文件名 = os.path.split(self.订单表文件绝对路径)[1] #客户名称-平台名称-表格名称-操作人-精确天数.xlsx
        # 订单表文件纯路径 = os.path.split(self.订单表文件绝对路径)[0] #C:\Users\Admin\Desktop\海月社中台数据
      
        if self.精确天数 == '':
            self.精确天数 = '10'

        #——————————————————————————————————————————————————————————————————打开与保存模块
        平台类型 = 订单表文件名.split('-')[1]
        客户名称 = 订单表文件名.split('-')[0]
        输出文件名格式 = f'\\{客户名称}-{平台类型}-揽收速度表-{self.操作人}-{self.精确天数}天内.xlsx'
        输出路径 = self.保存文件绝对路径 + 输出文件名格式


        if 平台类型 == '快手' :
            订单表 = pd.read_excel(self.订单表文件绝对路径)
            运单表 = pd.read_excel(self.运单表文件绝对路径)
            揽收速度表,揽收时间表 = 快手揽收速度表(订单表,运单表,self.精确天数)
            
        elif 平台类型 == '抖音' :
            订单表 = pd.read_excel(self.订单表文件绝对路径)
            运单表 = pd.read_excel(self.运单表文件绝对路径)
            揽收速度表,揽收时间表 = 抖音揽收速度表(订单表,运单表,self.精确天数)
            
        elif 平台类型 == '拼多多' :
            订单表 = pd.read_excel(self.订单表文件绝对路径)
            运单表 = pd.read_excel(self.运单表文件绝对路径)
            揽收速度表,揽收时间表 = 拼多多揽收速度表(订单表,运单表,self.精确天数)
            
        elif 平台类型 == '天猫' :
            订单表 = pd.read_excel(self.订单表文件绝对路径)
            揽收速度表,揽收时间表 = 天猫揽收速度表(订单表,self.精确天数)
            
        elif 平台类型 == '淘宝' :
            订单表 = pd.read_excel(self.订单表文件绝对路径)
            揽收速度表,揽收时间表 = 天猫揽收速度表(订单表,self.精确天数)
        else :
            print('命名格式错误：平台类型')

        #——————————————————————————————————————————————————————————————————打开与保存模块

        # #中间过程表核验【以后可以拓展选择是否核验中间过程】
        #使用pd.ExcelWriter
        writer = pd.ExcelWriter(输出路径)
        揽收速度表.to_excel(writer, sheet_name='揽收速度金额表')
        揽收时间表.to_excel(writer, sheet_name='揽收时间金额表')
        writer.save()
        #不用删掉，不然文件短时间内不能编辑，只能读取
        writer.close()


        QMessageBox.about(self, "处理结果", f'成功！\n请于“{self.保存文件绝对路径}”查看结果文件')

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()

