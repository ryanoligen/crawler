import os, sys
import json

import requests

import bs4

# search = input('你想搜索的赛程:')
search = '曼联 2021 赛程'
url = 'https://cn.bing.com/search'

params = {'q':search}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'}
res = requests.get(url, params=params, headers=headers)

# print(res.text)
# print(res.status_code)
# with open('search_bing.html', 'w') as f:
    # f.write(res.text)

soup = bs4.BeautifulSoup(res.text, 'html.parser')

# 时间：第二周
# 主队：sa
# 时间：明天 9:00
# 客队：MU

match_row = soup.find_all('div', attrs='spl-matchRowTitle b_sectxt')

sched = []


for match in match_row:
    game = {}
    game['round'] = match.string
    host = match.find_next('h3')
    date = match.find_next(attrs='spl-focusTextMid')
    tmp = date.find_next(attrs='spl-focusTextMid')
    time = tmp.find_next(attrs='spl-focusTextMid')
    guest = time.find_next('h3')
    game['match'] = host.string + ' ' + date.string + ' ' + time.string + ' ' + guest.string
    sched.append(game)

with open('manutd-match-sched', 'w') as f:
    json.dump(sched, f)
    


