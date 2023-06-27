# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 22:24:46 2022

@author: Admin
"""

import pandas as pd
import datetime
import os 



#可以筛选日期和列的序列    

def walkFile(file,开始日期,结束日期,输出路径):
    
    
    for root, dirs, files in os.walk(file,topdown=False):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件名list

        # 遍历文件
        for f in files:
            # print(f)
            文件名前缀 = os.path.splitext(f)[0]
            l = 文件名前缀.split('-') #列表
            if len(l) == 5 and l[2] == '订单表': #从左到右判断，如果为5才判断后面【感觉这个语法很有问题】
                店铺名称 = l[0]
                平台类型 = l[1]
                try:
                   data = pd.read_excel(os.path.join(root,f),usecols=['订单编号','订单应付金额','订单状态','订单创建时间','商品名称','成交数量','发货时间']) 
                #打开文件，并进行筛选
                except(ValueError):
                    data = pd.read_excel(os.path.join(root,f),usecols=['订单编号','订单应付金额','订单状态','订单创建时间','商品名称','成交数量'])
                    data['发货时间'] = ''
                    
                data = data[(data['订单创建时间'] >= f'{开始日期} 00:00:00') & (data['订单创建时间'] <= f'{结束日期} 23:59:59')]                     
                #改变列的序列
                data = data.loc[:,['订单编号','订单应付金额','订单状态','订单创建时间','商品名称','成交数量','发货时间']]
                #调整展示格式
                data['订单编号'] = data['订单编号'].astype(str)
                #保存到一个文件夹内，给命名名字
                输出文件名格式 = f'\\{平台类型}-订单表-{店铺名称}.xlsx'
                文件保存路径 = 输出路径 + 输出文件名格式
                data.to_excel(文件保存路径,index=False)




from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget
from ui_ExtractTheOrderByCycle import Ui_Form

class Window(QWidget):
    def __init__(self):
        super().__init__()
        # 使用ui_Clean文件导入界面定义类
        self.ui = Ui_Form()
        self.ui.setupUi(self)  # 传入QWidget对象
        self.ui.retranslateUi(self)

        # 实例变量

        self.客户时间文件夹路径 = ''
        self.保存文件绝对路径 = ''
        self.当天日期 = ''
        self.周期天数 = '' #默认为20天
        self.temp = ''  # 用于保存打开文件的路径

        self.ui.InputButton.clicked.connect(self.getInputDir)
        self.ui.OutputButton.clicked.connect(self.getOutputDir)
        self.ui.RunButton.clicked.connect(self.handel)



    def getInputDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择客户时间文件夹路径") 
        if self.temp != '':
            self.客户时间文件夹路径 = self.temp
            self.ui.InputDir.setText(self.客户时间文件夹路径)

    def getOutputDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")  # 不使用本地对话框，可以查看文件夹内文件
        # self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")
        if self.temp != '':
            self.保存文件绝对路径 = self.temp
            self.ui.OutputDir.setText(self.保存文件绝对路径)

    def handel(self):

        # 获取输入值
        self.当天日期 = self.ui.dateEdit.text()
        self.周期天数 = self.ui.CycleDays.text()  

        # 输入值为空时
        if self.客户时间文件夹路径 == '':
            QMessageBox.about(self, "报错！", '请选择客户时间文件夹路径')
            return
        if self.保存文件绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择保存路径')
            return
        if self.当天日期 == '':
            QMessageBox.about(self, "报错！", '请输入操作人')
            return
        #处理周期天数
        if self.周期天数 == '':
            self.周期天数 = '20' #最后转成int型即可

        #不同电脑的输入当天日期格式可能不一样
        try:
            日期格式 = datetime.datetime.strptime(f'{self.当天日期}','%Y/%m/%d').strftime('%Y-%m-%d')
        except:
            日期格式 = self.当天日期

        #字符串日期先转换格式，再进行加减天数
        try:
            减去天数 = int(self.周期天数)
        except:
            QMessageBox.about(self, "报错！", '周期天数只包含数字且仅为整数！')
        
        结束日期 = datetime.datetime.strptime(日期格式,'%Y-%m-%d').date()
        开始日期 = 结束日期 + datetime.timedelta(days=-减去天数)
        walkFile(self.客户时间文件夹路径,str(开始日期),str(结束日期),self.保存文件绝对路径)
            
        QMessageBox.about(self, "处理结果", f'成功！\n请于“{self.保存文件绝对路径}”查看结果文件')

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()