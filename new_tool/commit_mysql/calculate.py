import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import DB_until
# 不可删除，否则打包会报错
import mysql.connector.plugins.mysql_native_password



def progress_bar(total, current):
    bar_length = 50
    filled_length = int(bar_length * current / total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    percent = current / total * 100
    print(f'\r上传中: |{bar}| {percent:.1f}%', end='')


def commit_yesterday_data(db_manager,data):
    # 清空数据库
    db_manager.execute_query("delete from yesterday_data")

    total_iterations = len(data)
    add_sql = "INSERT INTO yesterday_data (id,platform_name,store_name,goods_name,sales_amount,talent_id,talent_name) VALUES ( default,%s, %s, %s, %s, %s, %s)"
    add_values = []
    count = 0
    for index, row in data.iterrows():
        add_values.append((
            row["平台"], row["店铺"], row["商品名称"], row["订单应付金额"], row["达人ID"], row["达人昵称"]
        ))
        count += 1
        progress_bar(total_iterations, index + 1)
    if len(add_values) == 1:
        db_manager.execute_query(add_sql, add_values[0])
    elif len(add_values) != 0:
        db_manager.executemany_query(add_sql, add_values)

    print("\n添加数据"+str(len(add_values))+"条")
    db_manager.commit()
    return "添加数据"+str(len(add_values))+"条\n"


def commit_data(db_manager,新处理,type):
    total_iterations = len(新处理)

    query = ["SELECT * FROM journal_shop","SELECT * FROM journal_talent"]
    if(type in [0,1]):
        results = db_manager.fetch_all(query[type])
        primary_key = []
        for row in results:
            primary_key.append(str(row[0+type]) + str(row[1+type]) + str(row[2+type]))

    add_sql = [
        ("INSERT INTO journal_shop (sale_date,platform_name,store_name,statistical_sales_amount,statistical_refund_amount,statistical_return_amount,statistical_remaining_sales_amount,statistical_platform_online_commission,statistical_platform_fee,statistical_repaid_amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"),
        ("INSERT INTO journal_talent (talent_id,platform_name,store_name,talent_name,statistical_sales_amount,statistical_refund_amount,statistical_return_amount,statistical_remaining_sales_amount) VALUES ( %s,%s, %s, %s, %s, %s, %s, %s)"),
    ]
    add_values = []
    update_sql = [
        ("update journal_shop set statistical_sales_amount = %s,statistical_refund_amount = %s,statistical_return_amount = %s,statistical_remaining_sales_amount = %s,statistical_platform_online_commission = %s,statistical_platform_fee = %s,statistical_repaid_amount = %s where sale_date = %s and platform_name = %s and store_name = %s"),
        ("update journal_talent set talent_name = %s, statistical_sales_amount = %s,statistical_refund_amount = %s,statistical_return_amount = %s,statistical_remaining_sales_amount = %s where talent_id = %s and platform_name = %s and store_name = %s")
    ]
    update_values = []
    count = 0
    # 插入数据到数据库表（假设表名为 your_table）
    for index, row in 新处理.iterrows():
        if type == 0:
            if (str(row["销售日期"]+row["平台"]+row["店铺"])) in primary_key:
                update_values.append((
                     row["统计销售额"], row["统计退款金额"], row["统计退货金额"],row["统计当前剩余销售额"], row["统计平台线上佣金"],
                     row["统计平台费用"], row["统计已回款金额"],row["销售日期"], row["平台"], row["店铺"]))
                count += 1
                progress_bar(total_iterations, index + 1)
            else:
                add_values.append((
                    row["销售日期"], row["平台"], row["店铺"], row["统计销售额"], row["统计退款金额"], row["统计退货金额"],
                    row["统计当前剩余销售额"], row["统计平台线上佣金"], row["统计平台费用"], row["统计已回款金额"]))
                count += 1
                progress_bar(total_iterations, index + 1)
        elif type == 1:
            if (str(row["达人ID"]+row["平台"])+row["店铺"]) in primary_key:
                update_values.append((
                    row["达人昵称"],row["订单应付金额"], row["统计退款金额"], row["统计退货金额"],row["统计当前剩余销售额"],row["达人ID"], row["平台"],row["店铺"]))
                count += 1
                progress_bar(total_iterations, index + 1)
            else:
                add_values.append((
                    row["达人ID"], row["平台"], row["店铺"],row["达人昵称"], row["订单应付金额"], row["统计退款金额"], row["统计退货金额"],row["统计当前剩余销售额"]))
                count += 1
                progress_bar(total_iterations, index + 1)

    if len(add_values) == 1:
        db_manager.execute_query(add_sql[type], add_values)
    elif len(add_values) != 0:
        db_manager.executemany_query(add_sql[type], add_values)

    if len(update_values) == 1:
        db_manager.execute_query(update_sql[type], update_values)
    elif len(update_values) != 0:
        db_manager.executemany_query(update_sql[type], update_values)

    print("\n添加数据"+str(len(add_values))+"条,更新数据"+str(len(update_values)) +"条")
    db_manager.commit()
    return "添加数据"+str(len(add_values))+"条,更新数据"+str(len(update_values)) +"条\n"


def generate_table(path,output_path):
    error_info = ""
    files = os.listdir(path)
    全状态表 = pd.DataFrame()
    shop_name =[]
    platform =[]
    for file in files:
        if ".xlsx" in file and "~$" not in file:
            try:
                shop_name.append(file.split("-")[0])
                platform.append(file.split("-")[1])
                data = pd.read_excel(path+"/"+file,dtype=str)
            except Exception as e:
                error_info+="读取文件发生错误！\n"
            全状态表 = pd.concat([全状态表,data])
    print("读取成功，共"+str(len(全状态表))+"条数据")
    全状态表 = 全状态表[~全状态表.订单创建时间.isna()]
    全状态表["订单应付金额"] = 全状态表["订单应付金额"].astype(float)
    全状态表["实际结算金额"] = 全状态表["实际结算金额"].astype(float)
    全状态表["预估推广佣金"] = 全状态表["预估推广佣金"].astype(float)
    全状态表["销售日期"] = 全状态表["订单创建时间"].apply(lambda x:str(x)[:10])


    全状态表['统计退款金额'] = np.where(全状态表['物流时间'].isin(["2000-01-01 00:00:00"]) & 全状态表['回退状态'].isin(["已退","回退"]),
                                              全状态表['订单应付金额'],0)
    全状态表['统计退货金额'] = np.where(~全状态表['物流时间'].isin(["2000-01-01 00:00:00"]) & 全状态表['回退状态'].isin(["已退","回退"]),
                                              全状态表['订单应付金额'],0)
    全状态表['统计平台线上佣金'] = np.where(~全状态表['物流时间'].isin(["2000-01-01 00:00:00"]) & 全状态表['回退状态'].isin(["已回","待回"]),
                                              全状态表['预估推广佣金'],0)
    全状态表['统计已回款金额'] = np.where(~全状态表['物流时间'].isin(["2000-01-01 00:00:00"]) & 全状态表['回退状态'].isin(["已回","待回","已回部分退"]),
                                              全状态表['实际结算金额'],0)

    # 统计销售额
    处理 = pd.pivot_table(
        全状态表,
        index=['销售日期','平台','店铺'],
        values=['订单应付金额','统计退款金额','统计退货金额','统计平台线上佣金','统计已回款金额'],
        aggfunc=[np.sum]
    )
    处理 = 处理.reset_index()
    新处理 = pd.DataFrame()
    新处理[["销售日期","平台","店铺"]] = 处理[["销售日期","平台","店铺"]]
    新处理["统计销售额"] = 处理[("sum","订单应付金额")]
    新处理["统计退款金额"] = 处理[("sum","统计退款金额")]
    新处理["统计退货金额"] = 处理[("sum","统计退货金额")]
    新处理["统计当前剩余销售额"] = 新处理["统计销售额"] - 新处理["统计退款金额"] - 新处理["统计退货金额"]
    新处理["统计平台线上佣金"] = 处理[("sum","统计平台线上佣金")]

    新处理["统计平台费用"] = 新处理["统计当前剩余销售额"]*0.05 + 新处理["统计平台线上佣金"]
    新处理["统计已回款金额"] = 处理[("sum","统计已回款金额")]

    db_manager = DB_until.DatabaseManager('localhost', "3306", 'root', 'root','yunying')

    db_manager.connect()
    try:
        error_info+="店铺日报上传成功！"+commit_data(db_manager,新处理,0)+"\n"
    except:
        error_info += "店铺日报上传失败！\n"




    # 达人销售数据监控处理
    达人_处理 = pd.pivot_table(
        全状态表[~全状态表.达人ID.isin(["0"])],
        index=['平台','店铺','达人ID'],
        values=['达人昵称','订单应付金额','统计退款金额',"统计退货金额"],
        aggfunc={'达人昵称':lambda x: x.iloc[0],'订单应付金额':np.sum,'统计退款金额':np.sum,'统计退货金额':np.sum}
    )
    达人_处理 = 达人_处理.reset_index()
    达人_处理 = 达人_处理.fillna("")
    达人_处理["统计当前剩余销售额"] = 达人_处理["订单应付金额"] - 达人_处理["统计退款金额"] - 达人_处理["统计退货金额"]
    try:
        error_info+="达人监控上传成功！"+commit_data(db_manager, 达人_处理,1)+"\n"
    except:
        error_info += "达人监控上传失败！\n"


    # 昨日销售情况处理
    yesterday = (datetime.now() - timedelta(days=1)).date()
    昨日_数据 = 全状态表[全状态表.销售日期.isin([str(yesterday)])]
    # 昨日_数据 = 全状态表

    昨日_处理_达人 = pd.pivot_table(
        昨日_数据,
        index=['店铺','平台','达人ID'],
        values=['达人昵称','订单应付金额'],
        aggfunc={'达人昵称':lambda x: x.iloc[0],'订单应付金额':np.sum}
    )
    try:
        昨日_处理_达人['达人昵称']
    except:
        昨日_处理_达人['达人昵称'] = ""
    try:
        昨日_处理_达人['订单应付金额']
    except:
        昨日_处理_达人['订单应付金额'] = 0
    昨日_处理_达人 = 昨日_处理_达人.reset_index()
    昨日_处理_达人 = 昨日_处理_达人.loc[昨日_处理_达人.groupby(['平台', '店铺'])['订单应付金额'].idxmax()]


    昨日_处理_达人["用于合并"] = 昨日_处理_达人['店铺'] + 昨日_处理_达人['平台']

    昨日_处理_商品 = pd.pivot_table(
        昨日_数据,
        index=['店铺','平台','商品名称'],
        values=['订单应付金额'],
        aggfunc={'订单应付金额':np.sum}
    )
    昨日_处理_商品 = 昨日_处理_商品.reset_index()
    try:
        昨日_处理_达人['商品名称']
    except:
        昨日_处理_达人['商品名称'] = ""
    try:
        昨日_处理_达人['订单应付金额']
    except:
        昨日_处理_达人['订单应付金额'] = 0
    昨日_处理_商品 = 昨日_处理_商品.loc[昨日_处理_商品.groupby(['平台', '店铺'])['订单应付金额'].idxmax()]
    昨日_处理_商品["用于合并"] = 昨日_处理_商品['店铺'].astype(str) + 昨日_处理_商品['平台'].astype(str)

    昨日_处理_销售额 = 新处理[新处理.销售日期.isin([str(yesterday)])]
    昨日_处理_销售额["用于合并"] = 昨日_处理_销售额['店铺'] + 昨日_处理_销售额['平台']
    昨日_处理 = pd.merge(昨日_处理_商品, 昨日_处理_达人[["用于合并","达人ID","达人昵称"]], how='left', left_on='用于合并',right_on='用于合并')
    昨日_处理 = pd.merge(昨日_处理, 昨日_处理_销售额[["用于合并","统计销售额"]], how='left', left_on='用于合并',right_on='用于合并')

    昨日_处理 = 昨日_处理.fillna("")
    try:
        error_info+="昨日数据上传成功！"+commit_yesterday_data(db_manager, 昨日_处理)+"\n"
    except:
        error_info += "昨日数据上传失败！\n"

    db_manager.close()
    # 输出
    if output_path != "":
        try:
            新处理[新处理.平台.isin([platform[0]])].to_excel(output_path+"/店铺日报数据.xlsx", sheet_name=platform[0] + "-" + shop_name[0],index=False)
            if len(shop_name) > 1:
                count = 0
                for name in shop_name[1:]:
                    count += 1
                    with pd.ExcelWriter(output_path+"/店铺日报数据.xlsx", mode='a') as writer:
                        新处理[新处理.平台.isin([platform[count]]) & 新处理.店铺.isin([shop_name[count]])].to_excel(writer, sheet_name=platform[count]+"-"+shop_name[count],index=False)
            with pd.ExcelWriter(output_path+"/店铺日报数据.xlsx", mode='a') as writer:
                达人_处理.rename(columns={'订单应付金额':'统计销售额'},inplace = True)
                达人_处理["佣金比例（团长）"] = ""
                达人_处理["佣金比例（达人）"] = ""
                达人_处理["统计佣金金额（团长）"] = ""
                达人_处理["统计佣金金额（达人）"] = ""

                达人_处理[["平台","达人ID","达人昵称","统计销售额","统计退款金额","统计退货金额","统计当前剩余销售额"
                           ,"佣金比例（团长）","佣金比例（达人）","统计佣金金额（团长）","统计佣金金额（达人）"]].to_excel(writer, sheet_name="达人销售数据监控",index=False)
            error_info += "文件导出成功！\n"
        except:
            error_info += "导出文件发生错误!\n"

    return error_info



if __name__ == "__main__":
    generate_table("C:/Users/26774/Desktop/熔视界9月11日","")