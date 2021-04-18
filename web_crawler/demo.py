import requests
from lxml import etree # 导入支持xpath路径表达的包

# UA伪装，伪装成浏览器。
headers = {
    #'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
}

response = requests.get('https://www.bilibili.com/v/popular/rank/all', headers=headers)

t = etree.HTML(response.text) # 实例化并解析网页源码为一个对象

# 解析排名
rank_num = t.xpath('//ul[@class="rank-list"]/li/div[1]/text()')

# 解析视频名称
video_name = t.xpath('//ul[@class="rank-list"]/li/div[2]/div[2]/a/text()')

# 合并成字典
videos_dict = dict(zip(rank_num, video_name))

# 打印结果
for k in videos_dict:
    print(k, videos_dict[k])