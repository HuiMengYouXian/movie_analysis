import collections
import os
import numpy as np
from datetime import datetime
import imageio
# 中文分词
import jieba
# 词云模块
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtGui import QPixmap
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt

# 解决中文乱码问题
plt.rcParams["font.sans-serif"] = "SimHei"
fig = plt.figure(figsize=(8, 6))

url_city = None
url_gen = None
url_score = None
url_scatter = None
url_stack = None

# TAB布局显示
def tab_view(tabWidget, city_view, gen_view, score_view, scatter_view, stack_view):
    index = tabWidget.currentIndex()
    if index == 1:
        # QPixmap解析图片
        pixmap = QPixmap(url_city)
        # 等比例缩放图片
        scaredPixmap = pixmap.scaled(QSize(500, 500), aspectRatioMode=Qt.KeepAspectRatio)
        city_view.setPixmap(scaredPixmap)
    if index == 2:
        pixmap = QPixmap(url_gen)
        scaredPixmap = pixmap.scaled(QSize(500, 500), aspectRatioMode=Qt.KeepAspectRatio)
        gen_view.setPixmap(scaredPixmap)
    if index == 3:
        pixmap = QPixmap(url_score)
        scaredPixmap = pixmap.scaled(QSize(500, 500), aspectRatioMode=Qt.KeepAspectRatio)
        score_view.setPixmap(scaredPixmap)
    if index == 4:
        pixmap = QPixmap(url_scatter)
        scaredPixmap = pixmap.scaled(QSize(500, 500), aspectRatioMode=Qt.KeepAspectRatio)
        scatter_view.setPixmap(scaredPixmap)
    if index == 5:
        pixmap = QPixmap(url_stack)
        scaredPixmap = pixmap.scaled(QSize(500, 500), aspectRatioMode=Qt.KeepAspectRatio)
        stack_view.setPixmap(scaredPixmap)


def gen_analy_result(df_result, df_source, movie_name, wc_view, state_label):
    print("===================开始生成结果======================")
    # 生成词云
    gen_wordcloud(df_source, movie_name, wc_view)
    # 生成折线图、柱状图、网页的函数
    draw_plot_bar(df_result, movie_name)
    draw_pie(df_result, movie_name)
    drwa_bar(df_result, movie_name)
    draw_scatter(df_result, movie_name)
    draw_stackplot(df_result, movie_name)
    state_label.setText("结果生成完毕")
    print("===================结果生成完毕======================")


# 气泡图
def draw_scatter(df_result, movie_name):
    global url_scatter
    city_result = df_result[1]
    city_main = city_result.sort_values("count", ascending=False)[0:10]
    # 建立坐标系
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # 指明x和y的值
    x = np.array(city_main['count'].tolist())  # 城市评论数做x轴
    y = np.array(city_main['mean'].tolist())  # 城市平均分做y轴
    # 绘图
    colors = y * 10  # 根据y值的大小生成不同的颜色
    area = y * 100  # 据y值的大小生成大小不同的形状
    ax1.scatter(x, y, marker="o", s=area, c=colors)
    # 设置标题
    ax1.set_title("城市评论数量与评分关系图", loc="center")

    # 添加数据标签 ha水平方向  va垂直方向
    for a, b in zip(x, y):
        plt.text(a, b, b, ha="center", va="center", fontsize=12, color="white")
    # 设置x轴和y轴
    ax1.set_xlabel('评论数量')
    ax1.set_ylabel('平均分')
    # 设置网格线
    plt.grid(False)
    url_scatter = movie_name + "scatter.jpg"
    fig.savefig(url_scatter)


# 词云函数
def gen_wordcloud(df_source, movie_name, wc_view):
    # 把所有评论串在一起，用空格分隔
    full_comment = " ".join(df_source["content"])
    # 分词
    word_list = []
    # cut_for_search搜索引擎模式：在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词
    words_gen = jieba.cut_for_search(full_comment)  # 返回的是生成器
    for w in words_gen:
        word_list.append(w)
    word_list = [k for k in word_list if len(k) > 1]  # 过滤只有一个词的评论
    print(word_list)

    # imageio导入照片功能比较好用，可以导入很多格式类型的图片
    if movie_name == "流浪地球":
        bg_color = imageio.imread("地球图片.jpg")
    elif movie_name == "大话西游":
        bg_color = imageio.imread("星爷.jpg")
    elif movie_name == "哪吒之魔童降世":
        bg_color = imageio.imread("哪吒.jpg")
    else:
        bg_color = imageio.imread("草莓.jpg")

    # WordCloud可以将文本中词语出现的频率作为一个参数绘制词云，而词云的大小、颜色、形状等都是可以设定的
    # 设置对象
    wc = WordCloud(background_color='white',  # 背景颜色
                   max_words=200,  # 最大词数
                   mask=bg_color,  # 设置词云形状  以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
                   max_font_size=300,  # 显示字体的最大值
                   font_path="simfang",  # 指定字体路径，系统字体路径：C:\Windows\Fonts
                   random_state=42,  # 为每个词返回一个PIL颜色
                   )

    # 统计列表元素出现次数，返回的数据中键对应词，值对应出现次数，例如：Counter({'blue': 3, 'red': 2, 'green': 1})
    counter = collections.Counter(word_list)
    # wc对象的生成器的词频
    wc.generate_from_frequencies(counter)  # frequencies频率
    print("================词云已生成================")
    # 从图片中取色
    image_colors = ImageColorGenerator(bg_color)  # 从图片中取色
    plt.figure()  # 创建画布
    plt.imshow(wc.recolor(color_func=image_colors))  # 绘制图像
    plt.axis("off")  # 关闭坐标轴
    wc.to_file(os.path.join(movie_name + "词云.jpg"))  # 生成词云图片
    print("================词云图片已生成================")
    # 将词云添加到主界面
    # QPixmap解析图片
    pixmap = QPixmap(movie_name + "词云.jpg")
    # 等比例缩放图片
    scaredPixmap = pixmap.scaled(QSize(400,400), aspectRatioMode=Qt.KeepAspectRatio)
    # 设置图片
    wc_view.setPixmap(scaredPixmap)
    # 判断选择的类型 根据类型做相应的图片处理
    print("显示词云图片")


# 评分统计
def drwa_bar(df_result, movie_name):
    global url_score
    # 建立坐标系
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # 指明x和y的值
    score_result = df_result[3]
    x = np.array(score_result.index)
    y = np.array(score_result['count'].tolist())  # 评论平均分作为折线图的Y轴
    # 绘制柱状图
    ax1.bar(x, y, color="r", label="评分数量")
    # 设置标题
    ax1.set_title(movie_name + "评分统计", loc="center")
    # 添加数据标签
    for a, b in zip(x, y):  # zip()需是np.array()
        ax1.text(a, b, b, ha="center", va="bottom", fontsize=11)
    # 设置x轴和y轴的名称
    ax1.set_xlabel('星级')
    ax1.set_ylabel('数量')
    # 设置x轴和y轴的刻度
    ax1.set_xticks(np.arange(0, 6, 1))
    ax1.set_yticks(np.arange(100, 600, 100))
    # 显示图例
    ax1.legend()
    # 保存图表到本地
    url_score = movie_name + "bar.jpg"
    fig.savefig(url_score)


# 城市分析
def draw_plot_bar(df_result, movie_name):
    print("=====================开始绘制城市分析图====================")
    global url_city
    # 建立坐标系
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # 指明x和y的值
    city_result = df_result[1]
    city_main = city_result.sort_values("count", ascending=False)[0:10]  # 取前10
    x = city_main['cityName'].tolist()
    y1 = city_main['mean'].tolist()  # 评论平均分作为折线图的Y轴
    y2 = city_main['count'].tolist()  # 评论数量作为柱状图的Y轴
    # 直接绘制折线图和柱形图
    ax1.plot(x, y1, color="r", linestyle="solid", linewidth=1, marker="o", markersize=3, label="平均评分")
    ax1.bar(x, y2, color="b", label="评论数量")
    # 设置标题
    ax1.set_title(movie_name+"-TOP10城市评论数量与平均评分", loc="center")
    # 添加数据标签
    for a, b in zip(x, y1):
        ax1.text(a, b, b, ha="center", va="bottom", fontsize=11)
    for a, b in zip(x, y2):
        ax1.text(a, b, b, ha="center", va="bottom", fontsize=11)
    # 设置x轴和y轴的名称
    ax1.set_xlabel('城市')
    ax1.set_ylabel('评论数量')
    # 设置x轴和y轴的刻度
    ax1.set_xticks(np.arange(0,10,1))
    ax1.set_yticks(np.arange(10, 60, 10))
    # 显示图例
    ax1.legend()
    # 保存图表到本地
    url_city = movie_name + "bar_plot.jpg"
    fig.savefig(url_city)
    print("=====================绘制城市分析图完毕====================")


# 性别分析
def draw_pie(df_result, movie_name):
    global url_gen
    genter_result = df_result[0]
    # 建立坐标系
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # 指明x值
    x = np.array(genter_result['sum'])
    lab = genter_result.index
    if lab[0] == 1:
        gen1 = "男"
    else:
        gen1 = "女"
    if lab[1] == 2:
        gen2 = "女"
    else:
        gen2 = "男"
    labels = [gen1, gen2]
    explode = [0, 0]
    labeldistance = 1.1  # 标签距离
    # autopct百分比格式  shadow是否有阴影  radius半径
    ax1.pie(x, labels=labels, autopct="%.0f%%", explode=explode, radius=1.0, labeldistance=labeldistance)
    # 设置标题
    ax1.set_title(movie_name+"评分男女占比", loc="center")
    # 保存图表到本地
    url_gen = movie_name + "pie.jpg"
    fig.savefig(url_gen)


# 面积图
def draw_stackplot(df_result, movie_name):
    global url_stack
    time_result = df_result[4]
    print(time_result)
    print(type(time_result))
    # 建立坐标系
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    # 指明x和y的值
    print("00")
    print(time_result.index)
    x = np.array(time_result.index)
    y = np.array(time_result['count'].tolist())
    # 绘图
    print("11")
    ax1.stackplot(x, y, labels="评论数量")
    # 设置标题
    ax1.set_title("评论数量与时间的关系图", loc="center")
    # 设置x轴和y轴名称
    ax1.set_xlabel('时间/小时')
    ax1.set_ylabel('评论数量')
    # 设置网格线
    plt.grid(False)
    # 显示图例
    ax1.legend()
    url_stack = movie_name + "stack.jpg"
    fig.savefig(url_stack)