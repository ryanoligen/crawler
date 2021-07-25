# crawler

## xpath

- install lxml: `pip install lxml`
	- `pip install  -i  https://pypi.tuna.tsinghua.edu.cn/simple  lxml` [使用清华](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)

```python
import requests
from lxml import etree

# 解析xml文件
xml = '''.........'''
tree = etree.XML(xml)
result = tree.xpath('/book')  # /表示层级关系，第一个/表示根节点
result = tree.xpath('/book/name/text()') # 根节点>book>name>里面的文本内容

result = tree.xpath('/book/name/author//nick/text()')  # 获取author下面的子孙nick节点中的文本

result = tree.xpath('/book/name/author/*/nick/text()') # * 通配符


# 解析html文件
html = '''........'''
tree = etree.parse(html)

result = tree.xpath('/html/body/ul/li[1]/a/text()') # 第一个li中的文本
result = tree.xpath('/html/body/ul/li/a/@href/text()') # 链接中属性href的值
result = tree.xpath('/html/body/ul/li/a[@href='dapao']/text()') # 链接中属性href值为dapao的文本
sub = tree.xpath('html/body/ol')
result = sub.xpath('./li/a/text()') # xpath子对象，用相对路径
```

- tip：xpath路径可以在抓包工具中elemnts中复制到