# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 17:24:28 2022

@author: Admin
"""

import pandas as pd
import numpy as np
import datetime as datetime
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

def 函数_提取日期(去重后,字符串日期):
    近20天日期列表 = []
    for 日期 in 去重后.loc[:,f'{字符串日期}']:
        近20天日期列表.append(日期)
    return 近20天日期列表

def 函数_计算日期差值(传入日期,对应日期列表):
    
    存放空间 = []
    创建日期 = datetime.datetime.strptime(传入日期,'%Y-%m-%d')
    for 对应日期 in 对应日期列表 :
        
        申请日期 = datetime.datetime.strptime(对应日期,'%Y-%m-%d')
        
        差值 = 申请日期 - 创建日期
        # print('申请日期%s'%申请日期,'创建日期%s'%创建日期)
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

#采用订单表与售后表的数据，最后结合成本表数据
#字段使用：订单创建日期，售后创建日期，成本价

def CostOfGoods(Order,Cost):

    # #防止表格读取后再写入相关字段乱码
    # Order['订单编号'] = Order['订单编号'].astype(str)
    # Order['商品单号'] = Order['商品单号'].astype(str)

    # 先精炼出订单创建日期
    Order['统计标志'] = '失败'
    # Order['批次标志'] = '失败'
    Order['统计成本价'] = round(Order['订单应付金额']/Order['成交数量'] * 0.4,2)
    # Order['批次成本价'] = round(Order['订单应付金额'] * 0.5,2)
    try:
        Order['订单创建日期'] = Order['订单创建日期'].map(timestamp_to_date)
    except:
        pass
    try:
        Order['订单创建日期'] = Order['订单创建日期'].map(str_to_date)
    except:
        pass
    try:
        Cost['统计日期'] = Cost['统计日期'].map(timestamp_to_date)
    except:
        pass
    try:
        Cost['统计日期'] = Cost['统计日期'].map(str_to_date)
    except:
        pass
    need_drop = Order.duplicated('订单创建日期') #返回与检测列相同长度的布尔类型Series，来反应某列中的重复值
    order_only = Order[~need_drop]
    orderDate = order_only['订单创建日期']

    orderDateList = orderDate.tolist()

    for date in orderDateList:
        """
        思路：第一个循环 —— 按订单创建日期切片
            第二个循环 —— 再按匹配编号切片
        """
        #提取同一订单创建日期下的唯一商家编码  
        temp_order = Order[Order['订单创建日期'].isin([date])] #返回类型：dataframe
        temp_need_drop = temp_order.duplicated('匹配编号') #返回类型：dataframe
        temp_order_only = temp_order[~temp_need_drop] #返回类型：dataframe
        orderBusinessCode = temp_order_only['匹配编号'] #返回类型：series
    
        for code in orderBusinessCode:
            #先切片匹配编号，再条件对比批次日期与统计日期

            temp_cost_use = Cost[Cost['匹配编号'].isin([code])]

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
                    Order.loc[Order['订单创建日期'].isin([date])&Order['匹配编号'].isin([code]),'统计成本价'] = use_price
                    Order.loc[Order['订单创建日期'].isin([date])&Order['匹配编号'].isin([code]),'统计标志'] = '成功'
                    break
            
    Order['统计成本总价'] = Order['统计成本价'] * Order['成交数量']
    # Order['批次成本总价'] = Order['批次成本价'] * Order['成交数量']
    return Order


def 抖音可回溯型退货退款表(订单表输入,售后表输入,成本表输入,当天日期):

    订单表输入['订单编号'] = 订单表输入['订单编号'].astype(str)
    订单表输入['商品单号'] = 订单表输入['商品单号'].astype(str)
    订单表输入['商家编码'] = 订单表输入['商家编码'].astype(str)
    订单表输入['匹配编号'] = 订单表输入['商家编码']

    当天日期 = datetime.datetime.strptime(当天日期,'%Y-%m-%d').date()
   
    订单货物成本表 = CostOfGoods(订单表输入,成本表输入)
    
    售后表输入 = 售后表输入[~(售后表输入.售后申请日期.isin([f'{当天日期}']))]
    
    
    售后表输入['商品单号'] = 售后表输入['商品单号'].astype(str)
    
    V2 = pd.merge(订单货物成本表,售后表输入,how= 'left', left_on = '商品单号',right_on = '商品单号') 
    #数据格式转换
    # print(type(V2.loc[5,'订单创建日期']))
    V2['订单创建日期'] = pd.to_datetime(V2['订单创建日期'], errors='coerce')
    V2['订单创建日期'] = V2['订单创建日期'].dt.date
    V2['订单创建日期'] = V2['订单创建日期'].astype(str)
    # V2['售后申请日期'] = V2['售后申请日期'].dt.date
    # V2['售后申请日期'] = V2['售后申请日期'].astype(str)
    V2['售后申请日期'] = pd.to_datetime(V2['售后申请日期'], errors='coerce')
    #【重要】将订单表VLOOKUP售后表中匹配不上的NA值改为2000-01-01
    V2['售后申请日期'] = np.where(V2.售后申请日期.notnull(),V2.售后申请日期.dt.strftime('%Y-%m-%d'),'2000-01-01') #售后申请日期 - 订单创建日期 为负数，不会影响
    # V2['总成本价'] = V2['成本价'] * V2['成交数量']
    #【用于合并】用于逐条存放结果—————————————————————————————————————————————————————双日期、价格输入模块
    用于合并 = pd.DataFrame()
    提取 = V2.copy()
    去重 = V2.copy()
    去重 = 去重.drop_duplicates('订单创建日期')
    横切用N列表 = 函数_提取日期(去重,'订单创建日期')
    #排序，从小到大
    横切用N列表.sort()
    
    for 订单创建日期 in 横切用N列表:
        #提取某一天执行操作
        横切表 = 提取[(提取['订单创建日期'] == 订单创建日期)]
        #获取同一个订单日期有几个售后申请日期
        获取 = 横切表.copy()
        #去除重复的售后申请日期
        获取 = 获取.drop_duplicates('售后申请日期')
        #将实际结算日期提取出来，返回形式为列表
        对应售后申请日期日期列表 = 函数_提取日期(获取,'售后申请日期')
        #再用每一个售后申请日期减去订单日期，得到一组整数
        数字列表 = 函数_计算日期差值(订单创建日期,对应售后申请日期日期列表)
        #补0，用于接收剩余GMV，例如：从[-8133, 1, 2, 3, 4, 5, 6, 8, 9, 11]变成[-8133,0, 1, 2, 3, 4, 5, 6, 8, 9, 11]，抛弃负数，0为场次剩余金额，1为第1天，如此类推
        数字列表.insert(0,0) 
        #【数据透析表】
        横切透析 = pd.pivot_table(横切表,index=['订单创建日期'],columns=['售后申请日期'],values=['统计成本总价'],aggfunc = [np.sum])
        #去除表头sum
        横切透析.columns = 横切透析.columns.droplevel(0)
        #创造字典，最后再修改字典
        明细字典1 = {f'第{i}天': 0.0 for i in range(90)}
        #防止 for 天数 in 数字列表 : 循环中 求和值 = 横切透析.iloc[0,计数] 的数组越界，属于小概率情况
        全退对齐 = 0
        if sum(数字列表) > 0 :
            数字列表.insert(0, -1) #只能在最开头的列表处添加负数，不然会导致循环中逻辑出错   
            print('当天销售全退')
            全退对齐 =  1 #当且仅当一个场次全部退货退款时，才会列表中没有负数，需要补负数，然后进行对齐
        #计数用于循环的过程中向右读取数据，从0开始意味着读取NA（剩余GMV），从1开始意味对应第1天读取
        计数 = 0
        for 天数 in 数字列表 :
            #在字典处定位需修改的地方，修改值为透析表中已经求和好的部分
            if 天数 >= 0 :
                求和值 = 横切透析.iloc[0,计数]
                计数 = 计数 + 1 - 全退对齐
                全退对齐 = 0
                明细字典1[f'第{天数}天'] = one_decimal(求和值)
                  
        某一天明细 = pd.Series(明细字典1)
        某一天明细.name = 订单创建日期
        #不断合并统计好的日期
        用于合并 = 用于合并.append(某一天明细)
    用于列顺序维护 = list(明细字典1)
    用于合并 = 用于合并.loc[:,用于列顺序维护]
    用于合并.rename(columns={'第0天':'场次剩余成本'},inplace = True)
    
    用于合并['场次总成本统计'] = 用于合并.apply(lambda x: x.sum(), axis=1) # 按行求和，添加为新列
    用于合并.insert(0, '场次总成本', 用于合并['场次总成本统计'])
    用于合并.drop(['场次总成本统计'],axis= 1,inplace=True)
    用于合并.index.name="订单创建日期"
    
    """
    下段代码X用于给运营统计哪些订单没有匹配成功
    """
    #将统计标志为成功的删除掉即可
    运营使用统计 = 订单货物成本表[订单货物成本表['统计标志'].isin(['失败'])]
    # 运营使用统计.drop(['订单创建时间','订单状态','售后状态','订单编号','商品单号'],axis=1,inplace=True)
    运营使用统计 = 运营使用统计.loc[:,['商品名称','成交数量','统计标志','匹配编号','订单创建日期']]

    
    return 用于合并,运营使用统计

def 快手可回溯型退货退款表(订单表输入,售后表输入,成本表输入,当天日期):
    
    订单表输入['订单编号'] = 订单表输入['订单编号'].astype(str)
    订单表输入['商品ID'] = 订单表输入['商品ID'].astype(str)
    订单表输入['匹配编号'] = 订单表输入['商品ID']

    当天日期 = datetime.datetime.strptime(当天日期,'%Y-%m-%d').date()
    
    售后表输入 = 售后表输入[~(售后表输入.售后申请日期.isin([f'{当天日期}']))]
    
    订单货物成本表 = CostOfGoods(订单表输入,成本表输入)
    
    售后表输入['订单编号'] = 售后表输入['订单编号'].astype(str)
    # V = pd.merge(订单表输入,售后表输入,how= 'left', on = '订单编号')   
    V2 = pd.merge(订单货物成本表,售后表输入,how= 'left', left_on = '订单编号',right_on = '订单编号') 
    #数据格式转换
    # print(type(V2.loc[5,'订单创建日期']))
    V2['订单创建日期'] = pd.to_datetime(V2['订单创建日期'], errors='coerce')
    V2['订单创建日期'] = V2['订单创建日期'].dt.date
    V2['订单创建日期'] = V2['订单创建日期'].astype(str)
    # V2['售后申请日期'] = V2['售后申请日期'].dt.date
    # V2['售后申请日期'] = V2['售后申请日期'].astype(str)
    V2['售后申请日期'] = pd.to_datetime(V2['售后申请日期'], errors='coerce')
    #【重要】将订单表VLOOKUP售后表中匹配不上的NA值改为2000-01-01
    V2['售后申请日期'] = np.where(V2.售后申请日期.notnull(),V2.售后申请日期.dt.strftime('%Y-%m-%d'),'2000-01-01') #售后申请日期 - 订单创建日期 为负数，不会影响
    # V2['总成本价'] = V2['成本价'] * V2['成交数量']
    #【用于合并】用于逐条存放结果—————————————————————————————————————————————————————双日期、价格输入模块
    用于合并 = pd.DataFrame()
    提取 = V2.copy()
    去重 = V2.copy()
    去重 = 去重.drop_duplicates('订单创建日期')
    横切用N列表 = 函数_提取日期(去重,'订单创建日期')
    #排序，从小到大
    横切用N列表.sort()
    
    for 订单创建日期 in 横切用N列表:
        #提取某一天执行操作
        横切表 = 提取[(提取['订单创建日期'] == 订单创建日期)]
        #获取同一个订单日期有几个售后申请日期
        获取 = 横切表.copy()
        #去除重复的售后申请日期
        获取 = 获取.drop_duplicates('售后申请日期')
        #将实际结算日期提取出来，返回形式为列表
        对应售后申请日期日期列表 = 函数_提取日期(获取,'售后申请日期')
        #再用每一个售后申请日期减去订单日期，得到一组整数
        数字列表 = 函数_计算日期差值(订单创建日期,对应售后申请日期日期列表)
        #补0，用于接收剩余GMV，例如：从[-8133, 1, 2, 3, 4, 5, 6, 8, 9, 11]变成[0,-8133, 1, 2, 3, 4, 5, 6, 8, 9, 11]，抛弃负数，0为场次剩余金额，1为第1天，如此类推
        数字列表.insert(0,0) 
        #【数据透析表】
        横切透析 = pd.pivot_table(横切表,index=['订单创建日期'],columns=['售后申请日期'],values=['统计成本总价'],aggfunc = [np.sum])
        #去除表头sum
        横切透析.columns = 横切透析.columns.droplevel(0)
        #创造字典，最后再修改字典
        明细字典1 = {f'第{i}天': 0.0 for i in range(90)}
        #防止 for 天数 in 数字列表 : 循环中 求和值 = 横切透析.iloc[0,计数] 的数组越界，属于小概率情况
        全退对齐 = 0
        if sum(数字列表) > 0 :
            数字列表.insert(0, -1) #只能在最开头的列表处添加负数，不然会导致循环中逻辑出错   
            print('当天销售全退')
            全退对齐 =  1 #当且仅当一个场次全部退货退款时，才会列表中没有负数，需要补负数，然后进行对齐
        #计数用于循环的过程中向右读取数据，从0开始意味着读取NA（剩余GMV），从1开始意味对应第1天读取
        # print(数字列表)
        计数 = 0
        for 天数 in 数字列表 :
            # print('天数%s'%天数)       

            #在字典处定位需修改的地方，修改值为透析表中已经求和好的部分
            if 天数 >= 0 :
                求和值 = 横切透析.iloc[0,计数]
                # print('计数%s'%计数)
                计数 = 计数 + 1 - 全退对齐  
                全退对齐 = 0
                明细字典1[f'第{天数}天'] = one_decimal(求和值)
                  
        某一天明细 = pd.Series(明细字典1)
        某一天明细.name = 订单创建日期
        #不断合并统计好的日期
        用于合并 = 用于合并.append(某一天明细)
    用于列顺序维护 = list(明细字典1)
    用于合并 = 用于合并.loc[:,用于列顺序维护]
    用于合并.rename(columns={'第0天':'场次剩余成本'},inplace = True)
    
    用于合并['场次总成本统计'] = 用于合并.apply(lambda x: x.sum(), axis=1) # 按行求和，添加为新列
    用于合并.insert(0, '场次总成本', 用于合并['场次总成本统计'])
    用于合并.drop(['场次总成本统计'],axis= 1,inplace=True)
    用于合并.index.name="订单创建日期"
    
    """
    下段代码X用于给运营统计哪些订单没有匹配成功
    """
    #将统计标志为成功的删除掉即可
    运营使用统计 = 订单货物成本表[订单货物成本表['统计标志'].isin(['失败'])]
    运营使用统计 = 运营使用统计.loc[:,['商品名称','成交数量','统计标志','匹配编号','订单创建日期']]


    
    return 用于合并,运营使用统计

def 天猫可回溯型退货退款表(宝贝表输入,售后表输入,成本表输入,当天日期):
    
    合并 = pd.merge(宝贝表输入,售后表输入,on = '订单编号',how = 'inner')
    合并['订单编号'] = 合并['订单编号'].astype(str)
    合并['商品编号'] = 合并['商品编号'].astype(str)
    #一定要排重，才符合真实情况
    合并 = 合并.drop_duplicates('商品编号')
    
    合并['匹配编号'] = 合并['商家编码']

    当天日期 = datetime.datetime.strptime(当天日期,'%Y-%m-%d').date()
    
    # 售后表输入 = 售后表输入[~(售后表输入.售后申请日期.isin([f'{当天日期}']))]
    
    订单货物成本表 = CostOfGoods(合并,成本表输入)
    V2 = 订单货物成本表
    # 售后表输入['订单编号'] = 售后表输入['订单编号'].astype(str)
    # V = pd.merge(订单表输入,售后表输入,how= 'left', on = '订单编号')   
    # V2 = pd.merge(订单货物成本表,售后表输入,how= 'left', left_on = '订单编号',right_on = '订单编号') 
    #数据格式转换
    # print(type(V2.loc[5,'订单创建日期']))
    V2['订单创建日期'] = pd.to_datetime(V2['订单创建日期'], errors='coerce')
    V2['订单创建日期'] = V2['订单创建日期'].dt.date
    V2['订单创建日期'] = V2['订单创建日期'].astype(str)
    # V2['售后申请日期'] = V2['售后申请日期'].dt.date
    # V2['售后申请日期'] = V2['售后申请日期'].astype(str)
    V2['售后申请日期'] = pd.to_datetime(V2['售后申请日期'], errors='coerce')
    #【重要】将订单表VLOOKUP售后表中匹配不上的NA值改为2000-01-01
    V2['售后申请日期'] = np.where(V2.售后申请日期.notnull(),V2.售后申请日期.dt.strftime('%Y-%m-%d'),'2000-01-01') #售后申请日期 - 订单创建日期 为负数，不会影响
    # V2['总成本价'] = V2['成本价'] * V2['成交数量']
    #【用于合并】用于逐条存放结果—————————————————————————————————————————————————————双日期、价格输入模块
    用于合并 = pd.DataFrame()
    提取 = V2.copy()
    去重 = V2.copy()
    去重 = 去重.drop_duplicates('订单创建日期')
    横切用N列表 = 函数_提取日期(去重,'订单创建日期')
    #排序，从小到大
    横切用N列表.sort()
    
    for 订单创建日期 in 横切用N列表:
        #提取某一天执行操作
        横切表 = 提取[(提取['订单创建日期'] == 订单创建日期)]
        #获取同一个订单日期有几个售后申请日期
        获取 = 横切表.copy()
        #去除重复的售后申请日期
        获取 = 获取.drop_duplicates('售后申请日期')
        #将实际结算日期提取出来，返回形式为列表
        对应售后申请日期日期列表 = 函数_提取日期(获取,'售后申请日期')
        #再用每一个售后申请日期减去订单日期，得到一组整数
        数字列表 = 函数_计算日期差值(订单创建日期,对应售后申请日期日期列表)
        #补0，用于接收剩余GMV，例如：从[-8133, 1, 2, 3, 4, 5, 6, 8, 9, 11]变成[0,-8133, 1, 2, 3, 4, 5, 6, 8, 9, 11]，抛弃负数，0为场次剩余金额，1为第1天，如此类推
        数字列表.insert(0,0) 
        #【数据透析表】
        横切透析 = pd.pivot_table(横切表,index=['订单创建日期'],columns=['售后申请日期'],values=['统计成本总价'],aggfunc = [np.sum])
        #去除表头sum
        横切透析.columns = 横切透析.columns.droplevel(0)
        #创造字典，最后再修改字典
        明细字典1 = {f'第{i}天': 0.0 for i in range(90)}
        #防止 for 天数 in 数字列表 : 循环中 求和值 = 横切透析.iloc[0,计数] 的数组越界，属于小概率情况
        全退对齐 = 0
        if sum(数字列表) > 0 :
            数字列表.insert(0, -1) #只能在最开头的列表处添加负数，不然会导致循环中逻辑出错   
            print('当天销售全退')
            全退对齐 =  1 #当且仅当一个场次全部退货退款时，才会列表中没有负数，需要补负数，然后进行对齐
        #计数用于循环的过程中向右读取数据，从0开始意味着读取NA（剩余GMV），从1开始意味对应第1天读取
        # print(数字列表)
        计数 = 0
        for 天数 in 数字列表 :
            # print('天数%s'%天数)       

            #在字典处定位需修改的地方，修改值为透析表中已经求和好的部分
            if 天数 >= 0 :
                求和值 = 横切透析.iloc[0,计数]
                # print('计数%s'%计数)
                计数 = 计数 + 1 - 全退对齐  
                全退对齐 = 0
                明细字典1[f'第{天数}天'] = one_decimal(求和值)
                  
        某一天明细 = pd.Series(明细字典1)
        某一天明细.name = 订单创建日期
        #不断合并统计好的日期
        用于合并 = 用于合并.append(某一天明细)
    用于列顺序维护 = list(明细字典1)
    用于合并 = 用于合并.loc[:,用于列顺序维护]
    用于合并.rename(columns={'第0天':'场次剩余成本'},inplace = True)
    
    用于合并['场次总成本统计'] = 用于合并.apply(lambda x: x.sum(), axis=1) # 按行求和，添加为新列
    用于合并.insert(0, '场次总成本', 用于合并['场次总成本统计'])
    用于合并.drop(['场次总成本统计'],axis= 1,inplace=True)
    用于合并.index.name="订单创建日期"
    
    """
    下段代码X用于给运营统计哪些订单没有匹配成功
    """
    #将统计标志为成功的删除掉即可
    运营使用统计 = 订单货物成本表[订单货物成本表['统计标志'].isin(['失败'])]
    运营使用统计 = 运营使用统计.loc[:,['成交数量','统计标志','匹配编号','订单创建日期','售后申请日期']]


    
    return 用于合并,运营使用统计

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
from ui_NewReturnsAndRefunds import Ui_Form

class Window(QWidget):

    def __init__(self):
        super().__init__()
        # 使用ui_Clean文件导入界面定义类
        self.ui = Ui_Form()
        self.ui.setupUi(self)  # 传入QWidget对象
        self.ui.retranslateUi(self)

        # 实例变量
        self.清洗后文件夹路径 = ''
        self.成本表文件绝对路径 = ''
        self.保存文件绝对路径 = ''
        self.操作人 = ''
        self.当天日期 = ''
        self.temp = ''  # 用于保存打开文件的路径

        self.ui.InputButton_1.clicked.connect(self.getInputDir)
        self.ui.InputButton_2.clicked.connect(self.getCostForm)
        self.ui.OutputButton.clicked.connect(self.getOutputDir)
        self.ui.RunButton.clicked.connect(self.handel)

    def getInputDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择清洗后文件夹路径") 
        if self.temp != '':
            self.清洗后文件夹路径 = self.temp
            self.ui.InputFile_1.setText(self.清洗后文件夹路径)

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
        self.操作人 = self.ui.User.text()
        self.当天日期 = self.ui.dateEdit.text()  # 获取日期
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
        if self.成本表文件绝对路径 == '':
            QMessageBox.about(self, "报错！", '请输入成本表')
            return        
        
        需打开表格名列表 = ['订单表','售后表','宝贝表'] #成本表需自己选择
        # 实例化对象,调用方法
        自动提取文件 = AutoExtractFiles(self.清洗后文件夹路径,需打开表格名列表)
        需打开表格字典 = 自动提取文件.handle() #['订单表'：对应文件路径]
        
        文件名 = os.path.basename(需打开表格字典['售后表']) # loose-天猫-账单表-清洗后.xlsx
        文件名前缀 = os.path.splitext(文件名)[0] # loose-天猫-账单表-清洗后
        平台类型 = 文件名前缀.split('-')[1] # loose-【天猫】-账单表-清洗后
        客户名称 = 文件名前缀.split('-')[0] # 【loose】-天猫-账单表-清洗后
        for k,v in 需打开表格字典.items():
            if k == '订单表':
                订单表 = pd.read_excel(v)
            elif k == '售后表':
                售后表 = pd.read_excel(v)
            elif k == '宝贝表':
                宝贝表 = pd.read_excel(v)
        
        if self.成本表文件绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择成本表')
            return
        
        if self.保存文件绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择保存路径')
            return
        
        if self.操作人 == '':
            QMessageBox.about(self, "报错！", '请输入操作人')
            return

        成本表 = pd.read_excel(self.成本表文件绝对路径)
        #——————————————————————————————————————————————————————————————————打开与保存模块

        try:
            日期格式 = datetime.datetime.strptime(f'{self.当天日期}','%Y/%m/%d').strftime('%Y-%m-%d')
        except:
            日期格式 = self.当天日期
        输出文件名格式 = f'\\{客户名称}-{平台类型}-退货退款表-{self.操作人}-{日期格式}.xlsx'
        输出路径 = self.保存文件绝对路径 + 输出文件名格式


        if 平台类型 == '抖音' :

            退货退款表,运营使用统计 = 抖音可回溯型退货退款表(订单表,售后表,成本表,日期格式)
        elif 平台类型 == '快手' :

            退货退款表,运营使用统计 = 快手可回溯型退货退款表(订单表,售后表,成本表,日期格式)
        elif 平台类型 == '天猫' :

            退货退款表,运营使用统计 = 天猫可回溯型退货退款表(宝贝表,售后表,成本表,日期格式)
        elif 平台类型 == '淘宝' :

            退货退款表,运营使用统计 = 天猫可回溯型退货退款表(宝贝表,售后表,成本表,日期格式)
        else :
            # print('命名格式错误：平台类型')
            QMessageBox.about(self, "报错！", "命名格式错误：平台类型")
            return

        #——————————————————————————————————————————————————————————————————打开与保存模块
        # 退货退款表.to_excel(输出路径)
        writer = pd.ExcelWriter(输出路径)
        退货退款表.to_excel(writer, sheet_name='退货退款表')
        # if 平台类型 == '抖音' :
        #     运营使用统计.to_excel(writer, sheet_name='匹配失败订单统计',index=False)
        # else:
        #     pass
        运营使用统计.to_excel(writer, sheet_name='匹配失败订单统计',index=False)
        writer.save()
        #不用删掉，不然文件短时间内不能编辑，只能读取
        writer.close()
        QMessageBox.about(self, "处理结果", f'成功！\n请于“{self.保存文件绝对路径}”查看结果文件')


app = QApplication([])
window = Window()
window.show()
app.exec_()



