import os

import numpy as np
import pandas as pd
import DB_until



def progress_bar(total, current):
    bar_length = 50
    filled_length = int(bar_length * current / total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    percent = current / total * 100
    print(f'\r上传中: |{bar}| {percent:.1f}%', end='')


def commit_data(db_manager,新处理):
    total_iterations = len(新处理)
    query = "SELECT * FROM journal_shop"
    results = db_manager.fetch_all(query)
    primary_key = []
    for row in results:
        primary_key.append(str(row[0]) + str(row[1]) + str(row[2]))

    add_sql = (
        "INSERT INTO journal_shop (sale_date,platform_name,store_name,statistical_sales_amount,statistical_refund_amount,statistical_return_amount,statistical_remaining_sales_amount,statistical_platform_online_commission,statistical_platform_fee,statistical_repaid_amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    add_values = []
    update_sql = (
        "update journal_shop set statistical_sales_amount = %s,statistical_refund_amount = %s,statistical_return_amount = %s,statistical_remaining_sales_amount = %s,statistical_platform_online_commission = %s,statistical_platform_fee = %s,statistical_repaid_amount = %s where sale_date = %s and platform_name = %s and store_name = %s")
    update_values = []
    count = 0
    # 插入数据到数据库表（假设表名为 your_table）
    for index, row in 新处理.iterrows():
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

    if len(add_values) != 0:
        db_manager.executemany_query(add_sql, add_values)
    elif len(add_values) == 1:
        db_manager.execut_query(add_sql, add_values)

    if len(update_sql) != 0:
        db_manager.executemany_query(update_sql, update_values)
    elif len(add_values) == 1:
        db_manager.execut_query(update_sql, update_values)

    print("\n添加数据"+str(len(add_values))+"条,更新数据"+str(len(update_values)) +"条")
    db_manager.commit()


def generate_table(path,output_path):
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
                print("文件数据有误",e)
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
    # 处理.to_excel("处理.xlsx")
    # print(处理[("sum","实际结算金额")])
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
    commit_data(db_manager,新处理)

    db_manager.close()

    # 达人销售数据监控处理



    # 输出
    if output_path != "":
        try:
            新处理[新处理.平台.isin([platform[0]])].to_excel("店铺日报数据.xlsx", sheet_name=platform[0] + "-" + shop_name[0])
            if len(shop_name) > 1:
                count = 0
                for name in shop_name[1:]:
                    count += 1
                    with pd.ExcelWriter("店铺日报数据.xlsx", mode='a') as writer:
                        新处理[新处理.平台.isin([platform[count]]) & 新处理.店铺.isin([shop_name[count]])].to_excel(writer, sheet_name=platform[count]+"-"+shop_name[count])
        except Exception as e:
            print("输出文件发生错误！",e)


if __name__ == "__main__":
    generate_table("C:/Users/26774/Desktop/熔视界9月6日","")