import pandas as pd

class CommonUtil():
    def 读取表格(path,name):
        # 路径+文件名
        文件位置 = path+'\\'+name
        if 'xlsx' in name:
            try:
                return pd.read_excel(文件位置,dtype=str);
            except(UnicodeDecodeError):
                return pd.read_excel(文件位置,dtype=str, encoding='GB18030')
        elif 'csv' in name:
            try:
                return pd.read_csv(文件位置,dtype=str);
            except(UnicodeDecodeError):
                return pd.read_csv(文件位置,dtype=str, encoding='GB18030')
