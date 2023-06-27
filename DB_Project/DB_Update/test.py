import os
import pandas as pd
import configparser
import pymysql
import datetime as datetime



def DBselect():

    # 调用对象属性
    db_dict = readDBConfig.DB_Dict
    client_dict = readDBConfig.client_Dict
    host = db_dict['host']
    user = db_dict['user']
    password = db_dict['password']
    database = db_dict['database']

    # 连接数据库
    mysql_ = MysqlDBUtils(host, user, password, database)
    数据库, 游标 = mysql_.connect()
    # 获取对应店铺的数据表名称
    table_name = client_dict['TB品牌鞋服']
    principal_table = table_name + '_principal'
    service_table = table_name + '_service'
    平台拼音 = table_name.split('_')[1]  # fola_douyin

    if 平台拼音 == 'kuaishou':
        平台名称 = '快手'
    elif 平台拼音 == 'douyin':
        平台名称 = '抖音'
    else:
        平台名称 = '无平台名称'

    # 内置数据
    永久列表 = ['订单编号', '商品单号', '成交数量', '订单应付金额', '订单创建时间', '订单状态', '售后状态',
                '售后申请时间', '实际结算时间', '实际结算金额', '预估推广佣金', '物流时间', '回退状态', '统计时间',
                '授信本金']
    list_cols = 永久列表
    len_cols = len(list_cols)

    # 【本金】根据用户输入日期获取那一天结算的订单记录：获取当日实际结算or当日售后时间的，合并，再根据商品单号去重，则得出某日需收回本金的订单依据
    sql_principal = "select %s from {tablename}  " % (
                "{}," * (len_cols - 1) + "{}")
    sql_principal = sql_principal.format(*list_cols, tablename=principal_table)
    pricipal_data = convert_Df_from_DataBase(游标, sql_principal)
    print('读取本金部分记录执行SQL语句：%s' % sql_principal)
    # print(pricipal_data)
    # 将mysql数据提取出来，转换为xlsx文件,但是需要补充表头！！！
    pricipal_data = dataframe_add_cols_name(pricipal_data, list_cols)

    pricipal_data = pricipal_data.drop_duplicates('商品单号')

    return pricipal_data


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


def convert_Df_from_DataBase(cur, sql_order):  # sql_order is a string

    """每天从数据库中读取近一个月内的商品单号，转换成dataframe再跟外部excel作比较，进行分组，然后分组操作更新或插入原数据库"""
    try:
        cur.execute(sql_order)  # 多少条记录
        data = cur.fetchall()
        frame = pd.DataFrame(list(data))
        print("successfully! convert_Df_from_DataBase")
    except Exception as e:  # , e:
        frame = pd.DataFrame()
        print("fail convert_Df_from_DataBase", e)
        # print e
        # continue
    return frame


def dataframe_add_cols_name(df, cols_list):
    if not df.empty:
        df.columns = cols_list
    else:
        df = pd.DataFrame(columns=cols_list)

    return df


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

if __name__ == '__main__':
    # 优先读取配置文件，比如先实例化对象，读取信息，凑成字典，读取时只需要访问对象属性即可
    readDBConfig = ReadDBConfig()
    readDBConfig.set_Client_info()
    readDBConfig.set_DB_info()
    data = DBselect()
    data.to_excel(r'C:\Users\Administrator\Desktop\火光全部数据分析\已授信数据.xlsx')