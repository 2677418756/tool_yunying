import pandas as pd

class CommonUtil():
    def 读取表格(self, path, name):
        # 路径+文件名
        文件位置 = path + '\\' + name
        data = pd.DataFrame()
        if 'xlsx' in name:
            try:
                data = pd.read_excel(文件位置, dtype=str).rename(columns=lambda x: x.strip())
            except(UnicodeDecodeError):
                data = pd.read_excel(文件位置, dtype=str, encoding='GB18030').rename(columns=lambda x: x.strip())
        elif 'csv' in name:
            try:
                data = pd.read_csv(文件位置, dtype=str).rename(columns=lambda x: x.strip())
            except(UnicodeDecodeError):
                data = pd.read_csv(文件位置, dtype=str, encoding='GB18030').rename(columns=lambda x: x.strip())
        data = data.replace('\t', '', regex=True).replace('\n', '', regex=True)
        return data