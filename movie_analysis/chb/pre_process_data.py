import pandas as pd


def pre_process_data(movie_name):
    print("===================开始数据清洗======================")
    df = pd.read_excel(movie_name+".xlsx",parse_dates=["time"])  # 读取源数据，将数据解析为时间格式
    df["小时"] = df["time"].map(lambda x: int(x.strftime("%H")))  # 提取小时
    df = df.drop_duplicates()  # 去重
    print("数据去重完毕")
    df = df.dropna(subset=["cityName"])  # 删除城市空值行
    df = df.dropna(subset=["gender"])  # 删除性别空值行
    print("去除空值完毕")
    df.to_excel(movie_name+".xlsx")  # 写入处理后的数据

    print("===================数据清洗完毕======================")
    return df

