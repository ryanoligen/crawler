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




import os, sys
import re 
import time

import requests
from bs4 import BeautifulSoup

import pandas as pd

# import lxml
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


time_filter = time.strftime('%m-%d')

def get_comment(url, time_filter):
    '''抓取单只基金不晚于某个时间点的评论
    
    '''
    comment_lst = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    guba_resp = requests.get(url, headers=headers)
    guba_resp.encoding = 'utf8'
    page = BeautifulSoup(guba_resp.text, 'html.parser')

    # 定位到评论
    rexp = re.compile(r'articleh normal_post')
    comments = page.find(id="mainbody").find_all(class_=rexp)
    for comment in comments:
        # 评论时间
        time_ = comment.find(class_="l5").string
        if time_.split(' ')[0] != time_filter: # 过滤掉不是time_filter当天的评论
            break
        # 评论作者，如果作者没有超链接直接取string，否则取a.string  
        author = comment.find(class_='l4').a.string if comment.find(class_='l4').a else comment.find(class_='l4').string
        if author == '基金资讯':  # 过滤掉基金资讯发表的评论（公告）
            continue
        # 评论内容
        content = comment.find('a').string
        comment_lst.append(dict(content=content, author=author, time_=time_))
    guba_resp.close()
    return comment_lst


comments = []
# 抓取汇添富所有基金不晚于某一时间点的评论
url = 'http://fund.eastmoney.com/company/80053708.html'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}

resp = requests.get(url, headers=headers)
resp.encoding = 'utf8'
# 定位到开放式基金区域
htf_fund_table = BeautifulSoup(resp.text, 'html.parser').find(id="kfsFundNetWrap")
htf_fund_rows = htf_fund_table.tbody # .获取的是第一个匹配的标签，这里是第一个tbody标签
# 定位到股吧链接
htf_funds = htf_fund_rows.find_all('tr')
for fund in htf_funds:
    time.sleep(2)
    fund_name = fund.find(class_='name').string
    fund_code = fund.find(class_='code').string
    name_code = {'fund_name':fund_name, 'fund_code':fund_code}
    # 股吧url
    fund_guba = 'http:' + fund.find_all('a')[2].get('href').strip()  # 第三个a标签
    guba_resp = requests.get(fund_guba, headers=headers)
    # 获取股吧response headers，获取重定向url
    guba_url = guba_resp.history[-1].headers['location']
    # print(guba_url)
    guba_resp.close()
    comment = get_comment(guba_url, time_filter)
    if comment: # 该基金当日有新的评论，过滤掉无评论的基金
        # dic = {'fund_name':fund_name, 'fund_code':fund_code, 'comment':comment}
        com_lst = [{**name_code, **dic} for dic in comment] # 将名称代码字典和评论字典合并
        comments += com_lst
        # df.append(dic, ignore_index=True)
        # df_lst.append(dic)
resp.close()


# 数据处理

com_df = pd.DataFrame([dic.values() for dic in comments], columns=list(comments[0].keys()))

today = time.strftime('%y-%m-%d')
dir_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(dir_path, 'htf_fund_comment\\'+today+'.xlsx')
com_df.to_excel(file_path, index=False)




# def main():
#     print(df)


# if __name__ == '__main__':
#     main()