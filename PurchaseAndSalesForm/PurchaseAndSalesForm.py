# -*- coding: utf-8 -*-
"""
Created on Sat May 28 16:46:41 2022

@author: Admin
"""


import pandas as pd
import numpy as np
import datetime
import os

def two_decimal(x_data):
    #【浮点数先转字符串，再转浮点数】让数据保留一位小数，且自动四舍五入
    x_str = '%.2f' % x_data #变成字符串来保留一位小数了
    return float(x_str)

def timestamp_to_date(timestamp_):
    date = timestamp_.to_pydatetime().date()
    return date

def OnedayCostOfGoods(Order,Cost,date):

    #防止表格读取后再写入相关字段乱码
    Order['订单编号'] = Order['订单编号'].astype(str)
    Order['商品单号'] = Order['商品单号'].astype(str)

    # 先精炼出订单创建日期
    Order['统计标志'] = '失败'
    # Order['批次标志'] = '失败'
    Order['统计成本价'] = round(Order['订单应付金额']/Order['成交数量'] * 0.4,2)
    # Order['批次成本价'] = round(Order['订单应付金额'] * 0.5,2)
    try:
        Order['订单创建日期'] = Order['订单创建日期'].map(timestamp_to_date)
    except:
        pass
    temp_need_drop = Order.duplicated('商家编码') #返回类型：dataframe
    temp_order_only = Order[~temp_need_drop] #返回类型：dataframe
    orderBusinessCode = temp_order_only['商家编码'] #返回类型：series

    for code in orderBusinessCode:
        #先切片商家编码，再条件对比批次日期与统计日期

        temp_cost_use = Cost[Cost['商家编码'].isin([code])]

        for i in range(len(temp_cost_use)):
            use_time = temp_cost_use['统计日期'].max()
            if use_time > date :
                #若提取的批次日期大于订单创建日期，则排除
                temp_cost_use = temp_cost_use[~temp_cost_use.统计日期.isin([use_time])]
            elif use_time <= date :
                #若提取的批次日期小于等于订单创建日期，则使用该批次对应的货物成本
                use_price_series  = temp_cost_use.loc[temp_cost_use['统计日期'].isin([use_time]),'成本价（含税）'] #返回类型：Series
                use_price = round(use_price_series.iloc[0],2) #按iloc索引
                #直接匹配到订单表内
                Order.loc[Order['订单创建日期'].isin([date])&Order['商家编码'].isin([code]),'统计成本价'] = use_price
                Order.loc[Order['订单创建日期'].isin([date])&Order['商家编码'].isin([code]),'统计标志'] = '成功'
                break
            
    Order['统计成本总价'] = Order['统计成本价'] * Order['成交数量']
    # Order['批次成本总价'] = Order['批次成本价'] * Order['成交数量']
    return Order


def 抖音采购与销售合同表格(目标值输入,场次日期输入,订单表,成本表):
    
    
    场次日期 = datetime.datetime.strptime(场次日期输入,'%Y-%m-%d').date()
    目标值 = float(目标值输入)
    
    订单表 = 订单表[(订单表.订单创建日期.isin([f'{场次日期}']))]
    订单表 = 订单表[~(订单表.售后状态.isin(['待买家退货'])|订单表.售后状态.isin(['待商家处理'])|订单表.售后状态.isin(['待商家收货'])|订单表.售后状态.isin(['同意退款，退款成功']))]
    订单货物成本表 = OnedayCostOfGoods(订单表,成本表,场次日期)
    订单货物成本表 = 订单货物成本表[(订单货物成本表.统计标志.isin(['成功']))] #只有匹配成功的货物，有了成本价才允许采购
    透析0 = pd.pivot_table(订单货物成本表,index=['商家编码'],values=['成交数量'],aggfunc=[np.sum]) #获取商家编码为唯一值的办法
    透析0.columns = 透析0.columns.droplevel(0)
    
    #两表合并成采购表
    订单货物成本表.drop(['成交数量'],axis= 1,inplace=True) #防止重复成交数量（偷懒了）
    订单货物成本表.drop(['商品名称'],axis= 1,inplace=True) #防止重复商品名称（偷懒了）
    采购表 = pd.merge(透析0,订单货物成本表,on = '商家编码',how = 'left')
    采购表 = 采购表.drop_duplicates('商家编码')
    采购表.rename(columns={'统计成本价':'单价'},inplace = True)
    采购表.rename(columns={'成交数量':'数量'},inplace = True)
    采购表.rename(columns={'商家编码':'商品名称'},inplace = True)
    #数据格式处理，保留两位小数
    采购表['单价'] = round(采购表['单价'],2)
    #降序排列
    采购表 = 采购表.sort_values(by='数量',ascending=False,axis=0)
    #将dataframe转换成字典，变成列表嵌套字典
    计算字典 = 采购表.to_dict('records') #形如[{'商品名称': 'XDNZ4402', '数量': 1, '单价': 41.2776}, {'商品名称': 'D2CTX0394', '数量': 1, '单价': 30.78}]
    
    #计算该场次下总金额
    采购表['金额'] = round(采购表['单价']*采购表['数量'],2)
    起始值 = 采购表['金额'].sum()

    #初始值设置
    # 中间值 = 0
    长度 = len(计算字典)
    
    while 长度 >= 0:
        print('长度%s:'%长度)
        单品总金额 = 计算字典[长度 - 1]['数量'] * 计算字典[长度 - 1]['单价']
        对应商品名称 = 计算字典[长度 - 1]['商品名称']
        print('单品总金额%s'%单品总金额,'对应商品名称%s'%对应商品名称)
        起始值 = 起始值 - 单品总金额
        长度 = 长度 - 1
        if 起始值 < 目标值: 
            # 中间值 = 起始值 + 单品总金额
            break
        计算字典 = [item for item in 计算字典 if not item['商品名称'] == 对应商品名称] #删除对应不需要的商品名称
        
    #数据表转换
    合同采购表 = pd.DataFrame.from_records(计算字典)
    合同供应表 = pd.DataFrame.from_records(计算字典)
    #采购表添加新的列
    合同采购表['序号'] = 合同采购表.index.values + 1
    合同采购表['规格'] = '均码'
    合同采购表['单位'] = '件'
    合同采购表['金额'] = round(合同采购表['单价']*合同采购表['数量'],2)
    #供应表添加新的列
    合同供应表['序号'] = 合同供应表.index.values + 1
    合同供应表['规格'] = '均码'
    合同供应表['单位'] = '件'
    合同供应表['单价'] = round(合同供应表['单价']*1.01,2)
    合同供应表['金额'] = round(合同供应表['单价']*合同供应表['数量'],2)
    
    #改变列的序列
    合同采购表 = 合同采购表.loc[:,['序号','商品名称','规格','单位','数量','单价','金额']]    
    合同供应表 = 合同供应表.loc[:,['序号','商品名称','规格','单位','数量','单价','金额']]  
    
    
    return 合同采购表,合同供应表




from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget
from ui_PurchaseAndSalesForm import Ui_Form

class Window(QWidget):

    def __init__(self):
        super().__init__()
        # 使用ui_Clean文件导入界面定义类
        self.ui = Ui_Form()
        self.ui.setupUi(self)  # 传入QWidget对象
        self.ui.retranslateUi(self)

        # 实例变量
        self.订单表文件绝对路径 = ''
        self.成本表文件绝对路径 = ''
        self.保存文件绝对路径 = ''
        self.目标值 = ''
        self.输入日期 = ''
        self.备注 = ''
        self.temp = ''  # 用于保存打开文件的路径

        self.ui.InputButton_1.clicked.connect(self.getOrderForm)
        self.ui.InputButton_2.clicked.connect(self.getCostForm)
        self.ui.OutputButton.clicked.connect(self.getOutputDir)
        self.ui.RunButton.clicked.connect(self.handel)

    def getOrderForm(self):
        self.temp, _ = QFileDialog.getOpenFileName(self, "选择订单表", '', "Forms(*.xlsx *.csv)")
        if self.temp != '':
            self.订单表文件绝对路径 = self.temp
            self.ui.InputFile_1.setText(self.订单表文件绝对路径)  # 显示路径

    def getCostForm(self):
        self.temp, _ = QFileDialog.getOpenFileName(self, "选择成本表", '', "Forms(*.xlsx *.csv)")
        if self.temp != '':
            self.成本表文件绝对路径 = self.temp
            self.ui.InputFile_2.setText(self.成本表文件绝对路径)

    def getOutputDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")  # 使用本地对话框
        # self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径", '', QFileDialog.DontUseNativeDialog)  # 不使用本地对话框，可以查看文件夹内文件
        if self.temp != '':
            self.保存文件绝对路径 = self.temp
            self.ui.OutputDir.setText(self.保存文件绝对路径)

    def handel(self):

        # 获取输入值
        self.目标值 = self.ui.Target.text()
        self.输入日期 = self.ui.dateEdit.text()
        self.备注 = self.ui.Remark.text()
        #【在前端提前避免一些错误，如空值检测】
        # 输入值为空时
        if self.订单表文件绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择订单表')
            return
        
        if self.成本表文件绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择成本表')
            return
        
        if self.保存文件绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择保存路径')
            return
        
        if self.目标值 == '':
            QMessageBox.about(self, "报错！", '请输入目标值')
            return
        
        if self.输入日期 == '':
            QMessageBox.about(self, "报错！", '请输入合同日期')
            return
        

        
        订单表文件名 = os.path.split(self.订单表文件绝对路径)[1] #客户名称-平台名称-表格名称-操作人-备注.xlsx
     
        文件名前缀 = os.path.splitext(订单表文件名)[0] # loose-天猫-账单表-清洗后
        平台类型 = 文件名前缀.split('-')[1] # loose-【天猫】-账单表-清洗后
        客户名称 = 文件名前缀.split('-')[0] # 【loose】-天猫-账单表-清洗后 
        
        try:
            日期格式 = datetime.datetime.strptime(f'{self.输入日期}','%Y/%m/%d').strftime('%Y-%m-%d')
        except:
            日期格式 = self.输入日期

        输出文件名格式 = f'\\{客户名称}-{平台类型}-采购与供应表-{self.备注}-{日期格式}.xlsx'
        输出路径 = self.保存文件绝对路径 + 输出文件名格式

        if 平台类型 == '抖音' :
            订单表 = pd.read_excel(self.订单表文件绝对路径)
            成本表 = pd.read_excel(self.成本表文件绝对路径,usecols=['商家编码','成本价（含税）','统计日期'])
            采购表格,供应表格 = 抖音采购与销售合同表格(self.目标值,日期格式,订单表,成本表)
        else :
            # print('命名格式错误：平台类型')
            QMessageBox.about(self, "报错！", "命名格式错误：平台类型")
            return

        #————————————————————————————————————————————————————————————————————————输出模块        
        #【writer】使用writer将dataframe放入不同的excel的sheet中
        #使用pd.ExcelWriter

        writer = pd.ExcelWriter(输出路径)
        采购表格.to_excel(writer, sheet_name='采购合同表格',index=False)
        供应表格.to_excel(writer, sheet_name='供应合同表格',index=False)

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