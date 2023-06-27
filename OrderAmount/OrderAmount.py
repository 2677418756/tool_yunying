# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 11:27:20 2022

@author: Admin
"""

import pandas as pd
import os
import os.path
import numpy as np


#整体逻辑
#一、
#根据订单编号将订单表中的订单时间匹配到售后表中（售后表行数量不变，只是多了一列）
#再售后表根据退商品金额仔细分类到是退款金额还是退货金额
#再售后表两次按自然日分组求和，也可以用透析表代替，行：提交日期，值：退货、退款
#二、
#按自然日的订单金额分组求和，作为分母（每日退款or退货金额/每日总订单应付金额）
#每日订单应付金额可以从订单表按订单创建日期为主键分组求和
#综上根据订单创建日期合并两表
#再新增两列计算比率

def 抖音订单金额表(订单表,售后表) :
    
    订单表_并入售后 = 订单表.copy()
    订单表_并入售后.drop('订单应付金额',axis = 1,inplace=True)
    售后表_增加时间列 = pd.merge(售后表,订单表_并入售后,left_on ='商品单号',right_on ='商品单号',how ='left') 
    
    #为了可以保留19位订单号后面尾数显示不丢失，进行类型转换
    # 售后表_增加时间列['订单编号'] = 售后表_增加时间列['订单编号'].astype(str)
    # 售后表_增加时间列.to_excel(r'C:\Users\Admin\Desktop\找丢.xlsx')
    售后表_增加时间列['商品单号'] = 售后表_增加时间列['商品单号'].astype(str)
    #售后表_增加时间列.to_excel(r'C:\Users\Admin\Desktop\松哥售后表\售后表_增加时间列.xlsx')
    
    
    #创建退款金额、退货金额列
    def 退款金额(flag):
        if flag == '未发货仅退款':
            return 1
        else:
            return 0
    
    def 退货金额(flag):
        if flag == '退货退款' or flag == '已发货仅退款' or flag == '换货': #此处的换货时清洗后的换货，保留了换货中退货的
            return 1
        else:
            return 0
        
    售后表_增加时间列['退款金额'] = 售后表_增加时间列['售后类型'].map(退款金额)
    售后表_增加时间列['退款金额'] = 售后表_增加时间列['退款金额'] * 售后表_增加时间列['实退款金额']
    
    售后表_增加时间列['退货金额'] = 售后表_增加时间列['售后类型'].map(退货金额)
    售后表_增加时间列['退货金额'] = 售后表_增加时间列['退货金额'] * 售后表_增加时间列['实退款金额']
    # 售后表_增加时间列.to_excel(r'C:\Users\Admin\Desktop\找丢失.xlsx')
    #让订单创建日期显示正确
    订单表['订单创建日期'] = 订单表['订单创建日期'].dt.date
    订单表['订单创建日期'] = 订单表['订单创建日期'].astype(str)  
    售后表_增加时间列['订单创建日期'] = 售后表_增加时间列['订单创建日期'].dt.date
    售后表_增加时间列['订单创建日期'] = 售后表_增加时间列['订单创建日期'].astype(str)  
    
    #建立订单金额透析表
    售后透析表 = pd.pivot_table(售后表_增加时间列,index=['订单创建日期'],values=['退款金额','退货金额'],aggfunc = [np.sum])
    #去除表头sum
    售后透析表.columns = 售后透析表.columns.droplevel(0)               
    #售后透析表.to_excel(r'C:\Users\Admin\Desktop\松哥售后表\售后透析表.xlsx')
    
    #——————————————————————————————————————————————————————————————————————————————————创建退款率、销售退货率、揽收退货率
    订单表透析 = pd.pivot_table(订单表,index=['订单创建日期'],values=['订单应付金额'],aggfunc = [np.sum])
    #去除表头sum
    订单表透析.columns = 订单表透析.columns.droplevel(0)
    #订单表透析.to_excel(r'C:\Users\Admin\Desktop\松哥售后表\订单表透析.xlsx')
    
    订单金额表 = pd.merge(订单表透析,售后透析表,on ='订单创建日期',how ='left') 
    #订单金额表.to_excel(r'C:\Users\Admin\Desktop\松哥售后表\订单金额表.xlsx')
    
    #给退款金额和退货金额补零
    订单金额表['退款金额'] = 订单金额表['退款金额'].fillna(0)
    订单金额表['退货金额'] = 订单金额表['退货金额'].fillna(0)
    
    #出现0除0的风险，暂时以runtimewarning警告【具体体现在揽收退货率】
    订单金额表['退款率'] = 订单金额表.apply(lambda x: x['退款金额']/x['订单应付金额'],axis=1)
    订单金额表['销售退货率'] = 订单金额表.apply(lambda x: x['退货金额']/x['订单应付金额'],axis=1)
    订单金额表['揽收退货率'] = 订单金额表.apply(lambda x: x['退货金额']/(x['订单应付金额'] - x['退款金额']),axis =1)
    订单金额表['揽收退货率'] = 订单金额表['揽收退货率'].fillna(0)
    
    # #——————————————————————————————————————————————————————————————————————————————————样式调整
    # 订单金额表[u'退款率'] = 订单金额表[u'退款率'].apply(lambda x: format(x, '.1%')) 
    # 订单金额表[u'销售退货率'] = 订单金额表[u'销售退货率'].apply(lambda x: format(x, '.1%')) 
    # 订单金额表[u'揽收退货率'] = 订单金额表[u'揽收退货率'].apply(lambda x: format(x, '.1%'))  
    # #——————————————————————————————————————————————————————————————————————————————————样式调整
    
    return 订单金额表
    
def 快手订单金额表(订单表,售后表) :
        
    #两表合并，也就是VLOOKUP
    data3 = pd.merge(订单表,售后表,left_on ='订单编号',right_on ='订单编号',how ='left') 
       
    #为了可以保留19位订单号后面尾数不丢失，进行类型转换
    data3['订单编号'] = data3['订单编号'].astype(str)

    #创建售后金额列，直接从退款金额的数值复制过来
    data3['售后金额'] = data3['实退款金额']
    # data3.insert(14, '售后金额', data3['应退款金额'])
    #创建退款金额、退货金额列
    def 退款金额(flag):
        if flag == '仅退款':
            return 1
        else:
            return 0
    
    def 退货金额(flag):
        if flag == '退货退款':
            return 1
        else:
            return 0
    
    def 订单佣金处理(flag):
        if flag == '仅退款':
            return 0
        elif flag == '退货退款':
            return 0
        else:
            return 1 
        
    data3['退款金额'] = data3['售后类型'].map(退款金额)
    data3['退款金额'] = data3['退款金额'] * data3['实退款金额']
    data3['退货金额'] = data3['售后类型'].map(退货金额)
    data3['退货金额'] = data3['退货金额'] * data3['实退款金额']
    #【快手独特处理】将有退款退货的订单佣金列强制改为0
    data3['预估推广佣金标志'] = data3['售后类型'].map(订单佣金处理)
    data3['预估推广佣金'] = data3['预估推广佣金'] * data3['预估推广佣金标志']

    #建立订单金额透析表
    data5 = pd.pivot_table(data3,index=['订单创建日期'],values=['订单应付金额','退款金额','退货金额','预估推广佣金'],aggfunc = [np.sum])
    #去除表头sum
    data5.columns = data5.columns.droplevel(0)
    
    #创建退款率、销售退货率、揽收退货率
    data5['退款率'] = data5.apply(lambda x: x['退款金额']/x['订单应付金额'],axis=1)
    data5['销售退货率'] = data5.apply(lambda x: x['退货金额']/x['订单应付金额'],axis=1)
    data5['揽收退货率'] = data5.apply(lambda x: x['退货金额']/(x['订单应付金额'] - x['退款金额']),axis =1)
    
    # #——————————————————————————————————————————————————————————————————————————————————样式调整
    # data5[u'退款率'] = data5[u'退款率'].apply(lambda x: format(x, '.1%')) 
    # data5[u'销售退货率'] = data5[u'销售退货率'].apply(lambda x: format(x, '.1%')) 
    # data5[u'揽收退货率'] = data5[u'揽收退货率'].apply(lambda x: format(x, '.1%'))  
    # #——————————————————————————————————————————————————————————————————————————————————样式调整
    
    return data5

def 拼多多订单金额表(订单表):
    
    #读取对应字段
    ##根据订单状态来bool，然后乘对应金额
        
    #创建退款金额、退货金额列
    def 退款金额(flag):
        if flag == '未发货，退款成功':
            return 1
        else:
            return 0
    
    def 退货金额(flag):
        if flag == '已签收，退款成功' or flag == '已发货，退款成功':
            return 1
        else:
            return 0
        
    订单表['退款金额'] = 订单表['订单状态'].map(退款金额)
    订单表['退款金额'] = 订单表['退款金额'] * 订单表['订单应付金额']
    
    订单表['退货金额'] = 订单表['订单状态'].map(退货金额)
    订单表['退货金额'] = 订单表['退货金额'] * 订单表['订单应付金额']

    #让订单创建日期显示正确
    订单表['订单创建日期'] = 订单表['订单创建日期'].dt.date
    订单表['订单创建日期'] = 订单表['订单创建日期'].astype(str)  
    
    #建立订单金额透析表
    订单金额表 = pd.pivot_table(订单表,index=['订单创建日期'],values=['订单应付金额','退款金额','退货金额'],aggfunc = [np.sum])
    #去除表头sum
    订单金额表.columns = 订单金额表.columns.droplevel(0)           
        
    #给退款金额和退货金额补零
    订单金额表['退款金额'] = 订单金额表['退款金额'].fillna(0)
    订单金额表['退货金额'] = 订单金额表['退货金额'].fillna(0)
    
    #出现0除0的风险，暂时以runtimewarning警告【具体体现在揽收退货率】
    订单金额表['退款率'] = 订单金额表.apply(lambda x: x['退款金额']/x['订单应付金额'],axis=1)
    订单金额表['销售退货率'] = 订单金额表.apply(lambda x: x['退货金额']/x['订单应付金额'],axis=1)
    订单金额表['揽收退货率'] = 订单金额表.apply(lambda x: x['退货金额']/(x['订单应付金额'] - x['退款金额']),axis =1)
    订单金额表['揽收退货率'] = 订单金额表['揽收退货率'].fillna(0)
    
    # #——————————————————————————————————————————————————————————————————————————————————样式调整
    # 订单金额表[u'退款率'] = 订单金额表[u'退款率'].apply(lambda x: format(x, '.1%')) 
    # 订单金额表[u'销售退货率'] = 订单金额表[u'销售退货率'].apply(lambda x: format(x, '.1%')) 
    # 订单金额表[u'揽收退货率'] = 订单金额表[u'揽收退货率'].apply(lambda x: format(x, '.1%'))  
    # #——————————————————————————————————————————————————————————————————————————————————样式调整
    return 订单金额表

def 京东订单金额表(订单表):
    
    #读取对应字段
    ##根据订单状态来bool，然后乘对应金额
        
    #创建退款金额、退货金额列
    def 退款金额(flag):
        if flag == '(删除)等待出库' or flag == '(删除)新订单' or flag == '(删除)暂停' or flag == '(锁定)等待出库':
            return 1
        else:
            return 0
    
    def 退货金额(flag):
        if flag == '(锁定)等待确认收货' or flag == '(删除)等待确认收货':
            return 1
        else:
            return 0
    
    订单表.insert(1, '订单总数量', 1)
    
    订单表['退款数量'] = 订单表['订单状态'].map(退款金额)
    订单表['退款金额'] = 订单表['退款数量'] * 订单表['订单应付金额']

    订单表['退货数量'] = 订单表['订单状态'].map(退货金额)
    订单表['退货金额'] = 订单表['退货数量'] * 订单表['订单应付金额']
    
    
    #让订单创建日期显示正确
    订单表['订单创建日期'] = 订单表['订单创建日期'].dt.date
    订单表['订单创建日期'] = 订单表['订单创建日期'].astype(str)  
    
    #建立订单金额透析表
    订单金额表 = pd.pivot_table(订单表,index=['订单创建日期'],values=['订单应付金额','订单总数量','退款金额','退款数量','退货金额','退货数量'],aggfunc = [np.sum])
    #去除表头sum
    订单金额表.columns = 订单金额表.columns.droplevel(0)           
        
    #给退款金额和退货金额补零
    订单金额表['退款金额'] = 订单金额表['退款金额'].fillna(0)
    订单金额表['退货金额'] = 订单金额表['退货金额'].fillna(0)
    
    #出现0除0的风险，暂时以runtimewarning警告【具体体现在揽收退货率】
    订单金额表['退款率'] = 订单金额表.apply(lambda x: x['退款数量']/x['订单总数量'],axis=1)
    订单金额表['销售退货率'] = 订单金额表.apply(lambda x: x['退货数量']/x['订单总数量'],axis=1)
    订单金额表['揽收退货率'] = 订单金额表.apply(lambda x: x['退货数量']/(x['订单总数量'] - x['退款数量']),axis =1)
    订单金额表['揽收退货率'] = 订单金额表['揽收退货率'].fillna(0)
    
    # #——————————————————————————————————————————————————————————————————————————————————样式调整
    # 订单金额表[u'退款率'] = 订单金额表[u'退款率'].apply(lambda x: format(x, '.1%')) 
    # 订单金额表[u'销售退货率'] = 订单金额表[u'销售退货率'].apply(lambda x: format(x, '.1%')) 
    # 订单金额表[u'揽收退货率'] = 订单金额表[u'揽收退货率'].apply(lambda x: format(x, '.1%'))  
    # #——————————————————————————————————————————————————————————————————————————————————样式调整
    return 订单金额表

def 天猫订单金额表(订单表):
    
    def 是否退货退款(退货退款金额):
        if 退货退款金额 !='没有申请退款' or  退货退款金额 !='退款关闭':
            return 1
        else :
            return 0
    
    def 是否发货(运单号):
        #已经提前将运单号转换为str格式，可以直接判断nan
        if 运单号 != 'nan' :
            return 1
        else :
            return 0
    
    #创建退款金额、退货金额列
    def 退款金额(flag1,flag2):
        if flag1 == 1 and flag2 == 0:
            return 1
        else:
            return 0
    
    def 退货金额(flag1,flag2):
        if flag1 == 1 and flag2 == 1:
            return 1
        else:
            return 0
    
    
    订单表['运单号'] = 订单表['运单号'].astype(str)
    
    订单表['是否退货退款'] = 订单表['售后状态'].map(是否退货退款)
    订单表['是否发货'] = 订单表['运单号'].map(是否发货)
    
    
    订单表['退款金额'] = list(map(退款金额,订单表['是否退货退款'],订单表['是否发货']))
    订单表['退款金额'] = 订单表['退款金额'] * 订单表['退货退款金额']
    
    订单表['退货金额'] = list(map(退货金额,订单表['是否退货退款'],订单表['是否发货']))
    订单表['退货金额'] = 订单表['退货金额'] * 订单表['退货退款金额']
    
    #让订单创建日期显示正确
    订单表['订单创建日期'] = 订单表['订单创建日期'].dt.date
    订单表['订单创建日期'] = 订单表['订单创建日期'].astype(str)  
    
    
    #建立订单金额透析表
    订单金额表 = pd.pivot_table(订单表,index=['订单创建日期'],values=['订单应付金额','退款金额','退货金额'],aggfunc = [np.sum])
    #去除表头sum
    订单金额表.columns = 订单金额表.columns.droplevel(0)           
        
    #给退款金额和退货金额补零
    订单金额表['退款金额'] = 订单金额表['退款金额'].fillna(0)
    订单金额表['退货金额'] = 订单金额表['退货金额'].fillna(0)
    
    #出现0除0的风险，暂时以runtimewarning警告【具体体现在揽收退货率】
    订单金额表['退款率'] = 订单金额表.apply(lambda x: x['退款金额']/x['订单应付金额'],axis=1)
    订单金额表['销售退货率'] = 订单金额表.apply(lambda x: x['退货金额']/x['订单应付金额'],axis=1)
    订单金额表['揽收退货率'] = 订单金额表.apply(lambda x: x['退货金额']/(x['订单应付金额'] - x['退款金额']),axis =1)
    订单金额表['揽收退货率'] = 订单金额表['揽收退货率'].fillna(0)
    
    # #——————————————————————————————————————————————————————————————————————————————————样式调整
    # 订单金额表[u'退款率'] = 订单金额表[u'退款率'].apply(lambda x: format(x, '.1%')) 
    # 订单金额表[u'销售退货率'] = 订单金额表[u'销售退货率'].apply(lambda x: format(x, '.1%')) 
    # 订单金额表[u'揽收退货率'] = 订单金额表[u'揽收退货率'].apply(lambda x: format(x, '.1%'))  
    # #——————————————————————————————————————————————————————————————————————————————————样式调整
    return 订单金额表

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

#——————————————————————————————————————————————————————主程序开始————————————————————————————————————————————————#
#输入表格命名规则：客户名称-平台名称-表格名称-操作人-备注
#输出表格命名规则：客户名称-订单金额表-操作人-备注

#自动获取：客户名称-0、备注-4、
#用户输入：订单表路径、售后表路径、操作人、备注

#——————————————————————————————————————————————————————————————————————————————用户输入模块

from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget
from ui_NewOrderAmount import Ui_Form

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
        self.备注 = '' 
        self.temp = ''  # 用于保存打开文件的路径

        self.ui.InputButton.clicked.connect(self.getInputDir)
        self.ui.OutputButton.clicked.connect(self.getOutputDir)
        self.ui.RunButton.clicked.connect(self.handel)


    def getInputDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择清洗后文件夹路径") 
        if self.temp != '':
            self.清洗后文件夹路径 = self.temp
            self.ui.InputDir.setText(self.清洗后文件夹路径)

    def getOutputDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")  # 不使用本地对话框，可以查看文件夹内文件
        # self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")
        if self.temp != '':
            self.保存文件绝对路径 = self.temp
            self.ui.OutputDir.setText(self.保存文件绝对路径)

    def handel(self):

        # 获取输入值
        self.操作人 = self.ui.User.text()
        self.备注 = self.ui.Remark.text()  

        # 输入值为空时
        if self.清洗后文件夹路径 == '':
            QMessageBox.about(self, "报错！", '请选择清洗后文件夹路径')
            return
        if self.保存文件绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择保存路径')
            return
        if self.操作人 == '':
            QMessageBox.about(self, "报错！", '请输入操作人')
            return

        需打开表格名列表 = ['订单表','售后表'] #成本表需自己选择
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
            elif k == '售后表':
                售后表 = pd.read_excel(v)

        #可以没有备注
        if self.备注 == '':
            self.备注 = '无备注'
        

        #——————————————————————————————————————————————————————————————————打开与保存模块
        输出文件名格式 = f'\\{客户名称}-{平台类型}-订单金额表-{self.操作人}-{self.备注}.xlsx'
        输出路径 = self.保存文件绝对路径 + 输出文件名格式


        if 平台类型 == '快手' :
            订单金额表 = 快手订单金额表(订单表,售后表)
        elif 平台类型 == '抖音' :
            订单金额表 = 抖音订单金额表(订单表,售后表)
        elif 平台类型 == '拼多多' :
            订单金额表 = 拼多多订单金额表(订单表)
        elif 平台类型 == '京东' :
            订单金额表 = 京东订单金额表(订单表)
        elif 平台类型 == '天猫' :
            订单金额表 = 天猫订单金额表(订单表)
        else :
            # print('命名格式错误：平台类型')
            QMessageBox.about(self, "报错！", "命名格式错误：平台类型")
            return

        #——————————————————————————————————————————————————————————————————打开与保存模块

        订单金额表.to_excel(输出路径)

        QMessageBox.about(self, "处理结果", f'成功！\n请于“{self.保存文件绝对路径}”查看结果文件')


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()








