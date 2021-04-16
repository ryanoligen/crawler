# 1.百度翻译

# import json
# import re
# import requests

# url = "https://fanyi.baidu.com/sug"
# word = input("你想翻译的单次：")
# dat = {'kw': word}

# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
# resp = requests.post(url, headers=headers, data=dat)
# ret = resp.text
# res = json.loads(ret)
# print(res)
# print(resp.json())



# # url = "https://fanyi.baidu.com/v2transapi"
# # post data需要定义token，sign，该接口暂时不可用

# # 有道翻译
# import requests

# url = "https://cn.bing.com/dict"



# # 2.豆瓣喜剧
# import requests

# url = "https://movie.douban.com/j/search_subjects"

# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}

# # movie_all = []
# movie_lst = []
# start = 0
# for i in range(10):
#     start = i * 20
#     params = {
#         "type": "movie",
#         "tag": "喜剧",
#         "sort": "recommend",
#         "page_limit": 20,
#         "page_start": start
#     }
#     resp = requests.get(url, params=params, headers=headers)
#     ret = resp.json()
#     # movie_all += [(item['title'], float(item['rate'])) for item in ret['subjects']]
#     movie_lst += [(item['title'], float(item['rate'])) for item in ret['subjects'] if float(item['rate']) >= 7.5]

# # print(movie_all)
# print(movie_lst)



# # 3.豆瓣250
# import re
# import requests
# import csv

# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}

# rexp = re.compile(r'<div class="info">.*?<span class="title">(?P<title>.*?)</span>.*?<br>(?P<year>.*?)&nbsp;.*?<span class="rating_num" property="v:average">(?P<rate>.*?)</span>.*?<span>(?P<population>.*?)</span>', re.S)


# with open('douban.csv', 'w', encoding='utf8') as f:
#     csvwriter = csv.writer(f)
#     for i in range(10):
#         page = i * 25
#         url = f"https://movie.douban.com/top250?start={page}"
#         resp = requests.get(url, headers=headers)
#         ret = rexp.finditer(resp.text)

#         for j in ret:
#             movie_dic = j.groupdict()
#             movie_lst = [j.strip() for j in movie_dic.values()]
#             # print(movie_lst)
#             csvwriter.writerow(tuple(movie_lst))
#         resp.close()



# 电影天堂


# # 新发地市场菜价
# import requests
# from bs4 import BeautifulSoup

# url = "http://www.xinfadi.com.cn/marketanalysis/0/list/1.shtml"

# resp = requests.get(url)

# res = BeautifulSoup(resp.text, "html.parser")
# ret = res.find(attrs={'class': 'hq_table'})
# vege_price = ret.find_all('tr')
# for i in vege_price:
#     elements = i.find_all('td')
#     lst = []
#     for j in elements:
#         lst.append(j.contents)
#     dic = dict(zip(['name', 'low', 'avg', 'high', 'type', 'size', 'date', 'apdx'], [lst]))
#     print(dic)



# 图片下载



# 曼联赛程

'''
1. bs 使用不熟练
2. 页面有类似于ajax的东西，需点击才能加载所有比赛，所以单次请求只能获取部分赛程
3. 请求的地址很奇怪，是get请求，为什么不是post，且get到的url看不懂
'''

# import requests
# from bs4 import BeautifulSoup

# # url = "https://dribbble.com/"

# url = "https://cn.bing.com/search?q=%E6%9B%BC%E8%81%94+%E8%B5%9B%E7%A8%8B&qs=n&form=QBRE&sp=-1&pq=%E6%9B%BC%E8%81%94+%E8%B5%9B%E7%A8%8B&sc=5-5&sk=&cvid=6FD5C6DAAD054B77A12502E9101B0FBA"

# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
# }

# resp = requests.get(url, headers=headers)
# bs_obj = BeautifulSoup(resp.text, "html.parser")

# match_table = bs_obj.find('div', attrs={'class': "spl-gameScoresScheduleContent"})
# # print(match_table)

# match_rows = match_table.find_all('tr')
# match_lst = []

# for row in match_rows:
#     # print(row)
#     teams = row.find_all('h3')
#     t_lst = [team.get_text() for team in teams]
#     # print(t_lst)
#     match_time = row.find(class_='spl-focusTextMid').get_text()
#     # print(match_time)
#     match = [t_lst[0], match_time, t_lst[-1]]
#     match_lst.append(match)

# print(match_lst)




# 天天基金
import re 
import time

import requests
from bs4 import BeautifulSoup

import pandas as pd

# import lxml
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

# 需求
# 1.爬取当天评论，所有基金下的
# 2.数据汇总，关键字匹配
# 3.发送邮件
# 4.定时任务
# 5.命令行执行
time_filter = time.strftime('%m-%d')

def get_comment(url, time_filter):
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
        if time_.split(' ')[0] < time_filter: # 过滤掉早于time_filter的评论
            break
        # 评论作者        
        author = comment.find(class_='l4').a.string
        if author == '基金资讯':  # 过滤掉基金资讯发表的评论（公告）
            continue
        # 评论内容
        content = comment.find('a').string
        comment_lst.append(dict(content=content, author=author, time_=time_))
    guba_resp.close()
    return comment_lst



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
    fund_name = fund.find(class_='name').string
    fund_code = fund.find(class_='code').string
    # 股吧url
    fund_guba = 'http:' + fund.find_all('a')[2].get('href').strip()  # 第三个a标签
    guba_resp = requests.get(fund_guba, headers=headers)
    # 获取股吧response headers，获取重定向url
    guba_url = guba_resp.history[-1].headers['location']
    guba_resp.close()
    comment = get_comment(guba_url, time_filter)
    if not comment: # 该基金当日有新的评论
        dic = {'fund_name':fund_name, 'fund_code':fund_code, 'comment':comment}
    print(dic)
resp.close()



    

# 每日2:50轮询 沪深300行情提醒 
# 跌幅大于2%，累计几天跌幅大于3%，邮件提醒



