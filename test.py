import requests
from lxml import etree

url = 'https://www.5tu.cn/colors/yansezhongwenming.html'
res = requests.get(url)
res.encoding = res.apparent_encoding

html = etree.HTML(res.text)

color_table = html.xpath('//table[@id="color"]/tbody/tr')

color_list = []
for tr in color_table[1:-1]:
    english_name = tr.xpath('./td[2]/text()')[0]
    chinese_name = tr.xpath('./td[3]/text()')[0]
    hex = tr.xpath('./td[4]/text()')[0]
    rgb = tr.xpath('./td[5]/text()')[0]
    print(english_name, chinese_name)
    color_list.append(dict(english_name=english_name, chinese_name=chinese_name,hex=hex, rgb=rgb))

print(color_list)