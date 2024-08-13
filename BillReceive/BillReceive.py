# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 14:47:50 2022

@author: Admin
"""

import pandas as pd
import datetime as datetime
import numpy as np
import os


class AutoExtractFiles():

    def __init__(self, 文件夹路径, 需打开表格名列表):
        # 实例变量初始化
        self.输出字典 = {}
        self.文件夹路径 = 文件夹路径
        self.需打开表格名列表 = 需打开表格名列表

    def handle(self):

        所有文件名列表 = os.listdir(self.文件夹路径)
        计数满足 = len(self.需打开表格名列表)

        for file in 所有文件名列表:
            # 判断列表中元素是否存在，若存在则打开
            文件名前缀 = os.path.splitext(file)[0]
            表格类型 = 文件名前缀.split('-')[2]  # FOLA旗舰店-抖音-剩余金额表-2022-05-14.xlsx
            for need_workbook in self.需打开表格名列表:
                if 表格类型 == need_workbook:
                    # 记录需打开的文件名，最后返回
                    计数满足 = 计数满足 - 1  # 若所需文件全部都存在，则最后计数为0
                    temp = self.文件夹路径 + '\\' + file
                    self.输出字典[表格类型] = temp

        return self.输出字典


def 函数_提取日期(去重后, 字符串日期):
    近20天日期列表 = []
    for 订单创建日期 in 去重后.loc[:, f'{字符串日期}']:
        近20天日期列表.append(订单创建日期)
    return 近20天日期列表


def 函数_计算日期差值(订单创建日期, 对应实际结算日期列表):
    存放空间 = []
    创建日期 = datetime.datetime.strptime(订单创建日期, '%Y-%m-%d')
    for 实际结算日期 in 对应实际结算日期列表:
        结算日期 = datetime.datetime.strptime(实际结算日期, '%Y-%m-%d')

        差值 = 结算日期 - 创建日期

        存放空间.append(差值.days + 1)

    存放空间.sort()

    return 存放空间


def 抖音求和对比(账单表, 结算表):
    sum1 = 账单表['实际结算金额(元)'].sum()
    sum2 = 结算表['实际结算金额(元)'].sum()
    if sum1 >= sum2:
        final_dataframe = 账单表
    elif sum1 < sum2:
        final_dataframe = 结算表

    return final_dataframe


def one_decimal(x_data):
    # 【浮点数先转字符串，再转浮点数】让数据保留一位小数，且自动四舍五入
    x_str = '%.1f' % x_data  # 变成字符串来保留一位小数了
    return float(x_str)


def two_decimal(x_data):
    # 【浮点数先转字符串，再转浮点数】让数据保留一位小数，且自动四舍五入
    x_str = '%.2f' % x_data  # 变成字符串来保留一位小数了
    return float(x_str)


def 抖音账单回款表(账单表):
    用于合并 = pd.DataFrame()

    账单表 = 账单表[~账单表.订单创建日期.isna()]

    # 将浮点数按一位小数使用
    账单表['实际结算金额(元)'] = 账单表['实际结算金额(元)'].map(two_decimal)
    # 第一句将时间戳转换为datatime时间组件，第二句将短日期组件提取出来，第三句转换成str方便用户查看
    账单表['订单创建日期'] = pd.to_datetime(账单表['订单创建日期'])
    账单表['订单创建日期'] = 账单表['订单创建日期'].dt.date
    账单表['订单创建日期'] = 账单表['订单创建日期'].astype(str)

    账单表['实际结算日期'] = pd.to_datetime(账单表['实际结算日期'])
    账单表['实际结算日期'] = 账单表['实际结算日期'].dt.date
    账单表['实际结算日期'] = 账单表['实际结算日期'].astype(str)

    # 回款透析1 = pd.pivot_table(账单表,index=['实际结算日期'],columns = ['订单创建日期'],values=['实际结算金额(元)'],aggfunc = [np.sum])
    # 回款透析1.columns = 回款透析1.columns.droplevel(0)
    # 回款透析2 = pd.pivot_table(账单表,index=['订单创建日期'],columns = ['实际结算日期'],values=['实际结算金额(元)'],aggfunc = [np.sum])
    # 回款透析2.columns = 回款透析2.columns.droplevel(0)

    # 提取账单表中所有订单创建日期，从小到大排序【切一条，透析一条，加入一条】
    # 将不同订单创建日期的数据从小到大切割出来，会对应不同的实际结算日期，进行透析（也就是分组求和），按照一定规则加入到新表中

    回款总表 = pd.pivot_table(账单表, index=['实际结算日期'], values=['实际结算金额(元)'], aggfunc=[np.sum])
    回款总表.columns = 回款总表.columns.droplevel(0)
    回款总表.rename(columns={'实际结算金额(元)': '总计金额'}, inplace=True)

    按订单创建日期回款表 = pd.pivot_table(账单表, index=['订单创建日期'], values=['实际结算金额(元)'], aggfunc=[np.sum])
    按订单创建日期回款表.columns = 按订单创建日期回款表.columns.droplevel(0)
    按订单创建日期回款表.rename(columns={'实际结算金额(元)': '总计金额'}, inplace=True)

    """
    账单表整理分享： 退回给用户的形式在账单表中有两种——
    第一种（已结算型）：订单结算+74%，服务费返还+26%，已退款or原路退-100%。
    第二种（未结算型）：极速退款分账+100%，已退款or原路退-100%。
    
    账单回款表的用途—— 
    第一种：按自然日区分的的回款总计，用于授信表测算
    第二种：按场次区分的回款总计，用于授信表测算
    第三种：用于给计费表读取的场次-天数 回款明细
    
    2022年08月01号，考虑到第三种情况，特地把退款类的关闭，比如极速退款分账，已退款or原路退，服务费返还，部分退款的订单结算
    由于是时间差结构性问题：①只能捕捉到退，没有捕捉到进，②只能捕捉到进，未来的退还没有发生,无法精确区分部分退款的订单结算
    2022年08月03号，考虑到退与回联动，还是不进行筛选
    """
    # 账单表改 = 账单表[账单表['动账方向'].isin(['入账'])]
    # 账单表改 = 账单表改[~(账单表改['动账摘要'].isin(['极速退款分账'])|账单表改['动账摘要'].isin(['服务费返还']))]

    提取 = 账单表.copy()
    去重 = 账单表.copy()
    去重 = 去重.drop_duplicates('订单创建日期')
    横切用N列表 = 函数_提取日期(去重, '订单创建日期')
    # 排序，从小到大
    横切用N列表.sort()

    def remove_nat(lst):
        return [item for item in lst if not pd.isnull(item) and item != 'NaT']


    横切用N列表 = remove_nat(横切用N列表)
    for 订单创建日期 in 横切用N列表:
        # 提取某一天执行操作
        横切表 = 提取[(提取['订单创建日期'] == 订单创建日期)]
        # 获取同一个订单日期有几个动账日期
        获取 = 横切表.copy()
        # 去除重复的动账日期
        获取 = 获取.drop_duplicates('实际结算日期')


        # 将实际结算日期提取出来，返回形式为列表
        对应实际结算日期列表 = 函数_提取日期(获取, '实际结算日期')
        # print(对应实际结算日期列表)
        # 再用每一个动账日期减去订单日期，得到一组整数

        数字列表 = 函数_计算日期差值(订单创建日期, 对应实际结算日期列表)

        # 【数据透析表】
        横切透析 = pd.pivot_table(横切表, index=['订单创建日期'], columns=['实际结算日期'], values=['实际结算金额(元)'],
                                  aggfunc=[np.sum])
        # 去除表头sum
        横切透析.columns = 横切透析.columns.droplevel(0)
        # 创造字典，最后再修改字典
        明细字典1 = {f'第{i}天': 0 for i in range(1, 91)}  # range 区间是左闭右开

        # 利用整数
        计数 = 0
        for 天数 in 数字列表:
            # 在字典处定位需修改的地方，修改值为透析表中已经求和好的部分
            if 天数 >= 1:
                求和值 = 横切透析.iloc[0, 计数]
                计数 = 计数 + 1
                明细字典1[f'第{天数}天'] = float(求和值)

        某一天明细 = pd.Series(明细字典1)
        某一天明细.name = 订单创建日期
        # 不断合并统计好的日期
        用于合并 = 用于合并.append(某一天明细)

    用于列顺序维护 = list(明细字典1)
    用于合并 = 用于合并.loc[:, 用于列顺序维护]
    用于合并.index.name = "订单创建日期"

    return 回款总表, 用于合并, 按订单创建日期回款表


def 快手账单回款表(账单表):
    # 8月9日完全基于抖音的逻辑
    用于合并 = pd.DataFrame()

    # 将浮点数按一位小数使用
    账单表['实际结算金额(元)'] = 账单表['实际结算金额(元)'].map(two_decimal)
    # 第一句将时间戳转换为datatime时间组件，第二句将短日期组件提取出来，第三句转换成str方便用户查看
    账单表['订单创建日期'] = pd.to_datetime(账单表['订单创建日期'])
    账单表['订单创建日期'] = 账单表['订单创建日期'].dt.date
    账单表['订单创建日期'] = 账单表['订单创建日期'].astype(str)

    账单表['实际结算日期'] = pd.to_datetime(账单表['实际结算日期'])
    账单表['实际结算日期'] = 账单表['实际结算日期'].dt.date
    账单表['实际结算日期'] = 账单表['实际结算日期'].astype(str)

    # 回款透析1 = pd.pivot_table(账单表,index=['实际结算日期'],columns = ['订单创建日期'],values=['实际结算金额(元)'],aggfunc = [np.sum])
    # 回款透析1.columns = 回款透析1.columns.droplevel(0)
    # 回款透析2 = pd.pivot_table(账单表,index=['订单创建日期'],columns = ['实际结算日期'],values=['实际结算金额(元)'],aggfunc = [np.sum])
    # 回款透析2.columns = 回款透析2.columns.droplevel(0)

    # 提取账单表中所有订单创建日期，从小到大排序【切一条，透析一条，加入一条】
    # 将不同订单创建日期的数据从小到大切割出来，会对应不同的实际结算日期，进行透析（也就是分组求和），按照一定规则加入到新表中

    回款总表 = pd.pivot_table(账单表, index=['实际结算日期'], values=['实际结算金额(元)'], aggfunc=[np.sum])
    回款总表.columns = 回款总表.columns.droplevel(0)
    回款总表.rename(columns={'实际结算金额(元)': '总计金额'}, inplace=True)

    按订单创建日期回款表 = pd.pivot_table(账单表, index=['订单创建日期'], values=['实际结算金额(元)'], aggfunc=[np.sum])
    按订单创建日期回款表.columns = 按订单创建日期回款表.columns.droplevel(0)
    按订单创建日期回款表.rename(columns={'实际结算金额(元)': '总计金额'}, inplace=True)

    提取 = 账单表.copy()
    去重 = 账单表.copy()
    去重 = 去重.drop_duplicates('订单创建日期')
    横切用N列表 = 函数_提取日期(去重, '订单创建日期')
    # 排序，从小到大
    横切用N列表.sort()

    for 订单创建日期 in 横切用N列表:
        # 提取某一天执行操作
        横切表 = 提取[(提取['订单创建日期'] == 订单创建日期)]
        # 获取同一个订单日期有几个动账日期
        获取 = 横切表.copy()
        # 去除重复的动账日期
        获取 = 获取.drop_duplicates('实际结算日期')
        # 将实际结算日期提取出来，返回形式为列表
        对应实际结算日期列表 = 函数_提取日期(获取, '实际结算日期')
        # print(对应实际结算日期列表)
        # 再用每一个动账日期减去订单日期，得到一组整数
        数字列表 = 函数_计算日期差值(订单创建日期, 对应实际结算日期列表)

        # 【数据透析表】
        横切透析 = pd.pivot_table(横切表, index=['订单创建日期'], columns=['实际结算日期'], values=['实际结算金额(元)'],
                                  aggfunc=[np.sum])
        # 去除表头sum
        横切透析.columns = 横切透析.columns.droplevel(0)
        # 创造字典，最后再修改字典
        明细字典1 = {f'第{i}天': 0 for i in range(1, 91)}  # range 区间是左闭右开

        # 利用整数
        计数 = 0
        for 天数 in 数字列表:
            # 在字典处定位需修改的地方，修改值为透析表中已经求和好的部分
            if 天数 >= 1:
                求和值 = 横切透析.iloc[0, 计数]
                计数 = 计数 + 1
                明细字典1[f'第{天数}天'] = float(求和值)

        某一天明细 = pd.Series(明细字典1)
        某一天明细.name = 订单创建日期
        # 不断合并统计好的日期
        用于合并 = 用于合并.append(某一天明细)

    用于列顺序维护 = list(明细字典1)
    用于合并 = 用于合并.loc[:, 用于列顺序维护]
    用于合并.index.name = "订单创建日期"

    return 回款总表, 用于合并, 按订单创建日期回款表


def 天猫账单回款表(订单表, 账单表):
    # 先将账单回款总表做出
    用于合并 = pd.DataFrame()

    # 第一句将时间戳转换为datatime时间组件，第二句将短日期组件提取出来，第三句转换成str方便用户查看与程序使用
    订单表['订单创建日期'] = pd.to_datetime(订单表['订单创建日期'])
    订单表['订单创建日期'] = 订单表['订单创建日期'].dt.date
    订单表['订单创建日期'] = 订单表['订单创建日期'].astype(str)

    订单表['主订单编号'] = 订单表['主订单编号'].astype(str)
    账单表['订单编号'] = 账单表['订单编号'].astype(str)

    # 将浮点数按一位小数使用
    账单表['实际结算金额(元)'] = 账单表['实际结算金额(元)'].map(two_decimal)

    # 第一句将时间戳转换为datatime时间组件，第二句将短日期组件提取出来，第三句转换成str方便用户查看与程序使用
    账单表['实际结算日期'] = pd.to_datetime(账单表['实际结算日期'])
    账单表['实际结算日期'] = 账单表['实际结算日期'].dt.date
    账单表['实际结算日期'] = 账单表['实际结算日期'].astype(str)

    # 筛选
    用于粗糙的计费表 = 账单表[
        账单表.业务描述.isin(['0010001|交易收款-交易收款', '0010002|交易收款-预售定金（买家责任不退还）'])]
    用于计费 = 账单表[~(账单表.备注.isin(['网商贷-放款', '网商贷-还款']) | 账单表.账务类型.isin(['贷款还款']))]

    # 先将账单表的数据进行透析形成回款总表
    回款总表 = pd.pivot_table(用于计费, index=['实际结算日期'], values=['实际结算金额(元)'], aggfunc=[np.sum])

    账单合并订单 = pd.merge(用于计费, 订单表, how='left', left_on='订单编号', right_on='主订单编号')
    账单合并订单.dropna(axis=0, how='any', subset=['订单创建日期'], inplace=True)

    # 回款透析1 = pd.pivot_table(账单合并订单,index=['实际结算日期'],columns = ['订单创建日期'],values=['实际结算金额(元)'],aggfunc = [np.sum])
    # 回款透析1.columns = 回款透析1.columns.droplevel(0)
    # 回款透析2 = pd.pivot_table(账单合并订单,index=['订单创建日期'],columns = ['实际结算日期'],values=['实际结算金额(元)'],aggfunc = [np.sum])
    # 回款透析2.columns = 回款透析2.columns.droplevel(0)

    回款总表.columns = 回款总表.columns.droplevel(0)
    回款总表.rename(columns={'实际结算金额(元)': '总计金额'}, inplace=True)

    按订单创建日期回款表 = pd.pivot_table(账单合并订单, index=['订单创建日期'], values=['实际结算金额(元)'],
                                          aggfunc=[np.sum])
    按订单创建日期回款表.columns = 按订单创建日期回款表.columns.droplevel(0)
    按订单创建日期回款表.rename(columns={'实际结算金额(元)': '总计金额'}, inplace=True)
    # 提取账单表中所有订单创建日期，从小到大排序【切一条，透析一条，加入一条】
    # 将不同订单创建日期的数据从小到大切割出来，会对应不同的实际结算日期，进行透析（也就是分组求和），按照一定规则加入到新表中

    提取 = 账单合并订单.copy()
    去重 = 账单合并订单.copy()
    去重 = 去重.drop_duplicates('订单创建日期')
    横切用N列表 = 函数_提取日期(去重, '订单创建日期')
    # 排序，从小到大
    横切用N列表.sort()

    for 订单创建日期 in 横切用N列表:
        # 提取某一天执行操作
        横切表 = 提取[(提取['订单创建日期'] == 订单创建日期)]
        # 获取同一个订单日期有几个动账日期
        获取 = 横切表.copy()
        # 去除重复的动账日期
        获取 = 获取.drop_duplicates('实际结算日期')
        # 将实际结算日期提取出来，返回形式为列表
        对应实际结算日期列表 = 函数_提取日期(获取, '实际结算日期')
        # print(对应实际结算日期列表)
        # 再用每一个动账日期减去订单日期，得到一组整数
        数字列表 = 函数_计算日期差值(订单创建日期, 对应实际结算日期列表)

        # 【数据透析表】
        横切透析 = pd.pivot_table(横切表, index=['订单创建日期'], columns=['实际结算日期'], values=['实际结算金额(元)'],
                                  aggfunc=[np.sum])
        # 去除表头sum
        横切透析.columns = 横切透析.columns.droplevel(0)
        # 创造字典，最后再修改字典
        明细字典1 = {f'第{i}天': 0 for i in range(1, 91)}  # range 区间是左闭右开
        # 明细字典2 = {f'第{i+10}天': 0 for i in range(50)}
        # #【数字格式统一化】 01~09 10~30 两位数方便自动列排序
        # 明细字典1.update(明细字典2)
        # 利用整数
        # print(数字列表)
        计数 = 0
        for 天数 in 数字列表:
            # 在字典处定位需修改的地方，修改值为透析表中已经求和好的部分
            if 天数 >= 1:
                求和值 = 横切透析.iloc[0, 计数]
                计数 = 计数 + 1
                明细字典1[f'第{天数}天'] = float(求和值)

        某一天明细 = pd.Series(明细字典1)
        某一天明细.name = 订单创建日期
        # 不断合并统计好的日期
        用于合并 = 用于合并.append(某一天明细)

    用于列顺序维护 = list(明细字典1)
    用于合并 = 用于合并.loc[:, 用于列顺序维护]
    用于合并.index.name = "订单创建日期"

    return 回款总表, 用于合并, 按订单创建日期回款表


def 京东账单回款表(订单表, 账单表):
    # 用于装账单明细表
    用于合并 = pd.DataFrame()

    # 将浮点数按一位小数使用
    账单表['实际结算金额(元)'] = 账单表['实际结算金额(元)'].map(two_decimal)

    # 两表合并
    V = pd.merge(账单表, 订单表, how='left', on='订单编号')

    # 第一句将时间戳转换为datatime时间组件，第二句将短日期组件提取出来
    V['订单创建日期'] = pd.to_datetime(V['订单创建日期'], errors='coerce')
    # V['订单创建日期'] = V['订单创建日期'].dt.date

    V['实际结算日期'] = pd.to_datetime(V['实际结算日期'], errors='coerce')
    # V['实际结算日期'] = V['实际结算日期'].dt.date

    # 【京东独有中间处理过程】
    # 将匹配不出来的NA，或者匹配为空白的数据删掉
    V.dropna(axis=0, how='any', inplace=True, subset=['订单创建日期'])
    V.dropna(axis=0, how='any', inplace=True, subset=['实际结算日期'])
    V['订单创建日期'] = V['订单创建日期'].astype(str)
    V['实际结算日期'] = V['实际结算日期'].astype(str)

    # #防止出错
    # V['实际结算日期'] = np.where(V.实际结算日期.notnull(),V.实际结算日期.dt.strftime('%Y-%m-%d'),'2000-01-01')
    # V['订单创建日期'] = np.where(V.订单创建日期.notnull(),V.订单创建日期.dt.strftime('%Y-%m-%d'),'2000-01-01') #实际结算日期 - 订单创建日期 为负数，不会影响
    # # V.to_excel(r'F:\运营数据（同步）\解耦天猫京东账单表\京东解耦文件\账单明细\账单回款表\京东-账单回款.xlsx')

    # 优先使用账单表中的 实际结算日期，实际结算金额(元)
    回款总表 = pd.pivot_table(V, index=['实际结算日期'], values=['实际结算金额(元)'], aggfunc=[np.sum])
    回款总表.columns = 回款总表.columns.droplevel(0)
    回款总表.rename(columns={'实际结算金额(元)': '总计金额'}, inplace=True)

    # 回款透析2 = pd.pivot_table(V,index=['订单创建日期'],columns = ['实际结算日期'],values=['实际结算金额(元)'],aggfunc = [np.sum])
    # 回款透析2.columns = 回款透析2.columns.droplevel(0)

    # 回款透析1 = pd.pivot_table(V,index=['实际结算日期'],columns = ['订单创建日期'],values=['实际结算金额(元)'],aggfunc = [np.sum])
    # 回款透析1.columns = 回款透析1.columns.droplevel(0)

    # 提取V中所有订单创建日期，从小到大排序【切一条，透析一条，加入一条】
    # 将不同订单创建日期的数据从小到大切割出来，会对应不同的实际结算日期，进行透析（也就是分组求和），按照一定规则加入到新表中
    提取 = V.copy()
    去重 = V.copy()
    去重 = 去重.drop_duplicates('订单创建日期')
    横切用N列表 = 函数_提取日期(去重, '订单创建日期')
    # 排序，从小到大
    横切用N列表.sort()

    for 订单创建日期 in 横切用N列表:
        # 提取某一天执行操作
        横切表 = 提取[(提取['订单创建日期'] == 订单创建日期)]
        # 获取同一个订单日期有几个动账日期
        获取 = 横切表.copy()
        # 去除重复的动账日期
        获取 = 获取.drop_duplicates('实际结算日期')
        # 将实际结算日期提取出来，返回形式为列表
        对应实际结算日期列表 = 函数_提取日期(获取, '实际结算日期')
        # print(订单创建日期)
        # print(对应实际结算日期列表)
        # 再用每一个动账日期减去订单日期，得到一组整数
        数字列表 = 函数_计算日期差值(订单创建日期, 对应实际结算日期列表)
        # print(数字列表)
        # 【数据透析表】
        横切透析 = pd.pivot_table(横切表, index=['订单创建日期'], columns=['实际结算日期'], values=['实际结算金额(元)'],
                                  aggfunc=[np.sum])
        # 去除表头sum
        横切透析.columns = 横切透析.columns.droplevel(0)

        # 创造字典，最后再修改字典
        明细字典1 = {f'第{i}天': 0 for i in range(1, 91)}  # range 区间是左闭右开

        计数 = 0
        for 天数 in 数字列表:
            # 在字典处定位需修改的地方，修改值为透析表中已经求和好的部分
            if 天数 >= 1:
                求和值 = 横切透析.iloc[0, 计数]
                计数 = 计数 + 1
                明细字典1[f'第{天数}天'] = float(求和值)

        某一天明细 = pd.Series(明细字典1)
        某一天明细.name = 订单创建日期
        # 不断合并统计好的日期
        用于合并 = 用于合并.append(某一天明细)

    用于列顺序维护 = list(明细字典1)
    用于合并 = 用于合并.loc[:, 用于列顺序维护]
    用于合并.index.name = "订单创建日期"

    return 回款总表, 用于合并

def 拼多多账单回款表(订单表,账单表):
    bill_data_start = 账单表

    订单表 = 订单表.loc[:, ['订单号', '订单成交时间']]
    订单表['订单成交时间'] = pd.to_datetime(订单表['订单成交时间'], errors='coerce')
    订单表['订单成交时间'] = np.where(订单表.订单成交时间.notnull(),
                                          订单表.订单成交时间.dt.strftime('%Y-%m-%d'), '2000-01-01')
    订单表['订单成交时间'] = 订单表['订单成交时间'].astype('datetime64[ns]')

    账单表.rename(columns={'商户订单号': '订单号'}, inplace=True)
    账单表.rename(columns={'收入金额（+元）': '收入金额'}, inplace=True)
    账单表.rename(columns={'支出金额（-元）': '支出金额'}, inplace=True)
    账单表['收入金额'] = 账单表['收入金额'].astype(float)
    账单表['支出金额'] = 账单表['支出金额'].astype(float)
    账单表['发生时间'] = pd.to_datetime(账单表['发生时间'], errors='coerce')
    账单表['发生时间'] = np.where(账单表.发生时间.notnull(), 账单表.发生时间.dt.strftime('%Y-%m-%d'),
                                     '2000-01-01')
    账单表['发生时间'] = 账单表['发生时间'].astype('datetime64[ns]')

    bill_order_data = pd.merge(账单表, 订单表,how='left', left_on='订单号',right_on='订单号')
    bill_order_data['天数'] = bill_order_data['发生时间'] - bill_order_data['订单成交时间']
    bill_order_data['天数'] = bill_order_data['天数'].astype(str)
    bill_order_data.to_excel("D:/test.xlsx")
    bill_order_data['天数'] = bill_order_data['天数'].str.split(" ", expand=True)[0]
    bill_order_data['天数'] = bill_order_data['天数'].apply(lambda x: '第' + x + '天')
    bill_order_data['金额'] = bill_order_data['收入金额'] + bill_order_data['支出金额']

    grouped = bill_order_data.groupby(['订单成交时间', '天数'], as_index=True)
    settle_amount_data = grouped['金额'].sum()
    settle_amount_data = settle_amount_data.reset_index()

    settle_amount_data = pd.pivot_table(
        settle_amount_data,
        index=['订单成交时间'],
        columns=['天数'],
        values=['金额']
    )

    settle_amount_data["金额"] = settle_amount_data["金额"].fillna(0)
    settle_amount_data["金额"] = settle_amount_data["金额"].astype(float)

    # 设置格式
    settle_amount_data.columns = settle_amount_data.columns.droplevel(0)
    settle_amount_data = settle_amount_data.reset_index()
    settle_amount_data["订单成交时间"] = settle_amount_data["订单成交时间"].apply(lambda x: str(x)[:10])
    settle_amount_data = settle_amount_data.set_index("订单成交时间")

    # 根据天数进行排序
    column_numbers = [int(col.split('第')[1].split('天')[0]) for col in settle_amount_data.columns]
    # 根据数字部分对列名进行排序
    sorted_columns = [x for _, x in sorted(zip(column_numbers, settle_amount_data.columns))]

    # 按照排序后的列名重新排列 DataFrame
    df_sorted = settle_amount_data[sorted_columns]

    用于合并 = df_sorted


    bill_data_start['发生时间'] = bill_data_start['发生时间'].apply(lambda x:str(x).split(" ")[0])
    bill_data_start["收入金额"] = bill_data_start["收入金额"].astype(float)
    bill_data_start["支出金额"] = bill_data_start["支出金额"].astype(float)

    处理 = pd.pivot_table(bill_data_start, index=['发生时间'],
                          values=['收入金额','支出金额'],
                          aggfunc={'收入金额': np.sum,'支出金额': np.sum})
    处理["实际结算金额(元)"] = 处理["收入金额"] + 处理["支出金额"]
    处理.index.name = "实际结算日期"
    处理 = 处理.sort_index()
    回款总表 =  处理[["实际结算金额(元)"]]


    df_sorted["总计金额"] = 0
    for i in range(0,len(df_sorted.columns) - 1):
        df_sorted["总计金额"] += df_sorted[df_sorted.columns[i]]
    按订单创建日期回款表 = df_sorted[["总计金额"]]

    return 回款总表, 用于合并, 按订单创建日期回款表


from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget
from ui_BillReceive import Ui_Form


def 视频号账单回款表(订单表, 订单流水表):
    订单流水表['实际结算金额'] = 订单流水表['实际结算金额'].astype(float)
    bill_data_start = 订单流水表

    订单表 = 订单表.loc[:, ['订单号', '订单创建日期']]
    订单表['订单创建日期'] = pd.to_datetime(订单表['订单创建日期'], errors='coerce')
    订单表['订单创建日期'] = np.where(订单表.订单创建日期.notnull(),
                                      订单表.订单创建日期.dt.strftime('%Y-%m-%d'), '2000-01-01')
    订单表['订单创建日期'] = 订单表['订单创建日期'].astype('datetime64[ns]')

    订单流水表 = 订单流水表[~订单流水表.商家结算时间.isin(["-"])]
    订单流水表['商家结算时间'] = pd.to_datetime(订单流水表['商家结算时间'], errors='coerce')
    订单流水表['商家结算时间'] = np.where(订单流水表.商家结算时间.notnull(),
                                          订单流水表.商家结算时间.dt.strftime('%Y-%m-%d'),
                                          '2000-01-01')
    订单流水表['商家结算时间'] = 订单流水表['商家结算时间'].astype('datetime64[ns]')

    bill_order_data = pd.merge(订单流水表, 订单表, how='left', on='订单号')
    bill_order_data['天数'] = bill_order_data['商家结算时间'] - bill_order_data['订单创建日期']
    bill_order_data['天数'] = bill_order_data['天数'].astype(str)
    bill_order_data['天数'] = bill_order_data['天数'].str.split(" ", expand=True)[0]
    bill_order_data['天数'] = bill_order_data['天数'].apply(lambda x: '第' + x + '天')

    grouped = bill_order_data.groupby(['订单创建日期', '天数'], as_index=True)
    settle_amount_data = grouped['实际结算金额'].sum()
    settle_amount_data = settle_amount_data.reset_index()

    settle_amount_data = pd.pivot_table(
        settle_amount_data,
        index=['订单创建日期'],
        columns=['天数'],
        values=['实际结算金额']
    )
    settle_amount_data["实际结算金额"] = settle_amount_data["实际结算金额"].fillna(0)

    # 设置格式
    settle_amount_data.columns = settle_amount_data.columns.droplevel(0)
    settle_amount_data = settle_amount_data.reset_index()
    settle_amount_data["订单创建日期"] = settle_amount_data["订单创建日期"].apply(lambda x: str(x)[:10])
    settle_amount_data = settle_amount_data.set_index("订单创建日期")

    # 根据天数进行排序
    column_numbers = [int(col.split('第')[1].split('天')[0]) for col in settle_amount_data.columns]
    # 根据数字部分对列名进行排序
    sorted_columns = [x for _, x in sorted(zip(column_numbers, settle_amount_data.columns))]

    # 按照排序后的列名重新排列 DataFrame
    df_sorted = settle_amount_data[sorted_columns]

    df_sorted.to_excel("D:/账单回款表.xlsx", sheet_name="账单回款明细表")

    bill_data_start['商家结算时间'] = 订单流水表['商家结算时间'].apply(lambda x: str(x).split(" ")[0])

    订单流水表["商家结算时间"] = 订单流水表["商家结算时间"].apply(lambda x:str(x)[:10])
    处理 = pd.pivot_table(订单流水表, index=['商家结算时间'],
                          values=['实际结算金额'],
                          aggfunc={'实际结算金额': np.sum})
    处理.index.name = "实际结算日期"
    处理 = 处理.sort_index()

    df_sorted["总计金额"] = 0
    for i in range(0, len(df_sorted.columns) - 1):
        df_sorted["总计金额"] += df_sorted[df_sorted.columns[i]]

    return 处理[["实际结算金额"]],df_sorted,df_sorted[["总计金额"]]


class Window(QWidget):

    def __init__(self):
        super().__init__()
        # 使用ui_Clean文件导入界面定义类
        self.ui = Ui_Form()
        self.ui.setupUi(self)  # 传入QWidget对象
        self.ui.retranslateUi(self)

        # 实例变量
        self.输入文件夹绝对路径 = ''
        self.保存文件绝对路径 = ''
        self.操作人 = ''
        self.备注 = ''
        self.temp = ''  # 用于保存打开文件的路径

        self.ui.InputButton.clicked.connect(self.getInputDir)
        self.ui.OutputButton.clicked.connect(self.getOutputDir)
        self.ui.RunButton.clicked.connect(self.handel)

    def getInputDir(self):
        # self.temp = QFileDialog.getExistingDirectory(self, "选择输入文件夹",'', QFileDialog.DontUseNativeDialog)  # 不使用本地对话框，可以查看文件夹内文件
        self.temp = QFileDialog.getExistingDirectory(self, "选择输入文件夹")
        if self.temp != '':
            self.输入文件夹绝对路径 = self.temp
            self.ui.InputDir.setText(self.输入文件夹绝对路径)  # 显示路径

    def getOutputDir(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")  # 使用本地对话框
        # self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径", '', QFileDialog.DontUseNativeDialog)  # 不使用本地对话框，可以查看文件夹内文件
        if self.temp != '':
            self.保存文件绝对路径 = self.temp
            self.ui.OutputDir.setText(self.保存文件绝对路径)  # 显示路径

    def handel(self):

        # 获取输入值
        self.操作人 = self.ui.User.text()
        self.备注 = self.ui.Remark.text()
        需打开表格名列表 = ['订单表', '账单表', '结算表','订单流水表']
        # 实例化对象,调用方法
        自动提取文件 = AutoExtractFiles(self.输入文件夹绝对路径, 需打开表格名列表)
        需打开表格字典 = 自动提取文件.handle()
        # 【在前端提前避免一些错误，如空值检测】
        # 输入值为空时
        if self.输入文件夹绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择输入路径')
            return
        if self.保存文件绝对路径 == '':
            QMessageBox.about(self, "报错！", '请选择保存路径')
            return
        if self.操作人 == '':
            QMessageBox.about(self, "报错！", '请输入操作人')
            return

        if self.备注 == '':
            self.备注 = '无'
        try:
            try:
                文件名 = os.path.basename(需打开表格字典['账单表'])  # loose-天猫-账单表-清洗后.xlsx
            except:
                文件名 = os.path.basename(需打开表格字典['结算表'])
        except:
            文件名 = os.path.basename(需打开表格字典['订单流水表'])

        文件名前缀 = os.path.splitext(文件名)[0]  # loose-天猫-账单表-清洗后
        表格类型 = 文件名前缀.split('-')[2]
        平台类型 = 文件名前缀.split('-')[1]  # loose-【天猫】-账单表-清洗后
        客户名称 = 文件名前缀.split('-')[0]  # 【loose】-天猫-账单表-清洗后
        # 设置两个空的datafrmae是为了抖音两个表格之间做比较时，防止无对象传入
        for k, v in 需打开表格字典.items():
            if k == '订单表':
                订单表 = pd.read_excel(v)
            elif k == '账单表':
                账单表 = pd.read_excel(v)
            elif k == '结算表':
                结算表 = pd.read_excel(v)
            elif k == '订单流水表':
                订单流水表 = pd.read_excel(v)


        输出文件名格式 = f'\\{客户名称}-{平台类型}-账单回款表-{self.操作人}-{self.备注}.xlsx'
        输出路径 = self.保存文件绝对路径 + 输出文件名格式

        if 平台类型 == '抖音':
            try:
                对账表 = 抖音求和对比(账单表, 结算表)
                回款总表, 用于合并, 按订单创建日期回款表 = 抖音账单回款表(对账表)
            except:
                if 表格类型 == '账单表':
                    回款总表, 用于合并, 按订单创建日期回款表 = 抖音账单回款表(账单表)
                elif 表格类型 == '结算表':
                    回款总表, 用于合并, 按订单创建日期回款表 = 抖音账单回款表(结算表)
                else:
                    QMessageBox.about(self, "报错！", "没有对应表格！！")
        elif 平台类型 == '快手':
            回款总表, 用于合并, 按订单创建日期回款表 = 快手账单回款表(账单表)
        elif 平台类型 == '天猫':
            回款总表, 用于合并, 按订单创建日期回款表 = 天猫账单回款表(订单表, 账单表)
        elif 平台类型 == '京东':
            回款总表, 用于合并 = 京东账单回款表(订单表, 账单表)
        elif 平台类型 == '淘宝':
            回款总表, 用于合并, 按订单创建日期回款表 = 天猫账单回款表(订单表, 账单表)
        elif 平台类型 == '拼多多':
            回款总表, 用于合并, 按订单创建日期回款表 = 拼多多账单回款表(订单表, 账单表)
        elif 平台类型 == '视频号':
            回款总表, 用于合并, 按订单创建日期回款表 = 视频号账单回款表(订单表, 订单流水表)
        else:
            # print('命名格式错误：平台类型')
            QMessageBox.about(self, "报错！", "命名格式错误：平台类型")
            return

        # ————————————————————————————————————————————————————————————————————————输出模块
        # 【writer】使用writer将dataframe放入不同的excel的sheet中
        # 使用pd.ExcelWriter

        writer = pd.ExcelWriter(输出路径)
        用于合并.to_excel(writer, sheet_name='账单回款明细表')
        # 回款透析1.to_excel(writer, sheet_name='实际结算时间透析表')
        回款总表.to_excel(writer, sheet_name='账单回款总表')
        # 回款透析2.to_excel(writer, sheet_name='订单创建时间透析表')
        if 平台类型 == '抖音':
            按订单创建日期回款表.to_excel(writer, sheet_name='订单创建日期回款表')
        elif 平台类型 == '快手':
            按订单创建日期回款表.to_excel(writer, sheet_name='订单创建日期回款表')
        elif 平台类型 == '天猫':
            按订单创建日期回款表.to_excel(writer, sheet_name='订单创建日期回款表')
        elif 平台类型 == '淘宝':
            按订单创建日期回款表.to_excel(writer, sheet_name='订单创建日期回款表')
        elif 平台类型 == '拼多多':
            按订单创建日期回款表.to_excel(writer, sheet_name='订单创建日期回款表')
        elif 平台类型 == '视频号':
            按订单创建日期回款表.to_excel(writer, sheet_name='订单创建日期回款表')
        else:
            pass
        writer.save()
        # 不用删掉，不然文件短时间内不能编辑，只能读取
        writer.close()

        # 成功后消息提醒
        QMessageBox.about(self, "处理结果", f'成功！\n请于“{self.保存文件绝对路径}”查看结果文件')


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()

# class Window(QWidget):

#     def __init__(self):
#         super().__init__()
#         # 使用ui_Clean文件导入界面定义类
#         self.ui = Ui_Form()
#         self.ui.setupUi(self)  # 传入QWidget对象
#         self.ui.retranslateUi(self)

#     # 实例变量
#         self.账单表文件绝对路径 = ''
#         self.输出至文件夹 = ''
#         self.备注 = ''
#         self.操作人 = ''
#         self.temp = ''  # 辅助变量 打开文件用的

#         self.ui.InputButton.clicked.connect(self.getBill)
#         self.ui.OutputButton.clicked.connect(self.getOutputDir)
#         self.ui.RunButton.clicked.connect(self.handel)

#     def getBill(self):
#         self.temp, _ = QFileDialog.getOpenFileName(self, "选择账单表", '', "Forms(*.xlsx *.csv)")
#         if self.temp != '':
#             self.账单表文件绝对路径 = self.temp
#             self.ui.InputFile.setText(self.账单表文件绝对路径)

#     def getOutputDir(self):
#         self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")  # 使用本地对话框
#         # self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径", '', QFileDialog.DontUseNativeDialog)  # 不使用本地对话框，可以查看文件夹内文件
#         if self.temp != '':
#             self.输出至文件夹 = self.temp
#             self.ui.OutputDir.setText(self.输出至文件夹)

#     def handel(self):
#         # 获取输入值
#         self.操作人 = self.ui.User.text()
#         self.备注 = self.ui.Remark.text()  # 备注可以为空
#         # 输入值为空时
#         if self.账单表文件绝对路径 == '':
#             QMessageBox.about(self, "报错！", '请选择账单表')
#             return
#         if self.输出至文件夹 == '':
#             QMessageBox.about(self, "报错！", '请选择保存路径')
#             return
#         if self.操作人 == '':
#             QMessageBox.about(self, "报错！", '请输入操作人')
#             return
#         # 写一个if语句即可，查看是否为空
#         if self.备注 == '':
#             self.备注 == '无备注'

#         #———————————————————————————————————————————————————————————————————————————————————————预处理模块
#         账单表文件名 = os.path.split(self.账单表文件绝对路径)[1] #客户名称-平台名称-表格名称-操作人-备注.xlsx
#         账单表文件纯路径 = os.path.split(self.账单表文件绝对路径)[0] #C:\Users\Admin\Desktop\海月社中台数据

#         #根据文件名前缀来执行不同的逻辑模块（还要区分快手抖音）
#         账单表客户名称 = 账单表文件名.split('-')[0] #if
#         #———————————————————————————————————————————————————————————————————————————————————————预处理模块

#         #——————————————————————————————————————————————————————————————————打开与保存模块
#         平台类型 = 账单表文件名.split('-')[1]
#         客户名称 = 账单表客户名称
#         输出文件名格式 = f'\\{客户名称}-订单金额表-{self.操作人}-{self.备注}.xlsx'
#         输出路径 = self.保存文件绝对路径 + 输出文件名格式


#         if 平台类型 == '抖音' :
#             账单表 = pd.read_excel(self.账单表文件绝对路径)
#             抖音账单回款表(账单表)
#         elif 平台类型 == '天猫' :
#             账单表 = pd.read_excel(self.账单表文件绝对路径)
#             天猫账单回款表(账单表)
#         else :
#             # print('命名格式错误：平台类型')
#             QMessageBox.about(self, "报错！", "命名格式错误：平台类型")
#             return

#         #——————————————————————————————————————————————————————————————————打开与保存模块

#         订单金额表.to_excel(输出路径)

#         #读取部分需要的字段，并进行分列
#         #直接读取子表速度更快

#         账单表 = pd.read_excel(self.账单表文件绝对路径,usecols=['订单创建日期','实际结算日期','实际结算金额(元)'])
#         # 用于合并 = pd.DataFrame()

#         # #将浮点数按一位小数使用
#         # 账单表['实际结算金额(元)'] = 账单表['实际结算金额(元)'].map(one_decimal)
#         # #第一句将时间戳转换为datatime时间组件，第二句将短日期组件提取出来，第三句转换成str方便用户查看
#         # 账单表['订单创建日期'] = pd.to_datetime(账单表['订单创建日期'])
#         # 账单表['订单创建日期'] = 账单表['订单创建日期'].dt.date
#         # 账单表['订单创建日期'] = 账单表['订单创建日期'].astype(str)

#         # 账单表['实际结算日期'] = pd.to_datetime(账单表['实际结算日期'])
#         # 账单表['实际结算日期'] = 账单表['实际结算日期'].dt.date
#         # 账单表['实际结算日期'] = 账单表['实际结算日期'].astype(str)

#         # 回款透析1 = pd.pivot_table(账单表,index=['实际结算日期'],columns = ['订单创建日期'],values=['实际结算金额(元)'],aggfunc = [np.sum])
#         # 回款透析1.columns = 回款透析1.columns.droplevel(0)
#         # 回款透析2 = pd.pivot_table(账单表,index=['订单创建日期'],columns = ['实际结算日期'],values=['实际结算金额(元)'],aggfunc = [np.sum])
#         # 回款透析2.columns = 回款透析2.columns.droplevel(0)
#         # 回款总表 = pd.pivot_table(账单表,index=['实际结算日期'],values=['实际结算金额(元)'],aggfunc = [np.sum])
#         # 回款总表.columns = 回款总表.columns.droplevel(0)
#         # 回款总表.rename(columns={'实际结算金额(元)':'总计金额'},inplace = True)


#         # # 提取账单表中所有订单创建日期，从小到大排序【切一条，透析一条，加入一条】
#         # # 将不同订单创建日期的数据从小到大切割出来，会对应不同的实际结算日期，进行透析（也就是分组求和），按照一定规则加入到新表中

#         # 提取 = 账单表.copy()
#         # 去重 = 账单表.copy()
#         # 去重 = 去重.drop_duplicates('订单创建日期')
#         # 横切用N列表 = 函数_提取日期(去重,'订单创建日期')
#         # #排序，从小到大
#         # 横切用N列表.sort()

#         # for 订单创建日期 in 横切用N列表:
#         #     #提取某一天执行操作
#         #     横切表 = 提取[(提取['订单创建日期'] == 订单创建日期)]
#         #     #获取同一个订单日期有几个动账日期
#         #     获取 = 横切表.copy()
#         #     #去除重复的动账日期
#         #     获取 = 获取.drop_duplicates('实际结算日期')
#         #     #将实际结算日期提取出来，返回形式为列表
#         #     对应实际结算日期列表 = 函数_提取日期(获取,'实际结算日期')
#         #     # print(对应实际结算日期列表)
#         #     #再用每一个动账日期减去订单日期，得到一组整数
#         #     数字列表 = 函数_计算日期差值(订单创建日期,对应实际结算日期列表)

#         #     #【数据透析表】
#         #     横切透析 = pd.pivot_table(横切表,index=['订单创建日期'],columns=['实际结算日期'],values=['实际结算金额(元)'],aggfunc = [np.sum])
#         #     #去除表头sum
#         #     横切透析.columns = 横切透析.columns.droplevel(0)
#         #     #创造字典，最后再修改字典
#         #     明细字典1 = {f'第{i}天': 0 for i in range(1,91)} #range 区间是左闭右开
#         #     # 明细字典2 = {f'第{i+10}天': 0 for i in range(50)}
#         #     # #【数字格式统一化】 01~09 10~30 两位数方便自动列排序
#         #     # 明细字典1.update(明细字典2)
#         #     #利用整数
#         #     # print(数字列表)
#         #     计数 = 0
#         #     for 天数 in 数字列表 :
#         #         #在字典处定位需修改的地方，修改值为透析表中已经求和好的部分
#         #          if 天数 >= 1 :

#         #              求和值 = 横切透析.iloc[0,计数]
#         #              计数 = 计数 + 1
#         #              明细字典1[f'第{天数}天'] = float(求和值)

#         #          # elif 天数 >= 10 :

#         #          #    求和值 = 横切透析.iloc[0,计数]
#         #          #    计数 = 计数 + 1
#         #          #    明细字典1[f'第{天数}天'] = float(求和值)


#         #     某一天明细 = pd.Series(明细字典1)
#         #     某一天明细.name = 订单创建日期
#         #     #不断合并统计好的日期
#         #     用于合并 = 用于合并.append(某一天明细)

#         # 用于列顺序维护 = list(明细字典1)
#         # 用于合并 = 用于合并.loc[:,用于列顺序维护]
#         # 用于合并.index.name="订单创建日期"
#         #————————————————————————————————————————————————————————————————————————输出模块
#         输出 = self.输出至文件夹 + f'\\{账单表客户名称}-账单回款表-{self.操作人}-{self.备注}.xlsx'
#         #【writer】使用writer将dataframe放入不同的excel的sheet中

#         writer = pd.ExcelWriter(输出)
#         用于合并.to_excel(writer, sheet_name='账单回款明细表')
#         回款透析1.to_excel(writer, sheet_name='实际结算时间透析表')
#         回款总表.to_excel(writer, sheet_name='账单回款总表')
#         回款透析2.to_excel(writer, sheet_name='订单创建时间透析表')
#         writer.save()
#         #不用删掉，不然文件短时间内不能编辑，只能读取
#         writer.close()

#         #成功后消息提醒
#         QMessageBox.about(self, "处理结果", f'成功！\n请于“{self.输出至文件夹}”查看结果文件')
#         #————————————————————————————————————————————————————————————————————————输出模块
