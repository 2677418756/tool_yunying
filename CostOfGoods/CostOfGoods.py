# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 10:59:54 2022

@author: Admin
"""

import pandas as pd
import datetime
import os


def str_to_date(str_):
    #【日期类型转换】让数据从str型转换成date型
    date_p = datetime.datetime.strptime(str_,'%Y-%m-%d').date()
    return date_p
def date_to_str(date_):
    #【日期类型转换】让数据从date型转换成str型
    return str(date_)

def timestamp_to_date(timestamp_):
    date = timestamp_.to_pydatetime().date()
    return date

def CostOfGoods(Order,Cost):

    #防止表格读取后再写入相关字段乱码
    Order['订单编号'] = Order['订单编号'].astype(str)
    Order['商品单号'] = Order['商品单号'].astype(str)

    
    # 先精炼出订单创建日期
    # Order['统计标志'] = '失败'
    Order['批次标志'] = '失败'
    # Order['统计成本价'] = round(Order['订单应付金额'] * 0.5,2)
    Order['批次成本价'] = round(Order['订单应付金额']/Order['成交数量'] * 0.4,2)
    Order['订单创建日期'] = Order['订单创建日期'].map(timestamp_to_date)
    need_drop = Order.duplicated('订单创建日期') #返回与检测列相同长度的布尔类型Series，来反应某列中的重复值
    order_only = Order[~need_drop]
    orderDate = order_only['订单创建日期']

    orderDateList = orderDate.tolist()

    for date in orderDateList:
        """
        思路：第一个循环 —— 按订单创建日期切片
            第二个循环 —— 再按商家编码切片
        """
        #提取同一订单创建日期下的唯一商家编码  
        temp_order = Order[Order['订单创建日期'].isin([date])] #返回类型：dataframe
        temp_need_drop = temp_order.duplicated('商家编码') #返回类型：dataframe
        temp_order_only = temp_order[~temp_need_drop] #返回类型：dataframe
        orderBusinessCode = temp_order_only['商家编码'] #返回类型：series
    
        for code in orderBusinessCode:
            #先切片商家编码，再条件对比批次日期与统计日期
            temp_cost_batch = Cost[Cost['商家编码'].isin([code])]
            # temp_cost_use = Cost[Cost['商家编码'].isin([code])]
            for i in range(len(temp_cost_batch)):
                # print(i)
                batch_time = temp_cost_batch['批次日期'].max()
                # print('当前批次日期提取是%s'%batch_time,'切片为%s'%temp_cost_batch)
                if batch_time > date :
                    #若提取的批次日期大于订单创建日期，则排除
                    temp_cost_batch = temp_cost_batch[~temp_cost_batch.批次日期.isin([batch_time])]
                elif batch_time <= date :
                    #若提取的批次日期小于等于订单创建日期，则使用该批次对应的货物成本
                    cost_price_series  = temp_cost_batch.loc[temp_cost_batch['批次日期'].isin([batch_time]),'成本价（含税）'] #返回类型：Series
                    cost_price = round(cost_price_series.iloc[0],2) #按iloc索引
                    #直接匹配到订单表内
                    Order.loc[Order['订单创建日期'].isin([date])&Order['商家编码'].isin([code]),'批次成本价'] = cost_price
                    Order.loc[Order['订单创建日期'].isin([date])&Order['商家编码'].isin([code]),'批次标志'] = '成功'
                    break
            # for i in range(len(temp_cost_use)):
            #     use_time = temp_cost_use['统计日期'].max()
            #     if use_time > date :
            #         #若提取的批次日期大于订单创建日期，则排除
            #         temp_cost_use = temp_cost_use[~temp_cost_use.统计日期.isin([use_time])]
            #     elif use_time <= date :
            #         #若提取的批次日期小于等于订单创建日期，则使用该批次对应的货物成本
            #         use_price_series  = temp_cost_use.loc[temp_cost_use['统计日期'].isin([use_time]),'成本价（含税）'] #返回类型：Series
            #         use_price = round(use_price_series.iloc[0],2) #按iloc索引
            #         #直接匹配到订单表内
            #         Order.loc[Order['订单创建日期'].isin([date])&Order['商家编码'].isin([code]),'统计成本价'] = use_price
            #         Order.loc[Order['订单创建日期'].isin([date])&Order['商家编码'].isin([code]),'统计标志'] = '成功'
            #         break
            
    # Order['统计成本总价'] = Order['统计成本价'] * Order['成交数量']
    Order['批次成本总价'] = Order['批次成本价'] * Order['成交数量']
    return Order


from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget
from ui_CostOfGoods import Ui_Form

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
        
        if self.备注 == '':
            self.备注 = '无'

        订单表文件名 = os.path.split(self.订单表文件绝对路径)[1] #客户名称-平台名称-表格名称-操作人-备注.xlsx
     
        文件名前缀 = os.path.splitext(订单表文件名)[0] # loose-天猫-账单表-清洗后
        平台类型 = 文件名前缀.split('-')[1] # loose-【天猫】-账单表-清洗后
        客户名称 = 文件名前缀.split('-')[0] # 【loose】-天猫-账单表-清洗后 

        输出文件名格式 = f'\\{客户名称}-{平台类型}-订单货物成本表-{self.备注}.xlsx'
        输出路径 = self.保存文件绝对路径 + 输出文件名格式

        if 平台类型 == '抖音' :
            订单表 = pd.read_excel(self.订单表文件绝对路径,usecols=['订单编号','商品单号','成交数量','商家编码','订单应付金额','订单状态','售后状态','订单创建日期'])
            成本表 = pd.read_excel(self.成本表文件绝对路径)
            Cost = CostOfGoods(订单表,成本表)
        else :
            QMessageBox.about(self, "报错！", "命名格式错误：平台类型")
            return

        #————————————————————————————————————————————————————————————————————————输出模块        

        writer = pd.ExcelWriter(输出路径)
        Cost.to_excel(writer,index=False, sheet_name='订单货物成本表')
        writer.save()
        #不用删掉，不然文件短时间内不能编辑，只能读取
        writer.close()
        # Cost.to_excel(输出路径,index=False,sheetnames = '订单货物成本表')
        #成功后消息提醒
        QMessageBox.about(self, "处理结果", f'成功！\n请于“{self.保存文件绝对路径}”查看结果文件')


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()












