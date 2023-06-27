# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 15:42:36 2022

@author: Admin
"""

import pandas as pd
import os
import numpy as np
import datetime

#【笔记】小店自卖的订单不会出现在联盟表，还有部分订单编号不会出现在团长表，所以合并表格时不能用inner

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
        V[f'{性质}成本（{temp}~{temp+24}h）'] = V[f'是否{temp+24}内{性质}'] * V['平台扣除费用']
        
        #拓展可移动的格子，及对应索引名称
        cols.append(f'{性质}成本（{temp}~{temp+24}h）')
        补充格.append(f'补充格{i}')
        
        #维护循环的参数
        temp = i*24
        i = i + 1
    
    #生成最后一列并进行对应判断
    V[f'是否超过{temp}{性质}'] = V[f'{时长计算}'].map(时长超过范围判断) 
    V[f'{性质}成本大于（{temp}h）'] = V[f'是否超过{temp}{性质}'] * V['平台扣除费用']
    cols.append(f'{性质}成本大于（{temp}h）')
       
    #数据透析
    透视表 = pd.pivot_table(V,index=['订单创建日期'],values = cols,aggfunc = [np.sum])
    透视表.columns = 透视表.columns.droplevel(0)
    透视表[f'{性质}总计'] = 透视表.apply(lambda x: x.sum(), axis=1) # 按行求和，添加为新列
    cols.insert(0,f'{性质}总计')
    
    #改变列的序列
    透视表 = 透视表.loc[:,cols]
    揽收时间表 = 透视表
    
    #初始化额外空间，然后上下合并到透析表中
    临时空间 = pd.DataFrame(columns = cols,index = 补充格,dtype = float)  
    金额速度表 = pd.concat([透视表,临时空间])
    金额速度表.index.name = '发货自然日'
    
    j = 1
    temp = 0   
    while j <= 精确天数:
            
        #循环向下移动格子
        金额速度表[f'{性质}成本（{temp}~{temp+24}h）'] = 金额速度表[f'{性质}成本（{temp}~{temp+24}h）'].shift(j)
        
        #维护循环的参数
        temp = j*24
        j = j + 1
        
    #向下移动最后一列   
    金额速度表[f'{性质}成本大于（{temp}h）'] = 金额速度表[f'{性质}成本大于（{temp}h）'].shift(j)
        
    return 金额速度表,揽收时间表

def 抖音揽收成本表(订单表,运单表,联盟表,团长表,精确天数):
    
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
    订单分组求和 = 订单金额求和.groupby(['订单编号'])['订单应付金额'].sum()
    #——————————————————————————————————————————————同一订单编号的金额求和
    
    # #——————————————————————————————————————————————同一订单编号的成本金额求和
    # #【分组求和】将订单表内同一订单编号的不同商品对应订单金额求和
    # 成本金额求和 = pd.merge(订单表,成本表,on ='商家编码',how ='left') 
    # 成本金额求和.drop(['订单创建时间'],axis= 1,inplace=True)
    # 成本金额求和.drop(['订单创建日期'],axis= 1,inplace=True)
    # 成本分组求和 = 成本金额求和.groupby(['订单编号'])['成本价'].sum()
    # #——————————————————————————————————————————————同一订单编号的成本金额求和
    
    # 运单表['订单编号'] = 运单表['订单编号'].astype(np.int64)
    # 联盟表['订单编号'] = 联盟表['订单编号'].astype(np.int64)
    # 团长表['订单编号'] = 团长表['订单编号'].astype(np.int64)
    联盟表['商品单号'] = 联盟表['商品单号'].astype(np.int64)
    团长表['商品单号'] = 团长表['商品单号'].astype(np.int64)
    #【Vlookup】本次V操作主要以运单表为主，使用right
    V1 = pd.merge(订单与时间合一,运单表,left_on ='订单编号',right_on ='订单编号',how ='inner') 
    #【重点】此处操作将同一订单编号但不同运单号的订单只保留一项
    V1.drop_duplicates('订单编号')
    # V1.to_excel(r'C:\Users\Admin\Desktop\FOLA揽收余额测算文件包\FOLA旗舰店-中间过程.xlsx')
    V2 = pd.merge(V1,联盟表,left_on ='订单编号',right_on ='商品单号',how ='left') 
    V3 = pd.merge(V2,团长表,left_on ='订单编号',right_on ='商品单号',how ='left') 

    
    V5 = pd.merge(V3,订单分组求和,left_on ='订单编号',right_on ='订单编号',how ='left') #为了拥有订单应付金额列
    # V5 = pd.merge(V4,成本分组求和,left_on ='订单编号',right_on ='订单编号',how ='left') #为了拥有订单对应成本金额列
    V5['平台扣点'] = V5['订单应付金额'].map(lambda x : round(x*0.05,2))
    V5['联盟佣金'].fillna(value=0,axis=0,inplace=True)
    V5['团长佣金'].fillna(value=0,axis=0,inplace=True)
    V5['平台扣除费用'] = V5['联盟佣金'] + V5['团长佣金'] + V5['平台扣点']
    # #方便人为检查
    # V['订单编号'] = V['订单编号'].astype(str)
    
    #抖音的时间格式本来就是字符串格式，现转换成时间戳
    V5['订单创建时间'] = pd.to_datetime(V5['订单创建时间'])
    V5['揽件时间']  = pd.to_datetime(V5['揽件时间'])
    
    V5['揽收时长'] = (V5['揽件时间'] - V5['订单创建时间'])  
    
    #【0614加入数据转换】————————————————————————
    V5['订单创建日期'] = V5['订单创建日期'].dt.date
    V5['订单创建日期'] = V5['订单创建日期'].astype(str)
    
    V6 = 日期连续性(V5,'订单创建日期') #使得日期连续
    #【0614加入数据转换】————————————————————————
    
    性质 = '揽收'
    时长计算 = '揽收时长' 
    #【0614加入数据转换】————————————————————————
    V6[f'{性质}时长'].fillna(pd.Timedelta(seconds=0),inplace=True) #中间过程
    #【0614加入数据转换】————————————————————————
    
    金额速度表,揽收时间表 = 中间过程判断(V6,性质,时长计算,精确天数)
    
    return 金额速度表,揽收时间表 #中间过程也传过去方便对比

def 快手揽收成本表(订单表,运单表,精确天数):
    
    # 数据清洗【去除退货退款的】
    订单表 = 订单表[~(订单表.退货退款.isin(['退款成功']))]
    
    订单表['订单编号'] = 订单表['订单编号'].astype(str)
    运单表['订单编号'] = 运单表['订单编号'].astype(str)
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
    订单分组求和 = 订单金额求和.groupby(['订单编号'])['订单应付金额'].sum()
    #——————————————————————————————————————————————同一订单编号的金额求和
    


    #【Vlookup】本次V操作主要以运单表为主，使用right
    V1 = pd.merge(订单与时间合一,运单表,left_on ='订单编号',right_on ='订单编号',how ='inner') 
    # V1.to_excel(r'C:\Users\Admin\Desktop\FOLA揽收余额测算文件包\FOLA旗舰店-中间过程.xlsx')

    #【重点】此处操作将同一订单编号但不同运单号的订单只保留一项
    V1.drop_duplicates('订单编号')
    
    V5 = pd.merge(V1,订单分组求和,left_on ='订单编号',right_on ='订单编号',how ='left') #为了拥有订单应付金额列
    # V5 = pd.merge(V4,成本分组求和,left_on ='订单编号',right_on ='订单编号',how ='left') #为了拥有订单对应成本金额列
    # V5['平台扣点'] = V5['订单应付金额'].map(lambda x : round(x*0.05,2))
    V5['预估推广佣金'].fillna(value=0,axis=0,inplace=True)
    # V5['平台扣除费用'] = V5['预估推广佣金'] + V5['平台扣点']
    V5['平台扣除费用'] = V5['预估推广佣金'] #期望平台扣除费用在授信表中计算，因为不同品类的平台扣除点数不一样
    # #方便人为检查
    # V['订单编号'] = V['订单编号'].astype(str)
    
    #抖音的时间格式本来就是字符串格式，现转换成时间戳
    V5['订单创建日期'] = pd.to_datetime(V5['订单创建日期'])
    V5['订单创建时间'] = pd.to_datetime(V5['订单创建时间'])
    V5['发货时间']  = pd.to_datetime(V5['发货时间'])
    
    V5['发货时长'] = (V5['发货时间'] - V5['订单创建时间'])  
    
    #【0614加入数据转换】————————————————————————
    V5['订单创建日期'] = V5['订单创建日期'].dt.date
    V5['订单创建日期'] = V5['订单创建日期'].astype(str)
    
    V6 = 日期连续性(V5,'订单创建日期') #使得日期连续
    #【0614加入数据转换】————————————————————————
    
    性质 = '发货'
    时长计算 = '发货时长' 
    #【0614加入数据转换】————————————————————————
    V6[f'{性质}时长'].fillna(pd.Timedelta(seconds=0),inplace=True) #中间过程
    #【0614加入数据转换】————————————————————————
    
    金额速度表,揽收时间表 = 中间过程判断(V6,性质,时长计算,精确天数)
    
    return 金额速度表,揽收时间表 #中间过程也传过去方便对比

def 天猫揽收成本表(订单表,淘客表,精确天数):
    
    # 数据清洗【去除退货退款的】
    def 是否退货退款(退货退款金额):
        if 退货退款金额 != '没有申请退款' or 退货退款金额 != '退款关闭':
            return 1
        else:
            return 0

    # 数据清洗【去除退货退款的】
    # 将没退的保留下来
    订单表['是否退货退款'] = 订单表['售后状态'].map(是否退货退款)
    订单表 = 订单表[(订单表.是否退货退款.isin([0]))]


    #天猫揽收成本表主要以发货时间为主,排除掉没有发货时间的
    订单表.dropna(axis = 0 ,how = 'any',subset=['发货时间'],inplace=True)
    
    #样式优化
    订单表['订单创建日期'] = 订单表['订单创建日期'].dt.date
    订单表['订单创建日期'] = 订单表['订单创建日期'].astype(str)
     
    #匹配求和模块
    V5 = pd.merge(订单表,淘客表,how = 'left', on = '订单编号')
    
    V5['佣金'].fillna(value=0,axis=0,inplace=True)
    V5['服务费金额'].fillna(value=0,axis=0,inplace=True)
    V5['平台扣除费用'] = V5['佣金'] + V5['服务费金额']
    
    #抖音的时间格式本来就是字符串格式，现转换成时间戳
    V5['订单创建时间'] = pd.to_datetime(V5['订单创建时间'])
    V5['发货时间']  = pd.to_datetime(V5['发货时间'])
    
    V5['发货时长'] = (V5['发货时间'] - V5['订单创建时间'])  
    
    #【0614加入数据转换】————————————————————————
    V5['订单创建日期'] = pd.to_datetime(V5['订单创建日期'])
    V5['订单创建日期'] = V5['订单创建日期'].dt.date
    V5['订单创建日期'] = V5['订单创建日期'].astype(str)
    
    V6 = 日期连续性(V5,'订单创建日期') #使得日期连续
    #【0614加入数据转换】————————————————————————
    
    性质 = '发货'
    时长计算 = '发货时长' 
    #【0614加入数据转换】————————————————————————
    V6[f'{性质}时长'].fillna(pd.Timedelta(seconds=0),inplace=True) #中间过程
    #【0614加入数据转换】————————————————————————
    
    金额速度表,揽收时间表 = 中间过程判断(V6,性质,时长计算,精确天数)
    
    return 金额速度表,揽收时间表 #中间过程也传过去方便对比

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
    



from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget
from ui_CollectCost import Ui_Form

class Window(QWidget):
    def __init__(self):
        super().__init__()
        # 使用ui_Clean文件导入界面定义类
        self.ui = Ui_Form()
        self.ui.setupUi(self)  # 传入QWidget对象
        self.ui.retranslateUi(self)

        # 实例变量
        self.清洗后文件夹路径 = ''
        self.保存文件绝对路径 = ''
        self.操作人 = ''
        self.精确天数 = '' 
        self.temp = ''  # 用于保存打开文件的路径

        self.ui.InputButton_2.clicked.connect(self.getSecondDir)
        self.ui.OutputButton.clicked.connect(self.getOutputDir)
        self.ui.RunButton.clicked.connect(self.handel)


    def getSecondDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择清洗后文件夹路径") 
        if self.temp != '':
            self.清洗后文件夹路径 = self.temp
            self.ui.InputFile_2.setText(self.清洗后文件夹路径)

    def getOutputDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")  # 不使用本地对话框，可以查看文件夹内文件
        # self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")
        if self.temp != '':
            self.保存文件绝对路径 = self.temp
            self.ui.OutputDir.setText(self.保存文件绝对路径)

    def handel(self):

        # 获取输入值
        self.操作人 = self.ui.User.text()
        self.精确天数 = self.ui.Remark.text()  

        if self.清洗后文件夹路径 == '':
            QMessageBox.about(self, "报错！", '请选择清洗后文件夹路径')
            return
        if self.保存文件绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择保存路径')
            return
        if self.操作人 == '':
            QMessageBox.about(self, "报错！", '请输入操作人')
            return

        需打开表格名列表 = ['订单表','团长表','联盟表','运单表','淘客表'] #成本表需自己选择
        # 实例化对象,调用方法
        自动提取文件 = AutoExtractFiles(self.清洗后文件夹路径,需打开表格名列表)
        需打开表格字典 = 自动提取文件.handle() #['订单表'：对应文件路径]
        
        文件名 = os.path.basename(需打开表格字典['订单表']) # loose-天猫-账单表-清洗后.xlsx
        文件名前缀 = os.path.splitext(文件名)[0] # loose-天猫-账单表-清洗后
        平台类型 = 文件名前缀.split('-')[1] # loose-【天猫】-账单表-清洗后
        客户名称 = 文件名前缀.split('-')[0] # 【loose】-天猫-账单表-清洗后
        for k,v in 需打开表格字典.items():
            if k == '订单表':
                订单表 = pd.read_excel(v)
            elif k == '团长表':
                团长表 = pd.read_excel(v)
            elif k == '联盟表':
                联盟表 = pd.read_excel(v)
            elif k == '运单表':
                运单表 = pd.read_excel(v)
            elif k == '淘客表':
                淘客表 = pd.read_excel(v)
      
        #可以没有备注
        if self.精确天数 == '':
            self.精确天数 = '10'

        精确天 = int(self.精确天数)
        输出文件名格式 = f'\\{客户名称}-{平台类型}-揽收成本表-{self.操作人}-{self.精确天数}天.xlsx'
        输出路径 = self.保存文件绝对路径 + 输出文件名格式

            
        if 平台类型 == '抖音' :

            揽收速度表,揽收时间表 = 抖音揽收成本表(订单表,运单表,联盟表,团长表,精确天)
        elif 平台类型 == '快手' :
            
            揽收速度表,揽收时间表 = 快手揽收成本表(订单表,运单表,精确天)
        elif 平台类型 == '天猫' or 平台类型 == '淘宝':
            
            揽收速度表,揽收时间表 = 天猫揽收成本表(订单表,淘客表,精确天)            
        else :
            QMessageBox.about(self, "报错！", "命名格式错误：平台类型")
            return

        #——————————————————————————————————————————————————————————————————打开与保存模块

        #写入
        writer = pd.ExcelWriter(输出路径)
        揽收速度表.to_excel(writer, sheet_name='揽收速度成本表')
        # 中间源数据.to_excel(writer, sheet_name='中间源数据',index=False)
        揽收时间表.to_excel(writer, sheet_name='揽收时间成本表')
        writer.save()
        #不用删掉，不然文件短时间内不能编辑，只能读取
        writer.close()

        QMessageBox.about(self, "处理结果", f'成功！\n请于“{self.保存文件绝对路径}”查看结果文件')

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()