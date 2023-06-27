
import configparser
import pandas as pd
import pymysql
import datetime as datetime
import os


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

    """每天从数据库中读取数据并转换成DataFrame"""
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

def readRepeatPrincipalDB(游标,principal_table,永久列表):


    list_cols = 永久列表
    len_cols = len(list_cols)

    # 参考SELECT * FROM `tbshoesandclothing_kuaishou_principal` a WHERE ((SELECT COUNT(*) FROM `tbshoesandclothing_kuaishou_principal` WHERE 订单编号 = a.订单编号) > 1) ORDER BY 订单编号 DESC;
    sql_principal = "select %s from {tablename}  Prin where ((select count(*) from {tablename} where 订单编号 = Prin.订单编号) > 1)" % ("{}," * (len_cols - 1) + "{}")
    sql_principal = sql_principal.format(*list_cols,tablename = principal_table)
    pricipal_data = convert_Df_from_DataBase(游标, sql_principal)

    # 将mysql数据提取出来，转换为xlsx文件,但是需要补充表头！！！
    pricipal_data = dataframe_add_cols_name(pricipal_data, list_cols)

    return pricipal_data

def readPrincipalDB(游标,principal_table,永久列表):


    list_cols = 永久列表
    len_cols = len(list_cols)

    # 参考SELECT * FROM `tbshoesandclothing_kuaishou_principal` a WHERE ((SELECT COUNT(*) FROM `tbshoesandclothing_kuaishou_principal` WHERE 订单编号 = a.订单编号) > 1) ORDER BY 订单编号 DESC;
    sql_principal = "select %s from {tablename} " % ("{}," * (len_cols - 1) + "{}")
    sql_principal = sql_principal.format(*list_cols,tablename = principal_table)
    pricipal_data = convert_Df_from_DataBase(游标, sql_principal)

    # 将mysql数据提取出来，转换为xlsx文件,但是需要补充表头！！！
    pricipal_data = dataframe_add_cols_name(pricipal_data, list_cols)

    return pricipal_data

if __name__ == '__main__':
    # 优先读取配置文件，比如先实例化对象，读取信息，凑成字典，读取时只需要访问对象属性即可
    readDBConfig = ReadDBConfig()
    readDBConfig.set_Client_info()
    readDBConfig.set_DB_info()
    # db_dict = readDBConfig.DB_Dict
    # client_dict = readDBConfig.client_Dict
    # 实例化数据库对象，设置con，cur属性，connect方法，close方法，excute方法(外部数据，SQL语句)
    # 通过外部类获取数据

    db_dict = readDBConfig.DB_Dict
    client_dict = readDBConfig.client_Dict
    host = db_dict['host']
    user = db_dict['user']
    password = db_dict['password']
    database = db_dict['database']
    # 建立字典转译客户名称与店铺数据表名
    客户名称 = 'TB品牌鞋服'

    table_name = client_dict[f'{客户名称}']

    principal_table = table_name + '_principal'
    service_table = table_name + '_service'
    # 内置数据
    principal_table_list = ['订单编号', '商品单号', '成交数量', '订单应付金额', '订单创建时间', '订单状态', '售后状态',
                '售后申请时间', '实际结算时间', '实际结算金额', '预估推广佣金', '物流时间', '回退状态', '统计时间',
                '授信本金']
    service_table_list = ['订单编号', '商品单号', '成交数量', '订单应付金额', '订单创建时间', '订单状态', '售后状态',
                '售后申请时间', '实际结算时间', '实际结算金额', '预估推广佣金', '物流时间', '回退状态', '统计时间',]
    # 连接数据库
    mysql_ = MysqlDBUtils(host, user, password, database)
    con, cursor = mysql_.connect()

    data = readPrincipalDB(cursor,principal_table,principal_table_list)

    data.to_excel(r'C:\Users\Administrator\Desktop\数据库读取表格\排除5万.xlsx',index=False)

    cursor.close()  # 先关闭游标
    con.close()  # 再关闭数据库