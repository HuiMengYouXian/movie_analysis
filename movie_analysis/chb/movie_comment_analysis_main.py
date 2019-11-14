# 调度主模块
import os
import re

from PyQt5 import QtWidgets

from chb.data_analysis import data_analysis
from chb.gen_analy_result import gen_analy_result
from chb.pre_process_data import pre_process_data
from chb.prepare_datat import prepare_data


movie_id = 1211270
movie_name = "哪吒之魔童降世"
df = None

def select_movie(sel_movie_cbx):
    global movie_id  # 提升作用域为全局
    global movie_name

    movie_name = sel_movie_cbx.currentText()
    movie_idx = sel_movie_cbx.currentIndex()

    if movie_idx == 0:
        movie_id = 1211270

    if movie_idx == 1:
        movie_id = 1212592

    print(movie_name, movie_id)


# 下载数据
def down_data(state_label):
    # 1.准备数据
    movie_file = movie_name + ".xlsx"
    if os.path.exists(movie_file):
        print("电影评论文件已经存在")
    else:
        state_label.setText("正在下载数据...")
        prepare_data(movie_id, movie_name)
    state_label.setText("数据准备完毕")


def open_file(MainWindow):
    global movie_name

    file_name, file_type = QtWidgets.QFileDialog.getOpenFileName(MainWindow, "请导入数据", "流浪地球",
                                                                 "xlsx文件 (*.xlsx;*.csv;)")  # 设置文件扩展名过滤,
    print(file_name)
    # 提取文件名
    if file_name:
        s = re.search(r'([\u4E00-\u9FA5]+).xlsx', file_name)
        movie_name = s.group(1)
        print(movie_name)


# 数据清洗
def pre_data(state_label):
    # 2.数据预处理
    global df

    df = pre_process_data(movie_name)
    state_label.setText("数据清洗完毕")

# 数据分析
def movie_analysis(wc_view, state_label):
    # 3.各项数据分析
    df_result = data_analysis(df)
    # 4.可视化与生成分析结果
    gen_analy_result(df_result, df, movie_name, wc_view, state_label)

    print("Done")

