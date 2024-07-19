import pandas as pd

data = pd.read_excel("D:/work/code/test/熔视界7月2日/抖音-MVAV鞋服工厂店/1、源文件/抖音-联盟表.xlsx")
# 获取第一列的数据(不包含表头)
print(data[data.columns[0]])
print("*"*100)
# 获取表头
print(len(data.columns))
print("*"*100)
# 获取第一列第一个数据
print(data[data.columns[0]][0])
print("*"*100)

# 根据列名获取列号
print(data.columns.get_loc("商品id"))

# 修改A1的值[行，列]
data.iloc[0, 1] = 1
data.to_excel('D:/work/code/test/熔视界7月2日/抖音-MVAV鞋服工厂店/1、源文件/抖音-联盟表.xlsx', index=False)


