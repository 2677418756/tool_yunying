# -*- coding: utf-8 -*-
"""
Created on Tue May 17 18:04:03 2022

@author: Admin
"""



import pandas as pd
import datetime as datetime
import os
import os.path
from PySide2.QtWidgets import QMessageBox

def read_more_sheets(path):
  data_xlsx = pd.io.excel.ExcelFile(path)
  data={}
  # print(data_xlsx.sheet_names)
  for name in data_xlsx.sheet_names:
    df=pd.read_excel(data_xlsx,sheet_name=name,header=0)#【重要！】这里header=0指用第0行作为列索引，如果index_cols=0则是第0列作为行索引
    data[name]=df
  return data #返回字典的形式

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

def one_decimal(x_data):
    #【浮点数先转字符串，再转浮点数】让数据保留一位小数，且自动四舍五入
    x_str = '%.1f' % x_data #变成字符串来保留一位小数了
    return float(x_str)

def 特殊回款模块(剩余金额表,特殊回款表,当天自然日字符串,客户名称):
    
    
    当天自然日 = datetime.datetime.strptime(当天自然日字符串,'%Y-%m-%d').date()
    特殊回款表['订单创建日期'] = 特殊回款表['订单创建日期'].map(timestamp_to_date)
    剩余金额表['订单创建日期'] = 剩余金额表['订单创建日期'].map(timestamp_to_date)
    try:
        剩余金额表['理论结算日期'] = 剩余金额表['理论结算日期'].map(timestamp_to_date)
    except(AttributeError):
        #若没有已结算场次，则可能跳转到此语句
        pass
    # 剩余金额表['理论结算日期'] = 剩余金额表['理论结算日期'].map(timestamp_to_date)
    #相当于强制结算，结算标志为否，但需要记录三种值
    需特殊回款表 = 特殊回款表[(特殊回款表['是否本次特殊回款'] == '是')]
    特殊回款列表 = 需特殊回款表[['订单创建日期','授信代码']].to_dict('split')
    
    店铺费率百分比字典 = {'FOLA旗舰店':{'2022-03-01':0.048,'2022-08-01':0.04},
       'XINGDAO STYLE':{'2022-03-01':0.048,'2022-08-01':0.04},'YIWEINUO':{'2022-08-20':0.04}}

    #用最蠢的方法    
    for k,v in 店铺费率百分比字典.items():
        #v是一个字典，如{'2022-08-01':0.048}
        if k == 客户名称:       
            本次计费字典 = v
            
    #创建特殊账单明细表
    特殊账单明细表 = pd.DataFrame()
    #需要计算特殊回款的金额，等于本次剩余金额
    for pair in 特殊回款列表['data']: # pair是列表[datetime.date(2022, 6, 7), 1]

        特殊场次日期 = pair[0]
        特殊授信代码 = pair[1]
        temp_time0 = 当天自然日 - 特殊场次日期 
        天数 = temp_time0.days + 1
        final_dataframe0 = 剩余金额表[(剩余金额表['订单创建日期'] == 特殊场次日期)&(剩余金额表['授信代码'] == 特殊授信代码)]
           
        #——————提取其他相关信息
        服务方0 = final_dataframe0.iloc[0].at['服务方']
        资金方式0 = final_dataframe0.iloc[0].at['资金方式']
        授信代码0 =  特殊授信代码      
     
        #——————提取其他相关信息
        
        
        #直接提取已更新的剩余金额表中，今日应统计且已经统计金额作为特殊回款金额，并将其填充为0
        本次已统计金额 = final_dataframe0.iloc[0].at[f'第{天数}天']
        需特殊回款金额 = 本次已统计金额
        剩余金额表.loc[剩余金额表['授信代码'].isin([特殊授信代码])&剩余金额表['订单创建日期'].isin([特殊场次日期]),f'第{天数}天'] = 0.0
        final_dataframe0.loc[:,f'第{天数}天'] = 0.0 #将该单条记录的对应第N天，再提取需要的数据之后，设置为0
        
        #计算总服务费，并写出结算方式为 特殊结算，并将本场次的结算标志设为 是
        使用天数求和0 = 0
        for num in range(1,41):
            使用天数求和0 = 使用天数求和0 + final_dataframe0.iloc[0].at[f'第{num}天']

        总计授信0 = final_dataframe0.iloc[0].at['总计授信']
        #【金融计算模块】
        中间记录差值 = -1
        for k,v in 本次计费字典.items():
            #k为字符串日期，v为费率
            #用当前日期 - 字典提取日期比较，只选择使用比值大于零且最小的那个参数
            使用场次日期 = datetime.datetime.strptime(k,'%Y-%m-%d').date()
            if (特殊场次日期 - 使用场次日期).days >= 0:
                差值 = (特殊场次日期 - 使用场次日期).days
                if 差值 < 中间记录差值 or 中间记录差值 < 0:
                    中间记录差值 = 差值
                    约定费率 = v/30
        # 约定费率 = 0.0016
        垫资费率 = 0.01/30
        理论费用 = round((总计授信0 + 使用天数求和0)*约定费率,2)
        垫资费用 = round((总计授信0 + 使用天数求和0)*垫资费率,2) #只有往来有，所以只写往来里    
        
        
        剩余金额表.loc[剩余金额表['授信代码'].isin([特殊授信代码])&剩余金额表['订单创建日期'].isin([特殊场次日期]),'是否结算'] = '是'
        剩余金额表.loc[剩余金额表['授信代码'].isin([特殊授信代码])&剩余金额表['订单创建日期'].isin([特殊场次日期]),'结算方式'] = '特殊结算'
        剩余金额表.loc[剩余金额表['授信代码'].isin([特殊授信代码])&剩余金额表['订单创建日期'].isin([特殊场次日期]),'理论结算日期'] = 当天自然日
        剩余金额表.loc[剩余金额表['授信代码'].isin([特殊授信代码])&剩余金额表['订单创建日期'].isin([特殊场次日期]),'理论应收服务费'] = float(理论费用)
        
        if 资金方式0 == '货款':
            货款利润 = round(总计授信0*0.01,2)
            剩余金额表.loc[剩余金额表['授信代码'].isin([授信代码0])&剩余金额表['订单创建日期'].isin([特殊场次日期]),'贸易尾款'] = 货款利润
            #小于，则在返利处写入，大于则在服务费中写入
            差额 = 理论费用 - 货款利润
            if 差额 >= 0:
                #写总计费表
                剩余金额表.loc[剩余金额表['授信代码'].isin([授信代码0])&剩余金额表['订单创建日期'].isin([特殊场次日期]),'运营服务费'] = 差额
                剩余金额表.loc[剩余金额表['授信代码'].isin([授信代码0])&剩余金额表['订单创建日期'].isin([特殊场次日期]),'贸易返利'] = 0.00
                
            elif 差额 < 0:

                剩余金额表.loc[剩余金额表['授信代码'].isin([授信代码0])&剩余金额表['订单创建日期'].isin([特殊场次日期]),'贸易返利'] = abs(差额)
                剩余金额表.loc[剩余金额表['授信代码'].isin([授信代码0])&剩余金额表['订单创建日期'].isin([特殊场次日期]),'运营服务费'] = 0.00         
                
        elif 资金方式0 == '往来款':
            
            运营往来费用 = 理论费用 - 垫资费用
            剩余金额表.loc[剩余金额表['授信代码'].isin([授信代码0])&剩余金额表['订单创建日期'].isin([特殊场次日期]),'运营服务费'] = 运营往来费用
            剩余金额表.loc[剩余金额表['授信代码'].isin([授信代码0])&剩余金额表['订单创建日期'].isin([特殊场次日期]),'垫资服务费'] = 垫资费用

        #【每一个for场次循环写入一次】提前写账单明细表
        明细字典1 = {}
        明细字典1['订单创建日期'] = 特殊场次日期
        明细字典1['特殊回款'] = 需特殊回款金额
        明细字典1['运营服务费'] = 0.00
        明细字典1['垫资服务费'] = 0.00
        明细字典1['贸易尾款'] = 0.00
        明细字典1['服务方'] = 服务方0
        明细字典1['资金方式'] = 资金方式0
        明细字典1['授信代码'] = 授信代码0
        #数据格式转换
        某一天明细 = pd.Series(明细字典1)
        某一天明细.name = 特殊场次日期
        #不断合并统计好的日期
        特殊账单明细表 = 特殊账单明细表.append(某一天明细)
    特殊账单明细表.index.name='订单创建日期'
    #改变列的序列
    特殊账单明细表 = 特殊账单明细表.loc[:,['订单创建日期','服务方','资金方式','授信代码','特殊回款','运营服务费','垫资服务费','贸易尾款']]
    
    #修改特殊回款表
    for pair in 特殊回款列表['data']: # pair是列表[datetime.date(2022, 6, 7), 1]
        场次日期1 = pair[0]
        授信代码1 = pair[1]
        #读取数据使用切片后再读取的方法，写数据直接在源数据写入
        #先切片，再读取数据
        final_dataframe1 = 剩余金额表[(剩余金额表['订单创建日期'] == 场次日期1)&(剩余金额表['授信代码'] == 授信代码1)]
        特殊回款表.loc[特殊回款表['订单创建日期'].isin([场次日期1])&特殊回款表['授信代码'].isin([授信代码1]),'特殊日期'] = 当天自然日
        特殊回款表.loc[特殊回款表['订单创建日期'].isin([场次日期1])&特殊回款表['授信代码'].isin([授信代码1]),'是否本次特殊回款'] = '否'
        
        #读取相关数据
        资金方式1 = final_dataframe1.iloc[0].at['资金方式']
        理论费用1 = final_dataframe1.iloc[0].at['理论应收服务费']

        if 资金方式1 == '货款':
            
            货款利润1 = final_dataframe1.iloc[0].at['贸易尾款']
            特殊账单明细表.loc[特殊账单明细表['订单创建日期'].isin([场次日期1])&特殊账单明细表['授信代码'].isin([授信代码1]),'贸易尾款'] = 货款利润1
            差额1 = 理论费用1 - 货款利润1
            if 差额1 >= 0:
                #写账单明细表
                特殊账单明细表.loc[特殊账单明细表['订单创建日期'].isin([场次日期1])&特殊账单明细表['授信代码'].isin([授信代码1]),'运营服务费'] = 差额1
                
            elif 差额1 < 0:
                #写账单明细表
                #账单明细中的运营服务费本来就是0.0
                pass                
                
        elif 资金方式1 == '往来款':
            垫资费用1 = final_dataframe1.iloc[0].at['垫资服务费']
            运营往来费用1 = 理论费用1 - 垫资费用1
            特殊账单明细表.loc[特殊账单明细表['订单创建日期'].isin([场次日期1])&特殊账单明细表['授信代码'].isin([授信代码1]),'运营服务费'] = float(运营往来费用1)
            特殊账单明细表.loc[特殊账单明细表['订单创建日期'].isin([场次日期1])&特殊账单明细表['授信代码'].isin([授信代码1]),'垫资服务费'] = 垫资费用1
            
    return 特殊回款表,剩余金额表,特殊账单明细表

class Maintain:

    def __init__(self, orderpath, inputdir, outputdir, user, date):
        #————————————————————————————————————————————————————————————————————用户输入模块
        self.M_今日计费表文件绝对路径 = orderpath
        self.M_特殊回款表绝对路径 = inputdir
        self.M_输出至文件夹 = outputdir
        self.M_操作人 = user
        self.M_当天日期 = date  # r'2022-02-12' #本质是订单创建日期 格式：2022-01-30          
        #————————————————————————————————————————————————————————————————————用户输入模块


    def maintain(self, Form):
        
        #数据预处理
        try:
            #可能在别的电脑上，会导致这样
            日期格式 = datetime.datetime.strptime(f'{self.M_当天日期}','%Y/%m/%d').strftime('%Y-%m-%d')
        except:
            日期格式 = self.M_当天日期
                
        #分解传入进来的路径self.M_今日计费表文件绝对路径，获取对应名字
        文件名 = os.path.basename(self.M_今日计费表文件绝对路径) # FOLA旗舰店-抖音-退货退款表-CJY-2022-05-14.xlsx
        文件名前缀 = os.path.splitext(文件名)[0] # FOLA旗舰店-抖音-退货退款表-CJY-2022-05-14
        平台类型 = 文件名前缀.split('-')[1] # FOLA旗舰店-【抖音】-退货退款表-CJY-2022-05-14
        客户名称 = 文件名前缀.split('-')[0] # 【FOLA旗舰店】-抖音-退货退款表-CJY-2022-05-14
        
        #打开需要的表格
        今日剩余金额表字典 = read_more_sheets(self.M_今日计费表文件绝对路径)
        特殊回款表 = pd.read_excel(self.M_特殊回款表绝对路径)
        
        #【例子】FOLA旗舰店-抖音-剩余金额表-2022-05-14
        输出文件名格式 = f'\\{客户名称}-{平台类型}-计费表(特)-{日期格式}-{self.M_操作人}.xlsx'
        特殊回款文件名格式 = f'\\{客户名称}-{平台类型}-特殊回款表.xlsx'
        输出路径 = self.M_输出至文件夹 + 输出文件名格式
        特殊回款路径 = self.M_输出至文件夹 + 特殊回款文件名格式
        
        变化特殊回款表,已维护剩余金额表,特殊账单明细表 = 特殊回款模块(今日剩余金额表字典[f'{日期格式}剩余金额表'],特殊回款表,日期格式,客户名称)
        
        
        变化特殊回款表.to_excel(特殊回款路径,index=False)
        #【writer】使用writer将dataframe放入不同的excel的sheet中
        #使用pd.ExcelWriter
        writer = pd.ExcelWriter(输出路径)
        已维护剩余金额表.to_excel(writer, sheet_name=f'{日期格式}剩余金额表',index=False)
        今日剩余金额表字典[f'{日期格式}账单明细表'].to_excel(writer, sheet_name=f'{日期格式}账单明细表',index=False)
        特殊账单明细表.to_excel(writer, sheet_name=f'{日期格式}特殊回款明细表',index=False)
        writer.save()
        #不用删掉，不然文件短时间内不能编辑，只能读取
        writer.close()

        #成功后消息提醒
        QMessageBox.about(Form, "处理结果", f'成功！\n请于“{self.M_输出至文件夹}”查看结果文件')