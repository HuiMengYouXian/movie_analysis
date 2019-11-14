# movie_analysis
## 简介
为了了解观看热门电影的用户都有哪些特征，爬取猫眼网站热门电影的评论数据进行分析：评分统计、词云、城市评论数量与平均评分、性别分析、评论数量与时间的关系。

## 开发环境Python-v3(3.6)
-pandas==0.25.1
-numpy==1.17.2
-jieba==0.39
-wordcloud==1.5.0
-matplotlib==2.2.2
-imageio==2.3.0
-requests==2.18.4
另外还需安装pyqt5

## 模块介绍
1.下载爬取数据：prepare_datat.py

2.数据预处理：pre_process_data.py

3.数据分析：data_analysis.py

4.数据可视化与成果生成：gen_analy_result.py

5.调度数据分析各模块的主模块：movie_comment_analysis_main.py

## 用法
  下载movie_analysis项目到本地，PyCharm导入项目并配好运行环境以及安装上述依赖包，运行Main.py，出现如下界面：
  ![image](https://github.com/HuiMengYouXian/movie_analysis/blob/master/image-folder/%E5%88%9D%E5%A7%8B.png)

  此时有两种选择：

  1.没有影评数据，需要下载影评

  ![image](https://github.com/HuiMengYouXian/movie_analysis/blob/master/image-folder/%E4%B8%8B%E8%BD%BD%E5%BD%B1%E8%AF%84.png)

  2.有影评数据，选择导入文件

  ![image](https://github.com/HuiMengYouXian/movie_analysis/blob/master/image-folder/%E5%AF%BC%E5%85%A5%E6%96%87%E4%BB%B6.png)
