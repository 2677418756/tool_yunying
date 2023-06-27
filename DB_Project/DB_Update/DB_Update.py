# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 15:43:51 2022

@author: Admin
"""


'''
应用场景:
    将excel等存储的数据 逐条 导入到 Mysql, 即 拼接sql 语句insert into.

    特点:
        1. 更适用于有主键约束的的表, 如花名册管理, 直接将新花名册逐条插入, 如有门店重复,则 替换 掉,保持最新.
        2. to_sql 则更适用用于无主键约束, 大批量导入数据的场景.

    原理:
        连接: 用Python提供的pymysql驱动,直接拼接SQL去执行
        数据: 将每条数据进行"insert into 或 replace into 表名 values (), (), (), ()...每个()放一条数据.
        过程:
            1. 创建连接对象 con  名字取通俗易懂哈
            2. 创建游标对象cursor (通俗理解为连接对象的一个小弟, 用来执行sql, 获取数据..)
            3. 执行sql语句cursor.execute() 或 executemany()....
            4. 提交命令(事务) con.commit()
            5. 查询或提取数据 cursor.fetchall()
            6. 关闭con, cursor

'''
import configparser
import pandas as pd
import pymysql
import datetime as datetime
import os


# def 插入数据(cursor, table, to_table, method="insert"):

#     len_cols = table.columns.size  # 字段的个数
#     name_cols = table.columns.values # 指定好列名
#     # 拼接sql语句: => insert into 表名 (字段1, 字段2 ...字段n) values (a,b,c), (d,e,f)....
#     if method not in ("insert", "replace"):
#         print("input error!")

#     temp_sql = "%s into %s (%s) values (%s)" % (method,to_table,"{},"*(len_cols-1) + "{}", "%s,"*(len_cols-1) + "%s") #会变成"insert into 表名 values (%s,%s,%s,%s,%s,%s)"
#     insert_sql = temp_sql.format(*name_cols) # format传入列表，SQL明确写出要插入哪一些字段，防止自增ID带来的插入困难
#     print(insert_sql)
#     # 变量每行数据, 组成生成器对象  ( (),(),(),(),(),()... ), 每个元组表示一条记录
#     args =  (tuple(row) for _, row in table.iterrows())
#     try:
#         _ = cursor.executemany(insert_sql, args)
#         print("successfully!")
#     except Exception as e:
#         print("fail",e)

            

def convert_Df_from_DataBase(cur, sql_order): # sql_order is a string
    
    """每天从数据库中读取近一个月内的商品单号，转换成dataframe再跟外部excel作比较，进行分组，然后分组操作更新或插入原数据库"""
    try:
        cur.execute(sql_order) # 多少条记录
        data  = cur.fetchall(  )
        frame = pd.DataFrame(list(data))
        print("successfully! convert_Df_from_DataBase")
    except Exception as e: #, e:
        frame = pd.DataFrame()
        print("fail convert_Df_from_DataBase",e)
        # print e
        # continue 
    return frame

def cut_table(last_table,now_table):
    """
    Parameters
    ----------
    last_table : DataFrame
        上次状态表
    table2 : DataFrame
        本次状态表
    逻辑：将同一商品单号的，前后状态不变的抛弃
    Returns
    -------
    DataFrame
    """
    #数据类型对齐，因为数据库中提取的列中的数据也是str
    now_table['商品单号'] = now_table['商品单号'].astype(str)
    # name_cols = now_table.columns.values
    # update_data = pd.DataFrame(columns = name_cols)
    上次已回 = last_table[last_table['回退状态'].isin(['已回'])]
    上次待回 = last_table[last_table['回退状态'].isin(['待回'])]  
    #直接Series转换成列表
    上次已回列表 = list(上次已回['商品单号']) 
    #分表操作,得到待更新数据和待插入数据
    对应本次已回 = now_table[now_table['商品单号'].isin([item for item in 上次已回列表])]
    # 精确切片 = 对应本次已回[对应本次已回['回退状态'].isin(['回退'])]
    #直接Series转换成列表
    上次待回列表 = list(上次待回['商品单号']) 
    #分表操作,得到待更新数据和待插入数据
    对应本次待回 = now_table[now_table['商品单号'].isin([item for item in 上次待回列表])]
  
    
    # frame = pd.DataFrame()
    frame = pd.concat([对应本次待回,对应本次已回])
    
    # for row in last_table.itertuples():
        
    #     """
    #     通过getattr获取row里面的值
    #     """
    #     商品单号 = getattr(row,'商品单号')
    #     上次回退状态 = getattr(row,'回退状态')
    #     本次回退状态 = str(now_table.loc[now_table['商品单号'].isin([商品单号]),'回退状态'])

    #     if 上次回退状态 == '待回' and 本次回退状态 == '待回':
    #         now_table = now_table[~(now_table['商品单号'].isin([商品单号]))]
    #     elif 上次回退状态 == '已回' and 本次回退状态 != '回退':
    #         now_table = now_table[~(now_table['商品单号'].isin([商品单号]))]
        
    frame.reset_index(inplace=True,drop=True)
        # print('成功切')
            
    return frame


class MysqlDBUtils(object):

    def __init__(self, host, username, password, db):
        self.host = host
        # self.port = port
        self.username = username
        self.password = password
        self.db = db
        self.conn = None
        self.cursor = None

    def connect(self, charset='utf8'):
        self.conn = pymysql.connect(host=self.host, user=self.username,
                                    password=self.password, db=self.db, charset=charset)
        self.cursor = self.conn.cursor()

        return self.conn, self.cursor


class ReadDBConfig(object):

    def __init__(self):

        # 根据系统环境路径获取配置文件路径
        try:
            print(os.environ['DB_CONFIG_PATH'])
            CONFIG_PATH = os.environ['DB_CONFIG_PATH']  # 直接获取到从环境变量中设置的文件绝对路径

        except Exception:
            raise ValueError
        # 调用库读取配置文件
        """
        .ini文件知识点:数据格式自己上网查，一个section对应多个option，
        每个option本身是类似于键值对 optionname = value 或者是 optionname : value
        """
        self.config = configparser.ConfigParser()
        self.config.optionxform = lambda option: option  # 这一句非常重要，对configparser模块的ConfigParser类对象的optionxform函数进行重载
        self.config.read(CONFIG_PATH, encoding="utf-8-sig")
        self.client_Dict = {}
        self.DB_Dict = {}

        # 获取配置文件信息

    def set_DB_info(self):
        self.host = self.config["DATABASE"]["HOST"]
        self.database = self.config["DATABASE"]["DBNAME"]
        self.user = 'root'
        self.password = 'zjs168198'
        self.DB_Dict['host'] = self.host
        self.DB_Dict['user'] = self.user
        self.DB_Dict['password'] = self.password
        self.DB_Dict['database'] = self.database

    def set_Client_info(self):
        """
        知识点：
        读取出来会忽略大小写！
        config.items("CLIENT") 返回[('fola旗舰店', 'fola_order_status')]元组类型
        dict(self.config.items("CLIENT"))  返回{'fola旗舰店': 'fola_order_status'}
        """
        self.client_Dict = dict(
            self.config.items("CLIENT"))  # {'FOLA旗舰店': 'fola_order_status', 'XINGDAO': 'xingdao_order_status'}


def dataframe_add_cols_name(df, cols_list):
    if not df.empty:
        df.columns = cols_list
    else:
        df = pd.DataFrame(columns=cols_list)

    return df


def 快手订单全状态表插入与更新(con,cursor,shop_tablename,now_data,nowday_str,usedays):

    update_all_status = False
    #————————————————————————————————————————————————————————————————————————————————————识别
    # 对应店铺字典 = {'FOLA旗舰店':'FOLA_OrderStatus'}
    # shop_tablename = 对应店铺字典[shop_name]
    #对用户输入的字符串时间进行处理
    list_cols = now_data.columns.values
    len_cols = now_data.columns.size
    # nowday_str = '2022-09-11 00:00:00' #来自用户输入
    nowday = datetime.datetime.strptime(nowday_str,'%Y-%m-%d') #datetime.datetime类型，且默认时间为 00:00:00
    drawday = nowday + datetime.timedelta(days = -usedays)
    print('数据库中提取时间范围是：%s-%s:'%(drawday,nowday))
    drawday_str = str(drawday)
    
    #构建SQL语句，获取一定时间范围内的商品单号
    sql_select = f"select 商品单号 from %s where %s.订单创建时间 >= \'{drawday_str}\'"%(shop_tablename,shop_tablename)
    print('classify_table函数，执行SQL语句：%s'%sql_select) #检查SQL语句
    
    #从数据中读取数据并转换成表格
    DB_data1 = convert_Df_from_DataBase(cursor,sql_select)
    #给数据库中提取的数据设置列名
    DB_data1.columns = ['商品单号']
    
    #直接Series转换成列表
    temp_list = list(DB_data1['商品单号']) 
    #数据类型对齐，因为数据库中提取的列中的数据也是str
    now_data['商品单号'] = now_data['商品单号'].astype(str) 
    #分表操作,得到待更新数据和待插入数据
    equal_data = now_data[now_data['商品单号'].isin([item for item in temp_list])]
    other_data = now_data[~(now_data['商品单号'].isin([item for item in temp_list]))]
    #————————————————————————————————————————————————————————————————————————————————————识别
    print(other_data) # 有可能同一天中重复更新同一个数据表就会插入失败，则other_data为空

    #排除待更新中待回的,减少SQL的花销
    equal_data = equal_data[~(equal_data['回退状态'].isin(['待回']))]

    sql_select2 = "select %s from {tablename} where {tablename}.订单创建时间 >= \'{day_str}\' and ({tablename}.回退状态 = '待回' or {tablename}.回退状态 = '已回')" % ("{},"*(len_cols-1) + "{}")
    sql_select2 = sql_select2.format(*list_cols,tablename = shop_tablename,day_str = drawday_str)

    DB_data2 = convert_Df_from_DataBase(cursor,sql_select2)
    DB_data2.columns = list_cols


    #【处理逻辑】逻辑：将同一商品单号的，前后状态不变的抛弃
    update_data = cut_table(DB_data2,equal_data)


    update_data['订单编号'] = update_data['订单编号'].astype(str)
    update_data['商品单号'] = update_data['商品单号'].astype(str)
    
    #【数据库update操作】
    #为了顺序问题组成新表再构建生成器
    temp = update_data[['订单状态','售后状态','售后申请时间','实际结算时间','实际结算金额','回退状态','物流时间','商品单号']]
    args =  (tuple(row) for _, row in temp.iterrows())
    update_sql = "update {tablename} set 订单状态 = %s,售后状态 = %s,售后申请时间 = %s,实际结算时间 = %s,实际结算金额 = %s,回退状态 = %s, 物流时间 = %s where {tablename}.商品单号 = %s "
    update_sql = update_sql.format(tablename = shop_tablename)
    try:
        _ = cursor.executemany(update_sql, args)
        con.commit()
        print("successfully update_sql!")
        update_all_status = True
    except Exception as e:
        print("fail update_sql",e)
        con.rollback()

    if not other_data.empty:
        #【数据库insert操作】
        #已完成待插入数据的插入测试
        insert_sql = "insert into %s (%s) values (%s)" % (shop_tablename,"{},"*(len_cols-1) + "{}", "%s,"*(len_cols-1) + "%s") #会变成"insert into 表名 values (%s,%s,%s,%s,%s,%s)"
        insert_sql = insert_sql.format(*list_cols) # format传入列表，SQL明确写出要插入哪一些字段，防止自增ID带来的插入困难
        print(insert_sql)
        # 变量每行数据, 组成生成器对象  ( (),(),(),(),(),()... ), 每个元组表示一条记录
        argss =  (tuple(row) for _, row in other_data.iterrows())
        try:
            _ = cursor.executemany(insert_sql, argss)
            con.commit()
            print("successfully insert_sql!")
        except Exception as e:
            print("fail insert_sql",e)
            con.rollback()

        cursor.close() # 先关闭游标
        con.close() # 再关闭数据库

    return update_all_status


def 淘系订单全状态表插入与更新(con, cursor, shop_tablename, now_data, nowday_str, usedays):
    update_all_status = False
    # ————————————————————————————————————————————————————————————————————————————————————识别
    # 对应店铺字典 = {'FOLA旗舰店':'FOLA_OrderStatus'}
    # shop_tablename = 对应店铺字典[shop_name]
    # 对用户输入的字符串时间进行处理
    list_cols = now_data.columns.values
    len_cols = now_data.columns.size
    # nowday_str = '2022-09-11 00:00:00' #来自用户输入
    nowday = datetime.datetime.strptime(nowday_str, '%Y-%m-%d')  # datetime.datetime类型，且默认时间为 00:00:00
    drawday = nowday + datetime.timedelta(days=-usedays)
    print('数据库中提取时间范围是：%s-%s:' % (drawday, nowday))
    drawday_str = str(drawday)

    # 构建SQL语句，获取一定时间范围内的商品单号
    sql_select = f"select 商品单号 from %s where %s.订单创建时间 >= \'{drawday_str}\'" % (
    shop_tablename, shop_tablename)
    print('classify_table函数，执行SQL语句：%s' % sql_select)  # 检查SQL语句

    # 从数据中读取数据并转换成表格
    DB_data1 = convert_Df_from_DataBase(cursor, sql_select)
    # 给数据库中提取的数据设置列名
    DB_data1.columns = ['商品单号']

    # 直接Series转换成列表
    temp_list = list(DB_data1['商品单号'])
    # 数据类型对齐，因为数据库中提取的列中的数据也是str
    now_data['商品单号'] = now_data['商品单号'].astype(str)
    # 分表操作,得到待更新数据和待插入数据
    equal_data = now_data[now_data['商品单号'].isin([item for item in temp_list])]
    other_data = now_data[~(now_data['商品单号'].isin([item for item in temp_list]))]
    # ————————————————————————————————————————————————————————————————————————————————————识别
    print(other_data)  # 有可能同一天中重复更新同一个数据表就会插入失败，则other_data为空

    # 排除待更新中待回的,减少SQL的花销
    equal_data = equal_data[~(equal_data['回退状态'].isin(['待回']))]

    sql_select2 = "select %s from {tablename} where {tablename}.订单创建时间 >= \'{day_str}\'" % (
                "{}," * (len_cols - 1) + "{}")
    sql_select2 = sql_select2.format(*list_cols, tablename=shop_tablename, day_str=drawday_str)

    DB_data2 = convert_Df_from_DataBase(cursor, sql_select2)
    DB_data2.columns = list_cols

    # 【处理逻辑】逻辑：将同一商品单号的，前后状态不变的抛弃
    update_data = cut_table(DB_data2, equal_data)

    update_data['订单编号'] = update_data['订单编号'].astype(str)
    update_data['商品单号'] = update_data['商品单号'].astype(str)

    # 【数据库update操作】
    # 为了顺序问题组成新表再构建生成器
    temp = update_data[
        ['订单状态', '售后状态', '售后申请时间', '实际结算时间', '实际结算金额', '回退状态', '物流时间', '商品单号']]
    args = (tuple(row) for _, row in temp.iterrows())
    # 按照子订单编号作条件，多次覆盖时，订单状态、售后状态、物流时间不会变，回退状态是根据

    update_sql = "update {tablename} set 订单状态 = %s,售后状态 = %s,售后申请时间 = %s,实际结算时间 = %s,实际结算金额 = %s,回退状态 = %s, 物流时间 = %s where {tablename}.商品单号 = %s "
    update_sql = update_sql.format(tablename=shop_tablename)
    try:
        _ = cursor.executemany(update_sql, args)
        con.commit()
        print("successfully update_sql!")
        update_all_status = True
    except Exception as e:
        print("fail update_sql", e)
        con.rollback()

    if not other_data.empty:
        # 【数据库insert操作】
        # 已完成待插入数据的插入测试
        insert_sql = "insert into %s (%s) values (%s)" % (shop_tablename, "{}," * (len_cols - 1) + "{}", "%s," * (
                    len_cols - 1) + "%s")  # 会变成"insert into 表名 values (%s,%s,%s,%s,%s,%s)"
        insert_sql = insert_sql.format(*list_cols)  # format传入列表，SQL明确写出要插入哪一些字段，防止自增ID带来的插入困难
        print(insert_sql)
        # 变量每行数据, 组成生成器对象  ( (),(),(),(),(),()... ), 每个元组表示一条记录
        argss = (tuple(row) for _, row in other_data.iterrows())
        try:
            _ = cursor.executemany(insert_sql, argss)
            con.commit()
            print("successfully insert_sql!")
        except Exception as e:
            print("fail insert_sql", e)
            con.rollback()

        cursor.close()  # 先关闭游标
        con.close()  # 再关闭数据库

    return update_all_status


def 已授信记录插入(con,cursor,shop_tablename,now_data):
    
    """
    shop_tablename = 数据库内对应表名，此处是已授信本金表，now_data = 当天已授信本金表
    时间维度选择：不选择，直接插入，但插入前检查，所以还是选揽件时间
    业务内容：昨日揽收的多场次订单记录及其金额
    特殊：少部分订单记录的揽件时间会因为：运单与订单合并的不对称性，导致揽件时间会变，但是要求不更新这些揽件时间，所以使用insert ignore
    """

    insert_credit_amount = False
    list_cols = now_data.columns.values
    len_cols = now_data.columns.size


    #【数据库insert操作】insert ignore
    #少部分订单记录的揽件时间会因为：运单与订单合并的不对称性，导致揽件时间会变，但是要求不更新这些揽件时间
    insert_sql = "insert ignore into %s (%s) values (%s)" % (shop_tablename,"{},"*(len_cols-1) + "{}", "%s,"*(len_cols-1) + "%s") #会变成"insert into 表名 values (%s,%s,%s,%s,%s,%s)"
    insert_sql = insert_sql.format(*list_cols) # format传入列表，SQL明确写出要插入哪一些字段，防止自增ID带来的插入困难
    print('已授信记录插入执行SQL语句：%s'%insert_sql)
    # 变量每行数据, 组成生成器对象  ( (),(),(),(),(),()... ), 每个元组表示一条记录
    argss =  (tuple(row) for _, row in now_data.iterrows())
    try:
        _ = cursor.executemany(insert_sql, argss)
        con.commit()
        print("successfully insert_sql!")
        insert_credit_amount = True
    except Exception as e:
        print("fail insert_sql",e)
        con.rollback()    
        
    cursor.close() # 先关闭游标
    con.close() # 再关闭数据库

    return insert_credit_amount
    
    
def 快手已授信记录更新(con,cursor,shop_tablename,now_data,nowday_str,usedays):

    update_credit_status = False
    #————————————————————————————————————————————————————————————————————————————————————哪些记录值得更新？
    list_cols = now_data.columns.values
    len_cols = now_data.columns.size
    
    #时间处理，选择30天内
    nowday = datetime.datetime.strptime(nowday_str,'%Y-%m-%d') #datetime.datetime类型，且默认时间为 00:00:00
    drawday = nowday + datetime.timedelta(days = -usedays)
    print('快手已授信记录更新数据库中提取时间范围是：%s-%s:'%(drawday,nowday))
    drawday_str = str(drawday)
      
    # 本金
    #排除本次本金中待回的,减少SQL的花销
    now_data = now_data[~(now_data['回退状态'].isin(['待回']))]
     
    sql_select2 = "select %s from {tablename} where {tablename}.订单创建时间 >= \'{start_day_str}\' and {tablename}.订单创建时间 < \'{end_day_str}\'and ({tablename}.回退状态 = '待回' or {tablename}.回退状态 = '已回')" % ("{},"*(len_cols-1) + "{}")
    sql_select2 = sql_select2.format(*list_cols,tablename = shop_tablename,start_day_str = drawday_str,end_day_str = nowday_str)

    DB_data2 = convert_Df_from_DataBase(cursor,sql_select2)
    #给数据库中提取的数据设置列名
    DB_data2 = dataframe_add_cols_name(DB_data2,list_cols)
    
    # DB_data2.columns = list_cols 

    #【处理逻辑】逻辑：将同一商品单号的，前后状态不变的抛弃
    update_data = cut_table(DB_data2,now_data)

    update_data['订单编号'] = update_data['订单编号'].astype(str)
    update_data['商品单号'] = update_data['商品单号'].astype(str)
    
    #【数据库update操作】
    #为了顺序问题组成新表再构建生成器
    temp = update_data[['订单状态','售后状态','售后申请时间','实际结算时间','实际结算金额','回退状态','商品单号']]
    args =  (tuple(row) for _, row in temp.iterrows())
    update_sql = "update {tablename} set 订单状态 = %s,售后状态 = %s,售后申请时间 = %s,实际结算时间 = %s,实际结算金额 = %s,回退状态 = %s where {tablename}.商品单号 = %s "
    update_sql = update_sql.format(tablename = shop_tablename)
    try:
        _ = cursor.executemany(update_sql, args)
        con.commit()
        print("successfully update_sql!")
        update_credit_status = True
    except Exception as e:
        print("fail update_sql",e)
        con.rollback()    
        
    cursor.close() # 先关闭游标
    con.close() # 再关闭数据库  

    return update_credit_status
    


from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QWidget, QComboBox,QInputDialog,QLineEdit
from ui_DB_Update import Ui_Form

class Window(QWidget):

    def __init__(self):
        super().__init__()
        # 使用ui_Clean文件导入界面定义类
        self.ui = Ui_Form()
        self.ui.setupUi(self)  # 传入QWidget对象
        self.ui.retranslateUi(self)

        # 实例变量
        self.本次状态表输入路径 = ''
        self.最新状态表输出路径 = ''
        self.天数 = ''
        self.当天日期 = ''
        self.开始日期 = ''
        self.结束日期 = ''
        self.选择客户 = '选择店铺'
        self.系统结算日期 = ''
        self.temp = ''  # 用于保存打开文件的路径
        # self.comboClient = QComboBox() # 店铺的下拉菜单
        client_list = list(readDBConfig.client_Dict.keys())
        self.ui.comboBox.addItem('选择店铺')
        self.ui.comboBox.addItems(client_list)

        # 链接嵌函数
        self.ui.InputButton.clicked.connect(self.getInputFile)
        self.ui.OutputButton.clicked.connect(self.getOutputFile)
        self.ui.UpdateButton.clicked.connect(self.DBupdate)
        self.ui.InsertButton.clicked.connect(self.DBinsert)
        self.ui.ReadButton.clicked.connect(self.DBselect)
        self.ui.comboBox.currentIndexChanged.connect(self.comboboxChange)

    def getInputFile(self):
        self.temp, _ = QFileDialog.getOpenFileName(self, "选择本次订单状态表文件夹路径", '', "Forms(*.xlsx *.csv)") 
        if self.temp != '':
            self.本次状态表输入路径 = self.temp
            self.ui.InputFile.setText(self.本次状态表输入路径)

    def getOutputFile(self):
        self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径")  # 使用本地对话框
        # self.temp = QFileDialog.getExistingDirectory(self, "选择保存路径", '', QFileDialog.DontUseNativeDialog)  # 不使用本地对话框，可以查看文件夹内文件
        if self.temp != '':
            self.最新状态表输出路径 = self.temp
            self.ui.OutputFile.setText(self.最新状态表输出路径)
            
    def printInfo(self, mes):
        self.ui.textBrowser.append(mes)  # 在指定的区域显示提示信息
        self.text_cursor = self.ui.textBrowser.textCursor()
        self.ui.textBrowser.moveCursor(self.text_cursor.End)
        # QWidget.QApplication.processEvents()
        
    def comboboxChange(self):
        """
        当下拉框COMBOBOX被选定选项后后会调用该函数，该函数采用.currentText()获取当前所选文本。
        """
        
        self.选择客户 = self.ui.comboBox.currentText()
        print('下拉框选择了店铺名称%s'%self.选择客户)
        
    def DBinsert(self):
        
        password, okPressed = QInputDialog.getText(self, "授信人员验证","密码:",QLineEdit.Normal,"")
        
        # 验证密码模块
        if not okPressed:
            return
        if not str(password) == '5585':
            QMessageBox.about(self, "报错！", '密码错误！')
            return

        # 防止误操作模块，识别dataframe里的列长度即可

        # 获取输入值
        self.当天日期 = self.ui.Today.text()  # 获取日期
        # self.printInfo(mes = '连接对应数据表成功！程序处理中，请稍后。。。')  
        
        # 输入值为空时
        if self.本次状态表输入路径 == '':
            QMessageBox.about(self, "报错！", '选择本次订单状态表文件夹路径')
            return        
        
        # 通过外部类获取数据
        db_dict = readDBConfig.DB_Dict
        client_dict = readDBConfig.client_Dict
        host = db_dict['host']
        user = db_dict['user']
        password = db_dict['password']
        database = db_dict['database']
        

        # 数据预处理
        try:
            self.当天日 = datetime.datetime.strptime(f'{self.当天日期}','%Y/%m/%d').strftime('%Y-%m-%d')
        except:
            self.当天日 = self.当天日期        
        
        # 打开输入路径对应数据   
        本金表 = pd.read_excel(self.本次状态表输入路径,sheet_name = '已揽收订单表') 
        文件名 = os.path.split(self.本次状态表输入路径)[1] #客户名称-平台名称-表格名称-操作人-备注.xlsx
        文件名前缀 = os.path.splitext(文件名)[0] #
        客户名称 = 文件名前缀.split('-')[0] #
        self.printInfo(mes = '成功读取表格数据！/n正在连接对应数据库，请稍后。。。')

        # 建立字典转译客户名称与店铺数据表名
        table_name =  client_dict[f'{客户名称}']
        
        principal_table = table_name + '_principal'
        # service_table = table_name + '_service'
        
        # 连接数据库
        mysql_ = MysqlDBUtils(host,user,password,database)
        数据库,游标 = mysql_.connect()
        insert_credit = 已授信记录插入(数据库,游标,principal_table,本金表)

        if insert_credit == True:
            self.printInfo(mes='本金数据库状态插入成功!')
        elif insert_credit == False:
            self.printInfo(mes = '本金数据库状态插入失败！')
            QMessageBox.about(self, "授信失败", '授信失败！')


        self.printInfo(mes = '授信操作结束！')

    def DBupdate(self):

        password, okPressed = QInputDialog.getText(self, "运营人员验证", "密码:", QLineEdit.Normal, "")

        # 验证密码模块
        if not okPressed:
            return
        if not str(password) == '0000':
            QMessageBox.about(self, "报错！", '密码错误！')
            return

        # 获取输入值
        self.天数 = self.ui.InputDay.text() #QLineEdit #天数可以设置不超过N天，防止数据库因查询数据量过大缓慢
        self.当天日期 = self.ui.Today.text()  # 获取日期
        # self.printInfo(mes = '连接对应数据表成功！程序处理中，请稍后。。。')  
        
        # 输入值为空时
        if self.本次状态表输入路径 == '':
            QMessageBox.about(self, "报错！", '选择本次订单状态表文件夹路径')
            return        
        
        # 通过外部类获取数据
        db_dict = readDBConfig.DB_Dict
        client_dict = readDBConfig.client_Dict
        host = db_dict['host']
        user = db_dict['user']
        password = db_dict['password']
        database = db_dict['database']

        # 数据预处理
        if self.天数 == '':
            self.天数 = 30
        else:
            try:
                self.天数 = int(self.天数)
            except:
                QMessageBox.about(self, "报错！", '请输入正确天数')
        
        # 数据预处理
        try:
            self.当天日 = datetime.datetime.strptime(f'{self.当天日期}','%Y/%m/%d').strftime('%Y-%m-%d')
        except:
            self.当天日 = self.当天日期        
        
        # 打开输入路径对应数据
        订单全状态表 = pd.read_excel(self.本次状态表输入路径,sheet_name = '订单全状态表')        
        # 本金表 = pd.read_excel(self.本次状态表输入路径,sheet_name = '已揽收订单表') 
        文件名 = os.path.split(self.本次状态表输入路径)[1] #客户名称-平台名称-表格名称-操作人-备注.xlsx
        文件名前缀 = os.path.splitext(文件名)[0] # loose-天猫-账单表-清洗后
        平台类型 = 文件名前缀.split('-')[1] # loose-【天猫】-账单表-清洗后
        客户名称 = 文件名前缀.split('-')[0] # 【loose】-天猫-账单表-清洗后 
        self.printInfo(mes = '成功读取表格数据！/n正在连接对应数据库，请稍后。。。')

        # 建立字典转译客户名称与店铺数据表名
        table_name =  client_dict[f'{客户名称}']
        
        principal_table = table_name + '_principal'
        service_table = table_name + '_service'
        

        # 按照平台作更新
        if 平台类型 == "淘宝" or 平台类型 == "天猫":
            pass




        elif 平台类型 == "快手":

            # 连接数据库
            mysql_ = MysqlDBUtils(host, user, password, database)
            数据库, 游标 = mysql_.connect()
            credit_status = 快手已授信记录更新(数据库, 游标, principal_table, 订单全状态表, self.当天日, self.天数)

            if credit_status == True:
                self.printInfo(mes='本金数据库状态更新完毕!')
            elif credit_status == False:
                self.printInfo(mes='本金数据库状态更新失败！')
                QMessageBox.about(self, "更新失败", '更新失败！')
            print('准备重新连接')

            # 连接数据库
            mysql_ = MysqlDBUtils(host, user, password, database)
            数据库, 游标 = mysql_.connect()
            all_status = 快手订单全状态表插入与更新(数据库, 游标, service_table, 订单全状态表, self.当天日, self.天数)

            if all_status == True:
                self.printInfo(mes='服务费数据库状态更新完毕!')
            elif all_status == False:
                self.printInfo(mes='服务费数据库状态更新失败！')
                QMessageBox.about(self, "更新失败", '更新失败！')

        # self.readDBConfig.关闭连接()
        QMessageBox.about(self, "更新操作结束", '更新操作结束！')


    def DBselect(self):
        
        # 获取输入值
        self.开始日期 = self.ui.StartTime.text()  # 获取日期
        self.结束日期 = self.ui.EndTime.text()  # 获取日期
        self.系统结算日期 =  self.ui.settlementDate.text() # 获取日期
        # 输入值为空时         
        if self.最新状态表输出路径 == '':
            QMessageBox.about(self, "报错！", '选择最新状态表输出路径')
            return        
        if self.选择客户 == '选择店铺':
            QMessageBox.about(self, "报错！", '选择对应店铺')
            return          
       
        # 数据预处理
        try:
            self.开始日 = datetime.datetime.strptime(f'{self.开始日期}','%Y/%m/%d').strftime('%Y-%m-%d')
        except:
            self.开始日 = self.开始日期  
        # 数据预处理
        try:
            self.结束日 = datetime.datetime.strptime(f'{self.结束日期}','%Y/%m/%d').strftime('%Y-%m-%d')
        except:
            self.结束日 = self.结束日期  
        # 数据预处理
        try:
            self.系统结算日 = datetime.datetime.strptime(f'{self.系统结算日期}','%Y/%m/%d').strftime('%Y-%m-%d')
        except:
            self.系统结算日 = self.系统结算日期  
       
            
        # 调用对象属性
        db_dict = readDBConfig.DB_Dict
        client_dict = readDBConfig.client_Dict
        host = db_dict['host']
        user = db_dict['user']
        password = db_dict['password']
        database = db_dict['database']
        
        # 连接数据库
        mysql_ = MysqlDBUtils(host,user,password,database)
        数据库,游标 = mysql_.connect()
        # 获取对应店铺的数据表名称
        table_name = client_dict[self.选择客户]
        principal_table = table_name + '_principal'
        service_table = table_name + '_service'
        平台拼音 = table_name.split('_')[1] # fola_douyin

        if 平台拼音 == 'kuaishou':
            平台名称 = '快手'
        elif 平台拼音 == 'douyin':
            平台名称 = '抖音'
        else:
            平台名称 = '无平台名称'
        
        # 内置数据
        永久列表 = ['订单编号','商品单号','成交数量','订单应付金额','订单创建时间','订单状态','售后状态','售后申请时间','实际结算时间','实际结算金额','预估推广佣金','物流时间','回退状态','统计时间','授信本金']
        list_cols = 永久列表
        len_cols = len(list_cols)
        
        
        #【本金】根据用户输入日期获取那一天结算的订单记录：获取当日实际结算or当日售后时间的，合并，再根据商品单号去重，则得出某日需收回本金的订单依据
        sql_principal = "select %s from {tablename} where DATE({tablename}.订单创建时间) >= \'{StartTime}\' and DATE({tablename}.订单创建时间) <= \'{EndTime}\' and (DATE({tablename}.实际结算时间) = \'{SettlementDate}\' or DATE({tablename}.售后申请时间) = \'{SettlementDate}\') "% ("{},"*(len_cols-1) + "{}")
        sql_principal = sql_principal.format(*list_cols,tablename = principal_table,StartTime = self.开始日,EndTime = self.结束日,SettlementDate = self.系统结算日)
        pricipal_data = convert_Df_from_DataBase(游标,sql_principal)
        print('读取本金部分记录执行SQL语句：%s' % sql_principal)
        # print(pricipal_data)
        #将mysql数据提取出来，转换为xlsx文件,但是需要补充表头！！！
        pricipal_data = dataframe_add_cols_name(pricipal_data,list_cols)
                  
        pricipal_data = pricipal_data.drop_duplicates('商品单号')

        # 内置数据
        永久列表2 = ['订单编号','商品单号','成交数量','订单应付金额','订单创建时间','订单状态','售后状态','售后申请时间','实际结算时间','实际结算金额','预估推广佣金','物流时间','回退状态','统计时间']
        list_cols2 = 永久列表2
        len_cols2 = len(list_cols2)
        
        #【服务费】对于单场次来说就是要获取该场次的全部订单，来评估每个场次的实时退货退款率与约定退货退款率做对比        

        sql_service = "select %s from {tablename} where DATE({tablename}.订单创建时间) >= \'{StartTime}\' and DATE({tablename}.订单创建时间) <= \'{EndTime}\'"% ("{},"*(len_cols2-1) + "{}")
        sql_service = sql_service.format(*list_cols2,tablename = service_table,StartTime = self.开始日,EndTime = self.结束日)
        service_data = convert_Df_from_DataBase(游标,sql_service)
        print('读取服务费部分记录执行SQL语句：%s' % sql_service)
        #将mysql数据提取出来，转换为xlsx文件,但是需要补充表头！！！
        service_data = dataframe_add_cols_name(service_data,list_cols2)

        
        游标.close()
        数据库.close()
        
        输出文件名格式 = f'\\{self.选择客户}-{平台名称}-订单明细表-系统结算日期{self.系统结算日}.xlsx' #可以打算按照数据库对应平台名称，然后内部查字典获取平台名称
        输出路径 = self.最新状态表输出路径 + 输出文件名格式
        
        
        writer = pd.ExcelWriter(输出路径)
        pricipal_data.to_excel(writer, sheet_name='可收本金明细表',index=False)

        service_data.to_excel(writer, sheet_name='可收服务费明细表',index=False)

        writer.save()
        #不用删掉，不然文件短时间内不能编辑，只能读取
        writer.close()
        
        #成功后消息提醒
        QMessageBox.about(self, "处理结果", f'成功！\n请于“{self.最新状态表输出路径}”查看结果文件')

    
if __name__ == '__main__':
    
    # 优先读取配置文件，比如先实例化对象，读取信息，凑成字典，读取时只需要访问对象属性即可
    readDBConfig = ReadDBConfig()
    readDBConfig.set_Client_info()
    readDBConfig.set_DB_info()
    # db_dict = readDBConfig.DB_Dict
    # client_dict = readDBConfig.client_Dict
    # 实例化数据库对象，设置con，cur属性，connect方法，close方法，excute方法(外部数据，SQL语句)

    
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()
    
    
    #优先读取配置文件，比如先实例化对象，读取信息，凑成字典，读取时只需要访问对象属性即可
    #然后实例化数据库对象，设置con，cur属性，connect方法，close方法，excute方法(外部数据，SQL语句)
    #然后打开小工具界面，处理两段业务代码

    """
    1、根据用户输入从数据库中提取一个月内场次的商品单号列，对新输入的table进行分类：待更新与待插入
    2、将待插入写进数据库中，然后释放
    3、将待更新表排除掉回退状态为：待回的，然后获取商品单号列，再次从数据库中读取数据，读取回退状态为：待回、已回，然后转换成表格，然后两表进行对比
    4、再将前后都是已回的记录从待更新中删除，检查一种情况作为异常：待更新：已退，数据库：已回
    5、剩余的待更新直接整体代替数据库中的（不知道会不会影响自增ID）
    """




