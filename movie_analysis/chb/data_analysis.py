from datetime import datetime

def data_analysis(df_comment):
    print("===================开始数据分析======================")

    df_comment_list = []
    df_score = df_comment.groupby(["cityName"])['score']  # 按城市分组
    df_gen_score = df_comment.groupby(["gender"])['score']  # 按性别分组
    df_time_score = df_comment.groupby(["time"])['time']  # 按时间分组
    time_count = df_comment.groupby("小时")["nick"].agg(['count'])  # 提取时间段

    comment_gender_sum = df_gen_score.agg(['sum'])  # 评分中男女总数
    df_comment_list.append(comment_gender_sum)
    comment_time_count = df_time_score.agg(['count'])  # 评分中日期计数
    comment_score_mean_count = df_score.agg(['mean', 'count'])  # 评分中各个城市的平均分、数量

    # 重新设置索引  inplace改变原来的
    comment_score_mean_count.reset_index(inplace=True)
    comment_score_mean_count['mean'] = round(comment_score_mean_count['mean'],2)
    df_comment_list.append(comment_score_mean_count)
    df_comment_list.append (comment_time_count)

    df_score = df_comment.groupby(["score"])
    df_score_nick = df_score["nick"]
    score_count = df_score_nick.agg(['count'])
    df_comment_list.append(score_count)
    df_comment_list.append(time_count)
    print("===================数据分析完毕======================")
    return df_comment_list

