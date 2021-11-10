# # 定时任务
# import schedule
# import time

# # 导入业务逻辑
# # 导入的py文件中的函数是否可以直接使用
# import htf_fund_comment

# def job():
#     htf_main()

# schedule.every().day.at("8:15").do(job)


# if __name__ == '__main__':
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


# # 分词 词云
# 需求
# - 基本功能
#     - 爬取所有基金的当天评论
#     - 写入excel
# - 程序优化
#     - 写入日志
#     - 定时任务
#     - 发送邮件
#     - 命令行执行
#     - 拆分成函数
#     - 写成类
# - 数据分析
#     - 简单统计分析
#     - 词云



# def main():
#     print(df)


# if __name__ == '__main__':
#     main()