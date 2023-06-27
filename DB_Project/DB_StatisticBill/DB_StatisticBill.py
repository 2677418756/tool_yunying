# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 18:18:12 2022

@author: Wind_Aleady_Here
"""

import pandas as pd
import datetime
import os
from collections import Counter
# 本金计费表的业务逻辑

"""
需要的数据来源：上一次本金计费表、本次的订单回款表
业务逻辑：读取

核心解决的的问题：
待解决的问题：
备注：
"""
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

def two_decimal(x_data):
    #【浮点数先转字符串，再转浮点数】让数据保留一位小数，且自动四舍五入
    x_str = '%.2f' % x_data #变成字符串来保留一位小数了
    return float(x_str)

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
            表格类型 = 文件名前缀.split('-')[2]  #FOLA旗舰店-抖音-订单表-CJY-无备注.xlsx
            for need_workbook in self.需打开表格名列表:
                if 表格类型 == need_workbook:
                    #记录需打开的文件名，最后返回
                    计数满足 = 计数满足 - 1 #若所需文件全部都存在，则最后计数为0
                    temp = self.文件夹路径 + '\\' + file
                    self.输出字典[表格类型] = temp
                    
        return self.输出字典
    
def 超30天判断并结算(剩余金额表,退本金统计表,当天自然日字符串):
    """
    逻辑：先将未结算的表格筛选出来，再提取成字典{场次日期:[授信代码1，授信代码2，。。。]}
    通过访问key值来与当天日期做对比，若成功则遍历其授信代码
    第一，读取对应天数的金额，并写出导账单明细表，最后再main函数中合并
    第二，将剩余金额表的对应记录修改，是否结算、结算方式
    第三，直接改变退本金统计表对应记录，当作已回，所以数值上不做改变
    """
    当天自然日 = datetime.datetime.strptime(当天自然日字符串, '%Y-%m-%d').date()

    剩余金额表['订单创建日期'] = 剩余金额表['订单创建日期'].map(timestamp_to_date)
    剩余金额表['授信日期'] = 剩余金额表['授信日期'].map(timestamp_to_date)
    try:
        剩余金额表['理论结算日期'] = 剩余金额表['理论结算日期'].map(timestamp_to_date)
    except(AttributeError):
        # 若没有已结算场次，则可能跳转到此语句
        pass

    退本金统计表['订单创建日期'] = 退本金统计表['订单创建日期'].map(timestamp_to_date)
    退本金统计表['授信日期'] = 退本金统计表['授信日期'].map(timestamp_to_date)
    try:
        退本金统计表['理论结算日期'] = 退本金统计表['理论结算日期'].map(timestamp_to_date)
    except(AttributeError):
        # 若没有已结算场次，则可能跳转到此语句
        pass
    # 创建空白dataframe
    账单核对表 = pd.DataFrame()
    当天特殊结算场次列表 = []

    未结算剩余金额表 = 剩余金额表[(剩余金额表['是否结算'] == '否')]
    list_ = list(未结算剩余金额表['订单创建日期'])
    # 返回字典，统计列表中值出现的次数，可统计重复值，Key为原列表中的values
    未结算剩余金额字典 = Counter(list_)

    for k, v in 未结算剩余金额字典.items():
        """
        按场次进行大循环，场次内的记录条数做小循环
        """
        未结算条数 = v
        场次日期 = k
        # 计算时间差距的
        temp_time = 当天自然日 - 场次日期
        天数 = temp_time.days + 1
        if 天数 > 31: # 因为为了读取前面加了一天
            # 第31天是特殊结算的第一天
            print('场次日期%s 对应天数是%s'%(场次日期,天数))
            特殊结算场次表 = 未结算剩余金额表[(未结算剩余金额表['订单创建日期'] == 场次日期)]
            special_list = list(特殊结算场次表['授信代码'])
            for i in special_list:
                结算授信代码 = i
                读取表 = 特殊结算场次表[(特殊结算场次表['授信代码'] == 结算授信代码)]

                本次应统计金额 = 读取表.iloc[0].at[f'第{天数}天']
                上次已统计金额 = 读取表.iloc[0].at[f'第{天数 - 1}天']
                # 【判断本次应统计金额需填入】本次应统计金额应该为0，也就是需要统计才对
                if not (本次应统计金额 == 0 and 上次已统计金额 != 0):
                    raise Exception('异常警告：本次应统计金额或者上次已统计金额')

                # 第二，剩余金额表修改对应表格的列
                剩余金额表.loc[剩余金额表['授信代码'].isin([结算授信代码]) & 剩余金额表['订单创建日期'].isin(
                    [场次日期]), '是否结算'] = '是'  # 某条记录结算
                剩余金额表.loc[剩余金额表['授信代码'].isin([结算授信代码]) & 剩余金额表['订单创建日期'].isin(
                    [场次日期]), '结算方式'] = '超时结算'
                剩余金额表.loc[剩余金额表['授信代码'].isin([结算授信代码]) & 剩余金额表['订单创建日期'].isin(
                    [场次日期]), '理论结算日期'] = 当天自然日

                # 只需要传递给退本金统计表，哪一个场次结束了即可，因为两边的授信代码是不对称的
                当天特殊结算场次列表.append(场次日期)

                明细字典2 = {}
                # ——————提取其他相关信息
                服务方1 = 读取表.iloc[0].at['服务方']
                资金方式1 = 读取表.iloc[0].at['资金方式']
                # ——————提取其他相关信息

                明细字典2['订单创建日期'] = 场次日期
                明细字典2['是否结算'] = '是'
                明细字典2['回款金额'] = 上次已统计金额
                明细字典2['服务方'] = 服务方1
                明细字典2['资金方式'] = 资金方式1
                明细字典2['授信代码'] = 结算授信代码
                某一天明细 = pd.Series(明细字典2)
                某一天明细.name = 场次日期
                # 不断合并统计好的日期
                账单核对表 = 账单核对表.append(某一天明细)

            # # 11.8 账单明细表订单创建日期排序，方便运营人员读取信息
            # 账单核对表 = 账单核对表.sort_values(by='订单创建日期', ascending=True)

            账单核对表.index.name = '订单创建日期'
            # 改变列的序列
            账单核对表 = 账单核对表.loc[:, ['订单创建日期', '服务方', '资金方式', '授信代码', '是否结算', '回款金额']]

            # 对本次结算的记录做处理
            for i in 当天特殊结算场次列表:
                退场次日期 = i
                对应未结算退本金表 = 退本金统计表[(退本金统计表['订单创建日期'] == 退场次日期) & (退本金统计表['是否结算'] == '否')]
                if not 对应未结算退本金表.empty:
                    退本金授信代码 = list(对应未结算退本金表['授信代码'])
                    for j in 退本金授信代码:
                        退结算授信代码 = j
                        退本金统计表.loc[退本金统计表['授信代码'].isin([退结算授信代码]) & 退本金统计表['订单创建日期'].isin(
                            [场次日期]), '是否结算'] = '是'  # 某条记录结算
                        退本金统计表.loc[退本金统计表['授信代码'].isin([退结算授信代码]) & 退本金统计表['订单创建日期'].isin(
                            [场次日期]), '结算方式'] = '超时结算'

    return 剩余金额表, 退本金统计表, 账单核对表


def 本金计费表(剩余金额表,结算回款表,当天自然日字符串):
    
    当天自然日 = datetime.datetime.strptime(当天自然日字符串,'%Y-%m-%d').date()
    
    # 剩余金额表['订单创建日期'] = 剩余金额表['订单创建日期'].map(timestamp_to_date)
    # 剩余金额表['授信日期'] = 剩余金额表['授信日期'].map(timestamp_to_date)
    # try:
    #     剩余金额表['理论结算日期'] = 剩余金额表['理论结算日期'].map(timestamp_to_date)
    # except(AttributeError):
    #     #若没有已结算场次，则可能跳转到此语句
    #     pass
 
    结算回款表['订单创建日期'] = 结算回款表['订单创建日期'].map(str_to_date)
    
    #创建空白dataframe
    账单核对表 = pd.DataFrame()

    当天正常结算场次包裹型列表 = [] # 希望可以[{'a':1},{'a':2},{'a':3}]同一KEY不同VALUE，直接拆列表来访问

    未结算剩余金额表 = 剩余金额表[(剩余金额表['是否结算'] == '否')]
    list_ = list(未结算剩余金额表['订单创建日期'])
    
    #返回字典，统计列表中值出现的次数，可统计重复值，Key为原列表中的values
    未结算剩余金额字典 = Counter(list_)

    
    for k,v in 未结算剩余金额字典.items():
        """
        按场次进行大循环，场次内的记录条数做小循环
        """
        未结算条数 = v
        场次日期 = k
        
        temp_dataframe0  = 未结算剩余金额表[(未结算剩余金额表['订单创建日期'] == 场次日期)]
        #下面两个本质是各自表中唯一的series
        temp_dataframe2  = 结算回款表[(结算回款表['订单创建日期'] == 场次日期)]  
           
        #【判断正确日期】如果当天自然日 - 场次日期 只计算大于1的自然日
        #计算时间差距的
        temp_time = 当天自然日 - 场次日期 
        天数 = temp_time.days + 1
        if 天数 <= 1 :
            #从第二天开始提取总金额 - 退 - 回 - 特殊
            print('需异常报错：输入当天自然日小于某场次日期')      
        #——————————————————————————————————————————————————————————————————读取数据模块
        
        try:
            场次本金回款金额 = temp_dataframe2.iloc[0].at[f'第{天数 - 1}天']
        except(IndexError):
            场次本金回款金额 = 0.00


        #让数据保留一位小数，且自动四舍五入
        场次本金回款金额 = two_decimal(场次本金回款金额)
        #——————————————————————————————————————————————————————————————————读取数据模块

        
        授信代码最小值 = temp_dataframe0['授信代码'].min() #min()返回series中的最小值,也就是返回授信代码这一列
        是否计算完毕 = True # 这里的逻辑可以理解为 相信第一次就能计算完毕，所以填True
        中间值记录 = 0.00

        # 条数退货退款金额 = 场次退货退款金额
        条数本金回款金额 = 场次本金回款金额
        while 未结算条数 >= 1:
            当天正常结算场次字典 = {}
            #【每一个while条数，只有改变的同场异次，循环写入一次】写账单明细表
            明细字典2 = {}

            #提取单独一条需要的记录，来提取数字
            final_dataframe1  = 未结算剩余金额表[(未结算剩余金额表['订单创建日期'] == 场次日期)&(未结算剩余金额表['授信代码'] == 授信代码最小值)]
            本次应统计金额 = final_dataframe1.iloc[0].at[f'第{天数}天']
            上次已统计金额 = final_dataframe1.iloc[0].at[f'第{天数 - 1}天']
            #【判断本次应统计金额需填入】本次应统计金额应该为0，也就是需要统计才对
            if not (本次应统计金额 == 0 and 上次已统计金额 != 0):
                print('异常警告：本次应统计金额或者上次已统计金额')
            
            #【将同场次下，没有改变总计的条数进行判断，并写入与跳过】
            if 未结算条数 != v and 是否计算完毕 == True:
                #未结算条数 != v 代表不是第一条记录，且计算完毕，所以上次总计等于本次总计
                print('同场其余未结算场次：',场次日期,授信代码最小值)
                剩余金额表.loc[剩余金额表['授信代码'].isin([授信代码最小值])&剩余金额表['订单创建日期'].isin([场次日期]),f'第{天数}天'] = 上次已统计金额
                授信代码最小值 = 授信代码最小值 + 1
                未结算条数 = 未结算条数 - 1
                continue #因为后面条数的本次应统计金额等于上次已统计金额，所以不用继续后面循环执行语句
            
            #【判断：选择总计的方法】
            if 是否计算完毕 == False: # 回款还没扣完需要下一条记录
                本次总计 = 上次已统计金额 - 中间值记录
            elif 是否计算完毕 == True : # 相信回款扣的完 或者 回款扣完了（已经在前面解决）
                # 第一次循环先走本条语句，因为前面设置为True了
                本次总计 = 上次已统计金额 - 场次本金回款金额
            #让数据保留一位小数，且自动四舍五入
            本次总计 = two_decimal(本次总计)
            
            #【判断：本条是否计算完毕】
            if 本次总计 <= 0.00:
                #若本次会结算，则本次总计填0，是否结算填是，账单表的值考虑改变
                #【判断后写入是否结算】写入要用剩余金额表，因为输出的也是剩余金额表
                剩余金额表.loc[剩余金额表['授信代码'].isin([授信代码最小值])&剩余金额表['订单创建日期'].isin([场次日期]),'是否结算'] = '是' #某条记录结算
                剩余金额表.loc[剩余金额表['授信代码'].isin([授信代码最小值])&剩余金额表['订单创建日期'].isin([场次日期]),'结算方式'] = '正常结算'
                当天正常结算场次字典[场次日期] = 授信代码最小值
                当天正常结算场次包裹型列表.append(当天正常结算场次字典)
                当天正常结算场次字典 = {}
                #11.5临时加
                是否结算 = '是'
                #影响多少用中间值记录
                中间值记录 = abs(本次总计)
                是否计算完毕 = False
                本次总计 = 0.00 
                """
                11.6日记载 上次条数本金回款金额 用于此情况： 假设三条同场次的记录一次性结算两个 
                此时 ①的条数回款 = ①的统计 用于全部扣减 所以 ①扣完后剩余 = 总场次回款 - ①的统计 ①扣完后剩余用中间值记录
                ②的条数回款 = ②的统计 用于全部扣减 所以 ②扣完后剩余 = ①扣完后剩余 - ②的统计 ②扣完后剩余用中间值记录
                最后 ③的条数回款 = ②扣完后剩余
                """
                # 只要是回款本条无法扣完，本条付出的都是上次已统计
                条数本金回款金额 = 上次已统计金额

                
            elif 本次总计 > 0.00:
                # 本条的确够扣完了，现在要看下本条是第一条还是最后一条，如果是第一条则 无中间值记录 直接场次回款是多少就是多少 ，如果是最后一条 就用上次扣完后剩余回款
                if 是否计算完毕 == False: # 本条是最后一条
                    #中间有过结算条数的后一条，把上次剩余留下
                    条数本金回款金额 = 中间值记录 # 11.5更改
                elif 是否计算完毕 == True: # 本条是第一条 （注：为了结构完善才加入elif）
                    条数本金回款金额 = 场次本金回款金额
                中间值记录 = 0.00
                是否计算完毕 = True
                是否结算 = '否'

            #——————提取其他相关信息
            服务方1 = final_dataframe1.iloc[0].at['服务方']
            资金方式1 = final_dataframe1.iloc[0].at['资金方式']
            授信代码1 =  授信代码最小值
            是否结算 = 是否结算
            #——————提取其他相关信息
            
            #1、一条全额够扣时，对应条数的退与回就是满额写
            #2、一条全额不够扣时，若有下一条，则本条部分写，下一条也部分写
            #3、一条全额不够扣时，若无下一条，本条部分写
            #上述三条中，2、3条合并写，因为没有下一条时，会跳出
            

            明细字典2['订单创建日期'] = 场次日期
            明细字典2['是否结算'] = 是否结算
            明细字典2['回款金额'] = 条数本金回款金额
            明细字典2['服务方'] = 服务方1
            明细字典2['资金方式'] = 资金方式1
            明细字典2['授信代码'] = 授信代码1
            某一天明细 = pd.Series(明细字典2)
            某一天明细.name = 场次日期
            
            #不断合并统计好的日期
            账单核对表 = 账单核对表.append(某一天明细)
            #【每次while循环写入一条记录】写入本次总计按正常计算还是归0  
            剩余金额表.loc[剩余金额表['授信代码'].isin([授信代码最小值])&剩余金额表['订单创建日期'].isin([场次日期]),f'第{天数}天'] = 本次总计
            授信代码最小值 = 授信代码最小值 + 1
            #进入本次循环代表使用过一条数据
            未结算条数 = 未结算条数 - 1
            
            # # 识别模块，未结算条数为0的情况的意思是本场次全部结算
            # if 未结算条数 == 0 and 是否计算完毕 == False:
            #     """"统计退本金用的是已回扣除，且是0.5，所以扣完后剩下的都是退本金，但是！！！很有可能扣不完或者扣多了"""
            #     完全结束场次字典.append(场次日期)
             
    # # 11.8 账单明细表订单创建日期排序，方便运营人员读取信息
    # 账单核对表 = 账单核对表.sort_values(by='订单创建日期',ascending=True)
        
    账单核对表.index.name='订单创建日期'
    #改变列的序列
    账单核对表 = 账单核对表.loc[:,['订单创建日期','服务方','资金方式','授信代码','是否结算','回款金额']]

    # 对本次结算的记录做处理
    for 被包裹字典 in 当天正常结算场次包裹型列表:
        for k,v in 被包裹字典.items():
            #k,v用于定位表格中的单元格
            当天结算场次 = k
            授信代码 = v
            #写入理论结算日期
            剩余金额表.loc[剩余金额表['授信代码'].isin([授信代码])&剩余金额表['订单创建日期'].isin([当天结算场次]),'理论结算日期'] = 当天自然日



    return 剩余金额表,账单核对表,当天正常结算场次包裹型列表

def 退本金统计表(退本金统计表,本金回款表,当天自然日字符串,当天正常结算场次包裹型列表):

    print(当天正常结算场次包裹型列表)
    当天自然日 = datetime.datetime.strptime(当天自然日字符串,'%Y-%m-%d').date()
    
    # 退本金统计表['订单创建日期'] = 退本金统计表['订单创建日期'].map(timestamp_to_date)
    # 退本金统计表['授信日期'] = 退本金统计表['授信日期'].map(timestamp_to_date)
    # try:
    #     退本金统计表['理论结算日期'] = 退本金统计表['理论结算日期'].map(timestamp_to_date)
    # except(AttributeError):
    #     #若没有已结算场次，则可能跳转到此语句
    #     pass
    本金回款表['订单创建日期'] = 本金回款表['订单创建日期'].map(str_to_date)
    
    # 创建空白dataframe
    退本金核对表 = pd.DataFrame()
    # # 循环筛选出结束场次，对该场次进行处理和统计
    for 被包裹字典 in 当天正常结算场次包裹型列表:
        for k,v in 被包裹字典.items():
            #k,v用于定位表格中的单元格
            当天结算场次 = k
            授信代码 = v
            #筛选
            enddataframe  = 退本金统计表[(退本金统计表['订单创建日期'] == 当天结算场次)&(退本金统计表['授信代码'] == 授信代码)]
            # 获取从左到右第一个不为零的列名来获取首次授信对应日期
            授信日期 = enddataframe.iloc[0].at['授信日期']

            #计算时间差距的
            temp_time1 = 当天自然日 - 当天结算场次
            第N天结束 = temp_time1.days + 1 # 不加1则是上次统计金额
            temp_time2 = 授信日期 - 当天结算场次
            第M天开始 = temp_time2.days + 1 # 11.5排查 会导致错误

            # 不做“上次金额=本次金额”处理，直接统计上次金额对应列的求和，并将结算标志改为是，并输出到核对表
            """
            本质上来说，使用 总本金 - 每一天的回本金 直到结算那一天 得到的 总退本金 是比实际要大，
            而且我这里采用直接读取昨天剩下的退本金 又比真正要算的要大，但不多才多几百块，
            这样做业务上是没问题的，因为退本金的统计是为了从另一个维度收服务费，
            但技术上需要考虑边界条件：针对昨天授信记录，但今天就回完的边界条件，需要检查再往前一天的格子应该为0，如果为0，则这次统计的退本金为0，反之正常进行
            """
            检测昨天 = enddataframe[f'第{第N天结束 - 1}天'].sum()
            if 检测昨天 == 0:
                总退本金 = 0.00
            else:
                总退本金 = enddataframe[f'第{第N天结束}天'].sum()
            退本金统计表.loc[退本金统计表['授信代码'].isin([授信代码])&退本金统计表['订单创建日期'].isin([当天结算场次]),'是否结算'] = '是' #某条记录结算
            退本金统计表.loc[退本金统计表['授信代码'].isin([授信代码])&退本金统计表['订单创建日期'].isin([当天结算场次]),'结算方式'] = '正常结算'
            #输出到退本金核对表
            明细字典2 = {}
            明细字典2['订单创建日期'] = 当天结算场次
            明细字典2['总退本金'] = 总退本金
            明细字典2['使用天数'] = int(第N天结束 - 第M天开始 + 1)
            明细字典2['授信代码'] = 授信代码
            某一天明细 = pd.Series(明细字典2)
            某一天明细.name = 当天结算场次

            #不断合并统计好的日期
            退本金核对表 = 退本金核对表.append(某一天明细)
    try:
        # 如果有回本金就用来扣减，没有的华dataframe为空，本质这里写if比较好
        退本金核对表 = 退本金核对表.sort_values(by='订单创建日期', ascending=True)
        退本金核对表.index.name = '订单创建日期'
        # 改变列的序列
        退本金核对表 = 退本金核对表.loc[:, ['订单创建日期', '授信代码', '总退本金', '使用天数']]
    except(KeyError):
        pass


    当天正常结算退场次包裹型列表 = []

        
    未结算退本金统计表 = 退本金统计表[(退本金统计表['是否结算'] == '否')]
    list_ = list(未结算退本金统计表['订单创建日期'])
    
    #返回字典，统计列表中值出现的次数，可统计重复值，Key为原列表中的values
    未结算剩余金额字典 = Counter(list_)
    
    for k,v in 未结算剩余金额字典.items():
        """
        按场次进行大循环，场次内的记录条数做小循环
        """
        未结算条数 = v
        场次日期 = k
        
        temp_dataframe0  = 未结算退本金统计表[(未结算退本金统计表['订单创建日期'] == 场次日期)]
        #下面两个本质是各自表中唯一的series
        temp_dataframe2  = 本金回款表[(本金回款表['订单创建日期'] == 场次日期)]  
           
        #【判断正确日期】如果当天自然日 - 场次日期 只计算大于1的自然日
        #计算时间差距的
        temp_time = 当天自然日 - 场次日期 
        天数 = temp_time.days + 1
        if 天数 <= 1 :
            #从第二天开始提取总金额 - 退 - 回 - 特殊
            print('需异常报错：输入当天自然日小于某场次日期')      
        #——————————————————————————————————————————————————————————————————读取数据模块
        
        try:
            场次本金回款金额 = temp_dataframe2.iloc[0].at[f'第{天数 - 1}天']
        except(IndexError):
            场次本金回款金额 = 0.00


        #让数据保留一位小数，且自动四舍五入
        场次本金回款金额 = two_decimal(场次本金回款金额)
        #——————————————————————————————————————————————————————————————————读取数据模块

        
        授信代码最小值 = temp_dataframe0['授信代码'].min() #min()返回series中的最小值,也就是返回授信代码这一列
        是否计算完毕 = True # 这里的逻辑可以理解为 相信第一次就能计算完毕，所以填True
        中间值记录 = 0.00
        # 条数退货退款金额 = 场次退货退款金额
        条数本金回款金额 = 场次本金回款金额
        while 未结算条数 >= 1:
            当天正常结算退场次字典 = {}
            #提取单独一条需要的记录，来提取数字
            final_dataframe1  = 未结算退本金统计表[(未结算退本金统计表['订单创建日期'] == 场次日期)&(未结算退本金统计表['授信代码'] == 授信代码最小值)]
            本次应统计金额 = final_dataframe1.iloc[0].at[f'第{天数}天']
            上次已统计金额 = final_dataframe1.iloc[0].at[f'第{天数 - 1}天']
            #【判断本次应统计金额需填入】本次应统计金额应该为0，也就是需要统计才对
            if not (本次应统计金额 == 0 and 上次已统计金额 != 0):
                print('异常警告：本次应统计金额或者上次已统计金额')
            
            #【将同场次下，没有改变总计的条数进行判断，并写入与跳过】
            if 未结算条数 != v and 是否计算完毕 == True:
                #未结算条数 != v 代表不是第一条记录，且计算完毕，所以上次总计等于本次总计
                退本金统计表.loc[退本金统计表['授信代码'].isin([授信代码最小值])&退本金统计表['订单创建日期'].isin([场次日期]),f'第{天数}天'] = 上次已统计金额
                授信代码最小值 = 授信代码最小值 + 1
                未结算条数 = 未结算条数 - 1
                continue #因为后面条数的本次应统计金额等于上次已统计金额，所以不用继续后面循环执行语句
            
            #【判断：选择总计的方法】
            if 是否计算完毕 == False:
                本次总计 = 上次已统计金额 - 中间值记录
            elif 是否计算完毕 == True :
                # 第一次循环先走本条语句，因为前面设置为True了
                本次总计 = 上次已统计金额 - 场次本金回款金额
            #让数据保留一位小数，且自动四舍五入
            本次总计 = two_decimal(本次总计)
            
            #【判断：本条是否计算完毕】
            if 本次总计 <= 0.00:
                #若本次会结算，则本次总计填0，是否结算填是，账单表的值考虑改变
                #【判断后写入是否结算】写入要用退本金统计表，因为输出的也是退本金统计表
                退本金统计表.loc[退本金统计表['授信代码'].isin([授信代码最小值])&退本金统计表['订单创建日期'].isin([场次日期]),'是否结算'] = '是' #某条记录结算
                退本金统计表.loc[退本金统计表['授信代码'].isin([授信代码最小值])&退本金统计表['订单创建日期'].isin([场次日期]),'结算方式'] = '正常结算'
                当天正常结算退场次字典[场次日期] = 授信代码最小值
                当天正常结算退场次包裹型列表.append(当天正常结算退场次字典)
                当天正常结算退场次字典 = {}
                #影响多少用中间值记录
                中间值记录 = abs(本次总计)
                是否计算完毕 = False
                本次总计 = 0.00
                # 本条记录对应的 回款金额
                # 只要是回款本条无法扣完，本条付出的都是上次已统计
                条数本金回款金额 = 上次已统计金额


            elif 本次总计 > 0.00:
                # 本条的确够扣完了，现在要看下本条是第一条还是最后一条，如果是第一条则 无中间值记录 直接场次回款是多少就是多少 ，如果是最后一条 就用上次扣完后剩余回款
                if 是否计算完毕 == False:  # 本条是最后一条
                    # 中间有过结算条数的后一条，把上次剩余留下
                    条数本金回款金额 = 中间值记录  # 11.5更改
                elif 是否计算完毕 == True:  # 本条是第一条 （注：为了结构完善才加入elif）
                    条数本金回款金额 = 场次本金回款金额
                中间值记录 = 0.00
                是否计算完毕 = True           
                

            #【每次while循环写入一条记录】写入本次总计按正常计算还是归0  
            退本金统计表.loc[退本金统计表['授信代码'].isin([授信代码最小值])&退本金统计表['订单创建日期'].isin([场次日期]),f'第{天数}天'] = 本次总计
            授信代码最小值 = 授信代码最小值 + 1
            #进入本次循环代表使用过一条数据
            未结算条数 = 未结算条数 - 1
            
        


    # 对本次结算的记录做处理
    for 被包裹退字典 in 当天正常结算退场次包裹型列表:
        for k,v in 被包裹退字典.items():
            #k,v用于定位表格中的单元格
            当天结算场次 = k
            授信代码 = v
            #写入理论结算日期
            退本金统计表.loc[退本金统计表['授信代码'].isin([授信代码])&退本金统计表['订单创建日期'].isin([当天结算场次]),'理论结算日期'] = 当天自然日


    return 退本金统计表,退本金核对表

from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget
from ui_DB_StatisticBill import Ui_Form

class Window(QWidget):

    def __init__(self):
        super().__init__()
        # 使用ui_Clean文件导入界面定义类
        self.ui = Ui_Form()
        self.ui.setupUi(self)  # 传入QWidget对象
        self.ui.retranslateUi(self)

        # 实例变量        
        self.C_昨日计费表文件绝对路径 = ''
        self.C_中台文件夹绝对路径 = ''
        self.C_输出至文件夹 = ''
        self.C_操作人 = ''
        self.C_当天日期 = ''        
        self.temp = ''  # 用于保存打开文件的路径
        
        self.ui.InputButton_1.clicked.connect(self.getInputFile)
        self.ui.InputButton_2.clicked.connect(self.getInputDir)
        self.ui.OutputButton.clicked.connect(self.getOutputDir)
        self.ui.RunButton.clicked.connect(self.handel)

    def getInputFile(self):
        self.temp, _ = QFileDialog.getOpenFileName(self, "选择昨日计费表", '', "Forms(*.xlsx *.csv)") 
        if self.temp != '':
            self.C_昨日计费表文件绝对路径 = self.temp
            self.ui.InputFile.setText(self.C_昨日计费表文件绝对路径)
    def getInputDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择数据库相关文件夹路径") 
        if self.temp != '':
            self.C_中台文件夹绝对路径 = self.temp
            self.ui.InputDir.setText(self.C_中台文件夹绝对路径)

    def getOutputDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")  # 不使用本地对话框，可以查看文件夹内文件
        # self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")
        if self.temp != '':
            self.C_输出至文件夹 = self.temp
            self.ui.OutputDir.setText(self.C_输出至文件夹)


       
    def handel(self):
        
        
        self.C_操作人 = self.ui.User.text()
        self.C_当天日期 = self.ui.dateEdit.text()  # 本质是订单创建日期 格式：2022-01-30
        
        #数据预处理
        try:
            日期格式 = datetime.datetime.strptime(f'{self.C_当天日期}','%Y/%m/%d').strftime('%Y-%m-%d')
        except:
            日期格式 = self.C_当天日期

        
        # 打开与保存模块
        需打开表格名列表 = ['订单回款表']
        # 实例化对象,调用方法
        自动提取文件 = AutoExtractFiles(self.C_中台文件夹绝对路径,需打开表格名列表)
        需打开表格字典 = 自动提取文件.handle()
        # 从文件名中提取相关信息
        文件名 = os.path.basename(需打开表格字典['订单回款表']) 
        文件名前缀 = os.path.splitext(文件名)[0] 
        平台类型 = 文件名前缀.split('-')[1] 
        客户名称 = 文件名前缀.split('-')[0] 
        # 打开需要的表格
        for k,v in 需打开表格字典.items():
            if k == '订单回款表':
                本金明细表 = pd.read_excel(v,sheet_name = '本金明细表')
                结算金额明细表 = pd.read_excel(v,sheet_name = '结算金额明细表')
                
        上次剩余金额表 = pd.read_excel(self.C_昨日计费表文件绝对路径,sheet_name = '剩余金额表')
        上次退本金表 = pd.read_excel(self.C_昨日计费表文件绝对路径,sheet_name = '退本金统计表')
        
        #【例子】FOLA旗舰店-抖音-剩余金额表-2022-05-14
        输出文件名格式 = f'\\{客户名称}-{平台类型}-新型计费表-{日期格式}-{self.C_操作人}.xlsx'
        输出路径 = self.C_输出至文件夹 + 输出文件名格式

        正常上次剩余金额表,正常上次退本金表,账单核对表特 = 超30天判断并结算(上次剩余金额表,上次退本金表,日期格式)
        # 下列函数种添加识别本场次的本金是否全部回完，如果回完则要让后面的函数知道且提取有关信息
        本次剩余金额表,账单核对表,当天正常结算场次包裹型列表 = 本金计费表(正常上次剩余金额表,结算金额明细表,日期格式) #当天日期用于提取第N天
        
        本次退本金表,退本金核对表 = 退本金统计表(正常上次退本金表,本金明细表,日期格式,当天正常结算场次包裹型列表)

        全账单明细表 = pd.concat([账单核对表特,账单核对表],axis=0)

        全账单明细表 = 全账单明细表.sort_index( ascending=True)

        writer = pd.ExcelWriter(输出路径)
        本次剩余金额表.to_excel(writer, sheet_name='剩余金额表',index=False)
        
        本次退本金表.to_excel(writer, sheet_name='退本金统计表',index=False)
        
        全账单明细表.to_excel(writer, sheet_name='账单核对表',index=False)
        
        退本金核对表.to_excel(writer, sheet_name='退本金核对表',index=False)
        
        writer.save()
        #不用删掉，不然文件短时间内不能编辑，只能读取
        writer.close()
        
        
        
        #成功后消息提醒
        QMessageBox.about(self, "处理结果", f'成功！\n请于“{self.C_输出至文件夹}”查看结果文件')

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()
# #读取文件
# 上次剩余金额表 = pd.read_excel(r'C:\Users\Admin\Desktop\本金计费测试\TB-快手-计费表-2022-10-07-GYH.xlsx',sheet_name = '2022-10-07剩余金额表')
# 上次退本金表 = pd.read_excel(r'C:\Users\Admin\Desktop\本金计费测试\TB-快手-计费表-2022-10-07-GYH.xlsx',sheet_name = '2022-10-07退本金统计表')

# 本金明细表 = pd.read_excel(r'C:\Users\Admin\Desktop\本金计费测试\黄金-订单回款表-GYH.xlsx',sheet_name = '本金明细表')
# 结算金额明细表 = pd.read_excel(r'C:\Users\Admin\Desktop\本金计费测试\黄金-订单回款表-GYH.xlsx',sheet_name = '结算金额明细表')

# # 下列函数种添加识别本场次的本金是否全部回完，如果回完则要让后面的函数知道且提取有关信息
# 本次剩余金额表,账单核对表,当天正常结算场次字典 = 本金计费表(上次剩余金额表,结算金额明细表,'2022-02-01') #当天日期用于提取第N天

# 本次退本金表,退本金核对表 = 退本金统计表(上次退本金表,本金明细表,'2022-02-01',当天正常结算场次字典)

# 输出路径 = r'C:\Users\Admin\Desktop\本金计费测试\测试结果.xlsx'

# writer = pd.ExcelWriter(输出路径)
# 本次剩余金额表.to_excel(writer, sheet_name='本次剩余金额表',index=False)

# 本次退本金表.to_excel(writer, sheet_name='本次退本金表',index=False)

# 账单核对表.to_excel(writer, sheet_name='账单核对表',index=False)

# 退本金核对表.to_excel(writer, sheet_name='退本金核对表',index=False)

# writer.save()
# #不用删掉，不然文件短时间内不能编辑，只能读取
# writer.close()




