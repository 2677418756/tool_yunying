# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 13:44:22 2022

@author: Admin
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 11:10:59 2022

@author: Admin
"""

#读取订单表，删除三待一同（去掉退货退款的），获取订单应付金额
#读取联盟佣金表，团长佣金表，匹配对应金额进订单表，将NA（也就是自然流量卖，不用付佣金的）的单元格变为0
#读取成本表，与订单表中商家编码匹配，获取对应成本价

import pandas as pd
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

def 抖音订单成本金额表(订单表,联盟表,团长表):
    
    #筛选
    订单表 = 订单表[~(订单表.售后状态.isin(['待买家退货处理'])|订单表.售后状态.isin(['待商家处理'])|订单表.售后状态.isin(['待商家收货'])|订单表.售后状态.isin(['同意退款，退款成功']))]
    #样式优化
    订单表['订单创建日期'] = 订单表['订单创建日期'].dt.date
    订单表['订单创建日期'] = 订单表['订单创建日期'].astype(str)
    #匹配求和模块
    # 订单计数项 = 订单表.copy()
    合并0 = pd.merge(订单表,联盟表,how = 'left', on = '商品单号')
    合并1 = pd.merge(合并0,团长表,how = 'left', on = '商品单号')


    透析0 = pd.pivot_table(合并1,index=['订单创建日期'],values = ['订单应付金额','联盟佣金','团长佣金','商品单号'],aggfunc={'订单应付金额':np.sum,'联盟佣金':np.sum,'团长佣金':np.sum,'商品单号':len})
    #透析0.columns = 透析0.columns.droplevel(0)
    
    #修改正确的字段的名称
    透析0.rename(columns={'商品单号':'统计数'},inplace = True)
    透析0.rename(columns={'订单应付金额':'剩余销售金额'},inplace = True)

    #增加算术运算得到的列
    透析0['运费'] = 透析0['统计数'].map(lambda x : round(x*2.7,2))
    # 透析0['上游成本税'] = 透析0['成本价'].map(lambda x : x*0.08)
    透析0['平台扣点'] = 透析0['剩余销售金额'].map(lambda x : round(x*0.05,2))
    透析0['资金成本'] = 透析0['剩余销售金额'].map(lambda x : round(x*0.035,2))
    #删除不需要显示的列
    透析0.drop('统计数', axis=1, inplace=True)
    #改变列的序列
    透析0 = 透析0.loc[:,['剩余销售金额','联盟佣金','团长佣金','运费','资金成本','平台扣点']]

    return 透析0

def 快手订单成本金额表(订单表):
    
    #筛选
    订单表 = 订单表[~(订单表.退货退款.isin(['退款成功']))]
    #样式优化
    订单表['订单创建日期'] = pd.to_datetime(订单表['订单创建日期'])
    订单表['订单创建日期'] = 订单表['订单创建日期'].dt.date
    订单表['订单创建日期'] = 订单表['订单创建日期'].astype(str)
    #匹配求和模块

    透析0 = pd.pivot_table(订单表,index=['订单创建日期'],values = ['订单应付金额','预估推广佣金'],aggfunc={'订单应付金额':np.sum,'预估推广佣金':np.sum})
    #透析0.columns = 透析0.columns.droplevel(0)
    
    #修改正确的字段的名称
    # 透析0.rename(columns={'商品单号':'统计数'},inplace = True)
    透析0.rename(columns={'订单应付金额':'剩余销售金额'},inplace = True)

    # #增加算术运算得到的列
    # 透析0['运费'] = 透析0['统计数'].map(lambda x : round(x*2.7,2))
    # 透析0['上游成本税'] = 透析0['成本价'].map(lambda x : x*0.08)
    # 透析0['平台扣点'] = 透析0['剩余销售金额'].map(lambda x : round(x*0.05,2))
    # 透析0['资金成本'] = 透析0['剩余销售金额'].map(lambda x : round(x*0.035,2))
    #删除不需要显示的列
    # 透析0.drop('统计数', axis=1, inplace=True)
    #改变列的序列
    透析0 = 透析0.loc[:,['剩余销售金额','预估推广佣金']]

    return 透析0

def 天猫订单成本金额表(订单表,淘客表):

    def 是否退货退款(退货退款金额):
        if 退货退款金额 !='没有申请退款' or  退货退款金额 !='退款关闭':
            return 1
        else :
            return 0

    #将没退的保留下来
    订单表['是否退货退款'] = 订单表['售后状态'].map(是否退货退款)
    订单表 = 订单表[(订单表.是否退货退款.isin([0]))]

    #样式优化
    订单表['订单创建日期'] = 订单表['订单创建日期'].dt.date
    订单表['订单创建日期'] = 订单表['订单创建日期'].astype(str)
    
    
    #匹配求和模块
    # 订单计数项 = 订单表.copy()
    合并0 = pd.merge(订单表,淘客表,how = 'left', on = '订单编号')


    透析0 = pd.pivot_table(合并0,index=['订单创建日期'],values = ['订单应付金额','佣金','服务费金额'],aggfunc={'订单应付金额':np.sum,'佣金':np.sum,'服务费金额':np.sum})
    #透析0.columns = 透析0.columns.droplevel(0)
    
    # #修改正确的字段的名称
    透析0.rename(columns={'订单应付金额':'剩余销售金额'},inplace = True)

    #增加算术运算得到的列
    #删除不需要显示的列
    透析0.drop('统计数', axis=1, inplace=True)
    #改变列的序列
    透析0 = 透析0.loc[:,['剩余销售金额','佣金','服务费金额']]

    return 透析0

from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget
from ui_OrderCost import Ui_Form

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
            self.ui.InputFile.setText(self.清洗后文件夹路径)

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

        需打开表格名列表 = ['订单表','团长表','联盟表','淘客表'] #成本表需自己选择
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
            elif k == '淘客表':
                淘客表 = pd.read_excel(v)
        
        
        #可以没有备注
        if self.备注 == '':
            self.备注 = '无备注'


        输出文件名格式 = f'\\{客户名称}-{平台类型}-订单成本金额表-{self.操作人}-{self.备注}.xlsx'
        输出路径 = self.保存文件绝对路径 + 输出文件名格式

            
        if 平台类型 == '抖音' :
            订单成本金额表 = 抖音订单成本金额表(订单表,联盟表,团长表)
        elif 平台类型 == '快手' :
            订单成本金额表 = 快手订单成本金额表(订单表)
        elif 平台类型 == '天猫' or 平台类型 == '淘宝' :
            订单成本金额表 = 天猫订单成本金额表(订单表,淘客表)            
        else :
            QMessageBox.about(self, "报错！", "命名格式错误：平台类型")
            return

        #——————————————————————————————————————————————————————————————————打开与保存模块

        订单成本金额表.to_excel(输出路径)#因为订单创建日期变成INDEX了

        QMessageBox.about(self, "处理结果", f'成功！\n请于“{self.保存文件绝对路径}”查看结果文件')

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()