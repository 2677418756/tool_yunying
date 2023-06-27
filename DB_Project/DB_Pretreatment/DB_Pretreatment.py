# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 10:33:15 2022

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


"""!!!!!!!!!!!!!!!!!!!!!!!!!!!抖音的售后表应该筛选只剩下三待一同，且使用他们的售后申请时间，申请了就当退"""

def 全合并抖音订单(订单表,售后表,账单表,运单表,联盟表,团长表):
    
    
    # print('打开成功')
    账单表 = 账单表[账单表.动账摘要.isin(['订单结算'])]
    账单表.drop('动账摘要', axis=1, inplace=True)
    运单表.rename(columns={'揽件时间':'物流时间'},inplace = True)
    #售后表只接收同意
    售后表 = 售后表[售后表.售后状态.isin(['同意退款，退款成功'])]
    
    订单表['商品单号'] = 订单表['商品单号'].astype(np.int64)
    售后表['商品单号'] = 售后表['商品单号'].astype(np.int64)
    账单表['商品单号'] = 账单表['商品单号'].astype(np.int64)

    
    data1 = pd.merge(订单表,售后表,how='left',on='商品单号')
    data1['商品单号'] = data1['商品单号'].astype(np.int64)
    # print('成功并入-售后表')
    data2 = pd.merge(data1,账单表,how='left',on='商品单号')
    data2['商品单号'] = data2['商品单号'].astype(np.int64)
    # print('成功并入-账单表')
    data3 = pd.merge(data2,联盟表,how='left',on='商品单号')
    # print('成功并入-联盟表')
    data4 = pd.merge(data3,团长表,how='left',on='商品单号')
    # print('成功并入-团长表')
    data5 = pd.merge(data4,运单表,how='left',on='订单编号')
    
    data5['实际结算金额(元)'].fillna(value=0,axis=0,inplace=True)
    data5['联盟佣金'].fillna(value=0,axis=0,inplace=True)
    data5['团长佣金'].fillna(value=0,axis=0,inplace=True)
    data5['售后状态'].fillna(value='-',axis=0,inplace=True)
    
    data5['订单编号'] = data5['订单编号'].astype(str)
    data5['商品单号'] = data5['商品单号'].astype(str)
    
    return data5
    
def 半合并抖音订单(订单表,售后表,账单表,运单表):  
    
    # print('打开成功')
    账单表 = 账单表[账单表.动账摘要.isin(['订单结算'])]
    账单表.drop('动账摘要', axis=1, inplace=True)
    运单表.rename(columns={'揽件时间':'物流时间'},inplace = True)
    #售后表只接收同意
    售后表 = 售后表[售后表.售后状态.isin(['同意退款，退款成功'])]
    
    订单表['商品单号'] = 订单表['商品单号'].astype(np.int64)
    售后表['商品单号'] = 售后表['商品单号'].astype(np.int64)
    账单表['商品单号'] = 账单表['商品单号'].astype(np.int64)
    
    data1 = pd.merge(订单表,售后表,how='left',on='商品单号')
    data1['商品单号'] = data1['商品单号'].astype(np.int64)
    # print('成功并入-售后表')
    data2 = pd.merge(data1,账单表,how='left',on='商品单号')
    data2['商品单号'] = data2['商品单号'].astype(np.int64)
    # print('成功并入-账单表')
    data3 = pd.merge(data2,运单表,how='left',on='订单编号')
    
    data3['售后状态'].fillna(value='-',axis=0,inplace=True)
    
    data3['实际结算金额(元)'].fillna(value=0,axis=0,inplace=True)    
    data3['订单编号'] = data3['订单编号'].astype(str)
    data3['商品单号'] = data3['商品单号'].astype(str)
    data3['联盟佣金'] = 0
    data3['团长佣金'] = 0
    
    return data3

def 抖音全订单状态表(union,date):

    """
    预处理模块
        #宽泛的先来处理数据：先提取每一条记录的结算时间和售后时间，把为空的时间赋值，且设置对应临时标志
    """
    union['回退状态'] = '待回'
       
    union['实际结算时间'] = pd.to_datetime(union['实际结算时间'], errors='coerce')
    union['实际结算时间'] = np.where(union.实际结算时间.notnull(),union.实际结算时间.dt.strftime('%Y-%m-%d %H:%M:%S'),'2000-01-01 00:00:00')
    union['实际结算时间'] = union['实际结算时间'].astype('datetime64[ns]')
    
    union['售后申请时间'] = pd.to_datetime(union['售后申请时间'], errors='coerce')
    union['售后申请时间'] = np.where(union.售后申请时间.notnull(),union.售后申请时间.dt.strftime('%Y-%m-%d %H:%M:%S'),'2000-01-01 00:00:00')
    union['售后申请时间'] = union['售后申请时间'].astype('datetime64[ns]')
    
    union['物流时间'] = pd.to_datetime(union['物流时间'], errors='coerce')
    union['物流时间'] = np.where(union.物流时间.notnull(),union.物流时间.dt.strftime('%Y-%m-%d %H:%M:%S'),'2000-01-01 00:00:00')
    union['物流时间'] = union['物流时间'].astype('datetime64[ns]')

    union['预估推广佣金'] = union['联盟佣金'] + union['团长佣金']

    union.drop('联盟佣金',axis = 1,inplace = True)
    union.drop('团长佣金',axis = 1,inplace = True)
    
    # 默认时间 = '2000-01-01 00:00:00'
    # print(type(date))
    统计日期 = datetime.datetime.strptime(date,'%Y-%m-%d').date()
    
    #
    有售后 = union[~(union['售后申请时间'].isin(['2000-01-01 00:00:00']))]
    无售后 = union[union['售后申请时间'].isin(['2000-01-01 00:00:00'])]
    已退 = 有售后[有售后['实际结算时间'].isin(['2000-01-01 00:00:00'])]
    回退 = 有售后[~(有售后['实际结算时间'].isin(['2000-01-01 00:00:00']))]
    已回 = 无售后[~(无售后['实际结算时间'].isin(['2000-01-01 00:00:00']))]
    待回 = 无售后[无售后['实际结算时间'].isin(['2000-01-01 00:00:00'])]
 
    回退['实际结算金额(元)'] = 回退['实际结算金额(元)'].map(lambda x : -x)
    回退['回退状态'] = '回退'
    已退['回退状态'] = '已退'
    已回['回退状态'] = '已回'
    
    frame = pd.DataFrame()
    frame1 = pd.concat([待回,已回])
    #对无售后的，有物流时间，单独提取出来再添加统计时间
    揽收可授信统计 = frame1[frame1['物流时间'].dt.date == 统计日期]
    #将昨日揽收的数据提取出来
    揽收可授信统计['统计时间'] = datetime.datetime.now()
    
    
    frame = pd.concat([frame1,已退])
    frame = pd.concat([frame,回退])
    #在终端改变名称，方便写入数据库
    frame.rename(columns={'实际结算金额(元)':'实际结算金额'},inplace = True)
    揽收可授信统计.rename(columns={'实际结算金额(元)': '实际结算金额'}, inplace=True)
    frame['统计时间'] = datetime.datetime.now()
    frame.reset_index(inplace=True,drop=True)
   
    return frame,揽收可授信统计

def 全合并快手订单(订单表,售后表,账单表,运单表):
    
    订单表['商品单号'] = 订单表['订单编号']

    运单表.rename(columns={'发货时间':'物流时间'},inplace = True)
    
    #售后表
    售后表 = 售后表[~售后表.售后状态.isin(['售后关闭'])]
    
    data1 = pd.merge(订单表,售后表,how='left',on='订单编号')

    data2 = pd.merge(data1,账单表,how='left',on='订单编号')

    data3 = pd.merge(data2,运单表,how='left',on='订单编号')
    
    data3['实际结算金额(元)'].fillna(value=0,axis=0,inplace=True) 
    data3['预估推广佣金'].fillna(value=0,axis=0,inplace=True)
    data3['售后状态'].fillna(value='-',axis=0,inplace=True)
    
    data3['订单编号'] = data3['订单编号'].astype(str)
    data3['商品单号'] = data3['商品单号'].astype(str)
    
    
    return data3

def 快手全订单状态表(union,date):
    
    """
    预处理模块
        #宽泛的先来处理数据：先提取每一条记录的结算时间和售后时间，把为空的时间赋值，且设置对应临时标志
    """
    union['回退状态'] = '待回'
       
    union['实际结算时间'] = pd.to_datetime(union['实际结算时间'], errors='coerce')
    union['实际结算时间'] = np.where(union.实际结算时间.notnull(),union.实际结算时间.dt.strftime('%Y-%m-%d %H:%M:%S'),'2000-01-01 00:00:00')
    union['实际结算时间'] = union['实际结算时间'].astype('datetime64[ns]')
    
    union['售后申请时间'] = pd.to_datetime(union['售后申请时间'], errors='coerce')
    union['售后申请时间'] = np.where(union.售后申请时间.notnull(),union.售后申请时间.dt.strftime('%Y-%m-%d %H:%M:%S'),'2000-01-01 00:00:00')
    union['售后申请时间'] = union['售后申请时间'].astype('datetime64[ns]')
    
    union['物流时间'] = pd.to_datetime(union['物流时间'], errors='coerce')
    union['物流时间'] = np.where(union.物流时间.notnull(),union.物流时间.dt.strftime('%Y-%m-%d %H:%M:%S'),'2000-01-01 00:00:00')
    union['物流时间'] = union['物流时间'].astype('datetime64[ns]')
    
    
    # 默认时间 = '2000-01-01 00:00:00'
    # print(type(date))
    统计日期 = datetime.datetime.strptime(date,'%Y-%m-%d').date()
    
    #
    有售后 = union[~(union['售后申请时间'].isin(['2000-01-01 00:00:00']))]
    无售后 = union[union['售后申请时间'].isin(['2000-01-01 00:00:00'])]
    已退 = 有售后[有售后['实际结算时间'].isin(['2000-01-01 00:00:00'])]
    回退 = 有售后[~(有售后['实际结算时间'].isin(['2000-01-01 00:00:00']))]
    已回 = 无售后[~(无售后['实际结算时间'].isin(['2000-01-01 00:00:00']))]
    待回 = 无售后[无售后['实际结算时间'].isin(['2000-01-01 00:00:00'])]

    真回退 = 回退[回退['实际结算时间']<回退['售后申请时间']]
    假回退 = 回退[回退['实际结算时间']>=回退['售后申请时间']]
    # 11.4日决定不要为负数
    # 回退['实际结算金额(元)'] = 回退['实际结算金额(元)'].map(lambda x : -x)
    真回退['回退状态'] = '回退'
    假回退['回退状态'] = '已退'
    已退['回退状态'] = '已退'
    已回['回退状态'] = '已回'


    
    frame = pd.DataFrame()
    frame1 = pd.concat([待回,已回])
    #对无售后的，有物流时间，单独提取出来再添加统计时间
    揽收可授信统计 = frame1[frame1['物流时间'].dt.date == 统计日期]
    #将昨日揽收的数据提取出来
    揽收可授信统计['统计时间'] = datetime.datetime.now()
    
    
    frame = pd.concat([frame1,已退])
    frame = pd.concat([frame,真回退])
    frame = pd.concat([frame, 假回退])
    frame.rename(columns={'实际结算金额(元)': '实际结算金额'}, inplace=True)
    揽收可授信统计.rename(columns={'实际结算金额(元)': '实际结算金额'}, inplace=True)
    frame['统计时间'] = datetime.datetime.now()
    frame.reset_index(inplace=True,drop=True)
   
    return frame,揽收可授信统计    

def 半合并淘系订单(订单表,售后表,账单表):

    # 按照主订单合并，售后时间按照循环覆盖，但需要联合订单表的售后状态来判断
    # 账单表的实际结算时间按照循环覆盖，多次用时间取出，但重点在于提取金额【需要更改更新规整】

    # 筛选出订单结算信息
    账单表 = 账单表[账单表.业务描述.isin(['0010001|交易收款-交易收款'])]
    账单表.drop('业务描述', axis=1, inplace=True)

    # 订单表的处理
    订单表.rename(columns={'发货时间': '物流时间'}, inplace=True)
    订单表 = 订单表[订单表.售后状态.isin(['没有申请退款'])|订单表.售后状态.isin(['退款关闭'])]

    data1 = pd.merge(订单表, 售后表, how='left', on='订单编号')
    # print('成功并入-售后表')
    data2 = pd.merge(data1, 账单表, how='left', on='订单编号')
    # print('成功并入-账单表')

    data2['售后状态'].fillna(value='-', axis=0, inplace=True)

    data2['实际结算金额(元)'].fillna(value=0, axis=0, inplace=True)
    data2['订单编号'] = data2['订单编号'].astype(str)
    data2['商品单号'] = data2['商品单号'].astype(str)


    return data2


from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget
from ui_DB_Pretreatment import Ui_Form

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
        self.统计揽收日期 = self.ui.dateEdit.text()  

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
        # 可以没有备注
        if self.备注 == '':
            self.备注 = '无备注'
            
        try:
            日期格式 = datetime.datetime.strptime(f'{self.统计揽收日期}','%Y/%m/%d').strftime('%Y-%m-%d')
        except:
            日期格式 = self.统计揽收日期
            
        # 每一个平台都有订单表
        需打开表格名列表 = ['订单表','团长表','联盟表','售后表','账单表','运单表'] 
        # 实例化对象,调用方法
        自动提取文件 = AutoExtractFiles(self.清洗后文件夹路径,需打开表格名列表)
        需打开表格字典 = 自动提取文件.handle() #['订单表'：对应文件路径]
        print(需打开表格字典)
        文件名 = os.path.basename(需打开表格字典['订单表']) # loose-天猫-账单表-清洗后.xlsx
        文件名前缀 = os.path.splitext(文件名)[0] # loose-天猫-账单表-清洗后
        平台类型 = 文件名前缀.split('-')[1] # loose-【天猫】-账单表-清洗后
        客户名称 = 文件名前缀.split('-')[0] # 【loose】-天猫-账单表-清洗后


        if 平台类型 == '抖音' :
            for k,v in 需打开表格字典.items():
                if k == '订单表':
                    订单表 = pd.read_excel(v,usecols=['订单编号','商品单号','成交数量','订单应付金额','订单创建时间','订单状态','商家编码','商品名称'])
                elif k == '团长表':
                    团长表 = pd.read_excel(v,usecols=['商品单号','团长佣金'])
                elif k == '联盟表':
                    联盟表 = pd.read_excel(v,usecols=['商品单号','联盟佣金'])
                elif k == '售后表':
                    售后表 = pd.read_excel(v,usecols=['商品单号','售后状态','售后申请时间'])
                elif k == '账单表':
                    账单表 = pd.read_excel(v,usecols=['商品单号','实际结算时间','动账摘要','实际结算金额(元)'])
                elif k == '运单表':
                    运单表 = pd.read_excel(v,usecols=['订单编号','揽件时间'])
            try:
                合并1 = 全合并抖音订单(订单表,售后表,账单表,运单表,联盟表,团长表)
                订单全状态表, 已揽收订单表 = 抖音全订单状态表(合并1, 日期格式)
            except:
                合并2 = 半合并抖音订单(订单表,售后表,账单表,运单表)
                订单全状态表, 已揽收订单表 = 抖音全订单状态表(合并2, 日期格式)



                    
        elif 平台类型 == '快手' :
            
            for k,v in 需打开表格字典.items():
                if k == '订单表':
                    订单表 = pd.read_excel(v,usecols=['订单编号','成交数量','订单应付金额','订单创建时间','订单状态','预估推广佣金','商家编码','商品名称'])
                elif k == '售后表':
                    售后表 = pd.read_excel(v,usecols=['订单编号','售后状态','售后申请时间'])
                elif k == '账单表':
                    账单表 = pd.read_excel(v,usecols=['订单编号','实际结算时间','实际结算金额(元)'])
                elif k == '运单表':
                    运单表 = pd.read_excel(v,usecols=['订单编号','发货时间'])

            合并 = 全合并快手订单(订单表,售后表,账单表,运单表)

            订单全状态表,已揽收订单表 = 快手全订单状态表(合并,日期格式)
            
        else :
            QMessageBox.about(self, "报错！", "命名格式错误：平台类型")
            return
        订单全状态表 = 订单全状态表.loc[:,['订单编号','商品单号','商家编码','商品名称','成交数量','订单应付金额','订单创建时间','订单状态','售后状态','售后申请时间','实际结算时间','实际结算金额','预估推广佣金','物流时间','回退状态','统计时间']]
        已揽收订单表 = 已揽收订单表.loc[:,['订单编号','商品单号','商家编码','商品名称','成交数量','订单应付金额','订单创建时间','订单状态','售后状态','售后申请时间','实际结算时间','实际结算金额','预估推广佣金','物流时间','回退状态','统计时间']]
        输出文件名格式 = f'\\{客户名称}-{平台类型}-订单状态表-{self.操作人}-统计揽收{日期格式}.xlsx'
        输出路径 = self.保存文件绝对路径 + 输出文件名格式

        #——————————————————————————————————————————————————————————————————打开与保存模块
        writer = pd.ExcelWriter(输出路径)
        订单全状态表.to_excel(writer, sheet_name='订单全状态表',index=False)

        已揽收订单表.to_excel(writer, sheet_name='已揽收订单表',index=False)

        writer.save()
        #不用删掉，不然文件短时间内不能编辑，只能读取
        writer.close()
        # 订单状态表.to_excel(输出路径,index=False)#因为订单创建日期变成INDEX了

        QMessageBox.about(self, "处理结果", f'成功！\n请于“{self.保存文件绝对路径}”查看结果文件')

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()















